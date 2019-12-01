from bronze.libs.google import APIVersions, GoogleBase
from enum import Enum
from bronze.libs.google.docs import doc as gdoc
from typing import Union


class GoogleDriveScopes(Enum):
    """Google Drive API scopes."""

    full_access = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.file',
    ]


class DriveAdmin(GoogleBase):
    """Read, edit, create and delete files through Google Drive API."""

    SCOPES = GoogleDriveScopes.full_access.value
    DRIVE_API = APIVersions.drive.name
    DRIVE_API_VERSION = APIVersions.drive.value

    def __init__(self, service_account_key: Union[str, dict]):
        super().__init__(
            service_account_key=service_account_key,
            scopes=self.SCOPES,
            api=self.DRIVE_API,
            api_version=self.DRIVE_API_VERSION,
        )

    def duplicateDocument(
        self, document_url, copy_title: str = None, raise_for_status: bool = True
    ):
        """Create a copy of the template using files.copy in the Drive API.

        See https://developers.google.com/drive/api/v2/reference/files/copy#examples_1
        """
        original_file_id = gdoc.getDocId(document_identifier=document_url)
        if copy_title:
            copied_file = {'name': copy_title}
            result_file = (
                self.service.files()
                .copy(fileId=original_file_id, body=copied_file)
                .execute()
            )
        else:
            result_file = self.service.files().copy(fileId=original_file_id).execute()
        return result_file
