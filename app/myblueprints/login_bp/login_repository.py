# Import necessary modules from SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from typing import Optional, List
from flask_bcrypt import Bcrypt

# Create a Base class to define database models
Base = declarative_base()
# Initialize Bcrypt
bcrypt = Bcrypt()

# Define a Users model that represents the 'users' table in the database
class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String, default='user')  # 'admin' if admin, 'superuser' if superuser (NOT CURRENTLY IN USE), 'user' otherwise
        
    @property
    def is_admin(self):
        return self.role == 'admin'

# Define a class to handle database operations for the User model
class UserRepository:
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
            self.add('admin', 'admin@example.com', self.hash_password('adminpass'), 'admin')
            self.add('h24sebsk', 'h24sebsk@example.com', self.hash_password('userpass'), 'user')
        
    def hash_password(self, password: str) -> str:
        # Hash the password using bcrypt
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def add(self, username: str, email: str, password_hash: str, role: str = 'user') -> User:
        with self.Session() as session:
            new_user = User(username=username, email=email, password_hash=password_hash, role=role)
            session.add(new_user)
            session.commit()
            return new_user
        
    def get_all(self) -> List[User]:
        with self.Session() as session:
            users = session.query(User).all()
            return users
        
    def find_by_id(self, user_id: int) -> Optional[User]:
        with self.Session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            return user
    def find_by_username(self, username: str) -> Optional[User]:
        with self.Session() as session:
            user = session.query(User).filter_by(username=username).first()
            return user
    def find_by_email(self, email: str) -> Optional[User]:
        with self.Session() as session:
            user = session.query(User).filter_by(email=email).first()
            return user