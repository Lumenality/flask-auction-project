from flask import Blueprint, render_template, current_app
import os
from flask import g

from ..auctionadmin_sqlalchemy_bp.auction_repository import AuctionRepository

auctions_bp = Blueprint('auctions_bp', __name__, template_folder='templates')

def get_auctions_from_repo() -> AuctionRepository:
    # Ensure ./instance exists and use ./instance/auctionsite.db
    
    os.makedirs(current_app.instance_path, exist_ok=True)
    db_path = os.path.join(current_app.instance_path, "auctionsite.db")

    if "auction_repo" not in g:
        g.auction_repo = AuctionRepository(db_path)

    auctions_list = g.auction_repo.get_all()
    return auctions_list

@auctions_bp.route('/')  # /auctions/
def our_auctions():
    return render_template('auctions_bp.html', auctions=get_auctions_from_repo())
@auctions_bp.route('/<int:auction_id>')
def auction_details(auction_id):
    found_auction = None
    for auction in get_auctions_from_repo():
          if auction.id == auction_id:
              found_auction = auction
              break
    if found_auction:
        return render_template('auction_details_bp.html', auction=found_auction)
    else:
        return 'Auction not found', 404