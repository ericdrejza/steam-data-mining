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

def main():
    parser = OptionParser()
    
    parser.add_option("-i", "--page", "--page-number", action="store", type="int",
                        dest="page_num", default=0,
                        help="Page number to start requests from.  0 <= i <= 44")
    parser.add_option("-n", "-N", "--number-of-pages", action="store", type="int",
                        dest="num_pages", default = 100000,
                        help="Number of pages to request. Runtime = ~60 * N")
    parser.add_option("-t", "--sleep-time", action="store", type="int",
                        dest="sleep_time", default=75,
                        help="How long the program sleeps between api calls")
    parser.add_option("-C", "--out_dir", action="store", type="string", dest="out_dir",
                        help="Path to directory to store outfiles.")

    (options, args) = parser.parse_args()

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dir_dt_string = now.strftime("%Y%m%d-%H%M")
    print(dt_string)

    if options.out_dir is None or not os.path.isdir(options.out_dir):
        data_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data'
        out_dir = data_dir+ '/' + dir_dt_string
    else:
        out_dir = options.out_dir
    print("out_dir: " + out_dir)
    os.system("mkdir -p {}".format(out_dir))
    os.chdir(out_dir)

    base_url = "https://steamspy.com/api.php?request=all&page={}"
    rq_part_1 = "all"
    rq_part_2 = "&page="
    
    response = '-1'
    page_num = options.page_num
    page_count = 0

    while response is not None and response != "" and page_count < options.num_pages:
        print(base_url.format(str(page_num)))
        response = requests.get(base_url.format(str(page_num)))
        if response is None or response == 0:
            break
        data = response.json()

        data_out = "page_{}.json".format(page_num)
        with open(data_out, "w") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
            print(data_out+'\n')

        # Sleep to respect site api call frequency
        time.sleep(options.sleep_time)

        page_num = page_num + 1
        page_count = page_count + 1

    print('Response: "' + response + '"')

if __name__ == "__main__":
    main()