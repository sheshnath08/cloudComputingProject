#install PSUTIL
#install urlib

from __future__ import print_function
import sys
from pyspark.streaming import StreamingContext
from pyspark import SparkContext,SparkConf
from pyspark.streaming.kafka import KafkaUtils
import time
from pyspark.mllib.recommendation import ALS,MatrixFactorizationModel, Rating
import math
from requests import get
# from kafka import KafkaProducer, KafkaClient
# import kafka
import json
import boto.sqs
from boto.sqs.message import RawMessage
# import urllib


class SimpleQueueService:
    q = None

    def __init__(self):
        conn = boto.sqs.connect_to_region("us-east-1",aws_access_key_id='####',aws_secret_access_key='###')
        self.q = conn.create_queue('sparkqueue')

    def addMessageToQueue(self,json_msg):
        m = RawMessage()
        m.set_body(json.dumps(json_msg))
        self.q.write(m)

def process(time,rdd):

    trainedModel = MatrixFactorizationModel.load(sc, "target/model/myCollaborativeFilter1")
    # trainedModel.cache()
    print("========= %s =========" % str(time))
    print("Processing RDD")
    sqs = SimpleQueueService()
    if rdd.count() > 0:
        # print(rdd.collect())
        # print("RDD Printed")
        predictions = trainedModel.predictAll(rdd).map(lambda r: ((r[0], r[1]), r[2]))
        # print(predictions.collect())
        # print("PredictionsDone")
        recommendations = predictions.takeOrdered(2, key=lambda x: -x[1])
        # print(recommendations)
        for rec in recommendations:
            userNo = str(rec[0][0])
            offerNo = str(rec[0][1])
            resp = (get("http://54.173.234.214:5000/api/helperclass/offermapping=true?userNo="+userNo+"&offerNo="+offerNo).json())
            sqs.addMessageToQueue(resp)
        print("OKDone")

# def tupprocess(tup):
#     print("Processing tuple")
#     print(tup)
def prepareRDD():
    f=open('trainingData.csv')
    list = []
    for line in f:
        # line = line.decode("utf-8")
        line = line.strip('\n')
        line = line.strip('\r')
        line = line.split(',')
        list.append(line)
    onlineRdd = sc.parallelize(list)
    print(onlineRdd.take(3))
    print("FILERDD formed.")

    return onlineRdd


def trainModel(rdd):
    # global trainedModel
    training_RDD, validation_RDD, test_RDD = rdd.randomSplit([6, 2, 2], seed=0)
    # training_RDD, test_RDD = rdd.randomSplit([8, 2], seed=0)
    validation_for_predict_RDD = validation_RDD.map(lambda x: (x[0], x[1]))
    test_for_predict_RDD = test_RDD.map(lambda x: (x[0], x[1]))

    seed = 5
    iterations = 10
    regularization_parameter = 0.1
    ranks = [4, 8, 12]
    errors = [0,0,0]
    err = 0
    tolerance = 0.02

    min_error = float('inf')
    best_rank = -1
    best_iteration = -1

    for rank in ranks:
        model = ALS.train(training_RDD, rank, seed=seed, iterations=iterations,
                          lambda_=regularization_parameter)
        predictions = model.predictAll(validation_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
        rates_and_preds = validation_RDD.map(lambda r: ((r[0], r[1]), float(r[2]))).join(predictions)
        error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1]) ** 2).mean())
        errors[err] = error
        err += 1
        print('For rank %s the RMSE is %s' % (rank, error))
        if error < min_error:
            min_error = error
            best_rank = rank

    print('The best model was trained with rank %s' % best_rank)

    trainedModel = ALS.train(training_RDD, best_rank, seed=seed, iterations=iterations,
                             lambda_=regularization_parameter)

    return trainedModel
    print('TrainDone')

conf = SparkConf().setAppName("Kafka-Spark")
sc = SparkContext(conf=conf)
ssc=StreamingContext(sc,5)
rdd = prepareRDD()


model = trainModel(rdd)
model.save(sc, "target/model/myCollaborativeFilter1")

topic = 'streamerspark1'
kafkaStream = KafkaUtils.createStream(ssc, '52.90.35.162:2181', "raw-event-streaming-consumer",{topic: 1})  # tried with localhost:2181 too
lines = kafkaStream.map(lambda x: x[1])
small_ratings_data_Dstream = lines.map(lambda line: line.split(",")).map(lambda tokens: (tokens[0], tokens[1])).cache()
small_ratings_data_Dstream.foreachRDD(process)

print("Streaming done:")

ssc.start()
ssc.awaitTermination()
