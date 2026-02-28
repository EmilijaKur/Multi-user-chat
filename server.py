import socket
from threading import Thread
class Server:
    Clients=[]
    def __init__(self, HOST, PORT):        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #here TCP is implemented
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print("Server waiting for connection ...")
    
    def broadcast_message(self, sender_name, message, channel=None):
        for client in Server.Clients:
            if client["client_name"] != sender_name:
                if channel is None or client["channel"] == channel:
                    try:
                        client["client_socket"].send(message.encode())
                    except:
                        pass   
    
    def private_message(self, sender_name, target_name, message):
        for client in Server.Clients:
            if client["client_name"] == target_name:
                client["client_socket"].send(
                    f"[PM from {sender_name}] {message}".encode()
                )
                return
            
    def listen(self):
        try:
            while True:
                client_socket, address = self.socket.accept()
                print("Connection from:", address)

                client_name = client_socket.recv(1024).decode()

                client = {
                "client_name": client_name,
                "client_socket": client_socket,
                "channel": "general"
                }

                Server.Clients.append(client)

                self.broadcast_message(
                    client_name,
                    client_name + " has joined the chat!",
                    "general"
                )

                Thread(target=self.handle_new_client, args=(client,)).start()
        except KeyboardInterrupt:
            print("\nShutting down server...")

            for client in Server.Clients:
                try:
                    client["client_socket"].close()
                except:
                    pass

            self.socket.close()
            print("Server closed.")

        
    def handle_new_client(self, client):
        client_name = client["client_name"]
        client_socket = client["client_socket"]

        while True:
            try:
                message = client_socket.recv(1024).decode()

                if not message:
                    break

                # join channel
                if message.startswith("/join "):
                    new_channel = message.split(" ", 1)[1]
                    client["channel"] = new_channel
                    client_socket.send(
                        f"You joined channel: {new_channel}".encode()
                    )

                # private message
                elif message.startswith("/pm "):
                    _, target, pm_msg = message.split(" ", 2)
                    self.private_message(client_name, target, pm_msg)

                # quit sending messages
                elif message == "/quit":
                    break

                # normal message
                else:
                    self.broadcast_message(
                        client_name,
                        f"[{client['channel']}] {client_name}: {message}",
                        client["channel"]
                    )

            except:
                break

        print(client_name, "disconnected")
        Server.Clients.remove(client)
        self.broadcast_message(client_name, client_name + " left the chat.")
        client_socket.close()

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000

    server = Server(HOST, PORT)
    server.listen()
