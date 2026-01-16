from flask import Blueprint, flash, jsonify, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..auctions_bp_sqlalchemy.auction_repository import AuctionRepository
import json

vue_frontend_bp = Blueprint('vue_frontend_bp', __name__, template_folder='templates', static_folder='static', static_url_path='/vue_frontend_bp/static')
auctions_repo = AuctionRepository()
auctions_api_url = 'http://127.0.0.1:5000/api/v1/auctions'

@vue_frontend_bp.route('/')
def vue_frontend():
    return render_template('home_vue.html')

@vue_frontend_bp.route('/auctions')
def vue_auctions():
    return render_template('auctions_vue.html')

@vue_frontend_bp.route('/auctions/<int:auction_id>')
def vue_auction_details(auction_id):
    auction = auctions_repo.find_by_id(auction_id)
    if not auction:
        return "Auktion inte hittad", 404
    if len(auction.description) > 20:
        auction_title = auction.description[:20] + "..."
    else:
        auction_title = auction.description
    return render_template('auction_details_vue.html', auction_id=auction_id, auction_title=auction_title)

@vue_frontend_bp.route('/user')
@login_required
def user_page():
    if not current_user.is_authenticated:
        flash('Du måste vara inloggad för att se din sida.', 'warning')
        return redirect(url_for('login_bp.login'))
    if current_user.is_authenticated and current_user.is_admin:
        flash('Administratörer har ingen användarsida.', 'warning')
        return redirect(url_for('admin'))
    user_auctions = auctions_repo.get_all_for_user(current_user.id)
    json_auctions = []
    for auction in user_auctions:
        json_auctions.append({
            'id': auction.id,
            'description': auction.description,
            'starting_bid': auction.starting_bid,
            'highest_bid': auction.highest_bid,
            'end_time': auction.end_time.isoformat() if auction.end_time else None,
            'image_url': auction.image_url
        })
    print(f'Json auctions are: {json_auctions}')
    return render_template('user_page_vue.html', user_auctions=json_auctions)