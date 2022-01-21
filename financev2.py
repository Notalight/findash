from enum import Enum
import datetime
from mongoengine import *

import rich
from rich import print
from rich.console import Console

import csv
from decimal import Decimal

import pandas as pd


class AccountType(Enum):
    COURANT = 'courant'
    TITRE = 'titre'

class Devise(Enum):
    EURO = 'EUR'
    DOLLAR = '$'

class Account(Document):
    reference_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    description = StringField(required=True)
    type = EnumField(AccountType, default=AccountType.COURANT)
    iban = StringField(default="Not defined")
    bic = StringField(default="Not defined")
    amount = DecimalField(default=0.0)
    bank = StringField(required=True)
    open = DateTimeField(default=datetime.date(1999, 1, 1))
    last_update = DateTimeField(default=datetime.date(1999, 1, 1))
    last_rec = DateTimeField(default=datetime.date(1999, 1, 1))
    devise = EnumField(Devise, default=Devise.EURO)

    

class Transaction(Document):
    title = StringField(required=True, unique_with = ['bank_account','operation_date','debit','credit'])
    bank_account = ReferenceField(Account, required=True)
    operation_date = DateTimeField(required=True)
    description = StringField()
    debit = DecimalField(required=True)
    credit = DecimalField(required=True)
    devise = EnumField(Devise, default=Devise.EURO)

    meta = {
        'allow_inheritance': True,
    #     'indexes': [
    #         {'fields': ('title', 'bank_account','operation_date','debit','credit'), 'unique': True}
    #     ]
    }
 

class Prelevement(Transaction):
    value_date = DateTimeField()

class Virement(Transaction):
    virement = StringField() 

class Reconciliation(Transaction):
    reconciliation = StringField()    

class Asset(Document):
    name = StringField(required=True, unique_with = ['acquisition_price'])
    description = StringField()
    type = StringField()
    acquisition_price = DecimalField(required=True)
    estimation_price = DecimalField(required=True)
    devise = EnumField(Devise, default=Devise.EURO)
    acquisition_date = DateTimeField(default=datetime.date(1999, 1, 1))

class Loan(Document):
    loan_id = StringField(required=True, unique = True)
    description = StringField()
    name = StringField()
    bank = StringField(required=True)
    pv = DecimalField(required=True)
    rate = DecimalField(required=True)
    nper = IntField(required=True)
    devise = EnumField(Devise, default=Devise.EURO)
    start_date = DateTimeField(default=datetime.date(1999, 1, 1))


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
        case '$':
            if value >= 0:
                return "{:,.2f} $".format(value)
            else:
                return "({:,.2f}) $".format(-value)
        case _:        
            return "Error conversion"


def display_accounts():
    # Format table to show
    table = rich.table.Table(title="Comptes")
    table.add_column("Référence", justify="right", style="cyan", no_wrap=True)
    table.add_column("Nom", style="magenta")
    table.add_column("Banque", style="magenta") 
    table.add_column("Type", style="magenta")  
    table.add_column("Valeur", justify="right", style="green")
    #
    for account in Account.objects:
        table.add_row(account.reference_id, account.name, account.bank,account.type.value,\
        format_currency(account.amount,account.devise.value))  
    # Display result
    # TODO why use console
    console = Console()
    console.print(table)

def add_account(account :dict):
    try:
        Account(reference_id=account["reference_id"], name=account["name"], \
        description=account["description"], iban=account["iban"], \
        bank=account["bank"]).save()
        return True
    except NotUniqueError:
        print("Oops!  Duplicate account...")
        return False

def add_asset(asset :dict):
    try:
        Asset(name=asset["name"], description=asset["description"], \
        type=asset["type"], acquisition_price=asset["acquisition_price"], \
        estimation_price=asset["estimation_price"],acquisition_date=asset["acquisition_date"]).save()
        return True
    except NotUniqueError:
        print("Oops!  Duplicate asset...")
        return False

