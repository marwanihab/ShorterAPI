from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongDB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mongoDB'

mongo = PyMongo(app)


if __name__ == '__main__':
    app.run(debug=True)
