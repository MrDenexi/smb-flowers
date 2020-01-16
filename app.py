import sys
from time import sleep
import RPi.GPIO as GPIO

from db.models import User, Access, Flower


class App:

    def __init__(self, session, reader, board):
        self.session = session
        self.reader = reader
        self.board = board

    def programLoop(self):
        try:
            while True:
                print("Hold a tag near the reader")
                id, text = self.reader.read()
                self.cardScan(id)
                print("ID: %s\nText: %s" % (id,text))
                sleep(5)
        except KeyboardInterrupt:
            self.stop()
            raise

    def run(self):
        return self.programLoop()

    def stop(self):
        GPIO.cleanup()
        self.board
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

        