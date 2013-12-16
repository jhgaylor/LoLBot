import logging

from pyee import EventEmitter
from brain import Brain
from listener import RegexListener
from response import Response

class LoLBot(object):
    """
    The api to communicate with the robot.
    Public methods all tell the robot to 'do' something
    """
    def __init__(self, adapter, name="StatBot"):
        self.listeners = []
        self.adapter = adapter(self, "jakegaylor@pvp.net", "AIR_t6thurpr=")
        self.brain = Brain()
        self.events = EventEmitter()
        self.name = name
        self._defaultListeners()

        self.on = self.events.on
        self.emit = self.events.emit

        # emit a local connected event when the adapter emits connected
        @self.adapter.on('connect')
        def _adapter_connect():
            self.emit('connect')

    def hear(self, pattern, cb=None):
        """
        Register a callback to a message 'heard' by the bot

        Used a trick picked up from jesusabdullah@github to use as a decorator
        https://github.com/jesusabdullah/pyee/blob/master/pyee/__init__.py#L68

        Example:
        @hear('foo')
        def foo(response):
            response.send("Foo!")

        OR

        def bar(response):
            response.send("Bar!")

        hear('!bar'. bar)
        """
        def _hear(cb):
            listener = RegexListener(self, pattern, cb)
            self.listeners.append(listener)

            # Return original function so removal works
            return cb

        if cb is None:
            return _hear
        else:
            return _hear(cb)


    def receive(self, message):
        """
        Sends the message to all the listeners
        FOR NOW: Message is an instance of the XMPP message
            but it will be a Message object
        Returns None
        """
        # START HERE: We can get here but listeners is always empty
        # FOR NOW: the message text is accessed at ['body']

        logging.info("Bot is listening to: %s", message.text)
        heard = False
        # send the message to each listener
        for listener in self.listeners:
            if message.done:
                break
            resp = listener(message)
            if resp and not heard:
                heard = True

        if not heard:
            # no listeners 'heard' the message (and
            # therefore no response has been generated)
            # add a catchall response here
            Response(self, message, True).send("Unknown command")

    def run(self):
        """
        Delegates to the adapter
        """
        logging.debug("LoLBot::run!")
        self.adapter.run()

    def send(self, *messages):
        """
        Delegates to the adapter
        """
        logging.debug("LoLBot::send!")
        self.adapter.send(*messages)

    def shutdown(self):
        """
        Gracefully shutdown the robot process
        """
        raise NotImplementedError
        # clearInterval @pingIntervalId if @pingIntervalId?
        # @adapter.close()
        # @brain.close()

    def _defaultListeners(self):
        """
        TODO: move this somewhere else.

        each callback needs to return true-ish if it succeeds
        """

        @self.hear('(!find) +(\w+)')  # lolking lookup
        def quickfind(response):
            """
            Called by a Listener instance
            """
            groups = response.match.groups()
            text = "http://quickfind.kassad.in/profile/na/%s/" % groups[1]
            response.send(text)
            return True


        self.hear('(!counter) +(\w+)')
        def championselect(response):
            """
            Send a url to a champion on championselect
            """
            groups = response.match.groups()
            text = "http://www.championselect.net/champ/%s/" % groups[1]
            response.send(text)
            return True

