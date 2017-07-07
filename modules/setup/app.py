from flask import Flask
from sqlalchemy.orm import sessionmaker
from database_setup import engine


app = Flask('item-catalog')

DBsession = sessionmaker(bind=engine)
session = DBsession()
