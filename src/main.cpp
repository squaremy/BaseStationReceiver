#include <Arduino.h>
#include <RF24.h>

/*
 * Program: Arduino receiver
 * Author: Jordan Martin
 * Version: 1.0
 * Date Created: 5 March 2019
 * Description: Receives information from the payload through a radio
 * Last Edited By: Jordan Martin
 * Last Edited: 11 March 2019
 * Reason Edited: Data testing for python graphs
 */
RF24 radio(7, 8);
const byte address[6] = "00001";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  radio.begin(); // start radio comms
  radio.openReadingPipe(0, address); // route radio to correct address
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening(); // start receiver on radio
  Serial.println("Listening...");
}

float x = 10.2, y = 18.7;
void loop() {
  while(radio.available()){ // continue while the radio is active
    char datIn[100] = ""; // create data in buffer
    radio.read(&datIn, sizeof(datIn)); // obtain incoming data
    Serial.println(datIn); // log incoming data to serial monitor
  }
  // x += 0.3;
  // y = 2*y;
  // String blah = String(x, sizeof(x)/sizeof(float)) + "," + String(y, sizeof(y)/sizeof(float));
  // char text[100] = "";
  // for(int i = 0; i < blah.length(); i++) {
  //   text[i] = blah.charAt(i);
  // }
  // Serial.println(text);
}
