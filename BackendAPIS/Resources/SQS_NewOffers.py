import boto.sqs
from boto.sqs.message import RawMessage
import json
from Resources.Config import *

class SQS_NewOffers:
    q = None

    def __init__(self):
        conn = boto.sqs.connect_to_region(REGION,aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        self.q = conn.create_queue('NewOffersQueue')

    def addMessageToQueue(self,json_msg):
        m = RawMessage()
        m.set_body(json.dumps(json_msg))
        self.q.write(m)