

from PIL import Image, ImageDraw, ImageFont
import textwrap, os

def meme(para = 'Hello, World!'):
    # INPUT
    im = Image.open('static/meme/cat.jpg')

    # CONFIGURATION
    image_width, image_height = im.size
    arial = ImageFont.truetype("arial.ttf", size = 120)
    draw = ImageDraw.Draw(im)
    shadowcolor = 'black'
    fillcolor = 'white'
    highlight_width = 5

    # MULTILINE
    paragraph = textwrap.wrap(str(para), initial_indent = '(output) ', placeholder = 'etc etc ...', width = 25, max_lines = 3, break_long_words = True)
    initial_height, line_spacing = (0.01 * image_height), 1
    for line in paragraph:
        text_width, text_height = draw.textsize(line, font = arial)
        x_coordinate, y_coordinate = (image_width - text_width) / 2, initial_height
        draw.text((x_coordinate - highlight_width, y_coordinate - highlight_width), line, font = arial, fill=shadowcolor)
        draw.text((x_coordinate + highlight_width, y_coordinate - highlight_width), line, font = arial, fill=shadowcolor)
        draw.text((x_coordinate - highlight_width, y_coordinate + highlight_width), line, font = arial, fill=shadowcolor)
        draw.text((x_coordinate + highlight_width, y_coordinate + highlight_width), line, font = arial, fill=shadowcolor)
        draw.text((x_coordinate, y_coordinate), line, font = arial, fill = fillcolor)
        initial_height += text_height + line_spacing

    # OUTPUT
    im.save('static/meme/output.png', "PNG")