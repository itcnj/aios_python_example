import aios
import time
import numpy as np

# Server_IP_list = ['192.168.2.226']#,'192.168.2.106']
# Server_IP_list = ['192.168.100.16','192.168.100.15','192.168.100.3']
Server_IP_list = ['192.168.1.190']#, '192.168.1.148'] # 执行器IP地址

# pos_list = [1000, 2000, 3000, 5000, 2000, 6000, 10000, 0, 5000, -10000, 15000, 20000]
# delay_list = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 1, 1, 1, 2, 2, 2]

pos_list = [1000, 2000, 3000, 5000, 8000, 0, -2000]
delay_list = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 0.3]

def main():

    if aios.broadcast_func():

        cali_flag = False
        for i in range(len(Server_IP_list)):
            if (not aios.encoderIsReady(Server_IP_list[i], 1)):
                aios.encoderOffsetCalibration(Server_IP_list[i], 1)
                cali_flag = True

        if cali_flag:
            time.sleep(10)
        else:
            for i in range(len(Server_IP_list)):
                aios.getRoot(Server_IP_list[i])

            time.sleep( 1 )

            # aios.getTrapTraj(Server_IP_1, 1)
            # aios.getControllerConfig(Server_IP_1, 1)
            # time.sleep( 2 )

            for i in range(20):
                cvp = aios.getCVP(Server_IP_list[0], 1)
                print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
                time.sleep(0.01)

            enableSuccess = True
            for i in range(len(Server_IP_list)):
                enableSuccess = aios.enable(Server_IP_list[i], 1)

            if enableSuccess:

                for i in range(len(Server_IP_list)):
                    aios.trapezoidalMove(0, Server_IP_list[i], 1)
                time.sleep( 2 )

                for i in range(400):
                    start = time.time()
                    pos = np.sin(i*0.1*np.pi)*1000
                    for j in range(len(Server_IP_list)):
                        aios.setPosition(pos, 0, 0, Server_IP_list[j], 1)
                        # aios.setPosition(i*100, 0, 0, Server_IP_list[j], 1)
                        # aios.trapezoidalMove(pos, Server_IP_list[j], 1)
                    aios.receive_func()
                    print((time.time() - start)*1000)
                    time.sleep(0.002)

                for i in range(len(pos_list)):
                    for j in range(len(Server_IP_list)):
                        aios.trapezoidalMove(pos_list[i], Server_IP_list[j], 1)
                    time.sleep( delay_list[i] )

                for i in range(len(Server_IP_list)):
                    aios.disable(Server_IP_list[i], 1)



if __name__ == '__main__':
    main()
