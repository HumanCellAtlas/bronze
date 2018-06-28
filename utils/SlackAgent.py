import arrow
import requests
import copy
import logging
from tenacity import retry, retry_if_result, stop_after_attempt
import sys


logger = logging.getLogger('DCP-ALARM.{module_path}'.format(module_path=__name__))


__all__ = ['SlackAlarm', 'SlackUser', 'SlackMsg', 'SlackUserGroupView', 'getSlackTag']


class SlackBase(object):
    SLACK_MSG_CONTENT = {'text': None}
    SLACK_MSG_HEADER = {'Content-type': 'application/json'}


def is_failed_ring(response):
    return not 200 <= response.status_code < 300


def getSlackTag(slackId):
    return '<@{id}>'.format(id=slackId)


class SlackAlarm(SlackBase):
    def __init__(self, webhook_url, func, sheet):
        self.webhook_url = webhook_url
        self.msg = func(sheet)

    @retry(retry=retry_if_result(is_failed_ring), stop=stop_after_attempt(5))
    def ring(self):
        response = requests.post(url=self.webhook_url,
                                 headers=self.SLACK_MSG_HEADER,
                                 json=self.msg)
        logger.info(response.text)
        logger.info('Successfully notified target group of users via Slack at {}'.format(arrow.utcnow()))
        return response


class SlackUser(SlackBase):
    def __init__(self, displayName, slackId, **kwargs):
        self._displayName = displayName
        self._slackId = slackId
        for k, v in kwargs.items():
            setattr(self, k, v)

    def has_valid_slackId(self):
        return len(self.slackId) == 9 and self.slackId.startswith('U')

    def has_valid_displayName(self):
        return self.displayName != ''

    @property
    def displayName(self):
        return self._displayName

    @property
    def slackId(self):
        return self._slackId

    @property
    def tag(self):
        return getSlackTag(slackId=self.slackId)

    def __eq__(self, other):
        if isinstance(other, SlackUser):
            return self.slackId == other.slackId
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str((self.displayName, self.slackId))

    def __repr__(self):
        return str((self.displayName, self.slackId))

    def __hash__(self):
        return hash(tuple(self.__dict__.items()))


class SlackUserGroupView(object):
    def __init__(self, *args):
        if sys.version_info.major < 3 and isinstance(args[0], list):
            self._group = {user for user in args[0] if
                           isinstance(user, SlackUser) and user.has_valid_displayName() and user.has_valid_slackId()}
        else:
            self._group = {user for user in args if
                           isinstance(user, SlackUser) and user.has_valid_displayName() and user.has_valid_slackId()}

    @property
    def group(self):
        return self._group

    def getSlackIdbyDisplayName(self, displayName):
        for user in self.group:
            if user.displayName == displayName:
                return user.slackId

    def getDisplayNamebySlackId(self, slackId):
        for user in self.group:
            if user.slackId == slackId:
                return user.displayName


class SlackMsg(SlackBase):
    def __init__(self, msg):
        self._msg = msg

    def extend_msg(self, *extra_msgs):
        for extra_msg in extra_msgs:
            self._msg += '{0}'.format(extra_msg)

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self.content)

    @property
    def content(self):
        return self._assemble_msg()

    def _assemble_msg(self):
        assembled_msg = copy.deepcopy(self.SLACK_MSG_CONTENT)
        assembled_msg['text'] = str(self._msg)
        return assembled_msg
