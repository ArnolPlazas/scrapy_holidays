from sqlalchemy import Column, Date, ForeignKey, Integer, String, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateSchema

from conect_sql_postgres import get_engine_from_settings

SCHEMA = 'holiday'

Base = declarative_base(metadata=MetaData(schema=SCHEMA))
engine = get_engine_from_settings()


class Country(Base):
    __tablename__ = 'countries'
    country_code = Column(String(3), primary_key=True)
    country_name = Column(String(20), nullable=False)

class HolidayCountry(Base):
    __tablename__ = 'holidays_country'
    id_holiday = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(String(10), nullable=False)
    date = Column(Date, nullable=False)
    holiday_name = Column(String)
    type_holiday = Column(String)
    comments = Column(String)
    country_code = Column(String(3), ForeignKey(Country.country_code, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    countries = relationship('Country', backref='holidays_countries')

def create():

    engine.execution_options = {"schema_translate_map": {None: SCHEMA}}
    with engine.connect() as conn:
        if engine.dialect.has_schema(conn, SCHEMA):
            Base.metadata.create_all(conn)
            conn.commit()
        else:
            print('here')
            conn.execute(CreateSchema(SCHEMA))
            Base.metadata.create_all(conn)
            conn.commit()
create()


