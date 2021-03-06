import pexpect
import re

from threading import Thread
from time import sleep, time
from subprocess import Popen, PIPE

class OMXPlayer(object):

    _FILEPROP_REXP = re.compile(r".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
    _VIDEOPROP_REXP = re.compile(r".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
    _AUDIOPROP_REXP = re.compile(r"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _STATUS_REXP = re.compile(r"V :\s*([\d.]+).*")
    _DONE_REXP = re.compile(r"have a nice day.*")
    _LENGTH_REXP = re.compile(r".*Duration: (\d\d:\d\d:\d\d.\d\d).*", re.DOTALL | re.MULTILINE)

    _LAUNCH_CMD = '/usr/bin/omxplayer -s -b %s %s' #add -b for good looks, start with start_playback=True
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'
    _INC_VOL = '+'
    _DEC_VOL = '-'
    _REWIND_30 = '^[[D'
    _REWIND_600 = '[[B'
    _FF_30 = '^[[C'
    _FF_600 = '[[A'


    paused = False
    subtitles_visible = True

    def __init__(self, mediafile, args=None, start_playback=True):
        if not args:
            args = ""
        cmd = self._LAUNCH_CMD % ('"%s"' % mediafile.replace("%20", " "), args)
        self.position = None
	self.paused = False
	self.subtitles_visible = True
        self.video = dict()
        self.audio = dict()

        # This lib crashes ocasionally when attempting to read OMXPlayer's output
        # Since I am not really interested in the file properties, I am adding a try catch block in order to ensure the program doesn't crash
        try:
            self.video_length = self._convert_time_to_seconds(
                                    self._LENGTH_REXP.match(
                                        Popen(["omxplayer","-i", mediafile], stdout=PIPE, stderr=PIPE, bufsize=4096
                                    ).communicate()[1]).groups()[0]
                                )
            print str(self.video_length)

        except Exception as e:
            print ("Error with finding length %s" % e)

        self._process = pexpect.spawn(cmd)
        self._start_time = time() #1 second buffer -1


        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()

        if not start_playback:
            self.toggle_pause()
        self.toggle_subtitles()


    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])
            if index == 1: continue
            elif index in (2, 3): break
            else:
                self.position = float(self._process.match.group(1))
            sleep(0.05)
    
    def _get_current_position(self):
        return time() - self._start_time
    
    def _convert_time_to_seconds(self, timeString):
        parts = timeString.split(':')
        return float(parts[2]) + (int(parts[1])*60) + (int(parts[0])*3600)

    def toggle_pause(self):
        BW = self._process.send(self._PAUSE_CMD)
        if BW:
            self.paused = not self.paused
        print BW

    def toggle_subtitles(self):
        if self._process.send(self._TOGGLE_SUB_CMD):
            self.subtitles_visible = not self.subtitles_visible
    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)

    def increase_volume(self):
        self._process.send(self._INC_VOL)
        self._process.send(self._INC_VOL)

    def decrease_volume(self):
        self._process.send(self._DEC_VOL)
        self._process.send(self._DEC_VOL)

    def rewind_30(self):
        print str(self._get_current_position())
        if self._get_current_position() - 30 > 5: #5 second buffer
            self._start_time = self._start_time + 30
            self._process.send(self._REWIND_30)

    def fast_forward_30(self):
        if self._get_current_position() + 30 < (self.video_length - 20): #20 second buffer
            self._start_time = self._start_time - 30
            self._process.send(self._FF_30)

    def rewind_600(self):
        if self._get_current_position() - 600 > 5: #5 second buffer
            self._start_time = self._start_time + 600
            self._process.send(self._REWIND_600)

    def fast_forward_600(self):
        if self._get_current_position() + 600 < self.video_length - 10: #10 second buffer
            self._start_time = self._start_time - 600
            self._process.send(self._FF_600)



    def set_speed(self):
        raise NotImplementedError

    def set_audiochannel(self, channel_idx):
        raise NotImplementedError

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_chapter(self, chapter_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        raise NotImplementedError

    def seek(self, minutes):
        raise NotImplementedError
