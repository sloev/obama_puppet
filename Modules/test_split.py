import sys
from split_mp4 import split_to_list

if len(sys.argv)<3:
    sys.exit()

video_filename = sys.argv[1]
grid_filename = sys.argv[2]
output_root = "/Users/johannes/Documents/advanceret_database/segments/"
print "[list]"
print split_to_list(video_filename, grid_filename, output_root)
