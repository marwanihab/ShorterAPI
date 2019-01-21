from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.examples


@app.route('/shortlinks', methods=['GET','POST'])
def get_add_handler():
    if request.method == 'GET':
       return "get request"
    else :
        return "post request"



if __name__ == '__main__':
    app.run(debug=True)
