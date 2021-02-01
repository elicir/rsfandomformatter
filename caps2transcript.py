import cv2
import pytesseract
import os
from natsort import os_sorted

path = '/home/frog/Videos/frames/cropped/crop2/'
i = 0
listdir = os_sorted(os.listdir(path))

with open("output.txt", "w") as create:
    pass

while i < len(listdir):
    f_name_img = listdir[i]
    name_img = cv2.imread(path+f_name_img, 0)
    name_text = pytesseract.image_to_string(name_img)
    name = name_text.rstrip()

    f_line_img = listdir[i+1]
    line_img = cv2.imread(path+f_line_img, 0)

    dsize = (int(line_img.shape[1] * 1.1), line_img.shape[0])
    line_img2 = cv2.resize(line_img, dsize, interpolation=cv2.INTER_AREA)
    line_text = pytesseract.image_to_string(line_img2)
    line = line_text.rstrip().replace('\n', ' ').replace('|', 'I').replace(' l ', ' I ').replace('}', '♪')
    i += 2

    with open('output.txt', 'a') as f_out:
        f_out.write(name + '\\' + line + '\n')
