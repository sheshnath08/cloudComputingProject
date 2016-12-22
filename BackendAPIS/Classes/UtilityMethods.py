from flask import jsonify
from bson.objectid import ObjectId

#Checks whether all fields required for table are present
def validateRecord(data,fields):
    for f in fields:
        if data.get(f) == None:
            print(f+" field is missing.")
            return False
    return True

def genResponseMsg(status,msg):
    response = jsonify({
        'status': status,
        'message': msg
    })

    return response

def genResponseId(objId):
    response = jsonify({
        '_id': str(objId)
    })

    return response

