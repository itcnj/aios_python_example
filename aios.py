import threading
import socket
import time
import json
import numpy as np
from enum import Enum
from math import *

# 初始化执行器状态
class AxisState(Enum):
        AXIS_STATE_UNDEFINED = 0
        AXIS_STATE_IDLE = 1
        AXIS_STATE_STARTUP_SEQUENCE = 2
        AXIS_STATE_FULL_CALIBRATION_SEQUENCE = 3
        AXIS_STATE_MOTOR_CALIBRATION = 4
        AXIS_STATE_SENSORLESS_CONTROL = 5
        AXIS_STATE_ENCODER_INDEX_SEARCH = 6
        AXIS_STATE_ENCODER_OFFSET_CALIBRATION = 7
        AXIS_STATE_CLOSED_LOOP_CONTROL = 8

# 执行器控制模式
class ControlMode(Enum):
        CTRL_MODE_VOLTAGE_CONTROL = 0
        CTRL_MODE_CURRENT_CONTROL = 1
        CTRL_MODE_VELOCITY_CONTROL = 2
        CTRL_MODE_POSITION_CONTROL = 3
        CTRL_MODE_TRAJECTORY_CONTROL = 4

start_time = 0
stop_time = 0



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3.0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT_rt = 2333  # 高实时控制数据端口 速度 位置 电流等高实时数据
PORT_srv = 2334 # 低优先级服务数据端口 参数设置和读取


# s.bind(('', PORT_srv))

network = '<broadcast>'

print('Listening for broadcast at ', s.getsockname())

# AIOS 使能
# 参数：包括设备IP和电机号
# 每个AIOS可以控制两个电机 分别为M0和M1 用0,1区别
def AIOSEnable(server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/requested_state',
        'property' : AxisState.AXIS_STATE_CLOSED_LOOP_CONTROL.value
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/requested_state'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/requested_state'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")
        return False

    if json_obj.get('status') == 'OK':
        return True
    else:
        print("Recv Data Error !")
        return False

# AIOS 失能
# 参数：包括设备IP和电机号
# 每个AIOS可以控制两个电机 分别为M0和M1 用0,1区别
def AIOSDisable(server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/requested_state',
        'property' : AxisState.AXIS_STATE_IDLE.value
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/requested_state'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/requested_state'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))

    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 获取当前状态
# 参数：包括设备IP
# 获取AIOS 获取当前状态
def AIOSGetState(server_ip, motor_number):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m0/requested_state',
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/requested_state'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/requested_state'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))

    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 获取根属性
