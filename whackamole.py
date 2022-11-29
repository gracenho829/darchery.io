from __future__ import print_function
import qwiic_i2c
import qwiic_button
import sys
import random
import time
import board
import busio
import adafruit_mpr121
import qwiic_led_stick
import math
import digitalio
import subprocess

import paho.mqtt.client as mqtt
import uuid

# parameters
round = 0
correct = 0
wrong = 0

# Fuction of rainbow effect
def walking_rainbow(LED_stick, rainbow_length, LED_length, delay, value):
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

        if value:  # just button A pressed Making correct
            round += 1
            correct += 2
            print(correct)
            time.sleep(0.1)

        elif not value:  # just button B pressed Making wrong
            round += 1
            wrong += 1
            print(wrong)
            time.sleep(0.1)

        time.sleep(delay)

def run_whack():
    # Configure Buttons
    print("\nConfig Buttons")
    my_button0 = qwiic_button.QwiicButton()
    my_button1 = qwiic_button.QwiicButton(0x5F)
    my_button2 = qwiic_button.QwiicButton(0x5E)
    my_button3 = qwiic_button.QwiicButton(0x5D)

    if my_button0.begin() == False:
        print("\nThe Qwiic Button 0 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    if my_button1.begin() == False:
        print("\nThe Qwiic Button 1 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    if my_button2.begin() == False:
        print("\nThe Qwiic Button 2 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    if my_button3.begin() == False:
        print("\nThe Qwiic Button 3 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    print("\nButton's ready!")

    # Configure Capacitive Touch
    print("\nConfig Capacitive Touch")
    i2c = busio.I2C(board.SCL, board.SDA)
    mpr121 = adafruit_mpr121.MPR121(i2c)
    print("\nCapacitive Touch Ready")

    # Configure
    print("\nSparkFun Qwiic LED Stick Example 1")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the sytsem. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")
    my_stick.set_all_LED_brightness(1)
    global round,correct,wrong

    out = []
    brightness = 100

    nxt1 = 0.0
    pushTime = time.time() + random.randrange(1, 4.0)
    popTime = pushTime + random.randrange(1, 3.0)
    prev = -1
    while True:
        # Generate next mole to pop up
        num = random.randint(0,4)
        while num == prev:
            num = random.randint(0,4)
        if len(out) < 2:
            popTime = pushTime + random.randrange(1, 4.0) 
            if pushTime < time.time():
                pushTime = time.time() + random.randrange(1, 3.0)
                out.append(num)
        
        # Bring mole down if it wasn't whacked
        if popTime < time.time():
            out.pop(0)

        # Visualize moles
        arr = [0, 0, 0, 0, 0]
        for x in out:
            arr[x] = 1
        
        # Check if button 0 is pressed
        if 0 in out:
            # print("\nButton 0 is pressed!")
            my_button0.LED_on(brightness)
        else:
            my_button0.LED_off()
            

        # Check if button1 is pressed
        if 1 in out:
            # print("\nButton 1 is pressed!")
            my_button1.LED_on(brightness)
        else:
            my_button1.LED_off()

        # Check if button2 is pressed
        if 2 in out:
            # print("\nButton 2 is pressed!")
            my_button2.LED_on(brightness)
        else:
            my_button2.LED_off()

        # Check if button3 is pressed
        if 3 in out:
            # print("\nButton 3 is pressed!")
            my_button3.LED_on(brightness)
        else:
            my_button3.LED_off()

        time.sleep(0.02)    # Don't hammer too hard on the I2C bus

        prev = num
        
        print(arr)

        # Check for whack
        # press = int(input())
        # if press in out:
        #     out.pop(out.index(press))
        #     print("Whack!")
        for i in range(4):
            if mpr121[i].value:
                if i in out:
                    out.pop(out.index(i))
                    val = f"Mole {i} whacked!"
                    print(val)
                    # walking_rainbow()
                    round += 1
                    my_stick.set_single_LED_color(round, 0, 255, 0)
                else:
                    round += 1
                    my_stick.set_single_LED_color(round, 255, 0, 0)
                    round = 0

                    wrong += 1
                    # time.sleep(0.3)
                    my_stick.LED_off()
                    
                # client.publish(topic, val)
        # time.sleep(0.25)

if __name__ == '__main__':
    try:
        run_whack()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 7")
        sys.exit(0)
