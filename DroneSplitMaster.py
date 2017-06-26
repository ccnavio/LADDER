import RPi.GPIO as GPIO
import time

# Set mode to BCM
GPIO.setmode( GPIO.BCM )

print "GPIO mode set to BCM"

# Designate pins here
TRIG = 23

# Setup pins
print "Setting up pin inputs/outputs"

GPIO.setup( TRIG, GPIO.OUT )

# Wait for other to be ready
time.sleep(5)

# Send break up letter
GPIO.output( TRIG, True )

print "Break up letter sent"












