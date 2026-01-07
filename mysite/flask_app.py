from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'af3fc57db372caf31143a78ce9036b955618517ac2855ef73e58df67ae11e51a'
from app import routes