from app.flask_app import app
from app.models.auction import clear_auctions

with app.app_context():
    clear_auctions()