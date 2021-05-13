########利用optimize.leastsq函数进行拟合
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

Y = np.array([7, 16, 25, 33, 38, 46, 56, 68, 82, 97, 111, 122, 132, 140, 148, 155, 164, 176, 189, 204, 219, 231, 242, 248, 255, 258, 262, 270, 280, 295, 309, 325, 338, 347, 355, 362, 368, 374, 382, 391, 402, 415, 427, 437, 446, 454, 460, 465, 471, 477, 485, 493, 504, 515, 527, 539, 552, 560, 571, 579, 586, 594, 602, 613, 624, 637, 650, 662, 671, 679, 687, 695, 704, 712, 725, 738, 751, 765, 775, 786, 795, 802, 806, 813, 820, 830, 845, 859, 875, 889, 899, 908, 916, 921, 929, 938, 950, 962, 976, 987, 998, 1007, 1014, 1020, 1026, 1031, 1038, 1045, 1053, 1067, 1083, 1096, 1110, 1121, 1131, 1140, 1148, 1154, 1162, 1173, 1185, 1200, 1213, 1225, 1235, 1244, 1251, 1259, 1268, 1276, 1286, 1298, 1314, 1327, 1340, 1352, 1361, 1367, 1372, 1379, 1387, 1396, 1409, 1422, 1435, 1447, 1455, 1463, 1470, 1477, 1484, 1492, 1501, 1515, 1527, 1542, 1554, 1563, 1570, 1577, 1582, 1586, 1595, 1606, 1619, 1632, 1647, 1658, 1668, 1676, 1683, 1690, 1698, 1706, 1718, 1731, 1744, 1758, 1769, 1778, 1787, 1795, 1803, 1811, 1822, 1835, 1847, 1860, 1872, 1883, 1894, 1903, 1912, 1920, 1928, 1935, 1946, 1959, 1973, 1986, 2000, 2009, 2018, 2027, 2034, 2042, 2049, 2061, 2075, 2090, 2105, 2119, 2130, 2139, 2145, 2150, 2157, 2164, 2177, 2192, 2208, 2223, 2236, 2245, 2252, 2258, 2263, 2272, 2283, 2296, 2311, 2326, 2338, 2348, 2354, 2359, 2367, 2373, 2383, 2393, 2405, 2420, 2433, 2446, 2456, 2464, 2473, 2480, 2487, 2498, 2510, 2522, 2533, 2546, 2554, 2563, 2570, 2579, 2587, 2597, 2605, 2616, 2629, 2642, 2654, 2667, 2676, 2685, 2692, 2699, 2706, 2715, 2727, 2739, 2752, 2764, 2776, 2786, 2795, 2803, 2809, 2817, 2826, 2839, 2854, 2869, 2884, 2895, 2904, 2911, 2915, 2920, 2931, 2944, 2960, 2977, 2993, 3005, 3014, 3022, 3028, 3034, 3043, 3053, 3067, 3081, 3097, 3110, 3119, 3128, 3135, 3142, 3149, 3158, 3170, 3183, 3197, 3212, 3224, 3235, 3245, 3253, 3260, 3266, 3274, 3283, 3295, 3308, 3323, 3334, 3344, 3352, 3359, 3366, 3372, 3380, 3388, 3400, 3415, 3427, 3438, 3448, 3458, 3464, 3470, 3475, 3478, 3485, 3493, 3505, 3518, 3529, 3543, 3554, 3564, 3571, 3578, 3584, 3592, 3602, 3616, 3630, 3644, 3657, 3665, 3673, 3679, 3686, 3693, 3701, 3711, 3722, 3739, 3752, 3765, 3777, 3787, 3797, 3804, 3813, 3820, 3832, 3844, 3859, 3872, 3883, 3893, 3902, 3910, 3918, 3926, 3934, 3946, 3959, 3971, 3985, 3998])
X = np.arange(Y.shape[0])

print(Y.shape[0])
print(X.shape[0])

print(X)
"计算以p为参数的直线和原始数据之间的残差"
def residuals(p):
    k,b = p
    return Y - (k*X + b)
# leastsq使得residuals()的输出数姐的平方和最小，参数的初始值为[1,0]
r = optimize.leastsq(residuals, [1, 0])
k, b = r[0]
print ("k =" ,k, "b =" ,b)
#####将计算结果可视化
XX=np.arange(0,Y.shape[0],1)
YY=k*XX+b

Z = YY - Y
print(Z)

# plt.plot(XX, YY, color='red', label = "line 1")
# plt.plot(X, Y, color='green', label = "line 2")
plt.plot(X, Z, color='green', label = "line 2")
plt.xlabel('X')
plt.ylabel('Y')
plt.show()