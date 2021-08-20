import socketio
from PIL import Image, ImageDraw, ImageFont
from pymitter import EventEmitter

with open("token.txt", "r") as f:
    token = f.read()

sio = socketio.Client(reconnection_delay_max=0)
sio.connect(f"https://sockets.streamlabs.com?token={token}", transports=["websocket"])

ee = EventEmitter()


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
def event(data):
    if "for" not in data or not data["for"] == "twitch_account":
        return

    for message in data["message"]:
        ee.emit(f"streamlabs.{data['type']}", message)


@ee.on("streamlabs.follow")
def follow_event(data):
    print("Follow event")


@ee.on("streamlabs.subscription")
def subscription_event(data):
    print("Sub event")


@ee.on("streamlabs.resub")
def resub_event(data):
    ee.emit("streamlabs.subscription", data)


@ee.on("streamlabs.bits")
def bits_event(data):
    pass


@ee.on("streamlabs.raid")
def raid_event(data):
    pass
