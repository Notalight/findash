from model import Account, Stock, Loan, Asset, mapper_registry
import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select


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
# Loans
#
loan1 = Loan(
    loan_number="AX05899559",
    name="0001338324701 ALTIMO FIX",
    description="Prêt Maison principale",
    pv=-67190.45,
    rate=0.0115,
    nper=66,
    start_date=datetime.datetime(2021, 2, 5)
)

loan2 = Loan(
    loan_number="00002681303",
    name="CCHQ 65080290572",
    description="Prêt Appt. Viry Chatillon",
    pv=-190021,
    rate=0.0063,
    nper=120,
    start_date=datetime.datetime(2021, 7, 22)
)

loan3 = Loan(
    loan_number="00002681285",
    name="CCHQ 65080290262",
    description="Prêt Appt.  Crépy en Valois",
    pv=-68325,
    rate=0.0063,
    nper=96,
    start_date=datetime.datetime(2021, 8, 19)
)


#
# Assets
#
asset1 = Asset(
    name="Appt Crépy",
    description="Appt Crépy",
    type="appt",
    acquisition_price=110000,
    acquisition_date =datetime.datetime(2017, 7, 1),
    estimation_price = 130000
)

asset2 = Asset(
    name="Maison Igny",
    description="Maison Igny",
    type="maison",
    acquisition_price=740000,
    acquisition_date =datetime.datetime(2021, 7, 1),
    estimation_price = 950000
)

asset3 = Asset(
    name="Appt Viry",
    description="Appt Viry",
    type="appt",
    acquisition_price=210000,
    acquisition_date =datetime.datetime(2021, 7, 1),
    estimation_price = 210000
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

stock2 = Stock(
    order_number="FR0014005HJ9",
    name="OVH GROUPE", symbol="OVH",
    market="EURONEXT", qty=35,
    purchase_date=datetime.datetime(2022, 1, 7),
    unit_purchase_price=26.825,
    currency="EUR",
    fees=1.90,
    currency_fees="EUR",
)

stock3 = Stock(
    order_number="US88554D2053",
    name="3 D SYS.PROV.REGPT", symbol="DDD",
    market="NYSE", qty=50,
    purchase_date=datetime.datetime(2022, 1, 7),
    unit_purchase_price=20.0499,
    purchase_change_rate=1.130594800,
    currency="DOLLAR",
    fees=8.5,
    currency_fees="EUR",
)

stock4 = Stock(
    order_number="US79466L3024",
    name="SALESFORCE.COM(NYSE)", symbol="CRM",
    market="NYSE", qty=5,
    purchase_date=datetime.datetime(2022, 1, 7),
    unit_purchase_price=226.96,
    purchase_change_rate=1.130594800,
    currency="DOLLAR",
    fees=8.5,
    currency_fees="EUR",
)

#
#
#


def populate(session):

    session.add_all(
        [
            bd1, bd2,
            stock1, stock2, stock3, stock4,
            loan1, loan2, loan3,
            asset1, asset2, asset3
        ]
    )

    session.commit()

    select_statement = select(Account)
    result = session.execute(select_statement)
    for account_obj in result.scalars():
        print("Account : ", account_obj)

    select_statement = select(Stock)
    result = session.execute(select_statement)
    for stock_obj in result.scalars():
        print("Stock : ", stock_obj)

    select_statement = select(Loan)
    result = session.execute(select_statement)
    for loan_obj in result.scalars():
        print("Loan : ", loan_obj)

    select_statement = select(Asset)
    result = session.execute(select_statement)
    for asset_obj in result.scalars():
        print("Asset : ", asset_obj)


#
#
#

def create_db_and_tables(db_file_name):
    engine = create_engine(
        f"sqlite:///{db_file_name}", echo=False, future=True)
    with engine.begin() as connection:
        mapper_registry.metadata.create_all(connection)

    Session = sessionmaker(bind=engine, future=True)
    session = Session()
    return session
