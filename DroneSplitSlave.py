import RPi.GPIO as GPIO
import time

# Set mode to BCM
GPIO.setmode( GPIO.BCM )

print "GPIO mode set to BCM"

# Designate pins here
ECHO = 23

# Setup pins
print "Setting up pin inputs/outputs"

GPIO.setup( ECHO, GPIO.IN )

# Callback function for event listener ( waiting for break up letter )
def call_back():
	# Dont EVER call back
	print "Break up letter received"
	exit();

# Receive break up letter
GPIO.add_event_detect( ECHO, GPIO.FALLING, callback=call_back)

time.sleep(3600);
