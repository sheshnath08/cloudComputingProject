#API Use

#GENERAL SECTION:
    #GELOCATION FIELD:
    # {"location":{"lat":40.12454,"lon":-40.45678}}

    #SAMPLE RECORD
    # data = {"userId":"1","name":"testuser","password":"test1234","category":"cat1","address":"210Hopkins","location":{"lat":40.12454,"lon":-40.45678}}

    # In [1]: from requests import get, post, put, delete

    #json data tuple
    # In [4]: data = {"offerId":"2","merchantId":"1","description":"5%off","validity":"2013-09-28 20:30:55"}

    #insert json data tuple into mongodb
    # In [5]: post("http://127.0.0.1:5000/api/offers", json=data).json()

#USERS SECTION
    #SAMPLE RECORD: { "_id" : ObjectId("58533df136e8b80e043b7e3d"), "password" : "pass1234", "name" : "vivek", "firebaseToken" : "123544", "location" : { "lat" : 34.4, "lon" : 34.4 }, "address" : "Jersey city, NJ" }

    #USER REGISTER
            #input data
            # data = {"name":"shesh","password":"1234567","address":"34street,NJ","lat":'40.12454',"lon":'-40.45678','firebaseToken':"123544"}
            #if record exists: password is updated
                    #repsonse: {"status": "ok", 'message':'pasword updated','_id': '58533df136e8b80e043b7e3d'}
            #else new record is created:
                    #response: {"status": "ok", 'message':'new user inserted','_id': '58533df136e8b80e043b7e3d'}
            #API LINK
            # post("http://127.0.0.1:5000/api/users/register=True", json=data)

    #GET USER WITH ID 58533df136e8b80e043b7e3d
            #get("http://127.0.0.1:5000/api/users/58533df136e8b80e043b7e3d")

    #UPDATE LOCATION OF USER AND PUSH TO USER SQS
            # data={"userId":"58533df136e8b80e043b7e3d","location":{"lat":40.12454,"lon":-40.45678}}
            # post("http://127.0.0.1:5000/api/users/updateLocation=True", json=data)

    #UPDATE FIELD IF EXISTING OTHERWISE ADD NEW FIELDS PASSED IN JSON
            #updateTokenFor is userId
            # data = {'firebaseToken':'123544'}
            # post("http://127.0.0.1:5000/api/users/updateTokenFor=58533df136e8b80e043b7e3d", json=data)
            # RESPONSE: {'status':'ok','message':'updated'}

    #USER LOGIN FOR USERID 58533df136e8b80e043b7e3d
            #URL: get("http://54.161.127.238:5000/api/users/login/userId=58533df136e8b80e043b7e3d")
            #repsonse: {"password":"mypassword", "status":"200"}

    #SEARCH USER BY LOCATION AND MAX DISTANCE RADIUS
            # get("http://127.0.0.1:5000/api/users/location/byLocation=true?lat=37.7577&lon=76.4476&maxdist=5000")


#MERCHANTS SECTION

    #SAMPLE RECORD: { "_id" : ObjectId("5853157536e8b82410e0d200"), "password" : "1234", "location" : { "lat" : "40.22454", "lon" : "-40.25678" }, "address" : "34street", "name" : "Macys" }

    #FIELDS COMPULSORY: ["name", "password", "address", "lat","lon"]

    #MERCHANT REGISTER
        #input data
        # data = {"name":"Target","password":"1234567","address":"34street","lat":'40.12454',"lon":'-40.45678'}
        #if record exists: password is updated
                #repsonse: {"status": "ok", 'message':'pasword updated','_id': '4567879189'}
        #else new record is created:
                #response: {"status": "ok", 'message':'new merchant inserted','_id': '4567879189'}
        #API LINK
        # post("http://127.0.0.1:5000/api/merchants/register=True", json=data)

    #GET MERCHANT WITH ID 4567879189
        #get("http://127.0.0.1:5000/api/merchants/4567879189")

    #MERCHANT LOGIN FOR MERCHANT ID 4567879189
        #URL: http://54.161.127.238:5000/api/merchants/login/merchantId=4567879189
        #if merchant present:
            #repsonse : {"password":"mypassword", "status":"ok"}
        # else: #repsonse : {'status': 404,'message': 'Merchant Not Found '}

    #SEARCH MERCHANTS BY LOCATION AND MAX DISTANCE RADIUS
    # get("http://127.0.0.1:5000/api/merchants/location/byMerchantLocation=true?lat=40.2454&lon=-40.45678&maxdist=5000")
    #SEARCH MERCHANTS BY LOCATION AND MAX DISTANCE RADIUS
    # get("http://127.0.0.1:5000/api/merchants/location/byMerchantLocation=spark?lat=40.2454&lon=-40.45678&maxdist=5000&userId=58533df136e8b80e043b7e3d")

