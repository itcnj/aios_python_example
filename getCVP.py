import aios
import time
import threading
import numpy as np
import json

Server_IP_list = []

pos_list_1 = [1000, 2000, 3000, 5000, 2000, 6000, 10000, 0, 5000, -10000, 15000, 20000, 0]
delay_list_1 = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 1, 1, 1, 2, 2, 2, 2]

pos_list_2 = [1000, 2000, 3000, 4000, 0]
delay_list_2 = [0, 0, 0, 0, 1]


def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:

        for i in range(1000):
            for i in range(len(Server_IP_list)):
                cvp = aios.getCVP(Server_IP_list[i], 1)
                print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))

            time.sleep(0.05)




if __name__ == '__main__':
    main()
