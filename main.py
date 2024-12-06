import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from sheets_helper import extract_spreadsheet_id, read_google_sheet, update_google_sheet

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1cHm4-a_2DtZlOHwt9nfPy1e1wCAORwGplJy8tkIqMWw/edit?usp=sharing"

spreadsheet_id = extract_spreadsheet_id(spreadsheet_url)

range_name = "Sheet1!A1:Z"


def Row():
    data = read_google_sheet(spreadsheet_id, range_name)

    for index, row in enumerate(data[1:], start=2):
        if row[8].strip() == "" and row[5] == "NẠP":

            update_range = f"Sheet1!I{index}"
            update_google_sheet(spreadsheet_id, update_range, "Đã Nạp")

        else:
            continue
        
        return row


options = uc.ChromeOptions()

profile_directory = f"Profile"
if not os.path.exists(profile_directory):
    os.makedirs(profile_directory)
options.user_data_dir = profile_directory

driver = uc.Chrome(options=options)

driver.maximize_window()

driver.get("https://www.google.com/")

# while True:
row = Row()
if row != None:
    ActionChains(driver).send_keys(f"{row}").perform()
    print(f"Đã nạp thành công cho tài khoản {row[1]}")
time.sleep(1000)
