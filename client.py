import socket
from threading import Thread
import sys

class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #uses TCP
        self.socket.connect((host, port))

        self.nickname = input("Enter your nickname: ")
        self.socket.send(self.nickname.encode())

        print("\nConnected to chat server!")
        print("Type messages and press ENTER")
        print("Commands:")
        print("  /join roomname   → join a channel")
        print("  /pm user message → private message")
        print("  /quit            → exit\n")

        Thread(target=self.receive_messages, daemon=True).start()
        self.send_messages()

    # send messages to server
    def send_messages(self):
        while True:
            try:
                message = input()

                if message == "/quit":
                    self.socket.send("/quit".encode())
                    self.socket.close()
                    sys.exit()

                self.socket.send(message.encode())

            except:
                print("Disconnected from server")
                self.socket.close()
                break

    # receive messages from server
    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()

                if not message:
                    print("Connection closed by server.")
                    break

                print("\033[92m" + message+ "\033[0m")

            except:
                print("Lost connection to server.")
                break

if __name__ == "__main__":
    HOST = input("Server IP: ")
    PORT = 5000

    Client(HOST, PORT)