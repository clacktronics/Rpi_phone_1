import RPi.GPIO as GPIO 
from omxplayer import OMXPlayer as omx 
from time import sleep
import sys,os

accepted_files = ['wav','mp3','m4a','mp4','aif'] 

omxargs = sys.argv

files = [elem for elem in os.listdir('files') if elem[0] != '.']
files = [elem for elem in files if elem[-3:] in accepted_files]
print files
number_files = len(files)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

HOOK = 4
GPIO.setup(HOOK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(HOOK, GPIO.FALLING)


while True:
    try:
        for file in files:
            otpt = 'files/%s' % file
            video = omx('korn.mp4', args = omxargs, pause=False)        
            plays = 0
            played = False

            while plays < 1:
                if GPIO.event_detected(HOOK) and not GPIO.input(HOOK):
                    video.play()
                    print "Playing %s" % file
                    played = True

                if played and GPIO.input(HOOK):
                    plays +=1
                    already_played = True
                    print "receiver down"

            print "Next track"
            video.stop()
            del video
            sleep(1)

    except KeyboardInterrupt:
        video.stop()
        print "Bye"
        break    

    except Exception as e:
        print e
