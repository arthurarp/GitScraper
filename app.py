import os
from flask import Flask
from pymongo import MongoClient
from controllers.GitController import GitController

app = Flask(__name__)

# client = MongoClient(
#   'mongodb',
#   27017,
#   username=os.environ.get('DATABASE_USER'),
#   password=os.environ.get('DATABASE_PASSWORD')
# )

GitController(app)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000)