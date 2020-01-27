import asyncio
from pyfirmata import PWM

class State: 

    def __init__(self, app):
        self.app = app

        print('created state ', self.__class__.__name__)

    def run(self):
        pass

    def getPin(self, port):
        if port in self.app.pins.keys():
            return self.app.pins[port]
        
        pin = self.board().get_pin('d:%s:p' % port)
        pin.mode = PWM

        self.app.pins[port] = pin
        return self.app.pins[port]

    def session(self):
        return self.app.session

    def board(self):
        return self.app.board

    async def openFlower(self, flower, time): 
        print('opening ', flower)
        pin = self.getPin(flower.port)
        pin.write(0.7)
        await asyncio.sleep(time)
        pin.write(0)
        print('closing ', flower)



        
        