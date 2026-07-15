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
import os



# # Initialize and clear screen
# print('Initializing and clearing screen.')
# epd = epd4in26.EPD() # Create object for display functions
# epd.init()
# print('Screen initialized.')
# epd.Clear()
# print('Screen cleared.')


def init_screen():
    print('Initializing and clearing screen.')
    epd = epd4in26.EPD() # Create object for display functions
    epd.init()
    print('Screen initialized.')
    return epd


def _prepare_image_for_epd(picfile, epd):
    """Load and normalize an image for 1-bit full refresh on epd4in26."""
    image_path = os.path.abspath(picfile)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path)
    image = image.resize((epd.width, epd.height))
    return image.convert('1')


# define funciton for writing image and sleeping for specified time
def write_to_screen(picfile, epd):
    print('Writing to screen.') # for debugging
    # Create new blank image template matching screen resolution
    h_image = Image.new('1', (epd.width, epd.height), 255)
    # Open and normalize the image for the panel
    image = _prepare_image_for_epd(picfile, epd)
    print('Screen output file opened.') # for debugging
    # Initialize the drawing context with template as background
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
def display_error(picfile, epd):
    print('Writing to screen.') # for debugging
    # Create new blank image template matching screen resolution
    h_image = Image.new('1', (epd.width, epd.height), 255)   
    image = _prepare_image_for_epd(picfile, epd)
    print('Error screen output file opened.') # for debugging
    # Initialize the drawing context with template as background
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

def partial_refresh(picfile, epd):
    print('Performing partial refresh.')  # for debugging
    image = _prepare_image_for_epd(picfile, epd)
    h_image = Image.new('1', (epd.width, epd.height), 255)
    h_image.paste(image, (0, 0))
    epd.display_Partial(epd.getbuffer(h_image))
    print('Partial refresh complete.')  # for debugging

if __name__ == "__main__":
    print('Running main function.')
    display_error()

