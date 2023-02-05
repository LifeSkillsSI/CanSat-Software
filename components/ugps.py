import gps
import os
import sys
from threading import Thread

class UGPS():
    def __init__(self, tty="/dev/ttyS3"):
        try:
            self.session = gps.gps("localhost", "2947")
        except ConnectionRefusedError:
            if os.geteuid() != 0:
                sys.exit("In order to initialize GPS, you have to run this script as root")
            os.system("sudo gpsd " + tty + " -F /var/run/gpsd.lock")
            self.session = gps.gps("localhost", "2947")
        self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        update_thread = Thread(target=self._update, args=[self])
        update_thread.start()
        self.latitude = 0.0
        self.longitude = 0.0
        self.time = 0

    def _update(num, self):
        while True:
            try:
                report = self.session.next()
                if report['class'] == 'TPV':
                    if hasattr(report, 'time'):
                        self.time = report.time
                    if hasattr(report, 'lon'):
                        self.longitude = report.lon
                    if hasattr(report, 'lat'):
                        self.latitude = report.lat
            except KeyError:
                pass
            except StopIteration:
                session = None
                print("GPSD has terminated")
