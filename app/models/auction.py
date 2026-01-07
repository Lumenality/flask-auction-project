# dbrepositories/models/auction.py
"""
🏠 AUCTION-MODELL - Beskriver hur en auktion ser ut i databasen (Schema Definition).

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera strukturen på 'auctions'-tabellen (kolumner, datatyper).
2. Tillhandahålla startdata (seeding data) för att fylla databasen vid första körningen.

OBS! Denna fil har INGEN affärslogik, rutter eller CRUD-operationer!
Den sköts av AuctionRepository.
"""
# Importera 'db' som är instansen av SQLAlchemy (eller Flask-SQLAlchemy)
from ..database import db
# Importera nödvändiga funktioner (i detta fall, inga extra behövs)


class Auction(db.Model):
    """
    Auction-modellen representerar EN auktion i databasen.
    Ärver från db.Model för att få alla ORM-funktionaliteter.

    Varje rad i tabellen 'auctions' blir ett Auction-objekt i Python.
    """
    # Berättar för SQLAlchemy vilket tabellnamn vi vill ha i databasen
    __tablename__ = 'auctions'

    # -----------------------------------------------------------------
    # KOLUMNDELAR (Tabellschema)
    # -----------------------------------------------------------------
    # id: Primärnyckel (unikt ID)
    id = db.Column(db.Integer, primary_key=True)
    
    # description: Sträng (max 500 tecken), MÅSTE fyllas i (nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    # starting_bid: int (max 9 siffror), MÅSTE fyllas i
    starting_bid = db.Column(db.Integer, nullable=False)
    
    # auction_duration: Sparas som int motsvarande antal dagar, MÅSTE fyllas i
    auction_duration = db.Column(db.Integer, nullable=False)
    
    # image_url: Sträng (max 1000 tecken), KAN vara NULL (frivillig)
    image_url = db.Column(db.String(1000), nullable=True)

    # -----------------------------------------------------------------
    # RELATIONER (Läggs till senare om Bostad har FK till t.ex. Mäklare)
    # -----------------------------------------------------------------
    
    def __repr__(self):
        """
        Denna metod definierar hur objektet visas när vi printar det (används för debugging).
        Ger en läsbar representation av objektet.
        """
        return f'<Auction for {self.description}, {self.starting_bid}, {self.auction_duration} days>'


# ============================================================
# STARTDATA (Seeding Data)
# ============================================================

STARTDATA_AUCTIONS = [
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
]


def create_start_auctions():
    """
    Funktion som körs för att säkerställa att tabellen 'bostader' har grunddata.
    Lägger till startdata i databasen ENDAST OM tabellen är tom.
    """
    # Använder Repository-logik (men koden finns i modellen)
    # 1. Fråga databasen hur många rader som finns
    antal_auctions = Auction.query.count()

    if antal_auctions == 0:
        print("📦 Lägger till startdata för auktioner...")

        # 2. Skapa ett Auction-objekt för varje dictionary i listan
        for data in STARTDATA_AUCTIONS:
            new_auction = Auction(
                description=data['description'],
                starting_bid=data['starting_bid'],
                auction_duration=data['auction_duration'],
                image_url=data.get('image_url')
            )
            db.session.add(new_auction) # Lägger till objektet i transaktionen

        # 3. Spara alla nya objekt permanent till databasen
        db.session.commit()
        print(f"✓ Lade till {len(STARTDATA_AUCTIONS)} auktioner")
    else:
        print(f"✓ Tabellen 'auctions' har redan {antal_auctions} rader. Ingen startdata lades till.")

def clear_auctions():
    """
    Tar bort alla rader från tabellen 'auctions'.
    För användning vid testning eller återställning av databasen.
    """
    num_deleted = Auction.query.delete()
    db.session.commit()
    print(f"🗑️  Tog bort {num_deleted} auktioner från databasen.")