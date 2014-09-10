#! /usr/bin/env python

import cwiid
import time
from RPIO import PWM

MIN_PULSE = 0
MAX_PULSE = 19990
PWM_SUBCYCLE = 20000
PWM_PULSE_INC = 10

PIN_F = 4
PIN_B = 17
PIN_L = 27
PIN_R = 22

PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

PWM.setup()
PWM.init_channel(0, subcycle_time_us = PWM_SUBCYCLE)
PWM.add_channel_pulse(0, PIN_F, 0, 0)
#servo = PWM.Servo()
#servo.set_servo(PIN_F, 0)

while True:
    print 'Press 1+2 on your Wiimote now...'
    try:
        wm = cwiid.Wiimote()
    except RuntimeError:
        print 'Trying again'
        continue
    break

print 'Wiimote connected'
wm.led = 1
wm.rpt_mode = cwiid.RPT_BTN

speed = 0
speed_0 = 0

while True:
    if wm.state['buttons'] & cwiid.BTN_UP:
        speed += 0.1
    elif wm.state['buttons'] & cwiid.BTN_DOWN:
        speed -= 0.1

    if speed != speed_0:
        if speed < 0:
            speed = 0
        elif speed > 1:
            speed = 1

        pulse_w = MIN_PULSE + speed * (MAX_PULSE - MIN_PULSE)
        # ??? using low level PWM, max becomes 2000
        pulse_w /= 10
        pulse_w -= pulse_w % PWM_PULSE_INC
        print pulse_w
        #PWM.clear_channel_gpio(0, PIN_F)
        PWM.add_channel_pulse(0, PIN_F, 0, int(pulse_w))
        #servo.stop_servo(PIN_F)
        #servo.set_servo(PIN_F, pulse_w)
        speed_0 = speed

    time.sleep(0.1)

