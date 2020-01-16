from pyfirmata import Arduino, util

board = Arduino('/dev/ttyUSB0')


while 1:
    port = board.digital[13].read()

    if port is None:
        port = 0

    x = input('switch?')

    if float(port) > 0.5:
        new = 0
    else:
        new = 1
    
    board.digital[13].write(new)
