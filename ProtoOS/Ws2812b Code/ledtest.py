import board
import neopixel

NUM_LEDS = 512  # Change this to the number of LEDs in your strip
PIN = board.D18  # GPIO 18

pixels = neopixel.NeoPixel(PIN, NUM_LEDS, brightness=0.5, auto_write=False)

pixels.fill((255, 0, 0))  # Set all LEDs to red
pixels.show()  # Send data to LEDs

