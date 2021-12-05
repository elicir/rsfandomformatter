# Revue Starlight Fandom Wiki Page Formatting Scripts

This is a series of command line scripts to format English Revue Starlight Re LIVE data for the [Revue Starlight Fandom Wiki](https://revuestarlight.fandom.com/wiki/Revue_Starlight_Wiki). The scripts create and open text files that can be copy pasted into a new page on the wiki, and make use of the [Project Karthuria](http://karth.top) API (thank you!)

Developed on Windows 10 and have not tested in other environments yet. 

## Requirements:
* Python 3.6+
* [requests API](https://docs.python-requests.org/en/latest/user/install/#install)

## Usage:

For all scripts, the "code" that must be entered is the number in the url on Karthuria, ie. 
* https://karth.top/dress/2040014 -> 2040014 (stage girl/bond story)
* https://karth.top/adventure/1000140001 -> 1000140001 (main story)
* https://karth.top/adventure/5000380001 -> 5000380001 (event story)
* https://karth.top/equip/4000190 -> 4000190 (memoir)

### story.py
* For formatting bond stories, event stories, and main stories
* Creates/overwrites a file `transcript.txt` (or other filename)
* Scene transitions are detected from a fade out effect in the story data, and an `<hr>` is inserted.
  * This can lead to a lot of page breaks where they don't necessarily need to be, so some manual removal based on what seems most appropriate is required.
* [usage](#storypy-command-line-usage)

### sg.py
* For formatting stage girl card pages
* Creates/overwrites a file `sg.txt` (or other filename)
* Downloads the main art into the appropriate filename (ie. `Stage Girl Ichie Otonashi.png`)
* 3D Model and Live2D images have to be created/downloaded separately (I just photoshop a screenshot for the 3D)
* [usage](#sgpy-command-line-usage)

### memoir.py
* For formatting memoir pages
* Creates/overwrites a file `memoir.txt` (or other filename)
* Downloads the main art into the appropriate filename (ie. `Sunny Lunchtime.png`)
* Accounts for names with [ ] in the title that have to be renamed for fandom wiki naming conventions (ie. `XIX Sun [Upright]` -> `XIX Sun -Upright-`)
* [usage](#memoirpy-command-line-usage)

### common.py
* Mappings and common functions/classes used by `sg` and `memoir`

## story.py command line usage:
***bond story***
```
py story.py -dresscode [-a] [-o filename] [--nometa]
```
***event story***
```
py story.py eventstorycode -e numChapters schools [-o filename] [--nometa]
```
***main story***
```
py story.py mainstorycode -m storyTitle numChapters [-o filename] [--nometa]
```
* there must be a `-` before the dresscode
* `-o filename` outputs to `filename` instead of `transcript.txt`
* `--nometa` flag does not append header/footer wiki metadata (useful for incremental main story updates)
* `-a` flag changes "Chapter" to "Part" for Arcana Arcadia Bond Stories and adds relevant header blurb
* `-e numChapters schools` designates number of chapters and which schools are involved in the story:
1. Seisho
2. Rinmeikan
3. Frontier
4. Siegfeld
5. Seiran
* `-m storyTitle numChapters` designates the title of the main story chapter in double quotes and the number of chapters to process starting from the chapter that was entered

examples:
```
py story.py -1070004 -a
py story.py 5000460001 -e 6 1 -o baseball.txt
py story.py 5000470001 -e 12 5 -o threekingdoms.txt
py story.py 1000120001 -m "Curtain Rises - The Journey Begins" 15
py story.py 1000120006 -m "Curtain Rises - The Journey Begins" 5 --nometa
```
## sg.py command line usage:
```
py sg.py dresscode [-o filename] [--lim/bf/season]
```
* `-o filename` outputs to `filename` instead of `sg.txt`
* `--lim` designates if the card is a limited card
* `--bf` designates if the card is a Brilliance Fest card
* `--season` designates if the card is a Season card

examples:
```
py sg.py 1070019 -o helldiver.txt --season
py sg.py 3050008 -o judgement.txt --bf
py sg.py 2040014 --lim
```

## memoir.py command line usage:
```
py memoir.py equipcode [-o filename]
```
* `-o filename` outputs to `filename` instead of `memoir.txt`

examples:
```
py sg.py 4000190
py sg.py 4000202 -o ruibdaymemoir.txt
```
