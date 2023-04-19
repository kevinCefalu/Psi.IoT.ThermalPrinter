import time
import numpy as np
from gpiozero import Button, RGBLED
from colorzero import Color

# Define the pins

btnPin = 23
btnLedRedPin = 12
btnLedGreenPin = 13
btnLedBluePin = 19
# btnBounceTime = 400

printerBaudRate = 9600
printerTimeout = 5

btn = Button(btnPin)
btnLed = RGBLED(btnLedRedPin, btnLedGreenPin, btnLedBluePin, False)

def onButtonHeld(btn):
  print('Button {btnName} held'.format(btnName = btn.pin.number))
  # Set LED to RED
  btnLed.color = Color('red')
  print('Red')
  time.sleep(3)

  # Set LED to GREEN
  btnLed.color = Color('green')
  print('Green')
  time.sleep(3)

  # Set LED to BLUE
  btnLed.color = Color('blue')
  print('Blue')
  time.sleep(3)

btn.when_held = onButtonHeld

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
