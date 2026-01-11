from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from .auction_repository import AuctionRepository
# remember to create auctionviews folder under templates folder since we have conflights with the same html file name in
auctions_bp_sqlalchemy = Blueprint('auctions_bp_sqlalchemy', __name__,template_folder='templates')
auctions_repo = AuctionRepository()

# ---------------------- Auction Routes ------------------ #
@auctions_bp_sqlalchemy.route('/', methods=['GET'])
def get_all_auctions():
    auctions_list = auctions_repo.get_all()
    return render_template('auctions_bp.html', auctions=auctions_list)

@auctions_bp_sqlalchemy.route('/<int:auction_id>', methods=['GET'])
def get_auction_by_id(auction_id):
    auction = auctions_repo.find_by_id(auction_id)
    if auction:
        bids = auctions_repo.get_bids_for_auction(auction_id)
        return render_template('auction_details_bp.html', auction=auction, bids=bids)
    else:
        return jsonify({"message": "Auction not found"}), 404
    
@auctions_bp_sqlalchemy.route('/add', methods=['GET'])
def add_auction_form():
    return render_template('add_auction_form.html')

@auctions_bp_sqlalchemy.route('/add', methods=['POST'])
def add_auction():
    # Get the highest current auction ID and increment by 1 for the new auction
    highest_id = max([auction.id for auction in auctions_repo.get_all()], default=0)
    new_id = highest_id + 1
    auctions_repo.add(
        new_id,
        request.form.get('description'),
        int(request.form.get('starting_bid')),
        int(request.form.get('duration')),
        request.form.get('image_url'))
    flash(f'You added a new auction with id: {new_id}.', 'success')
    return redirect(url_for('auctions_bp_sqlalchemy.get_all_auctions'))
    
@auctions_bp_sqlalchemy.route('/edit/<int:auction_id>', methods=['GET'])
def edit_auction(auction_id):
    auction = auctions_repo.find_by_id(auction_id)
    if auction:
        return render_template('edit_auction_form.html', auction=auction)
    else:
        return jsonify({"message": "Auction not found"}), 404
    
@auctions_bp_sqlalchemy.route('/update/<int:auction_id>', methods=['POST'])
def update_auction(auction_id):
    #create auction object from form data
    auctions_repo.update(
        auction_id,
        request.form.get('description'),
        float(request.form.get('starting_bid')),
        int(request.form.get('duration')),
        request.form.get('image_url'))
    
    flash(f'You updated the auction with id: {auction_id}.', 'success')
    return redirect(url_for('auctions_bp_sqlalchemy.get_auction_by_id', auction_id=auction_id))

@auctions_bp_sqlalchemy.route('/delete/<int:auction_id>', methods=['GET','POST'])
@login_required
def delete_auction(auction_id):
    if current_user.is_admin:
        if not auctions_repo.find_by_id(auction_id):
            return jsonify({"message": "Auction not found"}), 404
        auctions_repo.delete(auction_id)
        flash(f'You deleted the auction with id: {auction_id}.', 'success')
        return redirect(url_for('auctions_bp_sqlalchemy.get_all_auctions'))
    else:
        return jsonify({"message": "You are not authorized to delete auctions."}), 403
    
# ---------------------- End of Auction Routes ------------------ #

# --------------------------- Like routes ----------------------- #
@auctions_bp_sqlalchemy.route('/like/<int:auction_id>', methods=['POST'])
def like_auction(auction_id):
    # Placeholder function to handle liking an auction
    if current_user.is_authenticated:
        auctions_repo.increment_likes_for_auction(auction_id)
        return redirect(url_for('auctions_bp_sqlalchemy.get_auction_by_id', auction_id=auction_id))
    else:
        flash("You must be logged in to dislike an auction.", "error")
        return redirect(url_for('login_bp.login'))

@auctions_bp_sqlalchemy.route('/dislike/<int:auction_id>', methods=['POST'])
def dislike_auction(auction_id):
    # Placeholder function to handle disliking an auction
    if current_user.is_authenticated:
        auctions_repo.increment_dislikes_for_auction(auction_id)
        return redirect(url_for('auctions_bp_sqlalchemy.get_auction_by_id', auction_id=auction_id))
    else:
        flash("You must be logged in to dislike an auction.", "error")
        return redirect(url_for('login_bp.login'))
    
# ------------------------- End of Functions --------------------- #

# -------------------------- Auction Routes ---------------------- #
@auctions_bp_sqlalchemy.route('/<int:auction_id>/bids/add', methods=['GET'])
def add_bid_form(auction_id):
    auction = auctions_repo.find_by_id(auction_id)
    if not auction:
        return jsonify({"message": "Auction not found"}), 404

    highest = auctions_repo.get_highest_bid_amount(auction_id)
    suggested_amount = (highest + 1) if highest is not None else (int(auction.starting_bid) + 1)

    return render_template(
        'add_bid_form.html',
        auction_id=auction_id,
        suggested_amount=suggested_amount
    )

@auctions_bp_sqlalchemy.route('/<int:auction_id>/bids/add', methods=['POST'])
def add_bid(auction_id):
    if current_user.is_authenticated:
        username = getattr(current_user, "username", None) or str(current_user.get_id())
        highest = auctions_repo.get_highest_bid_amount(auction_id)
        if highest is not None and int(request.form.get('amount')) <= highest:
            flash(f'Your bid must be higher than the current highest bid of {highest}.', 'error')
            return redirect(url_for('auctions_bp_sqlalchemy.add_bid_form', auction_id=auction_id))
        
        auctions_repo.add_bid(
            auction_id,
            username,
            int(request.form.get('amount'))
        )
    else:
        flash("You must be logged in to place a bid.", "error")
        return redirect(url_for('login_bp.login'))

    flash(f'You placed a bid of {request.form.get("amount")} on auction with id: {auction_id}.', 'success')
    return redirect(url_for('auctions_bp_sqlalchemy.get_auction_by_id', auction_id=auction_id))
# ------------------------ End of Bid Routes --------------------- #