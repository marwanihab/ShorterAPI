import json
import random , string
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

class DataValidationError(ValueError):
    pass

class User:

    def __init__(self, name , password_hash):
        self.name = name 
        self.password_hash = password_hash 

    def add_user(self,db):
     user = {}
     user['username'] = self.name
     user['password'] = self.password_hash   
     db.users.insert_one(user)    

    def hash_password(self,password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self,password):
        
        return pwd_context.verify(str(password), str(self.password_hash))

    def generate_auth_token(self, expiration=600):
    	s = Serializer(secret_key, expires_in = expiration)
    	return s.dumps({'id': self.name })     

    @staticmethod #user is not known untill decoding the token
    def verify_auth_token(token):
    	s = Serializer(secret_key)
    	try:
    		data = s.loads(token)
    	except SignatureExpired:
    		#Valid Token, but expired
    		return None
    	except BadSignature:
    		#Invalid Token
    		return None
    	user_id = data['id']
    	return user_id    