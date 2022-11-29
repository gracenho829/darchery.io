from __future__ import print_function
import qwiic_button
import time
import sys

brightness = 100

def run_example():

    print("\nSparkFun Qwiic Button Example 2")
    my_button = qwiic_button.QwiicButton(0x5D)

    if my_button.begin() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nButton ready!")

    while True:

        if my_button.is_button_pressed() == True:
            print("\nThe button is pressed!")
            my_button.LED_on(brightness)
        
        else:
            print("\nThe button is not pressed.")
            my_button.LED_off()
        
        time.sleep(0.02)
    
if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 2")
        sys.exit(0)
