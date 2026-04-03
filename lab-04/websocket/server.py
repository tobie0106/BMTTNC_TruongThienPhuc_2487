import random
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketServer.clients.add(self)

    def on_close(self):
        WebSocketServer.clients.remove(self)

    @classmethod
    def send_message(cls, message: str):
        for client in cls.clients:
            client.write_message(message)
        print(f"Sent message to {len(cls.clients)} clients")

class RandomWordSelector:
    def __init__(self, words):
        self.words = words

    def sample(self):
        return random.choice(self.words)

def main():
    app = tornado.web.Application([
        (r"/websocket/", WebSocketServer),
    ])
    app.listen(8888)

    selector = RandomWordSelector(["apple", "banana", "cherry", "date", "fig", "grape"])

    def send_random_word():
        word = selector.sample()
        WebSocketServer.send_message(word)

    periodic_callback = tornado.ioloop.PeriodicCallback(send_random_word, 3000)
    periodic_callback.start()

    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
