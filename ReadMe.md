<h1>
WIT Senior Project - Raspberry TV
</h1>

This project's main goal was to provide some limited smart TV functionality via a raspberry pi.

The orginally stated goals were:
An app which would push commands to a public server
A local server which would display the smart TV splash screen
Normal TV controls:
- Volume up/down
- fast forward/rewind
- Play/Pause
- Stop

In addition to playing local media, one can download YouTube videos.
The YouTube downloading comes from a utility called youtube-dl (the windows .exe is given, linux version can be downloaded via apt-get)
Originally this was designed to use VLC as its media player, however a lack of hardware acceleration meant VLC was largely useless in this project.
Instead python bindings for the default Raspberry Pi player, omxplayer, had to be written (and consequently so did the back end).  There will soon be a separate project for tracking changes to pyomxplayer

In implementation the servers had to be combined due to having the same address binding. As such on the two url's used on the from the Raspberr Pi itself have a rule which will 404 any non localhost access.

The rest of the URL's are deliberately public so as to be used by the application.

For future development:
- Rework the application and back end to only accept POST requests to make it more secure
- Improve the shutdown procedure as currently the threaded nature must be stopped in a non intuitive way
- Deploy with a true web server like Twisted or apache. Although not difficult, the built in server is more than enough to handle the small number of requests and connections.
- Have a keyboard default possibility, this was originally implemented but with the move from VLC to omxplayer the front end JS would have had to been rewritten as well.

Development will continue as this application is used in my home. Late night coding practices will be cleaned up for clarity.

There is a good deal of depreciated JS on the front end because of the abandoned keyboard default and the raspberry pi/chromiums inability to handle by JS background and visualizer (for mp3s) which had horrible color banding and issues rendering the elements (I believe chromium is unintentionally doing something nonstandard, I will explore other chromium packages).
In addition, the rasptv.py file (which was the local web server) has been built into the publicServer.py and it's code still exists for reference.