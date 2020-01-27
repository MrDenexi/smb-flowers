from pyfirmata import Arduino, util, PWM
from time import sleep

board = Arduino('/dev/ttyUSB0')

pin3 = board.get_pin('d:3:p')
pin3.mode = PWM

for i in [13]:
    board.digital[i].write(1)

while True:
    it = util.Iterator(board)
    it.start()
    board.analog[0].enable_reporting()
    pot = board.analog[0].read()
    

    if pot is None:
        pass 
    elif pot <= 1.00:
        pot = pot
        print(pot)
        pin3.write(pot)

    sleep(0.05)



