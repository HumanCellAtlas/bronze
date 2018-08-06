import logging
import apiclient.discovery
from httplib2 import Http
from oauth2client import file, client, tools
from pathlib import Path
import re
from tenacity import retry, stop_after_attempt

from google.oauth2 import service_account


__all__ = ['GoogleSheetBase', 'GoogleSpreadSheetReader']


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Bronze.{module_path}'.format(module_path=__name__))


class AuthError(Exception): pass


class GoogleSheetBase(object):
    def __init__(self, credentials_json=None, scopes='', oauth_secret='', sheetsAPIVersion='v4'):
        self._service = self._authenticate_with_Google(
            credentials_json, scopes, oauth_secret, sheetsAPIVersion
        )

    @staticmethod
    def _check_file(path_to_file):
        return Path(path_to_file).is_file()

    def _authenticate_with_Google(self, service_accounts_json, scopes, oauth_secret, sheetsAPIVersion):
        if service_accounts_json:  # authenticate with service account credentials from JSON string stream
            credentials = service_account.Credentials.from_service_account_info(service_accounts_json, scopes=[scopes])
            return apiclient.discovery.build('sheets', sheetsAPIVersion, credentials=credentials)
        else:
            if not self._check_file('credentials.json'):
                logger.warning('Missing credentials file: credentials.json')
            cred_store = file.Storage('credentials.json')  # authenticate with credentials.json
            credentials = cred_store.get()

        if not credentials or getattr(credentials, 'invalid', None):
            logger.info('Failed to load from credentials, redirecting to Google OAuth Page.')

            if not self._check_file(oauth_secret):
                raise IOError('Missing OAuth Secret file: {} !'.format(oauth_secret))
            flow = client.flow_from_clientsecrets(oauth_secret, scopes)   # authenticate through OAuth
            credentials = tools.run_flow(flow, cred_store)

        if not credentials or getattr(credentials, 'invalid', None):
            raise AuthError('Failed to authenticate with Google Sheets API!!')

        return apiclient.discovery.build('sheets', sheetsAPIVersion, http=credentials.authorize(Http()))

    @property
    def service(self):
        return self._service


class GoogleSpreadSheetReader(GoogleSheetBase):
    def __init__(self, spreadsheet_url, service_accounts_json=None, oauth_secret='', sheetsAPIVersion='v4'):
        super(GoogleSpreadSheetReader, self).__init__(
            credentials_json=service_accounts_json,
            scopes='https://www.googleapis.com/auth/spreadsheets.readonly',
            oauth_secret=oauth_secret,
            sheetsAPIVersion=sheetsAPIVersion
        )
        self.spreadsheet_url = spreadsheet_url
        self.spreadsheet_id = self.get_sheet_id(self.spreadsheet_url)

    @staticmethod
    def getRows(sheet):
        if not isinstance(sheet, dict):
            raise TypeError('Input must be a valid sheet dictionary!')
        return sheet.get('values', [])

    @staticmethod
    def get_sheet_id(spreadsheet_url):
        try:
            return re.findall('/spreadsheets/d/([a-zA-Z0-9-_]+)', spreadsheet_url)[0]
        except IndexError:
            raise ValueError('Invalid Google Docs SPREADSHEET_URL is provided!')

    @retry(stop=stop_after_attempt(5), reraise=True)
    def loadSheet(self, sheet_name, sheet_range='A1:Z1000'):
        sheet = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range='{0}!{1}'.format(sheet_name, sheet_range)
        ).execute()
        return sheet
