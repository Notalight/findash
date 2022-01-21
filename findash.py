import datetime

from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts="http://localhost:8529")


# Connect to "_system" database as root user.
# This returns an API wrapper for "_system" database.
sys_db = client.db('_system', username='root', password='Zalem2022$')

# Create a new database named "findash" if it does not exist.
if not sys_db.has_database('findash'):
    sys_db.create_database('findash')

# Connect to "findash" database as root user.
# This returns an API wrapper for "findash" database.
db = client.db('findash', username='root', password='Zalem2022$')

# Create a new collection named "accounts" if it does not exist.
# This returns an API wrapper for "students" collection.
if db.has_collection('accounts'):
    col_accounts = db.collection('accounts')
else:
    col_accounts = db.create_collection('accounts') 


