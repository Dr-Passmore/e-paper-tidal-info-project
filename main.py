import tideInfo
import einkDisplayUpdate
import logging
import datetime
import time
import configparser
import os

class TideInformationDisplay:
    def __init__(self):
        logging.info('Initialising Data Retrieval and e-ink update')
        config = configparser.ConfigParser()
        configFile = os.path.exists('config.ini')
        if configFile == False:
            #if the file does not exist then create one
            logging.error("No config file found")
            TideInformationDisplay.configurationFileCreation(self, config)
        else:
            pass
        data = tideInfo.tidalEvents.get_data()
        
        screenupdate = TideInformationDisplay.data_processing(self, config, data)
        print(screenupdate)
    def data_processing(self, config, data):
        """
        Process tidal event data, update records, and send processed data to the e-ink display script.

        Input:
        - config: ConfigParser instance for handling configuration.
        - data: List of dictionaries containing tidal event information.

        Output:
        - screen_update: Result of updating the e-ink display message 
        """
        
        config.read('config.ini')
        
        if data == None:
            logging.error('Display failed to update')
            
        else:
            ''' 
            Data contains multiple events which are ordered oldest to the next tide event.
            The old varibles overwrite data held in the past varibles 'pastevent' etc
            This leaves only the previous tide event and the next tide event. 
            ''' 
            for x in data:
                    event = (x['EventType'])
                    height = (x['Height'])
                    eventTime = (x['DateTime'])
                    eventTime = eventTime[:19]
                    
                    when = datetime.datetime.strptime(eventTime,"%Y-%m-%dT%H:%M:%S")
                    recordsdate = when
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
            
            if event == 'HighWater':
                currentRecord = config.get('Records', 'Highest Tide Height')
                
                if float(currentRecord) < height:
                    logging.info(f"New {event} record set of a height of {height}M")
                    config.set('Records', 'Highest Tide Height', str(height))
                    config.set('Records', 'Highest Tide Date', str(recordsdate))
                    with open(r"config.ini", 'w') as configuration:
                        config.write(configuration)
            else:
                currentRecord = config.get('Records', 'Lowest Tide Height')
                
                if float(currentRecord) > height:
                    logging.info(f"New {event} record set of a height of {height}M")
                    config.set('Records', 'Lowest Tide Height', str(height))
                    config.set('Records', 'Lowest Tide Date', str(recordsdate))
                    with open(r"config.ini", 'w') as configuration:
                        config.write(configuration)
            
            progress = TideInformationDisplay.percentage_calculation(self, timestamp, prioreventTime, now, event)
                
            print(f"The next tide event is {event} at a Height of {height} meters on {eventTime}")
            print(f"The last tide event was {pastevent} at a Height of {pastheight} meters on {previousEventTime}")
            print(f"{progress}%")
            
            screenupdate = einkDisplayUpdate.einkUpdate.display_tide_info(event, height, eventTime, pastevent, pastheight, previousEventTime, progress)

            return screenupdate
        
    def percentage_calculation(self, timestamp, prioreventTime, now, event):
        """
        Calculates the progress percentage between previous and next tide events.

        Input:
        - timestamp: Timestamp of the next tide event.
        - prioreventTime: Timestamp of the previous tide event.
        - now: Current timestamp.
        - event: Type of tide event (e.g., "HighWater" or "LowWater").

        Output:
        - progress: Progress percentage between previous and next tide events.
        """
        timeRemaining = (timestamp - now) / 60
        timeSince = (now - prioreventTime) / 60
        total = timeRemaining + timeSince
        percentage = 100 / total
        progress = percentage * timeSince
        
        if event == "LowWater":
            progress = 100 - progress
        
        return progress
    
    def configurationFileCreation(self, config):
        """
        Creates a configuration file 'config.ini' if it doesn't exist.

        Input:
        - config: ConfigParser instance for handling configuration.

        Output:
        - None (Creates or updates the 'config.ini' file.)
        """
        logging.info("Creating 'config.ini' file")
        try:
            tide_api = input("Please enter your API key:\n")
            config.add_section('API Key')
            config.set('API Key', 'Key', tide_api)
            config.add_section('Records')
            config.set('Records', 'Highest Tide Date', str(datetime.date.today()))
            config.set('Records', 'Highest Tide Height', str(0.00))
            config.set('Records', 'Lowest Tide Date', str(datetime.date.today()))
            config.set('Records', 'Lowest Tide Height', str(10.00))
            config.set('Records', 'Start Date', str(datetime.date.today()))
            with open(r"config.ini", 'w') as configuration:
                config.write(configuration)
            logging.info('config.ini created successfully')
        except Exception as e:
            logging.error(f"Failed to create config.ini: {e}")
            
        
logging.basicConfig(filename='TideInfo.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    tide_display = TideInformationDisplay()