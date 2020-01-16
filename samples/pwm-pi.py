
import RPi.GPIO as IO          #calling header file which helps us use GPIO ^`^ys of PI

import time                            #calling time to provide delays in program

IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as  ^`^xGPIO19 ^`^y)

IO.setup(19,IO.OUT)           # initialize GPIO19 as an output.

p = IO.PWM(19,100)          #GPIO19 as PWM output, with 100Hz frequency
p.start(0)                              #generate PWM signal with 0% duty cycle

i = 100

try: 
    while 1:                               #execute loop forever
        for x in range (i):                          #execute loop for 50 times, x being incremented from 0 to 49.
            print('a. ' + str(x) + '\n')
            p.ChangeDutyCycle(x)               #change duty cycle for varying the brightness of LED.
            time.sleep(0.1)                           #sleep for 100m second

        for x in range (i):                         #execute loop for 50 times, x being incremented from 0 to 49.
            print('b. ' + str(x) + ' \n')
            p.ChangeDutyCycle(i-x)        #change duty cycle for changing the brightness of LED.
            time.sleep(0.1)                          #sleep for 100m second
except KeyboardInterrupt:
    IO.cleanup()
    raise
