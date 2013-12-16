#!/bin/python
import sys
import getpass
from optparse import OptionParser
import logging

if __name__ == '__main__':
    # add the bot source to $PATH
    sys.path.append('../src/')
    from robot import LoLBot
    from adapter import LoLXMPPAdapter
    # # Setup the command line arguments.
    optp = OptionParser()

    # # Output verbosity options.
    # optp.add_option('-q', '--quiet', help='set logging to ERROR',
    #                 action='store_const', dest='loglevel',
    #                 const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    # optp.add_option('-v', '--verbose', help='set logging to COMM',
    #                 action='store_const', dest='loglevel',
    #                 const=5, default=logging.INFO)

    # # JID and password options.
    # optp.add_option("-j", "--jid", dest="jid",
    #                 help="JID to use")
    # optp.add_option("-p", "--password", dest="password",
    #                 help="password to use")

    opts, args = optp.parse_args()

    # # Setup logging.

    logging.basicConfig(level=opts.loglevel,
                        # filename='../log.txt',
                        format='[%(asctime)s]%(levelname)-8s %(message)s')
    # format='%(levelname)s:%(message)s'

    # if opts.jid is None:
    #     opts.jid = raw_input("Username: ")
    # if opts.password is None:
    #     opts.password = getpass.getpass("Password: ")

    # Setup the LOLBot and register plugins.
    bot = LoLBot(LoLXMPPAdapter)

    bot.run()


# available bots
# user: statbot
# password: 4ecr3fra
# handle: StatBot

#inspected the lolking form and found out
#lolking.com/search?name=summonerName redirects to their lolking page
#http://www.lolking.net/search/?name=igetkills redirects to
#http://www.lolking.net/summoner/na/20306036
# except lol king does black magic to bone us


#mind blown
#https://github.com/markstory/hubot-xmpp/blob/master/src/xmpp.coffee#L147
#this 'user' is an internal user to the bot, not an xmpp user