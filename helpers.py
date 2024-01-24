from models import Base, URLShortener
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import random
import string
import os

#Random url generator
def generateRandomString():
    characters = ''.join([string.ascii_letters, string.digits])
    key = ""
    for i in range(3):
        random_char = random.choice(characters)
        key += random_char
    return key

def create_session():
    # Check if 'urls.db' exists in the volume
    db_file_path = '/data/urls.db'

    if os.path.exists(db_file_path):
        engine = create_engine(f'sqlite:///{db_file_path}', echo=True)
    else:
        # Create a new database and initialize tables
        engine = create_engine(f'sqlite:///{db_file_path}', echo=True)
        Base.metadata.create_all(bind=engine, checkfirst=True)

    Session = sessionmaker(bind=engine)
    return Session()

#Check if the random url generated already exists -> if yes, regenerate
def shortURLExists(session, new_short_url):
    result = session.query(URLShortener).filter_by(short_url=new_short_url).first()
    return result is not None

#Check if original url already in DB -> if yes, return details and increment hit
def originalURLExists(new_original_url):
    session = create_session()
    result = session.query(URLShortener).filter_by(original_url=new_original_url).first()
    session.close()
    return result if result else False

def incrementHit(session, new_original_url):
    result = session.query(URLShortener).filter_by(original_url=new_original_url).first()
    if result:
        result.hits+=1
        session.commit()
    else:
        print(f"Entry with short_url {new_original_url} not found")

def getHits(new_short_url):
    session = create_session()
    result = session.query(URLShortener).filter_by(short_url= new_short_url).first()
    session.close()
    return result

def addNewURL(session, new_short_url, new_original_url):
    newURL = URLShortener(short_url=new_short_url, original_url=new_original_url, hits=1)
    session.add(newURL)
    session.commit()

def handle_short_url(short_url):
    session = create_session()
    result = session.query(URLShortener).filter_by(short_url=short_url).first()
    session.close()
    return result and result.original_url or None

def handleNewURL(new_url):
    #check if already exists in db
    existing_url = originalURLExists(new_url)
    session = create_session()
    if (existing_url==False):
        #new url, generate a random short url for it
        new_short_url = generateRandomString()
        #check if random url not generated before
        while(shortURLExists(session,new_short_url)):
            new_short_url = generateRandomString()
        
        #add new random url and original to db
        addNewURL(session, new_short_url, new_url) 
        session.close()
        return new_short_url
    else:
        incrementHit(session, new_url)
        session.close()
        return existing_url.short_url
    
        