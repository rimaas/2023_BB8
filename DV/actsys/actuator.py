from ev3dev2.motor import SpeedRPM as ev3_speed_rpm
from ev3dev2.motor import LargeMotor, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

import DV.DVxCONST as constants


def drive_motor_front(setpoint_rpm):

    motor_front = Motor(OUTPUT_B)

    if setpoint_rpm > constants.Motor().peak:
        setpoint_rpm = constants.Motor().peak

    if setpoint_rpm < -constants.Motor().peak:
        setpoint_rpm = -constants.Motor().peak

    motor_front.on(ev3_speed_rpm(setpoint_rpm))


def drive_motor_back_left(setpoint_rpm):

    motor_back_left = LargeMotor(OUTPUT_A)

    if setpoint_rpm > constants.LargeMotor().peak:
        setpoint_rpm = constants.LargeMotor().peak

    if setpoint_rpm < -constants.LargeMotor().peak:
        setpoint_rpm = -constants.LargeMotor().peak

    motor_back_left.on(ev3_speed_rpm(setpoint_rpm))


def drive_motor_back_right(setpoint_rpm):

    motor_back_right = LargeMotor(OUTPUT_C)

    if setpoint_rpm > constants.LargeMotor().peak:
        setpoint_rpm = constants.LargeMotor().peak

    if setpoint_rpm < -constants.LargeMotor().peak:
        setpoint_rpm = -constants.LargeMotor().peak

    motor_back_right.on(ev3_speed_rpm(setpoint_rpm))
