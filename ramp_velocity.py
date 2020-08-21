import aios
import time

Server_IP_1 = '192.168.1.188' # 执行器IP地址
# Server_IP_1 = '192.168.100.21'  # 执行器IP地址
# Server_IP_1 = '39.97.214.191' # 执行器IP地址
# Server_IP_1 = '123.57.14.125' # 执行器IP地址
# Server_IP_2 = '192.168.1.148'

vel_list = [10000, 20000, 30000, 50000, 80000, 10000, 0]
delay_list = [1, 1, 1, 1, 1, 2, 1]


def main():

    if aios.broadcast_func():

        if (not aios.encoderIsReady(Server_IP_1, 1)):
            aios.encoderOffsetCalibration(Server_IP_1, 1)
            time.sleep(10)
        else:
            aios.AIOSGetRoot(Server_IP_1)
            time.sleep( 1 )

            for i in range(10):
                cvp = aios.getCVP(Server_IP_1, 1)
                print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
                time.sleep(0.01)

            if aios.AIOSEnable(Server_IP_1, 1):

                aios.trapezoidalMove(0, Server_IP_1, 1)
                time.sleep( 4 )

                aios.controlMode(2, Server_IP_1, 1)
                aios.velRampEnable(True, Server_IP_1, 1)


                for i in range(len(vel_list)):
                    aios.velRampTarget(vel_list[i], Server_IP_1, 1)
                    time.sleep( delay_list[i] )


                aios.AIOSDisable(Server_IP_1, 1)



if __name__ == '__main__':
    main()
