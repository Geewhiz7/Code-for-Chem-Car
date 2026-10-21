#include <Wire.h>
#include <Adafruit_INA219.h>


Adafruit_INA219 ina219(0x40);
const unsigned long SAMPLE_INTERVAL_MS = 100; // 10 samples/second
unsigned long lastSample = 0;


void setup() {
  Serial.begin(115200);
  Wire.begin();
  if (!ina219.begin()) {
    while (true) {
      Serial.println("# ERROR: INA219 not found. Check wiring/address.");
      delay(1000);  - check that ina219 board works
    }
  }
  ina219.setCalibration_32V_2A(); 
  Serial.println("time_ms,load_voltage_V,current_mA");
}


void loop() {
  unsigned long now = millis();
  if ((unsigned long)(now - lastSample) < SAMPLE_INTERVAL_MS) return;
  lastSample = now; -samples over a certain interval


  float voltage = ina219.getBusVoltage_V(); -get voltage (volts)
  float current = ina219.getCurrent_mA(); -get current (millamps) 


  Serial.print(now);
  Serial.print(',');
  Serial.print(voltage, 3); -return voltage
  Serial.print(',');
  Serial.println(current, 3); -return current
}


