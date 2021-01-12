import threading
import socket
import time
import json
import numpy as np
from enum import Enum
from math import *

# Initialize the actuator state
class AxisState(Enum):
        AXIS_STATE_IDLE = 1
        AXIS_STATE_ENABLE = 8

# Actuator control mode
class ControlMode(Enum):
        VOLTAGE_CONTROL = 0
        CURRENT_CONTROL = 1
        VELOCITY_CONTROL = 2
        POSITION_CONTROL = 3
        TRAJECTORY_CONTROL = 4

start_time = 0
stop_time = 0



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(2)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT_rt = 2333  # Real-time control data port, ie. speed, position, current and other real-time data
PORT_srv = 2334 # Low priority service data port. ie, parameter setting and reading


# s.bind(('', PORT_srv))

network = '<broadcast>'
network_multicast = '192.168.2.255'

print('Listening for broadcast at ', s.getsockname())

# AIOS enable
# Parameters: including device IP and motor number
# Each AIOS can control two motors, M0 and M1
def enable(server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/requested_state',
        'property' : AxisState.AXIS_STATE_ENABLE.value
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


# AIOS Disable
# Parameters: including device IP and motor number
# Each AIOS can control two motors, M0 and M1
def disable(server_ip, motor_number):
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


# AIOS Get current status
# Parameters: including device IP
# Get AIOS Get current status
def getState(server_ip, motor_number):
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

# AIOS Get root attributes
# Parameters: including device IP
# Get all basic attributes of AIOS, including serial number, bus voltage, motor temperature, inverter temperature, version number
def getRoot(server_ip):
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

# AIOS Get Root Config property
# Parameters: including device IP
# Get AIOS bus voltage over-voltage and under-voltage protection threshold
def getRootConfig(server_ip):
    data = {
        'method' : 'GET',
        'reqTarget' : '/config',
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

# AIOS set Root Config properties
#Parameter: The protection threshold of bus voltage overvoltage and undervoltage
# Return success or failure
def setRootConfig(dict, server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/config',
        'dc_bus_overvoltage_trip_level' : 30,
        'dc_bus_undervoltage_trip_level' : 10,
    }
    data['dc_bus_overvoltage_trip_level'] = dict['dc_bus_overvoltage_trip_level']
    data['dc_bus_undervoltage_trip_level'] = dict['dc_bus_undervoltage_trip_level']
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS save configuration
# Parameters: including device IP
def saveConfig(server_ip):
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

# AIOS clear configuration
# Parameters: including device IP
def eraseConfig(server_ip):
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

# AIOS restart
# Parameters: including device IP
def reboot(server_ip):
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

# AIOS restart the motor drive 
# Parameters: including device IP
def rebootMotorDrive(server_ip):
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

# AIOS OTA upgrade
# Parameters: including device IP
def OTAupdate(server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/',
        'property' : 'OTA_update'
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

# AIOS get error code
# Parameters: including device IP
def getError(server_ip, motor_number):
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
def clearError(server_ip, motor_number):
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
def getMotionCtrlConfig(server_ip, motor_number):
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
def setMotionCtrlConfig(dict, server_ip, motor_number):
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
def setTrapTraj(dict, server_ip, motor_number):
    data = {
        'method' : 'SET',
        'reqTarget' : '/m0/trap_traj',
        'accel_limit' : 320000,
        'decel_limit' : 320000,
        'vel_limit' : 200000
    }
    if motor_number == 0:
        data['reqTarget'] = '/m0/trap_traj'
    elif motor_number == 1:
        data['reqTarget'] = '/m1/trap_traj'
    data['accel_limit'] = dict['accel_limit']
    data['decel_limit'] = dict['decel_limit']
    data['vel_limit'] = dict['vel_limit']
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
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    # if reply_enable:
    #     try:
    #         data, address = s.recvfrom(1024)
    #         # print('Server received from {}:{}'.format(address, data.decode('utf-8')))
    #         json_obj = json.loads(data.decode('utf-8'))
    #         print("Position = %.2f, Velocity = %.0f, Current = %.4f \n" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
    #     except socket.timeout: # fail after 1 second of no activity
    #         print("Didn't receive anymore data! [Timeout]")

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
        'method' : 'XET',
        'reqTarget' : '/',
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))

def receive_func():
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        return True
    except socket.timeout: # fail after 1 second of no activity
        return False
        print("Didn't receive anymore data! [Timeout]")


# IO_Module 设置IO_State状态
# 参数：PWM0_CH PWM1_CH SERVO0 SERVO1
# 参数取值范围: PWM0_CH,PWM1_CH[0~65535], SERVO0,SERVO1[0~180]
# 返回 AI0 AI1 DI0 DI1
def setIOState(dict, reply_enable, server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/IO_State',
        'reply_enable' : True
    }
    data['reply_enable'] = reply_enable
    data['PWM0_CH'] = dict['PWM0_CH']
    data['PWM1_CH'] = dict['PWM1_CH']
    data['SERVO0'] = dict['SERVO0']
    data['SERVO1'] = dict['SERVO1']
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    if reply_enable:
        try:
            data, address = s.recvfrom(1024)
            print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            # json_obj = json.loads(data.decode('utf-8'))
            # print("Position = %.2f, Velocity = %.0f, Current = %.4f \n" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
        except socket.timeout: # fail after 1 second of no activity
            print("Didn't receive anymore data! [Timeout]")

# IO_Module 获取IO_State状态
# 返回值PWM0_CH,PWM1_CH[0~65535], SERVO0,SERVO1[0~180]
# 返回 AI0[0~4096] AI1[0~4096] DI0[0,1] DI1[0,1] PWM0_CH,PWM1_CH[0~65535], SERVO0,SERVO1[0~180]
def getIOState(server_ip):
    data = {
        'method' : 'GET',
        'reqTarget' : '/IO_State',
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_rt))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        # json_obj = json.loads(data.decode('utf-8'))
        # print("Position = %.2f, Velocity = %.0f, Current = %.4f \n" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# aios 获取network_setting状态
