#include <CanSatKit.h>
#include <SPI.h>
#include <SD.h>

using namespace CanSatKit;

const int chipSelect = 11;
int counter = 0;
float pressure, lm_temp, bmp_temp;

Radio radio(Pins::Radio::ChipSelect,
            Pins::Radio::DIO0,
            433.0,                  // frequency in MHz
            Bandwidth_125000_Hz,    // bandwidth - check with CanSat regulations to set allowed value
            SpreadingFactor_9,      // see provided presentations to determine which setting is the best
            CodingRate_4_8);        // see provided presentations to determine which setting is the best

void setup() {
  SerialUSB.begin(115200);

  while (!SerialUSB) {
    ; // wait for SerialUSB port to connect. Needed for native USB port only
  }


  SerialUSB.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    SerialUSB.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  SerialUSB.println("card initialized.");

  // start radio module  
  radio.begin();
}

void loop() {
  // prepare empty space for received frame
  // maximum length is maximum frame length + null termination
  // 255 + 1 byte = 256 bytes
  uint8_t data[256];

  uint8_t dummy;
  radio.receive((uint8_t*)data, dummy);
  memcpy(&counter, data, 4);
  memcpy(&pressure, data+4, 4);
  memcpy(&lm_temp, data+8, 4);
  memcpy(&bmp_temp, data+12, 4);


  // get and print signal level (rssi)
  SerialUSB.print("Received (RSSI = ");
  SerialUSB.print(radio.get_rssi_last());
  SerialUSB.print("): ");

  SerialUSB.print(counter);
  SerialUSB.print(" ");
  SerialUSB.print(pressure);
  SerialUSB.print(" ");
  SerialUSB.print(lm_temp);
  SerialUSB.print(" ");
  SerialUSB.print(bmp_temp);
  SerialUSB.print("\n");

  File dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.print(counter);
    dataFile.print(",");
    dataFile.print(pressure);
    dataFile.print(",");
    dataFile.print(lm_temp);
    dataFile.print(",");
    dataFile.print(bmp_temp);
    dataFile.print("\n");
    dataFile.close();
  }
  // if the file isn't open, pop up an error:
  else {
    SerialUSB.println("error opening datalog.txt");
  }
  counter++;
}
