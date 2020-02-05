import yaml
import os
import requests
from bronze.libs.google.docs import spreadsheet as ss
from bronze.libs import slack
import pandas as pd


class Alarm:
    SLACK_MSG_HEADER = {'Content-type': 'application/json'}

    def __init__(self, alarm='alarm.yml'):
        """Initialization, path to the YAML is required."""
        with open(alarm, 'r') as fp:
            self.core = yaml.load(fp, Loader=yaml.FullLoader)

    # def send_msg(self, msg):
    #     """Send the composed message to the slack_target."""
    #     response = requests.post(
    #         url=self.slack_target, headers=self.SLACK_MSG_HEADER, json={'text': msg}
    #     )
    #     response.raise_for_status()
    #     return response.text

    @property
    def message(self):
        """Helper property, get the raw message from the YAML."""
        return self.core.get('message')

    # @property
    # def slack_target(self):
    #     """Get the targeting Slack webhook URL, the message will be sent there."""
    #     slack_var = self.core.get('slack_channel_target_var')
    #     if not slack_var:
    #         raise ValueError('Slack channel undefined, please double check the YAML!')
    #     else:
    #         slack = os.environ.get(slack_var)
    #         if not slack:
    #             # TODO: send an email to the maintainers or ping a fixed Slack channel
    #             raise ValueError(
    #                 f'No Slack channel is provided, please double check your environment var: {slack_var}!'
    #             )
    #     return slack

    # @property
    # def sheet_target(self):
    #     """Get the targeting Google Spreadsheet URL, the alarm can optionally read from it."""
    #     sheet_var = self.core.get('spreadsheet_target_var')
    #     if not sheet_var:
    #         print('No Spreadsheet available for this alarm.')
    #         return None
    #     else:
    #         sheet = os.environ.get(sheet_var)
    #         if not sheet:
    #             # TODO: send an email to the maintainers or ping a fixed Slack channel
    #             raise ValueError(
    #                 f'No Spreadsheet is provided, please double check your environment var: {sheet_var}!'
    #             )
    #     return sheet

    # @property
    # def creds_target(self):
    #     """Get the targeting credentials path or file name. The alarm will need it to read from the spreadsheet."""
    #     creds_var = self.core.get('credentials_target_var')
    #     if not creds_var:
    #         print(
    #             'No Credentials available for this alarm. Be sure your spreadsheet is publicly available!'
    #         )
    #         return None
    #     else:
    #         creds = os.environ.get(creds_var)
    #         if not creds:
    #             # TODO: send an email to the maintainers or ping a fixed Slack channel
    #             raise ValueError(
    #                 f'No Credentials is provided, please double check your environment var: {creds_var}!'
    #             )
    #     return creds


# def get_slack_mapping(
#     spreadsheet: ss.SpreadSheetReader, remove_header: bool = True
# ) -> dict:
#     """Load the `SlackIDs` sheet and construct a name -> slackID mapping dict."""
#     slack_user_mapping_list = spreadsheet.getSheet(sheet_name='SlackIDs', values=True)
#     if remove_header:
#         slack_user_mapping_list.pop(0)  # remove the header
#     return {
#         array[0]: slack.User(slack_id=array[1]) for array in slack_user_mapping_list
#     }  # ignore the 3rd column: comments


# def load_cell_from_row(column_name: str, row: pd.DataFrame) -> str:
#     """Extract the value of a cell based on the column_name the row that cell lives.
#
#     An example row could be:
#
#     Date Coordinator
#     Aug 08, 2018       PersonA
#     """
#     cell = row[column_name].tolist()
#     if len(cell) != 1:
#         raise ValueError(
#             f"Failed to find exact-match values: {cell} for {column_name}, there's something wrong with the spreadsheet, please double check!"
#         )
#     return cell[0]
