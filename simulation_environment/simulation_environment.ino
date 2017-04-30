#include <ESP8266WiFi.h>
#include "RestClient.h"   // Library Downloaded from: https://github.com/DaKaZ/esp8266-restclient
#include "cardIDS.h"

#define WiFi_ID       ""
#define WiFi_Password ""

#define SWITCH_PIN    5
#define Green_Led     15
#define Red_Led       0

RestClient client = RestClient("unlv-spots.herokuapp.com");
String lotID, cardID;
int lotNUM;
long randIndex;
//bool vacant;

// List of all the beautiful functions used for this immaculate device
void Wifi_connect();  // Setup code to connect the ESP8266 to the wifi_chip
void flash_LED(int, int);
void updateVacancy(String);
bool swipeCard();
bool getVacancy();

void setup() {

  pinMode(SWITCH_PIN, INPUT);
  pinMode(Green_Led, OUTPUT);
  pinMode(Red_Led, OUTPUT);
  Serial.begin(9600);
  //vacant = false;
  Wifi_connect();

}

void loop() {

  digitalWrite(Green_Led, LOW);
  digitalWrite(Red_Led, LOW);
  
  if(digitalRead(SWITCH_PIN)) {

    lotNUM = 13;
    while(lotNUM == 13)
      lotNUM = random(1, 151);
    if(lotNUM < 10)
      lotID = "000" + String(lotNUM);
    else if(lotNUM > 99)
      lotID = "0" + String(lotNUM);
    else
      lotID = "00" + String(lotNUM);
    lotID = "0100";
      
    if(getVacancy()) {
      updateVacancy("/false");
      if(swipeCard()) {
        Serial.print("User was authorized and parked at spot: ");
        Serial.println(lotID);
        flash_LED(Red_Led, 2000);
      }
      else {
        Serial.print("User wasn't authorized and left from spot: ");
        Serial.println(lotID);
        updateVacancy("/true");
        flash_LED(Green_Led, 2000);
      }
    }
    else {
      Serial.print("User left from spot: ");
      Serial.println(lotID);
      updateVacancy("/true");
      flash_LED(Green_Led, 2000);
    }
    Serial.println();
    
  }

}

// Connects the ESP8266 to a WiFi Network
// If unable to connect, check the weefee_ID and weefee_Password fields
void Wifi_connect()
{
  Serial.print(F("Card UID: "));
  // Code to setup esp8266 to connect to zee weefee 
  //WiFi.begin(WiFi_ID, WiFi_Password);
  Serial.print("Connecting to ze network");
  WiFi.begin(WiFi_ID, WiFi_Password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
}

// Flashes a designated LED for a specified duration, the LED will always remain
// off at the end of the flashing sequence
// int LED - the pin number of the LED
// int duration - the amount of time to flash in milliseconds
void flash_LED(int LED, int duration)
{
  int initTime = millis();
  bool flash = true;
  while((millis() - initTime) <= duration )
  {
    // Flash with a period of 500ms
    flash = !flash;
    digitalWrite(LED, flash);
    delay(250);
  }
  digitalWrite(LED, LOW);
}

void updateVacancy(String vacancy) {

  String response = "";
  String dbPath = "/spotsHW/update/1234/LB/";
  dbPath += lotID;
  dbPath += vacancy;

  const char* c = dbPath.c_str();
  Serial.println(dbPath);
  int statusCode = client.post(c, "POSTDATA", &response);

}

bool swipeCard() {

  String response = "";
  String dbPath = "/spotsHW/swipe/1234/LB/";
  dbPath += lotID;
  randIndex = random(1, 100);
  cardID = randomCard(int(randIndex));

  const char* c = dbPath.c_str();
  Serial.print("Checking for authorization of cardID: ");
  Serial.println(cardID);
  Serial.println(dbPath);
  int statusCode = client.post(c, "POSTDATA", &response);
  
  if(response == "{\"authorized\":true}")
    return true;
  else
    return false;
 
}

bool getVacancy() {

  String response = "";
  String dbPath = "/spotsHW/getVacancy/1234/LB/";
  dbPath += lotID;
  
  const char* c = dbPath.c_str();
  Serial.println(dbPath);
  int statusCode = client.get(c, &response);
  Serial.println(statusCode);
  Serial.println(response);
  
  if(response == "{\"Vacancy\":true}")
    return true;
  else
    return false;

}

