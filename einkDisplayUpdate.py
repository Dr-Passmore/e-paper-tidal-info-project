import logging
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd2in13bc
import time






class einkUpdate:
    def __init__(self) -> None:
        
        
        pass
    def error_display(e):
        print(f"error: {e}")
        epd = epd2in13bc.EPD()
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)
        
        robotoblack32 = ImageFont.truetype('pic/Roboto-Black.ttf', 32)
        drawblack = ImageDraw.Draw(HBlackimage)
        
        drawblack.text((2, 0), f'hello world {e}', font = robotoblack32, fill = 1)
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
        robotoblack32 = ImageFont.truetype('pic/Roboto-Black.ttf', 32)
        robotoblack18 = ImageFont.truetype('pic/Roboto-Black.ttf', 18)
        drawblack = ImageDraw.Draw(HBlackimage)
        
        #drawblack.text((2, 0), 'hello world', font = robotoblack32, fill = 0)
        drawblack.text((2, 0), f'event: {event}', font = robotoblack18, fill = 0)
        drawblack.text((2, 20), f'height: {height:.2f}', font = robotoblack18, fill = 0)
        drawblack.text((2, 40), f'Time: {eventTime}', font = robotoblack18, fill = 0)
        
        print("Tide info")
        einkUpdate.loading_message(epd)
        print(f"{event}: {eventTime} with a height of {height}M")
        
        epd.Clear()
        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HBlackimage))
        
        
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