# 参数：包括设备IP
# 获取AIOS 全部基本属性 包括序列号 母线电压 电机温度 逆变器温度 版本号
def AIOSGetRoot(server_ip):
    data = {
        'method' : 'GET',
        'reqTarget' : '/',
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 保存配置
# 参数：包括设备IP
def AIOSSaveConfig(server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/',
        'property' : 'save_config'
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 清除配置
# 参数：包括设备IP
def AIOSEraseConfig(server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/',
        'property' : 'erase_config'
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 重启
# 参数：包括设备IP
def AIOSReboot(server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/',
        'property' : 'reboot'
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 只重启电机驱动部分
# 参数：包括设备IP
def AIOSRebootMotorDrive(server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/',
        'property' : 'reboot_motor_drive'
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 获取错误代码
# 参数：包括设备IP
def AIOSGetError(server_ip, motor_number):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m0/error',
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/error'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/error'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 清除错误
# 参数：包括设备IP
def AIOSClearError(server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/error',
        'clear_error' : True
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/error'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/error'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 获取执行器位置 速度 电流
# 参数：包括设备IP 电机号
# 以元组方式返回 位置 速度 电流
def getCVP(server_ip, motor_number):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m0/CVP',
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/CVP'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/CVP'
    json_str = json.dumps(data)
    # print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    try:
        data, address = s.recvfrom(1024)
        # print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
        if json_obj.get('status') == 'OK':
            return json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 编码器校准 (初期版本电机编码器需要先校准才能使用，后期完善后不需要此操作)
# 参数：包括设备IP 电机号
# 无返回
def encoderOffsetCalibration(server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/requested_state',
        'property' : AxisState.AXIS_STATE_ENCODER_OFFSET_CALIBRATION.value
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/requested_state'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/requested_state'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 获取编码器是否准备好 (如果没有准备好 则执行编码器校准)
# 参数：包括设备IP 电机号
# 无返回
def encoderIsReady(server_ip, motor_number):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m0/encoder/is_ready',
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/encoder/is_ready'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/encoder/is_ready'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive data! [Timeout]")

    if json_obj.get('status') == 'OK':
        return json_obj.get('property')
    else:
        print("Recv Data Error !")

# AIOS 设置控制模式
# 参数：包括设备IP 控制模式 电机号
# 无返回
def controlMode(ctrlMode, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/controller/config',
        'control_mode' : 3
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/controller/config'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/controller/config'

    data['control_mode'] = ctrlMode
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 重新设置电机位置
# 参数：位置参数 包括设备IP 电机号
# 无返回
def setLinearCount(set_linear_count, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/encoder',
        'set_linear_count' : 0
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/encoder'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/encoder'

    data['set_linear_count'] = set_linear_count
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")


# AIOS 获取执行器PID控制器参数
# 参数：包括设备IP 电机号
# 以元组方式返回 控制模式 位置比例增益 速度比例增益 速度积分增益 速度限制 速度限制容差
def getPIDControllerConfig(server_ip, motor_number):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m0/controller/config',
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/controller/config'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/controller/config'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
        if json_obj.get('status') == 'OK':
            return json_obj.get('control_mode'), json_obj.get('pos_gain'), json_obj.get('vel_gain'), json_obj.get('vel_integrator_gain'), json_obj.get('vel_limit'), json_obj.get('vel_limit_tolerance')
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 设置执行器PID控制器参数
# 参数：位置比例增益 速度比例增益 速度积分增益 速度限制 速度限制容差
# 返回 成功或失败
def setPIDControllerConfig(dict, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/controller/config',
        'pos_gain' : 20,
        'vel_gain' : 0.0005,
        'vel_integrator_gain' : 0.0002,
        'vel_limit' : 40000,
        'vel_limit_tolerance' : 1.2,
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/controller/config'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/controller/config'
    data['pos_gain'] = dict['pos_gain']
    data['vel_gain'] = dict['vel_gain']
    data['vel_integrator_gain'] = dict['vel_integrator_gain']
    data['vel_limit'] = dict['vel_limit']
    data['vel_limit_tolerance'] = dict['vel_limit_tolerance']
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 获取执行器MotorConfig参数
# 参数：包括设备IP 电机号
# 以元组方式返回 电机电流限制 电流限制余量 逆变器温度下线 逆变器温度上限 电流控制带宽 包括设备IP 电机号
def getMotorConfig(server_ip, motor_number):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m1/motor/config',
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/motor/config'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/motor/config'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
        if json_obj.get('status') == 'OK':
            return json_obj.get('current_lim'), json_obj.get('current_lim_margin'), json_obj.get('inverter_temp_limit_lower'), json_obj.get('inverter_temp_limit_upper'), json_obj.get('requested_current_range'), json_obj.get('current_control_bandwidth')
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 设置执行器MotorConfig参数
# 参数：电机电流限制 电流限制余量 逆变器温度下线 逆变器温度上限 电流控制带宽 包括设备IP 电机号
# 返回 成功或失败
def setMotorConfig(dict, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m1/motor/config',
        'current_lim' : 15,
        'current_lim_margin' : 5,
        'inverter_temp_limit_lower' : 100,
        'inverter_temp_limit_upper' : 120,
        'requested_current_range' : 30,
        'current_control_bandwidth' : 1000,
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/motor/config'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/motor/config'
    data['current_lim'] = dict['current_lim']
    data['current_lim_margin'] = dict['current_lim_margin']
    data['inverter_temp_limit_lower'] = dict['inverter_temp_limit_lower']
    data['inverter_temp_limit_upper'] = dict['inverter_temp_limit_upper']
    data['requested_current_range'] = dict['requested_current_range']
    data['current_control_bandwidth'] = dict['current_control_bandwidth']
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
        if json_obj.get('status') == 'OK':
            return json_obj.get('current_lim'), json_obj.get('current_lim_margin'), json_obj.get('inverter_temp_limit_lower'), json_obj.get('inverter_temp_limit_upper'), json_obj.get('requested_current_range'), json_obj.get('current_control_bandwidth')
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 获取执行器梯形模式轨迹参数
# 参数：包括设备IP 电机号
# 以元组方式返回 梯形加速度 梯形减速度 梯形速度限制
def getTrapTraj(server_ip, motor_number):
    data = {
        'method' : 'GET',
        'reqTarget' : '/m0/trap_traj',
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/trap_traj'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/trap_traj'
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
        if json_obj.get('status') == 'OK':
            return json_obj.get('accel_limit'), json_obj.get('decel_limit'), json_obj.get('vel_limit')
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 设置执行器梯形模式轨迹参数
# 参数：包括梯形加速度 梯形减速度 梯形速度限制 设备IP 电机号
# 以元组方式返回 成功或失败
def setTrapTraj(accel_limit, decel_limit, vel_limit, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/trap_traj',
        'accel_limit' : 0,
        'decel_limit' : 0,
        'vel_limit' : 0
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/trap_traj'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/trap_traj'
    data['accel_limit'] = accel_limit
    data['decel_limit'] = decel_limit
    data['vel_limit'] = vel_limit
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")


# AIOS 速度斜坡模式使能
# 参数：包括设备IP 控制模式 电机号
# 无返回
def velRampEnable(enable, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/controller',
        'vel_ramp_enable' : False
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/controller'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/controller'
    data['vel_ramp_enable'] = enable
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 速度斜坡模式 设置目标速度
# 参数：包括设备IP 目标速度 电机号
# 无返回
def velRampTarget(target, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/controller',
        'vel_ramp_target' : 0
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/controller'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/controller'
    data['vel_ramp_target'] = target
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS 设置梯形运动轨迹目标位置
# 参数：位置 反馈使能 设备IP 电机号
# 返回 位置 速度 电流
def trapezoidalMove(position, reply_enable, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/trapezoidalMove',
        'property' : 0,
        'reply_enable' : True
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/trapezoidalMove'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/trapezoidalMove'
    data['property'] = position
    data['reply_enable'] = reply_enable
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    if reply_enable:
        try:
            data, address = s.recvfrom(1024)
            # print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            json_obj = json.loads(data.decode('utf-8'))
            print("Position = %.2f, Velocity = %.0f, Current = %.4f \n" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
        except socket.timeout: # fail after 1 second of no activity
            print("Didn't receive anymore data! [Timeout]")

# AIOS 位置控制
# 参数：目标位置 速度前馈 电流前馈 设备IP 电机号
# 返回 位置 速度 电流
def setPosition(position, velocity_ff, current_ff, reply_enable, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/setPosition',
        'reply_enable' : False,
        'position' : 0,
        'velocity_ff' : 0,
        'current_ff' : 0
    }
    data['reply_enable'] = reply_enable
    if motor_number == 0:
        data['reqTarget'] = '/m0/setPosition'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/setPosition'
    data['position'] = position
    data['velocity_ff'] = velocity_ff
    data['current_ff'] = current_ff
    json_str = json.dumps(data)
    # print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    if reply_enable:
        try:
            data, address = s.recvfrom(1024)
            # print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            json_obj = json.loads(data.decode('utf-8'))
            print("Position = %.2f, Velocity = %.0f, Current = %.4f \n" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
        except socket.timeout: # fail after 1 second of no activity
            print("Didn't receive anymore data! [Timeout]")

# AIOS 速度控制
# 参数 速度 电流前馈 设备IP 电机号
# 返回 位置 速度 电流
def setVelocity(velocity, current_ff, reply_enable, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/setVelocity',
        'velocity' : 0,
        'current_ff' : 0
    }
    data['reply_enable'] = reply_enable
    if motor_number == 0:
        data['reqTarget'] = '/m0/setVelocity'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/setVelocity'
    data['velocity'] = velocity
    data['current_ff'] = current_ff
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    if reply_enable:
        try:
            data, address = s.recvfrom(1024)
            # print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            json_obj = json.loads(data.decode('utf-8'))
            print("Position = %.2f, Velocity = %.0f, Current = %.4f \n" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
        except socket.timeout: # fail after 1 second of no activity
            print("Didn't receive anymore data! [Timeout]")

# AIOS 电流控制
# 参数：电流 设备IP 电机号
# 返回 位置 速度 电流
def setCurrent(current, reply_enable,server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/setCurrent',
        'current' : 0,
    }
    data['reply_enable'] = reply_enable
    if motor_number == 0:
        data['reqTarget'] = '/m0/setCurrent'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/setCurrent'
    data['current'] = current
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    if reply_enable:
        try:
            data, address = s.recvfrom(1024)
            # print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            json_obj = json.loads(data.decode('utf-8'))
            print("Position = %.2f, Velocity = %.0f, Current = %.4f \n" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
        except socket.timeout: # fail after 1 second of no activity
            print("Didn't receive anymore data! [Timeout]")

def dum_func(server_ip):
    data = {
        'method' : 'GET',
        'reqTarget' : '/',
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))

def receive_func():
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        return True
    except socket.timeout: # fail after 1 second of no activity
        return False
        print("Didn't receive anymore data! [Timeout]")

# 广播查询局域网下的全部 AIOS
# 参数：无
# 返回 成功 失败 超时
def broadcast_func():
    timeout = 3
    found_server = False

    s.sendto('Is any AIOS server here?'.encode('utf-8'), (network, PORT_srv))
    print('\n')

    start = time.time();
    while True:
        try:
            data, address = s.recvfrom(1024)
            print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            json_obj = json.loads(data.decode('utf-8'))
            found_server = True
        except socket.timeout: # fail after 1 second of no activity
            if found_server:
                print('lookuping Finished! \n')
                return True
            else:
                print("Do not have any server! [Timeout] \n")
                return False
            break

    print('\n')