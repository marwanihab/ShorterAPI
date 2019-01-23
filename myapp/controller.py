from flask import Flask
from flask import abort
from flask import jsonify
from flask import g, request, current_app 
from datetime import datetime
from pymongo import MongoClient
from flask import make_response
import random, string
from flask_api import status 
import schemas
from jsonschema.exceptions import ValidationError 
from models import User ,  DataValidationError
from flask_httpauth import HTTPBasicAuth
from myapp import app , db 



def generate_random_slug():
       x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
       return x


auth = HTTPBasicAuth()

def get_shortlink(db,slug):
    return db.links.find_one({"slug":slug})

def add_shortlink(db,shortlink):
    db.links.insert_one(shortlink)


######################################################################
# Authentication
######################################################################

@auth.verify_password
def verify_password(username_or_token, password):
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
     user = db.users.find_one({'username':user_id})
     user_object = User(user['username'],user['password'])
     
    else:    
     user = db.users.find_one({'username':username_or_token}) #username case sensitive
     if user :
      user_object = User(user['username'],user['password'])
      #print(user['username'],user['password'])
      if not user_object.verify_password(password): 
       abort(401)     
       return False 
     else: 
         abort(401)     
         return False  
    
    g.user = user_object
    return True
    

######################################################################
# ERROR Handling
######################################################################

@app.errorhandler(ValidationError)
def request_schema_error(e):
    return make_response(jsonify(status=400, error='Bad Request', message=str(e)), status.HTTP_400_BAD_REQUEST)



@app.errorhandler(DataValidationError)
def request_validation_error(e):

    return make_response(jsonify(status=400, error='Bad Request', message=str(e)), status.HTTP_400_BAD_REQUEST)

@app.errorhandler(404)
def not_found(e):
    response = {
                         "status": "failed",
                         "message": "not found"
                        }
    schemas.validate_client_error_schema(response)                    
    return make_response(jsonify(response), status.HTTP_404_NOT_FOUND)

@app.errorhandler(401)
def auth_failed(e):
    response = {
                         "status": "failed",
                         "message": "auth failed, failed to login user"
                        }
    schemas.validate_client_error_schema(response)                    
    return make_response(jsonify(response), status.HTTP_401_NOT_FOUND)

@app.errorhandler(400)
def bad_request(e):
    response = {
                          "status": "failed",
                          "message": "Bad Request"
                         }
    schemas.validate_client_error_schema(response)                     
    return make_response(jsonify(response), status.HTTP_400_BAD_REQUEST)

@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(jsonify(status=405, error='Method not Allowed', message='Your request method is not supported. Check your HTTP method and try again.'), status.HTTP_405_METHOD_NOT_ALLOWED)

@app.errorhandler(500)
def internal_error(e):
 response = {}
 schemas.validate_server_error_schema(response)
 return make_response(jsonify(response), status.HTTP_500_INTERNAL_SERVER_ERROR)


######################################################################
# Rounting
######################################################################

@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})



@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        raise DataValidationError('please enter a valid arguments')
    if db.users.find_one({'username':username}) is not None:
        raise DataValidationError('username already exists')
    user = User(username,"")
    user.hash_password(password)
    user.add_user(db)
    return jsonify({'username':username , 'message':'you have successfully created a new user'}) , 201


@app.route('/shortlinks', methods=['GET','POST'])
@auth.login_required
def get_add_handler():
    if request.method == 'GET':
        
        response =[]
        for link in db.links.find():
             response.append({'slug':link['slug'],'ios':link['ios'],'android':link['android'] , 'web':link['web']})
        
        output={}
        output['shortlinks'] = response
        schemas.validate_get_schema(output)
        return jsonify(output)
    else :
        
        if not request.is_json:
            raise DataValidationError('Case Non-JSON Content-Type')
        
        schemas.validate_post_schema(request.get_json())

        slugID = request.json['slug']
        
        if slugID == "" :
                slugID = generate_random_slug()

        if get_shortlink(db,slugID):
            raise DataValidationError('You have entered an already existed slug,please provide a unique slug')       
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
         schemas.validate_post_response_schema(response)
         return  jsonify(response)


@app.route('/shortlinks/<slug>' , methods=['PUT'])
@auth.login_required
def update_handler(slug):

    if not request.is_json:
            raise DataValidationError('Case Non-JSON Content-Type')

    if not get_shortlink(db,slug):
            raise DataValidationError('Please enter a valid slug')    
    
    schemas.validate_put_schema(request.get_json())

    data = request.get_json()
    response={'slug':slug}
    if 'ios' in data: 
        ios = {} 
        if 'primary' in data['ios']:
            ios['primary'] = data['ios']['primary']
            db.links.update_one({'slug':slug },{"$set": { 'ios.primary':ios['primary'] } })
        if 'fallback' in data['ios']:
            ios['fallback'] = data['ios']['fallback']
            db.links.update_one({'slug':slug },{"$set": { 'ios.fallback':ios['fallback'] } })
        if not len(ios) == 0:
         response['ios']= ios       
         

    if 'android' in data:
        android = {} 
        if 'primary' in data['android']:
            android['primary'] = data['android']['primary']
            db.links.update_one({'slug':slug},{"$set": { 'android.primary': android['primary']} })
        if 'fallback' in data['android']:
            android['fallback'] = data['android']['fallback']
            db.links.update_one({'slug':slug},{"$set": { 'android.fallback': android['fallback']} })
        if not len(android) == 0: 
         response['android']= android
              
        
    if 'web' in data:
        web = data['web']

        if not len(web) == 0: 
         response['web']= web
         db.links.update_one({'slug':slug},{"$set": { 'web': web} }) 

    schemas.validate_put_response_schema(response)
    return jsonify(response)            
       
     
 #TODO 
 # schema validation
 # authentication  
 # Tests
   

if __name__ == '__main__':
    
    app.run(debug=True)
   
    