import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

# error_f = [1, 2, 3, 34]
# error_b = [2, 92, 94, 345, 0]

# np.save('error_f.npy',error_f) 
# np.save('error_b.npy',error_b) 

error_f = np.load('error_f.npy')
error_b = np.load('error_b.npy')

error_b = error_b[::-1]

error = (error_f + error_b)/2



# b, a = signal.butter(8, 0.02, 'lowpass')   #配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, error)  #data为要过滤的信号

# b, a = signal.butter(10, [0.02,0.9], 'bandstop')   #配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, error)  #data为要过滤的信号

filtedData = moving_average(error, 50)

filtedData = filtedData.shift(50)

print(error_f)
print(error_b)

plt.plot(error_f)
plt.plot(error_b)
plt.plot(error)
plt.plot(filtedData)
plt.ylabel('error_b')
plt.show()