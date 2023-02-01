import signal
import sys
import time
import csv
from components.bmp280 import BMP280
from components.icm20948 import ICM20948
from components.lm35 import LM35
from components.mcp3008 import MCP3008
from smbus2 import SMBus
import psutil

TIME = 15*60; # 15 minutes
table = []

def main_loop():
    global mcp3008, lm35, bmp280
    mcp3008 = MCP3008(bus=0, device=1)
    lm35 = LM35(mcp3008, 1)
    smbus = SMBus(0)
    bmp280 = BMP280(i2c_bus=smbus)
    icm20948 = ICM20948(i2c_bus=smbus)
    counter = 0

    while counter < TIME:
        print("[*] Reading sensor data no. %d" % counter)
        beginning = time.time()

        lm_temp = lm35.get_temperature()
        bmp_temp = bmp280.get_temperature()
        try:
          cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        except:
          cpu_temp = -1.0
        icm_temp = icm20948.read_temperature()

        table.append([int((time.time()-beginning)*10), lm_temp, bmp_temp, cpu_temp, icm_temp])

        time.sleep(1-(time.time()-beginning))
        counter += 1

    with open("data" + str((time.time()*10)//1)+".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(table)

def exit_handler(signal, frame):
  print("[*] Shutting down gracefully")
  mcp3008.close()
  sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    main_loop()