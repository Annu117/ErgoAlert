import numpy as np
import math
# import cv2
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

def padding(img, stride, padValue):
    if isinstance(img, Image.Image):
        h, w = img.size
        img_padded = img.crop((-pad[1], -pad[0], w + pad[3], h + pad[2]))
    else:
        h, w = img.shape[:2]
        pad = 4 * [None]
        pad[0] = 0  # up
        pad[1] = 0  # left
        pad[2] = 0 if (h % stride == 0) else stride - (h % stride)  # down
        pad[3] = 0 if (w % stride == 0) else stride - (w % stride)  # right

        img_padded = Image.fromarray(img)
        img_padded = img_padded.crop((-pad[1], -pad[0], w + pad[3], h + pad[2]))

    pad_up = np.tile(np.array(img_padded)[0:1, :, :] * 0 + padValue, (pad[0], 1, 1))
    img_padded = np.concatenate((pad_up, np.array(img_padded)), axis=0)
    pad_left = np.tile(np.array(img_padded)[:, 0:1, :] * 0 + padValue, (1, pad[1], 1))
    img_padded = np.concatenate((pad_left, np.array(img_padded)), axis=1)
    pad_down = np.tile(np.array(img_padded)[-2:-1, :, :] * 0 + padValue, (pad[2], 1, 1))
    img_padded = np.concatenate((np.array(img_padded), pad_down), axis=0)
    pad_right = np.tile(np.array(img_padded)[:, -2:-1, :] * 0 + padValue, (1, pad[3], 1))
    img_padded = np.concatenate((np.array(img_padded), pad_right), axis=1)

    return img_padded, pad

# transfer caffe model to pytorch which will match the layer name
def transfer(model, model_weights):
    transfered_model_weights = {}
    for weights_name in model.state_dict().keys():
        transfered_model_weights[weights_name] = model_weights['.'.join(weights_name.split('.')[1:])]
    return transfered_model_weights

# get max index of 2d array
def npmax(array):
    arrayindex = array.argmax(1)
    arrayvalue = array.max(1)
    i = arrayvalue.argmax()
    j = arrayindex[i]
    return i, j

# pose vis
def pose_vis(img, candidate, subset, al_list):
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    pose_color = np.random.rand(len(subset), 3) * 255

    for i in range(len(subset)):
        mid_x1 = candidate[subset[i][8].astype(int)][0]
        mid_x2 = candidate[subset[i][11].astype(int)][0]
        mid_y1 = candidate[subset[i][8].astype(int)][1]
        mid_y2 = candidate[subset[i][11].astype(int)][1]
        mid_x = int((mid_x1 + mid_x2) / 2)
        mid_y = int((mid_y1 + mid_y2) / 2)

        text_size = 72  
        font = ImageFont.truetype("arial.ttf", text_size)
        text_to_display = str(i + 1)
        # text_color = (0, 128, 0)  # Default color -> Green
        text_color = (0, 255, 0)
        if text_to_display == '3':
            text_color = (255, 165, 0)  # Orange
        elif text_to_display == '4':
            text_color = (255, 0, 0)  # Red

        draw.text((mid_x, mid_y), text_to_display, fill=text_color, font=font)        
        for jj in range(18):
            if subset[i][jj] > -1:
                point_x = int(candidate[subset[i][jj].astype(int)][0])
                point_y = int(candidate[subset[i][jj].astype(int)][1])

                ellipse_size = 5  
                draw.ellipse([(point_x - ellipse_size, point_y - ellipse_size),
                            (point_x + ellipse_size, point_y + ellipse_size)],
                            fill=tuple(map(int, pose_color[i])))

    img_array = np.array(img)
    return img_array