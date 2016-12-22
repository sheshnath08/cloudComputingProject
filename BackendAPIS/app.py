#!/usr/bin/env python3


from flask_restful import Api

#Custome IMPORTS
from Classes.Users import *
from Classes.Merchants import *
from Classes.Offers import *
from Classes.Claims import *
from Classes.HelperClass import *

class Index(Resource):
    def get(self):
        return {"status":"ok"}

api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Users, "/api/users", endpoint="users")
api.add_resource(Claims, "/api/claims", endpoint="claims")
api.add_resource(Users, "/api/users/<string:userId>", endpoint="userId")
api.add_resource(Merchants, "/api/merchants", endpoint="merchants")
api.add_resource(Merchants, "/api/merchants/<string:merchantId>", endpoint="merchantId")
api.add_resource(Offers, "/api/offers", endpoint="offers")
api.add_resource(Offers, "/api/offers/<string:offerId>", endpoint="offerId")
api.add_resource(HelperClass, "/api/helperclass/buildtrainingdata=<string:buildtrainingdata>", endpoint="buildtrainingdata")
api.add_resource(HelperClass, "/api/helperclass/offermapping=<string:offerMapping>", endpoint="offerMapping")
api.add_resource(HelperClass, "/api/helperclass", endpoint="helperclass")

#PUSH post req from userid for location to SQS
api.add_resource(Users, "/api/users/updateLocation=<string:updateLocation>", endpoint="updateLocation")
#PUT Support for ANDROID
api.add_resource(Users, "/api/users/updateTokenFor=<string:updateTokenFor>", endpoint="updateTokenFor")

#SIGNUPS
api.add_resource(Merchants, "/api/merchants/register=<string:merchantRegister>", endpoint="merchantRegister")
api.add_resource(Users, "/api/users/register=<string:userRegister>", endpoint="userRegister")

#LOGINS
api.add_resource(Users, "/api/users/login/userId=<string:userloginId>", endpoint="userloginId")
api.add_resource(Merchants, "/api/merchants/login/merchantId=<string:merchantloginId>", endpoint="merchantloginId")


#SEARCH USERS BY LOCATION
api.add_resource(Users, "/api/users/location/byLocation=<string:byLocation>", endpoint="byLocation")

#SEARCH MERCHANTS BY LOCATION
api.add_resource(Merchants, "/api/merchants/location/byMerchantLocation=<string:byMerchantLocation>", endpoint="byMerchantLocation")

#VALID OFFFERS
api.add_resource(Offers, "/api/offers/validity=<string:validity>", endpoint="validity")

#GET OFFERS CLAIMED BY A GIVEN USER
api.add_resource(Claims, "/api/claims/userId=<string:claimedOffersForUserId>", endpoint="claimedOffersForUserId")

#GET USERS WHO CLAIMED THE OFFER
api.add_resource(Claims, "/api/claims/offerId=<string:UsersClaimedTheOffer>", endpoint="UsersClaimedTheOffer")

if __name__ == "__main__":
    #Run on localhost
    # app.run(host='127.0.0.1', debug=True, port=5000)
    #Run on Aws instance
    app.run(host='0.0.0.0', debug=True, port=5000)
