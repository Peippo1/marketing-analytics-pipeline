import gspread
from google.oauth2.service_account import Credentials

def sync_to_google_sheets(df, sheet_name, credentials_dict):
    creds = Credentials.from_service_account_info(credentials_dict)
    client = gspread.authorize(creds)

    try:
        sheet = client.open(sheet_name).sheet1
    except gspread.SpreadsheetNotFound:
        sheet = client.create(sheet_name).sheet1

    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    return True