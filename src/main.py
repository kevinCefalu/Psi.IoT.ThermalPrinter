import time
import numpy as np
import serial
from gpiozero import Button, RGBLED
from colorzero import Color
import adafruit_thermal_printer

# Define the pins
btnPin = 23
btnLedRedPin = 12
btnLedGreenPin = 13
btnLedBluePin = 19

# Define the printer settings
serialPath = "/dev/serial0"
printerClass = 2.69
printerBaudRate = 9600
printerTimeout = 3000

btn = Button(btnPin)
btnLed = RGBLED(btnLedRedPin, btnLedGreenPin, btnLedBluePin, False)

thermalPrinterClass = adafruit_thermal_printer.get_printer_class(printerClass)
uart = serial.Serial(serialPath, baudrate = printerBaudRate, timeout = printerTimeout)
printer = thermalPrinterClass(uart)

def printWorkDetails():
  printer.warm_up()
  printer.feed(1)
  printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
  printer.size = adafruit_thermal_printer.SIZE_LARGE
  printer.print("Kevin Cefalu")
  printer.size = adafruit_thermal_printer.SIZE_MEDIUM
  printer.print("Netchex, Senior DevOps")
  printer.print("Engineer III")
  printer.feed(2)
  printer.print("Mandeville, La 70448")
  printer.print("kcefalu@netchexonline.com")
  printer.feed(4)

def fadeFromToColor(fromColor, toColor, steps = 100, delay = 0.025):
  for color in fromColor.gradient(toColor, steps = steps):
    btnLed.color = color
    time.sleep(delay)

def onButtonHeld(btn):
  fadeFromToColor(Color('black'), Color('yellow'))
  time.sleep(2)
  printWorkDetails()
  fadeFromToColor(Color('yellow'), Color('green'))
  time.sleep(2)
  btnLed.color = Color('black')

btn.when_held = onButtonHeld

message = input("Press enter to quit\n\n")
