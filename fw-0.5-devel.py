import aios
import time
import threading
import numpy as np

Server_IP_list = ['192.168.2.40']
# Server_IP_list = []



def main():

    # Server_IP_list = aios.broadcast_func()
    if Server_IP_list:

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r vbus_voltage\n")
        print('\n')
     
        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r axis1.encoder.is_ready\n")
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r config.dc_bus_undervoltage_trip_level\n")
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r axis1.encoder.count_in_cpr\n")
        print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r axis1.encoder.config.offset\n")
        print('\n')


        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.encoder.config.offset 1000\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.encoder.is_ready 1\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w config.uart_baudrate 2000000\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "ss\n") # save motor drive config
        # print('\n')


        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.encoder.is_ready\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.requested_state 8\n")
        # print('\n')


        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.controller.config.input_mode 1\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.current 5\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.finish_on_vel 1\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.vel 1600\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.config.general_lockin.accel 400\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.requested_state 9\n")
        # print('\n')

        # time.sleep(5)

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.requested_state 1\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r config.dc_bus_undervoltage_trip_level\n")
        # print('\n')
        
        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w config.dc_bus_undervoltage_trip_level 12\n")
        # print('\n')
        
        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r config.dc_bus_undervoltage_trip_level\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.encoder.config.offset\n")
        # print('\n')
        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.controller.config.vel_ramp_rate 400000.00\n")
        # print('\n')
        
        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.controller.config.vel_ramp_rate\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.motor.config.direction\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "ih\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "if\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "is\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "sr\n")
        # print('\n')
        
        # for i in range(len(Server_IP_list)):
        #     start = time.time()
        #     aios.passthrough(Server_IP_list[i], "v 1 1.0 0.0 0.0\n")
        #     latency = time.time() - start
        # print('\n')

        # print(latency*1000)
        

        # time.sleep(2)

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "v 1 4.0 0.0 0.0\n")
        # print('\n')

        # time.sleep(2)

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "v 1 8.0 0.0 0.0\n")
        # print('\n')

        # time.sleep(2)


        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.motor.get_inverter_temp\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.error\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.motor.error\n")
        # print('\n')


        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.controller.error\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.error 0\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.motor.error 0\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.encoder.error 0\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "w axis1.controller.error 0\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.error\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.motor.error\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.encoder.error\n")
        # print('\n')

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "r axis1.controller.error\n")
        # print('\n')

        for i in range(len(Server_IP_list)):
            aios.passthrough(Server_IP_list[i], "r config.uart_baudrate\n")
        print('\n')

        # for j in range(1000):
        #     for i in range(len(Server_IP_list)):
        #         start = time.time()
        #         aios.passthrough_pt(Server_IP_list[i], "f 1\n")
        #         latency = time.time() - start
        #         print(latency*1000)
        #     print('\n')
        #     time.sleep(0.01)

        # for i in range(len(Server_IP_list)):
        #     aios.passthrough(Server_IP_list[i], "c 1 0.0\n")
        # print('\n')



if __name__ == '__main__':
    main()
