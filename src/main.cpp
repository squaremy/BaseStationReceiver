// #include <Arduino.h>
// #include <SPI.h>
// #include <RF24.h>
//
// /*
//  * Program: Arduino receiver
//  * Author: Jordan Martin
//  * Version: 1.1
//  * Date Created: 5 March 2019
//  * Description: Receives information from the payload through a radio
//  * Last Edited By: Jordan Martin
//  * Last Edited: 8 May 2019
//  * Reason Edited: Added radio testing
//  */
// RF24 radio(7, 8); // CE = 7, CSN = 8
// const byte addresses[][6] = {"00001", "00002"};
//
// bool checksum(String line) {
//   float x;
//   float y;
//   if(line.indexOf("LX:") >= 0) { // if format is for location
//     x = atof(line.substring(line.indexOf("LX:")+3, line.indexOf("LY:")).c_str()); // get lat of location
//     y = atof(line.substring(line.indexOf("LY:")+3, line.indexOf("*")).c_str()); // get lng of location
//   } else if(line.indexOf("PA:") >= 0) { // if format if for altitude
//     x = atof(line.substring(line.indexOf("PA:")+3, line.indexOf("TS:")).c_str()); // get altitude
//     y = atoi(line.substring(line.indexOf("TS:")+3, line.indexOf("*")).c_str()); // get timestamp
//   } else {
//     int sum = 0;
//     for(char i : line) {
//       if(line.indexOf("*") > 0) break;
//       sum += (int)i;
//     }
//     sum %= 0xff;
//     char toCheck[100] = "";
//     sprintf(toCheck, "*%X", sum);
//     if(line.substring(line.indexOf("*"), line.indexOf("/r")).equalsIgnoreCase(toCheck)) return true;
//   }
//   char toCheck[100] = "";
//   double temp = x + y; // combine float values
//   int sum = 0;
//   for(char i : String(temp)){
//     sum += i; // sum ascii values
//   }
//   sum %= 0xff; // limit to 2 hexadecimal characters
//   sprintf(toCheck, "*%X", sum); // create checksum
//   if(line.substring(line.indexOf("*"), line.indexOf("/r")).equalsIgnoreCase(toCheck)) return true; // determine if checksum matches
//   return false; // false if checksum doesn't match
// }
//
// void setup() {
//   // put your setup code here, to run once:
//   Serial.begin(9600);
//   radio.begin(); // start radio comms
//   radio.openReadingPipe(0, addresses[1]); // route radio to correct address
//   radio.openWritingPipe(addresses[0]);
//   radio.setPALevel(RF24_PA_MIN);
//   radio.startListening(); // start receiver on radio
//   Serial.println("Listening...");
// }
// void loop() {
//   radio.startListening();
//   while(radio.available()){ // continue while the radio is active
//     String commandIn = "";
//     char datIn[100] = ""; // create data in buffer
//     while(Serial.available()) {
//       delay(3);
//       if(Serial.available() > 0) {
//         commandIn += (char)(Serial.read());
//       }
//     }
//     radio.read(&datIn, sizeof(datIn)); // obtain incoming data
//     Serial.println(datIn);
//     if(checksum(datIn)) Serial.println(datIn); // log incoming data to serial monitor
//     else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("ABORT")) {
//       Serial.println("ABORTED");
//     } else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("SYNC")) {
//       Serial.println("SYNCED");
//     } else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("ARM")) {
//       Serial.println("ARMED");
//     } else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("LAUNCH")) {
//       Serial.println("STARTING_COUNTDOWN");
//     } else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("WRITE_SD")) {
//       radio.stopListening();
//       char writeSD[] = "WRITE_SD";
//       radio.write(&writeSD, sizeof(writeSD));
//     } else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("TOGGLE_BUZZER")) {
//       radio.stopListening();
//       char toggleBuzzer[] = "TOGGLE_BUZZER";
//       radio.write(&toggleBuzzer, sizeof(toggleBuzzer));
//     } else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("TOGGLE_CAMERA")) {
//       radio.stopListening();
//       char toggleCamera[] = "TOGGLE_CAMERA";
//       radio.write(&toggleCamera, sizeof(toggleCamera));
//     } else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("DEPLOY_CHUTE")) {
//       radio.stopListening();
//       char deployChute[] = "DEPLOY_CHUTE";
//       radio.write(&deployChute, sizeof(deployChute));
//     } else if(commandIn.substring(0, commandIn.indexOf("/r")).equalsIgnoreCase("REQUESTING_GRAPH_DATA")) {
//       radio.stopListening();
//       char requestGraphData[] = "REQUESTING_GRAPH_DATA";
//       radio.write(&requestGraphData, sizeof(requestGraphData));
//     }
//
//     radio.startListening();
//   }
// }
