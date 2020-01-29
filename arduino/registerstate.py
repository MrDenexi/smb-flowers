import random

from arduino.state import State
from db.models import Flower

from arduino.standbystate import StandbyState

# state when a new card (or user) is detected
class RegisterState(State):

    def __init__(self, app, user):
        super().__init__(app)

        self.user = user


    async def run(self):
        return StandbyState(self.app)
        