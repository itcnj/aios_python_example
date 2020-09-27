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
            aios.getMotionCtrlConfig(Server_IP_list[i], 1)
        print('\n')

        dict = {
            'pos_gain' : 30,
            'vel_gain' : 0.0002,
            'vel_integrator_gain' : 0.0002,
            'vel_limit' : 400000,
            'vel_limit_tolerance' : 1.2,
        }
        for i in range(len(Server_IP_list)):
            aios.setMotionCtrlConfig(dict, Server_IP_list[i], 1)
        print('\n')
        # aios.AIOSaveConfig(Server_IP_list[0])
        # aios.AIOSRebootMotorDrive(Server_IP_list[0])
        # time.sleep(2)
        #
        for i in range(len(Server_IP_list)):
            aios.getMotionCtrlConfig(Server_IP_list[i], 1)
        print('\n')




if __name__ == '__main__':
    main()
