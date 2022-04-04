import RPi.GPIO as GPIO
import time


dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
troyka = 17
leds = [21, 20, 16, 12, 7, 8, 25, 24]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

def bin_2(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = bin_2(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    left = 0
    right = 256
    value = 128
    #voltage = value / levels * maxVoltage
    while right - value != 1:
        signal = num2dac(value)
        time.sleep(0.001)
        compValue = GPIO.input(comp)
        if compValue:
            left = value
            value += (right - value) // 2
        else:
            right = value
            value -= (value - left) // 2
    GPIO.output(leds, signal)                                                                    

try:
    while True:
        adc()


finally:
    time.sleep(10)
    GPIO.output(dac, 0)
    GPIO.cleanup()
