files = ['/Users/johannes/Documents/obama_puppet/segments/2Y/26X3K3HPWBDTLBV2AS7ZHOON3XUTOULWTWDSKZXIGHOTYDIHDA.mp4','/Users/johannes/Documents/obama_puppet/segments/TC/PV2W6ZMA6P6QXLKMIO3VDQ4QGM6D6G3YBZZ52MDIRP6YA2JQ4Q.mp4','/Users/johannes/Documents/obama_puppet/segments/2Y/26X3K3HPWBDTLBV2AS7ZHOON3XUTOULWTWDSKZXIGHOTYDIHDA.mp4','/Users/johannes/Documents/obama_puppet/segments/TC/PV2W6ZMA6P6QXLKMIO3VDQ4QGM6D6G3YBZZ52MDIRP6YA2JQ4Q.mp4']
with open ("/tmp/obama.txt", "w") as f:
    f.writelines(files)
from moviepy.editor import *

videos = []
final_video = None
for f in files:
    videos += [VideoFileClip(f)]
    if len(videos) > 2:
        if not final_video:
            final_video = concatenate(videos)
        else:
            final_video = concatenate([final_video] + videos)
        videos = []
if videos:
    final_video = concatenate([final_video] + videos)
final_video.write_videofile("/tmp/obama_tmp.mp4")


