#!/usr/bin/env python3
# from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
# from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, ColorSensor

from DV.actsys import conversion, actuator
from DV.meassys import sensor
from PG.actsys import gain_balancing
from PG.spg import p2p_setpoint
from facilities import trace

import numpy as np

import SYSxCONST as sysxconst
import DV.DVxCONST as dvxconst

import time
import pause

begin_point = 0     # m
end_point = 0.2     # m

time_signal, pos_signal, vel_signal, acc_signal, jer_signal = p2p_setpoint.setpoint_3th_order(begin_point, end_point)

# start download DV parameters

# offset_calibrated = True
axis = 'Rx'
calibration_mode = 'GYRO-ANG'
# static_offset = 1324
# gain_offset = 325
#
# Rx = dvxconst.GyroOffsetsCalibrated(axis)
# Rx.set_values(offset_calibrated, calibration_mode, static_offset, gain_offset)
#
# print(Rx.get_values().offset_calibrated)
# print(Rx.get_values().axis)
# print(Rx.get_values().calibration_mode)
# print(Rx.get_values().static_offset)
# print(Rx.get_values().gain_offset)

sensor.download_gyro_parameters(axis, calibration_mode)

dvxconst.GyroOffsetsCalibrated.get_instance().set_values_rx(False, 'GYRO-ANG', 1, 2)
dvxconst.GyroOffsetsCalibrated.get_instance().set_values_ry(False, 'GYRO-ANG', 3, 4)
# sensor.write_calibrated_parameters()
sensor.restore_default_parameters()

# colorsens = ColorSensor(INPUT_4)
# colorsens.mode = 'COL-COLOR'
#
# RunSensorCalibration = True
#
# if RunSensorCalibration:
#
#     # test constants
#     test_duration = 1
#     # number_of_samples = 20
#     calibration_mode = 'GYRO-ANG'
#
#     sensor.set_mode_gyro_rx(calibration_mode)
#
#     gyro_rx_data, gyro_rx_time = sensor.read_gyro_rx(test_duration)
#     gyro_rx_mean = np.mean(gyro_rx_data)
#
#     print(gyro_rx_data)
#     print(np.diff(gyro_rx_time))
#     print(gyro_rx_time)
#     print(gyro_rx_mean)
#
#
# # Step1: Generate setpoint (acceleration, velocity, position, and time)
#
# # Step2: send setpoint information to network -- run
#
#
#
#
# # t_end = time.time() + 20
# #
# # sensor.set_mode_gyro_rx('GYRO-ANG')
# #

t_end = time.time() + time_signal[-1]
t_start = time.time()

setpoint_v = np.zeros((vel_signal.shape[0],3))
# setpoint_v[:, 1] = np.transpose(vel_signal)

gain_balancing_matrix = gain_balancing.nominal()

time_old = time.time()

for sample_id in range(time_signal.shape[0]):

    setpoint_rpm = conversion.mps_to_rpm(setpoint_v[sample_id][:])

    setpoint_raw = np.matmul(gain_balancing_matrix, setpoint_rpm)

    actual_speed = np.zeros(3)

    # actual_speed[0] = actuator.drive_motor_front(setpoint_raw[0])
    # actual_speed[1] = actuator.drive_motor_back_left(setpoint_raw[1])
    # actual_speed[2] = actuator.drive_motor_back_right(setpoint_raw[2])

    pause.until(t_start + (sample_id * 1 / sysxconst.SystemConstants().sample_rate))
    time_old = time.time()

    print('Rx: ' + str(sensor.read_gyro_rx()))
    print('Ry: ' + str(sensor.read_gyro_ry()))

actuator.drive_motor_front(0)
actuator.drive_motor_back_left(0)
actuator.drive_motor_back_right(0)

# while time.time() < t_end:
#
#     # actual_time = 20-(t_end-time.time())
#     #
#     # setpoint_v = [0, 0.3, -0.1]  # m/s
#
#     setpoint_rpm = conversion.mps_to_rpm(setpoint_v)
#
#     gain_balancing_matrix = gain_balancing.nominal()
#
#     setpoint_raw = np.matmul(gain_balancing_matrix,setpoint_rpm)
#     actual_speed = np.zeros(3)
#
#     actual_speed[0] = actuator.drive_motor_front(setpoint_raw[0])
#     actual_speed[1] = actuator.drive_motor_back_left(setpoint_raw[1])
#     actual_speed[2] = actuator.drive_motor_back_right(setpoint_raw[2])
#
# #     gyro_rx_data = sensor.read_gyro_rx(10)
# #
# #     print(gyro_rx_data)
# #
# #     # print([actual_time, actual_speed, setpoint_raw])
# #     # trace.collect_data([actual_time, actual_speed, setpoint_raw])
# #
# actuator.drive_motor_front(0)
# actuator.drive_motor_back_left(0)
# actuator.drive_motor_back_right(0)

