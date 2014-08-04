from pyomxplayer import OMXPlayer
from threading import Thread
from os.path import isfile
from os import remove
from time import sleep
import urllib
def funct():
	print "hello"
	media_path = "./content/local-media/"
	OMX = None
	while True:
		if isfile("command.txt"):
			with open("command.txt") as file:
				command = file.read().strip()
			print command
			remove("command.txt")
			if command == 'p':				
				OMX.toggle_pause()	
			elif command == 's':
				OMX.stop()
				OMX = None
			elif command == '+30':
				OMX.fast_forward_30()
			elif command == '-30':
				OMX.rewind_30()
			elif command == '+600':
				OMX.fast_forward_600()
			elif command == '-600':
				OMX.rewind_600()
			elif command == '-':
				OMX.decrease_volume()
			elif command == '+':
				OMX.omcrease_volume()
			elif command == 'k':
				OMX.stop()
				return
			else:
				if OMX is not None:
					OMX.stop()
					OMX = None
				OMX = OMXPlayer(media_path+command)
				
		else:
			sleep(.5)
				

def startPublicServer():
	import publicServer
	publicServer.start()

def startPrivateServer():
	import rasptv
	rasptv.start()

def startBrowser():
	from subprocess import Popen
	Popen(["chromium", "--kiosk", "localhost:5000"])

if __name__ =='__main__':
	
	OMXThread = Thread(target=funct)
	PublicServerThread = Thread(target=startPublicServer)
	#PrivateServerThread = Thread(target=startPublicServer)
	#BrowserThread = Thread(target=startBrowser)	
	try:
		PublicServerThread.start()
		PrivateServerThread.start()
		OMXThread.start()
		sleep(2)
		BrowserThread.start()
	except Exception:
		print "in here"
		urllib.urlopen("localhost:5000/112358")
		urllib.urlopen(urllib.urlopen("http://myip.dnsdynamic.org").read()+":5000/112358")
		PublicServerThread.stop()
		with open("command.txt", "w+") as file:
			file.write("k")
		OMXThread.stop()
		PrivateServerThread.stop()
		PublicServerThread.join()
		OMXThread.join()
		PrivateServerThread.join()
	
