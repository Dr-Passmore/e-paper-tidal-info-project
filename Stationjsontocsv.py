import json
import csv

with open('station.json') as json_file:
    data = json.load(json_file)

features = data['features']

csv_filename = 'station.csv'
csv_columns = ['Id', 'Name', 'Country', 'ContinuousHeightsAvailable', 'Footnote']

with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    
    csv_writer.writeheader()
    
    for feature in features:
        properties = feature['properties']
        csv_writer.writerow(properties)
        
print(f'Conversion completed. CSV file saved as {csv_filename}')