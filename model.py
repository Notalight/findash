import datetime
from sqlalchemy import DateTime, Float, create_engine, text, select
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import enum


class myClass:
	def __init__(self,val):
		self.val=val
	def getVal(self):
		return self.val

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
