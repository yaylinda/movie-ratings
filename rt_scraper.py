"""
Fetch data from Rotten Tomatoes API for all movie ratings and export as CSV.
"""

import csv
import json
import os
import requests
import math


ROTTON_TOMATO_URL = "https://www.rottentomatoes.com/api/private/v2.0/browse?type=dvd-streaming-all"
DATA_FILE_NAME = "data.csv"


def fetch(url):
    r = requests.get(url)
    return r.json()


def write_page(page_num, data):
    print("\tWriting page: %d, with %d rows\n" % (page_num, len(data)))

    if (page_num == 1):
        with open(DATA_FILE_NAME, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))                            
            writer.writeheader()

    with open(DATA_FILE_NAME, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))                            
        for row in data:
            writer.writerow(row)


def parse_page(page_num):
    print("\tParsing page: %d" % page_num)

    url = ROTTON_TOMATO_URL + "&page=" + str(page_num)
    raw_data = fetch(url)['results']
    
    data = []

    for raw_datum in raw_data:
        if 'theaterReleaseDate' not in raw_datum:
            continue

        datum = {}
        datum['title'] = raw_datum['title']
        datum['freshness'] = raw_datum['tomatoIcon'] == 'fresh'
        datum['tomatoScore'] = raw_datum['tomatoScore']

        datum['year'] = int(raw_datum['url'][-4:]) # TODO - some urls do not end with year of movie. Year of movie is not available from list
        datum['month'] = raw_datum['theaterReleaseDate'][0:3]

        print(datum)
        data.append(datum)

    
    
    write_page()


def main():
    data = fetch(ROTTON_TOMATO_URL)

    counts = data['counts']
    num_pages = math.ceil((counts['total'] * 1.0) / counts['count'])
    print("Total pages: %d" % num_pages)

    for i in range(1, 1 + 1):
        parse_page(i)
        
    
if __name__ == '__main__':
    main()

