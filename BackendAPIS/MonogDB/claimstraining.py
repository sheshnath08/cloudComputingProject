#Custome Imports
from myConfig import *

outFile = open('trainingFile.csv','w')

# f = open('claims.json')
# for line in f:
#     line = line.strip('\n')
#     line = line.strip(' ')
#     try:
#         line = line.split(':')
#         if line[0] == 'offerId':
#             offerId = line[1]
#         elif line[0] == 'userId':
#             userId = line[1]
#             outLine = (userId + ',' + offerId+'\n')
#             outLine.strip(' ')
#             outFile.write(outLine)
#     except:
#         continue

def getUserIds():
    cursor = mongo.db.users.find({}, {"update_time": 0}).limit(10)
    userIdList = []
    for user in cursor:
        user['_id'] = str(user['_id'])


getUserIds()