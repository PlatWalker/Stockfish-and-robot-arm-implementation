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
  const int FirstZero = 65;
  const int SecondZero = 178;
  const int RotateZero = 90;

  Serial.begin(9600);

  First.attach(FirstPIN);
  First.write(FirstZero);

  Second.attach(SecondPIN);
  Second.write(SecondZero);

  Rotate.attach(RotatePIN);
  Rotate.write(RotateZero);

}

void loop() {
  recvWithEndMarker();
  showNewData();
}

void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;

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
    
    Test();
    
    int rotateAngleAdd = getValue(String(receivedChars), 's', 0).toInt();
    int firstJointAngleAdd = getValue(String(receivedChars), 's', 1).toInt();
    int secondJointAngleAdd = getValue(String(receivedChars), 's', 2).toInt();

    Rotate.write(rotateAngleAdd);
    First.write(firstJointAngleAdd);
    Second.write(secondJointAngleAdd);

    newData = false;
  }
}

void Test() {
    Serial.print("This just in ... ");
    String test1 = getValue(String(receivedChars), 's', 0);
    String test2 = getValue(String(receivedChars), 's', 1);
    String test3 = getValue(String(receivedChars), 's', 2);
    Serial.println(" 1 = " + test1 + " 2 = " + test2 + " 3 = " + test3 );
    Serial.println(" can write again... ");
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }

  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
