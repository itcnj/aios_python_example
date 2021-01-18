import aios
import time
import threading
import numpy as np
import json

Server_IP_list = []


def main():

    # Server_IP_list = aios.broadcast_func()
    Server_IP_list = aios.multicast_func()
    if Server_IP_list:

        for i in range(len(Server_IP_list)):
            aios.getNetworkSetting(Server_IP_list[i])
        print('\n')
        time.sleep(1)

        for i in range(len(Server_IP_list)):
            dict = {
                'DHCP_enable' : False,
                'SSID' : 'AMBER',
                'password' : 'amber3.1415926',
                'staticIP' : [10,0,0,i+10],
                'gateway' : [10,0,0,1],
                'subnet' : [255,255,255,0],
                'dns_1' : [114,114,114,114],
                'dns_2' : [8,8,8,8]
            }
            aios.setNetworkSetting(dict, Server_IP_list[i])
        print('\n')
        time.sleep(1)



if __name__ == '__main__':
    main()
