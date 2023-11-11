import argparse
import re
import random
from moviepy.editor import *

from pixel import process

# example use: python videoedit.py --mainvid "ricardo.mp4" --extravid "..\subway-surfers\part0new.avi" --output "richard.mp4"

def edit(mainvid, extravids, output, percentile, attentionSpan):
    # clip1 is main, clip2 is distraction
    clip1 = VideoFileClip(mainvid)
    clips2 = [VideoFileClip(vid).without_audio().resize(0.75) for vid in extravids]
    clip2 = clips2[random.randint(0,len(clips2)-1)]
    times = process(mainvid, clip2.h, clip2.w, percentile, attentionSpan)
    splits = times.split('s ')
    cliplist = [clip1]
    fps2 = clip2.fps

    for s in splits:
        clip2 = clips2[random.randint(0,len(clips2)-1)]
        data = re.split(r'g\(|,|\) ', s)
        if data[0]=="":
            continue
        start = int(data[0])/fps2
        if (data[3] == ''):
            stop = clip1.duration
        elif (int(data[3])/fps2 - start > clip2.duration):
            stop = int(data[3])/fps2
            while(stop - start > clip2.duration):
                subclipx = clip2.subclip(0, clip2.duration)\
                        .set_start(start)\
                        .set_position((int(data[1]) - clip2.w//2, int(data[2]) - clip2.h//2))
                cliplist.append(subclipx)
                start += clip2.duration
        else:
            stop = int(data[3])/fps2

        subclip2 = clip2.subclip(0, stop-start)\
                        .set_start(start)\
                        .set_position((int(data[1]) - clip2.w//2, int(data[2]) - clip2.h//2))
        cliplist.append(subclip2)

    video = CompositeVideoClip(cliplist)
    video.write_videofile(output)
def splitscreen(mainvid, extravids, output):
    #continuously play  asdsad
    clip1 = VideoFileClip(mainvid)
    clips2 = [VideoFileClip(vid).without_audio().resize(0.75) for vid in extravids]
    clip2 = clips2[random.randint(0,len(clips2)-1)]
    start = 0
    stop = clip1.duration
    cliplist = [clip1]
    while(stop - start > clip2.duration):
        subclipx = clip2.subclip(0, clip2.duration)\
                .set_start(start)\
                .set_position((clip1.w, 0))
        cliplist.append(subclipx)
        start += clip2.duration
    cliplist.append(clip2.subclip(0, clip1.duration - start)\
                .set_start(start)\
                .set_position((clip1.w, 0)))
    video = CompositeVideoClip(cliplist, size=(clip2.w + clip1.w, clip1.h))
    video.write_videofile(output)
if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--mainvid", help="path to main video")
    a.add_argument("--extravid", help="list of paths to distraction videos separated bby commas ")
    a.add_argument("--output", help="path of output video")
    a.add_argument("--percentile", default=70, help="how much of the video should be subway surfers")
    a.add_argument("--attentionSpan", default=300, help="time in between subway surfers")
    a.add_argument("--splitScreen", default=False, help="true to do split screen, false to do on top")
    args = a.parse_args()
    extravids = args.extravid.split(",")
    if (args.splitScreen == "True"):
        splitscreen(args.mainvid, extravids, args.output)
    else:
        edit(args.mainvid, extravids, args.output, int(args.percentile), int(args.attentionSpan))