from flask import Blueprint, jsonify, request, render_template
import json

vue_frontend_bp = Blueprint('vue_frontend_bp', __name__, static_folder='static', template_folder='templates')
auctions_api_url = 'http://localhost:5000/api/v1/auctions'

@vue_frontend_bp.route('')
def vue_frontend():
    return render_template('home_vue.html')