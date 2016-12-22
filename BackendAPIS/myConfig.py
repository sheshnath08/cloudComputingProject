from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

#database name
app.config["MONGO_DBNAME"] = "students_db"
mongo = PyMongo(app, config_prefix='MONGO')
# mongo = MongoClient('mongodb://54.173.234.214/students_db')

APP_URL = "http://0.0.0.0:5000"

