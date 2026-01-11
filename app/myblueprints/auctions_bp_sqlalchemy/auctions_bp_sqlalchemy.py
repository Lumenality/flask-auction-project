from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, make_response

from .auction_repository import AuctionRepository
# remember to create auctionviews folder under templates folder since we have conflights with the same html file name in
auctions_bp_sqlalchemy = Blueprint('auctions_bp_sqlalchemy', __name__,template_folder='templates')
auctions_repo = AuctionRepository()

@auctions_bp_sqlalchemy.route('/', methods=['GET'])
def get_all_auctions():
    auctions_list = auctions_repo.get_all()
    #return auctions, need to add the subfoldersname, carviews
    return render_template('auctionviews/auctions_bp.html', auctions=auctions_list)

@auctions_bp_sqlalchemy.route('/<int:auction_id>', methods=['GET'])
def get_auction_by_id(auction_id):
    auction = auctions_repo.find_by_id(auction_id)
    if auction:
        return render_template('auctionviews/auction_details_bp.html', auction=auction)
    else:
        return jsonify({"message": "Auction not found"}), 404
    
@auctions_bp_sqlalchemy.route('/edit/<int:auction_id>', methods=['GET'])
def edit_auction(auction_id):
    auction = auctions_repo.find_by_id(auction_id)
    if auction:
        return render_template('auctionviews/edit_auction.html', auction=auction)
    else:
        return jsonify({"message": "Auction not found"}), 404
    
@auctions_bp_sqlalchemy.route('/update', methods=['POST'])
def update_auction(auction_id):
    #create auction object from form data
    auctions_repo.update(
        request.form.get('auction-id'),
        request.form.get('description'),
        float(request.form.get('starting-bid')),
        int(request.form.get('auction-duration')),
        request.form.get('image-url'))
    
    flash(f'You updated the auction with id: {auction_id}.', 'success')
    return redirect(url_for('auctions_bp_sqlalchemy.get_auction_by_id', auction_id=request.form.get('auction-id')))

@auctions_bp_sqlalchemy.route('/<int:auction_id>')
def auction_details(auction_id):
    found_auction = None
    for auction in auctions_repo.get_all():
        if auction.id == auction_id:
            found_auction = auction
            break
    if found_auction:
        return render_template('auctionviews/auction_details_bp.html', auction=found_auction)
    else:
        return 'Auction not found', 404