from moviepy.editor import *


def extract_wave_from_mp4(mp4_filename, wave_filename):
    mp4_file = VideoFileClip(mp4_filename)
    mp4_file.audio.write_audiofile(wave_filename)
