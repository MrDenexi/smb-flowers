
import random

from arduino.state import State
from db.models import Flower

class LoginState(State):

    def __init__(self, board, session):
        super().__init__(board,session)


    async def run(self):
        pass
        