import signal
import sys
import time
import csv
from components.bmp280 import BMP280
from smbus2 import SMBus

FIL = open("data" + str((time.time()*10)//1)+".csv", "w")

def main_loop():
    global bmp280
    smbus = SMBus(0)
    bmp280 = BMP280(i2c_bus=smbus)
    counter = 0
    writer = csv.writer(FIL)

    while True:
        beginning = time.time()

        bmp_press = bmp280.get_pressure()
        print("[*] Read BMP data no. %d: %f" % (counter, bmp_press))
        writer.writerow([int((time.time()-beginning)*10), bmp_press])

        time.sleep(1-(time.time()-beginning))
        counter += 1

def exit_handler(signal, frame):
  print("[*] Shutting down gracefully")
  FIL.close()
  sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    main_loop()
