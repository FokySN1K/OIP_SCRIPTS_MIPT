import RPi.GPIO as GPIO
import time

def bin(num, number):
    i = 7
    if num >= 256 or num < 0:
        print("FAAAALSE")
        return 0
    while num != 0:
        number[i] = num % 2
        num //= 2
        i -= 1


GPIO.setmode(GPIO.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
number = [0, 0, 0, 0, 0 ,0 , 0, 0]

GPIO.setup(dac, GPIO.OUT)
GPIO.output(dac, 0)

bin(127, number)

GPIO.output(dac, number)

time.sleep(6)
GPIO.output(dac, 0)



GPIO.cleanup()