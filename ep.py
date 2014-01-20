SENDTO_PATH = "C:\\"
#edit this value to change the destination directory
#use double backslashes (eg. "c:\\videos\\series")

NAME = "s%s%e%e% - %title%"
#this value sets the episode file naming convention
#use the following variables::
#%show% - show name
#%SHOW% - CAPITALIZED SHOW NAME
#%title% - episode title
#%s% - season number, e.g. s3
#%ss% - two-digit season number, e.g. s03
#%e% - episode number, e.g. e4
#%ee% - two-digit episode number, e.g. e04


import sys
import re
from os import listdir, makedirs
from os.path import isfile, splitext, exists, dirname, basename
from shutil import move
from urllib import request
from bs4 import BeautifulSoup

if SENDTO_PATH[len(SENDTO_PATH)-1] != "\\": SENDTO_PATH += "\\"

path = sys.argv[1]

info = re.findall(".*[\\\\-] *(.*)\.S(\d*)E(\d*)", path)[0]
show = info[0].replace(".", " ")
s = info[1]
e = info[2]
print(show, "s" + s + "e" + e)

#print("url: ", "http://www.tvrage.com/" + show.replace(" ", "_") + "/episode_list/" + s)
src = request.urlopen("http://www.tvrage.com/" + show.replace(" ", "_") + "/episode_list/" + s).read()

if "tvr_oops_alpha" in str(src):
    if show[-5:-4] == ' ' and show[-4:].isdigit():
        show = show[:-5]
        src = request.urlopen("http://www.tvrage.com/" + show.replace(" ", "_") + "/episode_list/" + s).read()

        if "tvr_oops_alpha" in str(src):
            print("Show not found on tvrage.com. Press enter to exit.")
            input()
            sys.exit(0)
            

soup = BeautifulSoup(src)

if "Episode List" not in str(soup.title):
    print("Error: show not found on TVRage.com.")
    print("Press any key to exit...")
    input()
    sys.exit(0)

title = soup.find_all(id="brow")[int(e)-1].text.split("\n")[4]
title = " ".join(title.split())
print(title)

if not isfile(path):
    #dir
    newPath = SENDTO_PATH + "_" + basename(path)
    move(path, newPath)
    path = newPath + "\\" + [f for f in listdir(newPath) if re.match(".*[sS]\d+[eE]\d+.*", f)][0]

dest = SENDTO_PATH + NAME.replace("%show%", show).replace("%SHOW%", show.upper()).replace("%title%", title).replace("%s%", str(int(s))).replace("%ss%", s).replace("%e%", str(int(e))).replace("%ee%", e) + splitext(path)[1]
if not exists(dirname(dest)): makedirs(dirname(dest))

move(path, dest)

print("Press any key to exit...")
input()
