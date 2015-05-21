class Subscription:
    subscriberCount = 0

    def __init__(self, url, destination):
        self.url = url
        self.destination = destination
        Subscription.subscriberCount += 1

    def displayCount(self):
        return self.subscriberCount

    def displaySubscriber(self):
        print("nothing")