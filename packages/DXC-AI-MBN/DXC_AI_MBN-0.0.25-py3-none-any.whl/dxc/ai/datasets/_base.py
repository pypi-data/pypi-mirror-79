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


##load data
def load_data(filename):
    module_path = dirname(__file__)
    finalfile = filename + '.csv'
    df = load_filedata(module_path, finalfile)
    return df

##Airbnb data
def load_abdata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'ABDATA.csv')
    return df

##Breast Cancer data
def load_breastcancerdata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'breast-cancer.csv')
    return df

##German data
def load_germandata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'german.csv')
    return df

##haberman data
def load_habermandata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'haberman.csv')
    return df

##horse-colic data
def load_horsecolicdata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'horse-colic.csv')
    return df
    
##ionosphere data
def load_horsecolicdata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'ionosphere.csv')
    return df

##oil-spill data
def load_oilspilldata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'oil-spill.csv')
    return df

##pima-indians-diabetes data
def load_pimaindiandiabetesdata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'pima-indians-diabetes.csv')
    return df

##sonar data
def load_sonardata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'sonar.csv')
    return df
