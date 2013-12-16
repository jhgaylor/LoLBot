
class Response(object):
    """
    A message to be sent from the bot
    """

    def __init__(self, robot, message, match):
        self.robot = robot
        self.message = message
        self.match = match

    def send(self, *strings):
        self.robot.adapter.send(self.message, *strings)

    def finish(self, *args, **kwargs):
        self.message.finish(*args, **kwargs)
