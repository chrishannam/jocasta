from Adafruit_IO import Client


class IOAdafruitConnector(object):
    def __init__(self, key, username, feeds) -> None:
        self.aio = Client(username=username, key=key)
        self.feeds = feeds

    def send(self, data):
        for feed in self.feeds.split(','):
            aio_feed = self.aio.feeds(feed)
            self.aio.send_data(aio_feed.key, data[feed])

        return {'status': 'ok'}
