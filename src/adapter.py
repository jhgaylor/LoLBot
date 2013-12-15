#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyee import EventEmitter
import sys


import logging
import sleekxmpp

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class LoLXMPPClient(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        # if for some reason this is causing a problem, try
        # flipping these
        super(LoLXMPPClient, self).__init__(jid, password)
        # sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # self.add_event_handler("session_start", self.start)
        # self.add_event_handler("message", self.message)

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping

    # def start(self, event):
    #     """
    #     Process the session_start event.

    #     Typical actions for the session_start event are
    #     requesting the roster and broadcasting an initial
    #     presence stanza.

    #     Arguments:
    #         event -- An empty dictionary. The session_start
    #                  event does not provide any additional
    #                  data.
    #     """
    #     self.send_presence()
    #     self.get_roster()

    # def message(self, msg):
    #     """
    #     Process incoming message stanzas. Be aware that this also
    #     includes MUC messages and error messages. It is usually
    #     a good idea to check the messages's type before processing
    #     or sending replies.

    #     Arguments:
    #         msg -- The received message stanza. See the documentation
    #                for stanza objects and the Message stanza to see
    #                how it may be used.
    #     """
    #     # logging.info("got a message")
    #     logging.info("\n===Received message===\n%s\n===End message===\n",
    #                  msg
    #                  )
    #     if msg['type'] in ('chat', 'normal'):
    #         msg.reply("I'm afk, probably asleep.").send()


class Adapter(EventEmitter):

    def __init__(self, robot):
        super(Adapter, self).__init__()
        self.robot = robot

    def receive(self, message):
        self.robot.receive(message)


class LoLXMPPAdapter(Adapter):
    """
    An adapter for LoLBot to the riot xmpp server
    This idea is mostly here to keep a clean seperation
    of duties between the bot and the client
    though I guess someone could write an irc adapter?!?!
    """

    def __init__(self, robot, jid, password,
                 host='chat.na1.lol.riotgames.com',
                 port=5223
                 ):
        super(LoLXMPPAdapter, self).__init__(robot)
        self.client = LoLXMPPClient(jid, password)

        self.client.add_event_handler("session_start", self._session_start)
        self.client.add_event_handler("message", self._message)

        @self.on('connected')
        def log_connected():
            logging.info("Connected to XMPP server.")

        # Connect to the XMPP server and start processing XMPP stanzas.
        try:
            if self.client.connect((host, port), use_ssl=True):
                # TODO: switch to false?
                self.emit('connected')
                self.client.process(block=True)
                # TODO: if block=False this should read differently
                logging.info("Disconnecting.")
            else:
                logging.warning("Unable to connect.")
        except KeyboardInterrupt:
            logging.error("===Kill signal received===")
            sys.exit()

    def _session_start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.client.send_presence()
        self.client.get_roster()


    def _message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        # logging.info("got a message")
        logging.info("\n===Received message===\n%s\n===End message===\n",
                     msg
                     )
        if msg['type'] in ('chat', 'normal'):
            msg.reply("I'm afk, probably asleep.").send()
