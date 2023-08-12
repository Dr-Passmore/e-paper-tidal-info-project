import logging
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd2in13bc
import time
import os





class einkUpdate:
    def __init__(self) -> None:
        
        
        pass
    def error_display(e):
        print(f"error: {e}")
        epd = epd2in13bc.EPD()
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)
        picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
        robotoblack32 = ImageFont.truetype(os.path.join(picdir, 'Roboto-Black.ttf'), 32)
        drawblack = ImageDraw.Draw(HBlackimage)
        
        drawblack.text((2, 0), f'hello world {e}', font = robotoblack32, fill = 0)
        epd.sleep()
    
    def refresh_display(epd):
        epd.init()
        epd.Clear()
        time.sleep(1)
    
    def loading_message(epd):
        print("loading")
        
    def display_tide_info(event, height, eventTime, pastevent, pastheight, previousEventTime, progress):
        logging.info("init and Clear")
        epd = epd2in13bc.EPD()
        einkUpdate.refresh_display(epd)
        
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)
        picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
        robotoblack32 = ImageFont.truetype(os.path.join(picdir, 'Roboto-Black.ttf'), 32)
        drawblack = ImageDraw.Draw(HBlackimage)
        
        drawblack.text((2, 0), 'hello world', font = robotoblack32, fill = 0)
        
        
        print("Tide info")
        einkUpdate.loading_message(epd)
        print(f"{event}: {eventTime} with a height of {height}M")
        
        
        epd.sleep()
        
        
        updateCompleted = "e-ink screen refresh has succesfully completed"
        logging.info(updateCompleted)
        
        return updateCompleted

logging.basicConfig(filename='TideInfo.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    tide_display = einkUpdate()