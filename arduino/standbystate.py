import random

from arduino.State import State
from db.models import Flower

class StandbyState(State):

    def __init__(self, board, session):
        super().__init__(board,session)

        flowers = session.query(Flower).all()
        random.shuffle(flowers)

        self.flowers = flowers
        self.flowerIndex = 0
        self.openTime = 10

    async def run(self):
        await self.openFlower(self.flowers[self.flowerIndex], self.board,  self.openTime)
        
        if (self.flowerIndex == self.flowers.count() - 1):
            self.flowerIndex = 0
        else:
            self.flowerIndex = self.flowerIndex + 1

        return self