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

raw_b = raw_b[::-1]
raw = (raw_f + raw_b)/2

print("raw_offset = %d" %(raw_offset))

print("\n\r Encoder non-linearity compensation table\n\r")
print(" Sample Number : Lookup Index : Lookup Value\n\r\n\r")

lut = [0 for i in range(n_lut)]    # Filling with 0

for i in range(n_lut):
    ind = int(float(raw_offset)/31.25) + i
    if ind > (n_lut-1):
        ind -= n_lut
    lut[ind] = (error_filt[i*NPP] - mean)
    print(i, ind, lut[ind])
    time.sleep(0.001)

offset_lut = lut
raw_list = []
offset_1_list = []
offset_2_list = []
off_interp_list = []
angle = []

for i in range(n):
    raw_ = int(raw[i]/31.25)
    raw_list.append(raw_)
    off_1 = offset_lut[raw_]
    if raw_+1 < 128: 
        off_2 = offset_lut[int((raw_+1))]
    offset_1_list.append(off_1)
    offset_2_list.append(off_2)
    off_interp = off_1 + ((off_2 - off_1)*(raw[i] - raw_*31.25)/31.25)     # Interpolate between lookup table entries
    off_interp_list.append(off_interp)
    angle.append(raw[i] + off_interp)                                              # Correct for nonlinearity with lookup table from calibration


print(error_f)
print(error_b)

# plt.plot(error_f)
# plt.plot(error_b)
# plt.plot(error)
# error_filt = list(map(int,error_filt))
# plt.plot(error_filt)
# plt.plot(lut)
plt.plot(offset_1_list)
# plt.plot(offset_2_list)
plt.plot(off_interp_list)
plt.ylabel('error_b')
plt.show()