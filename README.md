# ShorterAPI

ShorterAPI is an API to deal with "url shortlinks" in a MongoDB database (create, read, update). 

## Installation
You will need to have a python 3.5.0 version installed on your computer.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install external packages required.

```bash
pip3 install pymongo
pip3 install flask
pip3 install lazy
pip3 install itsdangerous
pip3 install flask_httpauth
pip3 install passlib
pip3 install jsonschema
pip3 install flask_api
pip3 install nose2
```

## How to run

```bash
python controller.py #to run the application
nose2 #cd to the directory of the files and run nose2 to test 

#Please make sure when sending requests you are using basic auth and you are sending a valid username and password 
#To create a valid account just go to 'http://localhost:5000/users' and do a post request with your desired username
#and desired password 
#After creating the account you have 2 ways of doing requests 
#One is the basic auth method if you are using Postman just enter 
#the proper username and the proper password 
#The other one is entering in the username field a token that will expire after 10 min , if you do so you do not need to 
#porvice a password 
#The way of getting a token is simply by going to 'http://localhost:5000/token' and of course you will use a GET request 
#using basic auth and providing valid username and password
```

## Technologies
* Python 3.5.0
* Flask
* Pymong

    


