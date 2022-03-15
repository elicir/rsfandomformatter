import sys, os
from common import NAMES, SCHOOLS, get_story, get_chara_names, get_dress, write_line

# init constants
CHAR_TALK = "{{CharTalk|"
END_CURLY_BRACES = "}}"
NEW_PART = "|-|\n"
TITLE_BOND = "Chapter "
TITLE_STORY = "Part "
TITLE_STORY_FINAL = "Final Part";
TITLE = "<span style=\"font-weight: bold; font-size: 20px;\" >"
END_SPAN = "</span>"
SUBTITLE = "<br><span style=\"font-weight: bold; font-size: 16px;\" >"
DIVIDER = "<hr>"
QUOTE = "{{Quote|"
CATEGORY = "[[Category:"
END_SQUARE_BRACES = "]]"
TABBER = "<tabber>"
TABBER_END = "</tabber>"
BOND_STORIES = "Bond Stories"
MAIN_STORIES = "Main Stories"
EVENT_STORIES = "Event Stories"
STORIES = "Stories"
TRANSCRIPTS = "Transcripts"
ARCANA = "''(Part 1 and Part 2 of [[Shōjo☆Kageki Revue Starlight: Re LIVE/Story#Third Part: Arcana Arcadia|Arcana Arcadia]] Stage Girl bond stories are viewable in the Gallery under [[Shōjo☆Kageki Revue Starlight: Re LIVE/Story#Intermission|Arcana Arcadia - Intermission]].)''"

