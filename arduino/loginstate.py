
import random

from arduino.state import State
from db.models import Flower

from arduino.standbystate import StandbyState

import asyncio

# state when a user returns (logs in)
class LoginState(State):

    def __init__(self, app, user):
        super().__init__(app)
        self.user = user

    async def run(self):
        # pulse flowers
        await self.openFlower(self.user.flower, 2)
        await asyncio.sleep(2)
        await self.openFlower(self.user.flower, 2)
        await asyncio.sleep(2)
        await self.openFlower(self.user.flower, 2)

        # return standby state
        return StandbyState(self.app)

        