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
int lotNUM, dbSuccess, dbFailure;
long randIndex;
//bool vacant;

// List of all the beautiful functions used for this immaculate device
void Wifi_connect();  // Setup code to connect the ESP8266 to the wifi_chip
void flash_LED(int, int);
void updateVacancy(String);
bool swipeCard();
bool getVacancy();
void printStats();

void setup() {

  pinMode(SWITCH_PIN, INPUT);
  pinMode(Green_Led, OUTPUT);
  pinMode(Red_Led, OUTPUT);
  Serial.begin(9600);
  delay(2000);
  //vacant = false;
  Wifi_connect();
  Serial.println("Push button for simulation of a parking spot!");

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
    //lotID = "0100";
      
    if(getVacancy()) {
      updateVacancy("/false");
      if(swipeCard()) {
        Serial.print("User was authorized and parked at spot: ");
        Serial.println(lotID);
        flash_LED(Red_Led, 2000);
      }
      else {
        Serial.print("User was not authorized and left from spot: ");
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
    Serial.println("Push button for simulation of a parking spot!");
    
  }

}

// Connects the ESP8266 to a WiFi Network
// If unable to connect, check the weefee_ID and weefee_Password fields
void Wifi_connect()
{
  //Serial.println(F("Card UID: "));
  // Code to setup esp8266 to connect to zee weefee 
  //WiFi.begin(WiFi_ID, WiFi_Password);
  Serial.print("Connecting to the network");
  WiFi.begin(WiFi_ID, WiFi_Password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected: ");
  Serial.println(WiFi.localIP());
  Serial.println();
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
  Serial.print("Updating vacancy of spot: ");
  Serial.println(lotID);
  Serial.print("POST request: ");
  Serial.println(dbPath);
  int statusCode = client.post(c, "POSTDATA", &response);
  if(statusCode == 200)
    dbSuccess++;
  else
    dbFailure++;
  //Serial.println(statusCode);
  return;
  
}

bool swipeCard() {

  String response = "";
  String dbPath = "/spotsHW/swipe/1234/LB/";
  dbPath += lotID;
  randIndex = random(1, 100);
  cardID = randomCard(int(randIndex));
  dbPath += "/";
  dbPath += cardID;

  const char* c = dbPath.c_str();
  Serial.print("Checking for authorization of user with cardID: ");
  Serial.println(cardID);
  Serial.print("POST request: ");
  Serial.println(dbPath);
  int statusCode = client.post(c, "POSTDATA", &response);
  if(statusCode == 200)
    dbSuccess++;
  else
    dbFailure++;
  //Serial.println(statusCode);
  
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
  Serial.print("Grabbing vacancy of spot: ");
  Serial.println(lotID);
  Serial.print("GET request: ");
  Serial.println(dbPath);
  int statusCode = client.get(c, &response);
  if(statusCode == 200)
    dbSuccess++;
  else
    dbFailure++;
  //Serial.println(statusCode);
  
  if(response == "{\"Vacancy\":true}") {
    Serial.println("Spot is available. User can swipe card.");
    return true;
  }
  else {
    Serial.println("Spot was taken. User is leaving.");
    return false;
  }

}

void printStats() {

  Serial.print("Successful DB Requests: ");
  Serial.println(dbSuccess);
  Serial.print("Failed DB Requests: ");
  Serial.println(dbFailure);
  return;

}

