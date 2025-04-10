from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float,DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
 
 

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    rating = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE") ,nullable=False)
    owner=relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 





class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)