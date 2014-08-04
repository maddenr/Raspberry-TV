from flask import Flask, render_template, request
import json
import os.path as path
from os import listdir, walk
import socket
from threading import Thread
from subprocess import Popen, PIPE
from time import sleep
import urllib
app = Flask(__name__)


app.root_path = path.abspath(path.dirname(__file__)).replace("\\","/")
app.media_path = app.root_path+"/content/local-media"

YTDownload = None
myIP = None

@app.route("/")
#return the app itself
def index():
	if request.remote_addr != "127.0.0.1":
		abort(403)
	#add IP
	return render_template("2col_base.html")

@app.route("/weatherColumn", methods=['GET', 'POST'])
def weatherColumn():
	if request is None or request.remote_addr != "127.0.0.1":
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



@app.route("/togglepause/")
def togglePause():
	if path.isfile("command.txt"):
		sleep(.700)
	with open("command.txt", "w+") as file:
		file.write("p")
	return render_template("base.json", status = True)
	
@app.route("/loadMedia/<path:mediaPath>")
def loadMedia(mediaPath):
	if path.isfile("command.txt"):
		sleep(.700)
	print app.media_path+"/"+mediaPath
	with open("command.txt", "w+") as file:
		file.write(mediaPath)

	return render_template("base.json", status = True)
	
@app.route("/stop/")
def stop():
	if path.isfile("command.txt"):
		sleep(.700)
	with open("command.txt", "w+") as file:
		file.write("s")
	
	return render_template("base.json", status=True)
	
	
@app.route("/seek/<string:direction>/<int:value>/")
def seek(direction, value):
	if path.isfile("command.txt"):
		sleep(.700)

	if direction == "ff":
		if value == 30:
			command = "+30"
		elif value == 600:
			command = "+600"
	elif direction == "rewind":
		if value == 30:
			command = "-30"
		elif value == 600:
			command = "-600"
	else:
		return render_template("base.json", status=False)
	with open("command.txt", "w+") as file:
		file.write(command)

	return render_template("base.json", status=True)

@app.route("/increaseVolume/")
def incVol():
	if path.isfile("command.txt"):
		sleep(.700)
	with open("command.txt", "w+") as file:
		file.write("+")

	return render_template("base.json", status=True)


@app.route("/decreaseVolume/")
def decVol():
	if path.isfile("command.txt"):
		sleep(.700)
	with open("command.txt", "w+") as file:
		file.write("-")

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
def YTDownload():
	if request is None:
		return render_template("base.json", status=False)
	mediaURL = app.media_path+"/"+request.form['url']
	YTDownload = Popen(["youtube-dl", mediaURL, "-o", "./content/local-media/YouTube Videos/%(title)s.%(ext)s", "--restrict-filenames"])
	return render_template("base.json", status=True)

@app.route("/isConnected/")
def isConnected():
	#remove the not connected file
	return render_template("base.json", success=True)

@app.route("/112358")
def fib():
	with open("command.txt", "w+") as file:
		file.write("k")
	request.environ.get('werkzeug.server.shutdown')()
	return

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

def start():
	global myIP
	myIP = urllib.urlopen("http://myip.dnsdynamic.org").read()
	print "Connect to: "+myIP+":5000"
	app.run(host="0.0.0.0")

if __name__ == '__main__':

	#create not connected file
	#start the web page
	#app.run(host="0.0.0.0" )
	start()
