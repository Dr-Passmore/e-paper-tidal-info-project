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
    def loading_message():
        print("loading")
        
    def display_tide_info(event, height, eventTime, pastevent, pastheight, previousEventTime, progress):
        logging.info("init and Clear")
        epd = epd2in13bc.EPD()
        epd.init()
        epd.Clear()
        time.sleep(1)
        
        
        print("Tide info")
        einkUpdate.loading_message()
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