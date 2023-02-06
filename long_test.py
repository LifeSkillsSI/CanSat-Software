from SX127x.LoRa import *
from SX127x.board_config import BOARD
from components.sx1278 import LoRaTransmitter
from components.bmp280 import BMP280
from components.lm35 import LM35
from components.mcp3008 import MCP3008
from smbus2 import SMBus
import time
import signal
import struct

BOARD.setup()
lora = LoRaTransmitter(verbose=False)
smbus = SMBus(0)
bmp280 = BMP280(i2c_bus=smbus)
mcp3008 = MCP3008(bus=0, device=1)
lm35 = LM35(mcp3008, 1)

def main_loop():
    counter = 0
    while True:
        pressure = bmp280.get_pressure()
        lm_temp = lm35.get_temperature()
        bmp_temp = bmp280.get_temperature()
        lora.send(list(struct.pack("i", counter)) +
                  list(struct.pack("f", pressure)) +
                  list(struct.pack("f", lm_temp)) +
                  list(struct.pack("f", bmp_temp)))
        print(pressure, lm_temp, bmp_temp)
        time.sleep(1)
        counter+=1

def exit_handler(signal, frame):
    print("[*] Shutting down gracefully")
    lora.set_mode(MODE.SLEEP)
    print(lora)
    BOARD.teardown()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    main_loop()
