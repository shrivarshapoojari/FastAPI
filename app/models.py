from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float



class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    published = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)