from flask import Flask
from sqlalchemy.orm import sessionmaker
from database import engine


app = Flask('item-catalog')

DBsession = sessionmaker(bind=engine)
session = DBsession()
