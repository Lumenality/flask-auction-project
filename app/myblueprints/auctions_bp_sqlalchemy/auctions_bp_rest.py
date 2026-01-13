from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from .auction_repository import AuctionRepository

auctions_bp_rest = Blueprint('auctions_bp_rest', __name__, template_folder='templates', static_folder='static')
auctions_repo = AuctionRepository()

@auctions_bp_rest.route('/', methods=['GET'])
def get_all_auctions():
    """Hämtar alla auktioner och returnerar dem som JSON."""
    auctions = auctions_repo.get_all()
    auctions_list = []
    for auction in auctions:
        auctions_list.append(
        {
            'id': auction.id,
            'description': auction.description,
            'starting_bid': auction.starting_bid,
            'current_bid': auction.current_bid if hasattr(auction, 'current_bid') else auction.starting_bid,
            'duration': auction.duration,
            'image_url': auction.image_url,
            'likes': auction.likes,
            'dislikes': auction.dislikes
        })
    return jsonify(auctions_list), 200

@auctions_bp_rest.route('/<int:auction_id>', methods=['GET'])
def get_auction(auction_id):
    """Hämtar en specifik auktion med dess bud."""
    auction = auctions_repo.find_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': 'Auktion inte hittad'}), 404
    
    auction_data = {
        'id': auction.id,
        'description': auction.description,
        'starting_bid': auction.starting_bid,
        'current_bid': auction.current_bid if hasattr(auction, 'current_bid') else auction.starting_bid,
        'duration': auction.duration,
        'image_url': auction.image_url,
        'likes': auction.likes,
        'dislikes': auction.dislikes
    }
    return jsonify(auction_data), 200

@auctions_bp_rest.route('/<int:auction_id>/bids', methods=['GET'])
def get_auction_bids(auction_id):
    """Hämtar alla bud för en specifik auktion."""
    auction = auctions_repo.find_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': 'Auktion inte hittad'}), 404
    
    bids = auctions_repo.get_bids_for_auction(auction_id)
    bids_list = []
    for bid in bids:
        bids_list.append(
        {
            'id': bid.id,
            'amount': bid.amount,
            'bidder': bid.bidder,
            'timestamp': bid.timestamp.isoformat() if hasattr(bid, 'timestamp') else None
        })

    return jsonify(bids_list), 200

@auctions_bp_rest.route('/<int:auction_id>/bids', methods=['POST'])
@login_required
def place_bid(auction_id):
    """Placerar ett bud på en auktion."""
    auction = auctions_repo.find_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': 'Auktion inte hittad'}), 404
    
    data = request.json
    if not data or 'amount' not in data:
        return jsonify({'error': 'Budbelopp saknas'}), 400
    
    bid_amount = float(data['amount'])
    current_highest = auction.current_bid if hasattr(auction, 'current_bid') else auction.starting_bid
    
    if bid_amount <= current_highest:
        return jsonify({'error': 'Budet måste vara högre än nuvarande bud'}), 400
    
    new_bid = auctions_repo.add_bid(auction_id, current_user.username, bid_amount)
    
    bid_data = {
        'id': new_bid.id,
        'amount': new_bid.amount,
        'bidder': new_bid.bidder,
        'timestamp': new_bid.timestamp.isoformat() if hasattr(new_bid, 'timestamp') else None
    }
    
    return jsonify(bid_data), 201

@auctions_bp_rest.route('/<int:auction_id>/like', methods=['POST'])
def like_auction(auction_id):
    """Ökar antal likes för en auktion."""
    auction = auctions_repo.find_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': 'Auktion inte hittad'}), 404
    
    auctions_repo.like_auction(auction_id)
    updated_auction = auctions_repo.find_by_id(auction_id)
    
    return jsonify({
        'id': updated_auction.id,
        'likes': updated_auction.likes,
        'dislikes': updated_auction.dislikes
    }), 200

@auctions_bp_rest.route('/<int:auction_id>/dislike', methods=['POST'])
def dislike_auction(auction_id):
    """Ökar antal dislikes för en auktion."""
    auction = auctions_repo.find_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': 'Auktion inte hittad'}), 404
    
    auctions_repo.dislike_auction(auction_id)
    updated_auction = auctions_repo.find_by_id(auction_id)
    
    return jsonify({
        'id': updated_auction.id,
        'likes': updated_auction.likes,
        'dislikes': updated_auction.dislikes
    }), 200

@auctions_bp_rest.route('/current_user', methods=['GET'])
def get_current_user():
    """Returnerar information om den nuvarande användaren."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Ej inloggad'}), 401
    
    user_data = {
        'username': current_user.username,
        'email': current_user.email
    }
    return jsonify(user_data), 200

@auctions_bp_rest.route('/vueauctions', methods=['GET'])
def showvue():
    """Visar Vue-auktionssidan."""
    return render_template('vueauctions.html')