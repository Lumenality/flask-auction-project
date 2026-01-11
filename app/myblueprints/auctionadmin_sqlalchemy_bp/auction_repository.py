# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Optional, List

# Create a Base class to define database models
Base = declarative_base()

# Define an Auction model that represents the 'auctions' table in the database
class Auction(Base):
    __tablename__ = 'auctions'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    starting_bid = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    image_url = Column(String(128), nullable=True)

# Define a class to handle database operations for the Auction model 
class AuctionRepository:
    def __init__(self, db_uri: str = 'sqlite:///auctions_sqlalchemy.db'):
        # Initialize the database connection
        self.engine: create_engine = create_engine(db_uri)
        self.Session: sessionmaker = sessionmaker(bind=self.engine)
        self.file_name = file_name
        # Create tables if they don't exist
        try:
            Base.metadata.create_all(self.engine)
        except OperationalError:
            pass
        ####
        #Base.metadata.create_all(self.engine, checkfirst=True)

        # If the database is empty, populate it with sample data
        if not self.get_all():
            self.add(1, "Skriet", 5, "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_Scream.jpg/256px-The_Scream.jpg?20160501101333")
            self.add(2, "Mona Lisa", 10, "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mona_Lisa.jpg/256px-Mona_Lisa.jpg?20100608143407")

    def add(self, id: int, description: str, starting_bid: int, duration:int, image_url: Optional[str] = None) -> None:
        # Add a new auction to the database
        session = self.Session()
        auction = Auction(
            id=id,
            description=description,
            starting_bid=starting_bid,
            duration=duration,
            image_url=image_url)
        session.add(auction)
        session.commit()
        return auction
    
    def find_by_id(self, auction_id: int) -> Optional[Auction]:
        with self.Session() as session:
            # Query the database for an auction with the specified ID
            return session.query(Auction).filter_by(id=auction_id).first()
    
    def update(self, id: int, description: str, starting_bid: int, duration:int, image_url: Optional[str] = None) -> Optional[Auction]:
        with self.Session() as session:
            # Find the auction to update
            auction = session.query(Auction).filter_by(id=id).first()
            if auction:
                # Update the auction's details
                if description is not None:
                    auction.description = description
                if starting_bid is not None:
                    auction.starting_bid = starting_bid
                if duration is not None:
                    auction.duration = duration
                if image_url is not None:
                    auction.image_url = image_url
                session.commit()
    
    def delete(self, auction_id: int) -> None:
        with self.Session() as session:
            # Find the auction to delete
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if auction:
                # Delete the auction from the database
                session.delete(auction)
                session.commit()

    def get_all(self) -> List[Auction]:
        with self.Session() as session:
            # Retrieve all auctions from the database
            return session.query(Auction).all()