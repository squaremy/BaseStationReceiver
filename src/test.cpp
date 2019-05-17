#include <Arduino.h>

void setup() {
  Serial.begin(9600);

}

int incomingByte = 0;

void loop() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
  }
}