class Story:
    filename = ""
    type = ""
    code = -1
    extra_args = {}
    no_meta = False

    def __init__(self, filename, type, code, extra_args, no_meta):
        self.filename = filename
        self.type = type
        self.code = code
        self.extra_args = extra_args
        self.no_meta = no_meta

    def __write(self, line: str):
        write_line(self.filename, line)

    def __process_main(self):
        if not self.no_meta:
            print("writing header")
            header = ""
            header += "==Transcript==\n" + TABBER
            self.__write(header)
        new_code = int(self.code)
        print("writing transcript")
        for _ in range(self.extra_args['num_chapters']):
            num = str(new_code % 100)
            line = NEW_PART + TITLE_STORY + num + "=\n" + TITLE + self.extra_args['story_title'] + \
                END_SPAN + " " + SUBTITLE[4:] + TITLE_STORY + num + END_SPAN
            self.__write(line)
            self.__process_script(str(new_code))
            new_code += 1
        if not self.no_meta:
            print("writing footer")
            footer = ""
            footer += TABBER_END + "\n" + CATEGORY + MAIN_STORIES + END_SQUARE_BRACES
            self.__write(footer)

    def __process_event(self):
        if not self.no_meta:
            print("writing header")
            header = ""
            header += TABBER;
            self.__write(header)
            new_code = int(self.code);
        print("writing transcript")
        for i in range(self.extra_args['num_chapters']):
            num = str(new_code % 100)
            if (i == self.extra_args['num_chapters']-1):
                self.__write(NEW_PART + TITLE_STORY_FINAL + "=")
            else:
                self.__write(NEW_PART + TITLE_STORY + num + "=")
            self.__process_script(str(new_code))
            new_code += 1
        if not self.no_meta:
            print("writing footer")
            footer = ""
            footer += TABBER_END + "\n" + CATEGORY + EVENT_STORIES + END_SQUARE_BRACES
            for char in str(self.extra_args['schools']):
                footer += "\n" + CATEGORY + SCHOOLS[int(char)] + ' ' + STORIES + END_SQUARE_BRACES
            footer += "\n" + CATEGORY + TRANSCRIPTS + END_SQUARE_BRACES
            self.__write(footer)

    def __process_bond(self):
        code = self.code[1:]
        if not self.no_meta:
            print("writing header")
            dress = get_dress(code)
            header = ""
            profile = dress["basicInfo"]["profile"]["en"]
            header += QUOTE + profile + END_CURLY_BRACES
            if self.extra_args['is_arcana']:
                header += "\n" + ARCANA
            header += "\n" + TABBER
            self.__write(header)
        print("writing transcript")
        for i in range(4):
            new_code = ""
            if i+1 < 3: # chapter/part 1 and 2
                title = TITLE_STORY if self.extra_args['is_arcana'] else TITLE_BOND
                self.__write(NEW_PART + title + str(i+1) + "=")
                new_code = "30" + code + str(i+1)
            elif i+1 == 3:
                self.__write(NEW_PART + "Bond Level 15 Talk=")
                new_code = "31" + code + "1"
            elif i+1 == 4:
                self.__write(NEW_PART + "Bond Level 30 Talk=")
                new_code = "31" + code + "2"
            self.__process_script(new_code)
        if not self.no_meta:
            print("writing footer")
            footer = ""
            footer += TABBER_END + "\n" + CATEGORY + BOND_STORIES + END_SQUARE_BRACES
            footer += "\n" + CATEGORY + NAMES[int(code[:3])] + " " + BOND_STORIES + END_SQUARE_BRACES
            footer += "\n" + CATEGORY + TRANSCRIPTS + END_SQUARE_BRACES
            self.__write(footer)

    def __process_script(self, code):
        print(code)
        story = get_story(code)
        chara_names = get_chara_names()
        out_line = ""
        for key in story["script"]:
            out_line = ""
            item = story["script"][key]
            if not isinstance(item, str):
                type = item["type"]
                args = item["args"]
                if isinstance(args, list):
                    continue
                if type == "message":
                    name_id = args["nameId"]
                    chara_id = args["characterId"]
                    characters = story["setting"]["character"]
                    if name_id != 0:
                        # single speaker identifiable from chara names json
                        out_line, name = self.__format_line_chara_name(chara_names, args, name_id)
                        if isinstance(chara_id, int): # ie. All does not need role check
                            live2d_name = self.__get_name_live2d(chara_id, chara_names, characters)
                            if live2d_name: # live2d_name is None if it is not a stage girl
                                if isinstance(chara_id, int) and 0 < chara_id <= len(characters) and live2d_name not in name:
                                    real_name = self.__get_name_live2d(chara_id, chara_names, characters)
                                    out_line = out_line.replace(name + '|', real_name + '|')
                                    out_line = out_line.replace(END_CURLY_BRACES, '|' + name + END_CURLY_BRACES)
                    elif isinstance(chara_id, int):
                        if chara_id == 0:
                            # sound effect
                            out_line = CHAR_TALK + "|" + args["body"]["en"] + END_CURLY_BRACES
                        else:
                            # single speaker identifiable from live2d
                            name = self.__get_name_live2d(chara_id, chara_names, characters)
                            out_line = CHAR_TALK + name + "|" + args["body"]["en"] + END_CURLY_BRACES
                    elif isinstance(chara_id, list):
                        # multiple speakers identifiable from live2ds
                        name = "";
                        for chara in chara_id:
                            chara_name = self.__get_name_live2d(chara, chara_names, characters)
                            name += chara_name + " & "
                            out_line = CHAR_TALK + name[:-3] + "|" + args["body"]["en"] + END_CURLY_BRACES
                elif type == "showTitle":
                    temp_title = SUBTITLE
                    if key == "3" or key == "4":
                        temp_title = TITLE
                    out_line = temp_title + args["body"]["en"] + END_SPAN
                elif type == "fadeOut":
                    out_line = DIVIDER
                if out_line != "":
                    write_line(self.filename, out_line)
        return True

    def __get_name_live2d(self, chara_id, chara_names, characters):
        code = str(characters[chara_id-1])[:3]
        if code not in chara_names:
            return None
        else: 
            return str(chara_names[code]["en"])

    def __format_line_chara_name(self, chara_names, args, name_id):
        name = chara_names[str(name_id)]["en"]
        speech = args["body"]["en"]
        if '(' in name:
            b = name.index('(')
            speech = "'''(" + name[(b + 1):] + "'''<br>" + speech
            name = name[:(b - 1)]
        out_line = CHAR_TALK + name + "|" + speech + END_CURLY_BRACES
        return out_line, name

    def write_file(self):
        if self.type == "main":
            self.__process_main()
        elif self.type == "event":
            self.__process_event()
        elif self.type == "bond":
            self.__process_bond()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("py story.py -dresscode [-a] [-o filename] [--nometa]")
        print("py story.py eventstorycode -e numChapters schools [-o filename] [--nometa]")
        print("py story.py mainstorycode -m storyTitle numChapters [-o filename] [--nometa]")
        exit(1)

    code = sys.argv[1]

    filename = "transcript.txt"
    no_meta = False
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-o":
            filename = sys.argv[i + 1]
        if sys.argv[i] == "--nometa":
            no_meta = True

    extra_args = {}
    if code[0] == '1':
        # Main Story: name of story and number of chapters to process should be provided after argument "-m"
        story_type = "main"
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-m":
                extra_args['story_title'] = sys.argv[i + 1]
                extra_args['num_chapters'] = int(sys.argv[i + 2])
    elif code[0] == '5':
        # Event Story: chapters provided as arg after -e ie. 6, 12 . after that schools involved ie. 13 = seisho frontier
        story_type = "event"
        extra_args['num_chapters'] = 6
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-e":
                extra_args['num_chapters'] = int(sys.argv[i + 1])
                extra_args['schools'] = int(sys.argv[i + 2])
    elif code[0] == '-':
        # Bond Story: 30{code}1,30{code}2 are Chapter 1,2 ; 31{code}1,31{code}2 are Bond Level 15 Talk, Bond Level 30 Talk
        story_type = "bond"
        extra_args['is_arcana'] = False
        for arg in sys.argv:
            if arg == "-a":
                extra_args['is_arcana'] = True
    else:
        print("Code is incorrect (not beginning with -, 3, or 5)")
        exit(1)

    with open(filename, "w", encoding="utf-8") as create:
        pass

    story = Story(filename, story_type, code, extra_args, no_meta)
    story.write_file()

    os.startfile(filename)