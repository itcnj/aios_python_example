import aios
import time


Server_IP_list = []

vel_list = [10000, 20000, 30000, 50000, -80000, -10000, 0]
delay_list = [1, 1, 1, 1, 1, 2, 1]


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
                aios.AIOSGetRoot(Server_IP_list[i])

            i = 2;
            enableSuccess = aios.AIOSEnable(Server_IP_list[i], 1)
            print('\n')

            if enableSuccess:

                aios.trapezoidalMove(0, True, Server_IP_list[i], 1)
                time.sleep( 4 )

                aios.controlMode(2, Server_IP_list[i], 1)
                aios.velRampEnable(True, Server_IP_list[i], 1)


                for j in range(len(vel_list)):
                    aios.velRampTarget(vel_list[j], Server_IP_list[i], 1)
                    time.sleep( delay_list[j] )

                time.sleep( 1 )

                print("\n")

                Pos, Vel, Cur = aios.getCVP(Server_IP_list[i], 1)
                print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(Pos, Vel, Cur))

                # enableSuccess = aios.AIOSEnable(Server_IP_list[i], 1)
                # aios.controlMode(3, Server_IP_list[i], 1)
                aios.setPosition(Pos, 0, 0, True, Server_IP_list[i], 1)
                aios.trapezoidalMove(0 , True, Server_IP_list[i], 1)
                time.sleep( 1 )
                aios.trapezoidalMove(3000 , True, Server_IP_list[i], 1)
                time.sleep( 1 )


                aios.AIOSDisable(Server_IP_list[i], 1)



if __name__ == '__main__':
    main()
