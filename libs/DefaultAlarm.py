import arrow
import logging
import requests
from tenacity import retry, retry_if_result, stop_after_attempt
from libs import SlackAgent
from libs import SheetAgent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Bronze.{module_path}'.format(module_path=__name__))


def request_is_failed(response):
    return not 200 <= response.status_code < 300


class DefaultAlarm(object):
    def __init__(self, slack_target, sheet_target, **kwargs):
        self.slack_webhook = slack_target
        self.sheet_target = sheet_target
        self.kwargs = kwargs
        self.name_id_mapping_sheet_name = 'User IDs'
        self.schedule_sheet = 'Rotation'

        # override the default prepare_message to custom the alarm
        self.message = self.prepare_message(*self.get_message_meta())

    @staticmethod
    def prepare_message(current_row, notify_group):
        return NotImplemented

    def get_message_meta(self):
        """
        Returns the required information for creating a message.

        Returns:
            current_row (list)
            notify_group (SlackAgent.SlackUserGroup)
        """
        sheets = SheetAgent.GoogleSpreadSheetReader(
            spreadsheet_url=self.sheet_target,
            **self.kwargs
        )
        user_mapping_sheet = sheets.loadSheet(self.name_id_mapping_sheet_name)
        schedule_sheet = sheets.loadSheet(self.schedule_sheet)

        user_info = SheetAgent.GoogleSpreadSheetReader.getRows(user_mapping_sheet)
        schedule_info = SheetAgent.GoogleSpreadSheetReader.getRows(schedule_sheet)

        notify_group = SlackAgent.SlackUserGroup(
            *[SlackAgent.SlackUser(user[0], user[1]) for user in user_info if len(user) == 2]
        )

        notify_schedule = self.getTodaySchedule(schedule_info)

        return notify_schedule, notify_group

    @staticmethod
    def getTodaySchedule(schedule_info):
        """
        This will return the row should be notified, based on today's date.
        Args:
            schedule_info (list): A sheet-like list, whose first column contains dates in a format 'MMM D, YYYY'

        Returns:
            The row selected to be notified, based on today's date.
        """
        today = arrow.get(arrow.utcnow().date())

        for idx, schedule in enumerate(schedule_info):
            # skip the header
            if idx == 0:
                continue

            scheduledDayInCurrentRow = arrow.get(schedule[0], 'MMM D, YYYY')

            # this checks if today is way earlier than the first date in the schedule
            # this usually happens if you create and deploy this alarm war earlier before
            # your first scheduled day
            # Note: idx == 1 is redundant here in the loop, leave it here just for readability
            if idx == 1 and today <= scheduledDayInCurrentRow:
                return schedule

            try:
                next_scheduledDayInRow = arrow.get(schedule_info[idx + 1][0], 'MMM D, YYYY')
                day_before_next_scheduledDayInCurrentRow = next_scheduledDayInRow.shift(days=-1)
            except IndexError:
                logger.warning('Reached the last row in the schedule, returning the last row!')
                return schedule

            if today in arrow.Arrow.range('day', scheduledDayInCurrentRow, day_before_next_scheduledDayInCurrentRow):
                return schedule
        raise ValueError('Failed to find the release plan!')

    @retry(retry=retry_if_result(request_is_failed), stop=stop_after_attempt(5))
    def alert(self):
        response = requests.post(
            url=self.slack_webhook,
            headers=SlackAgent.MessageBase.SLACK_MSG_HEADER,
            json=self.message
        )

        logger.info(response.text)

        if not request_is_failed(response):
            logger.info('Successfully notified target group of users via Slack at {}'.format(arrow.utcnow()))
        return response

    # @retry(retry=retry_if_result(request_is_failed), stop=stop_after_attempt(5))
    def setTopic(self):
        """Placeholder, require a bot user in Slack rather than a simple webhook."""
        return NotImplemented

