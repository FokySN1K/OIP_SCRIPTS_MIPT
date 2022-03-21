import RPi.GPIO as GPIO
import time

def bin_2(number):
    return [int(i) for i in bin(number)[2:].zfill(8)]

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
number = [0, 0, 0, 0, 0 ,0 , 0, 0]
GPIO.setup(dac, GPIO.OUT)
GPIO.output(dac, 0)

try:
    while True:
        for x in range(0, 256):
            VOLT = (3.3*x/256)
            number = bin_2(x)
            GPIO.output(dac, number)
            print("Предполагаемое значение напряжения на выходе: ", VOLT)
            time.sleep(0.5)
            continue
finally:
    time.sleep(1)
    GPIO.output(dac, 0)
    GPIO.cleanup()

