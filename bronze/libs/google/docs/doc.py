from bronze.libs.google.docs import GoogleDocuments, GoogleDocsScopes, APIVersions
from typing import Union


class DocReader(GoogleDocuments):
    """Read docs through Google Docs API."""

    SCOPES = GoogleDocsScopes.readonly.value
    DOCS_API_VERSION = APIVersions.docs.value

    def __init__(self, service_account_key: Union[str, dict]):
        super().__init__(
            service_account_key=service_account_key,
            scopes=self.SCOPES,
            api_version=self.DOCS_API_VERSION,
        )


class DocAdmin(GoogleDocuments):
    """Read, edit, create and delete docs through Google Docs API."""

    SCOPES = GoogleDocsScopes.full_access.value
    DOCS_API_VERSION = APIVersions.docs.value

    def __init__(self, service_account_key: Union[str, dict]):
        super().__init__(
            service_account_key=service_account_key,
            scopes=self.SCOPES,
            api_version=self.DOCS_API_VERSION,
        )
