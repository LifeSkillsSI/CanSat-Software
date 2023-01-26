#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 Jan Przebor <przebot@gmail.com> [Modifications]
Copyright (C) 2021 Luiz Eduardo Amaral <luizamaral306@gmail.com> [Original]
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import spidev

RESOLUTION = 1 << 10 # 10 bits resolution

class MCP3008(spidev.SpiDev):
    '''
    Object that listens the MCP3008 in the SPI port of the RPi.
    Connects the object to the specified SPI device.
    The initialization arguments are MCP3008(bus=0, device=0) where:
    MCP3008(X, Y) will open /dev/spidev-X.Y, same as spidev.SpiDev.open(X, Y).
    '''
    def __init__(self, bus=0, device=0, max_speed_hz=976000, vref=5.0):
        self.bus = bus
        self.device = device
        self.open(self.bus, self.device)
        self.max_speed_hz = max_speed_hz
        self.vref = vref

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __repr__(self):
        return 'MCP3008 object at bus {0}, device {1}'.format(self.bus, self.device)

    def _read(self, channels):
        reading = []
        for ch in channels:
            request = [0x1, (1 << 7)|(ch << 4), 0x0]
            _, byte1, byte2 = self.xfer2(request)
            value = (byte1 & 0x03 << 8) | byte2
            reading.append(value)
        return reading

    def read(self, channel):
        if not 0 <= channel <= 7:
            raise IndexError('Outside the channels scope, please use: 0, 1 ..., 7')
        
        return self._read([channel])[0]

    def read_all(self):
        return self.read(range(8))

    def read_voltage(self, channel):
        if not 0 <= channel <= 7:
            raise IndexError('Outside the channels scope, please use: 0, 1 ..., 7')
        
        return self._read([channel])[0] / 1024.0 * self.vref

    def read_all_voltage(self):
        values = self.read(range(8))
        return [v / 1024.0 * self.vref for v in values]