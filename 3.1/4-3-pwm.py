import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
22
p = GPIO.PWM(22, 1000)
p.start(0)

try:
    while True:
        dc = int(input())
        p.stop()
        p.start(dc)
        VOLT = 3.3*dc/100
        print(VOLT)
except:
    print("Fail")
finally:
    GPIO.cleanup()
        