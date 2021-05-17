import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import time

NPP = 21
n = 128*NPP 
window = 128
n_lut = 128
lut = []
CPR = 4000

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

# error_f = [1, 2, 3, 34]
# error_b = [2, 92, 94, 345, 0]

# np.save('error_f.npy',error_f) 
# np.save('error_b.npy',error_b) 

error_f = np.load('error_f.npy')
error_b = np.load('error_b.npy')
raw_f = np.load('raw_f.npy')
raw_b = np.load('raw_b.npy')

error_b = error_b[::-1]

error = (error_f + error_b)/2                  # Average the forward and back directions

error_filt = [0 for i in range(len(error))]    # Filling with 0
mean = 0
for i in range(n):
    for j in range(window):
        ind = -window/2 + j + i                # Indexes from -window/2 to + window/2
        if ind < 0:
            ind += n                           # Moving average wraps around
        elif ind > n-1:
            ind -= n
        error_filt[i] += error[int(ind)]/float(window)
    mean += error_filt[i]/n

raw_offset = (raw_f[0] + raw_b[n-1])/2

print("raw_offset = %d" %(raw_offset))

print("\n\r Encoder non-linearity compensation table\n\r")
print(" Sample Number : Lookup Index : Lookup Value\n\r\n\r")

lut = [0 for i in range(n_lut)]    # Filling with 0

for i in range(n_lut):
    ind = int(raw_offset/128) + i
    if ind > (n_lut-1):
        ind -= n_lut
    lut[ind] = (error_filt[i*NPP] - mean)
    print(i, ind, lut[ind])
    time.sleep(0.001)



# b, a = signal.butter(8, 0.03, 'lowpass')   #配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, error)  #data为要过滤的信号

# b, a = signal.butter(10, [0.02,0.9], 'bandstop')   #配置滤波器 8 表示滤波器的阶数
# filtedData = signal.filtfilt(b, a, error)  #data为要过滤的信号

# filtedData = moving_average(error, 100)

# filtedData = filtedData.shift(50)

# data = pd.Series(error)
# filtedData = data.rolling(window=50).mean()
# moving_averages = windows.mean()

# moving_averages_list = moving_averages.tolist()
# without_nans = moving_averages_list[window_size - 1:]

print(error_f)
print(error_b)

plt.plot(error_f)
plt.plot(error_b)
plt.plot(error)
# error_filt = list(map(int,error_filt))
plt.plot(error_filt)
plt.plot(lut)
plt.ylabel('error_b')
plt.show()