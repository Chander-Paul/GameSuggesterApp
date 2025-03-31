from mobyapi import get_data
import helper
import csv
import os
from time import sleep

def get_group_offset(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        last_row = None
        for row in reader:
            last_row = row
        if last_row:
            return str(int(last_row[1])+1 )
        return None

file_path = "data\groups.csv"
endpoint = 'groups'

offset = 0
for x in range(140):  
    
    params = {"offset":offset}
    data = get_data(endpoint, params)
    if data is None:
        break
    helper.save_json_to_csv(data[endpoint], file_path)
    offset=offset+100
    sleep(5)



