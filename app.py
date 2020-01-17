import sys
from time import sleep
import RPi.GPIO as GPIO

from db.models import User, Access, Flower


class App:

    def __init__(self, session, reader, board):
        self.session = session
        self.reader = reader
        self.board = board

        # turn on led
        self.board.digital[13].write(1)

    def programLoop(self):
        try:
            while True:
                print("Hold a tag near the reader")
                id, text = self.reader.read()
                self.cardScan(id)
                print("ID: %s\nText: %s" % (id,text))
                sleep(1)
        except KeyboardInterrupt:
            self.stop()
            raise

    def run(self):
        return self.programLoop()

    def stop(self):
        # rPi gpio cleanup
        GPIO.cleanup()
        
        # set arduino pins to low
        for i in range(14):
            self.board.digital[i].write(0)

        print('Bye bye :)')


    def cardScan(self, id):
        port = self.board.digital[13].read()

        if port is None:
            port = 0

        if float(port) > 0.5:
            new = 0
        else:
            new = 1
        
        self.board.digital[13].write(new)

        