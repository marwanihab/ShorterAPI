from flask import Flask
from flask import abort
from flask import jsonify
from flask import g, request, current_app 
from datetime import datetime
from pymongo import MongoClient
from flask import make_response
import random, string
from flask_api import status # HTTP Status Codes


######################################################################
# Custom Exceptions
######################################################################
class DataValidationError(ValueError):
    pass


app = Flask(__name__)

client = MongoClient('mongodb://marwan:Mm1234567@ds163164.mlab.com:63164/mongotask')
db = client.mongotask


######################################################################
# ERROR Handling
######################################################################

def generate_random_slug():
       x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
       return x


def get_shortlink(db,slug):
    return db.links.find_one({"slug":slug})

def add_shortlink(db,shortlink):
    db.links.insert_one(shortlink)


    

@app.errorhandler(DataValidationError)
def request_validation_error(e):
    return make_response(jsonify(status=400, error='Bad Request', message=str(e)), status.HTTP_400_BAD_REQUEST)

@app.errorhandler(404)
def not_found(e):
    response = {
                         "status": "failed",
                         "message": "not found"
                        }
    return make_response(jsonify(response), status.HTTP_404_NOT_FOUND)

@app.errorhandler(400)
def bad_request(e):
    response = {
                          "status": "failed",
                          "message": "Bad Request you have provided already existed slug ID"
                         }
    return make_response(jsonify(response), status.HTTP_400_BAD_REQUEST)

@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(jsonify(status=405, error='Method not Allowed', message='Your request method is not supported. Check your HTTP method and try again.'), status.HTTP_405_METHOD_NOT_ALLOWED)

@app.errorhandler(500)
def internal_error(e):
 response = {}
 return make_response(jsonify(response), status.HTTP_500_INTERNAL_SERVER_ERROR)
 

@app.route('/shortlinks', methods=['GET','POST'])
def get_add_handler():
    if request.method == 'GET':
        
        response =[]
        for link in db.links.find():
             response.append({'slug':link['slug'],'ios':link['ios'],'android':link['android'] , 'web':link['web']})

        return jsonify({'shortlinks':response})
    else :
        
        if not request.is_json:
            raise DataValidationError('Case Non-JSON Content-Type')

        slugID = request.json['slug']
        
        if slugID == "" :
                slugID = generate_random_slug()

        if get_shortlink(db,slugID):
            abort(400)         
        else :
         ios = request.json['ios']
         android = request.json['android']
         web = request.json['web']
         shortlink = {
             "slug": slugID,
             "ios": ios,
             "android": android,
             "web": web
                     }

         add_shortlink(db,shortlink)
         response = {
             "status": "successful",
             "slug": slugID,
             "message": "created successfully"
                    } 

         return  jsonify(response)


@app.route('/shortlinks/<slug>' , methods=['PUT'])
def update_handler(slug):

    if not request.is_json:
            raise DataValidationError('Case Non-JSON Content-Type')

    if not get_shortlink(db,slug):
            abort(400)       
    
    data = request.get_json()
    response={'slug':slug}
    if 'ios' in data: 
        ios = {} 
        if 'primary' in data['ios']:
            ios['primary'] = data['ios']['primary']
        if 'fallback' in data['ios']:
            ios['fallback'] = data['ios']['fallback']
        if not len(ios) == 0:
         response['ios']= ios       
         db.links.update_one({'slug':slug},{"$set": { 'ios': ios} })

    if 'android' in data:
        android = {} 
        if 'primary' in data['android']:
            android['primary'] = data['android']['primary']
        if 'fallback' in data['android']:
            android['fallback'] = data['android']['fallback']
        if not len(android) == 0: 
         response['android']= android
         db.links.update_one({'slug':slug},{"$set": { 'android': android} })     
        
    if 'web' in data:
        web = data['web']

        if not len(web) == 0: 
         response['web']= web
         db.links.update_one({'slug':slug},{"$set": { 'web': web} })    

    return jsonify(response)            
       
     
 #TODO 
 # schema validation
 # authentication  
 # Tests
   

if __name__ == '__main__':
    
    app.run(debug=True)
   
    