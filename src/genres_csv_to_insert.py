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
    out_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data/insert_scripts'
    outfile = 'insert_genres.sql'
    print("out_dir: " + out_dir)
    os.system("mkdir -p {}".format(out_dir))
    os.chdir(out_dir)
    
    # gather tag info
    tags = []
    with open("/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data/genres.csv", \
        newline='') as tagfile:
        reader = csv.DictReader(tagfile)

        script_string = 'INSERT INTO genres VALUES\n'

        for row in reader:
            # print(row)
            genre = row['genre']
            num_games = row['num_games']
            userscore_avg = (float(row['userscore_avg'][:-1]) / 100).__round__(4)
            metascore_avg = (float(row['metascore_avg'][:-1]) / 100).__round__(4)
            playtime_avg = playtime = str(int(row['playtime_avg'].split(':')[0]) * 60 + int(row['playtime_avg'].split(':')[1]))
            total_copies_owned = row['total_copies_owned']
            price_avg = float(row['price_avg']) / 100

            # parameters = [genre, num_games, userscore_avg, metascore_avg, playtime_avg, total_copies_owned, price_avg]

            
            #                                    s    i   f   f   i   i    i
            script_string = script_string + '\t(DEFAULT, "{}", {}, {}, {}, {}, {}, {}),\n'\
              .format(genre, num_games, userscore_avg, metascore_avg, playtime_avg, total_copies_owned, price_avg).replace('-0.01', 'NULL')
    #                  s       i          f               f           i              i                       f

    script_string = script_string[:-2]
    print(script_string)
    outfile = open(outfile, 'w')
    outfile.write(script_string)
    outfile.close()

if __name__ == "__main__":
    main()