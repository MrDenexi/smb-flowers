import asyncio
from pyfirmata import PWM


# base state all the other extend on
class State: 

    def __init__(self, app):
        # set the app instance
        self.app = app

        print('created state ', self.__class__.__name__)

    # default function to run a state, always returns another state
    def run(self):
        return self

    # get db session
    def session(self):
        return self.app.session

    # get board
    def board(self):
        return self.app.board

    # helper function to get the pin
    def getPin(self, port):
        # if pin is already instantiated, return it
        if port in self.app.pins.keys():
            return self.app.pins[port]
        
        # create pin
        pin = self.board().get_pin('d:%s:p' % port)
        # set pwm
        pin.mode = PWM

        # add pin to app.pins
        self.app.pins[port] = pin

        # return pin
        return self.app.pins[port]

    # helper function to open flower for an amount of time
    async def openFlower(self, flower, time): 
        print('opening ', flower)

        # get pin of the flower
        pin = self.getPin(flower.port)

        # write pwm to open flower
        pin.write(0.7)

        # sleep for given amount of time
        await asyncio.sleep(time)

        # set pin low
        pin.write(0)
        print('closing ', flower)



        
        