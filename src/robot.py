import logging

from pyee import EventEmitter
from brain import Brain
from listener import RegexListener


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

    def hear(self, pattern, callback):
        """
        Register a callback to a message 'heard' by the bot
        """
        listener = RegexListener(self, pattern, callback)
        self.listeners.append(listener)

    def receive(self, message):
        """
        Sends the message to all the listeners
        FOR NOW: Message is an instance of the XMPP message
            but it will be a Message object
        Returns None
        """
        # START HERE: We can get here but listeners is always empty
        # FOR NOW: the message text is accessed at ['body']

        logging.info(message)
        # get the response from each listener
        responses = [listener(message['body']) for listener in self.listeners]
        # remove the empty responses
        responses = [response for response in responses if response]
        if not len(responses):
            # no listeners 'heard' the message (and
            # therefore no response has been generated)
            # add a catchall response here
            pass
        self.send(responses)

    def run(self):
        """
        Delegates to the adapter
        """
        logging.debug("LoLBot::run!")
        self.adapter.run()

    def send(self, *strings):
        """
        Delegates to the adapter
        """
        logging.debug("LoLBot::send!")
        self.adapter.send(*strings)

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
        """
        import requests
        def quickfind(response, listener):
            """
            Called by a Listener instance
            """
            try:
                url = "http://quickfind.kassad.in/profile/na/%s/" % (listener.parts[1], )
                return url
            except:
                return "I would lookup lolking"

        self.hear('(!find) +(\w+)', quickfind)  # lolking lookup
