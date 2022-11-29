from __future__ import print_function
import qwiic_i2c
import qwiic_button
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Button Example 7")
    my_button1 = qwiic_button.QwiicButton()
    my_button2 = qwiic_button.QwiicButton(0x5F)
    my_button3 = qwiic_button.QwiicButton(0x5E)
    my_button4 = qwiic_button.QwiicButton(0x5D)

    if my_button1.begin() == False:
        print("\nThe Qwiic Button 1 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    if my_button2.begin() == False:
        print("\nThe Qwiic Button 2 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    if my_button3.begin() == False:
        print("\nThe Qwiic Button 2 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    if my_button4.begin() == False:
        print("\nThe Qwiic Button 2 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nButton's ready!")

    while 1:

        # Check if button 1 is pressed
        if my_button1.is_button_pressed() == True:
            print("\nButton 1 is pressed!")
        
        # Check if button2 is pressed
        if my_button2.is_button_pressed() == True:
            print("\nButton 2 is pressed!")
        
        # Check if button3 is pressed
        if my_button3.is_button_pressed() == True:
            print("\nButton 3 is pressed!")
        
        # Check if button4 is pressed
        if my_button4.is_button_pressed() == True:
            print("\nButton 4 is pressed!")
        
        time.sleep(0.02)    # Don't hammer too hard on the I2C bus

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 7")
        sys.exit(0)
