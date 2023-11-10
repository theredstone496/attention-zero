# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:14:17 2023

@author: User

"""
#example use: python pixel.py --vidPath "attention-zero/video/videos/Renai Circulation.mp4" --percentile 70 --vid2height 480 --vid2width 360 --attentionSpan 300
import math
import numpy as np
import cv2
import argparse
import sys
np.set_printoptions(threshold=sys.maxsize)
def imagediff(image, previmage):
    total = 0
    image = image.astype("int64")
    previmage = previmage.astype("int64")
    total = (np.abs(image - previmage)).sum()
    total = total / image.shape[0] / image.shape[1]
    #total = math.sqrt(total)
    return total
def conv2d(a, f):
    s = f.shape + tuple(np.subtract(a.shape, f.shape) + 1)
    strd = np.lib.stride_tricks.as_strided
    subM = strd(a, shape = s, strides = a.strides * 2)
    return np.einsum('ij,ijkl->kl', f, subM)
def process(vidPath, percent, vid2height, vid2width, attentionSpan):
    vidcap = cv2.VideoCapture(vidPath)
    success,image = vidcap.read()
    image = cv2.resize(image, (400, 400))
    count = 0
    diffs = []
    previmg = image
    while success:
      success,image = vidcap.read()
      if not success:
          break
      image = cv2.resize(image, (400, 400))
      diff = imagediff(image, previmg)
      diffs.append(diff)
      previmage = image
      count += 1
    perdiff = np.percentile(diffs, percent)
    stopped = True
    file = open("startstop.txt", "w")
    lastcount = 0
    for i in range(len(diffs)):
        if (not stopped) and diffs[i] >= perdiff and i >= lastcount + 300:
            stopped = True
            file.write(str(i) + "s" + " ")
            lastcount = i
        if (stopped) and diffs[i] < perdiff and i >= lastcount + attentionSpan:
            stopped = False
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, i - 1)
            success, image = vidcap.read()
            orgshape = image.shape
            image = cv2.resize(image, (image.shape[0] // 10, image.shape[1] // 10))
            newimg1 = np.square(conv2d(image[:, :, 0], np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])))
            newimg2 = np.square(conv2d(image[:, :, 1], np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])))
            newimg3 = np.square(conv2d(image[:, :, 2], np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])))
            newimg = newimg1 + newimg2 + newimg3
            newimg4 = conv2d(newimg, np.ones([vid2height // 10, vid2width // 10]))
            amin = newimg4.argmin()
            idx = (amin // newimg4.shape[1], amin % newimg4.shape[1])
            tot = newimg4.shape
            file.write(str(i) + "g" + "(" + str(int(0.5 * vid2width + (orgshape[1] - vid2width) * idx[1] / (tot[1]-1))) + "," + str(int(0.5 * vid2height + (orgshape[0] - vid2height) * idx[0] / (tot[0]-1))) + ")" + " ")
            lastcount = i
    file.close()
if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--vidPath", help="path to video")
    a.add_argument("--percentile", help="how much of the video should be subway surfers")
    a.add_argument("--vid2height", help="target height of subway surfers")
    a.add_argument("--vid2width", help="target width of subway surfers")
    a.add_argument("--attentionSpan", help="time in between subway surfers")
    args = a.parse_args()
    print(args)
    process(args.vidPath, int(args.percentile), int(args.vid2height), int(args.vid2width), int(args.attentionSpan))
