from components.mcp3008 import MCP3008

class LM35():
    def __init__(self, adc: MCP3008, channel: int):
        self.adc = adc
        self.channel = channel

    def setup(self):
        # Setup not required here
        pass
    
    def get_temperature(self):
        return self.adc.read_voltage(self.channel) * 100