from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dataclasses import dataclass
from pydantic import BaseModel

Base = declarative_base()

#Creating a class for URL data
@dataclass
class URLShortener(Base):
    __tablename__ = "urls"

    short_url: str = Column(String, primary_key=True)
    original_url: str = Column(String)
    hits: int = Column(Integer)

# engine = create_engine("sqlite:///urls.db", echo=True)  
# # Base.metadata.create_all(bind=engine, checkfirst=True)

# Session = sessionmaker(bind=engine)
# session = Session()

# urls = session.query(URLShortener).all()

# for url in urls: 
#     print(url)






