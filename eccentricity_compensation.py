import aios
import time
import threading
import numpy as np
import matplotlib.pyplot as plt

Server_IP_list = ['192.168.2.40']
# Server_IP_list = []
count_in_cpr_list = []



def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:
        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.current 2\n")
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.finish_on_vel 0\n") 
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.finish_on_distance 1\n") 
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.finish_distance 10000\n") # 1600
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.vel 100\n") # 1600
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.accel 100\n") # 400
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w axis1.requested_state 9\n")
        print('\n')

        for j in range(200):
            for i in range(len(Server_IP_list)):
                start = time.time()
                count_in_cpr = aios.getCountInCpr(Server_IP_list[i])
                count_in_cpr_list.append(count_in_cpr)
                latency = time.time() - start
                print(latency*1000)
            print('\n')
            time.sleep(0.01)

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w axis1.requested_state 1\n")
        print('\n')

        print(count_in_cpr_list)

        plt.plot(count_in_cpr_list)
        plt.ylabel('count_in_cpr_list')
        plt.show()



if __name__ == '__main__':
    main()