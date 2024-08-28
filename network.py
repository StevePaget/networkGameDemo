import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.178.23"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        print("Player", self.p)

    def getP(self):
        return int(self.p)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(100).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return "OK"
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return pickle.loads(self.client.recv(2048*4))
        except socket.error as e:
            print(e)