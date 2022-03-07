import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [21, 20, 16, 12, 7, 8, 25, 24]

GPIO.setup(leds, GPIO.OUT)

GPIO.output(leds, 0)

for i in range(100):
    for j in leds:
        GPIO.output(j, 1)
        time.sleep(0.1)
        GPIO.output(j, 0)

GPIO.output(leds, 0)

GPIO.cleanup()