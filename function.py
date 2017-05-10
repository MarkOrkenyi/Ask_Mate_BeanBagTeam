import csv
import base64
import datetime


def read_csv(filename, question):
    '''Opens csv file(filename) and returns a list of lists with it's content
    \nUse: read_csv(<filename>,<True:question, False:answer>"'''
    csv_content = []
    with open(filename) as data:
        content = csv.reader(data, delimiter=',')
        for row in content:
            row[1] = datetime.datetime.utcfromtimestamp(float(row[1]))
            row[4] = bytes.decode(base64.b64decode(row[4]))
            if question:
                row[5] = bytes.decode(base64.b64decode(row[5]))
            csv_content.append(row)
    return csv_content


def write_csv(filename, to_add, question):
    '''Writes out the list of lists to a csv file.
    \nUse: write_csv(<filename>,<a list of lists to add>,<True:question, False:answer>'''
    csv_content = read_csv(filename, question)
    print(csv_content)
    csv_content.append(to_add)
    with open(filename, mode="w") as data:
        datawriter = csv.writer(data, delimiter=',')
        for row in csv_content:
            row[1] = row[1].strftime("%s")
            row[4] = bytes.decode(base64.b64encode(str.encode(row[4])))
            if question:
                row[5] = bytes.decode(base64.b64encode(str.encode(row[5])))
            datawriter.writerow(row)


def get_new_id(filename, questionoranswer):
    id_ = []
    data = read_csv(filename, questionoranswer)
    for row in data:
        id_.append(row[0])
    max_id = max(map(int, id_))
    return (int(max_id) + 1)
