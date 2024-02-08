from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
# Create engine to connect to PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

