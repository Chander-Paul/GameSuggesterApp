from mobyapi import get_data
import helper
import csv
import os

def get_group_offset(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        last_row = None
        for row in reader:
            last_row = row
        if last_row:
            return last_row[2]  
        return None

file_path = "data\groups.csv"
endpoint = 'groups'
params = {"offset": get_group_offset(file_path)}
data = get_data(endpoint, params)

helper.save_json_to_csv(data[endpoint], file_path)


