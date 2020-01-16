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

    def start(self):
        return programLoop()

    def stop(self):
        GPIO.cleanup()
        self.board
        print('Bye bye')



    def cardScan(id):
        # find card in db

        