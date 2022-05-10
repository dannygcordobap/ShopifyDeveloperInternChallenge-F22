import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongodbURI = os.getenv("MONGO_URI")

server = Flask(__name__)

mongodb = MongoClient(mongodbURI)

from inventorytracker import routes
