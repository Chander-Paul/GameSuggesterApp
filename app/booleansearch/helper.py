import json
import csv


def load_json(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        data = json.load(file)
    return data

def save_json_to_csv(data, file_path):
    with open(file_path, 'a+', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        
        csv_file.seek(0)
        if csv_file.read(1) == '':
            header = data[0].keys()
            writer.writerow(header)
        for row in data:
            writer.writerow(row.values())

def load_csv(file_path):
    with open(file_path, 'r', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
    return data

def load_text(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        data = file.readlines()
    return [row.strip() for row in data]
