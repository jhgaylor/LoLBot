import re
from message import TextMessage
from response import Response


class Listener(object):
    """
    initializes a callable class which sends the robot a
    message if a truth test is passed

    instance is callable with a single parameter
    """
    def __init__(self, robot, truth_func, cb):
        self.robot = robot
        self.isHeard = truth_func
        self.cb = cb

    def __call__(self, message):
        match = self.isHeard(message)
        if match:
            # match is the return value of the truth function
            response = Response(self.robot, message, match)
            return self.cb(response)


class RegexListener(Listener):
    """
    A listener whose truth function is the existance
    of a match to the regex passed on initialization
    """
    def __init__(self, robot, pattern, cb):
        self.regex = re.compile(pattern)
        super(RegexListener, self).__init__(robot, self.isHeard, cb)

    def isHeard(self, message):
        if isinstance(message, TextMessage):
            return self.regex.match(message.text)

#TODO:
#Possibly have class FriendRequestListener?
