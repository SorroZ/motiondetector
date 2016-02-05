#/usr/bin/python

import sys
import time
import syslog
import json

from daemon import Daemon
from pinHandler import PinHandler

# ------------------------------------------------------------------------------


class MotionDetectorDaemon (Daemon):

    def __init__(self):
        Daemon.__init__(self, '/var/run/motiondetector.pid',
                        stderr='/var/log/motiondetector.log')
        self.ph = PinHandler()

    def run(self):
        syslog.syslog('Motion detector now running.')
        self.ph.run()

        return

    def shutdown(self):
        syslog.syslog('Motion detector shutting down.')
        self.ph.cleanup()
        return


if __name__ == "__main__":
    daemon = MotionDetectorDaemon()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
