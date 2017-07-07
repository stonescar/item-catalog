from sqlalchemy import (Column, Integer, String, DateTime,
                        ForeignKey, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    def serialize(self, items):
        return {
            'id': self.id,
            'name': self.name,
            'creator_id': self.user_id,
            'creator_name': self.user.name,
            'items': [i.serialize for i in items]
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(350))
    picture = Column(String())
    time = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'pictureURL': self.picture,
            'creator_id': self.user_id,
            'creator_name': self.user.name
        }


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
