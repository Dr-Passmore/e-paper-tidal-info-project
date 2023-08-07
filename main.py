import tideInfo
import logging

class TideInformationDisplay:
    def __init__(self):
        logging.info('Initialising Data Retrieval and e-ink update')
        data = tideInfo.tidalEvents.get_data()
        print(data)
        pass


logging.basicConfig(filename='TideInfo.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    tide_display = TideInformationDisplay()