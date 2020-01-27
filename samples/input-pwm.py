from pyfirmata import Arduino, util, PWM

board = Arduino('/dev/ttyUSB0')

pin3 = board.get_pin('d:11:p')
pin3.mode = PWM

try: 
    while 1:
        x = float(input('pwm?'))

        if isinstance(x, float) and (x >= 0.0) and (x <= 1.0):
            pin3.write(x)
        else:
            print('oh noes.')

except KeyboardInterrupt:
    # set arduino pins to low
    for i in range(2, 14):
        board.digital[i].write(0)

    print('Bye bye :)')

        

