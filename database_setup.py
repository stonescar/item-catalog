from sqlalchemy import (Column, Integer, String, DateTime,
                        ForeignKey, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(350))
    picture = Column(String())
    time = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)


if __name__ == '__main__':
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.create_all(engine)
