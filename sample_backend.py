from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string
from model_mongodb import User

app = Flask(__name__)
#CORS stands for Cross Origin Requests.
CORS(app) #Here we'll allow requests coming from any domain. Not recommended for production environment.

@app.route('/')
def hello_world():
	return 'Hello, world!'

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            result = User().find_by_name_job(search_username, search_job) 
        elif search_username:
            result = User().find_by_name(search_username)
        else:
            result = User().find_all()
        return {"users_list": result}
    elif request.method == 'POST':
        userToAdd = request.get_json() # no need to generate an id ourselves
        newUser = User(userToAdd)
        newUser.save() # pymongo gives the record an "_id" field automatically
        resp = jsonify(newUser), 201
        return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        user = User({"_id":id})
        if user.reload() :
            return user
        else :
            return jsonify({"error": "User not found"}), 404
    elif request.method == 'DELETE':
        user = User({"_id":id})
        resp = user.remove()
        #Note: I'm making an assumption about the return value of the 'ok' entry in WriteResult. I can't find anything about it online
        #successful deletes result in {'n': 1, 'ok': 1.0} for resp. Not sure why it's 'n' and not 'nRemoved' also...
        if resp.get('ok') > 0:
            return jsonify(success=True), 204 #204 if user found and deleted
        elif resp.get('ok') <= 0:
            return jsonify(success=False), 404 #404 if user not found

# def find_users_by_name_job(name, job):
#     subdict = {'users_list' : []}
#     for user in users['users_list']:
#         if user['name'] == name and user['job'] == job:
#             subdict['users_list'].append(user)
#     return subdict  

# @app.route('/users', methods=['GET', 'POST'])
# def get_users():
#     if request.method == 'GET':
#         search_name = request.args.get('name')
#         search_job = request.args.get('job')
#         if search_name or search_job:
#             subdict = {'users_list' : []}
#             for user in users['users_list']:
#                 if search_name and (not search_job): #If searching by name only
#                     if user['name'] == search_name:
#                         subdict['users_list'].append(user)
#                 if (not search_name) and search_job: #If searching by job only
#                     if user['job'] == search_job:
#                         subdict['users_list'].append(user)
#                 if search_name and search_job: #If searching by name and job
#                     if (user['name'] == search_name) and (user['job'] == search_job):
#                         subdict['users_list'].append(user)
#             return subdict
#         return users
#     elif request.method == 'POST':
#         userToAdd = request.get_json()
#         # Here we're adding a (hopefully) unique ID to the userToAdd dict entry
#         userToAdd.update({'id': randID()}) #userToAdd is now complete with random ID and ready to be added to users list and returned to frontend
#         users['users_list'].append(userToAdd)
#         return userToAdd, 201

# @app.route('/users/<id>', methods=['GET', 'DELETE']) #flask allows the use of <> to wrap a variable that is part of the URL
# def get_user(id): #Here we are using id as parameter because we wrap <id> as a variable that comes from the HTTP request
#     if request.method == 'GET': #Unless specified otherwise, HTTP requests are GET by default
#         if id:
#             for user in users['users_list']:
#                 if user['id'] == id:
#                     return user
#             return ({})
#         return users
#     elif request.method == 'DELETE':
#         if id:
#             for user in users['users_list']:
#                 if user['id'] == id:
#                     users['users_list'].remove(user) #Remove user from list
#                     return jsonify(success=True), 204 #204 if user found and deleted
#             return jsonify(success=False), 404 #404 if user not found
#         return users

# def randID():
#     id = ""
#     for i in range(0,3):
#         id += random.choice(string.ascii_lowercase)
#     for i in range(0,3):
#         id += str(random.randint(0,9))
#     return id

# users = { 
#    'users_list' :
#    [
#       { 
#          'id' : 'xyz789',
#          'name' : 'Charlie',
#          'job': 'Janitor',
#       },
#       {
#          'id' : 'abc123', 
#          'name': 'Mac',
#          'job': 'Bouncer',
#       },
#       {
#          'id' : 'ppp222', 
#          'name': 'Mac',
#          'job': 'Professor',
#       }, 
#       {
#          'id' : 'yat999', 
#          'name': 'Dee',
#          'job': 'Aspring actress',
#       },
#       {
#          'id' : 'zap555', 
#          'name': 'Dennis',
#          'job': 'Bartender',
#       }
#    ]
# }
