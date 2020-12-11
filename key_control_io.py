import aios
import time
import threading
import numpy as np
import json

from pynput import keyboard

Server_IP_list = ['192.168.5.89']

def on_press(key):
    try:
        dict = {
            'PWM0_CH' : 1400,
            'PWM1_CH' : 2048,
            'SERVO0' : 0,
            'SERVO1' : 90
        }
        aios.setIOState(dict, True, Server_IP_list[0])
        print('alphanumeric key  {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    dict = {
        'PWM0_CH' : 60000,
        'PWM1_CH' : 60000,
        'SERVO0' : 180,
        'SERVO1' : 120
    }
    aios.setIOState(dict, True, Server_IP_list[0])
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        return False

def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:
        while True:
            with keyboard.Listener(
                on_press = on_press,
                on_release = on_release) as listener:
                listener.join()
            time.sleep(0.1)

if __name__ == '__main__':
    main()
