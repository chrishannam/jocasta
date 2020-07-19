#define DHTPIN 2
#define DHTTYPE DHT22
#define ONE_WIRE_BUS 3

#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include <OneWire.h>
#include <DallasTemperature.h>

DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);


float humidity;
float temperature;
float light;


void setup() {
  Serial.print("Starting");
  Serial.begin(9600);
  dht.begin();

  if (!tsl.begin())
  {
    /* There was a problem detecting the TSL2561 ... check your connections */
    Serial.print("Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

  /* Setup the sensor gain and integration time */
  configureSensor();

}

void loop() {

  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  sensors_event_t event;
  tsl.getEvent(&event);
  if (event.light)
  {
    light = event.light;
  }
  else
  {
    /* If event.light = 0 lux the sensor is probably saturated
       and no reliable data could be generated! */
    light = -1;
  }


  Serial.print("{");
  Serial.print("\"temperature\":");
  Serial.print(temperature);
  Serial.print(",\"humidity\":");
  Serial.print(humidity);
  Serial.print(",\"light\":");
  Serial.print(light);
  Serial.print(",\"location\":\"outside\"");
  Serial.print(",\"name\":\"greenhouse_two\"");
  Serial.println("}");

  delay(1000); //just here to slow down the output for easier reading

}

void configureSensor(void)
{
  /* You can also manually set the gain or enable auto-gain support */
  //tsl.setGain(TSL2561_GAIN_1X);      /* No gain ... use in bright light to avoid sensor saturation */
  // tsl.setGain(TSL2561_GAIN_16X);     /* 16x gain ... use in low light to boost sensitivity */
  //tsl.enableAutoRange(true);          /* Auto-gain ... switches automatically between 1x and 16x */

  /* Changing the integration time gives you better sensor resolution (402ms = 16-bit data) */
  //tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);      /* fast but low resolution */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_101MS);  /* medium resolution and speed   */
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_402MS);  /* 16-bit data but slowest conversions */

}
