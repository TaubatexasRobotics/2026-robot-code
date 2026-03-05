#include <FastLED.h>

#define LED_PIN 7
#define NUM_LEDS 60

CRGB leds[NUM_LEDS];
uint8_t waveOffset = 0;

void changeColor(int red, int green, int blue) {
  for (int i = 0; i < NUM_LEDS; i++)
    leds[i] = CRGB(red, green, blue);
  FastLED.show();
}

void rainbow() {
  for(int i = 0; i < NUM_LEDS; i++) {
    uint8_t wave = sin8(i * 12 + waveOffset);
    leds[i] = CHSV(i * 5 + waveOffset, 255, wave);
  }
  FastLED.show();
  waveOffset += 4;
  delay(20);
}

void blinkGreen() {
  changeColor(0, 255, 0);
  delay(500);
  changeColor(0, 0, 0);
}

void updateSelectedColor() {
  if (Serial.available() > 0) {
    byte received = Serial.read();
    if (received == 'r')
      changeColor(255, 0, 0);
    else if (received == 'g')
      changeColor(0, 255, 0);
    else if (received == 'b')
      changeColor(0, 0, 255);
    else if (received == 'w')
      blinkGreen();
    else if (received == 'a')
      rainbow();
  }
}

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  changeColor(255, 0, 0);
}

void loop() {
  updateSelectedColor();
}
