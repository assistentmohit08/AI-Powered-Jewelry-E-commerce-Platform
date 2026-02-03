from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import SQLALCHEMY_DATABASE_URI

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String)
    metal_type = Column(String)
    price = Column(Float)
    occasion = Column(String)
    style = Column(String)
    image_url = Column(String)
    description = Column(Text)
    popularity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    interactions = relationship('Interaction', back_populates='product')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'metal_type': self.metal_type,
            'price': self.price,
            'occasion': self.occasion,
            'style': self.style,
            'image_url': self.image_url,
            'description': self.description,
            'popularity': self.popularity
        }


class UserSession(Base):
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, unique=True, nullable=False)
    budget_min = Column(Float)
    budget_max = Column(Float)
    metal_type = Column(String)
    occasion = Column(String)
    style = Column(String)
    category = Column(String)
    conversation_state = Column(String, default='started')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship('ConversationHistory', back_populates='session')
    interactions = relationship('Interaction', back_populates='session')
    
    def to_dict(self):
        return {
            'session_id': self.session_id,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'metal_type': self.metal_type,
            'occasion': self.occasion,
            'style': self.style,
            'category': self.category,
            'conversation_state': self.conversation_state
        }


class ConversationHistory(Base):
    __tablename__ = 'conversation_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey('user_sessions.session_id'), nullable=False)
    message = Column(Text)
    sender = Column(String)  # 'user' or 'bot'
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    session = relationship('UserSession', back_populates='conversations')
    
    def to_dict(self):
        return {
            'message': self.message,
            'sender': self.sender,
            'timestamp': self.timestamp.isoformat()
        }


class Interaction(Base):
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey('user_sessions.session_id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    action_type = Column(String)  # 'view', 'click', 'like', 'add_to_cart'
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship('UserSession', back_populates='interactions')
    product = relationship('Product', back_populates='interactions')
    
    def to_dict(self):
        return {
            'session_id': self.session_id,
            'product_id': self.product_id,
            'action_type': self.action_type,
            'timestamp': self.timestamp.isoformat()
        }


# Database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Session will be closed by caller
