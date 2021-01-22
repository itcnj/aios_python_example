import aios
import time
import threading
import numpy as np

# Server_IP_list = ['192.168.5.35']
Server_IP_list = []



def main():

    Server_IP_list = aios.multicast_func()
    if Server_IP_list:

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r vbus_voltage\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r config.dc_bus_undervoltage_trip_level\n")
        # print('\n')
        #
        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w config.dc_bus_undervoltage_trip_level 12\n")
        # print('\n')
        #
        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r config.dc_bus_undervoltage_trip_level\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.encoder.config.offset\n")
        # print('\n')
        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.controller.config.vel_ramp_rate 400000.00\n")
        # print('\n')
        #
        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.controller.config.vel_ramp_rate\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.motor.config.direction\n")
        # print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r axis1.motor.get_inverter_temp\n")
        print('\n')
        # for j in range(10000):
        #     for i in range(len(Server_IP_list)):
        #         start = time.time()
        #         aios.passthrough(Server_IP_list[i], "p 1 0.0 0.0 0.0\nf 1\n")
        #         latency = time.time() - start
        #         print(latency*1000)
        #     print('\n')
        #     time.sleep(0.01)





if __name__ == '__main__':
    main()
