import aios
import time
import threading
import numpy as np

# Server_IP_list = ['192.168.1.136','192.168.1.112','192.168.1.164']#,'192.168.1.190']
Server_IP_list = []
# Server_IP_list = ['192.168.100.21']#,'192.168.100.15','192.168.100.3']
# Server_IP_list = ['192.168.1.189']#,'192.168.1.148'] # 执行器IP地址
# Server_IP_list = ['39.97.214.191']
# Server_IP_list = ['123.57.14.125']
# Server_IP_list = ['192.168.31.96']

pos_list_1 = [1000, 2000, 3000, 5000, 2000, 6000, 10000, 0, 5000, -10000, 15000, 20000]
delay_list_1 = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 1, 1, 1, 2, 2, 2]

pos_list_2 = [0, 1000, 2000, 3000, 4000, 0]
pos_list_3 = [0, -1000, -2000, -3000, -4000, 0]
delay_list_2 = [0, 0.2, 0.2, 0.2, 0.3, 1]

t = 0
def fun_timer():
    global t
    start = time.time()
    pos = np.sin(t*(0.005+(t/30000))*np.pi)*1000
    print ("Set position = ", pos)
    for j in range(len(Server_IP_list)):
        aios.setPosition(pos, 0, 0, Server_IP_list[j], 1)
        # aios.setPosition(i*100, 0, 0, Server_IP_list[j], 1)
        # aios.trapezoidalMove(pos, Server_IP_list[j], 1)
    # for j in range(len(Server_IP_list)):
    #     aios.receive_func()

    print((time.time() - start)*1000)
    t += 1

    if t < 800:
        timer = threading.Timer(0.005,fun_timer)
        timer.start()



def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:

        for i in range(len(Server_IP_list)):
            aios.AIOSGetRoot(Server_IP_list[i])

        for i in range(300):
            start = time.time()
            for j in range(len(Server_IP_list)):
                aios.dum_func(Server_IP_list[j])
            for j in range(len(Server_IP_list)):
                aios.receive_func()
            print((time.time() - start)*1000)
            time.sleep(0.005)
        # aios.getPIDControllerConfig(Server_IP_list[0], 1)

        # aios.getMotorConfig(Server_IP_list[0], 1)

        # aios.getMotorConfig(Server_IP_list[0], 0)
        #
        # dict = {
        #     'current_lim' : 16,
        #     'current_lim_margin' : 4,
        #     'inverter_temp_limit_lower' : 90,
        #     'inverter_temp_limit_upper' : 110,
        #     'requested_current_range' : 30,
        #     'current_control_bandwidth' : 500,
        # }
        # aios.setMotorConfig(dict, Server_IP_list[0], 0)
        # aios.AIOSaveConfig(Server_IP_list[0])
        # aios.AIOSRebootMotorDrive(Server_IP_list[0])
        # time.sleep(2)
        #
        # aios.getMotorConfig(Server_IP_list[0], 0)
        # print('\n')
        #
        # aios.AIOSGetError(Server_IP_list[0], 1)
        # aios.AIOSGetError(Server_IP_list[0], 0)
        # aios.AIOSClearError(Server_IP_list[0], 1)
        # aios.AIOSClearError(Server_IP_list[0], 0)


        # cali_flag = False
        # for i in range(len(Server_IP_list)):
        #     if (not aios.encoderIsReady(Server_IP_list[i], 1)):
        #         aios.encoderOffsetCalibration(Server_IP_list[i], 1)
        #         cali_flag = True
        #
        # if cali_flag:
        #     time.sleep(10)
        #
        # cali_flag = False
        # for i in range(len(Server_IP_list)):
        #     if (not aios.encoderIsReady(Server_IP_list[i], 0)):
        #         aios.encoderOffsetCalibration(Server_IP_list[i], 0)
        #         cali_flag = True
        #
        # print('\n')
        #
        # if cali_flag:
        #     time.sleep(10)
        # else:
        #     for i in range(len(Server_IP_list)):
        #        aios.AIOSGetRoot(Server_IP_list[i])
        #     print('\n')
        #
        #     for j in range(1):
        #         for i in range(len(Server_IP_list)):
        #             cvp = aios.getCVP(Server_IP_list[i], 1)
        #             print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
        #             cvp = aios.getCVP(Server_IP_list[i], 0)
        #             print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
        #             print('\n')
        #
        #     print('\n')
        # for i in range(len(Server_IP_list)):
        #     aios.AIOSGetState(Server_IP_list[i], 1)
        #     aios.AIOSGetState(Server_IP_list[i], 0)
        # print('\n')
        #

        # for i in range(len(Server_IP_list)):
        #     aios.getPIDControllerConfig(Server_IP_list[i], 1)
        #     aios.getPIDControllerConfig(Server_IP_list[i], 0)
        # print('\n')
        #
        # pid = {
        #     'pos_gain' : 10,
        #     'vel_gain' : 0.0003,
        #     'vel_integrator_gain' : 0.0002,
        #     'vel_limit' : 400000,
        #     'vel_limit_tolerance' : 1.2,
        # }
        # for i in range(len(Server_IP_list)):
        #     aios.setPIDControllerConfig(pid, Server_IP_list[i], 1)
        #     aios.setPIDControllerConfig(pid, Server_IP_list[i], 0)
        # print('\n')

        #
        #
        #     enableSuccess = True
        #     for i in range(len(Server_IP_list)):
        #         enableSuccess = aios.AIOSEnable(Server_IP_list[i], 1)
        #         enableSuccess = aios.AIOSEnable(Server_IP_list[i], 0)
        #     print('\n')
        #
        #     if enableSuccess:
        #
        #
        #         # aios.getPIDControllerConfig(Server_IP_list[0], 0)
        #         # print('\n')
        #         # aios.setTrapTraj(320000, 320000, 200000, Server_IP_list[0], 0)
        #         # aios.getTrapTraj(Server_IP_list[0], 0)
        #
        #
        #         # str = input("Press Enter：")
        #
        #         # time.sleep( 1 )
        #
        #         # for i in range(len(Server_IP_list)):
        #         #     aios.setLinearCount(0, Server_IP_list[i], 1)
        #         #     aios.setLinearCount(0, Server_IP_list[i], 0)
        #         # print('\n')
        #         #
        #         # for i in range(len(Server_IP_list)):
        #         #     cvp = aios.getCVP(Server_IP_list[i], 1)
        #         #     print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
        #         #     cvp = aios.getCVP(Server_IP_list[i], 0)
        #         #     print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
        #         print('\n')
        #         for i in range(len(Server_IP_list)):
        #             aios.AIOSGetState(Server_IP_list[i], 1)
        #             aios.AIOSGetState(Server_IP_list[i], 0)
        #         print('\n')
        #
        #         time.sleep( 3 )
        #
        #         # for i in range(len(pos_list_2)):
        #         #     start = time.time()
        #         #     for j in range(len(Server_IP_list)):
        #         #         aios.trapezoidalMove(pos_list_2[i], True, Server_IP_list[j], 1)
        #         #         aios.trapezoidalMove(pos_list_3[i], True, Server_IP_list[j], 0)
        #         #     print((time.time() - start)*1000)
        #         #     time.sleep( delay_list_2[i] )
        #
        #         for i in range(len(Server_IP_list)):
        #             aios.AIOSDisable(Server_IP_list[i], 1)
        #             aios.AIOSDisable(Server_IP_list[i], 0)



if __name__ == '__main__':
    main()
