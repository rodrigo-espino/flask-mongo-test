import json
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] ='mongodb://admin:admin@cluster0-shard-00-00.akami.mongodb.net:27017,cluster0-shard-00-01.akami.mongodb.net:27017,cluster0-shard-00-02.akami.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-hs05il-shard-0&authSource=admin&retryWrites=true&w=majority'

mongo = PyMongo(app)

CORS(app)

db = mongo.db.users
@app.route('/')
def home():
    return jsonify({"Error": "404"})
@app.route('/users', methods=['POST'])
def createUser():
    id = db.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    return jsonify({"msg": "Ok"})
    

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })
    

@app.route('/user/<id>', methods=['DELETE'])
def deleleUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({"msg": "User deleted"})

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    db.update_one({'_id':ObjectId(id)}, {'$set':{
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({"msg": "User Updated"})




if __name__ == "__main__":
    app.run(debug=True)
