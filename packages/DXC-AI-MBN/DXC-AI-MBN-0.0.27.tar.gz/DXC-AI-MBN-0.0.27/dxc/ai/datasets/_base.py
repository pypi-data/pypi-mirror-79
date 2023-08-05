# import pandas as pd

# def load_abdata():
#     df = pd.read_csv("data/ABDATA.csv")
#     return df

from os.path import dirname, join
import csv
import pandas as pd

def load_filedata(module_path, data_file_name):
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    with open(join(module_path, 'data', data_file_name)) as csv_file:
        data_file = csv.reader(csv_file)
        for i, ir in enumerate(data_file):
            if i == 0:
                header = ir
                df = pd.DataFrame(columns = header)
            else:
                df1 = pd.DataFrame([ir],columns = header)
            df = df.append(df1, ignore_index = True)
    return df

# def load_filecontent(module_path, content_file_name):
#     f = open(join(module_path, 'data', content_file_name))
#     file_content = f.read()
#     return file_content

##load data
def load_data(filename):
    module_path = dirname(__file__)
    finalfile = filename + '.csv'
    df = load_filedata(module_path, finalfile)
    return df

#load file content
def load_data_details(filename):
    module_path = dirname(__file__)
    finalfile = filename + '.txt'
    f = open(join(module_path, 'data', finalfile))
    file_content = f.read()
    return file_content