def add_loan(loan :dict):
    try:
        Loan(loan_id=loan["loan_id"], description=loan["description"], \
        name=loan["name"], bank=loan["bank"], \
        pv=loan["pv"], rate=loan["rate"], \
        nper=loan["nper"], \
        start_date=loan["start_date"]).save()
        return True
    except NotUniqueError:
        print("Oops!  Duplicate loan...")
        return False

def add_prelevement(transaction :dict):
    # TODO check bank existance
    #
    try:  
        Prelevement(title=transaction["title"],bank_account=transaction["bank_account"],\
            credit=transaction["credit"],debit=transaction["debit"],\
            operation_date=transaction["operation_date"]).save()
        return True
    except NotUniqueError:
        print("Oops!  Duplicate transaction...")
        return False

def load_transactions(account_ref_id :str,file):
    #
    # AXA file extract
    #
    with open(file, 'r', newline='') as csvfile:
        #transac_reader = csv.reader(csvfile, delimiter=';')
        #for row in transac_reader:
        #    print(row)
        input_file = csv.DictReader(csvfile,delimiter=';')
        for raw_transact in input_file:
            bank_id = Account.objects(reference_id=account_ref_id).first()
            title = raw_transact['Libelle']
            credit = 0.0
            debit = 0.0
            if raw_transact['Credit']!='':
                credit = raw_transact['Credit'].replace(',','.')
            if raw_transact['Debit']!='':
                debit = raw_transact['Debit'].replace(',','.')
            operation_date = datetime.datetime.strptime(raw_transact['Date operation'], '%d/%m/%Y')
            value_date = datetime.datetime.strptime(raw_transact['Date valeur'], '%d/%m/%Y')
            #
            add_prelevement({'title':title,'bank_account':bank_id,'credit': credit,'debit':debit,\
                'operation_date':operation_date,'value_date':value_date})

#
# Connect to the MongoDB database
#
connect('mydb_test')


def setup():
    # Accounts
    add_account({'reference_id':'12548940010338324704025', 'name' : 'CC AXA Commun', 'description' : 'Compte Axa Banque Commun', 'iban' : "FR76 1254 8940 0103 3832 4704 025", 'bank' : "AXA Banque"})
    # Transactions
    bank_id = Account.objects(reference_id='12548940010338324704025').first()
    load_transactions("12548940010338324704025","AXA_COMPTE_COURANT_COMMUN_1_2022_01_10_12_18_27.csv")
    # Loans
    add_loan({'loan_id':'AX05899559', 'name':'0001338324701 ALTIMO FIX','description': 'Prêt Maison principale','bank':'AXA Banque','pv':-67190.45,'nper':66,'rate':0.0115, 'start_date':datetime.date(2021, 2, 5)})
    add_loan({'loan_id':'00002681303', 'name':'CCHQ 65080290572','description': 'Prêt Appt. Viry Chatillon','bank':'Crédit Agricole','pv':-190021,'nper':120,'rate':0.0063, 'start_date':datetime.date(2021, 7, 22)})
    add_loan({'loan_id':'00002681285', 'name':'CCHQ 65080290262','description': 'Prêt Appt.  Crépy en Valois ','bank':'Crédit Agricole','pv':-68325,'nper':96,'rate':0.0063, 'start_date':datetime.date(2021, 8, 19)})
    # Assets
    add_asset({'name':'Appt Crépy','description':'Appt Crépy','type':'appt','acquisition_price':110000,'estimation_price':130000,'acquisition_date':datetime.date(2017, 7, 1)})
    add_asset({'name':'Appt Viry','description':'Appt Viry','type':'appt','acquisition_price':210000,'estimation_price':210000,'acquisition_date':datetime.date(2021, 7, 1)})
    add_asset({'name':'Maison Igny','description':'Maison Igny','type':'maison','acquisition_price': 740000,'estimation_price':950000,'acquisition_date':datetime.date(2019, 5, 1)})




