import aios
import time
import threading
import numpy as np

Server_IP_list = []



def main():

    Server_IP_list = aios.broadcast_func()
    
    if Server_IP_list:

        for i in range(len(Server_IP_list)):
            aios.getRoot(Server_IP_list[i])

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r axis1.error\n")
            aios.passthrough(Server_IP_list[i], "r axis1.encoder.error\n")
            aios.passthrough(Server_IP_list[i], "r axis1.motor.error\n")
            aios.passthrough(Server_IP_list[i], "r axis1.controller.error\n")

            aios.passthrough(Server_IP_list[i], "w axis1.error 0\n")
        print('\n')




if __name__ == '__main__':
    main()
