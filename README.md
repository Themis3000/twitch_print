### Currently incomplete/non-working

# Twitch receipt printer
This repo aims ot make it easy (for a developer) to implement printing twitch notifications on a physical receipt printer. This repo utilizes streamlab's socket api in order to receive notifications. You will have to implement the actual printing part yourself, but the entire process of generating the image to be printed and the socket handling will all be handled for you.

This project is used by me at https://twitch.tv/themis3000 with a receipt printer

## Usage
1. Run `pip3 install -r requirement.txt` in this directory
2. Create an account on streamlabs and get your socket access token (found in `settings > api settings > api tokens`)
3. Create a file named token.txt and paste your access token in it
4. Edit the `print_img` method in `printer.py` to handle the incoming image and print it (note: images passed in will have a width of 550px and could have any height)

Feel free to create an issue or email me to reach out for help setting this up if you're interested
