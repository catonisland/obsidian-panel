__author__ = "Nigshoxiz"

import redis
import threading
import pickle
class MessageQueueProxy:
    '''
    What is a .. Message Queue Proxy?
    A message queue proxy is responsible for receiving message from message queue
    and send message to it.
    Because we use a standalone websocket server, we use message queue to delegate
    websocket server to send websocket message, instead of sending message directly.
    '''
    def __init__(self):
        self.redis = redis.Redis()
        self.pubsub = self.redis.pubsub()

        self.channel = "socketio"
        # subscribe socketio to recv data from websocket server
        self.pubsub.subscribe(self.channel)

        self.handlers = []

        t = threading.Thread(target=self._listen)
        t.start()

    def _listen(self):
        for msg in self.pubsub.listen():
            print(msg)
            # run handlers
            pass

    def send(self, event, message, namespace="/", room=None, skip_sid=None):
        send_msg = {
            "method" : "emit",
            "event": event,
            "data" : message,
            "namespace" : namespace,
            "room": room,
            "skip_sid" : skip_sid,
            "callback" : None
        }
        #self._publish({'method': 'emit', 'event': event, 'data': data,
        #               'namespace': namespace, 'room': room,
        #               'skip_sid': skip_sid, 'callback': callback})
        self.redis.publish(self.channel, pickle.dumps(send_msg))

    def on(self, message):
        
        pass


