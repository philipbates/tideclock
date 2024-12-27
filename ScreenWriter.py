'''
****************************************************************
****************************************************************

                TideTracker for E-Ink Display

                        by Sam Baker
        Modified for UK tides API and 5.83" screen by Gwil

****************************************************************
****************************************************************
'''

import time
from PIL import Image, ImageDraw, ImageFont
from lib.waveshare_epd import epd4in26



# Initialize and clear screen
print('Initializing and clearing screen.')
epd = epd4in26.EPD() # Create object for display functions
epd.init()
print('Screen initialized.')
epd.Clear()
print('Screen cleared.')




# define funciton for writing image and sleeping for specified time
def write_to_screen(image):
    print('Writing to screen.') # for debugging
    # Create new blank image template matching screen resolution
    h_image = Image.new('1', (epd.width, epd.height), 255)
    # Open the template
    if image is None:   
        picfile = r"wave.png"
        image = Image.open(picfile)
    print('Screen output file opened.') # for debugging
    # Initialize the drawing context with template as background
    #ensure the image is the same size as the screen
    image = image.resize((epd.width, epd.height))
    h_image.paste(image, (0, 0))
    print('Screen output file pasted.') # for debugging
    epd.display(epd.getbuffer(h_image))
    print('Screen output file displayed.') # for debugging
    # Sleep
    epd.sleep() # Put screen to sleep to prevent damage
    # print('Sleeping for ' + str(sleep_seconds) +'.')
    # time.sleep(sleep_seconds) # Determines refresh rate on data
    # epd.init() # Re-Initialize screen
    # print('Screen re-initialized.') # for debugging


# define function for displaying error
def display_error():
    print('Writing to screen.') # for debugging
    # Create new blank image template matching screen resolution
    h_image = Image.new('1', (epd.width, epd.height), 255)   
    picfile = r"wave.png"
    image = Image.open(picfile)
    print('Screen output file opened.') # for debugging
    # Initialize the drawing context with template as background
    #ensure the image is the same size as the screen
    # image = image.resize((epd.width, epd.height))
    h_image.paste(image, (0, 0))
    print('Screen output file pasted.') # for debugging
    epd.display(epd.getbuffer(h_image))
    print('Screen output file displayed.') # for debugging
    # Sleep
    epd.sleep() # Put screen to sleep to prevent damage
    # print('Sleeping for ' + str(sleep_seconds) +'.')
    # time.sleep(sleep_seconds) # Determines refresh rate on data
    # epd.init() # Re-Initialize screen
    # print('Screen re-initialized.') # for debugging



if __name__ == "__main__":
    print('Running main function.')
    display_error()

