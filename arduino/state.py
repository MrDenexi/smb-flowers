import asyncio
from pyfirmata import PWM

class State: 

    def __init__(self, board, session):
        self.board = board
        self.session = session

    def run(self, session, board):
        pass

    async def openFlower(self, flower, time): 
        print('opening ', flower)
        pin = self.board.get_pin('d:%s:p' % flower.port)
        pin.mode = PWM
        pin.write(0.7)
        await asyncio.sleep(time)
        pin.write(0)
        print('closing ', flower)



        
        