
import random

from arduino.state import State
from db.models import Flower

from arduino.standbystate import StandbyState

import asyncio

class LoginState(State):

    def __init__(self, app, user):
        super().__init__(app)
        self.user = user

    async def run(self):
        await self.openFlower(self.user.flower, 2)
        await asyncio.sleep(2)
        await self.openFlower(self.user.flower, 2)
        await asyncio.sleep(2)
        await self.openFlower(self.user.flower, 2)

        return StandbyState(self.app)

        