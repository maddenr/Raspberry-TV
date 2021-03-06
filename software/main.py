from pyomxplayer import OMXPlayer
from threading import Thread
from os.path import isfile
from os import remove
from time import sleep
import urllib
def funct():
	print "Start OMXPlayer Thread"
	media_path = "./content/local-media/"
	OMX = None
	while True:
		if isfile("command.txt"):
			with open("command.txt") as file:
				command = file.read().strip()
			remove("command.txt")
			if OMX is None and command in ['p', 's', '-30', '+30', '+600', '-600', '-', '+']:
				print "OMXPlayer not started, load media first"
				continue
			else:
				print "Command: %s" % command
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
				OMX.increase_volume()
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


def startBrowser():
	from subprocess import Popen
	Popen(["chromium", "--kiosk", "localhost:5000"])



if __name__ =='__main__':
	if isfile("command.txt"):
		remove("command.txt")
	OMXThread = Thread(target=funct)
	PublicServerThread = Thread(target=startPublicServer)
	BrowserThread = Thread(target=startBrowser)	
	try:
		PublicServerThread.start()
		OMXThread.start()
		sleep(4)
		BrowserThread.start()
	except Exception as e:
		print "********************"
		print e
		print "********************"
		with open("command.txt", "w+") as file:
			file.write("k")
		PublicServerThread.stop()
		OMXThread.stop()
		PublicServerThread.join()
		OMXThread.join()

