import os
import unittest
from controller import app 
from base64 import b64encode
import base64
import re
import json
import random, string
from lazy import lazy
import time

class BasicTests(unittest.TestCase):
    
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
    
    def getshortlinks(self):
     userAndPass = b64encode(b"Mo:1").decode("ascii")
     headers={
     'content-type': 'application/json',
      'Authorization': 'Basic %s' % userAndPass
     } 
     return self.app.get('/shortlinks',  headers=headers, follow_redirects=True)
    
    def post_invalid_shortlink(self,slug):
        userAndPass = b64encode(b"Mo:1").decode("ascii")
        headers={
        'content-type': 'application/json',
        'Authorization': 'Basic %s' % userAndPass
         } 
        return self.app.post(
        '/shortlinks',
        data=json.dumps(dict(slug=slug)),
        follow_redirects=True,headers=headers
    )

    def post_valid_shortlink(self, slug , iosPrimary , iosFallback , androidPrimary , androidFallback , webb):
        ios = {}
        android={}
        
        ios["primary"] = iosPrimary
        ios["fallback"] = iosFallback
        android["primary"] = androidPrimary
        android["fallback"] = androidFallback
        userAndPass = b64encode(b"Mo:1").decode("ascii")
        headers={
        'content-type': 'application/json',
        'Authorization': 'Basic %s' % userAndPass
         } 
        response ={}
        response["slug"] = slug
        response["ios"] = ios
        response["android"] = android
        response["web"] = webb  
        return self.app.post(
        '/shortlinks',
        data=json.dumps(response),
        follow_redirects=True,headers=headers
    )

    def post_exited_valid_shortlink(self, slug , iosPrimary , iosFallback , androidPrimary , androidFallback , webb):
        ios = {}
        android={}
        
        ios["primary"] = iosPrimary
        ios["fallback"] = iosFallback
        android["primary"] = androidPrimary
        android["fallback"] = androidFallback
        userAndPass = b64encode(b"Mo:1").decode("ascii")
        headers={
        'content-type': 'application/json',
        'Authorization': 'Basic %s' % userAndPass
         } 
        response ={}
        response["slug"] = slug
        response["ios"] = ios
        response["android"] = android
        response["web"] = webb  
        return self.app.post(
        '/shortlinks',
        data=json.dumps(response),
        follow_redirects=True,headers=headers
    )

    

    def put_valid_response(self, slug ,iosPrimary):
        ios = {}
        ios["primary"] = iosPrimary
        userAndPass = b64encode(b"Mo:1").decode("ascii")
        headers={
        'content-type': 'application/json',
        'Authorization': 'Basic %s' % userAndPass
         }
        response={} 
        response["ios"] = ios
        return self.app.put(
        '/shortlinks/%s' %slug,
        data=json.dumps(response),
        
        follow_redirects=True,headers=headers
    )

    def put_invalid_response(self,iosPrimary):
        ios = {}
        ios["primary"] = iosPrimary
        userAndPass = b64encode(b"Mo:1").decode("ascii")
        headers={
        'content-type': 'application/json',
        'Authorization': 'Basic %s' % userAndPass
         }
        response={} 
        response["ios"] = ios
        return self.app.put(
        '/shortlinks/',
        data=json.dumps(response),
        
        follow_redirects=True,headers=headers
    )



    

    def test_valid_get_response(self):
     response = self.getshortlinks()
     self.assertEqual(response.status_code, 200)
    
    slug  = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))

    def test_invalid_post_response(self):
     response = self.post_invalid_shortlink(self.slug)
     self.assertEqual(response.status_code, 400)
    
    def test_valid_post_response(self):
     response = self.post_valid_shortlink(self.slug, "http://iosPrimary" , "http://iosFallbak" , "http://androidPrimary" ,"http://androidFallback" ,"http://web")
     self.assertEqual(response.status_code, 200) 
    
    def test_valid_put_response(self):
     response = self.put_valid_response(self.slug, "http://iosPrimary" )
     self.assertEqual(response.status_code, 200)

    def test_invalid_put_response(self):
     response = self.put_invalid_response("http://iosPrimary" )
     self.assertEqual(response.status_code, 404) 


 

 
if __name__ == "__main__":
    unittest.main()