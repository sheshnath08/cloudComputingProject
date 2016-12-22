from flask import jsonify, url_for, redirect, request
from flask_restful import Resource
from flask_pymongo import PyMongo
from Resources import SQS_UserRequests

#Custome Imports
from myConfig import *
from Classes.UtilityMethods import *
from requests import get
#CLASS API

class HelperClass(Resource):


    def get(self,buildtrainingdata=None,offerMapping=None):

        if offerMapping:
            userNo = int(request.args['userNo'])
            offerNo = int(request.args['offerNo'])
            userId = mongo.db.userMappings.find_one({'no':userNo})['id']
            offerId = mongo.db.offerMappings.find_one({'no': offerNo})['id']
            return {'userId':userId,'offerId':offerId}

        elif buildtrainingdata:
            trainingFile = open('trainingData1.csv', 'w')
            if 'userMappings' in mongo.db.collection_names():
                mongo.db.userMappings.drop()

            if 'offerMappings' in mongo.db.collection_names():
                mongo.db.offerMappings.drop()

            userIdList = []

            userCount = 0
            offerCount = 0
            cursor = mongo.db.users.find({}, {"update_time": 0})
            for user in cursor:
                userCount = userCount + 1
                userIdList.append((userCount,str(user['_id'])))
                data = {'no':userCount,'id': str(user['_id'])}
                mongo.db.userMappings.insert(data)

            offerIdList = []
            cursor = mongo.db.offers.find({}, {"update_time": 0})
            for offer in cursor:
                offerCount = offerCount + 1
                offerIdList.append((offerCount,str(offer['_id'])))
                data = {'no': offerCount, 'id': str(offer['_id'])}
                mongo.db.offerMappings.insert(data)

            for user in userIdList:
                userCount = userCount + 1
                for offer in offerIdList:
                    offerCount = offerCount + 1

                    record = mongo.db.claims.find_one({"userId": ObjectId(user[1]), "offerId": ObjectId(offer[1])})
                    if record:
                        claimed = '1'
                    else:
                        claimed = '0'
                    outLine = (str(user[0]) + ',' + str(offer[0]) +',' + claimed + '\n')

                    trainingFile.write(outLine)
            return  {'response': 'Built TrainingFile'}

        else:
            offerNo = request.args['offerNo']
            offerId = mongo.db.offerMappings.find_one({'no': offerNo})['id']
            resp = get("http://127.0.0.1:5000/api/offers/"+offerId)
            return resp



