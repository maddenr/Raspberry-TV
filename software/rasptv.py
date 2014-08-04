from flask import Flask, render_template, abort, send_file, request, redirect
import os.path as path
import os
import re
from subprocess import call, Popen
import json
import pprint
from datetime import date
pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)
app.root_path = path.abspath(path.dirname(__file__)).replace("\\","/")
app.media_path = app.root_path+"/content/local-media"#path.join(app.root_path, "content", "local-media")
#create custom 404 page for friendly faults and then have an ajax for internet connection check (succeed reload old url, failure report)
streams = [ ('localMedia', 'images/local-media-icon.png'),
		('youtube', 'images/youtube-icon.png')  ]

app.download = None

@app.route("/")
#return the app itself
def index():
	return render_template("2col_base.html")
	
	
@app.route("/mediaPlayerAction/<string:action>")
def mediaPlayerAction(action):
#	if action == "play":
#		if mediaPlayer.get_state() == vlc.State.Ended:
#			mediaPlayer.stop()
#		if mediaPlayer.get_state() == vlc.State.Stopped:
#			mediaPlayer.play()
#		else:
#			mediaPlayer.set_pause(False)
#	elif action == "pause":
#		mediaPlayer.set_pause(True)
#	elif action == "stop":
#		mediaPlayer.stop()
#	elif action == "mute":
#		mediaPlayer.audio_set_mute(True)
#	elif action == "unmute":
#		mediaPlayer.audio_set_mute(False)
#	else:
#		return render_template("base.json", status=False)
	return render_template("base.json", status=True)

	
	
	
@app.route("/loadMedia")
def loadMedia():
#	if path.isfile(app.root_path+"/path.txt") is not True:
#		return render_template("base.json", status=False, payload='"reason":"no file"')
		
#	mediaPath = app.media_path+"/"+open(app.root_path+"/path.txt").readline()
	
#	if path.isfile(mediaPath) is not True:
#		return render_template("base.json", status=False, payload='"reason":"media not there"')
#	elif mediaPlayer.get_state() is not vlc.State.Ended:
#		mediaPlayer.stop()
		
#	mediaPlayer.set_media(i.media_new("file:///"+mediaPath))
#	mediaPlayer.play()
#	mediaPlayer.set_fullscreen(True)
	return render_template("base.json", status=True)
	# return JSON response
	#make sure that things are displayed alphabetically, use numbers to sort track numbers... this is where we add tracks to play and album
	
	
@app.route("/setVolume/<int:volume>")
def setVolume(volume):
#	mediaPlayer.audio_set_volume(volume)
	return render_template("base.json", status=True)
	
	
@app.route("/skipPlaybackInterval/<string:direction>")
def skipPlayback(direction):
#	if mediaPlayer.get_state() == vlc.State.NothingSpecial:
#		return render_template("base.json", status=False)
	
	#mediaPlayer.set_pause(True)
#	if direction == "forward":
#		mediaPlayer.set_time(mediaPlayer.get_time()+300000)
#	elif direction == "backward":
#		mediaPlayer.set_time(mediaPlayer.get_time()-300000)
	#if it changes state to ended that means it went too far in a direction... I think
#	mediaPlayer.set_pause(False)
	
	return render_template("base.json", status=True)
	
	
	
	
	
	
#-------------------------------------------------------------------------
	
@app.route("/YTDownload")
def YTDownload():
	if path.isfile(app.root_path+"/path.txt") is not True:
		return render_template("base.json", status=False)
	
	mediaURL = open(app.root_path+"/path21.txt").readline()
	
	#verify url!
	#create lock file
	#popen?
	
	app.download = Popen(["youtube-dl.exe", mediaURL, "-o", "./content/local-media/YouTube Videos/%(title)s.%(ext)s", "--restrict-filenames"])
	return render_template("base.json", status=True)
	#start the download and set the path.txt to the path. Create lock file for polling, TY.lock. Delete when done....
	#maybe jut tell by weather the video is in the correct place. this then would need to be async.
	#Could also have a buffering gif and have it say that it will appear in the folder and they should select it
	
@app.route("/isDownloading")
def isDownloading():
	if app.download is None:
		return render_template("base.json", status=False)
	if app.download.poll() is None:
		result = "true"
	else:
		result = "false"
	return render_template("base.json", status=False, payload='"isDownloading":'+result)
	
	
	
@app.route("/weatherColumn", methods=['GET', 'POST'])
def weatherColumn():
	if request is None:
		print "blah"
		return render_template("base.json", status=False)
	else:
		today = date.today()
		forcastDays = [
			date.fromordinal(today.toordinal()+6).strftime("%A"),
			date.fromordinal(today.toordinal()+5).strftime("%A"),
			date.fromordinal(today.toordinal()+4).strftime("%A"),
			date.fromordinal(today.toordinal()+3).strftime("%A"),
			date.fromordinal(today.toordinal()+2).strftime("%A"),
			date.fromordinal(today.toordinal()+1).strftime("%A"),
			today.strftime("%A, %d. %B %Y")
		]
		return render_template("weatherColumn.html", weatherData=json.loads(request.form['data']), forcastDays = forcastDays)#

@app.route("/112358")
def fib():
	request.environ.get('werkzeug.server.shutdown')()
	return
	
	
@app.context_processor
def utility_processor():
	def listLocalMedia(path=app.media_path):
		return os.listdir(path)
		
	def getFileExt(path):
		filePath, fileExt = path.splittext(path)
		return fileExt
		
	def jsonSuccessEval(bool):
		if bool:
			return "true"
		elif not bool:
			return "false"
		else:
			return '"template error"'
		
	return dict(
		getFileExt=getFileExt,
		listLocalMedia=listLocalMedia,
		jsonSuccessEvaluation=jsonSuccessEval
	)
def start():
	app.run()

if __name__ == '__main__':
	start()
