import sys
from time import sleep
from datetime import datetime, timedelta
from random import randint, choice

import asyncio
import concurrent.futures

import RPi.GPIO as GPIO

import pyfirmata

from sqlalchemy import func, text
from sqlalchemy.orm import joinedload, configure_mappers

from db.models import User, Access, Flower
from arduino.standbystate import StandbyState
from arduino.loginstate import LoginState
from arduino.registerstate import RegisterState

# main app where all the cool stuff happens 
class App:

    def __init__(self, session, reader, board):
        configure_mappers()

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
    async def readLoop(self, task_state):
        
        loop = asyncio.get_running_loop()

        while True:
            print("Hold a tag near the reader")

            # await blocking readCard code in parallel thread
            id, text = await loop.run_in_executor(None, self.readCard)
            task_state.cancel()
    
            print(id, text)
            
            # go to card scan flow using card id
            self.cardScan(id)

            # sleep to prevent duplicate scans
            await asyncio.sleep(3)

            return self.currentState

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
            while True:
                task_state = asyncio.Task(self.stateLoop())
                task_read = asyncio.Task(self.readLoop(task_state))
                await asyncio.gather(
                    task_state,
                    task_read
                )               
        except:
            # nice cleanup on error
            self.stop()
            # start again
            await self.main()
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
        leastPopular = self.session.query(Access, User.flower_id, func.count(User.id).label('total')) \
            .options(joinedload(Access.user)) \
            .filter(Access.accessed_at > (datetime.today() - timedelta(30))) \
            .group_by(User.flower_id) \
            .order_by(text('total asc')) \
            .all()  
        
        print('leastPopular', leastPopular)
        
        # get all flowers
        allFlowers = self.session.query(Flower).all()        

        # get another flower if not all are accessed
        if len(leastPopular) < len(allFlowers):
            print('not all flowers are set')

            accessedFlowersIds = []
            for access, flowerId, amount in leastPopular:
                accessedFlowersIds.append(flowerId)

            # only one flower accessed, pick another one
            leastPopularFlower = self.session.query(Flower) \
                .filter(Flower.id.notin_(accessedFlowersIds)) \
                .first()    
            
        else:
            print('more flowers')
            # set least popular flower
            leastPopularFlowerId = leastPopular[0][1]
            leastPopularFlower = self.session.query(Flower).get(leastPopularFlowerId)
            
       
        # create a new user, with card and flower
        newUser = User(card, leastPopularFlower)
        self.session.add(newUser)

        # commit new user
        self.session.commit()

        # add an access for this user
        newAccess = Access(newUser.id)
        self.session.add(newAccess)

        # commit all
        self.session.commit()
        
        # set state to RegisterState
        self.currentState = RegisterState(self, newUser)
        