class User:
    """TODO: switch to slack official api client: https://github.com/slackapi/python-slackclient"""

    def __init__(self, slack_name, slack_id, **kwargs):
        self.slack_name, self.slack_id = slack_name, slack_id
        for k, v in kwargs.items():
            setattr(self, k, v)

    def valid_name(self) -> bool:
        return self.slack_name != ''

    def valid_id(self) -> bool:
        return len(self.slack_id) == 9 and self.slack_id.startswith('U')

    @property
    def tag(self) -> str:
        return f"<@{self.slack_id}>"

    def __str__(self):
        return f"{self.slack_id} {self.slack_name}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.slack_id, self.slack_name))

    def __eq__(self, other) -> bool:
        return self.slack_id == other.slack_id if isinstance(other, User) else False

    def __json__(self):
        return {'slack_name': self.slack_name, 'slack_id': self.slack_id}


if __name__ == '__main__':
    # a = User('test', '123')
    # print(a, a.tag)
    pass
