import aios
import time
import threading
import numpy as np
import json
import colorama
from colorama import Fore, Back, Style

# Server_IP_list = ['192.168.5.126']
Server_IP_list = []

pos_list_1 = [1000, 2000, 3000, 5000, 2000, 6000, 10000, 0, 5000, -10000, 15000, 20000, 0]
delay_list_1 = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 1, 1, 1, 2, 2, 2, 2]

pos_list_2 = [1000, 2000, 3000, 4000, 0]
delay_list_2 = [0, 0, 0, 0, 1]


def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:

        cali_flag = False
        for i in range(len(Server_IP_list)):
            if (not aios.encoderIsReady(Server_IP_list[i], 1)):
                aios.encoderOffsetCalibration(Server_IP_list[i], 1)
                # aios.encoderIndexSearch(Server_IP_list[i], 1)
                cali_flag = True


        print('\n')

        if cali_flag:
            time.sleep(10)
        else:
            for i in range(len(Server_IP_list)):
                aios.getRoot(Server_IP_list[i])

            print('\n')


            enableSuccess = True

            for i in range(len(Server_IP_list)):
                enableSuccess = aios.enable(Server_IP_list[i], 1)
            print('\n')

            if enableSuccess:

                # aios.controlMode(3, Server_IP_list[0], 1)

                for i in range(len(Server_IP_list)):
                    aios.trapezoidalMove(0, False, Server_IP_list[i], 1)
                time.sleep( 3 )


                # for i in range(len(pos_list_1)):
                #     start = time.time()
                #     for j in range(len(Server_IP_list)):
                #         aios.trapezoidalMove(pos_list_1[i], True, Server_IP_list[j], 1)
                #     print((time.time() - start)*1000)
                #     time.sleep( delay_list_1[i] )
                #
                #
                # for i in range(len(pos_list_2)):
                #     start = time.time()
                #     for j in range(len(Server_IP_list)):
                #         aios.trapezoidalMove(pos_list_2[i], True, Server_IP_list[j], 1)
                #         time.sleep( 0.2 )
                #     print((time.time() - start)*1000)
                #     time.sleep( delay_list_2[i] )

                # pos = 0
                for i in range(240000):
                    start = time.time()
                    pos = np.sin(i*0.002*np.pi)*20000
                    # pos = pos + 10
                    # print(pos)
                    for j in range(len(Server_IP_list)):
                        # aios.setPosition(pos, 0, 0, True, Server_IP_list[j], 1)
                        aios.trapezoidalMove(pos, False, Server_IP_list[j], 1)
                    # for j in range(len(Server_IP_list)):
                    #     aios.receive_func()

                    latency = time.time() - start
                    if latency > 0.2:
                        print(Fore.RED + Style.BRIGHT + str(latency))
                    time.sleep(0.002)


                for i in range(len(Server_IP_list)):
                    aios.trapezoidalMove(0, False, Server_IP_list[i], 1)
                time.sleep( 2 )



                for i in range(len(Server_IP_list)):
                    aios.disable(Server_IP_list[i], 1)



if __name__ == '__main__':
    main()
