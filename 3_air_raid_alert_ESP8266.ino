#ifdef ESP32
  #include <WiFi.h>
#else
  #include <ESP8266WiFi.h>
#endif
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>   // Universal Telegram Bot Library written by Brian Lough: https://github.com/witnessmenow/Universal-Arduino-Telegram-Bot
#include <ArduinoJson.h>

// Replace with your network credentials
const char* ssid = "home";
const char* password = "home1111"; 

//const char* ssid = "***";
//const char* password = "****7"; 



// Initialize Telegram BOT
#define BOTtoken "511****:*****"  // (ds)

//id of users with access to bot
#define CHAT_ID "56*****"
#define CHAT_ID1 "15****"
#define CHAT_ID2 "552*****"

#ifdef ESP8266
  X509List cert(TELEGRAM_CERTIFICATE_ROOT);
#endif

WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

// Checks for new messages every 1 second.
int botRequestDelay = 500;
unsigned long lastTimeBotRan;

const int ledPin = 13;
bool ledState = LOW;

int start_ac = 0;

// Handle what happens when you receive new messages
void handleNewMessages(int numNewMessages) {
  Serial.println("handleNewMessages");
  Serial.println(String(numNewMessages));

  for (int i=0; i<numNewMessages; i++) {
    // Chat id of the requester
    String chat_id = String(bot.messages[i].chat_id);
    if (chat_id != CHAT_ID && chat_id != CHAT_ID1 && chat_id != CHAT_ID2){
      bot.sendMessage(chat_id, "Unauthorized user", "");
      Serial.println("UN USR ID:");
      Serial.println(chat_id);
      continue;
    }
    
    // Print the received message
    String text = bot.messages[i].text;
    text.toLowerCase();
    Serial.println(text);

    String from_name = bot.messages[i].from_name;

    if (text == "/start") {
      String welcome = "Welcome, " + from_name + ".\n";
      welcome += "Use the following commands to control your outputs.\n\n";
      welcome += "/on to turn siren ON \n";
      welcome += "/off to turn siren OFF \n";
      welcome += "/state to request current siren state \n";
      bot.sendMessage(chat_id, welcome, "");
    }

    else if (text == "/on" || text == "старт" || text == "Старт" || text == "on" || text == "+" || text == "start") {
      ledState = HIGH;
      digitalWrite(ledPin, ledState);
      bot.sendMessage(chat_id, "🔴УВАГА! СИРЕНУ ВВІМКНЕНО!🔴", ""); 
      bot.sendMessage("100000", "🔴Turned ON by " + from_name + "!🔴", ""); // 100000 - telegram id of admin
          }
    
    else if (text == "/off" || text == "стоп" || text == "Стоп" || text == "of" || text == "off" || text == "-" || text == "stop") {
      ledState = LOW;
      digitalWrite(ledPin, ledState);
      bot.sendMessage(chat_id, "🟢Сирену вимкнено.🟢", "");
      bot.sendMessage("100000", "🟢Turned OFF by " + from_name + "!🟢", "");
    }
    
    else if (text == "/status" || text == "/state" || text == "чек" || text == "стан" || text == "check" || text == "status" ) {
      if (digitalRead(ledPin)){
        bot.sendMessage(chat_id, "🔴Поточний стан: лунає сирена!🔴", "");
      }
      else{
        bot.sendMessage(chat_id, "🟢Поточний стан: вимкнено.🟢", "");
      }
    }

    else{
      bot.sendMessage(chat_id, "Невідома команда, спробуйте знову.", "");
    }
  }
}

void setup() {
  Serial.begin(115200);

  #ifdef ESP8266
    configTime(0, 0, "pool.ntp.org");      // get UTC time via NTP
    client.setTrustAnchors(&cert); // Add root certificate for api.telegram.org
  #endif

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, ledState);

  //led
  pinMode(BUILTIN_LED, OUTPUT);
  digitalWrite(BUILTIN_LED, HIGH); 
  // Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  #ifdef ESP32
    client.setCACert(TELEGRAM_CERTIFICATE_ROOT); // Add root certificate for api.telegram.org
  #endif
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  // Print ESP32 Local IP Address
  Serial.println(WiFi.localIP());
}

void loop() {
  if (start_ac == 0){
    bot.sendMessage("100000", "🔹 Увага! Було відсутнє живлення. Роботу системи відновлено! 🔹");
    start_ac = 1;
  } 
  if (millis() > lastTimeBotRan + botRequestDelay)  {
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);

    while(numNewMessages) {
      Serial.println("got response");
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
    lastTimeBotRan = millis();
  }
}
