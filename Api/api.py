from flask import Flask
from flask import Response
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)
