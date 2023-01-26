from components.bmp280i2c import BMP280I2C
from smbus2 import SMBus

class BMP280():
    # Set i2c to False in order to use BMP280 over spi
    def __init__(self, i2c = True, i2c_bus = 0, gnp = 1010.0):
        self.i2c_enabled = i2c
        self.gnp = gnp # Ground level pressure
        if i2c:
            self.smbus = SMBus(i2c_bus)
            self._i2cbmp = BMP280I2C(i2c_dev=self.smbus)
        else:
            pass
        pass

    def get_pressure(self):
        if self.i2c_enabled:
            return self._i2cbmp.get_pressure()
        else:
            pass
    
    def get_temperature(self):
        if self.i2c_enabled:
            return self._i2cbmp.get_temperature()
        else:
            pass
    
    def get_altitude(self):
        if self.i2c_enabled:
            return self._i2cbmp.get_altitude(qnh = self.gnp)
        else:
            pass
        