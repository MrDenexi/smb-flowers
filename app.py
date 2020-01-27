import sys
from time import sleep
from datetime import datetime
from random import randint, choice
import asyncio

import RPi.GPIO as GPIO

import pyfirmata

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from db.models import User, Access, Flower
from arduino.standbystate import StandbyState
from arduino.loginstate import LoginState
from arduino.registerstate import RegisterState


class App:

    def __init__(self, session, reader, board):
        self.board = board
        self.session = session
        self.reader = reader

        self.currentState = StandbyState(board, session)

    async def readLoop(self):
        while True:
            print("Hold a tag near the reader")
            id, text = await self.reader.read()
            self.cardScan(id)
            await asyncio.sleep(3)

    async def stateLoop(self):
        while True:
            currentState = self.currentState
            resultState = await currentState.run()
            
            # make resultState currentState if currentState did not change
            if self.currentState is currentState:
                self.currentState = resultState
        
    
    async def main(self):
        try: 
            await asyncio.gather(
                self.readLoop(),
                self.stateLoop()
            )
        except:
            self.stop()
            raise

    def stop(self):
        # rPi gpio cleanup
        GPIO.cleanup()
        
        # set arduino pins to low
        for i in range(2, 14):
            self.board.digital[i].write(0)

        print('Bye bye :)')


    def cardScan(self, card):
        user = self.session.query(User).filter_by(card=card).first() 
        if user:
            self.userLogin(user)
        else:
            self.userRegister(card)

    def userLogin(self, user):
        access = Access(user.id)
        self.session.add(access)
        self.session.commit
        self.currentState = LoginState(self.board, self.session)

    def userRegister(self, card):
        leastPopularFlowerId = self.session.query(User.flower_id, func.count(User.flower_id).label('total') ) \
            .options(joinedload(User.accesses)) \
            .filter(User.accesses.time > datetime.today() - datetime.timedelta(30)) \
            .group_by(User.flower_id) \
            .order_by('total ASC') \
            .first() \
            .flower_id
        leastPopularFlower = Flower.get(leastPopularFlowerId)

        newUser = User(card, leastPopularFlower)
        self.session.add(newUser)

        newAccess = Access(newUser.id)
        self.session.add(newAccess)

        self.session.commit
        
        self.currentState = RegisterState(self.board, self.session)
        