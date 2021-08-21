# fandomstoryformatter

**t2f.exe command line usage:**
* t2f.exe -dresscode [-a] ***bond story***
* t2f.exe storycode -e 12345 ***event story***
* t2f.exe storycode -m storyTitle numChapters ***main story***
* ***-o filename*** outputs to filename instead of transcript.txt
* ***--nometa*** flag does not append header/footer wiki metadata (useful for main story updates)
* ***-a*** flag changes "Chapter" to "Part" for Arcana Arcadia Bond Stories
* ***-e*** designates which schools are involved in the story
1. Seisho
2. Rinmeikan
3. Frontier
4. Siegfeld
5. Seiran

sample:
```
t2f.exe -1070004 -a
t2f.exe 5000460001 -e 1 -o baseball.txt
t2f.exe 1000120001 -m "Curtain Rises - The Journey Begins" 15
t2f.exe 1000120006 -m "Curtain Rises - The Journey Begins" 5 --nometa
```

***TODO: make a batch file template to use for things like events***


vvv Now mostly defunct vvv

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
  * \>.empty line (br)
  * <no speaker
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
