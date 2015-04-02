import shutil
import os
from hash_helper import file_to_b32_hash

from textgrid import TextGrid
from moviepy.editor import *

def split_to_list(mp4_filename, textgrid_filename, output_root_dir):
    tmp_mp4_filename = "/tmp/obama_segmenter.mp4"
    textgrid_abs_filename = os.path.abspath(textgrid_filename)
    textgrid = TextGrid.fromFile(textgrid_abs_filename)
    textgrid = textgrid[len(textgrid)-1]

    original_videoclip = VideoFileClip(mp4_filename)

    counter = 0

    query_list = []

#    print "files loaded into video splitter"

    for interval in textgrid:
        if counter>5: break
        interval_string = str(interval)
        beginning, end, mark = interval_string[interval_string.find("(") + 1 : interval_string.find(")")].split(",")
        beginning = float(beginning)
        end = float(end)
    #    print beginning, end, mark
        mark = mark.split()[0]
        if mark != "sil":
            if mark == "sp":
                mark = "SILENT_SPACE"
            new_clip = original_videoclip.subclip(beginning, end)
            print beginning, end, mark, new_clip
            new_clip.to_videofile(tmp_mp4_filename)
            try:
                hash_string = file_to_b32_hash(tmp_mp4_filename)
            except:
                continue
            new_dir = hash_string[:2]

            new_filename = new_dir + "/" + hash_string[2:] + ".mp4"
            if not os.path.exists(output_root_dir + new_dir):
                os.makedirs(output_root_dir + new_dir)
            shutil.move(tmp_mp4_filename, output_root_dir + new_filename)
            duration = end - beginning
            values = [counter, mark, beginning, end, duration, new_filename]
            #query_list += [{"seq_number" : counter, "mark" : mark, "beginning" : beginning, "end" : end, "duration" : duration, "relative_filepath" : new_filename}]
            query_list += [values]
            counter += 1
        else:
            pass
 #           print "error with mark:"+mark
    return query_list

