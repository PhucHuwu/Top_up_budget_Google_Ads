import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from sheets_helper import extract_spreadsheet_id, read_google_sheet, update_google_sheet
import click
import config


spreadsheet_url = "https://docs.google.com/spreadsheets/d/1cHm4-a_2DtZlOHwt9nfPy1e1wCAORwGplJy8tkIqMWw/edit?usp=sharing"

spreadsheet_id = extract_spreadsheet_id(spreadsheet_url)

range_name = "Sheet1!A1:Z"


def Row():
    data = read_google_sheet(spreadsheet_id, range_name)

    for row in data[1:]:
        if row[8].strip() == "":
            if row[5] == "NẠP":
                return row


def Done():
    data = read_google_sheet(spreadsheet_id, range_name)

    for index, row in enumerate(data[1:], start=2):
        if row[8].strip() == "":
            if row[5] == "NẠP":
                update_range = f"Sheet1!I{index}"
                update_google_sheet(spreadsheet_id, update_range, "Đã Nạp")
                return
            else:
                update_range = f"Sheet1!I{index}"
                update_google_sheet(spreadsheet_id, update_range, "Đã Rút")
                return


options = uc.ChromeOptions()

profile_directory = f"Profile"
if not os.path.exists(profile_directory):
    os.makedirs(profile_directory)
options.user_data_dir = profile_directory

driver = uc.Chrome(options=options)

driver.maximize_window()

driver.get("https://ads.google.com/aw/overview")

account_id = "974-884-2844"  # input("Vui lòng nhập id: ")

if (account_id):
    while True:
        row = Row()
        if row != None:
            customer_id = row[1]
            id = row[2]
            request = row[5]
            top_up = row[7]
            money_request = row[3]
            money_left = row[13]
            if request == "NẠP" and money_request <= money_left:
                driver.get("https://ads.google.com/aw/overview")

                try:
                    click.auto_click(driver, "//span[text()='" + account_id + "']", 30)
                except Exception:
                    print(f"Lỗi 1")
                    print()
                    continue
                time.sleep(5)

                try:
                    click.auto_click(driver, config.arrow_drop_down_button_xpath, 30)
                except Exception:
                    print(f"Lỗi 2")
                    print()
                    continue
                time.sleep(3)

                try:
                    click.auto_click(driver, config.search_button_xpath, 30)
                except Exception:
                    print(f"Lỗi 3")
                    print()
                    continue

                ActionChains(driver).send_keys(f"{id}").perform()
                time.sleep(3)

                try:
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'customer-title')]")))
                    link_element = driver.find_element(By.XPATH, "//a[contains(@class, 'customer-title')]")
                    href = link_element.get_attribute("href")
                    driver.get(href)

                except Exception as e:
                    print(f"Lỗi: {e}")
                time.sleep(5)

                try:
                    click.auto_click(driver, config.pay_button_xpath, 30)
                except Exception:
                    print(f"Lỗi 5")
                    print()
                    continue

                try:
                    click.auto_click(driver, config.account_budget_button_xpath, 30)
                except Exception:
                    print(f"Lỗi 6")
                    print()
                    continue
                time.sleep(10)

                try:
                    element = driver.find_element(By.XPATH, "//material-button//span[contains(text(), 'Chỉnh sửa')]")
                    driver.execute_script("arguments[0].click();", element)
                except Exception:
                    print(f"Lỗi 7")
                    print()
                    continue
                time.sleep(5)

                try:
                    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "input-area")))
                    input_areas = driver.find_elements(By.CLASS_NAME, "input-area")
                    if len(input_areas) > 1:
                        driver.execute_script("arguments[0].value = '';", input_areas[1])
                        input_areas[1].send_keys(f'{top_up}')
                    else:
                        time.sleep(5)
                        driver.execute_script("arguments[0].value = '';", input_areas[1])
                        input_areas[1].send_keys(f'{top_up}')
                except Exception:
                    print(f"Lỗi 8")
                    continue

                try:
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "material-button.btn.btn-yes")))
                    save_button = driver.find_element(By.CSS_SELECTOR, "material-button.btn.btn-yes")
                    save_button.click()
                except Exception:
                    print(f"Lỗi 9")
                    print()
                    continue
                
                Done()
                print(f"Đã nạp xong cho tài khoản {customer_id}: {id}")
                
                time.sleep(10)