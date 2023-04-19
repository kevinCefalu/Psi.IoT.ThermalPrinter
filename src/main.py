import time
import numpy as np
from gpiozero import Button, RGBLED
from colorzero import Color
from lib import Adafruit_Thermal

# Define the pins

btnPin = 23
btnLedRedPin = 12
btnLedGreenPin = 13
btnLedBluePin = 19

printerBaudRate = 9600
printerTimeout = 5

btn = Button(btnPin)
btnLed = RGBLED(btnLedRedPin, btnLedGreenPin, btnLedBluePin, False)
printer = Adafruit_Thermal("/dev/serial0", printerBaudRate, timeout = printerTimeout)

def linear(steps):
  for t in range(steps):
    yield t / (steps - 1)

def ease_in(steps):
  for t in linear(steps):
    yield t ** 2

def ease_out(steps):
  for t in linear(steps):
    yield t * (2 - t)

def ease_in_out(steps):
  for t in linear(steps):
    yield 2 * t * t if t < 0.5 else (4 - 2 * t) * t - 1

def onButtonHeld(btn):
  # Personal Business Card requested
  for color in Color('black').gradient(Color('red'), steps = 100):
    btnLed.color = color
    time.sleep(0.025)
  time.sleep(2)
  printer.feed(1)
  printer.justify('C')
  printer.setSize('L')
  printer.println("Kevin Cefalu")
  printer.setSize('M')
  printer.println("Netchex, Senior DevOps Engineer III")
  printer.feed(2)
  printer.println("Mandeville, La 70448")
  printer.println("kcefalu@netchexonline.com")
  printer.feed(4)

  # Restore printer to defaults
  printer.setDefault()

  for color in Color('red').gradient(Color('green'), steps = 100):
    btnLed.color = color
    time.sleep(0.025)
  time.sleep(5)
  btnLed.color = Color('black')
  return

btn.when_held = onButtonHeld

message = input("Press enter to quit\n\n")

# running = True

# while running:
#   try:
#     # for x in range(100, 0, -1):
#     #   btnLedRed.ChangeDutyCycle(x)
#     #   time.sleep(0.025)

#     # Set LED to RED
#     btnLed.color = Color('red')
#     print('Red')
#     time.sleep(3)

#     # Set LED to GREEN
#     btnLed.color = Color('green')
#     print('Green')
#     time.sleep(3)

#     # Set LED to BLUE
#     btnLed.color = Color('blue')
#     print('Blue')
#     time.sleep(3)

#   # On Keyboard Interrupt, stop the loop
#   except KeyboardInterrupt:
#     running = False
