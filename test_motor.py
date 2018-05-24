#!/usr/bin/python
RASPBERRY = True
import sys, json
if RASPBERRY == True:
    import RPi.GPIO as GPIO
from time import sleep

FREQUENCY = 100
MIN_SPEED = 0
MAX_SPEED = 30
MAX_FORWARD_SPEED = 50
MAX_BACKWARD_SPEED = 95
SLEEP_TIME = 3.5
MAX_TURN_SPEED = 70

def read_gpio_conf(field):
    print('read_gpio_conf')
    with open('gpio_pins.txt') as json_data:
        data = json.load(json_data)
        print('gpio_pins  data: ', data)
        json_data.close()
    return data[field]


def gpio_init(gpio_data, pwm_motor):
    print ('gpio_init')
    gpio_data = read_gpio_conf('gpio_pins')
    if RASPBERRY == True:
       GPIO.setmode(GPIO.BOARD)
    print('GPIO.setmode(GPIO.BOARD)')
    reset_gpio(gpio_data)
    reset_pwm_motor(gpio_data, pwm_motor)
    return (gpio_data, pwm_motor)

def reset_gpio(gpio_data):
    for key, val in list(gpio_data.items()):
        if key != 'stop':
            if RASPBERRY == True:
                GPIO.setup(val,GPIO.OUT)
                GPIO.output(val,GPIO.LOW)
            print ('GPIO.setup(',val,',GPIO.OUT)')
            print ('GPIO.output(',val,',GPIO.LOW)')


def reset_pwm_motor(gpio_data, pwm_motor):
    for key, val in list(gpio_data.items()):
        if key in ('enable_dir'):
            if RASPBERRY == True:
                pwm_motor[key] = GPIO.PWM(val, FREQUENCY)
                pwm_motor[key].start(MIN_SPEED)
            print ('pwm_motor[',key,'] = GPIO.PWM(',val,',',FREQUENCY,')')
            print ('pwm_motor[',key,'].start(',MIN_SPEED,')')
    return pwm_motor


def forward():
    pwm_motor['enable_dir'].ChangeDutyCycle(MAX_FORWARD_SPEED)
    GPIO.output(gpio_data['forward_dir'], GPIO.HIGH)
    GPIO.output(gpio_data['backward_dir'], GPIO.LOW)
    GPIO.output(gpio_data['enable_dir'], GPIO.HIGH)


def backward():
    pwm_motor['enable_dir'].ChangeDutyCycle(MAX_BACKWARD_SPEED)
    GPIO.output(gpio_data['backward_dir'], GPIO.HIGH)
    GPIO.output(gpio_data['forward_dir'], GPIO.LOW)
    GPIO.output(gpio_data['enable_dir'], GPIO.HIGH)


def turn_right():
    pwm_motor['enable_dir'].ChangeDutyCycle(MAX_TURN_SPEED)
    GPIO.output(gpio_data['turn_right'], GPIO.HIGH)
    GPIO.output(gpio_data['turn_left'], GPIO.LOW)
    GPIO.output(gpio_data['enable_turn'], GPIO.HIGH)


def turn_left():
    pwm_motor['enable_dir'].ChangeDutyCycle(MAX_TURN_SPEED)
    GPIO.output(gpio_data['turn_left'], GPIO.HIGH)
    GPIO.output(gpio_data['turn_right'], GPIO.LOW)
    GPIO.output(gpio_data['enable_turn'], GPIO.HIGH)


def stop():
    pwm_motor['enable_dir'].ChangeDutyCycle(MIN_SPEED)


def noTurn():
    GPIO.output(gpio_data['enable_turn'], GPIO.LOW)

def test_motor(gpio_data):
    if RASPBERRY == True:
        print ('testing motion_engine - forward direction')
        input('print enter to continue')
        forward()
        sleep(SLEEP_TIME)
        print ('testing motion_engine - backward direction')
        #input('print enter to continue')
        backward()
        sleep(SLEEP_TIME)
        print ('testing motion_engine - forward direction')
        #input('print enter to continue')
        forward()
        sleep(SLEEP_TIME)
        print ('testing steering_wheel - right turn')
        #input('print enter to continue')
        turn_right()
        sleep(SLEEP_TIME)
        print ('testing steering_wheel - left turn')
        #input('print enter to continue')
        turn_left()
        sleep(SLEEP_TIME)
        print ('test concluded')
        #input('press enter to terminate the test')

gpio_data = {}
gpio_data = read_gpio_conf('gpio_pins')

pwm_motor = {}
gpio_init(gpio_data, pwm_motor)

