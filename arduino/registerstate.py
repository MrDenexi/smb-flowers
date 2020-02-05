import random

from arduino.state import State
from db.models import Flower

from arduino.standbystate import StandbyState
from arduino.loginstate import LoginState

# state when a new card (or user) is detected
class RegisterState(State):

    def __init__(self, app, user):
        super().__init__(app)

        self.user = user

    async def run(self):
        return LoginState(self.app, self.user)
        