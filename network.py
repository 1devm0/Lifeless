import socket, pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.3.8"
        self.port = 4445
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048*30))
        except Exception as e:
            print(str(e))
            pass

    def send(self, data: str):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*30))
        except Exception as e:
            print(str(e))
