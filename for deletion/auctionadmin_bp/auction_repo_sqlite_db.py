import os.path
import sqlite3
from .auction import Auction

class AuctionRepository:
    def __init__(self, file_name: str):
        self.file_name = file_name
        # Skapa databasen om den inte finns
        if not os.path.exists(self.file_name):
            self.__init_auction_sqlite()

    def get_all(self) -> list:
        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM auctions")
        auction_records = cursor.fetchall()

        auctions = []
        for record in auction_records:
            auction = Auction(*record)
            auctions.append(auction)

        conn.close()
        return auctions
    
    def add(self, auction: Auction):
        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO auctions (id, description, starting_bid, duration, image_url)
            VALUES (?, ?, ?, ?, ?)
            ''', (auction.id, auction.description, auction.starting_bid, auction.duration, auction.image_url))
        
        conn.commit()
        conn.close()

    def delete(self, auction_id: int) -> bool:
        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM auctions WHERE id = ?", (auction_id,))

        conn.commit()
        conn.close()
        return True
    
    def update(self, auction: Auction):
        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE auctions
            SET description = ?, starting_bid = ?, starting_duration = ?, image_url = ?
            WHERE id = ?
            ''', (auction.description, auction.starting_bid, auction.duration, auction.image_url, auction.id))
        
        conn.commit()
        conn.close()

    def find_by_id(self, auction_id: int) -> Auction:
        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM auctions WHERE id = ?", (auction_id,))
        auction_record = cursor.fetchone()

        conn.close()

        if auction_record:
            return Auction(*auction_record)
        return None
        
    # Private helper methods
    def __init_auction_sqlite(self):
        # Connects to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()

        # Create the auctions table
        cursor.execute('''
            CREATE TABLE auctions (
                id INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                starting_bid REAL NOT NULL,
                duration INTEGER NOT NULL,
                image_url TEXT
            )
        ''')
        
        # Sample start data
        sample_auctions = [
            Auction(1, "Skriet", 5, "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_Scream.jpg/256px-The_Scream.jpg?20160501101333",2),
            Auction(2, "Mona Lisa", 10, "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mona_Lisa.jpg/256px-Mona_Lisa.jpg?20100608143407",2),
            # Add more auctions here if needed
        ]

        for auction in sample_auctions:
            cursor.execute(
                '''
                INSERT INTO auctions (id, description, starting_bid, duration, image_url)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (auction.id, auction.description, auction.starting_bid, auction.duration, auction.image_url)
            )

        conn.commit()
        conn.close()