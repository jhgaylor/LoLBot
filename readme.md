Note: After spending a lot of time working with node.js/coffeescript I decided to use Hubot and the project is called StatBot. I've opened this up just to show something I worked on back in the day.

Mad props to hubot.  I spent a long time deciding between writing a bot in python and writing a league adapter for hubot.  I decided to do it in python 1) my colleagues use python 2) I don't enjoy reading coffeescript and 3) to flex sharpen my python saw.  Meteor has me writing a lot of js/cs these days.

This is my first foray into evented programming in python :D

The gist of how the bot works internally is
Adapter receives a msg from a remote host
Adapter uses the brain to get a user
adapter uses the msg and the user to make a full Message object
Adapter calls robot.receive(Message)
Robot sends Message to listeners
Listeners attempts to match Message, if so does callback(Response), where response is the message sent from the bot
Response.send(*strings)

# TODO:

short term:
    internal storage
    Persistant data store
    !register (web account)
    !subscribe (join a list or something)
    cli

long term:
    listen on group chats


