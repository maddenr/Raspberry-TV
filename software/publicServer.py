from flask import Flask, render_template, request
import json
import os.path as path
from os import listdir, walk
import socket
from pyomxplayer import OMXPlayer
from threading import Thread

app = Flask(__name__)

app.root_path = path.abspath(path.dirname(__file__)).replace("\\","/")
app.media_path = app.root_path+"/content/local-media"

OMX = None
YTDownload = None

@app.route("/togglepause/")
def togglePause():
	OMX.toggle_pause()
	return render_template("base.json", status = True)
	
@app.route("/loadMedia/<path:mediaPath>")
def loadMedia(mediaPath):
	if OMXPlayer is not None:
		OMX.stop()
	OMX = OMXPlayer(mediaPath, start_playback=True)
	return render_template("base.json", status = True)
	
@app.route("/stop/")
def stop():
	if OMXPlayer is not None:
		OMX.stop()
		OMX = None
	return render_template("base.json", status=True)
	
	
@app.route("/seek/<string:direction>/<int:value>/")
def seek(direction, value):
	if direction == "ff":
		if value == 30:
			OMX.fast_forward_30()
		elif value == 600:
			OMX.fast_forward_600()
	elif direction == "rewind":
		if value == 30:
			OMX.rewind_30()
		elif value == 600:
			OMX.rewind_600()
	else:
		return render_template("base.json", status=False)
	
	return render_template("base.json", status=True)

	
	
#write the path relative to ~, where ~ is the root of the local media folder
@app.route("/listLocalMedia/<path:desiredPath>")
def localMediaFiles(desiredPath):
	desiredPath = desiredPath.replace("~", app.media_path)
	if path.isfile(app.root_path+"/path.txt") is not True:
		return render_template("base.json", status=False, payload='"reason":"no file"')
	files = []
	dirs = []
	for file in listdir(desiredPath):
		if path.isfile(desiredPath+file):
			files.append(file)
		else:
			dirs.append(file)
	fileHeirarchy={'dirs': dirs, 'files' : files}
	jsonData = json.dumps(fileHeirarchy)
	return render_template("base.json", status=True, payload=jsonData[1:-1])#trim ends
	
@app.route("/YTDownload/", methods=['POST'])
	if request is None:
		return render_template("base.json", status=False)
	YTDownload = Popen(["youtube-dl.exe", mediaURL, "-o", "./content/local-media/YouTube Videos/%(title)s.%(ext)s", "--restrict-filenames"])


@app.context_processor
def utility_processor():
	def listLocalMedia(path=app.media_path):
		return listdir(path)
		
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
	
if __name__ == '__main__':
	print "Connect to: "+socket.gethostbyname(socket.gethostname())+":5000"
	#start the web page
	app.run(host="0.0.0.0" )