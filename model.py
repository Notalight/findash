import datetime
from statistics import pvariance
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

import pandas as pd

from rich import print
import rich
from rich.console import Console



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

@mapper_registry.mapped
class Loan:
    __tablename__ = "loan"
    id = Column(Integer, primary_key=True)
    loan_number = Column(String)
    name = Column(String)
    description = Column(String)
    pv = Column(Float)
    rate = Column(Float)
    nper = Column(Float)
    start_date = Column(DateTime)

    def __repr__(self):
        return "<Loan(%r, %r)>" % (self.name, self.description)


@mapper_registry.mapped
class Asset:
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    type = Column(String)
    acquisition_price = Column(Float)
    acquisition_date = Column(DateTime)
    estimation_price = Column(Float)

    def __repr__(self):
        return "<Asset(%r, %r)>" % (self.name, self.description)


#
# Helper functions
#

#
# format currency to display on console
#
def format_currency(value, currency):
    match currency:
        case 'EUR':
            if value >= 0:
                return "{:,.2f} €".format(value)
            else:
                return "({:,.2f}) €".format(-value)
        case 'DOLLAR':
            if value >= 0:
                return "{:,.2f} $".format(value)
            else:
                return "({:,.2f}) $".format(-value)
        case _:
            return "Error conversion"

def display_accounts(accounts):
    # Format table to show
    table = rich.table.Table(title="Accounts")
    table.add_column("RÃ©fÃ©rence", justify="right",
                     style="cyan", no_wrap=True)
    table.add_column("Nom", style="magenta")
    table.add_column("Banque", style="magenta")
    table.add_column("Type", style="magenta")
    table.add_column("Valeur", justify="right", style="green")
    #
    for account in accounts:
        table.add_row(account.account_number, account.name, account.bank_name, account.type,
                      format_currency(account.amount, account.currency))
    # Display result
    # TODO why use console
    console = Console()
    console.print(table)


def display_stocks(stocks):
    # Format table to show
    table = rich.table.Table(title="Stocks")
    table.add_column("Symbol", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Market", style="magenta")
    table.add_column("Qty", style="magenta")
    table.add_column("Value", justify="right", style="green")
    #
    for stock in stocks:
        table.add_row(stock.symbol, stock.name, stock.market,
                      "{:,.2f}".format(stock.qty),
                      format_currency(stock.purchase_price, stock.currency))
    # Display result
    # TODO why use console
    console = Console()
    console.print(table)

    def convert_to_dataframe(stocks):
        symbols = []
        quantities = []
        for stock in stocks:
            symbols.append(stock.symbol)
            quantities.append(stock.qty)
        stocks_list = [symbols, quantities]
        df = pd.DataFrame(stocks_list).transpose()
        df.columns = ['ticker', 'qty']
        #df.columns = ['ticker', 'qty','unit price', 'currency', 'total']
        #print (df)
        return df



        
# class Transaction(Document):
#     title = StringField(required=True, unique_with = ['bank_account','operation_date','debit','credit'])
#     bank_account = ReferenceField(Account, required=True)
#     operation_date = DateTimeField(required=True)
#     description = StringField()
#     debit = DecimalField(required=True)
#     credit = DecimalField(required=True)
#     devise = EnumField(Devise, default=Devise.EURO)

#     meta = {
#         'allow_inheritance': True,
#     #     'indexes': [
#     #         {'fields': ('title', 'bank_account','operation_date','debit','credit'), 'unique': True}
#     #     ]
#     }