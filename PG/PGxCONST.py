
# NOMINAL PARAMETERS

# parameters used to compute nominal gain balancing matrix
class GainBalancingNominal:
    def __init__(self):
        self.alpha_motor_front = 0
        self.alpha_motor_back_left = 60
        self.alpha_motor_back_right = 60


# CALIBRATED PARAMETERS
class GainBalancingCalibrated:
    def __init__(self):
        self.gain_balancing_calibrated = False
