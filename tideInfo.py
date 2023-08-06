import secrets
import urllib.request, json, datetime, time

class tidalEvents:
    def __init__(self) -> None:
        pass
    
    def get_data(self):
        apiKey = secrets.apiKey
        with urllib.request.urlopen(f"https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0005/TidalEvents?duration=2&key={apiKey}") as url:
            data = json.load(url)