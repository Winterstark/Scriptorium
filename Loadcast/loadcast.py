from urllib import request
from os import makedirs
from subprocess import call
import re
import sys


if len(sys.argv) < 2:
	print("Missing argument: URL of the RSS feed you want to download.")
	sys.exit(0)
elif len(sys.argv) == 2:
	skip = False
elif len(sys.argv) == 3:
	skip = True
	last_ep = sys.argv[2]

url = sys.argv[1]
src = request.urlopen(url).read().decode("utf-8")

#create dl dir
path = re.findall("<title>(.*?)</title>", src)[0] + "\\"
makedirs(path)

#dl episodes
for ep in re.findall("<enclosure url=\"(http:.*?\.mp3)\"", src):
	filename = ep.split('/')[-1]
	if skip:
		if filename == last_ep:
			skip = False
		continue

	print("Downloading {0}...".format(ep))
	with open(path + filename, "b+w") as f:
		f.write(request.urlopen(ep).read())

call(["explorer", path])