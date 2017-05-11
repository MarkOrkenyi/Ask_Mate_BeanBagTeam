import csv
import base64
import time
import datetime


def read_csv(filename, type_of_csv):
    '''Opens csv file(filename) and returns a list of lists with it's content
    \nUse: read_csv(<filename>,type_of_csv can be "question" or "answer"'''
    csv_content = []
    with open(filename, mode="r") as data:
        content = csv.reader(data, delimiter=',')
        for row in content:
            csv_content.append(row)
    csv_data = decode(csv_content, type_of_csv)
    return csv_data


def write_csv(csv_path, csv_data, type_of_csv):
    '''csv_data is the FULL list of lists of the csv file, type_of_csv can be "question" or "answer"'''
    csv_data = encode(csv_data, type_of_csv)
    with open(csv_path, mode="w") as data:
        datawriter = csv.writer(data, delimiter=',')
        for row in csv_data:
            datawriter.writerow(row)


def encode(csv_data, type_of_csv):
    for row in csv_data:
        row[1] = convert_time(row[1], "string")
        row[4] = bytes.decode(base64.b64encode(str.encode(row[4])))
        if type_of_csv == "question":
            row[5] = bytes.decode(base64.b64encode(str.encode(row[5])))
    return csv_data


def decode(csv_data, type_of_csv):
    for row in csv_data:
        row[1] = convert_time(row[1], "unix")
        row[4] = bytes.decode(base64.b64decode(row[4]))
        if type_of_csv == "question":
            row[5] = bytes.decode(base64.b64decode(row[5]))
    return csv_data


def convert_time(input_, type_):
    if type_ == "string":
        dt_time_e = datetime.datetime.strptime(str(input_), ("%Y-%m-%d %H:%M:%S"))
        tuple_ = dt_time_e.timetuple()
        return time.mktime(tuple_)
    elif type_ == "unix":
        dt_time = datetime.datetime.fromtimestamp(float(input_))
        return datetime.datetime.strftime(dt_time, ("%Y-%m-%d %H:%M:%S"))


def get_new_id(filename, type_of_csv):
    id_ = ['0']
    data = read_csv(filename, type_of_csv)
    for row in data:
        id_.append(row[0])
    max_id = max(map(int, id_))
    return (int(max_id) + 1)


def remove(file_data, id_, num):
    to_pop = []
    for index, elements in enumerate(file_data):
        if elements[num] == id_:
            to_pop.append(index)
    for i in reversed(list(map(int, to_pop))):
        file_data.pop(i)
    return file_data
