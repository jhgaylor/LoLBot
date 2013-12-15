import re

class Listener(object):
    def __init__(self, robot, truth_func, cb):
        self.isHeard = truth_func
        self.cb = cb

    def __call__(self, message):
        if self.isHeard(message):
            response = object()
            return cb(response)
            # return some object with all the stuff necessary to represent the response

    @property
    def name(self):
        return self.regex.pattern

class RegexListener(Listener):
    def __init__(self, robot, pattern, cb):
        self.regex = re.compile(pattern)
        self.isHeard = self.regex.match
        self.cb = cb
