import random

from arduino.state import State
from db.models import Flower

from arduino.standbystate import StandbyState

class RegisterState(State):

    def __init__(self, board, session):
        super().__init__(board,session)


    async def run(self):
        return StandbyState(board,session)
        