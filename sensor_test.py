from components.lm35 import LM35
from components.mcp3008 import MCP3008

lm35 = LM35(MCP3008(bus=0, device=0), 0)
print(lm35.get_temperature())