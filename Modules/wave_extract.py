from moviepy.editor import *


def extract_wave(mp4_filename, wave_filename):
    print mp4_filename, wave_filename
    mp4_file = VideoFileClip(mp4_filename)
    print mp4_file.audio.write_audiofile(wave_filename, codec="pcm_s16le", bitrate="22k", ffmpeg_params=['-ac', '1'])

if __name__ == "__main__":
    import sys, os
    p = os.path.abspath(sys.argv[1])
    print p
    extract_wave(p, os.path.splitext(p)[0]+".wav")
