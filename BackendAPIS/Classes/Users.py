from flask import jsonify, url_for, redirect, request
from flask_restful import Resource
from flask_pymongo import PyMongo
from Resources import SQS_UserRequests

#Custome Imports
from myConfig import *
from Classes.UtilityMethods import *

#LOAD RESOURCES
user_sqs = SQS_UserRequests.SQS_UserRequests()

#CLASS API

class Users(Resource):

    fields = []

    def get(self, userId=None,userloginId=None,byLocation=None):
        data = []
        if userId:
            user = mongo.db.users.find_one({"_id": ObjectId(userId)}, {"_id": 0})
            if user:
                return jsonify({"status": "ok", "data": user})
            else:
                return {"response": "no user found with id {}".format(userId)}
        elif(userloginId != None):

            user = mongo.db.users.find_one({"_id": ObjectId(userloginId)}, {"_id": 0})
            if user:
                return jsonify({"status": "ok", "data": user['password']})
            else:
                # return {"response": "no user found with id {}".format(userId)}
                message = {
                    'status': 404,
                    'message': 'Not Found: ' + request.url,
                }
                resp = jsonify(message)
                resp.status_code = 404
                return resp
        elif (byLocation):
            data = []
            lat = float(request.args['lat'])
            lon = float(request.args['lon'])
            maxdist = float(request.args['maxdist'])

            # cursor = mongo.db.users.find({"location": {"$near":{"$geometry":{"type": "Point","coordinates": [lat, lon]},"$maxDistance":maxdist}}}, {"_id": 0, "update_time": 0})
            cursor = mongo.db.users.find({"location": {"$within": {"$center": [[lat, lon], maxdist]}}},{"update_time": 0})
            for user in cursor:
                user['_id'] = str(user['_id'])
                data.append(user)
            return jsonify({"response": data})
        else:
            cursor = mongo.db.users.find({}, { "update_time": 0})

            print("limit 10")
            for user in cursor:
                user['_id'] = str(user['_id'])
                data.append(user)

            return jsonify({"response": data})

    def post(self,userRegister=None,updateLocation=None,updateTokenFor=None):
        data = request.get_json()

        if userRegister:
            query_data = {}
            query_data['name'] = data['name']
            query_data['address'] = data['address']
            query_data['location'] = {'lat': data['lat'], 'lon': data['lon']}
            user = mongo.db.users.find_one(query_data, {"update_time": 0})

            if user:
                update_data = {'password':data['password']}
                mongo.db.users.update({'_id': user['_id']}, {'$set': update_data})
                return jsonify({"status": "ok", 'message':'pasword updated','_id': str(user['_id'])})
            else:
                new_user = {}
                new_user['name'] = data['name']
                new_user['address'] = data['address']
                new_user['password'] = data['password']
                new_user['location'] = {'lat':data['lat'],'lon':data['lon']}
                new_user['firebaseToken'] = data['firebaseToken']

                _id = mongo.db.users.insert(new_user)
                # return {"response": "no user found with id {}".format(userId)}
                response = {
                    'status': 'ok',
                    'message': 'new user inserted',
                    '_id': str(_id)
                }
                resp = jsonify(response)
                return resp

        if updateLocation != None:
            user_sqs.addMessageToQueue(data)
            update_data = data
            mongo.db.users.update({'_id': ObjectId(data['userId'])}, {'$set': update_data})

        elif updateTokenFor != None:
            userId = ObjectId(updateTokenFor)
            mongo.db.users.update({'_id': userId}, {'$set': data})
            return genResponseMsg('ok','updated')
        #insert user to db
        else:

            pass


    # def put(self, userId):
    #     userId = ObjectId(userId)
    #     data = request.get_json()
    #     mongo.db.users.update({'_id': userId}, {'$set': data})
    #     return redirect(url_for("users"))

    def delete(self, userId):
        mongo.db.users.remove({'userId': userId})
        return redirect(url_for("users"))