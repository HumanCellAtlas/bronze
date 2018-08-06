import os
from libs import SlackAgent
from libs import DefaultAlarm
from libs import cryptor
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Bronze.{module_path}'.format(module_path=__name__))


class DCP_DEMO_PM_ALARM(DefaultAlarm.DefaultAlarm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def prepare_message(current_row, notify_group):
        message = SlackAgent.SlackMessage(':wave: Hello @here! There is a DCP demo tomorrow *{date}*. The demo coordinator this week is {coordinator}. The *{team}* team is first.\n'.format(date=current_row[0], coordinator=notify_group.getSlackUserByName(current_row[1]).tagSlackName, team=current_row[2]))
        message.extend_msg('\n', '*This message serves as a reminder to all PMs to update the demo agenda here:* https://goo.gl/VwCSo2 \n')
        message.extend_msg('\n', 'The demo coordinator is responsible for:')
        message.extend_msg('\n', '1. Making sure folks add to the agenda')
        message.extend_msg('\n', '2. Ensuring the agenda time boxes to 1 hour')
        message.extend_msg('\n', '3. Leading the demo meeting (order of teams, keeping it moving, asking for questions, sticking to time boxes)')
        message.extend_msg('\n', '4. Sending a summary of the demo in the #dcp-meeting-digest channel\n')
        message.extend_msg('\n', '* If you are not able to be demo coordinator, please find a replacement. The schedule is here:* https://goo.gl/VbXRTj \n')
        return message.msg


if __name__ == '__main__':
    # Load credentials from environment variables
    slack_target = os.environ.get('DCP_DEMO_PM_SLACK_TARGET')
    sheet_target = os.environ.get('DCP_DEMO_PM_SHEET_TARGET')
    google_service_account_credentials = cryptor.decrypt_from_environment_variable_with_base64(
        os.environ.get('GOOGLE_SERVICE_ACCOUNT_VIEWER')
    )

    # Create the alarm instance, using the 'service_account' AuthN method to contact Google G-suite
    alarm = DCP_DEMO_PM_ALARM(
        slack_target=slack_target,
        sheet_target=sheet_target,
        service_accounts_json=google_service_account_credentials
    )

    alarm.alert()
