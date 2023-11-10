# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:14:17 2023

@author: User

"""
import math
import numpy as np
import cv2
import argparse
def imagediff(image, previmage):
    total = 0
    image = image.astype("int64")
    previmage = previmage.astype("int64")
    total = (np.abs(image - previmage)).sum()
    total = total / image.shape[0] / image.shape[1]
    #total = math.sqrt(total)
    return total

def process(vidPath, percentile):
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
    perdiff = np.percentile(diffs, percentile)
    stopped = True
    file = open("startstop.txt", "w")
    lastcount = 0
    for i in range(len(diffs)):
        if (not stopped) and diffs[i] >= perdiff and i >= lastcount + 300:
            stopped = True
            file.write(str(i) + "s" + " ")
            lastcount = i
        if (stopped) and diffs[i] < perdiff and i >= lastcount + 300:
            stopped = False
            file.write(str(i) + "g" + " ")
            lastcount = i
    file.close()
if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--vidPath", help="path to video")
    a.add_argument("--percentile", help="how much of the video should be subway surfers")
    args = a.parse_args()
    print(args)
    process(args.vidPath, args.percentile)
