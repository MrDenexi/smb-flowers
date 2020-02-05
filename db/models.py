
from sqlalchemy import Column, DateTime, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.db import Base
import datetime

# user model 
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    # card id 
    card = Column(Integer, unique=True)

    # couple user to one flower
    flower_id = Column(Integer, ForeignKey('flowers.id'))
    flower = relationship("Flower")

    # couple accesses (or logins)
    accesses = relationship("Access", backref="user")

    def __init__(self, card, flower):
        self.card = card
        self.flower = flower

    def __repr__(self):
        return '<User: %r %r>' % (self.id, self.card)

# accesses of user (or when a user logins)
class Access(Base):
    __tablename__ = 'accesses'

    id = Column(Integer, primary_key=True)

    # user relationship
    user_id = Column(Integer, ForeignKey('users.id'))

    # set access to now
    accessed_at = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
         return '<Access: %r %r>' % (self.id, self.user_id)

# flower model
class Flower(Base): 
    __tablename__ = 'flowers'

    id = Column(Integer, primary_key=True)

    # port number on arduino
    port = Column(Integer)

    # active (default yes, might be unnecessary)
    active = Column(Boolean, default=True)

    # some priorit to create an order when needed
    priority = Column(Integer)

    def __init__(self, port, active, priority):
        self.port = port
        self.active = active
        self.priority = priority

    def __repr__(self):
         return '<Flower: %r %r>' % (self.id, self.port)
