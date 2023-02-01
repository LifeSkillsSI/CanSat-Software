from SX127x.LoRa import *
from SX127x.board_config import BOARD

class LoRaTransmitter(LoRa):
    def __init__(self, verbose=False):
        super(LoRaTransmitter, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])

    def on_rx_done(self):
        print("\nRxDone")
        print(self.get_irq_flags())
        print(map(hex, self.read_payload(nocheck=True)))
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())
    
    def send(self, payload):
        self.set_mode(MODE.STDBY)
        self.write_payload(payload)
        self.set_mode(MODE.TX)
