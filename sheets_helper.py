from googleapiclient.discovery import build
from google.oauth2 import service_account

file_json = 'credentials.json'


def extract_spreadsheet_id(url):
    return url.split("/d/")[1].split("/")[0]


def read_google_sheet(spreadsheet_id, range_name):
    creds = service_account.Credentials.from_service_account_file(file_json)
    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values


def update_google_sheet(spreadsheet_id, range_name, value):
    creds = service_account.Credentials.from_service_account_file(file_json)
    service = build('sheets', 'v4', credentials=creds)

    body = {
        'values': [[value]]
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
