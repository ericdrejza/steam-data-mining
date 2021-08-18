#!/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/venv/bin/python3
# Eric Drejza
# Data Mining II

from ast import dump
import os
import sys
import time
from datetime import datetime
import requests
import json
import jsonmerge
from optparse import OptionParser
import csv

from requests.api import request

def main():
    parser = OptionParser()

    parser.add_option("-t", "--sleep-time", action="store", type="int",
                        dest="sleep_time", default=75,
                        help="How long the program sleeps between api calls")
    parser.add_option("-C", "--out_dir", action="store", type="string", dest="out_dir",
                        help="Path to directory to store outfiles.")

    (options, args) = parser.parse_args()

    # gather tag names
    tags = []
    with open("/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data/tags.csv", \
        newline='') as tagfile:
        reader = csv.DictReader(tagfile)

        for row in reader:
            tag = row['Tag']
            print(tag)
            tags.append(tag)

    # set up out directory
    if options.out_dir is None or not os.path.isdir(options.out_dir):
        data_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data'
        for root, dirs, files in os.walk(data_dir):

            if len(dirs) == 0:
                sys.exit("Error: No directories to choose from")
            print("root: " + root)
            print("dirs: " + str(dirs))
            dirs.sort(reverse=True)
            dir_path = data_dir+'/'+dirs[0]
            break
    else:
        out_dir = options.out_dir
    print("out_dir: " + out_dir)
    os.system("mkdir -p {}".format(out_dir))
    os.chdir(out_dir)

    base_url = "https://steamspy.com/api.php?request=tag&tag={}"
    
    aggregate = None
    response = '-1'

    for tag in tags:
        request_string = base_url.format(str(tag))
        print(request_string)
        response = requests.get(request_string)
        if response is None or response == "":
            break
        data = response.json()
        if aggregate is None:
            aggregate = data
        else:
            aggregate = jsonmerge.merge(aggregate, data)

        # Sleep to respect site api call frequency
        time.sleep(options.sleep_time)

    data_out = "tags.json"
    with open(data_out, "w") as outfile:
        json.dump(aggregate, outfile, indent=4, sort_keys=True)
        print(data_out+'\n')

    print('Response: "' + response + '"')

if __name__ == "__main__":
    main()