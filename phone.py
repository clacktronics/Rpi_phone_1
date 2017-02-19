import RPi.GPIO as GPIO
from omxplayer import OMXPlayer as omx
import sys
from time import sleep


vid = sys.argv[0]
omxargs = sys.argv[1:]

try:

    video = omx(vid, args = omxargs, pause=True)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    HOOK = 4
    GPIO.setup(HOOK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(HOOK, GPIO.RISING)

    already_stopped = True

    while True:
        if GPIO.event_detected(HOOK) and GPIO.input(HOOK):
            video.play()
            already_stopped = False
            print "play"

        if not already_stopped and not GPIO.input(HOOK):
            video.pause()
            video.set_position(0)
            already_stopped = True
            print "hold"

except KeyboardInterrupt:
    video.stop()
    print "Bye"    
