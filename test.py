import aios
import time
import threading
import numpy as np
import json

Server_IP_list = []



def main():

    Server_IP_list = aios.broadcast_func()
    
    if Server_IP_list:

        for i in range(len(Server_IP_list)):
            aios.getRootTest(Server_IP_list[i])
            aios.getRootTest_2(Server_IP_list[i])
            aios.getRootTest(Server_IP_list[i])
            aios.getRootTest_2(Server_IP_list[i])

        for i in range(len(Server_IP_list)):
            aios.receive_func()
            aios.receive_func()
            aios.receive_func()
            aios.receive_func()



if __name__ == '__main__':
    main()
