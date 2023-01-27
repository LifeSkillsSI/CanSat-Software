import signal
import sys
import time
from components.bmp280 import BMP280
from components.icm20948 import ICM20948
from components.lm35 import LM35
from components.mcp3008 import MCP3008
from smbus2 import SMBus
import psutil

def main_loop():
    global mcp3008, lm35, bmp280
    mcp3008 = MCP3008(bus=0, device=0)
    lm35 = LM35(mcp3008, 0)
    smbus = SMBus(0)
    bmp280 = BMP280(i2c_bus=smbus)
    icm20948 = ICM20948(i2c_bus=smbus)

    while True:
        beginning = time.time()

        lm_temp = lm35.get_temperature()
        bmp_temp = bmp280.get_temperature()
        bmp_pressure = bmp280.get_pressure()
        bmp_altitude = bmp280.get_altitude()
        x, y, z = icm20948.read_magnetometer_data()
        ax, ay, az, gx, gy, gz = icm20948.read_accelerometer_gyro_data()
        try:
          cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        except:
          cpu_temp = -1.0
        icm_temp = icm20948.read_temperature()

        print("""[*] LM35 temperature: %.2f *C
[*] BMP280:
\t- %.2f *C
\t- %.2f hPa
\t- %.2f m
[*] ICM20948:
\tAccel: %.2f %.2f %.2f
\tGyro:  %.2f %.2f %.2f
\tMag:   %.2f %.2f %.2f
\tDie Temp:  %.2f *C
[*] CPU temperature: %.2f *C
[*] Reading took %.4f seconds""" % (
            lm_temp, bmp_temp, bmp_pressure, bmp_altitude, ax, ay, az, gx, gy, gz, x, y, z, icm_temp, cpu_temp, time.time()-beginning
        ))
        time.sleep(1-(time.time()-beginning))

def exit_handler(signal, frame):
  print("[*] Shutting down gracefully")
  mcp3008.close()
  sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    main_loop()