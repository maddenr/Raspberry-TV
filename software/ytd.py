from subprocess import Popen
from sys import argv
from shutil import move
from time import sleep
from os import listdir

if __name__ == '__main__':
	YTD = Popen(["youtube-dl", argv[1], "-o", "./tmp/%(title)s.%(ext)s", "--restrict-filenames"])
	while YTD.poll() is None:
		sleep(1)

	for file in listdir("./tmp"):
		move("./tmp/"+file, "./content/local-media/YouTube Videos/"+file)
