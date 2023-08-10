import pandas as pd

from models import HistoricalSL, HistoricalConciliador
from conect_sql_postgres import get_session

session = get_session()

def convert_dataframe_to_dict(df):
    columns = df.columns
    list_dict = []
    
    for i, r in df.iterrows():
        dict_holidays_countries = {
            columns[0]: r[columns[0]],
            columns[1]: r[columns[1]],
            columns[2]: r[columns[2]],
            columns[3]: r[columns[3]],
            columns[4]: r[columns[4]],
            columns[5]: r[columns[5]],
            columns[6]: r[columns[6]],
        }
        list_dict.append(dict_holidays_countries)
    
    return list_dict
        

def insert_data_db(list_dict):
    session.bulk_insert_mappings(HistoricalSL, list_dict)
    session.commit()
    session.close()

def run():
    df= pd.read_csv('../../PBI/Conciliador de inventarios/sl.csv', header=0, names=['SL', 'Uso', 'Unrestricted', 'Quality_inspection', 'Blocked', 'Country', 'Date'])
    list_dict = convert_dataframe_to_dict(df)
    insert_data_db(list_dict)

if __name__ == '__main__':
    run()