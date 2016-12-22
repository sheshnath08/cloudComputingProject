from kafka import SimpleProducer, KafkaClient
import json
from Resources.Config import *

class SparkKafkaService:
    producer = None
    topic = None

    def __init__(self):
        kafka = KafkaClient(sparkkafka_ip)
        self.producer = SimpleProducer(kafka)
        self.topic = sparkkafka_topic

    def addMessageToQueue(self,json_msg):
        try:
            self.producer.send_messages(self.topic, json_msg)
        except Exception as e:
            print(e)