import json
from pprint import pprint

with open('getIndianPolNames.json') as f:
    data_names = json.load(f)
    for item in data_names:
        print(item['names'])