from flask import jsonify, url_for, redirect, request
from flask_restful import Resource
from bson.objectid import ObjectId
import datetime
from Resources import SparkKafka
from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError

import random

#Custome Imports
from myConfig import *
from Classes.UtilityMethods import *

#LOAD RESOURCE
kafkaInstance = SparkKafka.SparkKafkaService()
# kafkaInstance = None
class Merchants(Resource):
    fields = ["name", "password", "address", "lat","lon"]

    def get(self, merchantId=None,merchantloginId=None,byMerchantLocation=None):
        data = []

        if merchantId:
            merchant = mongo.db.merchants.find_one({"_id": ObjectId(merchantId)})

            if merchant:
                merchant['_id'] = str(merchant['_id'])
                return jsonify({"status": "ok", "data": merchant})
            else:
                return {"response": "no merchant found with id {}".format(merchantId)}
        elif merchantloginId:

            merchant = mongo.db.merchants.find_one({"_id": ObjectId(merchantloginId)})
            merchant['_id'] = str(merchant['_id'])
            if merchant:
                return jsonify({"status": "ok", "password": merchant['password']})
            else:
                # return {"response": "no user found with id {}".format(userId)}
                message = {
                    'status': 404,
                    'message': 'Merchant Not Found '
                }
                resp = jsonify(message)
                resp.status_code = 404
                return resp
        elif (byMerchantLocation):
            data = []
            lat = float(request.args['lat'])
            lon = float(request.args['lon'])
            maxdist = float(request.args['maxdist'])

            #ONLY FOR SPARK
            if byMerchantLocation == 'spark':
                userId = request.args['userId']
                merchantIds = []
                dt = datetime.datetime.now()
                cursor = mongo.db.merchants.find({"location": {"$within": {"$center": [[lat, lon], maxdist]}}},{"update_time": 0,'location':0,'name':0,'password':0,'address':0})
                for merchant in cursor:
                    merchantIds.append(merchant['_id'])
                # offerCursor = mongo.db.offers.find({'merchantId': { '$in': merchantIds}} )
                pipe_query = [
                    {
                        '$match': {
                            "merchantId": {'$in': merchantIds},
                            "validity": { '$gte': dt }
                        }
                    },
                    {
                        '$lookup': {
                            'from': "merchants",
                            'localField': "merchantId",
                            'foreignField': "_id",
                            'as': "merchantDetails"
                        }
                    }
                ]

                cursor = mongo.db.offers.aggregate(pipe_query)
                data = []
                userId = mongo.db.userMappings.find_one({'id':userId})['no']
                for offer in cursor:
                    try:
                        offerId = mongo.db.offerMappings.find_one({'id':str(offer['_id'])})['no']
                        rec = str(userId) + "," + str(offerId)
                        print(rec)
                        # rec = bytes(rec,'utf-8')
                        kafkaInstance.addMessageToQueue(rec)
                    except:
                        continue
                # return data
                return {'status':'sent'}
            #FOR GENERAL API CALLERS
            else:
                # userId = request.args['userId']
                merchantIds = []
                dt = datetime.datetime.now()
                cursor = mongo.db.merchants.find({"location": {"$within": {"$center": [[lat, lon], maxdist]}}},
                                                 {"update_time": 0, 'location': 0, 'name': 0, 'password': 0,
                                                  'address': 0})
                for merchant in cursor:
                    merchantIds.append(merchant['_id'])
                # offerCursor = mongo.db.offers.find({'merchantId': { '$in': merchantIds}} )
                pipe_query = [
                    {
                        '$match': {
                            "merchantId": {'$in': merchantIds},
                            "validity": {'$gte': dt}
                        }
                    },
                    {
                        '$lookup': {
                            'from': "merchants",
                            'localField': "merchantId",
                            'foreignField': "_id",
                            'as': "merchantDetails"
                        }
                    }
                ]

                cursor = mongo.db.offers.aggregate(pipe_query)
                data = []

                for offer in cursor:
                    joined_offer = {}
                    joined_offer['_id'] = str(offer['_id'])
                    joined_offer['description'] = offer['description']
                    joined_offer['validity'] = offer['validity']
                    joined_offer['merchantId'] = str(offer['merchantDetails'][0]['_id'])
                    joined_offer['merchantName'] = offer['merchantDetails'][0]['name']
                    joined_offer['location'] = offer['merchantDetails'][0]['location']
                    data.append(joined_offer)


                # cursor = mongo.db.merchants.find({"location": {"$within": {"$center": [[lat, lon], maxdist]}}}, {"update_time": 0})
                #
                # for merchant in cursor:
                #     merchant['_id'] = str(merchant['_id'])
                #     data.append(merchant)

                return jsonify({"response": data})
        else:
            cursor = mongo.db.merchants.find({}, {"update_time": 0}).limit(10)

            for merchant in cursor:
                merchant['_id'] = str(merchant['_id'])
                data.append(merchant)

            return jsonify({"response": data})

    def post(self,merchantRegister=None):

        data = request.get_json()

        if merchantRegister == 'True':
            query_data = {}
            query_data['name'] = data['name']
            query_data['address'] = data['address']
            merchant = mongo.db.merchants.find_one(query_data, {"update_time": 0})

            if merchant:
                update_data = {'password':data['password']}
                mongo.db.merchants.update({'_id': merchant['_id']}, {'$set': update_data})
                return jsonify({"status": "ok", 'message':'pasword updated','_id': str(merchant['_id'])})
            else:
                new_merchant = {}
                new_merchant['name'] = data['name']
                new_merchant['address'] = data['address']
                new_merchant['password'] = data['password']
                new_merchant['location'] = {'lat':data['lat'],'lon':data['lon']}

                _id = mongo.db.merchants.insert(new_merchant)
                # return {"response": "no user found with id {}".format(userId)}
                response = {
                    'status': 'ok',
                    'message': 'new merchant inserted',
                    '_id': str(_id)
                }
                resp = jsonify(response)
                return resp

        else:
            if validateRecord(data,self.fields):
                mongo.db.merchants.insert(data)
                response = {
                    'status': 'ok',
                    'message': 'inserted'
                }
                resp = jsonify(response)
                return resp
            else:
                response = {
                    'status': 'error',
                    'message': 'Validation of fields failed'
                }
                resp = jsonify(response)
                return resp

    def put(self, merchantId):
        data = request.get_json()
        mongo.db.merchants.update({'_id': ObjectId(merchantId)}, {'$set': data})
        response = {
            'status': 'ok',
            'message': 'updated'
        }
        resp = jsonify(response)
        return resp

    def delete(self, merchantId):
        mongo.db.merchants.remove({'_id': ObjectId(merchantId)})
        response = {
            'status': 'ok',
            'message': 'deleted'
        }
        resp = jsonify(response)
        return resp