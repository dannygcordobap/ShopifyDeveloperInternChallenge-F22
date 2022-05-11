import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongodbURI = os.getenv("MONGO_URI")

# Initializing the flask app
server = Flask(__name__)

# Establishing the mongodb client connection
mongodb = MongoClient(mongodbURI)

# Importing routes following server initialization
from inventorytracker import routes
