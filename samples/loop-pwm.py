from pyfirmata import Arduino, util, PWM

import sys
import time

board = Arduino('/dev/ttyUSB0')

try: 
    pwm_val = float(sys.argv[1])
    print('pwm is', pwm_val)
    pins = []

    for i in [3, 5, 6, 9, 10, 11]:
        pin = board.get_pin(format('d:%s:p', str(i)))
        pin.mode = PWM
        pins.append(pin)

    for pin in pins: 
        if isinstance(pwm_val, float) and (pwm_val >= 0.0) and (pwm_val <= 1.0):
            print('on:', pin.port)
            pin.write(pwm_val)
            time.sleep(1)
            print('off:', pin.port)
            pin.write(0)
        else:
            print('oh noes.')

except KeyboardInterrupt:
    # set arduino pins to low
    for i in range(2, 14):
        board.digital[i].write(0)

    print('Bye bye :)')
