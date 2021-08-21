#!/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/venv/bin/python3
# Eric Drejza
# Data Mining II

from ast import dump
import os
import sys
import json

from requests.api import request

def main():
    out_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data/insert_scripts'
    outfile_apps = 'insert_apps.sql'
    outfile_app_tag = 'insert_app_tag.sql'
    outfile_app_genre = 'insert_app_genre.sql'

    print("out_dir: " + out_dir)
    os.system("mkdir -p {}".format(out_dir))
    os.chdir(out_dir)
    
    data_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data'
    # gather name_id jsons
    tags_name_id_json = json.load(open(data_dir + '/tags_name_id.json'))
    genres_name_id_json = json.load(open(data_dir + '/genres_name_id.json'))

    app_tags = []
    app_genres = []

    app_string = 'INSERT INTO apps VALUES\n'
    app_tag_string = 'INSERT INTO app_tag VALUES\n'
    app_genre_string = 'INSERT INTO app_genre VALUES\n'

    app_file = open("/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data/full_app_data_merge/aggregate_app_data.json")
    apps_json = json.load(app_file)
    app_file.close()

    keys = apps_json.keys()
    for k in keys:
        e = apps_json[k]
        print(k)
        print(json.dumps(e, indent=4, sort_keys=True))

        appid = str(e['appid'])
        name = e['name']
        developer = e['developer']
        publisher = e['publisher']
        score_rank = e['score_rank']
        if score_rank == '':
            score_rank == "NULL"
        userscore = e['userscore']
        intitial_price = str((float(e['initial_price']) / 100).__round__(2))
        price = str((float(e['price']) / 100).__round__(2))
        discount = e['discount']
        owners = e['owners']
        positive = e['positive']
        negative = e['negative']
        playtime_2w_avg = e['average_2weeks']
        playtime_2w_median = e['median_2weeks']
        playtime_forever_avg = e['average_forever']
        playtime_forever_median = e['median_forever']
        concurrent_users = e['ccu']
        
        app_genres.append([appid, genres_name_id_json[e['genre']]])
        tags_found = e['tags'].keys()
        for tk in tags_found:
            app_tags.append([appid, tags_name_id_json[tk], e['tags'][tk]])
        break

        sys.exit()
        # type                              i    s    i   i   i    f   f  i   i
        app_string = app_string + '\t({}, "{}", {}, {}, {}, {}, {}, {}, {}),\n'\
          .format(_id_, tag, num_games, num_votes, tag_weight, price_median, userscore_median, owners, playtime)
    #     type     i     s       i          i          i           f              f              i        i
    
    app_string = app_string[:-2]+';'

    for at in app_tags:
        app_tag_string = app_tag_string + '\t({}, {}, {}),\n'.format(at[0], at[1], at[2])
    at = at[:-2]+';'

    for ag in app_genres:
        app_genre_string = app_genre_string + '\t({}, {}, {}),\n'.format(ag[0], ag[1])
    ag = ag[:-2]+';'

    print(app_string + '\n')
    print(app_tag_string + '\n')
    print(app_genre_string)
    with open(outfile_apps, 'w') as outfile:
        outfile.write(app_string)
    with open(outfile_app_tag, 'w') as outfile:
        outfile.write(app_tag_string)
    with open(outfile_app_genre, 'w') as outfile:
        outfile.write(app_genre_string)

if __name__ == "__main__":
    main()