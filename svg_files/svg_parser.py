'''Script creates a json file containing data of svg files in 2 dirs
in the following form: key: filename, value: '1x1': 1x1 svg , '4x3': 4x3 svg
'''
import os
from itertools import zip_longest
import json


dir1 = "1x1"
dir2 = "4x3"
final = 'final.json'

dir1_files = os.listdir(dir1)
dir2_files = os.listdir(dir2)

with open(final, 'w',) as output:
    
    data = {}
    for filename_1, filename_2 in zip_longest(dir1_files, dir2_files):
        with (open(os.path.join(dir1, filename_1), 'r') as file1, \
            open(os.path.join(dir2, filename_2), 'r') as file2):
            content1 = file1.read()
            content2 = file2.read()
            data[filename_1] = {'1x1': content1, '4x3': content2}
    json.dump(data, output)
