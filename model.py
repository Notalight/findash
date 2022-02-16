from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pydantic import ValidationError
#
import numpy as np
import numpy_financial as npf
import pandas as pd

import rich
#from rich import print
from rich.console import Console

console = Console()


class Asset(BaseModel):
    name: str
    description: str
    type: str
    acquisition_price: float
    acquisition_date: str
    estimation_price: float


class Loan(BaseModel):
    loan_number: str
    name: str
    description: str
    pv: float
    rate: float
    nper: int
    start_date: str


class Stock(BaseModel):
    order_number: str
    name: str
    symbol: str
    market: str
    qty: float
    purchase_date: str
    unit_purchase_price: float
    purchase_change_rate: Optional[float] = 1.0
    currency: str
    fees: float
    currency_fees: str


class Account(BaseModel):
    id: str
    name: str
    account_number: str
    type: str
    bank_name: str
    loans: Optional[list[Loan]] = []
    stocks: Optional[list[Stock]] = []


class Portfolio(BaseModel):
    id: str
    name: str
    accounts: list[Account]
    assets: Optional[list[Asset]] = None

    def get_loans(self):
        loans = []
        for account in self.accounts:
            for loan in account.loans:
                loans.append(loan)
        return loans

    def show_accounts(self):
        # Format table to show
        table = rich.table.Table(title="Accounts")
        table.add_column("", justify="right",
                         style="blue", no_wrap=True)
        table.add_column("Name", justify="left",
                         style="cyan", no_wrap=True)
        table.add_column("Bank Name", style="magenta")
        table.add_column("Type", style="green")
        table.add_column("Account Number", style="magenta", justify="right")
        count = 1
        for account in self.accounts:
            table.add_row(str(count), account.name,
                          account.bank_name, account.type, account.account_number)
            count += 1
        console.print(table)

    def get_loan_list(self):
        loan_list = []
        for account in self.accounts:
            for loan in account.loans:
                loan_list.append(loan)
        return loan_list

    def get_stock_list(self):
        stock_list = []
        for account in self.accounts:
            for stock in account.stocks:
                stock_list.append(stock)
        return stock_list


def get_df_from_loan(loan: Loan):
    date_index = pd.date_range(
        start=loan.start_date, periods=loan.nper, freq='M')
    df = pd.DataFrame(
            index = date_index,
            columns = ['period', 'pmt', 'interest','ppmt']
    )
    df.period = range(1,loan.nper+1)
    df.pmt = npf.pmt(loan.rate/12, loan.nper, loan.pv, 0.0)
    df.ppmt = npf.ppmt(loan.rate/12, df.period, loan.nper, loan.pv, 0.0)
    df.interest = df.pmt - df.ppmt
    return df



def load_portfolio(path: str):
    portfolio_json = open(path, 'r').read()
    portfolio = Portfolio.parse_raw(portfolio_json)
    return portfolio


def save_portfolio(path: str):
    pass


portfolio = load_portfolio('portfolio.json')
loan1 = get_df_from_loan(portfolio.get_loan_list()[0])
loan1.drop('ppmt', inplace=True, axis=1)

#portfolio_json = open('portfolio.json', 'r').read()
# jsonpickle.set_preferred_backend('simplejson')
# jsonpickle.load_backend(simplejson)

# portfolio.show_accounts()

# portfolio.get_loans()
