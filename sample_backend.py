from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, world!'

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name') # accessing the value of parameter 'name' given in HTTP request
        if search_username:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['name'] == search_username:
                    subdict['users_list'].append(user)
            return subdict
        return users
    elif request.method == 'POST':
        userToAdd = request.get_json()
        users['users_list'].append(userToAdd)
        resp = jsonify(success=True)
        #resp.status_code = 200 #optionally, you can always set a response code. 
        # 200 is the default code for a normal response
        return resp

@app.route('/users/<id>', methods=['GET', 'DELETE']) #flask allows the use of <> to wrap a variable that is part of the URL
def get_user(id): #Here we are using id as parameter because we wrap <id> as a variable that comes from the HTTP request
    if request.method == 'GET': #Unless specified otherwise, HTTP requests are GET by default
        if id:
            for user in users['users_list']:
                if user['id'] == id:
                    return user
            return ({})
        return users
    elif request.method == 'DELETE':
        if id:
            for user in users['users_list']:
                if user['id'] == id:
                    users['users_list'].remove(user) #Remove user from list
                    resp = jsonify(success=True)
                    return resp
            #Not sure if this is proper API etiquette to return success=false when attempting to delete a use that doesn't exist
            resp = jsonify(success=False)
            return resp

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