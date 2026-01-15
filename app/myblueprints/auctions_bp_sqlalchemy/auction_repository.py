# Import necessary modules from SQLAlchemy
from sqlalchemy import Boolean, create_engine, Column, Integer, String, Float
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask_login import login_required, current_user
from typing import Optional, List

# Import the User Base from login_repository to share the same Base
from ..login_bp.login_repository import Base, User

# Define an Auction model that represents the 'auctions' table in the database
class Auction(Base):
    __tablename__ = 'auctions'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    starting_bid = Column(Integer, nullable=False)
    highest_bid = Column(Integer, nullable=True)
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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    auction = relationship("Auction", back_populates="bids")
    user = relationship("User")  # Add relationship to User

# Define a UserLikesDislikes model that represents the 'user_likes_dislikes' table in the database
class UserLikesDislikes(Base):
    __tablename__ = "user_likes_dislikes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False)
    liked = Column(Boolean, default=False)    # 1 if liked, 0 otherwise
    disliked = Column(Boolean, default=False) # 1 if disliked, 0 otherwise
    
    user = relationship("User")  # Add relationship to User

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

        # If the database is empty, populate it with sample data
        if not self.get_all():
            # id, description, starting_bid, highest_bid, duration, image_url, likes, dislikes
            self.add(1, "Skriet", 10000, 5, "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_Scream.jpg/256px-The_Scream.jpg?20160501101333",0,0)
            self.add(2, "Mona Lisa", 10000, 7,"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mona_Lisa.jpg/256px-Mona_Lisa.jpg?20100608143407",0,0)

    def add(self, id: int, description: str, starting_bid: int, duration:int, image_url: Optional[str] = None, likes=0, dislikes=0) -> None:
        session = self.Session()
        auction = Auction(
            id=id,
            description=description,
            starting_bid=starting_bid,
            highest_bid=starting_bid,
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
    
    def update(self, id: int, description: str, starting_bid: int, highest_bid: int, duration:int, image_url: Optional[str] = None) -> Optional[Auction]:
        with self.Session() as session:
            # Find the auction to update
            auction = session.query(Auction).filter_by(id=id).first()
            if auction:
                # Update the auction's details
                if description is not None:
                    auction.description = description
                if starting_bid is not None:
                    auction.starting_bid = starting_bid
                if highest_bid is not None:
                    auction.highest_bid = highest_bid
                if duration is not None:
                    auction.duration = duration
                if image_url is not None:
                    auction.image_url = image_url
                session.commit()
    
    def delete(self, auction_id: int) -> None:
        '''Delete an auction by its ID'''
        with self.Session() as session:
            # Find the auction to delete
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if auction:
                # Delete the auction from the database
                session.delete(auction)
                session.commit()

    def get_all(self) -> List[Auction]:
        '''Retrieve all auctions from the database'''
        with self.Session() as session:
            return session.query(Auction).all()
                       
    def toggle_like_dislike(self, user_id: int, auction_id: int, like: bool) -> None:
        ''' Toggle either like or dislike for a user on a specific auction '''
        with self.Session() as session:
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if not auction:
                return

            record = session.query(UserLikesDislikes).filter_by(
                user_id=user_id, 
                auction_id=auction_id
            ).first()
            if not record:
                record = UserLikesDislikes(
                    user_id=user_id,
                    auction_id=auction_id,
                    liked=like,
                    disliked=not like
                )
                if like:
                    auction.likes = auction.likes + 1
                else:
                    auction.dislikes = auction.dislikes + 1
                session.add(record)
            else:
                if like:
                    if record.liked:
                        record.liked = False
                        auction.likes = auction.likes - 1
                    else:
                        record.liked = True
                        auction.likes = auction.likes + 1
                        if record.disliked:
                            record.disliked = False
                            auction.dislikes = auction.dislikes - 1
                else:
                    if record.disliked:
                        record.disliked = False
                        auction.dislikes = auction.dislikes - 1
                    else:
                        record.disliked = True
                        auction.dislikes = auction.dislikes + 1
                        if record.liked:
                            record.liked = False
                            auction.likes = auction.likes - 1

            session.commit()
        
    def add_bid(self, auction_id: int, user_id: int, amount: int) -> Optional[Bid]:
        with self.Session() as session:
            auction = session.query(Auction).filter_by(id=auction_id).first()
            if not auction:
                return None
            if amount <= auction.starting_bid:
                return None
            highest_bid = self.get_highest_bid_amount(auction_id)
            if highest_bid is not None and amount <= highest_bid:
                return None
            bid = Bid(auction_id=auction_id, user_id=user_id, amount=amount)
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
    def get_highest_bids_for_auction(self, auction_id: int, limit: int = 2) -> List[Bid]:
        with self.Session() as session:
            return (
                session.query(Bid)
                .filter(Bid.auction_id == auction_id)
                .order_by(Bid.amount.desc())
                .limit(limit)
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