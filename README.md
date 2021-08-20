### Currently incomplete/non-working

# Twitch printer
This repo aims ot make it easy (for a developer) to implement printing twitch notifications on a physical printer. This repo utilizes streamlab's socket api in order to receive notifications. You will have to implement the actual printing part yourself, but the entire process of generating the image to be printed and the socket handling will all be handled for you.

This project is used by me at https://twitch.tv/themis3000 with a receipt printer

## Usage
Edit the `print_img` method in `printer.py` to handle the incoming image and print it
