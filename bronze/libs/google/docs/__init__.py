from enum import Enum


class GoogleSheetsScopes(Enum):
    """Google Sheets API scopes."""

    readonly = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    full_access = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleDocsScopes(Enum):
    """Google Docs API scopes."""

    readonly = ['https://www.googleapis.com/auth/documents.readonly']
    full_access = ['https://www.googleapis.com/auth/documents']
