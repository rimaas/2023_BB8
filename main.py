#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor

from DV.actsys import conversion, drive
from PG.actsys import gain_balancing

import numpy as np

import time

gyro = GyroSensor()

# MotorBackLeft = LargeMotor( OUTPUT_A )
# MotorBackRight = LargeMotor( OUTPUT_C )
# MotorFront = Motor( OUTPUT_B )

# MotorBackLeft.on_for_rotations(SpeedPercent(5), 1)
# MotorBackRight.on_for_rotations(SpeedPercent(5), 1)
# MotorFront.on_for_rotations(SpeedPercent(5), 1)

GyroRx = GyroSensor( INPUT_2 )
GyroRy = GyroSensor( INPUT_1 )
UltraSensor = UltrasonicSensor( INPUT_3 )

GyroRx.mode = 'GYRO-ANG'
GyroRx.mode = 'GYRO-ANG'
UltraSensor.mode = 'US-DIST-CM'

PROPORTIONAL_GAIN = 0.3

t_end = time.time() + 60 * 0.1

while time.time() < t_end:

    setpoint_v = [2, 0, 0]  # m/s

    setpoint_rpm = conversion.mps_to_rpm(setpoint_v)

    gain_balancing_matrix = gain_balancing.nominal()

    setpoint_raw = np.matmul(gain_balancing_matrix,setpoint_rpm)

    drive.drive_motor_front(setpoint_raw[0])
    drive.drive_motor_back_left(setpoint_raw[1])
    drive.drive_motor_back_right(setpoint_raw[2])

drive.drive_motor_front(0)
drive.drive_motor_back_left(0)
drive.drive_motor_back_right(0)

