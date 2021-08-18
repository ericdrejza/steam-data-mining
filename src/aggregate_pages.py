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

    parser.add_option("-i", "--page", "--page-number", action="store", type="int",
                        dest="page_num", default=0,
                        help="Page number to start requests from.  0 <= i <= 44")
    parser.add_option("-n", "-N", "--number-of-pages", action="store", type="int",
                        dest="num_pages", default = 50,
                        help="Number of pages to request. Runtime = ~60 * N")
    (options, args) = parser.parse_args()

    if len(args) > 0:
        dir_path = args[0]
        dir_path = os.path.abspath(dir_path)
        if not os.path.isdir(dir_path):
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
        basename = os.path.basename(str(f))
        if 'page_' in basename:
            files.append(basename)
        # else:
        #     files.append(basename)

    start = options.page_num
    end = min(start + options.num_pages, len(files) - start)
    files = files[start : end]
    print('Files:')
    for f in files:
        print(f)

    aggregate = None
    i = 0

    print("\nLoading and Aggregating:")
    for f in files:
        print(f)
        file = open(f)
        if aggregate is None:
            aggregate = json.load(file)
        else:
            data = json.load(file)
            aggregate = jsonmerge.merge(aggregate, data)
        file.close()
        # with open("aggregate_pages_iter_{}.json".format(i), "w") as outfile:
        #   json.dump(aggregate, outfile, indent=4, sort_keys=True)
        
        if i >= options.num_pages:
            break
        i = i + 1
    
    with open("aggregate_pages.json", "w") as outfile:
        json.dump(aggregate, outfile, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()