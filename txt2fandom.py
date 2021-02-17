import sys
import re

chartalk1 = "{{CharTalk|"
chartalk2 = "}}"
new_part = "|-|\n"
if sys.argv[2] == "-e":
    title1 = "Part "
else:
    title1 = "Chapter "
title1final = "Final Part"
title2 = '=\n<span style="font-weight: bold; font-size: 20px;" >'
title_end = '</span>'
subtitle1 = '<br><span style="font-weight: bold; font-size: 16px;" >'

with open("transcript.txt", "w") as create:
    pass

f = open(sys.argv[1], "r")
for line in f:
    line = line.rstrip()
    if line[0] == "|":
        num = line[1]
        if num == "F" and line[2] == " ":
            new = new_part + title1final + title2 + line[3:] + title_end
        elif num.isdigit():
            new = new_part + title1 + num + title2 + line[3:] + title_end
        else:
            new = new_part + line[1:] + "="
    elif line[0] == ">":
        if line[1] == "|":
            new = title2[2:] + line[2:] + title_end
        elif line[1] == ".":
            new = "<br>"
        else:
            new = subtitle1 + line[1:] + title_end
    elif line[0] == "<":
        new = chartalk1 + "|" + line[1:] + chartalk2
    else:
        i = line.find('\\')
        name = line[:i]
        speech = line[i+1:]
        b = name.find('(')
        if b != -1:
            speech = "'''(" + name[b+1:] + "'''<br>" + speech
            name = name[:b-1]
        if name == "Mei Fan":
            name = "Meifan"
        new = chartalk1 + name + "|" + speech + chartalk2
    with open('transcript.txt', 'a') as transcript:
        transcript.write(new + '\n')
f.close()



