#include <FastLED.h>
#include <Pixy2.h>
#define LED_PIN 7
#define NUM_LEDS 30

CRGB leds[NUM_LEDS];
Pixy2 pixy;

void changeColor(int red, int green, int blue) {
  for (int i = 0; i < NUM_LEDS; i++)
    leds[i] = CRGB(red, green, blue);
  FastLED.show();
}

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  changeColor(255, 0, 0);
  pixy.init();
}

void loop() {
  {int i;
  pixy.ccc.getBlocks();

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
}
  if (pixy.ccc.numBlocks)
  {
    Serial.print("Detected ");
    Serial.println(pixy.ccc.numBlocks);
    for (i=0; i<pixy.ccc.numBlocks; i++)
    {
      Serial.print("  block ");
      Serial.print(i);
      Serial.print(": ");
      pixy.ccc.blocks[i].print();
    }
  }  
}
