from pyfirmata import Arduino, util, PWM

board = Arduino('/dev/ttyUSB0')

pin3 = board.get_pin('d:3:p')
pin3.mode = PWM

try: 
    while 1:
        port = board.digital[13].read()

        if port is None:
            port = 0

        x = input('pwm?')

        if float(port) > 0.0 and float(port) <= 1.0:
            new = float(port)
            pin3.write(new)
            print('---- \n')
            print(pin3.read())

except KeyboardInterrupt:
    stop()
    raise

def stop(self):
        
        # set arduino pins to low
        for i in range(2, 14):
            self.board.digital[i].write(0)

        print('Bye bye :)')

