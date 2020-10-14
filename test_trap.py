import aios
import time
import threading
import numpy as np
import json

Server_IP_list = ['192.168.1.100']

pos_list_1 = [1000, 2000, 3000, 5000, 2000, 6000, 10000, 0, 5000, -10000, 15000, 20000, 0]
delay_list_1 = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 1, 1, 1, 2, 2, 2, 2]

pos_list_2 = [1000, 2000, 3000, 4000, 0]
delay_list_2 = [0, 0, 0, 0, 1]


def main():

    aios.trapezoidalMove(0, True, Server_IP_list[0], 1)
    time.sleep(1)
    aios.trapezoidalMove(4000, True, Server_IP_list[0], 1)
    time.sleep(1)
    aios.trapezoidalMove(-4000, True, Server_IP_list[0], 1)
    time.sleep(1)
    aios.trapezoidalMove(4000, True, Server_IP_list[0], 1)
    time.sleep(1)
    aios.trapezoidalMove(-4000, True, Server_IP_list[0], 1)
    time.sleep(1)



if __name__ == '__main__':
    main()
