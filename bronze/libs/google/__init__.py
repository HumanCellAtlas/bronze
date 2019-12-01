from google.oauth2 import service_account
from googleapiclient import discovery
from pathlib import Path
from enum import Enum
from typing import Union, List
from bronze.libs import cryptor


class APIVersions(Enum):
    """Google Documents and Drive API versions."""

    sheets = 'v4'
    docs = 'v1'
    drive = 'v3'


class GoogleBase:
    """Base class for working with Google Common Product APIs, such as Drive, Sheets or Docs."""

    def __init__(
        self,
        service_account_key: Union[str, dict],
        scopes: List[str],
        api: str,
        api_version: str,
    ):
        self.service = self.authenticate(service_account_key, scopes, api, api_version)

    def authenticate(
        self,
        service_account_key: Union[str, dict],
        scopes: List[str],
        api: str,
        api_version: str,
    ):
        valid_api = (
            APIVersions.docs.name,
            APIVersions.sheets.name,
            APIVersions.drive.name,
        )
        creds = None
        if not creds or not creds.valid:
            if isinstance(service_account_key, str):
                try:
                    if Path(service_account_key).is_file():
                        creds = service_account.Credentials.from_service_account_file(
                            service_account_key, scopes=scopes
                        )
                    else:
                        service_account_key = cryptor.decrypt_from_environment_variable_with_base64(
                            base64string=service_account_key
                        )
                # Sometimes the base64 string is too long to be detected by the pathlib
                except OSError:
                    service_account_key = cryptor.decrypt_from_environment_variable_with_base64(
                        base64string=service_account_key
                    )
            if isinstance(service_account_key, dict):
                creds = service_account.Credentials.from_service_account_info(
                    service_account_key, scopes=scopes
                )

        if api not in valid_api:
            raise ValueError(f'api must be one of {valid_api}!')
        return discovery.build(api, api_version, credentials=creds)
