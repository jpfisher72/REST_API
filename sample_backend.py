from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	return 'Hello, world!'

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        search_name = request.args.get('name')
        search_job = request.args.get('job')
        if search_name or search_job:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if search_name and (not search_job): #If searching by name only
                    if user['name'] == search_name:
                        subdict['users_list'].append(user)
                if (not search_name) and search_job: #If searching by job only
                    if user['job'] == search_job:
                        subdict['users_list'].append(user)
                if search_name and search_job: #If searching by name and job
                    if (user['name'] == search_name) and (user['job'] == search_job):
                        subdict['users_list'].append(user)
            return subdict
        return users
    elif request.method == 'POST':
        userToAdd = request.get_json()
        # Here we're adding a (hopefully) unique ID to the userToAdd dict entry
        userToAdd.update({'id': randID()}) #userToAdd is now complete with random ID and ready to be added to users list and returned to frontend
        users['users_list'].append(userToAdd)
        # resp = jsonify(success=True)
        # resp.status_code = 201
        #resp.status_code = 200 #optionally, you can always set a response code. 
        # 200 is the default code for a normal response
        #return resp
        return userToAdd, 201

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
                    return jsonify(success=True), 204
            return jsonify(success=False), 404
        return users

def randID():
    id = ""
    for i in range(0,3):
        id += random.choice(string.ascii_lowercase)
    for i in range(0,3):
        id += str(random.randint(0,9))
    return id

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