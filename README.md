# CanSat-Software
This is a repository for LifeSkills CanSat's on-board software.
To-do: main algorithm loop prototype.
## Requirements
- requirements.txt
- [our pySX127x fork](https://github.com/LifeSkillsSI/pySX127x)
- currently works on [Qengineering's image](https://github.com/Qengineering/BananaPi-M2-Zero-OV5640)

## Supported components
- BMP280 (I2C)
- MCP3008 (SPI)
- LM35 (through ADC)
- ICM20948 (I2C)
- SX1278 (SPI)
- Adafruit Ultimate GPS (UART?)
- Camera (OV5640) (BananaPi 24-pin CSI)

## To-do components
- Google Coral TPU (USB)