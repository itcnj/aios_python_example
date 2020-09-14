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


        aios.getMotionCtrlConfig(Server_IP_list[0], 1)

        dict = {
            'pos_gain' : 20,
            'vel_gain' : 0.0002,
            'vel_integrator_gain' : 0.0002,
            'vel_limit' : 400000,
            'vel_limit_tolerance' : 1.2,
        }
        aios.setMotionCtrlConfig(dict, Server_IP_list[0], 1)
        # aios.AIOSaveConfig(Server_IP_list[0])
        # aios.AIOSRebootMotorDrive(Server_IP_list[0])
        # time.sleep(2)
        #
        aios.getMotionCtrlConfig(Server_IP_list[0], 1)
        print('\n')




if __name__ == '__main__':
    main()
