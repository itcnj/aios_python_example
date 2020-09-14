import aios
import time
import threading
import numpy as np

# Server_IP_list = ['192.168.1.136','192.168.1.112','192.168.1.164']#,'192.168.1.190']
# Server_IP_list = ['192.168.8.157']
Server_IP_list = ['192.168.8.167']#,'192.168.100.15','192.168.100.3']
# Server_IP_list = ['192.168.1.189']#,'192.168.1.148'] # 执行器IP地址
# Server_IP_list = ['39.97.214.191']
# Server_IP_list = ['123.57.14.125']
# Server_IP_list = ['192.168.31.96']



def main():

    if aios.broadcast_func():

        for i in range(len(Server_IP_list)):
            aios.AIOSGetRoot(Server_IP_list[i])


        aios.AIOSGetError(Server_IP_list[0], 1)
        aios.AIOSGetError(Server_IP_list[0], 0)
        aios.AIOSClearError(Server_IP_list[0], 1)
        aios.AIOSClearError(Server_IP_list[0], 0)
        print('\n')




if __name__ == '__main__':
    main()
