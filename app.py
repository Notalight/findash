import datetime
from locale import currency
from symtable import Symbol
from typing import List, Optional
from datetime import date

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, or_, select, col


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    account_number: str = Field(index=True)
    bank_name: str
    type: str
    iban: Optional[str] = None
    currency: str = Field(default="EUR")
    amount: float = Field(default=float(0.0))
    stocks: List["Stock"] = Relationship(back_populates="account")
    last_update: datetime.datetime = Field(default=datetime.date.today())


class Stock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    symbol: str
    market: str
    qty: float
    purchase_date : datetime.date
    purchase_price : float
    selling_date : Optional[datetime.date]
    selling_price : Optional[float]
    account_id: int = Field(default=None, foreign_key="account.id")
    account: Account = Relationship(back_populates="stocks")
    currency: str = Field(default="EUR")


def create_db_and_tables(db_file_name):
    sqlite_url = f"sqlite:///{db_file_name}"
    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


def create_accounts(engine):
    today = date.today().strftime("%d/%m/%Y")

    with Session(engine) as session:

        bd1 = Account(name="Banque Direct - PEA",
                  account_number="508TI00083401569EUR",
                  type="PEA", bank_name="Bourse Direct")

        bd2 = Account(name="Banque Direct - Titre",
                  account_number="508TI00085561050EUR",
                  type="Titre", bank_name="Bourse Direct")

        stock1 = Stock(name="3 D SYS.PROV.REGPT(NYSE)", symbol="DDD",
                   market="NYSE", qty=50, account=bd2,
                   purchase_date=datetime.date(2021,1,10),
                   purchase_price=0.0,
                   currency="DOLLAR")

        session.add(bd1)
        #session.add(bd2)
        #session.commit()

        session.add(stock1)
        session.commit()

        session.refresh(stock1)
        

        print("Created stock:", stock1)
        print("Created account:", stock1.account.stocks[0].name)

        # session.refresh(acc1)
        # By this point, after the with block is finished, the session is automatically closed.
        #print("Après : ", acc1)
        #acc1.name = "Test"
        #print("Après : ", acc1.bank_name)
        # session.refresh(acc1)
        #print("Après : ",type(acc1.last_update))


def select_accounts(engine):
    with Session(engine) as session:
        statement = select(Account).where(
            Account.last_update.month == datetime.date(2022, 1, 24).month)
        results = session.exec(statement)
        accounts = results.all()
        print(accounts)


engine = create_db_and_tables("testv1.db")
create_accounts(engine)


print("Hello World")


# def main():
#     create_db_and_tables()
#     create_heroes()


# if __name__ == "__main__":
#     main()
