# coding=utf-8
import json
import time
from dircache import cache

from channels import Group
# Connected to websocket.connect
from channels.auth import channel_session_user_from_http, channel_session_user
from channels.generic.websockets import WebsocketConsumer
from channels.handler import AsgiRequest

from ws.ws_authentication import token_authenticate


# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    print "------------------ws_add-------------------------------"
    # Add them to the right group
    Group("chat-%s" % message.user.username[0]).add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    print "[user] %s" % message.content['text']
    Group("chat").send({
        "text": "[user] %s" % message.content['text'],
    }
    )

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)


class ChatServer(WebsocketConsumer):
    # 如果你想使用channel_session或者channel_session_user，那么只要在类中设置
    channel_session_user = True

    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["test"]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        # Accept the connection; this is done by default if you don't override
        # the connect function.
        try:
            request = AsgiRequest(message)
        except Exception as e:
            self.close()
            return
        token = request.GET.get("token", None)
        if token is None:
            self.close()
            return
        user, token = token_authenticate(token, message)
        message.token = token
        message.user = user
        message.channel_session['user'] = user
        self.message.reply_channel.send({"accept": True})
        print '连接状态', message.user

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        # Simple echo
        value = cache.get('test')
        print value
        while True:
            if cache.get('test') is not None and cache.get('test') != value:
                value = cache.get('test')
                break
            time.sleep(1)
        self.send(json.dumps({
            "text": cache.get('test')
        }))

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass