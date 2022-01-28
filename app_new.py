import datetime
import pandas as pd
from locale import currency
from symtable import Symbol
from typing import List, Optional
from datetime import date
from sqlalchemy import text

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, or_, select, col


class Account(SQLModel, table=True, inherit_cache = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    account_number: str = Field(index=True)
    bank_name: str
    type: str
    iban: Optional[str] = None
    currency: str = Field(default="EUR")
    amount: float = Field(default=float(0.0))
#    stocks: List["Stock"] = Relationship(back_populates="account")
    last_update: datetime.datetime # = Field(default=datetime.date.today())
    


def create_db_and_tables(db_file_name):
    sqlite_url = f"sqlite:///{db_file_name}"
    engine = create_engine(sqlite_url, echo=False, future=True)
    SQLModel.metadata.create_all(engine)
    return engine


def create_accounts(engine):
    today = date.today().strftime("%d/%m/%Y")

    with Session(engine) as session:
        bd1 = Account(name="Banque Direct - PEA",
                      account_number="508TI00083401569EUR",
                      type="PEA", bank_name="Bourse Direct",
                      last_update=datetime.datetime(2021, 1, 10))
        bd2 = Account(name="Banque Direct - PEA",
                      account_number="508TI00083401569EUR",
                      type="PEA", bank_name="Bourse Direct",
                      last_update=datetime.datetime(2022, 1, 10))

    session.add(bd1)
    session.add(bd2)
    session.commit()

    session.refresh(bd1)
    session.refresh(bd2)

    with Session(engine) as session:
        statement = select(Account).where(
            Account.last_update > datetime.date(2021, 1, 1))
        results = session.exec(statement)
        accounts = results.all()
        print("-------------------------------------")
        print(accounts)
        print("-------------------------------------")
        
        #pd.read_sql_query('SELECT account_number FROM account', session.connection())
        #df = pd.DataFrame(sql_query, columns = ['account_number'])
        #print (df)
        result = pd.read_sql(text('SELECT name FROM account'), session.connection())
        print(result)

    #print("Après : ", bd1)


#
#
#
#engine = create_db_and_tables(":memory:")
engine = create_db_and_tables("testdb.db")
create_accounts(engine)


print("Ending World!")

# def main():
#     create_db_and_tables()
#     create_heroes()


# if __name__ == "__main__":
#
