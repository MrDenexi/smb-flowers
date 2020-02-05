import random
import asyncio

from datetime import timedelta, datetime

from arduino.state import State
from db.models import Flower, Access

# default state when nothing is happening
class StandbyState(State):

    def __init__(self, app):
        super().__init__(app)

        self.accesses = self.session().query(Access) \
            .filter(Access.accessed_at > (datetime.now() - timedelta(0,0,0,0,0,1))) \
            .order_by(Access.accessed_at.desc()) \
            .all()  

    async def run(self):
        if len(self.accesses) == 0:
            allFlowers = self.session().query(Flowers).all()
            currentFlower = random.choice(allFlowers)
        else:
            currentAccess = random.choice(self.accesses)
            currentFlower = currentAccess.user.flower

        await self.openFlower(currentFlower, random.randrange(7))
        
        await asyncio.sleep(3)

        return self