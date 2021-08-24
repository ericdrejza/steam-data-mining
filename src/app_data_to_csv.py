#!/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/venv/bin/python3
# Eric Drejza
# Data Mining II

import os
import sys
import json
import pandas as pd
import numpy as np

""" 
Indices of the csv table will contain the following:
row = [0-11=genres, 12-350=tags]
"""
genre_id_index_offset = -1   # genre ids start at 1, so 1 + 1 = 2
tag_id_index_offset = 11    # tag ids start at 1, so 1 + 13 = 14


data_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data'
json_dir = data_dir + '/json'
out_dir = data_dir + '/csv'
outfile_csv_votes_df = 'app_genres_tags_votes_df.csv'

# gather name_id jsons
genres_name_id_json = json.load(open(json_dir + '/genres_name_id.json'))
tags_name_id_json = json.load(open(json_dir + '/tags_name_id.json'))

def column_sum(array, column_index):
    col_sum = 0
    for ri, row in enumerate(range(0, len(array))):
        e = array[ri][column_index]
        if isinstance(e, int):
            col_sum = col_sum + e
    return col_sum

def genre_sum_confirmation(counter_map, array, genre):
    return counter_map[genre] == column_sum(array, genres_name_id_json['name_key'][genre]+genre_id_index_offset)

def tag_sum_confirmation(counter_map, array, tag):
    return counter_map[tag] == column_sum(array, tags_name_id_json[tag]+tag_id_index_offset)

def main():

    print("out_dir: " + out_dir)
    os.system("mkdir -p {}".format(out_dir))
    os.chdir(out_dir)

    app_file = open(json_dir + "/aggregate_app_data.json")
    apps_json = json.load(app_file)
    app_file.close()

    genre_counter={}
    tag_vote_counter = {}

    for g in genres_name_id_json['name_key']:
        genre_counter[g] = 0
    for t in tags_name_id_json:
        tag_vote_counter[t] = 0

    csv_table = []
    csv_table.append([str(g) for g in genres_name_id_json['name_key'].keys()])
    csv_table[0].extend([str(t) for t in tags_name_id_json.keys()])

    keys = apps_json.keys()
    for k in keys:
        e = apps_json[k]

        row = [0]*351
        ### GENRES ###
        genre = str(e['genre'])
        if genre != '':
            # if len(genre.split(',')) > 1:
            for g in genre.split(','):
                g = g.strip()
                if g in genres_name_id_json['name_key'].keys():
                    col_idx = genres_name_id_json['name_key'][g] + genre_id_index_offset
                    row[col_idx] = 1
                    genre_counter[g] = genre_counter[g]+1

            csv_table.append(row)
            
            ### TAGS ###
            if not isinstance(e['tags'], list):
                tags_found = e['tags'].keys()
                for tk in tags_found:
                    if tk in tags_name_id_json.keys():
                        col_idx = tags_name_id_json[tk] + tag_id_index_offset
                        row[col_idx] = e['tags'][tk]  # add number of votes to cell
                        tag_vote_counter[tk] = tag_vote_counter[tk]+e['tags'][tk] # add number of votes to counter
    

    ### CHECKING ###
    print(genre_counter)
    print(tag_vote_counter)
    print("Incorrect Genre Sums:")
    for g in genres_name_id_json['name_key'].keys():
        if not genre_sum_confirmation(genre_counter, csv_table, g):
            print(g)
    
    print("Incorrect Tag Sums:")
    for t in tags_name_id_json.keys():
        if not tag_sum_confirmation(tag_vote_counter, csv_table, t):
            print(t)

    df = pd.DataFrame(csv_table)
    print(df.shape)
    df.to_csv(outfile_csv_votes_df, index=False)

if __name__ == "__main__":
    main()