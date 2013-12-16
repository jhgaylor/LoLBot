class Message(object):
    """
    A message received by the bot
    """

    def __init__(self, user, done=False):
        self.user = user
        self.done = not not done  # ensure boolean

class TextMessage(Message):

    def __init__(self, user, text, id=None, done=False):
        super(TextMessage, self).__init__(user, done=done)
        self.text = text

class LoginMessage(Message):
    pass

class LogoutMessage(Message):
    pass