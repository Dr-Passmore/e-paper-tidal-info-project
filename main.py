import tideInfo
import logging
import datetime
import time

class TideInformationDisplay:
    def __init__(self):
        logging.info('Initialising Data Retrieval and e-ink update')
        data = tideInfo.tidalEvents.get_data()
        TideInformationDisplay.data_processing(self, data)

    def data_processing(self, data):
        for x in data:
                event = (x['EventType'])
                height = (x['Height'])
                eventTime = (x['DateTime'])
                eventTime = eventTime[:19]
                
                when = datetime.datetime.strptime(eventTime,"%Y-%m-%dT%H:%M:%S")
                timestamp = datetime.datetime.timestamp(when)
                now = time.time()
                eventTime = eventTime[11:16]
                if timestamp > now:
                    break
                else: 
                    pastevent = event
                    pastheight = height
                    previousEventTime = eventTime
                    prioreventTime = timestamp
            
        timeRemaining = (timestamp - now) / 60
        timeSince = (now - prioreventTime) / 60
        total = timeRemaining + timeSince
        percentage = 100 / total
        progress = percentage * timeSince
        
        if event == "LowWater":
            progress = 100 - progress
            
        print(f"The next tide event is {event} at a Height of {height} meters on {eventTime}")

logging.basicConfig(filename='TideInfo.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    tide_display = TideInformationDisplay()