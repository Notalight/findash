#import pymongo
from pymongo.errors import BulkWriteError
from rich import print
import rich
from rich.console import Console

from typing import Optional
from pydantic import BaseModel
from beanie import Document, Indexed, Link,  init_beanie
from beanie.exceptions import CollectionWasNotInitialized
import asyncio
import motor

import pandas as pd
import matplotlib.pyplot as plt

#
# Data Model
#


class Category(BaseModel):
    name: str
    description: str


class Account(Document):
    name: str
    account_number: Indexed(str, unique=True)
    bank_name: str
    type: str
    iban: Optional[str] = None
    currency: str = "EUR"
    amount: float = 0.0
    description: Optional[str] = None

    class Collection:
        name = "accounts"


class Stock(Document):
    order_number: str
    name: str
    symbol: str
    market: str
    qty: float
    purchase_date: str #datetime.date
    purchase_price: float = 0.0
    selling_date: Optional[str] #datetime.date]
    selling_price: Optional[float] = 0.0
    currency: str = "EUR"
    change_rate: Optional[float] = 1.0
    fees: float = 0.0
    currency_fees: str
    account:  Link[Account]

    class Collection:
        name = "stocks"

# Beanie is fully asynchronous, so we will access it from an async function


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


async def init():
    # Crete Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017"
    )

    # Init beanie with the Product document class
    await init_beanie(
        database=client.db_chris,
        document_models=[
            Account,
            Stock
        ])
    #
    # Accounts
    #
    bd1 = Account(name="Banque Direct - PEA",
                  account_number="508TI00083401569EUR",
                  type="PEA", bank_name="Bourse Direct")

    bd2 = Account(name="Banque Direct - Titre",
                  account_number="508TI00085561050EUR",
                  type="Titre", bank_name="Bourse Direct")

    axa1 = Account(name="Banque Direct - PEA",
                   account_number="508TI00083401569EUR",
                   type="PEA", bank_name="Bourse Direct")

    axa2 = Account(name="Banque Direct - Titre",
                   account_number="508TI00085561050EUR",
                   type="Titre", bank_name="Bourse Direct")
    bnp1 = Account(name="Banque Direct - PEA",
                   account_number="508TI00083401569EUR",
                   type="PEA", bank_name="Bourse Direct")

    bnp2 = Account(name="Banque Direct - Titre",
                   account_number="508TI00085561050EUR",
                   type="Titre", bank_name="Bourse Direct")
    wize1 = Account(name="Banque Direct - PEA",
                    account_number="508TI00083401569EUR",
                    type="PEA", bank_name="Bourse Direct")

    wize2 = Account(name="Banque Direct - Titre",
                    account_number="508TI00085561050EUR",
                    type="Titre", bank_name="Bourse Direct")
    n26 = Account(name="Banque Direct - PEA",
                  account_number="508TI00083401569EUR",
                  type="PEA", bank_name="Bourse Direct")

    swisslife = Account(name="Banque Direct - Titre",
                        account_number="508TI00085561050EUR",
                        type="Titre", bank_name="Bourse Direct")
    amundi = Account(name="Banque Direct - Titre",
                     account_number="508TI00085561050EUR",
                     type="Titre", bank_name="Bourse Direct")
    morganstanley = Account(name="Banque Direct - Titre",
                            account_number="508TI00085561050EUR",
                            type="Titre", bank_name="Bourse Direct")
    #
    # Stocks
    #
    stock1 = Stock(
        order_number="US7437131094",
        name="PROTO LABS", symbol="PRLB",
        market="NYSE", qty=20,
        purchase_date="2022/01/07",
        unit_purchase_price=51.85,
        change_rate=1.130594800,
        currency="DOLLAR",
        fees=8.5,
        currency_fees="EUR",
        account= bd2
    )
    stock2 = Stock(
        order_number="FR0014005HJ9",
        name="OVH GROUPE", symbol="OVH",
        market="EURONEXT", qty=35,
        purchase_date="2022/01/07",
        purchase_price=26.825,
        currency="EUR",
        fees=1.90,
        currency_fees="EUR",
        account= bd2
    )
    stock3 = Stock(
        order_number="US88554D2053",
        name="3 D SYS.PROV.REGPT", symbol="DDD",
        market="NYSE", qty=50,
        purchase_date="2022/01/07",
        purchase_price=20.0499,
        change_rate=1.130594800,
        currency="DOLLAR",
        fees=8.5,
        currency_fees="EUR",
        account= bd2
    )
    stock4 = Stock(
        order_number="US79466L3024",
        name="SALESFORCE.COM(NYSE)", symbol="CRM",
        market="NYSE", qty=5,
        purchase_date="2022/01/07",
        purchase_price=226.96,
        change_rate=1.130594800,
        currency="DOLLAR",
        fees=8.5,
        currency_fees="EUR",
        account= bd2
    )

    try:
        await bd1.insert()
        await bd2.insert()
        #await stock1.insert()
        #await Account.insert_many([bd1, bd2])
        await stock1.insert()
        await stock2.insert()
        await stock3.insert()
        await stock4.insert()
        #await Stock.insert_many([stock1, stock2, stock3, stock4])
    except BulkWriteError as err:
        print("================================")
        print(f"Unexpected {err=}, {type(err)=}")
        print("================================")

    accounts = await Account.find().to_list()
    display_accounts(accounts)
    stocks = await Stock.find().to_list()

    display_stocks(stocks)
    
    stock = await Stock.find(Stock.symbol == "DDD")


# asyncio.run(example())
# asyncio.run(init())

async def main():
    await init()


#asyncio.get_event_loop().run_until_complete(main())
asyncio.run(main())


# if __name__ == "__main__":
#    main()
#
# https://github.com/wilsonfreitas/awesome-quant#data-sources
#
