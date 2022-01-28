import datetime
from pandas_datareader import test
from sqlalchemy import DateTime, Float, create_engine, text, select
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import pandas as pd
import enum

#
# SQLAlchemy Model
#
mapper_registry = registry()


@mapper_registry.mapped
class Account:
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    account_number = Column(String)
    type = Column(String)
    bank_name = Column(String)
    last_update = Column(DateTime)

    def __repr__(self):
        return "<Account(%r, %r)>" % (self.name, self.bank_name)


@mapper_registry.mapped
class Stock:
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    order_number = Column(String)
    name = Column(String)
    symbol = Column(String)
    market = Column(String)
    qty = Column(Float)
    purchase_date = Column(DateTime)
    unit_purchase_price = Column(String)
    purchase_change_rate = Column(String)
    #currency = Column(enum.Enum('EUR', 'DOLLAR'))
    currency = Column(String)
    fees = Column(String)
    currency_fees = Column(String)

    def __repr__(self):
        return "<Stock(%r, %r)>" % (self.name, self.qty)


#
# Accounts
#
bd1 = Account(
    name="Banque Direct - PEA",
    account_number="508TI00083401569EUR",
    type="PEA",
    bank_name="Bourse Direct",
    last_update=datetime.datetime(2021, 1, 10)
)
bd2 = Account(
    name="Banque Direct - PEA",
    account_number="508TI00083401569EUR",
    type="PEA",
    bank_name="Bourse Direct",
    last_update=datetime.datetime(2022, 1, 10)
)
#
# Stocks
#

stock1 = Stock(
    order_number="US7437131094",
    name="PROTO LABS", symbol="PRLB",
    market="NYSE", qty=20,
    purchase_date=datetime.datetime(2022, 1, 7),
    unit_purchase_price=51.85,
    purchase_change_rate=1.130594800,
    currency="DOLLAR",
    fees=8.5,
    currency_fees="EUR",
)


engine = create_engine("sqlite:///:memory:", echo=True, future=True)
with engine.begin() as connection:
    mapper_registry.metadata.create_all(connection)

Session = sessionmaker(bind=engine, future=True)
session = Session()
session.add_all(
    [
        bd1, bd2,
        stock1
    ]
)
#session.add(bd1)
#session.add(bd2)
#session.add(stock1)

select_statement = select(Account).filter_by(bank_name="Bourse Direct")
result = session.execute(select_statement)

# meta = MetaData()

# students = Table(
#    'students', meta,
#    Column('id', Integer, primary_key = True),
#    Column('name', String),
#    Column('lastname', String),
# )

# engine = create_engine("sqlite:///:memory:", echo=True, future=True)
# meta.create_all(engine)

# #mapper_registry = registry()

# ins = students.insert()
# ins = students.insert().values(name = 'Ravi', lastname = 'Kapoor')
# conn = engine.connect()
# result = conn.execute(ins)
# conn.execute(students.insert(), [
#    {'name':'Rajiv', 'lastname' : 'Khanna'},
#    {'name':'Komal','lastname' : 'Bhandari'},
#    {'name':'Abdul','lastname' : 'Sattar'},
#    {'name':'Priya','lastname' : 'Rajhans'},
# ])

# result = pd.read_sql(text('SELECT name FROM students'), conn)
# print(result)
# #with engine.connect() as conn:
# #    result = conn.execute(ins)
# #    for item in result.cursor():
# #        print(type(item))
