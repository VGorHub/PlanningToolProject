from flask import Flask
from flask import render_template
from flask_restful import Api , Resource , reqparse

app = Flask(__name__)
api = Api()
