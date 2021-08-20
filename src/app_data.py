#!/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/venv/bin/python3
# Eric Drejza
# Data Mining II

import os
import sys
import time
from datetime import datetime
import requests
import json
import jsonmerge
from optparse import OptionParser
# import mysql.connector
# from mysql.connector import errorcode

def main():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file_dt_string = now.strftime("%Y%m%d-%H%M")
    print(dt_string)

    parser = OptionParser()
    
    parser.add_option("-a", "--file", action="store", type="string",
                        dest="argument_file", default=None,
                        help="file path to app ids")
    parser.add_option("-g", "--aggregate-file", action="store", type="string",
                        dest="agg_file_path", default=None,
                        help="Path to json file that will serve a base to merge into")
    parser.add_option("-i", "--index", action="store", type="int",
                        dest="id_start_index", default=0,
                        help="app id to start requests from")
    parser.add_option("-n", "-N", "--number-of-apps", action="store",
                        dest="num_apps", default = float('inf'),
                        help="Number of pages to request. Runtime = ~60 * N")
    parser.add_option("-t", "--sleep-time", action="store", type="int",
                        dest="sleep_time", default=1,
                        help="How long the program sleeps between api calls")
    parser.add_option("-o", "--out-path", action="store", type="string", dest="out_path",
                        default="full_app_data.{}.json".format(file_dt_string),
                        help="Path to outfile.")

    (options, args) = parser.parse_args()

    ### MYSQL SETUP ###
    # steam DB
    # try:
    #     connect = mysql.connector.connect(host='localhost',
    #                                       user='tester',
    #                                       passwd='tester1',
    #                                       database='steam')
    # except mysql.connector.Error as err:
    #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #       print("Something is wrong with the username or password")
    #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #       print("Database does not exist")
    #     else:
    #       print(err)

    # cursor = connect.cursor(buffered=True)

    if options.out_path is None or not os.path.isdir(options.out_path):
        data_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data'
        out_dir = data_dir+ '/' + file_dt_string
        outfile = 'app_data_full.json'
    else:
        out_dir = os.path.dirname(options.out_path)
        outfile = os.path.basename(options.out_path)
    os.system("mkdir -p {}".format(out_dir))
    print("outpath: " + os.path.abspath(out_dir) + '/' + outfile)
    os.chdir(out_dir)

    base_url = "https://steamspy.com/api.php?request=appdetails&appid={}"
    
    response = '-1'
    index = options.id_start_index
    app_count = 0

    app_ids = []
    if len(args) > 0:
        app_ids = args
    if options.argument_file is not None:
        with open(os.path.abspath(options.argument_file)) as arg_file:
            lines = arg_file.readlines()
            stripped_lines = [str(l).strip() for l in lines]
            app_ids.extend(stripped_lines)
    
    if options.agg_file_path is not None:
        aggregate = json.load(open(options.agg_file_path))
    else:
        aggregate = {}

    while response is not None and response != "" and app_count < options.num_apps and index < len(app_ids):
        app_id = app_ids[index]
        print(base_url.format(str(app_id)))
        response = requests.get(base_url.format(str(app_id)))
        if response is None or response == 0:
            break
        data = response.json()
        aggregate[str(data["appid"])] = data
        # aggregate = jsonmerge.merge(aggregate, data)


        # Sleep to respect site api call frequency
        time.sleep(options.sleep_time)

        index = index + 1
        app_count = app_count + 1
        print(app_count)
    
    # print(json.dumps(aggregate, indent=4, sort_keys=True))

    with open(outfile, "w") as outfile_file:
        json.dump(aggregate, outfile_file, indent=4, sort_keys=True)
        print(outfile + '\n')
    print('Response: "' + str(response) + '"')

if __name__ == "__main__":
    main()