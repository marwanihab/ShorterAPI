import json
from passlib.apps import custom_app_context as pwd_context

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