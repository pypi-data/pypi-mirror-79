import cv2
import os

import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import copy
from service import constants as const

STANDARD_COLORS = [
    'AliceBlue', 'BlueViolet', 'Chocolate', 'Crimson', 'DeepSkyBlue', 'DarkKhaki', 'DarkSeaGreen',
    'ForestGreen', 'Gold', 'HoneyDew', 'Khaki', 'LemonChiffon', 'LightGoldenRodYellow',
    'LightPink', 'LightSteelBlue', 'Linen','MediumPurple', 'MediumTurquoise', 'Moccasin',
    'OliveDrab', 'PaleGoldenRod', 'Pink'
]
#
# STANDARD_COLORS = [
#     'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
#     'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
#     'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
#     'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
#     'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
#     'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
#     'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
#     'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
#     'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
#     'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
#     'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
#     'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
#     'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
#     'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
#     'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
#     'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
#     'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
#     'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
#     'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
#     'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
#     'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
#     'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
#     'WhiteSmoke', 'Yellow', 'YellowGreen'
# ]

REMARKS = { y: idx for idx, (x, y) in enumerate(const.VA_TYPES.items())}


def __is_debug(func):
    def func_1(*args, **kwargs):
        if "DEBUG" in os.environ and os.environ["DEBUG"] == '1':
            return func(*args, **kwargs)

    return func_1

def _draw_bounb_box(image_np, boxs, scores, draw, color, expend_line):
    im_height, im_width, ch = image_np.shape

    for box, score in zip(boxs, scores):
        (ymin, xmin, ymax, xmax) = box
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                      ymin * im_height, ymax * im_height)

        left, right, top, bottom = left-expend_line, right+expend_line, top-expend_line, bottom+expend_line
        top_text = top - (expend_line*1.5)

        draw.line([(left, top), (left, bottom), (right, bottom),
                   (right, top), (left, top)], width=2, fill=color)

        font = ImageFont.load_default()
        draw.text(
            (left, top_text),
            '%.2f'%(score),
            fill=color,
            font=font)

@__is_debug
def show(image_np):
    cv2.imshow('img', image_np)
    cv2.waitKey()

@__is_debug
def show_images(image_np):
    for idx, image in enumerate(image_np):
        cv2.imshow(str(idx), cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    cv2.waitKey()

@__is_debug
def show_output_context(sc):
    for idx, ((image_np_org, wh, va_type, ch_id, _), out_dict) in enumerate(zip(sc.input, sc.output)):
        image_np = copy.copy(image_np_org)
        image_pil = Image.fromarray(np.uint8(image_np)).convert('RGB')
        draw = ImageDraw.Draw(image_pil)

        va_type_debug = list()
        for key in out_dict:
            _draw_bounb_box(image_np, out_dict[key][0], out_dict[key][1], draw, STANDARD_COLORS[REMARKS[key]], REMARKS[key]*2)
            va_type_debug.append([key, len(out_dict[key][2])])

        display_remarks(image_np, draw, va_type_debug)
        np.copyto(image_np, np.array(image_pil))
        cv2.imshow(str(idx), cv2.resize(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB), (720, 480)))

@__is_debug
def display_remarks(image_np, draw, va_type_debug):
    im_height, im_width, ch = image_np.shape

    font_size = int(im_height/20)

    try:
        # font = ImageFont.truetype('arial.ttf', font_size)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        font_size = 16

    left_padding = 5
    top_padding = 3

    for (type, count) in va_type_debug:
        draw.text(
            (left_padding, top_padding),
            type + ' : ' + str(count),
            fill=STANDARD_COLORS[REMARKS[type]],
            font=font)
        top_padding = top_padding + font_size