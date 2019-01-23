from flask import Flask
from pymongo import MongoClient

# Create Flask application
app = Flask(__name__)
client = MongoClient('mongodb://marwan:Mm1234567@ds163164.mlab.com:63164/mongotask')
db = client.mongotask

