import aios
import time
import threading
import numpy as np
import json

Server_IP_list = ['192.168.5.81']


def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:

        cali_flag = False
        for i in range(len(Server_IP_list)):
            aios.encoderOffsetCalibration(Server_IP_list[i], 1)
            # aios.encoderIndexSearch(Server_IP_list[i], 1)
            cali_flag = True

        print('\n')

        time.sleep(10)
        for i in range(len(Server_IP_list)):
            aios.encoderIsReady(Server_IP_list[i], 1)
        print('\n')
        for i in range(len(Server_IP_list)):
            aios.saveConfig(Server_IP_list[i])
        print('\n')



if __name__ == '__main__':
    main()
