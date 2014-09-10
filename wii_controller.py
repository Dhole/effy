#! /usr/bin/env python

import cwiid
import time
import RPIO
from RPIO import PWM

MIN_PULSE = 0
MAX_PULSE = 19990
PWM_SUBCYCLE = 20000
PWM_PULSE_INC = 10

PIN_F = 4
PIN_B = 17
PIN_L = 27
PIN_R = 22

CHAN_F = 0
CHAN_B = 1

def set_speed(pin, chan, speed, speed_0):

    pulse_inc = PWM.get_pulse_incr_us()
    cycle_dur = PWM.get_channel_subcycle_time_us(chan)
    num_pulses = int(cycle_dur * speed / pulse_inc)

    PWM.add_channel_pulse(chan, pin, 0, num_pulses)
    

PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

RPIO.setup(PIN_L, RPIO.OUT)
RPIO.setup(PIN_R, RPIO.OUT)
RPIO.output(PIN_L, False)
RPIO.output(PIN_R, False)

PWM.setup()
PWM.init_channel(CHAN_F, subcycle_time_us = PWM_SUBCYCLE)
PWM.init_channel(CHAN_B, subcycle_time_us = PWM_SUBCYCLE)
PWM.add_channel_pulse(CHAN_F, PIN_F, 0, 0)
PWM.add_channel_pulse(CHAN_B, PIN_B, 0, 0)

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

speed = 0.6
speed_0 = speed
move = '0'
move_0 = move
turn = '0'
turn_0 = turn

while True:
    move = '0'
    turn = '0'
    if wm.state['buttons'] & cwiid.BTN_UP:
        turn = 'l'
    if wm.state['buttons'] & cwiid.BTN_DOWN:
        turn = 'r'
    if wm.state['buttons'] & cwiid.BTN_1:
        turn = 'b'
    if wm.state['buttons'] & cwiid.BTN_2:
        move = 'f'
    if wm.state['buttons'] & cwiid.BTN_PLUS:
        speed += 0.1
    if wm.state['buttons'] & cwiid.BTN_MINUS:
        speed -= 0.1

    if speed != speed_0:
        if speed < 0:
            speed = 0
        elif speed > 1:
            speed = 1

    if (move != move_0):
        if move == 'f':
            set_speed(PIN_B, CHAN_B, 0, 1)
            set_speed(PIN_F, CHAN_F, speed, speed_0)
        elif move == 'b':
            set_speed(PIN_F, CHAN_F, 0, 1)
            set_speed(PIN_B, CHAN_B, speed, speed_0)
        elif move == '0':
            set_speed(PIN_B, CHAN_F, 0, 1)
            set_speed(PIN_F, CHAN_F, 0, 1)

    if (turn != turn_0):
        if turn == 'l':
            RPIO.output(PIN_L, True)
            RPIO.output(PIN_R, False)
        elif turn = 'r':
            RPIO.output(PIN_L, False)
            RPIO.output(PIN_R, True)
        elif turn = '0':
            RPIO.output(PIN_L, False)
            RPIO.output(PIN_R, False)
        
    move_0 = move
    turn_0 = turn
    speed_0 = speed
    time.sleep(0.1)

