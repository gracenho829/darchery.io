from __future__ import print_function
import qwiic_led_stick
import math
import time
import sys
import board
import digitalio
import subprocess


# buttons set up
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# parameters
round = 0
correct = 0
wrong = 0

# Fuction of rainbow effect
def walking_rainbow(LED_stick, rainbow_length, LED_length, delay):
    red_array = [None] * LED_length
    blue_array = [None] * LED_length
    green_array = [None] * LED_length

    global round,correct,wrong

    for j in range(0, rainbow_length):

        for i in range(0, LED_length):
            # There are n colors generated for the rainbow
            # The value of n determins which color is generated at each pixel
            n = i + 1 - j

            # Loop n so that it is always between 1 and rainbow_length
            if n <= 0:
                n = n + rainbow_length

            # The nth color is between red and yellow
            if n <= math.floor(rainbow_length / 6):
                red_array[i] = 255
                green_array[i] = int(math.floor(6 * 255 / rainbow_length * n))
                blue_array[i] = 0
            
            # The nth color is between yellow and green
            elif n <= math.floor(rainbow_length / 3):
                red_array[i] = int(math.floor(510 - 6 * 255 / rainbow_length * n))
                green_array[i] = 255
                blue_array[i] = 0
            
            # The nth color is between green and cyan
            elif n <= math.floor(rainbow_length / 2):
                red_array[i] = 0
                green_array[i] = 255
                blue_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 510))
            
            # The nth color is between blue and magenta
            elif n <= math.floor(5 * rainbow_length / 6):
                red_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 1020))
                green_array[i] = 0
                blue_array[i] = 255
            
            # The nth color is between magenta and red
            else:
                red_array[i] = 255
                green_array[i] = 0
                blue_array[i] = int(math.floor(1530 - (6 *255 / rainbow_length * n)))

        # Set all the LEDs to the color values accordig to the arrays
        LED_stick.set_all_LED_unique_color(red_array, green_array, blue_array, LED_length)

        if buttonB.value and not buttonA.value:  # just button A pressed Making correct
            round += 1
            correct += 2
            print(correct)
            time.sleep(0.1)

        elif buttonA.value and not buttonB.value:  # just button B pressed Making wrong
            round += 1
            wrong += 1
            print(wrong)
            time.sleep(0.1)

        time.sleep(delay)

"""
For this LED-scoring system, we want to make such effect:
Normal Mode:
After the player start the game, each time the player hit a mole, a Green LED will light up. If the player miss a mole, a Red
LED will light up. The order is from left to right.

Crazy Time:
When User hit 10/10 moles, the system will get into the Crazy time so that all points are x5 times, 
and the LED will show rainbow effect.
"""

def run_example():
    print("\nSparkFun Qwiic LED Stick Example 1")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the sytsem. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")
    
    my_stick.set_all_LED_brightness(1)
    global round,correct,wrong
    while True:
        my_stick.LED_off()

        while round < 10:
            if buttonB.value and not buttonA.value:  # just button A pressed Making correct
                round += 1
                my_stick.set_single_LED_color(round, 0, 255, 0)
                
                correct += 1
                time.sleep(0.1)

            elif buttonA.value and not buttonB.value:  # just button B pressed Making wrong
                round += 1
                my_stick.set_single_LED_color(round, 255, 0, 0)
                round = 0

                wrong += 1
                time.sleep(0.3)
                my_stick.LED_off()

            time.sleep(0.1)
        while 10 <= correct and round < 15:
            walking_rainbow(my_stick, 20, 10, 0.1)
        
        round = 0
            
        #else:
        #    my_stick.set_all_LED_color(255, 0, 0)


        my_stick.LED_off()
        time.sleep(1)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)