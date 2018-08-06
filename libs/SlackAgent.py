import copy
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Bronze.{module_path}'.format(module_path=__name__))


__all__ = ['SlackUser', 'SlackUserGroup', 'SlackMessage']


class SlackUser(object):
    def __init__(self, slackName, slackId, **kwargs):
        self._slackName = str(slackName)
        self._slackId = str(slackId)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def has_valid_slackId(self):
        return len(self._slackId) == 9 and self._slackId.startswith('U')

    def has_valid_slackName(self):
        return self._slackName != ''

    @property
    def slackName(self):
        return self._slackName

    @property
    def slackId(self):
        return self._slackId

    @property
    def tagSlackName(self):
        return '<@{id}>'.format(id=self._slackId)

    def __eq__(self, other):
        if isinstance(other, SlackUser):
            return self.slackId == other.slackId
        return False

    def __str__(self):
        return str((self.slackName, self.slackId))

    def __repr__(self):
        return str((self.slackName, self.slackId))

    def __hash__(self):
        return hash(tuple(self.__dict__.items()))


class SlackUserGroup(object):
    def __init__(self, *args):
        self._slackUserGroup =  {
            slackUser for slackUser in args if isinstance(slackUser, SlackUser)
                                               and slackUser.has_valid_slackId()
                                               and slackUser.has_valid_slackName()
        }

    @property
    def slackUserGroup(self):
        return self._slackUserGroup

    def getSlackUserById(self, slackId):
        for slackUser in self.slackUserGroup:
            if slackUser.slackId == slackId:
                return slackUser

    def getSlackUserByName(self, slackName):
        for slackUser in self.slackUserGroup:
            if slackUser.slackName == slackName:
                return slackUser


class MessageBase(object):
    SLACK_MSG_CONTENT = {'text': None}
    SLACK_MSG_HEADER = {'Content-type': 'application/json'}


class SlackMessage(MessageBase):
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
        return self._msg
    
    @property
    def msg(self):
        return self._assemble_msg()

    def _assemble_msg(self):
        assembled_msg = copy.deepcopy(self.SLACK_MSG_CONTENT)
        assembled_msg['text'] = str(self._msg)
        return assembled_msg