#OFFERS SECTION

    #SAMPLE RECORD: { "_id" : ObjectId("58532e6636e8b80734ef1624"), "validity" : ISODate("2013-09-28T20:30:55Z"), "description" : "5%off", "merchantId" : ObjectId("5853157536e8b82410e0d200") }
    #Input Validity Datetime format: "2013-09-28 20:30:55"

    #CREATE A NEW OFFER:
        #data = {"merchantId":"5853157536e8b82410e0d200","description":"50%off","validity":"2013-09-28 20:30:55"}
        #RESPONSE:
        #IF OFFER EXISTS: #RESPONSE: {"response": "offer already exists."}
        #ELSE:  RESPONSE: {'_id': '4567879189'}

    #GET ALL OFFERS:
        # get("http://127.0.0.1:5000/api/offers")
        #RESPONSE: {'response': [{'_id': '58532e6636e8b80734ef1624', 'name': 'Macys', 'location': {'lon': '-40.25678', 'lat': '40.22454'}, 'merchantId': '5853157536e8b82410e0d200', 'description': '5%off', 'Validity': 'Sat, 28 Sep 2013 20:30:55 GMT'}]}

    #Get offer with offerId = 58532e6636e8b80734ef1624
        # ln [3]: get("http://127.0.0.1:5000/api/offers/58532e6636e8b80734ef1624")
        #RESPONSE: {'data': {'_id': '58532e6636e8b80734ef1624', 'location': {'lon': '-40.25678', 'lat': '40.22454'}, 'merchantName': 'Macys', 'validity': 'Sat, 28 Sep 2013 20:30:55 GMT', 'merchantId': '5853157536e8b82410e0d200', 'description': '5%off'}, 'status': 'ok'}

    # Update offer with offerId = 2
        # In [6]: put("http://127.0.0.1:5000/api/offers/2", json={"description": "10% Off"}).json()

    #Delete offer with offerId =2
        # In [7]: delete("http://127.0.0.1:5000/api/offers/2").json()

    # GET VALID OFFERS AT CURRENT TIME
        # get("http://127.0.0.1:5000/api/offers/validity=now")
    # GET VALID OFFERS AT SPECIFIC TIME
        # get("http://127.0.0.1:5000/api/offers/validity=2013-09-28 20:30:55")
        #RESPONSE: {'response': [{'_id': '58532e6636e8b80734ef1624', 'name': 'Macys', 'location': {'lon': '-40.25678', 'lat': '40.22454'}, 'merchantId': '5853157536e8b82410e0d200', 'description': '5%off', 'Validity': 'Sat, 28 Sep 2013 20:30:55 GMT'}]}


#CLAIMS SECTION

    #SAMPLE RECORD:
    # { "_id" : ObjectId("58539b4b36e8b82504b9cc19"), "offerId" : ObjectId("58532e6636e8b80734ef1624"), "userId" : ObjectId("58533df136e8b80e043b7e3d") }

    # CREATE A CLAIM RECORD:
            # input: data = {'userId':'58533df136e8b80e043b7e3d','offerId':'58532e6636e8b80734ef1624'}
            # API Link: post("http://127.0.0.1:5000/api/claims", json=data)
            # IF RECORD ALREADY EXISTS: RESPONSE: {'Error': 'Record Already Exists.'}
            #ELSE RESPONSE: {'Success': 'Record Inserted.'}

    #GET OFFERS CLAIMED BY A GIVEN USER
        # get("http://127.0.0.1:5000/api/claims/userId=58533df136e8b80e043b7e3d")
        #RESPONSE: list of all offerIds
            # {'response': ['58532e6636e8b80734ef1624','58532e2343324734ef1624']}

    #GET USERS WHO CLAIMED THE OFFER
            # get("http://127.0.0.1:5000/api/claims/offerId=58532e6636e8b80734ef1624")
            #RESPONSE: list of all userIds
                # {'response': ['58532e6636e8b80734ef1624','58532e2343324734ef1624']}

    #GET ALL CLAIMS RECORDS:
            # get("http://127.0.0.1:5000/api/claims")
            #RESPONSE: {'response': [{'offerId': '58532e6636e8b80734ef1624', 'userId': '58533df136e8b80e043b7e3d'}]}


#SPARK

# get("http://127.0.0.1:5000/api/helperclass/buildtrainingdata=true")
# get("http://127.0.0.1:5000/api/helperclass/offermapping=true?userNo=1&offerNo=1")