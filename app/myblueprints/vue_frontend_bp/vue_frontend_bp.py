from flask import Blueprint, jsonify, request, render_template
import json

vue_frontend_bp = Blueprint('vue_frontend_bp', __name__, template_folder='templates', static_folder='static', static_url_path='/vue_frontend_bp/static')
auctions_api_url = 'http://localhost:5000/api/v1/auctions'

@vue_frontend_bp.route('/')
def vue_frontend():
    return render_template('home_vue.html')

@vue_frontend_bp.route('/auctions')
def vue_auctions():
    return render_template('auctions_vue.html')

@vue_frontend_bp.route('/user_page')
def user_page():
    return render_template('user_page_vue.html')