# 返回值
def getNetworkSetting(server_ip):
    data = {
        'method' : 'GET',
        'reqTarget' : '/network_setting',
    }
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        # json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# aios 设置network_setting状态
# 返回值
def setNetworkSetting(dict, server_ip):
    data = {
        'method' : 'SET',
        'reqTarget' : '/network_setting',
        'DHCP_enable' : 'True',
    }
    data['DHCP_enable'] = dict['DHCP_enable']
    data['SSID'] = dict['SSID']
    data['password'] = dict['password']
    if dict['DHCP_enable'] == False:
        data['staticIP'] = dict['staticIP']
        data['gateway'] = dict['gateway']
        data['subnet'] = dict['subnet']
        data['dns_1'] = dict['dns_1']
        data['dns_2'] = dict['dns_2']
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        # json_obj = json.loads(data.decode('utf-8'))
        # print("Position = %.2f, Velocity = %.0f, Current = %.4f \n" %(json_obj.get('position'), json_obj.get('velocity'), json_obj.get('current')))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")

# AIOS passthrough
# 参数：包括设备IP 电机号
# 无返回
def passthrough(server_ip, tx_messages):
    data = {
        'method' : 'SET',
        'reqTarget' : '/passthrough',
        'tx_messages' : ''
    }
    data['tx_messages'] = tx_messages
    json_str = json.dumps(data)
    print ("Send JSON Obj:", json_str)
    s.sendto(str.encode(json_str), (server_ip, PORT_srv))
    try:
        data, address = s.recvfrom(1024)
        print('Server received from {}:{}'.format(address, data.decode('utf-8')))
        json_obj = json.loads(data.decode('utf-8'))
    except socket.timeout: # fail after 1 second of no activity
        print("Didn't receive anymore data! [Timeout]")
        
# 广播查询局域网下的全部 AIOS
# 参数：无
# 返回 成功 失败 超时
def broadcast_func():
    timeout = 3
    found_server = False
    address_list = []
    i = 0

    s.sendto('Is any AIOS server here?'.encode('utf-8'), (network, PORT_srv))
    print('\n')

    start = time.time();
    while True:
        try:
            data, address = s.recvfrom(1024)
            address_list.append(address[0])
            print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            json_obj = json.loads(data.decode('utf-8'))
            found_server = True
        except socket.timeout: # fail after 1 second of no activity
            if found_server:
                print('\n')
                print('found servers')
                print(address_list)
                print('lookup Finished! \n')
                time.sleep(2)
                return address_list
            else:
                print("Do not have any server! [Timeout] \n")
                return False
            break

    print('\n')


def multicast_func():
    found_server = False
    address_list = []

    s.sendto('Is any AIOS server here?'.encode('utf-8'), (network_multicast, PORT_srv))
    print('\n')

    while True:
        try:
            data, address = s.recvfrom(1024)
            address_list.append(address[0])
            print('Server received from {}:{}'.format(address, data.decode('utf-8')))
            json_obj = json.loads(data.decode('utf-8'))
            found_server = True
        except socket.timeout: # fail after 1 second of no activity
            if found_server:
                print('\n')
                print('found servers')
                print(address_list)
                print('lookup Finished! \n')
                time.sleep(2)
                return address_list
            else:
                print("Do not have any server! [Timeout] \n")
                return False
            break

    print('\n')
