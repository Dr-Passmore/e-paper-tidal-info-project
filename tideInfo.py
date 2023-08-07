import apiInfo
import urllib.request, json, datetime, time

class tidalEvents:
    def __init__(self) -> None:
        pass
    
    def get_data():
        apiKey = apiInfo.apiKey
        with urllib.request.urlopen(f"https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0005/TidalEvents?duration=2&key={apiKey}") as url:
            data = json.load(url)
            return data
            
data = tidalEvents.get_data()
print(data)