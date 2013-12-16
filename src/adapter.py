#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyee import EventEmitter
import sys


import logging
import sleekxmpp
from message import TextMessage
from botuser import User
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
    """
    A thin wrapper around sleekxmpp.ClientXMPP that
    also registers some plugins
    """
    def __init__(self, jid, password):
        super(LoLXMPPClient, self).__init__(jid, password)

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping


class Adapter(EventEmitter):
    """
    The interface for an adapter to LoLBot
    """
    def __init__(self, robot):
        super(Adapter, self).__init__()
        self.robot = robot

    def receive(self, message):
        self.robot.receive(message)

    def send(self):
        """
        Must be overwritten
        """
        raise NotImplementedError


class LoLXMPPAdapter(Adapter):
    """
    An adapter for LoLBot to the riot xmpp server
    This idea is mostly here to keep a clean seperation
    of duties between the bot and the client
    """

    def __init__(self, robot, jid, password,
                 host='chat.na1.lol.riotgames.com',
                 port=5223
                 ):
        """
        Create an instance of LoLXMPPClient, bind
        event handlers to instance methods

        """
        super(LoLXMPPAdapter, self).__init__(robot)
        self.client = LoLXMPPClient(jid, password)
        self.host = host
        self.port = port

        # handle the xmpp client events in the adapter
        self.client.add_event_handler("session_start", self._session_start)
        self.client.add_event_handler("message", self._message)
        presence_events = ["presence_available", "presence_probe", "presence_subscribe", "presence_subscribed"]
        for event in presence_events:
            self.client.add_event_handler(event, self._presence)

        # bind events upon creation
        @self.on('connect')
        def on_connect():
            logging.info("Connected to XMPP server.")

        @self.on("disconnect")
        def on_disconnect():
            logging.info("Disconnected from XMPP server.")

    def run(self):
        # Connect to the XMPP server and start processing XMPP stanzas.
        try:
            if self.client.connect((self.host, self.port), use_ssl=True):
                self.emit('connect')
                # TODO: switch to false?
                # if block=False. this isn't where we
                # emit disconnected
                self.client.process(block=True)
                self.emit('disconnect')
            else:
                logging.warning("Unable to connect.")
        except KeyboardInterrupt:
            logging.error("===Kill signal received===")
            sys.exit()

    def send(self, message, *strings):
        logging.info(strings)
        jid = message.user.id
        for body in strings:
            m = self.client.make_message(jid, body, mtype='chat')
            logging.debug(m)
            m.send()

    # Define xmpp client event handlers
    # naming pattern is '_event_name'
    def _session_start(self, event):
        """
        Process the session_start event.

        requests the roster
        broadcasts an initial presence stanza
        TODO: talk to brain about the user

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        logging.debug("Begin handling session_start event")
        self.client.send_presence()
        self.client.get_roster()
        logging.debug("End handling session_start event")

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
        logging.debug("Begin handling message event")
        logging.info("Incoming message: %s", msg)
        # TODO: Have the bot deal with presences/other message stanzas
        # FOR NOW only send the bot chat messages
        if msg['type'] in ('chat', 'normal'):
            jid_from = msg['from']
            # TODO: hook up the brain
            # user = self.robot.brain.userForId(msg['from'])
            user = User(jid_from)
            message = TextMessage(user, msg['body'], id=msg['id'])
            self.robot.receive(message)

        logging.debug("End handling message event.")

    def _presence(self, msg):
        logging.info("Incoming presence: %s", msg)
