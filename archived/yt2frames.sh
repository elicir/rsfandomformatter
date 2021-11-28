#!/bin/bash
URL=$1

mkdir frames
youtube-dl -f 136 -o video.mp4 "$URL"
ffmpeg -skip_frame nokey -i video.mp4 -vsync 0 -frame_pts true frames/out%d.png
cd frames
mkdir cropped
for f in *.png; do
    convert "$f" -crop 1280x240+0+480 cropped/"$f" 
done
rm *.png
