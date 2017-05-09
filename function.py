import csv


def read_csv(filename):
    '''Opens csv file(filename) and returns a list of lists with it's content called ***"csv_content***"'''
    csv_content = []
    with open(filename) as data:
        content = csv.reader(data, delimiter=',')
        for row in content:
            csv_content.append(row)
    return csv_content


def write_csv(filename, to_add):
    '''Writes out the list of lists to a csv file. ***REQUIRED: "csv_content" list of lists!*** '''
    csv_content.append(to_add)
    with open(filename, mode="w") as data:
        datawriter = csv.writer(data, delimiter=',')
        for row in csv_content:
            datawriter.writerow(row)
