import csv
import base64
import time
import datetime


def read_csv(filepath, type_of_csv):
    ''''Opens csv file and returns a list of lists with it's content
    \nUse: read_csv(<filepath>,type_of_csv can be "question" or "answer"'''
    csv_content = []
    with open(filepath, mode="r") as data:
        content = csv.reader(data, delimiter=',')
        for row in content:
            csv_content.append(row)
    csv_data = decode(csv_content, type_of_csv)
    return csv_data


def write_csv(csv_path, csv_data, type_of_csv):
    '''Encodes the csv_data with encode(), then writes it out to the given csv_path.
    \nUse:<csv_path>,<csv_data> is the FULL list of lists of the csv file, <type_of_csv> can be "question" or "answer"'''
    csv_data = encode(csv_data, type_of_csv)
    with open(csv_path, mode="w") as data:
        datawriter = csv.writer(data, delimiter=',')
        for row in csv_data:
            datawriter.writerow(row)


def encode(csv_data, type_of_csv):
    '''Encodes the csv_data'''
    for row in csv_data:
        row[1] = convert_time(row[1], "encode")
        row[4] = bytes.decode(base64.b64encode(str.encode(row[4])))
        if type_of_csv == "question":
            row[5] = bytes.decode(base64.b64encode(str.encode(row[5])))
    return csv_data


def decode(csv_data, type_of_csv):
    '''Decodes the csv_data'''
    for row in csv_data:
        row[1] = convert_time(row[1], "decode")
        row[4] = bytes.decode(base64.b64decode(row[4]))
        if type_of_csv == "question":
            row[5] = bytes.decode(base64.b64decode(row[5]))
    return csv_data


def convert_time(input_, type_):
    '''Converts time from UNIX to readable format, or vice-versa'''
    if type_ == "encode":
        datetime_obj = datetime.datetime.strptime(str(input_), ("%Y-%m-%d %H:%M:%S"))
        tuple_ = datetime_obj.timetuple()
        return time.mktime(tuple_)
    elif type_ == "decode":
        datetime_obj = datetime.datetime.fromtimestamp(float(input_))
        return datetime.datetime.strftime(datetime_obj, ("%Y-%m-%d %H:%M:%S"))


def get_new_id(filepath, type_of_csv):
    '''Returns a new ID for the entry. If no entry is present, the first ID will be 1'''
    id_ = ['0']
    data = read_csv(filepath, type_of_csv)
    for row in data:
        id_.append(row[0])
    max_id = max(map(int, id_))
    return (int(max_id) + 1)


def remove(file_data, id_, index_):
    '''Removes the matching row from the csv_data, and returns csv_data'''
    to_pop = []
    for index, elements in enumerate(file_data):
        if elements[index_] == id_:
            to_pop.append(index)
    for i in reversed(list(map(int, to_pop))):
        file_data.pop(i)
    return file_data
