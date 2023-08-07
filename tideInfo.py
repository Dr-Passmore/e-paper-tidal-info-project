import apiInfo
import urllib.request, json
import logging

class tidalEvents:
    def __init__(self) -> None:
        
        pass
    
    def get_data():
        logging.info('Requesting json file from Admiralty API')
        apiKey = apiInfo.apiKey
        try:
            with urllib.request.urlopen(f"https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0005/TidalEvents?duration=2&key={apiKey}") as url:
                data = json.load(url)
                logging.info('Request completed')
                return data
        except:
            logging.error('Failed to get data from Admiralty API')
logging.basicConfig(filename='TideInfo.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

tidalEvents()