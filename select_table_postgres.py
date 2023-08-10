from create_db_postgres import Country
from conect_sql_postgres import get_session


session = get_session()


countries = session.query(Country).all()

countries_dict = {country.country_code:country.country_name for country in countries}

print(countries_dict)

# for country in countries:
#     print(country.country_name)

session.close()