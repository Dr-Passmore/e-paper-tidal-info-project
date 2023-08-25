import einkDisplayUpdate
import urllib.request
import json
import logging
import configparser

class tidalEvents:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_data():
        """
        Retrieves tidal event data from the Admiralty API.

        Output:
        - data: JSON data containing tidal event information.
        """
        logging.info('Requesting json file from Admiralty API')
        
        # Read the API key from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')
        apiKey = config.get('API Key', 'Key')
        try:
            try:
                with urllib.request.urlopen(f"https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0005/TidalEvents?duration=2&key={apiKey}") as url:
                    data = json.load(url)
                    logging.info('Request completed')
                    return data
            except Exception as e:
                logging.error('Failed to get data from Admiralty API')
                logging.error(f'{e}')
                einkDisplayUpdate.einkUpdate.error_display(e)
        except Exception as e:
                logging.error('Failed to get data from Admiralty API')
                logging.error(f'{e}')
                einkDisplayUpdate.einkUpdate.error_display(e)
                
logging.basicConfig(filename='TideInfo.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

tidalEvents()