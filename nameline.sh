#!/bin/bash
cd frames/cropped
mkdir crop2
for f in *.png; do
    convert "$f" +repage -crop 380x45+93+25 crop2/"${f/.png/-01.png}" 
    convert "$f" +repage -crop 1040x110+72+88 crop2/"${f/.png/-02.png}"
done
