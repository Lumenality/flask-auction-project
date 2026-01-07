from flask import Blueprint, render_template
auctions_bp = Blueprint('auctions_bp', __name__, template_folder='templates')

# Define som sample auction data
auctions_list = [
    {
        'id': 1,
        'description': 'Skriet',
        'starting_bid': 5,
        'auction_duration': 7,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_Scream.jpg/256px-The_Scream.jpg?20160501101333'
    },
    {
        'id': 2,
        'description': 'Mona Lisa',
        'starting_bid': 10,
        'auction_duration': 7,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mona_Lisa.jpg/256px-Mona_Lisa.jpg?20100608143407'
    }
    # Add more auctions here
]

@auctions_bp.route('/')#..../auctions/
def our_auctions():
        return render_template('auctions_bp.html', auctions=auctions_list)

@auctions_bp.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    found_auction = None
    for auction in auctions_list:
          if auction['id'] == auction_id:
              found_auction = auction
              break
    if found_auction:
        return render_template('auction_details_bp.html', auction=found_auction)
    else:
        return 'Auction not found', 404