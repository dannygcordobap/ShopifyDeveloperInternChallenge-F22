import os
import certifi
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongodbURI = os.getenv("MONGO_URI")

# Initializing the flask app
server = Flask(__name__)

# Establishing the mongodb client connection
certificate = certifi.where()
mongodb = MongoClient(mongodbURI, tlsCAFile = certificate)

# Importing routes following server initialization
from inventorytracker import routes
