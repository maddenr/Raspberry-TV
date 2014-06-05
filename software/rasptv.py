from flask import Flask, render_template
import os.path as path
import os
import re

app = Flask(__name__)
app.root_path = path.abspath(path.dirname(__file__))
app.media_path = path.join(app.root_path, "content", "local-media")
#create custom 404 page for friendly faults and then have an ajax for internet connection check (succeed reload old url, failure report)
streams = [ ('localMedia', 'images/local-media-icon.png'),
		('youtube', 'images/youtube-icon.png')  ]

@app.route("/")
#return the app itself
def index():
	return render_template("2col_base.html")
	
	
@app.route("/youtube/*")
#return a streaming service template
def getYoutubeService():
	return "TODO2"
	
	
@app.route("/localMedia/<path:mediaPath>")
#return the proper local media		depreciated? use modal window
def getLocalMedia(mediaPath):
	mediaPath = path.join(app.media_path, mediaPath)
		
	if path.isfile(mediaPath) is not True:
		abort(404)
	else:
		return "TODO3" #render local streaming template
		

@app.route("/modalWindow/<string:type>")
#return the proper local media
#give path in POST
def getModalWindow(type):
	return render_template(type+"Modal.html", path=request.form['path'])

#list local media handler
# 1 level deep for now... can do more folders later
#------------------------------------------------------------------------------------------

	
@app.route("/weather/*")
#poll this from front end, save refresh interval in a session cookie
def getWeatherData():
	return "TODO7"
	

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