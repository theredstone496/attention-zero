import argparse
import re
from moviepy.editor import *

from pixel import process

# example use: python videoedit.py --mainvid "ricardo.mp4" --extravid "..\subway-surfers\part0new.avi" --output "richard.mp4"

def edit(mainvid, extravid, output, percentile, attentionSpan):
    # clip1 is main, clip2 is distraction
    clip1 = VideoFileClip(mainvid).without_audio()
    clip2 = VideoFileClip(extravid).without_audio().resize(0.75)

    splits = process(mainvid, clip2.h, clip2.w, percentile, attentionSpan).split('s ')
    cliplist = [clip1]
    fps2 = clip2.fps

    for s in splits:
        data = re.split(r'g\(|,|\) ', s)

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

    video = CompositeVideoClip(cliplist).without_audio()
    cliplist = [video]
    start = 0
    stop = clip1.duration
    while(stop - start > clip2.duration):
        subclipx = clip2.subclip(0, clip2.duration)\
                .set_start(start)\
                .set_position(clip1.w, 0)
        cliplist.append(subclipx)
        start += clip2.duration
    video.write_videofile(output)
def splitscreen(mainvid, extravid, output):
    #continuously play
    clip1 = VideoFileClip(mainvid).without_audio()
    clip2 = VideoFileClip(extravid).without_audio().resize(0.75)
    cliplist = [[clip1], [clip2]]
    video = CompositeVideoClip.clips_array(cliplist)
    video.write_videofile(output)
if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--mainvid", help="path to main video")
    a.add_argument("--extravid", help="path to distraction video")
    a.add_argument("--output", help="path of output video")
    a.add_argument("--percentile", default=70, help="how much of the video should be subway surfers")
    a.add_argument("--attentionSpan", default=300, help="time in between subway surfers")
    a.add_argument("--splitScreen", type=bool, default=False, help="true to do split screen, false to do on top")
    args = a.parse_args()
    if (args.splitScreen):
        splitscreen(args.mainvid, args.extravid, args.output)
    else:
        edit(args.mainvid, args.extravid, args.output, args.percentile, args.attentionSpan)