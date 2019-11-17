import re
import pandas as pd
from typing import Union, List
from bronze.libs.google.docs import GoogleDocuments, GoogleSheetsScopes, APIVersions


def getSpreadSheetId(spreadsheet_url: str):
    try:
        return re.findall('/spreadsheets/d/([a-zA-Z0-9-_]+)', spreadsheet_url)[0]
    except IndexError:
        raise ValueError(f'Invalid spreadsheet URL {spreadsheet_url}!')


class SpreadSheetReader(GoogleDocuments):
    """Read spreadsheets through Google Sheets API."""

    SCOPES = GoogleSheetsScopes.readonly.value
    SHEETS_API_VERSION = APIVersions.sheets.value

    def __init__(self, service_account_key: Union[str, dict], spreadsheet_url: str):
        super().__init__(
            service_account_key=service_account_key,
            scopes=self.SCOPES,
            api_version=self.SHEETS_API_VERSION,
        )
        self.spreadsheet_url = spreadsheet_url
        self.spreadsheet_id = getSpreadSheetId(self.spreadsheet_url)

    def getSheet(self, sheet_name, sheet_range='A1:Z1000', values=True) -> dict:
        sheet = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=f'{sheet_name}!{sheet_range}')
            .execute()
        )
        if values:
            return sheet.get('values')
        else:
            return sheet

    def sheetToDataFrame(
        self, sheet_name, sheet_range='A1:Z1000', has_header=True
    ) -> pd.DataFrame:
        sheet = self.getSheet(sheet_name, sheet_range, True)
        if has_header:
            headers = sheet.pop(0)
            return pd.DataFrame(sheet, columns=headers)
        else:
            return pd.DataFrame(sheet)

    def sheetFromDataFrame(self, data_frame, has_header=True) -> List[List]:
        if has_header:
            headers = data_frame.columns.values.tolist()
            values = data_frame.values.tolist()
            values.insert(0, headers)
            return values
        else:
            return data_frame.values.tolist()


class SpreadSheetAdmin(GoogleDocuments):
    """Read, edit, create and delete spreadsheets through Google Sheets API."""

    SCOPES = GoogleSheetsScopes.full_access.value
    SHEETS_API_VERSION = APIVersions.sheets.value

    def __init__(self, service_account_key: Union[str, dict], spreadsheet_url: str):
        super().__init__(
            service_account_key=service_account_key,
            scopes=self.SCOPES,
            api_version=self.SHEETS_API_VERSION,
        )
        self.spreadsheet_url = spreadsheet_url
        self.spreadsheet_id = getSpreadSheetId(self.spreadsheet_url)
