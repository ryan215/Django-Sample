#-*- coding: utf-8 -*-
from django.conf import settings
from websocketsredis import settings as redis_settings
from nbash.models import NBash

class RedisStore(object):
    """
    Control the messaging from and to the Redis datastore.
    """
    subscription_channels = ['subscribe-session', 'subscribe-user', 'subscribe-broadcast']
    publish_channels = ['publish-session', 'publish-user', 'publish-broadcast']

    def __init__(self, connection, expire=redis_settings.WS4REDIS_EXPIRE):
        self._connection = connection
        self._subscription = None
        self._expire = expire

    def unsubscribe(self, request, access_token):
        key = request.path_info.replace(settings.WEBSOCKET_URL, "", 1)
        key_list = key.split('/')

        def nbashes():
            if len(key_list) > 1:
                self._connection.publish("nbashes", key_list[1] + " Unsubscribed")
                #if self._expire > 0:
                    #self._connection.set("nbashes", key_list[1] + " Unsubscribed", ex=self._expire)
                try:
                    nbash = NBash.objects.get(mac_id=key_list[1])
                    nbash.online = False
                    nbash.save()
                except:
                    pass
                    #print "Some big error."

        actions = {
            "nbashes": nbashes
        }
        try:
            actions[key_list[0]]()
        except KeyError:
            pass
            #print "Key Doesn't exist"
        return

    def subscribe(self, request, access_token):
        """
        Initialize the channels used for subscribing and sending messages.
        """
        self._subscription = self._connection.pubsub()
        self._publishers = set()

        key = request.path_info.replace(settings.WEBSOCKET_URL, "", 1)
        key_list = key.split('/')
        #print key_list
        def nbashes():
            ## Right now I am only checking for the id to match the access token
            # It should actually check for the id corresponding to the access token
            if len(key_list) > 1 and key_list[1] == access_token:
                self._connection.publish("nbashes", key_list[1] + " Subscribed")
                #if self._expire > 0:
                    #self._connection.set("nbashes", key_list[1] + " Subscribed", ex=self._expire)
                try:
                    nbash = NBash.objects.get(mac_id=key_list[1])
                    nbash.online = True
                    nbash.save()
                except:
                    nbash = NBash(mac_id=key_list[1], online=True)
                    nbash.save()
            self._subscription.subscribe(key)
            self._publishers.add(key)

        actions = {
            "nbashes": nbashes
        }
        try:
            actions[key_list[0]]()
        except KeyError:
            pass
            #print "Key Doesn't exist"


    def publish_message(self, message):
        """Publish a message on the subscribed channel on the Redis datastore."""
        if message:
            for channel in self._publishers:
                self._connection.publish(channel, message)
                # if self._expire > 0:
                #     self._connection.set(channel, message, ex=self._expire)

    def send_persited_messages(self, websocket):
        """
        This method is called immediately after a websocket is openend by the client, so that
        persisted messages can be sent back to the client upon connection.
        """
        for channel in self._subscription.channels:
            message = self._connection.get(channel)
            if message:
                websocket.send(message)

    def parse_response(self):
        """
        Parse a message response sent by the Redis datastore on a subscribed channel.
        """
        return self._subscription.parse_response()

    def get_file_descriptor(self):
        """
        Returns the file descriptor used for passing to the select call when listening
        on the message queue.
        """
        return self._subscription.connection and self._subscription.connection._sock.fileno()
