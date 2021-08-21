import socketio
import glob
import os
import math
import textwrap
from PIL import Image, ImageDraw
from pymitter import EventEmitter
from img_gen import gen_img, paper_width, font_body
from printer import print_img
from utils import make_ordinal

# Load token
with open("token.txt", "r") as f:
    token = f.read()

# Find image paths
image_paths = []
for search in ["assets/*.png", "assets/*.jpg"]:
    search_result = glob.glob(search)
    image_paths.extend(search_result)

# Load images
images = {}
for image_path in image_paths:
    with Image.open(image_path) as image:
        image_name = os.path.basename(image_path)
        image = image.resize((275, 275))
        images[image_name] = image

bits_dict = {1: "1.png", 100: "100.png", 1000: "1000.png", 5000: "5000.png", 10000: "10000.png"}

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
    image = gen_img(images["follow.png"], data["name"], "Has followed")
    print_img(image)


@ee.on("streamlabs.subscription")
def subscription_event(data):
    body_str = f"Has subscribed for the {make_ordinal(data['months'])} month\n\n" \
               f"\"{data['message']}\""
    image = gen_img(images["sub.png"], data["name"], body_str)
    print_img(image)


@ee.on("streamlabs.resub")
def resub_event(data):
    ee.emit("streamlabs.subscription", data)


@ee.on("streamlabs.bits")
def bits_event(data):
    bit_symbol_path = ""
    for key, img_path in bits_dict.items():
        if int(data["amount"]) >= key:
            bit_symbol_path = img_path

    body_str = f"Has cheered {data['amount']} bits\n\n" \
               f"\"{data['message']}\""
    image = gen_img(images[bit_symbol_path], data["name"], body_str)
    print_img(image)


@ee.on("streamlabs.raid")
def raid_event(data):
    paper_height = 80 + math.ceil(data["raiders"] / 2)*275
    img_out = Image.new("RGBA", (paper_width, paper_height), color=(255, 255, 255, 0))
    img_draw = ImageDraw.Draw(img_out)

    # Header
    header_text = f"{data['name']} is raiding with a party of {data['raiders']}"
    header_text_wrapped = "\n".join(textwrap.wrap(header_text, width=41))
    header_w, header_h = img_draw.textsize(header_text_wrapped, font=font_body)
    img_draw.text((int((paper_width-header_w)/2), 0), header_text, font=font_body, fill="black")

    # Raider profiles
    for raid_pair in range(math.floor(data["raiders"]/2)):
        place_height = 80 + raid_pair*275
        img_out.paste(images["raider.png"], (0, place_height), images["raider.png"])
        img_out.paste(images["raider.png"], (275, place_height), images["raider.png"])

    # handles if odd
    if data["raiders"] % 2 == 1:
        img_out.paste(images["raider.png"], (int(275/2), paper_height-275), images["raider.png"])
    print_img(img_out)
