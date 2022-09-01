

// Humidity control system
// Written by Bevan Pulling 23/5/22


// REQUIRES the following Arduino libraries:
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor

#include <Adafruit_AHTX0.h>


Adafruit_AHTX0 aht;


// Variables
const int waitTime = 10000;
float tAverage = 0.0;
float hAverage = 0.0;
float hSetPoint = 50.0;
float hOffset = 5.0;
int mistPin = 13;



void setup() {
  Serial.begin(115200);
  
  if (! aht.begin()) {
//    Serial.println("Could not find AHT? Check wiring");
    while(1) delay(10);
  }
//  Serial.println("AHT10 or AHT20 found");

 
  //setup ultrasonic mister and ensure it is off
  pinMode(mistPin, OUTPUT);
  digitalWrite(mistPin, LOW);
}




void loop() {
  
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);// populate temp and humidity objects with fresh data
  Serial.print(temp.temperature); Serial.print(", ");Serial.println(humidity.relative_humidity);
  tAverage = temp.temperature;
  hAverage = humidity.relative_humidity;  

  //basic control system (ON/OFF control)
  if (hAverage < (hSetPoint-hOffset)) {
    digitalWrite(mistPin, HIGH);
  }
  else if (hAverage > (hSetPoint+hOffset)) {
    digitalWrite(mistPin, LOW);
  }
  delay(waitTime);// Wait a few seconds between measurements.
}
