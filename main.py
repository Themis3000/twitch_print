import socketio

with open("token.txt", "r") as f:
    token = f.read()

sio = socketio.Client(reconnection_delay_max=0)
sio.connect(f"https://sockets.streamlabs.com?token={token}", transports=["websocket"])


@sio.event()
def connect():
    print("Connected to streamlabs!")


@sio.event()
def connect_error():
    print("Connection failed :\\")


@sio.event()
def disconnect():
    print("Disconnected")


@sio.on("event")
def follow(data):
    print(data)
