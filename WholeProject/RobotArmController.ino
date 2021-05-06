#include "Servo.h"

#define FirstPIN 9
#define SecondPIN 5
#define RotatePIN 6

Servo First;
Servo Second;
Servo Rotate;

int rot = 0;
int fir = 0;
int sec = 0;

String inputString = "";
bool stringComplete = false;
int angleAdd = -1;

const byte numChars = 32;
char receivedChars[numChars] = ""; // an array to store the received data
boolean newData = false;

void setup() {
  Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
  First.attach(FirstPIN);
  First.write(90);

  Second.attach(SecondPIN);
  Second.write(90);
  double proba = 101.11;
  Rotate.attach(RotatePIN);
  Rotate.write(proba);

}

void loop() {
  /*
  if (stringComplete) {
    Serial.println(inputString + " : ");
    Serial.println(angleAdd);
    inputString = "";
    angleAdd = -1;
    stringComplete = false;
  }
  */

  something();
}


void something() {
  
  recvWithEndMarker();
  showNewData();
  
  /*
  while (Serial.available()) {

    char inChar = (char)Serial.read();

    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }

  angleAdd = inputString.toInt();
  Rotate.write(angleAdd);
  */

  //angleAdd = String(receivedChars).toInt();
  //Rotate.write(angleAdd);
}

void recvWithEndMarker() {
 static byte ndx = 0;
 char endMarker = '\n';
 char rc;

 // if (Serial.available() > 0) {
 while (Serial.available() > 0 && newData == false) {
  
  rc = Serial.read();

  if (rc != endMarker) {
    receivedChars[ndx] = rc;
    ndx++;
    if (ndx >= numChars) {
      ndx = numChars - 1;
    }
  }
  else {
    receivedChars[ndx] = '\0'; // terminate the string
    ndx = 0;
    newData = true;
  }
 }
}

void showNewData() {
 if (newData == true) {
 //Serial.print("This just in ... ");
 Serial.println(" sum up: " + String(receivedChars) );
 Serial.println(" can write again... ");
 angleAdd = String(receivedChars).toInt();
 Rotate.write(angleAdd);
 newData = false;
 }
}
