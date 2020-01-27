
import random

from arduino.state import State
from db.models import Flower

from arduino.standbystate import StandbyState

import asyncio

class LoginState(State):

    def __init__(self, board, session, user):
        super().__init__(board,session)
        self.user = user


    async def run(self):
        self.openFlower(self.user.flower, 2)
        await asyncio.sleep(2)
        self.openFlower(self.user.flower, 2)
        await asyncio.sleep(2)
        self.openFlower(self.user.flower, 2)

        return StandByState(self.board, self.session)

        