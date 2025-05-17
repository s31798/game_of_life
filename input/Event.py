from collections import defaultdict

class Events:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, channel, callback):
        self.subscribers[channel].append(callback)

    def publish(self, channel, data):
        for callback in self.subscribers[channel]:
            callback(data)


