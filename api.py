from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.mongoDB


@app.route('/shortlinks', methods=['GET','POST'])
def get_add_handler():
    if request.method == 'GET':
       return "get request"
    else :
        return "post request"


@app.route('/shortlinks/<slug>' , methods=['PUT'])
def update_handler(slug):
    return "update request"

if __name__ == '__main__':
    app.run(debug=True)
