import RPi.GPIO as GPIO
import time
import numpy as np

# Define the pins

btn = 23
btnLedRedPin = 12
btnLedGreenPin = 13
btnLedBluePin = 19

btnBounceTime = 400
printerBaudRate = 9600
printerTimeout = 5

# Choose a frequency for PWM:
# Frequency can be any number above 0
# 256 because we are going to use 8-bit per channel
frequency = 256

calcDutyCycle = lambda x: 100 - x * 100 / 256

GPIO.setmode(GPIO.BCM)  # Used for GPIO numbering
GPIO.setwarnings(False) # Clear warnings

GPIO.setup(btnLedRedPin, GPIO.OUT)
GPIO.setup(btnLedGreenPin, GPIO.OUT)
GPIO.setup(btnLedBluePin, GPIO.OUT)

# Set GPIO to PWM mode to frequency defined above
btnLedRed = GPIO.PWM(btnLedRedPin, frequency)
btnLedGreen = GPIO.PWM(btnLedGreenPin, frequency)
btnLedBlue = GPIO.PWM(btnLedBluePin, frequency)

running = True

# Common Anode RGB LED, so we need to invert the PWM signal
btnLedRed.start(100)
btnLedGreen.start(100)
btnLedBlue.start(100)

while running:
  try:
    # for x in range(100, 0, -1):
    #   btnLedRed.ChangeDutyCycle(x)
    #   time.sleep(0.025)

    # Set LED to RED
    btnLedRed.ChangeDutyCycle(calcDutyCycle(100))
    btnLedGreen.ChangeDutyCycle(calcDutyCycle(0))
    btnLedBlue.ChangeDutyCycle(calcDutyCycle(0))
    print('Red')
    time.sleep(3)

    # Set LED to GREEN
    btnLedRed.ChangeDutyCycle(calcDutyCycle(0))
    btnLedGreen.ChangeDutyCycle(calcDutyCycle(100))
    btnLedBlue.ChangeDutyCycle(calcDutyCycle(0))
    print('Green')
    time.sleep(3)

    # Set LED to BLUE
    btnLedRed.ChangeDutyCycle(calcDutyCycle(0))
    btnLedGreen.ChangeDutyCycle(calcDutyCycle(0))
    btnLedBlue.ChangeDutyCycle(calcDutyCycle(100))
    print('Blue')
    time.sleep(3)

  # On Keyboard Interrupt, stop the loop
  except KeyboardInterrupt:
    running = False

# Stop PWM
btnLedRed.stop()
btnLedGreen.stop()
btnLedBlue.stop()

# Clean up GPIO
GPIO.cleanup()
