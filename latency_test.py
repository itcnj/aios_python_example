import aios
import time
import threading
import numpy as np

Server_IP_list = []

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
            aios.getRoot(Server_IP_list[i])

        for i in range(10000):
            start = time.time()
            for j in range(len(Server_IP_list)):
                aios.dum_func(Server_IP_list[j])
            for j in range(len(Server_IP_list)):
                aios.receive_func()
            print((time.time() - start)*1000)
            time.sleep(0.005)


if __name__ == '__main__':
    main()
