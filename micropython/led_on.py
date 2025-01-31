from picozero import LED
from time import sleep
from machine import Pin

yellow = LED(14, Pin.OUT)

while True:
    yellow.on()
    sleep(1)
    yellow.off()
    sleep(1)
    

#from machine import Pin
#from time import sleep

#buzzer = Pin(14, Pin.OUT)  # Connect to GPIO 14

#while True:
 #   buzzer.on()  # Turn the buzzer on
  #  sleep(0.1)     # Wait for 1 second
   # buzzer.off() # Turn the buzzer off
    #sleep(1)   