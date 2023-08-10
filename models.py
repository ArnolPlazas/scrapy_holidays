from sqlalchemy import Column, Date, Integer, String, MetaData
from sqlalchemy.orm import declarative_base

from conect_sql_postgres import get_engine_from_settings

SCHEMA = 'conciliadores'

Base = declarative_base(metadata=MetaData(schema=SCHEMA))
engine = get_engine_from_settings()


class User(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30))
    email = Column(String(50))
    type_user = Column(String(20))
    country = Column(String(20))

class HistoricalSL(Base):
    __tablename__ = 'historical_sl'
    id_historical_sl = Column(Integer, primary_key=True, autoincrement=True)
    SL = Column(String(20), nullable=False)
    Uso = Column(String(50), nullable=False)
    Unrestricted = Column(Integer, nullable=False)
    Quality_inspection = Column(Integer, nullable=False)
    Blocked = Column(Integer, nullable=False)
    Country = Column(String(20), nullable=False)
    Date = Column(Date, nullable=False)

class HistoricalConciliador(Base):
    __tablename__ = 'historical_conciliator'
    id_historical_conciliator = Column(Integer, primary_key=True, autoincrement=True)
    Material = Column(String(30), nullable=False)
    SL_HP = Column(String(50))
    SL_LSP = Column(String(50))
    Quantity_HP = Column(Integer, nullable=False)
    Quantity_LSP = Column(Integer, nullable=False)
    Difference = Column(Integer, nullable=False)
    Country = Column(String(20), nullable=False)
    Date = Column(Date, nullable=False)
    




