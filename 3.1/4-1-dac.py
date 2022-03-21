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
        x = input("Введите целочисленное значение от 0 до 255 или 'q' для выхода \n")
        if x == 'q':
            break
        elif( not x.isdigit()):
            try:
                float(x)
                print("Ошибка: введено число с плавающей точкой")
                continue
            except ValueError:
                print("Ошибка: введена строка")
                continue
        else:
            x = int(x)
            VOLT = (3.3*x/256)
            if(0 <= x <= 255):
                number = bin_2(x)
                GPIO.output(dac, number)
                print("Предполагаемое значение напряжения на выходе: ", VOLT)
                break
            else:
                print("Ошибка: введено число, несоответствующее заданным условиям")
                continue
finally:
    time.sleep(1)
    GPIO.output(dac, 0)
    GPIO.cleanup()

