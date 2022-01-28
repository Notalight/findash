from pandas_datareader import test
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import text

import pandas as pd

#
# SQLAlchemy Model
#
meta = MetaData()

students = Table(
   'students', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('lastname', String), 
)

engine = create_engine("sqlite:///:memory:", echo=True, future=True)
meta.create_all(engine)

#mapper_registry = registry()

ins = students.insert()
ins = students.insert().values(name = 'Ravi', lastname = 'Kapoor')
conn = engine.connect()
result = conn.execute(ins)
conn.execute(students.insert(), [
   {'name':'Rajiv', 'lastname' : 'Khanna'},
   {'name':'Komal','lastname' : 'Bhandari'},
   {'name':'Abdul','lastname' : 'Sattar'},
   {'name':'Priya','lastname' : 'Rajhans'},
])

result = pd.read_sql(text('SELECT name FROM students'), conn)
print(result)
#with engine.connect() as conn:
#    result = conn.execute(ins)
#    for item in result.cursor():
#        print(type(item))
    
    