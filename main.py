#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Rens Moring & Jeroen van den Berg"
__version__ = "0.1.0"
__license__ = "MIT"

from db.db import session_factory
from pyfirmata import Arduino
from mfrc522 import SimpleMFRC522
import asyncio

from app import App

def main():
    """ Main entry point of the app """
    session = session_factory()
    reader = SimpleMFRC522()
    board = Arduino('/dev/ttyUSB0')

    mainApp = App(session, reader, board)
    asyncio.run(mainApp.main())



if __name__ == "__main__":
    main()