import numpy as np
import PG.PGxCONST as constants


def nominal():

    alpha_motor_front = np.radians(constants.GainBalancingNominal().alpha_motor_front)
    alpha_motor_back_left = np.radians(constants.GainBalancingNominal().alpha_motor_back_left)
    alpha_motor_back_right = np.radians(constants.GainBalancingNominal().alpha_motor_back_right)

    nominal_matrix_inv = [[-np.cos(alpha_motor_front), -np.cos(alpha_motor_back_left), np.cos(alpha_motor_back_right)],
                          [np.sin(alpha_motor_front), np.sin(alpha_motor_back_left), np.sin(alpha_motor_back_right)],
                          [1, -1, 1]]

    nominal_matrix = np.linalg.pinv(nominal_matrix_inv)

    return nominal_matrix


def calibrated():

    if constants.GainBalancingCalibrated().gain_balancing_calibrated:

        calibrated_matrix = np.ones([3, 3])

    else:

        # report error in errorlog!
        calibrated_matrix = nominal()

    return calibrated_matrix
