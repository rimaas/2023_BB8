
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class Motor:
    def __init__(self):
        self.peak = 260
        self.rms = 0


class LargeMotor:
    def __init__(self):
        self.peak = 175
        self.rms = 0


# NOMINAL parameters for measurement system
class GyroOffsetsNominal():
    def __init__(self):
        self.offset_calibrated = False
        self.calibration_mode = 'Undefined'
        self.static_offset = 0
        self.gain_offset = 0

    def get_values(self):
        return self


# CALIBRATED parameters for measurement system
# class GyroOffsetsCalibrated(Singleton):
#     def __init__(self):
#         self.offset_calibrated = False
#         self.calibration_mode = 'None'
#         self.static_offset = 0
#         self.gain_offset = 0
#
#     def set_values(self, offset_calibrated, calibration_mode, static_offset, gain_offset):
#         self.offset_calibrated = offset_calibrated
#         self.calibration_mode = calibration_mode
#         self.static_offset = static_offset
#         self.gain_offset = gain_offset
#
#     def get_values(self):
#         return self

class InnerStruct:
    def __init__(self, offset_calibrated, calibration_mode, static_offset, gain_offset):
        self.offset_calibrated = offset_calibrated
        self.calibration_mode = calibration_mode
        self.static_offset = static_offset
        self.gain_offset = gain_offset


class GyroOffsetsCalibrated(Singleton):
    def __init__(self):
        self.rx = None
        self.ry = None

    def set_values_rx(self, offset_calibrated, calibration_mode, static_offset, gain_offset):
        self.rx = InnerStruct(offset_calibrated, calibration_mode, static_offset, gain_offset)

    def set_values_ry(self, offset_calibrated, calibration_mode, static_offset, gain_offset):
        self.ry = InnerStruct(offset_calibrated, calibration_mode, static_offset, gain_offset)

    def get_values(self):
        return self


# supporting functions
def struct_to_dict(obj):
    if isinstance(obj, InnerStruct):

        return {'offset_calibrated': obj.offset_calibrated, 'calibration_mode': obj.calibration_mode,
                'static_offset': obj.static_offset, 'gain_offset': obj.gain_offset}

    if isinstance(obj, GyroOffsetsCalibrated):

        inner_dict_rx = struct_to_dict(obj.rx)
        inner_dict_ry = struct_to_dict(obj.ry)

        return {'rx': inner_dict_rx, 'ry': inner_dict_ry}


def dict_to_struct(data_dict):
    if 'offset_calibrated' in data_dict and 'calibration_mode' in data_dict \
                                    and 'gain_offset' in data_dict and 'static_offset' in data_dict:

        return InnerStruct(data_dict['offset_calibrated'], data_dict['calibration_mode'],
                           data_dict['gain_offset'], data_dict['static_offset'])

    if 'rx' in data_dict and 'ry' in data_dict:
        inner_struct_rx = dict_to_struct(data_dict['rx'])
        inner_struct_ry = dict_to_struct(data_dict['ry'])

        return inner_struct_rx, inner_struct_ry

