import re
import sys
import logging
from tenacity import retry, stop_after_attempt
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

__all__ = ['SpreadSheetBase', 'SpreadSheetReader']


logger = logging.getLogger('DCP-ALARM.{module_path}'.format(module_path=__name__))


class SpreadSheetBase(object):
    def __init__(self, SCOPES='', oauth_secret='', sheetsAPIVersion='v4'):
        self._SCOPES = SCOPES

        if not self._check_file('credentials.json'):
            logger.warning('Missing credentials file: credentials.json')
        cred_store = file.Storage('credentials.json')
        credentials = cred_store.get()

        if not credentials or credentials.invalid:
            logger.info('Failed to load from credentials, redirecting to Google OAuth Page.')

            if not self._check_file(oauth_secret):
                raise FileNotFoundError('Missing OAuth Secret file: {} !'.format(oauth_secret))
            flow = client.flow_from_clientsecrets(oauth_secret, self._SCOPES)
            credentials = tools.run_flow(flow, cred_store)

        self._service = build('sheets', sheetsAPIVersion, http=credentials.authorize(Http()))

    @staticmethod
    def _check_file(path_to_file):
        if sys.version_info < (3, 4):
            import os
            return os.path.isfile(path_to_file)
        else:
            from pathlib import Path
            return Path(path_to_file).is_file()

    @property
    def service(self):
        return self._service


class SpreadSheetReader(SpreadSheetBase):

    def __init__(self, spreadsheet_url, oauth_secret=''):
        super(SpreadSheetReader, self).__init__(SCOPES='https://www.googleapis.com/auth/spreadsheets.readonly',
                                                oauth_secret=oauth_secret)
        self.spreadsheet_url = spreadsheet_url

        try:
            self.spreadsheet_id = re.findall('/spreadsheets/d/([a-zA-Z0-9-_]+)', self.spreadsheet_url)[0]
        except IndexError:
            raise ValueError('Invalid Google Docs SPREADSHEET_URL is provided!')

    @retry(stop=stop_after_attempt(5))
    def loadSheet(self, sheet_name, sheet_range='A1:Z1000'):
        sheet = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range='{0}!{1}'.format(sheet_name, sheet_range)
        ).execute()
        return sheet

    @staticmethod
    def getRows(sheet):
        if not isinstance(sheet, dict):
            raise TypeError('Input must be a valid sheet dictionary!')
        return sheet.get('values', [])
