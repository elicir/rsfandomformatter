Outdated, txt2fandom does not use Karth APIs and other scripts were written before I discovered Karth existed.

**txt2fandom.py usage:**

* python3 caps2transcript.py input.txt -e/-b (-e for event story, -b for bond story)
* outputs to transcript.txt
* no dependencies

* ***when formatting txt file for conversion:***
  * |# Title //starts new "Part" ("Chapter" if bond story)
  * |F Title //Final Part
  * |Bond Level 15 Talk
  * |Bond Level 30 Talk
  * \>subheading
  * \>|subheading but next to main title
  * \>. horizontal break (<hr>)
  * <no speaker (sfx,etc)
  * Name\Line

**yt2frames.sh usage:**
* ./yt2frames.sh "YOUTUBE-URL"
* requires youtube-dl, ffmpeg, and imagemagick
* creates frames/cropped and dumps cropped images in there, then you need to go in and sort and delete unnecessary images before running caps2transcript

**nameline.sh usage:**
* ./nameline.sh
* requires imagemagick
* looks in a directory frames/cropped for all cropped images to be double cropped, makes directory frames/cropped/crop2 and dumps final files in there

**caps2transcript.py usage:**
* python3 caps2transcript.py
* outputs to output.txt
* linux file path '/home/frog/Videos/frames/cropped/crop2/' with all cropped images inside (1 for name, 1 for line), change as necessary for other OS
* requires cv2, pytesseract, and natsort
