import aios
import time
import threading
import numpy as np

# Server_IP_list = ['192.168.1.136','192.168.1.112','192.168.1.164']#,'192.168.1.190']
Server_IP_list = ['192.168.100.21']
# Server_IP_list = ['192.168.100.21']#,'192.168.100.15','192.168.100.3']
# Server_IP_list = ['192.168.1.189']#,'192.168.1.148'] # 执行器IP地址
# Server_IP_list = ['39.97.214.191']
# Server_IP_list = ['123.57.14.125']
# Server_IP_list = ['192.168.31.96']



def main():

    if aios.broadcast_func():

        for i in range(len(Server_IP_list)):
            aios.AIOSGetRoot(Server_IP_list[i])


        aios.getMotorConfig(Server_IP_list[0], 0)

        dict = {
            'current_lim' : 15,
            'current_lim_margin' : 4,
            'inverter_temp_limit_lower' : 90,
            'inverter_temp_limit_upper' : 110,
            'requested_current_range' : 30,
            'current_control_bandwidth' : 300,
        }
        aios.setMotorConfig(dict, Server_IP_list[0], 0)
        aios.AIOSSaveConfig(Server_IP_list[0])
        aios.AIOSRebootMotorDrive(Server_IP_list[0])
        time.sleep(2)

        aios.getMotorConfig(Server_IP_list[0], 0)
        print('\n')




if __name__ == '__main__':
    main()
