import RPi.GPIO as GPIO
import time
import syslog
import json
import socket

from socketConnection import SocketConnection
import config

class PinHandler:

    ledPin = 35
    sensor = 7

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # Broadcom pin-numbering scheme
        GPIO.setup(self.ledPin, GPIO.OUT)  # LED pin set as output
        GPIO.setup(self.sensor, GPIO.IN, GPIO.PUD_UP)

        GPIO.output(self.ledPin, GPIO.LOW)
        return



    def run(self):
        counter = 0  # min 0 max 10
        prev_state = 0
        while(True):
            current_state = GPIO.input(self.sensor)
            if(current_state == 1):
                GPIO.output(self.ledPin, GPIO.HIGH)
                if(current_state != prev_state):
                    syslog.syslog("motion detected")
                    j = json.dumps(['command', 'snapshot', 'motion'])
                    sock = socket.socket()
                    try:
                        sock.connect((config.SOCKET_HOST, config.SOCKET_PORT))
                        sock.send(j)
                        sock.recv(1024)
                    except:
                        syslog.syslog('Could not connect to CCTV-server')



            else:
                GPIO.output(self.ledPin, GPIO.LOW)

            prev_state = current_state
            time.sleep(0.2)

        return

    def cleanup(self):
        GPIO.cleanup()
        return
