import random
import json
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
printer = thermalPrinterClass(uart, auto_warm_up = False)
logging.debug("Printer setup complete")

f = open ('jokes.json', "r")
jokes = json.loads(f.read())

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
  printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
  printer.print("Kevin Cefalu")
  printer.underline = None
  printer.size = adafruit_thermal_printer.SIZE_MEDIUM
  printer.print("Senior DevOps Engineer III")
  printer.print("Netchex Online")
#   printer.size = adafruit_thermal_printer.SIZE_SMALL
  printer.feed(2)
#   printer.size = adafruit_thermal_printer.SIZE_MEDIUM
  printer.print("Mandeville, LA 70448")
  printer.print("kcefalu@netchexonline.com")
  printer.feed(1)
  printer.print("--------------------------------")
  printer.feed(1)
  printer.size = adafruit_thermal_printer.SIZE_SMALL
  for line in random.choice(jokes):
    printer.print(line)
  printer.feed(4)
  printer.set_defaults()

def printTest():
  printer.warm_up()

  # Print a test page:
  printer.test_page()

  # Move the paper forward two lines:
  printer.feed(1)

  # Print a line of text:
  printer.print("Hello world!")

  # Print a normal/thin underline line of text:
  printer.underline = adafruit_thermal_printer.UNDERLINE_THIN
  printer.print("Thin underline!")

  # Print a thick underline line of text:
  printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
  printer.print("Thick underline!")

  # Disable underlines.
  printer.underline = None

  # Print an inverted line.
  printer.inverse = True
  printer.print("Inverse hello world!")
  printer.inverse = False

  # Print a double height line.
  printer.double_height = True
  printer.print("Double height!")
  printer.double_height = False

  # Print a double width line.
  printer.double_width = True
  printer.print("Double width!")
  printer.double_width = False

  # Print medium size text.
  printer.size = adafruit_thermal_printer.SIZE_MEDIUM
  printer.print("Medium size text!")

  # Print large size text.
  printer.size = adafruit_thermal_printer.SIZE_LARGE
  printer.print("Large size text!")

  # Back to normal / small size text.
  printer.size = adafruit_thermal_printer.SIZE_SMALL

  # Print center justified text.
  printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
  printer.print("Center justified!")

  # Print right justified text.
  printer.justify = adafruit_thermal_printer.JUSTIFY_RIGHT
  printer.print("Right justified!")

  # Back to left justified / normal text.
  printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT

  # Print a UPC barcode.
  printer.print("UPCA barcode:")
  printer.print_barcode("123456789012", printer.UPC_A)

  # Feed a few lines to see everything.
  printer.feed(4)

def onButtonHeld(btn):
  logging.debug("Button held")

  if printer.has_paper():
    btnLed.pulse(0.5, 0.5, Color('teal'), Color('black'), 4)
    fadeFromToColor(Color('black'), Color('greenyellow'))
    time.sleep(2)
    printWorkDetails()
    fadeFromToColor(Color('teal'), Color('black'))
    btnLed.pulse(0.5, 0.5, Color('green'), Color('black'), 4)
    time.sleep(2)
  else:
    logging.error("Printer might be out of paper, or TX/RX is disconnected!")
    btnLed.pulse(0.5, 0.5, Color('red'), Color('black'), 8)

  btnLed.color = Color('black')

btn.when_held = onButtonHeld

logging.info("Started print request service...")

message = input("Press enter to quit...")

logging.info("Stopped print request service.")
