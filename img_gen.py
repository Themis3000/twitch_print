from PIL import Image, ImageDraw, ImageFont
import textwrap


paper_width = 550
font_header = ImageFont.truetype('assets/Roboto-Medium.ttf', 60)
font_body = ImageFont.truetype('assets/Roboto-Medium.ttf', 30)


def gen_img(img, header_text, body_text):
    img_out = Image.new("RGBA", (paper_width, paper_width), color=(255, 255, 255, 0))

    # paste input image centered and at the top of the img_out
    img_width, img_height = img.size
    img_out.paste(img, (int((paper_width-img_width)/2), 0), img)
    img_draw = ImageDraw.Draw(img_out)

    # Header text
    header_w, header_h = img_draw.textsize(header_text, font=font_header)
    img_draw.text((int((paper_width-header_w)/2), img_height+15), header_text, font=font_header, fill="black")

    # Body text
    body_text_wrapped = "\n".join(["\n".join(textwrap.wrap(line, width=41)) for line in body_text.splitlines()])
    body_w, body_h = img_draw.textsize(body_text_wrapped, font=font_body)
    img_draw.text((int((paper_width-body_w)/2), img_height+90), body_text_wrapped, font=font_body, fill="black")

    return img_out
