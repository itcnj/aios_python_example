import aios
import time
import threading
import numpy as np

Server_IP_list = []



def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:

        for i in range(len(Server_IP_list)):
            aios.AIOSGetRoot(Server_IP_list[i])
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.getTrapTraj(Server_IP_list[i], 1)
        print('\n')

        dict = {
            'accel_limit' : 320000,
            'decel_limit' : 320000,
            'vel_limit' : 200000
        }
        for i in range(len(Server_IP_list)):
            aios.setTrapTraj(dict, Server_IP_list[i], 1)
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.AIOSaveConfig(Server_IP_list[i])
            # aios.AIOSRebootMotorDrive(Server_IP_list[i])

        print('\n')
        time.sleep(2)

        for i in range(len(Server_IP_list)):
            aios.getTrapTraj(Server_IP_list[i], 1)
        print('\n')




if __name__ == '__main__':
    main()
