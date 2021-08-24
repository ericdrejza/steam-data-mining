#!/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/venv/bin/python3
# Eric Drejza
# Data Mining II

from ast import dump
import os
import sys
import json

from requests.api import request

def null_maker(input):
    if input is None or input == '' or str(input).lower == 'null':
        return 'NULL'
    else:
        return input

def main():
    data_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data'
    out_dir = data_dir + '/insert_scripts'
    outfile_apps = 'insert_apps.sql'
    outfile_app_tag = 'insert_app_tag.sql'
    outfile_app_genre = 'insert_app_genre.sql'

    print("out_dir: " + out_dir)
    os.system("mkdir -p {}".format(out_dir))
    os.chdir(out_dir)
    
    # gather name_id jsons
    json_dir = data_dir + '/json'
    tags_name_id_json = json.load(open(json_dir + '/tags_name_id.json'))
    genres_name_id_json = json.load(open(json_dir + '/genres_name_id.json'))

    app_tags = []
    app_genres = []

    app_string = 'INSERT INTO apps VALUES\n'
    app_tag_string = 'INSERT INTO app_tag VALUES\n'
    app_genre_string = 'INSERT INTO app_genre VALUES\n'

    app_file = open(data_dir + '/json/aggregate_app_data.json')
    apps_json = json.load(app_file)
    app_file.close()

    missing_genre_list = []

    keys = apps_json.keys()
    for k in keys:
        try:
            e = apps_json[k]
            # print(k)
            # print(json.dumps(e, indent=4, sort_keys=True))

            appid = str(e['appid'])
            name = null_maker(e['name'])
            developer = null_maker(e['developer'])
            publisher = null_maker(e['publisher'])

            intitial_price = null_maker(e['initialprice'])
            if intitial_price != "NULL":
                intitial_price = str((float(intitial_price) / 100).__round__(2))
            
            price = null_maker(e['price'])
            if price != "NULL":
                price = str((float(price) / 100).__round__(2))
            
            discount = null_maker(e['discount'])
            if discount != "NULL":
                discount = str((float(discount) / 100).__round__(2))
            
            owners_lower = str(e['owners']).split('..', maxsplit=1)[0].replace(',','').strip()
            owners_upper = str(e['owners']).split('..', maxsplit=1)[1].replace(',','').strip()
            positive = e['positive']
            negative = e['negative']
            playtime_2w_avg = e['average_2weeks']
            playtime_2w_median = e['median_2weeks']
            playtime_forever_avg = e['average_forever']
            playtime_forever_median = e['median_forever']
            concurrent_users = e['ccu']
    
        except TypeError as ex:
            print(json.dumps(e, indent=4, sort_keys=True))
            print(ex.with_traceback)

        ### GENRE ###
        genre = str(e['genre'])
        if genre != '':
            # if len(genre.split(',')) > 1:
            for g in genre.split(','):
                g = g.strip()
                if g in genres_name_id_json['name_key'].keys():
                    app_genres.append([appid, genres_name_id_json['name_key'][g]])
        
        ### TAGS ###
        if not isinstance(e['tags'], list):
            tags_found = e['tags'].keys()
            for tk in tags_found:
                if tk in tags_name_id_json.keys():
                    app_tags.append([appid, tags_name_id_json[tk], e['tags'][tk]])
        
        # #                  1    2     3     4    5    6   7   8  9   10  11  12  13  14  15  16
        # type               i    s     s     s    f    f   f  i   i   i    i  i   i   i   i   i
        ind_app_string = '({}, "{}", "{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'\
          .format(appid, name, developer, publisher, intitial_price, price, discount, owners_lower, owners_upper, positive, negative, playtime_2w_avg, playtime_2w_median, playtime_forever_avg, playtime_forever_median, concurrent_users)
        #     type     i    s           s         s           f            f        f           i             i          i         i           i                 i                   i                    i                     i
        # #         1     2      3            4              5         6       7           8              9          10         11            12                13                  14                   15                     16
        ind_app_string = ind_app_string.replace('"NULL"', 'NULL')
        app_string = app_string + '\t' + ind_app_string + ',\n'
    
    app_string = app_string[:-2]+';'

    for at in app_tags:
        app_tag_string = app_tag_string + '\t({}, {}, {}),\n'.format(at[0], at[1], at[2])
    app_tag_string = app_tag_string[:-2]+';'

    for ag in app_genres:
        app_genre_string = app_genre_string + '\t({}, {}),\n'.format(ag[0], ag[1])
    app_genre_string = app_genre_string[:-2]+';'

    # print(app_string + '\n')
    # print(app_tag_string + '\n')
    # print(app_genre_string)
    
    with open(outfile_apps, 'w') as outfile:
        outfile.write(app_string)
    with open(outfile_app_tag, 'w') as outfile:
        outfile.write(app_tag_string)
    with open(outfile_app_genre, 'w') as outfile:
        outfile.write(app_genre_string)

if __name__ == "__main__":
    main()