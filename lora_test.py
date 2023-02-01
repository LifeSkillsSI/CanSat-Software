from SX127x.LoRa import *
from SX127x.board_config import BOARD
from components.sx1278 import LoRaTransmitter
import time
import signal

BOARD.setup()
lora = LoRaTransmitter(verbose=False)

def main_loop():
    while True:
        lora.send([0x60, 0x61, 0x62])
        time.sleep(1)

def exit_handler(signal, frame):
    print("[*] Shutting down gracefully")
    lora.set_mode(MODE.SLEEP)
    print(lora)
    BOARD.teardown()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    main_loop()
