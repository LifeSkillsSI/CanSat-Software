from components.ugps import UGPS
import time

gps = UGPS()

while True:
    print(gps.longitude, gps.latitude, gps.time)
    time.sleep(1)