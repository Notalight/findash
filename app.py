import datetime

from sqlalchemy import DateTime, Float, create_engine, text, select
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy import text
from sqlalchemy import Column, Integer, String

import pandas as pd
from pandas_datareader import test
import warnings
import matplotlib.pyplot as plt
import numpy as np




import enum

from setup_db import *




#
# Setup SQLAchemy
#
#mapper_registry = registry()
# engine = create_engine("sqlite:///:memory:", echo=True, future=True)
# with engine.begin() as connection:
#     mapper_registry.metadata.create_all(connection)

# Session = sessionmaker(bind=engine, future=True)
# session = Session()

session = create_db_and_tables(":memory:")
print("Populate...")
populate(session)

#









# result = pd.read_sql(text('SELECT name FROM students'), conn)
# print(result)
# #with engine.connect() as conn:
# #    result = conn.execute(ins)
# #    for item in result.cursor():
# #        print(type(item))
