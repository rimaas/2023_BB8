from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, ColorSensor

import json

# import SYSxCONST as constants
#
# import numpy as np
# import time
# import pause

# import PG.PGxCONST as constants

import DV.DVxCONST as dvxconst


def download_gyro_parameters(axis, mode):

    # load nominal or calibrated values (.json) and store these in global class
    # in the .json various offsets are stored for different modes
    # if parameters are uncalibrated, the values defined in GyroOffsetsNominal are used

    # todo: make saved parameters a function of the gyro mode

    print('Download: Gyro DV parameters')

    # load json file
    with open('MC/DVxMCxGYRO.json', 'r') as f:
        gyroaxis_dict = json.load(f)

    inner_struct_rx, inner_struct_ry = dvxconst.dict_to_struct(gyroaxis_dict)

    dvxconst.GyroOffsetsCalibrated.get_instance().set_values_rx(inner_struct_rx.offset_calibrated,
                                                                inner_struct_rx.calibration_mode,
                                                                inner_struct_rx.gain_offset,
                                                                inner_struct_rx.static_offset)

    dvxconst.GyroOffsetsCalibrated.get_instance().set_values_ry(inner_struct_ry.offset_calibrated,
                                                                inner_struct_ry.calibration_mode,
                                                                inner_struct_ry.gain_offset,
                                                                inner_struct_ry.static_offset)

    gyro = GyroSensor()

    if axis == 'Rx':
        gyro = GyroSensor(INPUT_2)
    elif axis == 'Ry':
        gyro = GyroSensor(INPUT_1)
    else:
        print('Unknown axis selected')

    print('Download: Gyro DV parameters - Done!')

    gyro.mode = dvxconst.GyroOffsetsCalibrated.get_instance().rx.calibration_mode
    print('Rx gyro mode set to: ' + dvxconst.GyroOffsetsCalibrated.get_instance().rx.calibration_mode)

    gyro.mode = dvxconst.GyroOffsetsCalibrated.get_instance().ry.calibration_mode
    print('Ry gyro mode set to: ' + dvxconst.GyroOffsetsCalibrated.get_instance().ry.calibration_mode)


def write_parameters():

    # function to write calibrated parameters to .json file

    gyroaxis_dict = dvxconst.struct_to_dict(dvxconst.GyroOffsetsCalibrated.get_instance())

    with open('MC/DVxMCxGYRO.json', 'w') as f:
        json.dump(gyroaxis_dict, f)             


def restore_default_parameters():

    # function to restore default parameters in .json file

    dvxconst.GyroOffsetsCalibrated.get_instance().set_values_rx(False, 'GYRO-ANG', 0, 0)
    dvxconst.GyroOffsetsCalibrated.get_instance().set_values_ry(False, 'GYRO-ANG', 0, 0)

    write_parameters()


def read_gyro_rx():

    gyro_rx = GyroSensor(INPUT_2)

    values = dvxconst.GyroOffsetsCalibrated.get_instance().rx

    sample_output = gyro_rx.value() * values.gain_offset + values.static_offset

    return sample_output


def read_gyro_ry():

    gyro_ry = GyroSensor(INPUT_1)

    values = dvxconst.GyroOffsetsCalibrated.get_instance().ry

    sample_output = gyro_ry.value() * values.gain_offset + values.static_offset

    return sample_output
