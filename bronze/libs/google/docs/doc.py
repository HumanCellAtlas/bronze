from bronze.libs.google.docs import GoogleDocsScopes
from bronze.libs.google import APIVersions, GoogleBase
from typing import Union
import re


def getDocId(document_identifier: str):
    if document_identifier.startswith('http'):
        try:
            return re.findall('/document/d/([a-zA-Z0-9-_]+)', document_identifier)[0]
        except IndexError:
            raise ValueError(f'Invalid document URL {document_identifier}!')
    else:
        # Assume this is already the document id
        return document_identifier


class DocReader(GoogleBase):
    """Read docs through Google Docs API."""

    SCOPES = GoogleDocsScopes.readonly.value
    DOCS_API = APIVersions.docs.name
    DOCS_API_VERSION = APIVersions.docs.value

    def __init__(self, service_account_key: Union[str, dict]):
        super().__init__(
            service_account_key=service_account_key,
            scopes=self.SCOPES,
            api=self.DOCS_API,
            api_version=self.DOCS_API_VERSION,
        )


class DocAdmin(GoogleBase):
    """Read, edit, create and delete docs through Google Docs API."""

    SCOPES = GoogleDocsScopes.full_access.value
    DOCS_API = APIVersions.docs.name
    DOCS_API_VERSION = APIVersions.docs.value

    def __init__(self, service_account_key: Union[str, dict]):
        super().__init__(
            service_account_key=service_account_key,
            scopes=self.SCOPES,
            api=self.DOCS_API,
            api_version=self.DOCS_API_VERSION,
        )

    def getDocument(self, document_identifier: str) -> dict:
        doc = self.service.documents().get(
            documentId=getDocId(document_identifier=document_identifier)
        )
        return doc.to_json()

    def updateDocument(self, document_identifier: str, update_requests: list) -> dict:
        result = (
            self.service.documents()
            .batchUpdate(
                documentId=getDocId(document_identifier=document_identifier),
                body={'requests': update_requests},
            )
            .execute()
        )
        return result
