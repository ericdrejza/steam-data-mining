#!/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/venv/bin/python3
# Eric Drejza
# Data Mining II

import os
import sys
from pathlib import Path
import json
import jsonmerge
from datetime import datetime
from optparse import OptionParser


def main():
    parser = OptionParser()
    (options, args) = parser.parse_args()

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file_dt_string = now.strftime("%Y%m%d%H%M%S")

    if len(args) > 0:
        dir_path = args[0]
        dir_path = os.path.abspath(dir_path)
        if not os.path.isdir():
            sys.exit("Error: directory path argument is not a directory")
    else:
        data_dir = '/home/ericdrejza/Rowan/Data_Mining/steam-data-mining/data'
        for root, dirs, files in os.walk(data_dir):

            if len(dirs) == 0:
                sys.exit("Error: No directories to choose from")
            print("root: " + root)
            print("dirs: " + str(dirs))
            dirs.sort(reverse=True)
            dir_path = data_dir+'/'+dirs[0]
            break

    print(os.getcwd())
    print('cd {}'.format(dir_path))
    os.chdir(dir_path)
    print(os.getcwd())

    file_paths = sorted(Path(dir_path).iterdir(), key=os.path.getmtime)
    files = []
    for f in file_paths:
        files.append(os.path.basename(str(f)))

    print('Files:')
    for f in files:
        print(f)

    aggregate = None

    print("\nLoading and Aggregating:")
    for f in files:
        print(f)
        f = open(f)
        if aggregate is None:
            aggregate = json.load(f)
        else:
            data = json.load(f)
            aggregrate = jsonmerge.merge(aggregate, data)
        
        f.close()

    with open(data_dir+'/'+"aggregate_pages.json", "w") as outfile:
        json.dump(aggregate, outfile, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()