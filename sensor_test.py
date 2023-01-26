import signal
import sys
import time
from components.bmp280 import BMP280
from components.lm35 import LM35
from components.mcp3008 import MCP3008

def main_loop():
    global mcp3008, lm35, bmp280
    mcp3008 = MCP3008(bus=0, device=0)
    lm35 = LM35(mcp3008, 0)
    bmp280 = BMP280()

    while True:
        beginning = time.time()
        print("[*] LM35 temperature: %f" % (lm35.get_temperature()))
        print("[*] BMP280:")
        print("\t- %f *C" % (bmp280.get_temperature()))
        print("\t- %f hPa" % (bmp280.get_pressure()))
        print("\t- %f m" % (bmp280.get_altitude()))
        time.sleep(1-(time.time()-beginning))

def exit_handler(signal, frame):
  print("[*] Shutting down gracefully")
  mcp3008.close()
  sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    main_loop()