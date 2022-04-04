import RPi.GPIO as GPIO
import time


dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
troyka = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)


def bin_2(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = bin_2(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    for value in range(256):
        signal = num2dac(value)
        voltage = value / levels * maxVoltage
        time.sleep(0.007)
        compValue = GPIO.input(comp)
        if compValue == 0:
            print("ADC value: = {} -> {}, input voltage = {:.2f}".format(value, signal, voltage))
            break


try:
    while True:
        adc()

finally:
    time.sleep(10)
    GPIO.output(dac, 0)
    GPIO.cleanup()
