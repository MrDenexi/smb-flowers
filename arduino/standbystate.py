import random

from arduino.state import State
from db.models import Flower

class StandbyState(State):

    def __init__(self, app):
        super().__init__(app)

        flowers = self.session().query(Flower).all()
        random.shuffle(flowers)

        self.flowers = flowers
        self.flowerIndex = 0
        self.openTime = 10

    async def run(self):
        await self.openFlower(self.flowers[self.flowerIndex], self.openTime)
        
        if (self.flowerIndex == len(self.flowers) - 1):
            self.flowerIndex = 0
        else:
            self.flowerIndex = self.flowerIndex + 1

        return self