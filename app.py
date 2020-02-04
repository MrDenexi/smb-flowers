import sys
from time import sleep
from datetime import datetime, timedelta
from random import randint, choice

import asyncio
import concurrent.futures

import RPi.GPIO as GPIO

import pyfirmata

from sqlalchemy import func, text
from sqlalchemy.orm import joinedload

from db.models import User, Access, Flower
from arduino.standbystate import StandbyState
from arduino.loginstate import LoginState
from arduino.registerstate import RegisterState

# main app where all the cool stuff happens
class App:

    def __init__(self, session, reader, board):

        # setting variables
        self.reader = reader
        self.session = session
        self.board = board

        # keeping track of pins using pins attribute
        self.pins = {}

        # setting first current state (standby)
        self.currentState = StandbyState(self)

    # blocking read card, returns id and text of the card when scanned
    def readCard(self):
        return self.reader.read()

    # asynchronous loop
    async def readLoop(self):
        loop = asyncio.get_running_loop()

        while True:
            print("Hold a tag near the reader")

            # await blocking readCard code in parallel thread
            id, text = await loop.run_in_executor(None, self.readCard)
    
            print(id, text)
            
            # go to card scan flow using card id
            self.cardScan(id)

            # sleep to prevent duplicate scans
            await asyncio.sleep(3)

    # main state loop
    async def stateLoop(self):
        while True:
            # run current state
            # (every state returns a result state)
            currentState = self.currentState
            resultState = await currentState.run()
            
            # make resultState currentState if currentState did not change by the readLoop
            if self.currentState is currentState:
                self.currentState = resultState
                print('state did not change')        
    
    # gather read loop and state loop
    async def main(self):
        try: 
            await asyncio.gather(
                self.readLoop(),
                self.stateLoop()
            )
        except:
            # nice cleanup on error
            self.stop()
            raise

    # oh no everything is wrong stop this shit
    def stop(self):
        # rPi gpio cleanup
        GPIO.cleanup()
        
        # set arduino pins to low
        for i in range(2, 14):
            self.board.digital[i].write(0)

        print('Bye bye :)')

    # to be called when a card is scanned
    def cardScan(self, card):
        # find user using card id
        user = self.session.query(User).filter_by(card=card).first() 

        if user:
            # login flow if user is found
            self.userLogin(user)
        else:
            # register if it is  new user
            self.userRegister(card)

    # user login flow (access) (existing user)
    def userLogin(self, user):
        # insert a new access for this user 
        access = Access(user.id)
        self.session.add(access)
        self.session.commit()

        # make currentState the loginstate using this user
        self.currentState = LoginState(self, user)

    # user register flow (existing user)
    def userRegister(self, card):

        # find the least popular flower
        # using least amount of accesses of the last 30 days
        leastPopularFlowerQuery = self.session.query(User, func.count(User.flower_id).label('total') ) \
            .options(joinedload(User.accesses)) \
            .filter(Access.accessed_at > (datetime.today() - timedelta(30))) \
            .group_by(User.flower_id) \
            .order_by(text('total asc')) \
            .first()
        
        if leastPopularFlowerQuery is None:
            # no flower found, just do the first
            print('least popular flower query still none :(')
            leastPopularFlower = self.session.query(Flower).first()
        else:
            # set least popular flower
            print('yay there is a new')
            leastPopularFlowerId = leastPopularFlowerQuery.User.flower_id
            leastPopularFlower = self.session.query(Flower).get(leastPopularFlowerId)
       
        # create a new user, with card and flower
        newUser = User(card, leastPopularFlower)
        self.session.add(newUser)

        # add an access for this user
        newAccess = Access(newUser.id)
        self.session.add(newAccess)

        # commit all
        self.session.commit()
        
        # set state to RegisterState
        self.currentState = RegisterState(self, newUser)
        