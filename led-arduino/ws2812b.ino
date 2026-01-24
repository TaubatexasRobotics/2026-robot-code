#include <FastLED.h>
#define LED_PIN 7
#define NUM_LEDS 30

CRGB leds[NUM_LEDS];

void changeColor(int red, int green, int blue) {
  for (int i = 0; i < NUM_LEDS; i++)
    leds[i] = CRGB(red, green, blue);
  FastLED.show();
}

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  changeColor(255, 0, 0);
}

void loop() {
  if (Serial.available() > 0) {
    byte received = Serial.read();
    if (received == 'r') {
      changeColor(255, 0, 0);
    else if (received == 'g')
      changeColor(0, 255, 0);
    else if (received == 'b')
      changeColor(0, 0, 255);
  }
}
