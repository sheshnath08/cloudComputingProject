from flask import jsonify, url_for, redirect, request
from flask_restful import Resource
import datetime
from Resources import SQS_NewOffers

#Custome Imports
from myConfig import *
from Classes.UtilityMethods import *

#LOAD RESOURCES
offer_sqs = SQS_NewOffers.SQS_NewOffers()

class Offers(Resource):
    fields = ["merchantId","validity"]

    def getOfferDetails(self,cursor):
        data = []
        for offer in cursor:
            joinedoffer = {}
            joinedoffer['_id'] = str(offer['_id'])
            joinedoffer['description'] = offer['description']
            joinedoffer['Validity'] = offer['validity']
            joinedoffer['merchantId'] = str(offer['merchantId'])
            joinedoffer['name'] = offer['merchantDetails'][0]['name']
            joinedoffer['location'] = offer['merchantDetails'][0]['location']
            data.append(joinedoffer)
        return data

    def get(self, offerId=None,validity=None):

        data = []

        if offerId:
            offer = mongo.db.offers.find_one({"_id": ObjectId(offerId)})
            if offer:
                merchant = mongo.db.merchants.find_one({'_id':ObjectId(offer['merchantId'])})
                joined_offer = {}
                joined_offer['_id'] = offerId
                joined_offer['description'] = offer['description']
                # joined_offer['validity'] = offer['validity']
                joined_offer['validity'] = datetime.datetime.strftime(offer['validity'], "%Y-%m-%d %H:%M:%S")
                joined_offer['merchantId'] = str(offer['merchantId'])
                joined_offer['merchantName'] = merchant['name']
                joined_offer['location'] = merchant['location']
                return jsonify({"status": "ok", "data": joined_offer})
            else:
                return {"response": "no offer found with id {}".format(offerId)}

        elif(validity):

            if validity=="now":
                dt = datetime.datetime.now()
            else:
                dt = datetime.datetime.strptime(validity, "%Y-%m-%d %H:%M:%S")

            pipe_query = [
                {
                    '$match': {
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

            data = self.getOfferDetails(cursor)
            return jsonify({"response": data})

        else:
            pipe_query = [{'$lookup': {
                'from': "merchants",
                'localField': "merchantId",
                'foreignField': "_id",
                'as': "merchantDetails"
            }}]

            cursor = mongo.db.offers.aggregate(pipe_query)
            # cursor = mongo.db.offers.find({}, {"_id": 0, "update_time": 0}).limit(10)


            data = self.getOfferDetails(cursor)

            return jsonify({"response": data})


    def post(self):
        #Input Datetime format: "2013-09-28 20:30:55"
        data = request.get_json()
        if validateRecord(data, self.fields):
            str_dt = data.get('validity')
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")
            data['validity'] = dt
            data['merchantId'] = ObjectId(data['merchantId'])

            # offerId = data.get('offerId')
            existingoffer = mongo.db.offers.find_one(data)
            if existingoffer:
                return {"response": "offer already exists."}
            else:
                merchant = mongo.db.merchants.find_one({"_id": ObjectId(data['merchantId'])})
                if merchant:
                    _id = mongo.db.offers.insert(data)
                    try:
                        data['_id'] = str(data['_id'])
                        data['merchantId'] = str(data['merchantId'])
                        data['validity'] = datetime.datetime.strftime(data['validity'], "%Y-%m-%d %H:%M:%S")
                        data['location'] = merchant['location']
                        data['merchantName'] = merchant['name']
                        data['merchantAddress'] = merchant['address']
                        offer_sqs.addMessageToQueue(data)
                    except Exception as e:
                        print(e)
                else:
                    return genResponseMsg('error', 'MerchantId does not exists.')

                return genResponseId(_id)
        else:
            return genResponseMsg('error','Validation of fields failed')

    def put(self, offerId):
        data = request.get_json()
        mongo.db.offers.update({'_id': ObjectId(offerId)}, {'$set': data})
        return genResponseMsg('ok','updated')

    def delete(self, offerId):
        mongo.db.offers.remove({'_id': ObjectId(offerId)})
        return genResponseMsg('ok', 'deleted')
