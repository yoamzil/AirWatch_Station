#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

// Wi-Fi credentials
const char* ssid = "1337-Guest";
const char* password = "M!Q4vJ8pZzSUr2X@";

// ThingsBoard HTTP telemetry URL (make sure the port matches your server, usually 8080)
const char* serverURL = "http://10.32.132.87:9090/api/v1/dSsrQgsYBuAQHVfMfvmw/telemetry";

// LCD setup
LiquidCrystal_I2C lcd(0x27, 16, 2);

// DHT22 setup
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// MQ-135 setup
#define MQ135PIN 35

// Sensor data structure
typedef struct {
    float temperature;
    float humidity;
    int airQuality;
} SensorData;

SensorData currentData;

// Timing variables
unsigned long previousMillis = 0;
const long interval = 2000; // 2 seconds

void setup() {
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    Serial.print("Connecting");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected!");
    Serial.println(WiFi.localIP());

    // Initialize LCD
    lcd.init();
    lcd.backlight();

    // Initialize DHT22 sensor
    dht.begin();
}

// =============================================
// Function to send sensor data to ThingsBoard
// =============================================
void sendToServer(float temp, float hum, int air) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverURL); // URL contains device token
        http.addHeader("Content-Type", "application/json");

        // Build JSON string
        String jsonData = "{\"temperature\":" + String(temp) +
                          ",\"humidity\":" + String(hum) +
                          ",\"airQuality\":" + String(air) + "}";

        Serial.println("Sending JSON: " + jsonData);

        int httpResponseCode = http.POST(jsonData);

        if (httpResponseCode > 0) {
            Serial.print("Server Response: ");
            Serial.println(httpResponseCode); // 200 = OK
        } else {
            Serial.print("Error sending POST: ");
            Serial.println(httpResponseCode); // -1 = connection failed
        }

        http.end();
    } else {
        Serial.println("WiFi disconnected! Cannot send data.");
    }
}

void loop() {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;

        // Read DHT22 sensor
        float temp = dht.readTemperature();
        float hum = dht.readHumidity();
        if (!isnan(temp)) currentData.temperature = temp;
        if (!isnan(hum)) currentData.humidity = hum;

        // Read MQ-135 air quality
        currentData.airQuality = analogRead(MQ135PIN);

        // Display on LCD without flickering
        lcd.setCursor(0, 0);
        lcd.print("T:");
        lcd.print(currentData.temperature, 1);
        lcd.print("C H:");
        lcd.print(currentData.humidity, 1);
        lcd.print("%  "); // clear extra chars

        lcd.setCursor(0, 1);
        lcd.print("AQI:");
        lcd.print(currentData.airQuality);
        lcd.print("    "); // clear extra chars

        // Serial debug output
        Serial.print("Temp: "); Serial.print(currentData.temperature);
        Serial.print("C, Hum: "); Serial.print(currentData.humidity);
        Serial.print("%, AQI: "); Serial.println(currentData.airQuality);

        // Send telemetry to ThingsBoard
        sendToServer(currentData.temperature, currentData.humidity, currentData.airQuality);
    }
}
