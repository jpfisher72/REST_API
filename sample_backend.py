from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, world!'

@app.route('/users')
def get_users():
   search_username = request.args.get('name') # accessing the value of parameter 'name' given in HTTP request
   if search_username:
      subdict = {'users_list' : []}
      for user in users['users_list']:
         if user['name'] == search_username:
            subdict['users_list'].append(user)
      return subdict
   return users

@app.route('/users/<id>') #flask allows the use of <> to wrap a variable that is part of the URL
def get_user(id): #Here we are using id as parameter because we wrap <id> as a variable that comes from the HTTP request
   if id:
      for user in users['users_list']:
        if user['id'] == id:
           return user
      return ({})
   return users

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}