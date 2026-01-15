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
            'highest_bid': auction.highest_bid,
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
        'highest_bid': auction.highest_bid,
        'duration': auction.duration,
        'image_url': auction.image_url,
        'likes': auction.likes,
        'dislikes': auction.dislikes
    }
    return jsonify(auction_data), 200

@auctions_bp_rest.route('/<int:auction_id>/bids', methods=['GET'])
# def get_auction_bids(auction_id):
#     """Hämtar alla bud för en specifik auktion."""
#     auction = auctions_repo.find_by_id(auction_id)
    
#     if not auction:
#         return jsonify({'error': 'Auktion inte hittad'}), 404
    
#     bids = auctions_repo.get_bids_for_auction(auction_id)
#     bids_list = []
#     for bid in bids:
#         bids_list.append(
#         {
#             'id': bid.id,
#             'auction_id': bid.auction_id,
#             'user_id': bid.user_id,
#             'amount': bid.amount,
#             'created_at': bid.created_at
#         })

#     return jsonify(bids_list), 200

# We only ever need the two highest bids for an auction
# so we limit the number of bids returned to 2
def get_two_highest_auction_bids(auction_id):
    """Hämtar de två högsta buden för en specifik auktion."""
    auction = auctions_repo.find_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': 'Auktion inte hittad'}), 404
    
    bids = auctions_repo.get_highest_bids_for_auction(auction_id)
    bids_list = []
    for bid in bids:
        bids_list.append(
        {
            'id': bid.id,
            'auction_id': bid.auction_id,
            'user_id': bid.user_id,
            'amount': bid.amount,
            'created_at': bid.created_at
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
    
    if bid_amount <= auction.highest_bid:
        return jsonify({'error': 'Budet måste vara högre än nuvarande bud'}), 400
    
    new_bid = auctions_repo.add_bid(auction_id, current_user.id, bid_amount)
    print(current_user.id)
    bid_data = {
        'id': new_bid.id,
        'auction_id': new_bid.auction_id,
        'user_id': new_bid.user_id,
        'amount': new_bid.amount,
        'created_at': new_bid.created_at
    }
    
    return jsonify(bid_data), 201

@auctions_bp_rest.route('/<int:auction_id>/like', methods=['POST'])
@login_required
def like_auction(auction_id):
    """Ökar antal likes för en auktion."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 401
    auction = auctions_repo.find_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': 'Auktion inte hittad'}), 404
    
    #toggle likes (if user has liked before, removes like)
    auctions_repo.toggle_like_dislike(current_user.id, auction_id, like=True)
    updated_auction = auctions_repo.find_by_id(auction_id)
    
    return jsonify({
        'id': updated_auction.id,
        'likes': updated_auction.likes,
        'dislikes': updated_auction.dislikes
    }), 200

@auctions_bp_rest.route('/<int:auction_id>/dislike', methods=['POST'])
@login_required
def dislike_auction(auction_id):
    """Ökar antal dislikes för en auktion."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 401
    auction = auctions_repo.find_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': 'Auktion inte hittad'}), 404
    
    #toggle dislikes (if user has disliked before, removes dislike)
    auctions_repo.toggle_like_dislike(current_user.id, auction_id, like=False)
    updated_auction = auctions_repo.find_by_id(auction_id)
    
    return jsonify({
        'id': updated_auction.id,
        'likes': updated_auction.likes,
        'dislikes': updated_auction.dislikes
    }), 200