import logging
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd2in13bc
import time
import configparser
import random






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
    
    def loading_message(epd, robotoblack12, robotoblack18, robotoblack32):
        
        #212(W) x 104(H) pixel
        logging.info("loading message - Records")
        
        previousRecords = ["high", "low"]
        LoadingBlackimage = Image.new('1', (epd.height, epd.width), 255)  
        Other = Image.new('1', (epd.height, epd.width), 255)
        drawLoadBlack = ImageDraw.Draw(LoadingBlackimage)
        draw_other = ImageDraw.Draw(Other)
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        startDate = config.get('Records', 'start date')
        highHeight = config.get('Records', 'highest tide height')
        highestTideDate = config.get('Records', 'highest tide date')
        lowHeight = config.get('Records', 'lowest tide height') 
        lowestTideDate = config.get('Records', 'lowest tide date')
        
        draw_other.rectangle((0, 0, epd.width, 40), fill=0)
        drawLoadBlack.text((30, 0), f'Records:', font=robotoblack32, fill=1)
        if random.choice(previousRecords) == "high":
            drawLoadBlack.text((2, 30), f'High Tide Height: {float(highHeight):.2f}', font=robotoblack18, fill=0)
            drawLoadBlack.text((2, 50), f'Time: {highestTideDate}', font=robotoblack18, fill=0)
            drawLoadBlack.text((2, 70), f'Since {startDate}', font=robotoblack12, fill=0)
            
        else: 
            drawLoadBlack.text((2, 30), f'Low Tide Height: {float(lowHeight):.2f}', font=robotoblack18, fill=0)
            drawLoadBlack.text((2, 50), f'Time: {lowestTideDate}', font=robotoblack18, fill=0)
            drawLoadBlack.text((2, 70), f'Since {startDate}', font=robotoblack12, fill=0)
        epd.Clear()
        epd.display(epd.getbuffer(LoadingBlackimage), epd.getbuffer(Other)) 
        
        time.sleep(180)
        
        einkUpdate.refresh_display(epd)
        
    def display_tide_info(event, height, eventTime, pastevent, pastheight, previousEventTime, progress):
        #212(H) x 104(V) pixel
        logging.info("init and Clear")
        epd = epd2in13bc.EPD()
        einkUpdate.refresh_display(epd)
        
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)
        Other = Image.new('1', (epd.width, epd.height), 255)
        robotoblack32 = ImageFont.truetype('pic/Roboto-Black.ttf', 32)
        robotoblack18 = ImageFont.truetype('pic/Roboto-Black.ttf', 18)
        robotoblack12 = ImageFont.truetype('pic/Roboto-Black.ttf', 12)
        drawblack = ImageDraw.Draw(HBlackimage)
        draw_other = ImageDraw.Draw(Other)
        einkUpdate.loading_message(epd, robotoblack12, robotoblack18, robotoblack32)
        
        #drawblack.text((2, 0), 'hello world', font = robotoblack32, fill = 0)
        drawblack.text((2, 0), f'event: {event}', font = robotoblack18, fill = 0)
        drawblack.text((2, 20), f'height: {height:.2f}', font = robotoblack18, fill = 0)
        drawblack.text((2, 40), f'Time: {eventTime}', font = robotoblack18, fill = 0)
        
        print("Tide info")
        
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