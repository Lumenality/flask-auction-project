from flask import Blueprint, flash, render_template, jsonify, request, redirect, url_for, flash, make_response, current_app, g
import os

from .auction_repo_sqlite_db import AuctionRepository
from .auction import Auction

auctionadmin_bp = Blueprint('auctionadmin_bp', __name__, template_folder='templates')

auction_repo = AuctionRepository('instance/auctionsite.db')

def get_auction_repo() -> AuctionRepository:
    # Ensure ./instance exists and use ./instance/auctionsite.db
    os.makedirs(current_app.instance_path, exist_ok=True)
    db_path = os.path.join(current_app.instance_path, "auctionsite.db")

    if "auction_repo" not in g:
        g.auction_repo = AuctionRepository(db_path)

    return g.auction_repo

@auctionadmin_bp.route('/', methods=['GET'])
def get_all_auctions():
    return redirect(url_for('auctions_bp.our_auctions'))

@auctionadmin_bp.route('/<int:auction_id>', methods=['GET'])
def get_auction_by_id(auction_id):
    auction = auction_repo.find_by_id(auction_id)
    if auction:
        return render_template('auction_details.html', auction=auction)
    return jsonify(message='Auction not found'), 404

'''
@auctionadmin_bp.route('/', methods=['POST'])
def create_auction():
    new_auction_data = request.json
    auction = auction_repository.create_car(new_car_data)
    return jsonify(auction), 201
'''
@auctionadmin_bp.route('/edit/<int:auction_id>', methods=['GET'])
def edit_auction(auction_id):
    auction = auction_repo.find_by_id(auction_id)
    if auction:
        return render_template('edit_auction_form.html', auction=auction)
    return jsonify(message='Auction not found'), 404

@auctionadmin_bp.route('/update', methods=['POST'])
def update_auction():
    #create auction object based on form data
    auction = Auction(request.form.get('id'),
                      request.form.get('description'),
                      request.form.get('starting_bid'),
                      request.form.get('duration'),
                      request.form.get('image_url') or None)
    auction_repo.update(auction)
    if auction:
        flash(f'Auction {auction.id} updated successfully!', 'success')
        return redirect(url_for('auctionadmin_bp.get_all_auctions'))
    return jsonify(message='Auction not found'), 404
    #return "updated"

@auctionadmin_bp.route('/delete/<int:auction_id>', methods=['DELETE', 'GET'])
def delete_auction(auction_id):
    success = auction_repo.delete(auction_id)
    if success:
        flash(f'Auction {auction_id} deleted successfully!', 'success')
        return redirect(url_for('auctionadmin_bp.get_all_auctions'))
    return jsonify(message='Auction not found'), 404

'''
def user_exists():
    list_of_admin_users=[{'username':'admin','password':'123'},{'username':'boss','password':'123'}]
    username = request.authorization.username
    password = request.authorization.password

    user_exists = false

    for user in list_of_admin_users:
        if user['username'] == username and user['password'] == password:
            user_exists = true
            break
    return user_exists
'''

@auctionadmin_bp.route('/add', methods=['GET'])
def add_auction_form():
    return render_template('add_auction_form.html')

@auctionadmin_bp.route('/add', methods=['POST'])
def add_auction():
    auction = Auction(request.form.get('id'),
                      request.form.get('description'),
                      request.form.get('starting_bid'),
                      request.form.get('duration'),
                      request.form.get('image_url') or None)
    auction_repo.add(auction)
    return redirect(url_for('auctionadmin_bp.get_all_auctions'))