# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask_login import login_required, current_user
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
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    bids = relationship("Bid", back_populates="auction", cascade="all, delete-orphan")

# Define a Bid model that represents the 'bids' table in the database
class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False)

    # Keep it simple for now (matches your “username” idea).
    # Better long-term: store user_id and relate to a User table.
    username = Column(String(80), nullable=False)

    amount = Column(Integer, nullable=False)  # or Float, but Integer is simpler for currency-like bids
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    auction = relationship("Auction", back_populates="bids")

# Define a UserLikesDislikes model that represents the 'user_likes_dislikes' table in the database
# This table tracks which users have liked or disliked which auctions
class UserLikesDislikes(Base):
    __tablename__ = "user_likes_dislikes"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False)
    liked = Column(Integer, default=0)    # 1 if liked, 0 otherwise
    disliked = Column(Integer, default=0) # 1 if disliked, 0 otherwise

# Define a class to handle database operations for the Auction model 
class AuctionRepository:
    def __init__(self, db_uri: str = 'sqlite:///auctions_sqlalchemy.db'):
        # Initialize the database connection and session factory
        self.engine: create_engine = create_engine(db_uri)
        self.Session: sessionmaker = sessionmaker(bind=self.engine)

        # Create tables if they don't exist
        try:
            Base.metadata.create_all(self.engine)
        except OperationalError:
            pass
        ####
        #Base.metadata.create_all(self.engine, checkfirst=True)

        # If the database is empty, populate it with sample data
        if not self.get_all():
            # id, description, starting_bid, duration, image_url, likes, dislikes
            self.add(1, "Skriet", 10000, 5, "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_Scream.jpg/256px-The_Scream.jpg?20160501101333",0,0)
            self.add(2, "Mona Lisa", 10000, 7,"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mona_Lisa.jpg/256px-Mona_Lisa.jpg?20100608143407",0,0)

    def add(self, id: int, description: str, starting_bid: int, duration:int, image_url: Optional[str] = None, likes=0, dislikes=0) -> None:
        # Add a new auction to the database
        session = self.Session()
        auction = Auction(
            id=id,
            description=description,
            starting_bid=starting_bid,
            duration=duration,
            image_url=image_url,
            likes=likes,
            dislikes=dislikes
        )
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
    
    # Methods to handle likes and dislikes
    def increment_likes_for_auction(self, auction_id):
        with self.Session() as session:
            # Find the auction to increment likes
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if auction:
                auction.likes += 1
                session.commit()
                return auction.likes
            else:
                return None
    def increment_dislikes_for_auction(self, auction_id):
        with self.Session() as session:
            # Find the auction to increment dislikes
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if auction:
                auction.dislikes += 1
                session.commit()
                return auction.dislikes
            else:
                return None
            
    def decrement_likes_for_auction(self, auction_id):
        with self.Session() as session:
            # Find the auction to decrement likes
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if auction and auction.likes > 0:
                auction.likes -= 1
                session.commit()
                return auction.likes
            else:
                return None      
    def decrement_dislikes_for_auction(self, auction_id):
        with self.Session() as session:
            # Find the auction to decrement dislikes
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if auction and auction.dislikes > 0:
                auction.dislikes -= 1
                session.commit()
                return auction.dislikes
            else:
                return None
    
    def has_user_liked_auction(self, username: str, auction_id: int) -> bool:
        with self.Session() as session:
            # Check if the user has liked the auction
            print(f"Checking if user {username} has liked auction {auction_id}")
            return None
    def has_user_disliked_auction(self, username: str, auction_id: int) -> bool:
        with self.Session() as session:
            # Check if the user has disliked the auction
            print(f"Checking if user {username} has disliked auction {auction_id}")
            return None
        
    def add_bid(self, auction_id: int, username: str, amount: int) -> Optional[Bid]:
        with self.Session() as session:
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if not auction:
                return None

            bid = Bid(auction_id=auction_id, username=username, amount=amount)
            session.add(bid)
            session.commit()
            session.refresh(bid)
            return bid

    def get_bids_for_auction(self, auction_id: int) -> List[Bid]:
        with self.Session() as session:
            return (
                session.query(Bid)
                .filter(Bid.auction_id == auction_id)
                .order_by(Bid.created_at.desc())
                .all()
            )
        
    def get_highest_bid_amount(self, auction_id: int) -> Optional[int]:
        with self.Session() as session:
            highest = (
                session.query(func.max(Bid.amount))
                .filter(Bid.auction_id == auction_id)
                .scalar()
            )
            return highest  # None if no bids yet
        
    def delete_bid(self, bid_id: int) -> None:
        # If the user is authorized to delete the bid (admin)
        if current_user.is_authenticated and getattr(current_user, "role", None) == 'admin':
            with self.Session() as session:
                bid = session.query(Bid).filter_by(id=bid_id).first()
                if bid:
                    session.delete(bid)
                    session.commit()