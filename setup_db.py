from model import Account,Stock
import datetime


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


def fill_bd(session):
    print("Filling Db...")

    session.add_all(
        [
            bd1, bd2,
            stock1, stock2, stock3, stock4
        ]
    )
    print(bd1.bank_name)
    print(bd1.id)
    session.commit()
