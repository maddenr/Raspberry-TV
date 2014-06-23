from flask import Flask, render_template, abort, send_file
import os.path as path
import os
import re
import vlc
app = Flask(__name__)
app.root_path = path.dirname(__file__)#path.abspath(path.dirname(__file__))
app.media_path = app.root_path+"/content/local-media"#path.join(app.root_path, "content", "local-media")
#create custom 404 page for friendly faults and then have an ajax for internet connection check (succeed reload old url, failure report)
streams = [ ('localMedia', 'images/local-media-icon.png'),
		('youtube', 'images/youtube-icon.png')  ]
		
i = vlc.Instance()
mediaPlayer = i.media_player_new()


@app.route("/")
#return the app itself
def index():
	return render_template("2col_base.html")
	
	
@app.route("/mediaPlayerAction/<string:action>")
def mediaPlayerAction(action):
	if action is "fullscreen":
		mediaPlayer.toggle_fullscreen()
	elif action is "play":
		if mediaPlayer.get_state() is vlc.State.Ended:
			mediaPlayer.stop()
		mediaPlayer.set_pause(False)
	elif action is "pause":
		mediaPlayer.set_pause(True)
	elif action is "stop":
		mediaPlayer.stop()
	elif action is "mute":
		mediaPlayer.audio_set_mute(True)
	elif action is "unmute":
		mediaPlayer.audio_set_mute(False)
		
	
@app.route("/loadMedia")
def loadMedia():
	mediaPath = open(path.join(app.root_path,"path.txt")).readLine()
	if path.isfile(mediaPath) is not True:
		abort(404)
	elif mediaPlayer.get_state() is not vlc.State.Ended:
		mediaPlayer.stop()
	mediaPlayer.set_media(i.media_new("file:///"+app.media_path+"/"+mediaPath))
	mediaPlayer.play()
	#make sure that things are displayed alphabetically, use numbers to sort track numbers... this is where we add tracks to play and album
	
	
@app.route("/setVolume/<int:volume>")
def setVolume(volume):
	mediaPlayer.audio_set_volume(volume)
	
	
@app.route("/skipPlaybackInterval/<string:direction>")
def setVolume(volume):
	mediaPlayer.set_pause(True)
	if direction is "forward":
		mediaPlayer.set_time(mediaPlayer.getTime()+300000)
	elif direction is "backward"
		mediaPlayer.set_time(mediaPlayer.getTime()-300000)
	#if it changes state to ended that means it went too far in a direction... I think
	mediaPlayer.set_pause(False)
	
	
	
	
	
	
#-------------------------------------------------------------------------
	
@app.route("/YTDownload")
def YTDownload():
	return None #start the download and set the path.txt to the path. Create lock file for polling, TY.lock. Delete when done....
	#maybe jut tell by weather the video is in the correct place. this then would need to be async.
	#Could also have a buffering gif and have it say that it will appear in the folder and they should select it
	
@app.route("/isDownloading")
def isDownloading():
	if path.isfile(app.root_path+"/TY.lock")
		
	
	
	
	
	
	
	
	
	
	#DEPRECIATED!!
# @app.route("/localMedia/<path:mediaPath>")
# #return the proper local media		depreciated? use modal window
# def getLocalMedia(mediaPath):
	# mediaPath = path.join(app.media_path, mediaPath)
	# print "BLAHHHHHHH"
	# print mediaPath
	# if path.isfile(mediaPath) is False:
		# print "rugs"+str(path.isfile(mediaPath))
		# abort(404)
	# else:
		# print mediaPath.replace('\\','/')
		# return app.send_static_file("wazzlejazzlebof.mp3")#send_file(mediaPath, cache_timeout=600)
		

		#DEPRECIATED!!
# @app.route("/modalWindow/<string:type>")
# #return the proper local media
# #give path in POST
# def getModalWindow(type):
	# print path.join(app.root_path,"path.txt")
	# if path.isfile(path.join(app.root_path,"path.txt")) is False:
		# abort(404)
	# file = open("path.txt")
	# return render_template(type+"Modal.html", path="localMedia/"+file.readline())#might have /n at the end

#list local media handler
# 1 level deep for now... can do more folders later
#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
@app.context_processor
def utility_processor():
    def listLocalMedia(path=app.media_path):
        return os.listdir(path)
    return dict(
		listLocalMedia=listLocalMedia
	)
	
@app.context_processor
def utility_processor():
    def getFileExt(path):
		filePath, fileExt = path.splittext(path)
		return fileExt
    return dict(
		getFileExt=getFileExt
	)
	
if __name__ == '__main__':
	app.run(debug=True)