
class Motor:
    def __init__(self):
        self.peak = 260
        self.rms = 0


class LargeMotor:
    def __init__(self):
        self.peak = 175
        self.rms = 0


# NOMINAL parameters for measurement system
class GyroOffsetsNominal:
    def __init__(self, axis):
        self.offset_calibrated = False
        self.axis = axis
        self.calibration_mode = 'Undefined'
        self.static_offset = 0
        self.gain_offset = 0

    def get_values(self):
        return self


# CALIBRATED parameters for measurement system
class GyroOffsetsCalibrated:
    def __init__(self, axis):
        self.offset_calibrated = False
        self.axis = axis
        self.calibration_mode = 'None'
        self.static_offset = 0
        self.gain_offset = 0

    def set_values(self, offset_calibrated, calibration_mode, static_offset, gain_offset):
        self.offset_calibrated = offset_calibrated
        self.calibration_mode = calibration_mode
        self.static_offset = static_offset
        self.gain_offset = gain_offset

    def get_values(self):
        return self

