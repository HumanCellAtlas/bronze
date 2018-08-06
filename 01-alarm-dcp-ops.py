import os
from libs import SlackAgent
from libs import DefaultAlarm
from libs import cryptor
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Bronze.{module_path}'.format(module_path=__name__))


class DCP_OPS_ALARM(DefaultAlarm.DefaultAlarm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def prepare_message(current_row, notify_group):
        DCP_BOX_PREFIX = {
            0: 'Week Of',
            1: '*DCP*',
            2: '*Metadata*',
            3: '*Purple*',
            4: '*Upload*',
            5: '*Blue*',
            6: '*Green*',
            7: '*Orange*'
        }

        message = SlackAgent.SlackMessage('*DCP OPS Reminder Week of: {0}*'.format(current_row[0]))
        message.extend_msg('\n', 'This week\'s release operation schedule:')
        for idx, slackName in enumerate(current_row):
            if idx == 0:
                continue  # skip the first column
            message.extend_msg(
                '\n', '- ', '{box_prefix} Release Engineer: {engineer_name}'.format(
                    box_prefix=DCP_BOX_PREFIX.get(idx),
                    engineer_name=notify_group.getSlackUserByName(slackName).tagSlackName
                )
            )
        return message.msg


if __name__ == '__main__':
    # Load credentials from environment variables
    slack_target = os.environ.get('DCP_OPS_SLACK_TARGET')
    sheet_target = os.environ.get('DCP_OPS_SHEET_TARGET')
    google_service_account_credentials = cryptor.decrypt_from_environment_variable_with_base64(
        os.environ.get('GOOGLE_SERVICE_ACCOUNT_VIEWER')
    )

    # Create the alarm instance, using the 'service_account' AuthN method to contact Google G-suite
    alarm = DCP_OPS_ALARM(
        slack_target=slack_target,
        sheet_target=sheet_target,
        service_accounts_json=google_service_account_credentials
    )

    alarm.alert()
