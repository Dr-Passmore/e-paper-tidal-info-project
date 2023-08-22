import logging
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd2in13bc
import time
import configparser
import random
from datetime import datetime





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
        logging.info("Refreshing Display")
        epd.init()
        epd.Clear()
        time.sleep(1)
    
    def loading_message(epd, robotoblack14, robotoblack18, robotoblack24, robotoblack32):
        
        #212(W) x 104(H) pixel
        logging.info("loading message - Records")
        
        # Selection process for whether the loading screen shows low or high tide record
        previousRecords = ["high", "low"]
        selection = random.choice(previousRecords) 
        
        logging.info(f"Loading message of {selection} tide record selected")
        LoadingBlackimage = Image.new('1', (epd.height, epd.width), 255)  
        Other = Image.new('1', (epd.height, epd.width), 255)
        drawLoadBlack = ImageDraw.Draw(LoadingBlackimage)
        draw_other = ImageDraw.Draw(Other)
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Gets stored values from config.ini
        startDate = config.get('Records', 'start date')
        highHeight = config.get('Records', 'highest tide height')
        highestTideDate = config.get('Records', 'highest tide date')
        lowHeight = config.get('Records', 'lowest tide height') 
        lowestTideDate = config.get('Records', 'lowest tide date')
        
        # Title of 'Records' added at top of layout
        drawLoadBlack.text((50, 2), f'Loading:', font=robotoblack24, fill=0)
        
        # Draws red borders
        draw_other.rectangle((0, 0, epd.height, 5), fill=0)
        draw_other.rectangle((0, 30, epd.height, 35), fill=0)
        draw_other.rectangle((0, 30, 5, 0), fill=0)
        draw_other.rectangle((207, 30, 212, 0), fill=0)
        draw_other.rectangle((0, 99, 212, 104), fill=0)
        draw_other.rectangle((0, 31, 5, 104), fill=0)
        draw_other.rectangle((207, 0, 212, 104), fill=0)
        
        
        # If high tide recorded select it provides the height, date and time recorded. Along with start date the screen has been running from
        if selection == "high":
            highest_tide_datetime = datetime.strptime(highestTideDate, "%Y-%m-%d %H:%M:%S")
            daterecorded = highest_tide_datetime.strftime("%Y-%m-%d")
            timerecorded = highest_tide_datetime.strftime("%H:%M:%S")
            drawLoadBlack.text((8, 35), f'Highest Height: {float(highHeight):.2f} m', font=robotoblack18, fill=0)
            drawLoadBlack.text((8, 52), f'Recorded: {daterecorded}', font=robotoblack18, fill=0)
            drawLoadBlack.text((8, 67), f'At: {timerecorded[0:5]}', font=robotoblack18, fill=0)
            drawLoadBlack.text((8, 82), f'Recording Since {startDate}', font=robotoblack14, fill=0)
        
        # If low tide recorded select it provides the height, date and time recorded. Along with start date the screen has been running from
        else: 
            lowest_tide_datetime = datetime.strptime(lowestTideDate, "%Y-%m-%d %H:%M:%S")
            daterecorded = lowest_tide_datetime.strftime("%Y-%m-%d")
            timerecorded = lowest_tide_datetime.strftime("%H:%M:%S")
            drawLoadBlack.text((8, 35), f'Lowest Height: {float(lowHeight):.2f} m', font=robotoblack18, fill=0)
            drawLoadBlack.text((8, 52), f'Recorded: {daterecorded}', font=robotoblack18, fill=0)
            drawLoadBlack.text((8, 67), f'At: {timerecorded}', font=robotoblack18, fill=0)
            drawLoadBlack.text((8, 82), f'Recording Since {startDate}', font=robotoblack14, fill=0)
        
        # Updates the display
        epd.display(epd.getbuffer(LoadingBlackimage), epd.getbuffer(Other)) 
        epd.sleep()
        
        # Waits 60 seconds
        time.sleep(60)
        
        # Refreshes the display ready for current tide info
        einkUpdate.refresh_display(epd)
        
    def display_tide_info(event, height, eventTime, pastevent, pastheight, previousEventTime, progress):
        #212(H) x 104(V) pixel
        progressDraw = einkUpdate.progressBar(progress)
        logging.info("init and Clear")
        epd = epd2in13bc.EPD()
        einkUpdate.refresh_display(epd)
        
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)
        HRedimage = Image.new('1', (epd.height, epd.width), 255)
        robotoblack32 = ImageFont.truetype('pic/Roboto-Black.ttf', 32)
        robotoblack24 = ImageFont.truetype('pic/Roboto-Black.ttf', 24)
        robotoblack18 = ImageFont.truetype('pic/Roboto-Black.ttf', 18)
        robotoblack14 = ImageFont.truetype('pic/Roboto-Black.ttf', 14)
        drawblack = ImageDraw.Draw(HBlackimage)
        draw_other = ImageDraw.Draw(HRedimage)
        einkUpdate.loading_message(epd, robotoblack14, robotoblack18, robotoblack24, robotoblack32)
        
        #drawblack.text((2, 0), 'hello world', font = robotoblack32, fill = 0)
        #drawblack.text((2, 0), f'event: {event}', font = robotoblack18, fill = 0)
        #drawblack.text((2, 20), f'height: {height:.2f}', font = robotoblack18, fill = 0)
        #drawblack.text((2, 40), f'Time: {eventTime}', font = robotoblack18, fill = 0)
        
        
        drawblack.text((10, 20), 'Low', font = robotoblack14, fill=0)
        drawblack.text((167, 20), 'High', font=robotoblack14, fill=0)
        
        # Progress Bar
        draw_other.rectangle((30, 70, 30 + progressDraw , 40), fill=0)
        drawblack.rectangle((29, 39, 10, 71), fill=0)
        drawblack.rectangle((182, 39, 183, 71), fill=0)
        drawblack.rectangle((29, 70, 183, 71), fill=0)
        drawblack.rectangle((29, 39, 183, 40), fill=0)
        
        print("Tide info")
        
        #chevron_y = 45  # Y-coordinate for the chevron pattern
        #chevron_height = 20  # Height of the chevron pattern
        #chevron_width = 5  
        
        if event == 'LowWater':
            drawblack.text((40, 5), 'Tide Going Out', font=robotoblack18, fill=0)
            drawblack.text((10, 85), f'{height:.2f} m', font=robotoblack14, fill=0)
            drawblack.text((10, 70), f'{eventTime}', font=robotoblack14, fill = 0)
            draw_other.text((10, 15), 'Next', font=robotoblack14, fill=0)
            drawblack.text((167,85), f'{pastheight:.2f} m', font=robotoblack14, fill = 0)
            drawblack.text((167, 70), f'{previousEventTime}', font=robotoblack14, fill = 0)
            
        else:
            drawblack.text((40, 5), 'Tide Coming In', font=robotoblack18, fill=0)
            drawblack.text((10, 85), f'{pastheight:.2f} m', font=robotoblack14, fill=0)
            drawblack.text((10, 70), f'{previousEventTime}', font=robotoblack14, fill = 0)
            draw_other.text((167, 15), 'Next', font=robotoblack14, fill=0)
            drawblack.text((167, 85), f'{height:.2f} m', font=robotoblack14, fill=0)
            drawblack.text((167, 70), f'{eventTime}', font=robotoblack14, fill = 0)
            
            '''for i in range(0, progressDraw, chevron_width):
                draw_other.polygon([(212 - 10 - i, chevron_y),
                (212 - 60 - i - chevron_width // 2, chevron_y + chevron_height),
                (212 - 60 - i - chevron_width, chevron_y)],
                fill=0)
            '''
        
        print(f"{event}: {eventTime} with a height of {height}M")
        print(f"{progressDraw}")
        
        
        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
        
        
        epd.sleep()
        
        
        updateCompleted = "e-ink screen refresh has succesfully completed"
        logging.info(updateCompleted)
        
        return updateCompleted
    
    def progressBar(progress):
        logging.info(f"Getting progress bar length")
        progressBarLength = float(progress)
        #212 - 30 - 30 = 152
        progress_map = {
            (0, 3.33): 7,
            (3.33, 6.66): 12,
            (6.66, 9.99): 17,
            (9.99, 13.32): 22,
            (13.32, 16.65): 27,
            (16.65, 19.98): 32,
            (19.98, 23.31): 37,
            (23.31, 26.64): 42,
            (26.64, 29.97): 47,
            (29.97, 33.30): 52,
            (33.30, 36.63): 57,
            (36.63, 39.96): 62,
            (39.96, 43.29): 67,
            (43.29, 46.62): 72,
            (46.62, 49.95): 77,
            (49.95, 53.28): 82,
            (53.28, 56.61): 87,
            (56.61, 59.94): 92,
            (59.94, 63.27): 97,
            (63.27, 66.60): 102,
            (66.60, 69.93): 107,
            (69.93, 73.26): 112,
            (73.26, 76.59): 117,
            (76.59, 79.92): 122,
            (79.92, 83.25): 127,
            (83.25, 86.58): 132,
            (86.58, 89.91): 137,
            (89.91, 93.24): 142,
            (93.24, 96.57): 147,
            (96.57, 100): 152
        }
        for range_start, range_end in progress_map:
            if range_start <= progressBarLength < range_end:
                return progress_map[(range_start, range_end)]
        return 0
        

logging.basicConfig(filename='TideInfo.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    tide_display = einkUpdate()