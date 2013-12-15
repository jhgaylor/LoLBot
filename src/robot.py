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
        self.adapter = adapter(self, "jhgaylor@pvp.net", "AIR_t6thurpr=")
        self.brain = Brain()
        self.events = EventEmitter()
        self.name = name
        self.listeners = []
        self._defaultListeners()

        self.on = self.events.on
        self.emit = self.events.emit

        # emit a local connected event when the adapter emits connected
        @self.adapter.on('connected')
        def _adapter_connected():
            self.events.emit('connected')

    def hear(self, pattern, callback):
        """
        Register a callback to a message 'heard' by the bot
        """
        listener = RegexListener(self, pattern, callback)
        self.listeners.append(listener)

    def receive(self, message):
        """
        Sends the message to all the listeners

        Returns None
        """
        responses = []
        for listener in listeners:
            responses.append(listener(message))

        if not len(responses):
            # no listeners 'heard' the message (and
            # therefore no response has been generated)
            # add a catchall response here
            pass

    def run(self):
        """
        Delegates to the adapter
        """
        print "We made it!"
        # self.adapter.run()

    def send(self, *strings):
        """
        Delegates to the adapter
        """
        self.adapter.send(*strings)

    def shutdown(self):
        """
        Gracefully shutdown the robot process
        """
        # clearInterval @pingIntervalId if @pingIntervalId?
        # @adapter.close()
        # @brain.close()

    def _defaultListeners(self):
        """
        TODO: move this somewhere else.
        """
        def lol_king(response):
            """
            Called by a Listener instance
            """
            return "I would lookup lolking"

        self.hear('(!lk) +(\w+)', lol_king)  # lolking lookup
