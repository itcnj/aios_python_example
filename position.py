import aios
import time
import numpy as np

# Server_IP_1 = '192.168.1.189' # 执行器IP地址
# Server_IP_1 = '192.168.100.21'  # 执行器IP地址
Server_IP_1 = '192.168.1.190'  # 执行器IP地址
# Server_IP_1 = '39.97.214.191' # 执行器IP地址
# Server_IP_1 = '123.57.14.125' # 执行器IP地址
# Server_IP_2 = '192.168.1.148'

# pos_list = [1000, 2000, 3000, 5000, 2000, 6000, 10000, 0, 5000, -10000, 15000, 20000]
# delay_list = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 1, 1, 1, 2, 2, 2]

pos_list = [1000, 2000, 3000, 5000, 8000, 0, -2000]
delay_list = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 0.3]

def main():

    if aios.broadcast_func():

        if (not aios.encoderIsReady(Server_IP_1, 1)):
            aios.encoderOffsetCalibration(Server_IP_1, 1)
            time.sleep(10)
        # elif (not aios.encoderIsReady(Server_IP_2, 1)):
        #     aios.encoderOffsetCalibration(Server_IP_2, 1)
        #     time.sleep(10)
        else:
            aios.getRoot(Server_IP_1)
            # getRoot(Server_IP_2)
            time.sleep( 1 )

            # aios.getTrapTraj(Server_IP_1, 1)
            # aios.getControllerConfig(Server_IP_1, 1)
            #
            # time.sleep( 2 )
            # aios.setLinearCount(0, Server_IP_1, 1)

            for i in range(20):
                cvp = aios.getCVP(Server_IP_1, 1)
                print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
                time.sleep(0.01)

            if aios.enable(Server_IP_1, 1):# and aios.enable(Server_IP_2, 1):

                # aios.controlMode(Server_IP_1, 2, 1)
                aios.trapezoidalMove(0, True, Server_IP_1, 1)
                time.sleep( 2 )

                for i in range(800):
                    start = time.time()
                    pos = np.sin(i*0.02*np.pi)*1000
                    print(pos)
                    aios.setPosition(pos, 0, 0, False, Server_IP_1, 1)
                    # aios.trapezoidalMove(pos, Server_IP_1, 1)
                    print(time.time() - start)
                    time.sleep(0.01)


                for i in range(len(pos_list)):
                    aios.trapezoidalMove(pos_list[i], True, Server_IP_1, 1)
                    # aios.trapezoidalMove(pos_list[i], Server_IP_2, 1)
                    time.sleep( delay_list[i] )


                aios.disable(Server_IP_1, 1)
                # aios.disable(Server_IP_1, 0)
                # aios.disable(Server_IP_2, 1)



if __name__ == '__main__':
    main()
