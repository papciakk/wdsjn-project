import csv


def load(filename):
    csv_data = {}
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_data[row[1]] = row[0]
    return csv_data

