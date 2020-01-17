
from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from db import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    card = Column(Integer, unique=True)
    flower_id = Column(Integer, ForeignKey('flowers.id'))

    flower = relationship("Flower")
    accesses = relationship("Access", backref="users")

    def __init__(self, card, flower):
        self.card = card
        self.flower = flower

    def __repr__(self):
        return '<User: %r %r>' % (self.id, self.card)

class Access(Base):
    __tablename__ = 'accesses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    accessed_at = Column(Date, default= lambda : datetime.datetime.now())

    def __repr__(self):
         return '<Access: %r %r>' % (self.id, self.user_id)

class Flower(Base): 
    __tablename__ = 'flowers'
    
    id = Column(Integer, primary_key=True)
    port = Column(Integer)
    active = Column(Boolean, default=True)
    priority = Column(Integer)

    def __init__(self, port, active, priority):
        self.port = port
        self.active = active
        self.priority = priority


    def __repr__(self):
         return '<Flower: %r %r>' % (self.id, self.port)
