from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Table, MetaData
import datetime

engine = create_engine('sqlite:///trades.db')
metadata = MetaData()

trades = Table('trades', metadata,
    Column('id', Integer, primary_key=True),
    Column('symbol', String),
    Column('price', Float),
    Column('qty', Integer),
    Column('timestamp', DateTime, default=datetime.datetime.utcnow)
)

metadata.create_all(engine)
print("Database initialized.")