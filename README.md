# Multi-User Chat Server & Client
A simple TCP-based multi-user chat application in Python, supporting multiple channels, private messaging, and real-time broadcast. 
The system consists of a threaded TCP server (`server.py`) and a command-line client (`client.py`). Each client connects over a raw TCP socket, picks a nickname, and can chat in channels, send private messages, or switch channels — all in real time.

## How It Works
### Server (`server.py`)

- Listens for incoming TCP connections on `0.0.0.0:5000`.
- On connect, reads the client's nickname and registers them in a shared `Clients` list, each entry storing their name, socket, and current channel (default: `"general"`).
- Spawns a new thread per client (`handle_new_client`) so all connections are handled concurrently without blocking each other.
- Routes incoming messages based on their content:
  - `/join <room>` — moves the client to a new channel.
  - `/pm <user> <message>` — sends a private message directly to one user's socket.
  - `/quit` — ends that client's session.
  - anything else — broadcast to everyone currently in the same channel.
- `broadcast_message()` loops over all connected clients and sends the message to everyone in the matching channel (excluding the sender).
- `private_message()` looks up the target client by nickname and sends the message only to them.
- On `Ctrl+C`, the server closes every open client socket before shutting itself down, rather than dropping connections abruptly.
- When a client disconnects (or an error occurs while reading from their socket), they're removed from the `Clients` list and the rest of the channel is notified.

### Client (`client.py`)

- Connects to the server via TCP and sends a chosen nickname.
- Runs two things in parallel:
  - `send_messages()` — the main thread loop, reads from stdin and sends each line to the server. Handles `/quit` by closing the socket and exiting.
  - `receive_messages()` — a background daemon thread that continuously listens for incoming data and prints it (in green, via ANSI escape codes).
- This threaded split lets the client send and receive messages at the same time, without blocking on input.

## Commands

| Command | Description |
|---|---|
| `/join <roomname>` | Switch to (or create) a channel |
| `/pm <user> <message>` | Send a private message to a specific user |
| `/quit` | Disconnect from the server |
| *(anything else)* | Sent as a normal message to your current channel |

## Running It

**Start the server:**

```bash
python server.py
```

**Start one or more clients:**

```bash
python client.py
```

You'll be prompted for the server IP and a nickname. Run multiple clients (in separate terminals, or on separate machines pointed at the server's IP) to chat between them.
