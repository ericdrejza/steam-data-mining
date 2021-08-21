#!/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/venv/bin/python3
# Eric Drejza
# Data Mining II

from ast import dump
import os
import sys
import csv

from requests.api import request

def main():
    out_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data/insert_scripts'
    outfile = 'insert_tags.sql'
    print("out_dir: " + out_dir)
    os.system("mkdir -p {}".format(out_dir))
    os.chdir(out_dir)
    
    # gather tag info
    tags = []
    with open("/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data/tags.csv", \
        newline='') as tagfile:
        reader = csv.DictReader(tagfile)

        script_string = 'INSERT INTO tags VALUES\n'

        for row in reader:
            # print(row)
            _id_ = row['id']
            tag = row['tag']
            num_games = row['num_games']
            num_votes = row['num_votes']
            tag_weight = row['tag_weight']
            price_median = float(row['price_median']) / 100
            userscore_median = float(row['userscore_median'][:-1]) / 100
            owners = row['owners_median']
            playtime = str(int(row['playtime_median'].split(':')[0]) * 60 + int(row['playtime_median'].split(':')[1]))
            
            # type                              i    s    i   i   i    f   f  i   i
            script_string = script_string + '\t({}, "{}", {}, {}, {}, {}, {}, {}, {}),\n'\
              .format(_id_, tag, num_games, num_votes, tag_weight, price_median, userscore_median, owners, playtime)
    #         type     i     s       i          i          i           f              f              i        i

    script_string = script_string[:-2]
    print(script_string)
    outfile = open(outfile, 'w')
    outfile.write(script_string)
    outfile.close()

if __name__ == "__main__":
    main()