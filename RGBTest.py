import RPi.GPIO as GPIO
import time

# Define LED colors in hexadecimal format
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]

# Define GPIO pins using the BOARD numbering system
pins = {'pin_R': 11, 'pin_G': 12, 'pin_B': 13}

# Set up GPIO
GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location

# Set up GPIO pins as output
for i in pins:
    GPIO.setup(pins[i], GPIO.OUT)
    GPIO.output(pins[i], GPIO.LOW)  # Set pins to high(+3.3V) to switch on LED

# Initialize PWM objects for each color
p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequency to 2KHz
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 5000)

# Start PWM with initial duty cycle = 0 (LEDs off)
p_R.start(0)
p_G.start(0)
p_B.start(0)

# Function to map values from one range to another
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Function to set the color based on the provided hexadecimal value
def setColor(col):
    R_val = (col & 0xFF0000) >> 16
    G_val = (col & 0x00FF00) >> 8
    B_val = (col & 0x0000FF) >> 0

    # Map color values from 0-255 to 0-100 for PWM duty cycle
    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)

    # Set PWM duty cycle for each color
    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)

try:
    # Main loop to cycle through colors
    while True:
        for col in colors:
            setColor(col)
            time.sleep(0.5)

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    p_R.stop()
    p_G.stop()
    p_B.stop()
    for i in pins:
        GPIO.output(pins[i], GPIO.LOW)  # Turn off all LEDs
    GPIO.cleanup()