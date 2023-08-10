
import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

from create_db_postgres import Country, HolidayCountry
from conect_sql_postgres import get_session

YEAR = date.today().year
URL_ROOT = 'https://www.officeholidays.com/countries/'
session = get_session()

def update_file_holidays_country():
    countries = session.query(Country).all()

    countries_dict = {country.country_code:country.country_name for country in countries}
    df_holidays_countries = pd.DataFrame() 
    for k, v in countries_dict.items():
        url = URL_ROOT + v + '/' + str(YEAR)
        holidays_request = requests.get(url)
        if holidays_request.status_code == 200:
            s_holidays_request = BeautifulSoup(holidays_request.text, 'html.parser')
            country_holidays_data = []
            country_holidays = s_holidays_request.find('table', attrs={'class': 'country-table'}).find_all('td')
            
            for data in country_holidays:
                if data:
                    country_holidays_data.append(data.get_text())
            holidays_data = []
            
            for i in range(0,len(country_holidays_data),5):
                r = []
                r = country_holidays_data[i:i+5]
                holidays_data.append(r)

            df_holidays_country = pd.DataFrame(data=holidays_data, columns=['day', 'date', 'holiday_name', 'type_holiday', 'comments'])
            df_holidays_country = df_holidays_country.convert_dtypes()
            df_holidays_country['date'] = df_holidays_country['date'].apply(lambda x:str(YEAR) + ' ' + x)
            df_holidays_country['date'] = pd.to_datetime(df_holidays_country['date'])
            df_holidays_country = df_holidays_country[~df_holidays_country['day'].isin(['Saturday', 'Sunday'])]
            df_holidays_country['country_code'] = k
            df_holidays_countries = pd.concat([df_holidays_countries, df_holidays_country])
        else:
            print(f'Error: {holidays_request.status_code}, country: {v}')
        
    return df_holidays_countries

    
def convert_dataframe_to_dict(df_holidays_countries):
    columns = df_holidays_countries.columns
    list_dict = []
    
    for i, r in df_holidays_countries.iterrows():
        dict_holidays_countries = {
            columns[0]: r[columns[0]],
            columns[1]: r[columns[1]],
            columns[2]: r[columns[2]],
            columns[3]: r[columns[3]],
            columns[4]: r[columns[4]],
            columns[5]: r[columns[5]],
        }
        list_dict.append(dict_holidays_countries)
    
    return list_dict
        

def insert_data_db(list_dict):
    session.bulk_insert_mappings(HolidayCountry, list_dict)
    session.commit()
    session.close()

def run():
    df_holidays_countries = update_file_holidays_country()
    # df_holidays_countries.to_csv('./input/holidays_countries_' + str(YEAR) + '.csv', index=False)
    list_dict = convert_dataframe_to_dict(df_holidays_countries)
    insert_data_db(list_dict)



if __name__ == '__main__':
    run()