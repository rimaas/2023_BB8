import numpy as np


# meter per second to rotations per minute
def mps_to_rpm(setpoint_mps):

    diameter_wheels = 0.058  # [m]
    circumference = np.pi * diameter_wheels

    setpoint_rps = np.divide(setpoint_mps, circumference)
    setpoint_rpm = setpoint_rps * 60

    return setpoint_rpm
