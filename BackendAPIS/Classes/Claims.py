from flask import jsonify, url_for, redirect, request
from flask_restful import Resource
from bson.objectid import ObjectId

# Custome Imports
from myConfig import *


# CLASS API
class Claims(Resource):

    fields = ["userId", "offerId"]

    def get(self,UsersClaimedTheOffer=None,claimedOffersForUserId=None):
        if claimedOffersForUserId:
            cursor = mongo.db.claims.find({'userId':ObjectId(claimedOffersForUserId)},{'_id':0,'userId':0})

            data=[]
            for claimedoffer in cursor:
                data.append(str(claimedoffer['offerId']))
            return jsonify({"response": data})
        elif UsersClaimedTheOffer:
            cursor = mongo.db.claims.find({'offerId': ObjectId(UsersClaimedTheOffer)}, {'_id': 0, 'offerId': 0})

            data = []
            for claimedoffer in cursor:
                data.append(str(claimedoffer['userId']))
            return jsonify({"response": data})
        else:
            cursor = mongo.db.claims.find({},{'_id': 0})
            data = []
            for record in cursor:
                record['userId'] = str(record['userId'])
                record['offerId'] = str(record['offerId'])
                data.append(record)
            return jsonify({"response": data})



    def post(self):
        data = request.get_json()

        # insert claim to db
        if data.get('userId') and data.get('offerId'):
            data['userId'] = ObjectId(data['userId'])
            data['offerId'] = ObjectId(data['offerId'])
            record = mongo.db.claims.find_one({"userId": data['userId'],"offerId":data['offerId']})
            if not record:
                mongo.db.claims.insert(data)
                return {"Success": "Record Inserted."}
            else:
                return {"Error": "Record Already Exists."}
        else:
            return {"Error": "Data fields missing. Must contain userId and offerId"}

