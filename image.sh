#!/bin/bash

# Define the directory for your project
# Define the output file names
video_output="slackviz.mp4"
image_output="slackviz.png"

# Generate the Gource video
gource -s 0.1 \
--font-scale 1 \
--file-font-size 10 \
--elasticity 0.1 \
--camera-mode overview \
repo -3840x2160  -o - | ffmpeg -y -r 1 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 $video_output


# Get the total number of frames in the video
total_frames=$(ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 $video_output)

# Subtract 1 because frame count starts at 0
last_frame=$((total_frames - 1))

# Extract the last frame
ffmpeg -i $video_output -vf "select=eq(n\,$last_frame)" -vframes 1 $image_output

