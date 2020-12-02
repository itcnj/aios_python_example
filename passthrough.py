import aios
import time
import threading
import numpy as np

Server_IP_list = []



def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r vbus_voltage\n")
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r config.dc_bus_undervoltage_trip_level\n")
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "w config.dc_bus_undervoltage_trip_level 12\n")
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r config.dc_bus_undervoltage_trip_level\n")
        print('\n')





if __name__ == '__main__':
    main()
