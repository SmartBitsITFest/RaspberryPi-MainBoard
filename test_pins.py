import RPi.GPIO as GPIO
from time import sleep
# Set GPIO mode and pins
GPIO.setmode(GPIO.BOARD)

# Define the pins for the buttons
b1 = 16  # Replace 11 with the actual pin number for Button 1
b2 = 18 # Replace 13 with the actual pin number for Button 2
GPIO.setup(b1, GPIO.IN)
GPIO.setup(b2, GPIO.IN)
def is_on(bt):
    return GPIO.input(bt)
    
def check_mode(b1,b2,seconds=1.5,percent=0.75):
    count_b1 = 0
    count_b2 = 0
    for i in range(int(seconds*10)):
        count_b1 += int(is_on(b1))
        count_b2 += int(is_on(b2))
        sleep(0.1)
    if count_b1 >= seconds*percent and count_b2 >= seconds*percent:
        print('both')
        sleep(0.5)
    elif count_b1 >= seconds*percent:
        print('b1')
        sleep(0.5)
    elif count_b2 >= seconds*percent:
        print('b2')
        sleep(0.5)
        
try:
    print("Press CTRL+C to exit")
    while True:
        if is_on(b1) or is_on(b2):
            check_mode(b1,b2)
            
        sleep(0.1)


except KeyboardInterrupt:
    print("\nExiting program")

