#include <WiFiNINA.h>
const int FWD_PIN = 7;
const int RHT_PIN = 3;
const int LHT_PIN = 5;
//const int TestOut = 6;
const int DELAY_TIME = 150;

//const int trigPin = 4;  // Trigger pin
//const int echoPin = 7;  // Echo pin


int incomingByte = 'S';  // a variable to read incoming serial data into
// Won't read as a char, will be the integer equivalent
int fwd_val = 0;
int rht_val = 0;
int lht_val = 0;
int bac_val=0;


bool turn_action = false;
char ssid[] = "WheelchairUno";     // your network SSID (name)
char pass[] = "wheelchair";  // your network password
void setup() {
  // initialize serial communication:9600
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.println("Connecting to WiFi...");
  }
  //Serial.println("Connected to WiFi");
  //}
  // initialize the pins as an output:
  //pinMode(trigPin,OUTPUT);
  //pinMode(echoPin,INPUT);
  
  pinMode(FWD_PIN, OUTPUT);
  pinMode(RHT_PIN, OUTPUT);
  pinMode(LHT_PIN, OUTPUT);
 // pinMode(TestOut, OUTPUT);

  
}

/*
Could add in a log for seeing how long it takes, but the loop is so minimal that it is negligible

Need to keep in mind though that the step size needs to be greater than the delay time
*/

/*
Commands:
'F' = Forward, 'B' = Reverse, 'L' = Left, 'R' = Right, 'S' = Stop
*/
void loop() {
  

    // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    //Serial.println("incomingByte");
    //incomingByte = Serial.readStringUntil('\n')

    // Check the incoming action and set the pin values
    if (incomingByte == 'F') {
      fwd_val = HIGH;
      rht_val = LOW;
      lht_val = LOW;
      Serial.println("F");
      
      turn_action = true;
    } else if (incomingByte == 'L') {
      
      fwd_val = LOW;
      rht_val = LOW;
      lht_val = HIGH;
      Serial.println("L");
      turn_action = true;
    } else if (incomingByte == 'R') {
      fwd_val = 0;
      rht_val = 1;
      lht_val = 0;
      Serial.println("R");
      turn_action = true;
    } else if (incomingByte == 'S') {
      fwd_val = 0;
      rht_val = 0;
      lht_val = 0;
      
      turn_action = false;
    }
    //Serial.println(incomingByte);
    

    // Set the pins
    digitalWrite(FWD_PIN, !fwd_val);
    digitalWrite(RHT_PIN, !rht_val);
    digitalWrite(LHT_PIN, !lht_val);
    //digitalWrite(BACK_PIN, LOW);
    //delay(1000);
    

    // Check if turn, if so sleep then set pins
    //if (turn_action) {
    // delay(DELAY_TIME);
    //  rht_val = 0;
    //  lht_val = 0;
    //}
  }
  else
  {
    digitalWrite(FWD_PIN, !fwd_val);
    digitalWrite(RHT_PIN, !rht_val);
    digitalWrite(LHT_PIN, !lht_val);
  }
//}
  //else{
    //Serial.println("Else");
    //Serial.println("Collision warning");
    //digitalWrite(FWD_PIN, 0);
    //digitalWrite(RHT_PIN, 0);
    //digitalWrite(LHT_PIN, 0);
    //Serial.println(digitalRead(FWD_PIN));
  //}  
  
}

/*
// Pin setup for the 4-pin fan
const int pwmPinL = 3; // Pin 3 is for PWM control of the left fan
const int pwmPinF = 5; // Pin 5 is for PWM control of the front fan
const int pwmPinR = 6; // Pin 6 is for PWM control of the right fan

void setup() {
  // Set the PWM pins as output pins
  pinMode(pwmPinL, OUTPUT);
  pinMode(pwmPinF, OUTPUT);
  pinMode(pwmPinR, OUTPUT);
  
  // Initialize Serial Communication
  Serial.begin(9600);
  Serial.println("Fan Control Initialized.");
  Serial.println("Enter 1 for Left Fan (L), 2 for Front Fan (F), 3 for Right Fan (R), s to stop.");
  
  // Ensure all fans are off initially
  digitalWrite(pwmPinL, LOW);
  digitalWrite(pwmPinF, LOW);
  digitalWrite(pwmPinR, LOW);
}

void loop() {
  // Check if there's any input from Serial Monitor
  if (Serial.available() > 0) {
    char input = Serial.read();  // Read the input from Serial Monitor
    
    // Check which fan to turn on based on the input
    if (input == 'F') {  // If user inputs '1', turn on the left fan
      Serial.println("Turning on Left Fan (L).");
      analogWrite(pwmPinL, 255); // Full speed for left fan
      analogWrite(pwmPinF, 0);   // Turn off the front fan
      analogWrite(pwmPinR, 0);   // Turn off the right fan
    } 
    else if (input == '2') {  // If user inputs '2', turn on the front fan
      Serial.println("Turning on Front Fan (F).");
      analogWrite(pwmPinL, 0);  // Turn off the left fan
      analogWrite(pwmPinF, 255); // Full speed for front fan
      analogWrite(pwmPinR, 0);  // Turn off the right fan
    } 
    else if (input == '3') {  // If user inputs '3', turn on the right fan
      Serial.println("Turning on Right Fan (R).");
      analogWrite(pwmPinL, 0);  // Turn off the left fan
      analogWrite(pwmPinF, 0);  // Turn off the front fan
      analogWrite(pwmPinR, 255); // Full speed for right fan
    }

    else if (input == 's') {  // If user inputs '3', turn on the right fan
      Serial.println("Off.");
      analogWrite(pwmPinL, 0);  // Turn off the left fan
      analogWrite(pwmPinF, 0);  // Turn off the front fan
      analogWrite(pwmPinR, 0); // Turn off the right fan
    } 
   
  }
}
*/
