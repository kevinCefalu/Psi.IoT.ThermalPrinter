import logging
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

logging.basicConfig(level=logging.INFO, filename='print-requests.log',
                    format='%(asctime)s :: %(levelname)s :: %(message)s')

logging.info("Starting print request service...")

btn = Button(btnPin)
btnLed = RGBLED(btnLedRedPin, btnLedGreenPin, btnLedBluePin, False)
logging.debug("Button setup complete")

thermalPrinterClass = adafruit_thermal_printer.get_printer_class(printerClass)
uart = serial.Serial(serialPath, baudrate = printerBaudRate, timeout = printerTimeout)
printer = thermalPrinterClass(uart)
logging.debug("Printer setup complete")

def fadeFromToColor(fromColor, toColor, steps = 100, delay = 0.025):
  for color in fromColor.gradient(toColor, steps = steps):
    btnLed.color = color
    time.sleep(delay)

def printWorkDetails():
  logging.info("Printing work details")
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

def onButtonHeld(btn):
  logging.debug("Button held")
  fadeFromToColor(Color('black'), Color('gold'))
  time.sleep(2)
  printWorkDetails()
  fadeFromToColor(Color('gold'), Color('green'))
  time.sleep(2)
  btnLed.color = Color('black')

btn.when_held = onButtonHeld

logging.info("Started print request service...")

message = input("Press enter to quit...")

logging.info("Stopping print request service.")
