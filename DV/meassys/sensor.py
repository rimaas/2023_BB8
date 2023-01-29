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

    # load nominal or calibrated values (.ddf) and store these in global class
    # in the .ddf various offsets are stored for different modes
    # if parameters are uncalibrated, the values defined in GyroOffsetsNominal are used

    # step 1: load .ddf corresponding to input argument "mode"
    # step 2: check if parameters are calibrated
    # step 3: download parameters to GyroOffsetsCalibrated
    #           if uncalibrated, use GyrOffsetsNominal

    # todo: make a global object which includes the offsets for both Rx and Ry

    print('Download: DV parameters')

    GyroAxis = dvxconst.GyroOffsetsCalibrated(axis)

    # # Convert the class to a dictionary
    # gyroaxis_dict = GyroAxis.__dict__
    #
    # with open('MC/DVxMCxGYRO.json', 'w') as f:
    #     json.dump(gyroaxis_dict, f)

    with open('MC/DVxMCxGYRO.json', 'r') as f:
        gyroaxis_dict = json.load(f)

    offset_calibrated = gyroaxis_dict.get('offset_calibrated')
    calibration_mode = gyroaxis_dict.get('calibration_mode')
    static_offset = gyroaxis_dict.get('static_offset')
    gain_offset = gyroaxis_dict.get('gain_offset')

    GyroAxis.set_values(offset_calibrated, calibration_mode, static_offset, gain_offset)

    gyro = GyroSensor()

    if axis == 'Rx':
        gyro = GyroSensor(INPUT_2)
    elif axis == 'Ry':
        gyro = GyroSensor(INPUT_1)
    else:
        print('Unknown axis selected')

    gyro.mode = GyroAxis.get_values().calibration_mode

    print('Download: DV parameters - Done!')

def write_calibrated_parameters():
    # function to write calibrated parameters to .ddf file
    pass


def restore_default_parameters():
    # function to restore parameters in .ddf file
    pass


def read_gyro_rx():

    gyro_rx = GyroSensor(INPUT_2)

    Rx = dvxconst.GyroOffsetsCalibrated('Rx')

    sample_output = gyro_rx.value() * Rx.get_values().gain_offset + Rx.get_values().static_offset

    # sample_rate = constants.SystemConstants().sample_rate
    #
    # gyro_rx = GyroSensor(INPUT_2)
    #
    # sample_output = np.zeros(duration*sample_rate+1)
    # sample_time = np.zeros(duration*sample_rate+1)
    #
    # print('Start sensor trace...')
    #
    # t_start = time.time()
    # sample = 0
    #
    # while time.time() < (t_start + duration):
    #     sample_time[sample] = time.time() - t_start
    #     sample_output[sample] = gyro_rx.value()
    #
    #     pause.until(t_start + (sample * 1/sample_rate))
    #     sample = sample + 1
    #
    # print('Finished tracing')

    return sample_output #, sample_time


def read_gyro_ry():

    gyro_ry = GyroSensor(INPUT_1)

    params = dvxconst.GyroOffsetsRy().get_values()

    sample_output = gyro_ry.value() * params.gain_offset + params.static_offset

    return sample_output