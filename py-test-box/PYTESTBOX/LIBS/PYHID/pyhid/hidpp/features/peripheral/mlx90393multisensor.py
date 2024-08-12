#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.peripheral.mlx90393multisensor
:brief: HID++ 2.0 MLX90393 Multiple Sensor management
:author: Ganesh Thiraviam <gthiraviam@logitech.com>
:date: 2021/01/28
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MLX90393MultiSensor(HidppMessage):
    """
    MLX90393MultiSensor implementation class

    Test interface for the Hall effect sensor MLX90393 from Melexis. This feature is intended to support the
    Hall sensor in a generic way, independently of the product or prototype where the sensor is included.

    It supports multiple sensors in one device.
    """
    FEATURE_ID = 0x9209
    MAX_FUNCTION_INDEX = 10

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class MLX90393MultiSensor


class MLX90393MultiSensorModel(FeatureModel):
    """
    MLX90393MultiSensor feature model
    """
    class INDEX(object):
        """
        Function index
        """
        READ_SENSOR_REGISTER = 0
        WRITE_SENSOR_REGISTER = 1
        RESET_SENSOR = 2
        SHUTDOWN_SENSOR = 3
        MONITOR_TEST = 4
        START_CALIBRATION = 5
        STOP_CALIBRATION = 6
        READ_CALIBRATION = 7
        WRITE_CALIBRATION = 8
        CALIBRATE = 9
        MANAGE_DYN_CALL_PARAM = 10

        MONITOR_REPORT_EVENT = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        MLX90393MultiSensor feature data model
        """
        return {
                "feature_base": MLX90393MultiSensor,
                "versions": {
                        MLX90393MultiSensorV0.VERSION: {
                                "main_cls": MLX90393MultiSensorV0,
                                "api": {
                                        "functions": {
                                                cls.INDEX.READ_SENSOR_REGISTER: {
                                                        "request": ReadSensorRegister,
                                                        "response": ReadSensorRegisterResponse
                                                },
                                                cls.INDEX.WRITE_SENSOR_REGISTER: {
                                                        "request": WriteSensorRegister,
                                                        "response": WriteSensorRegisterResponse
                                                },
                                                cls.INDEX.RESET_SENSOR: {
                                                        "request": ResetSensor,
                                                        "response": ResetSensorResponse
                                                },
                                                cls.INDEX.SHUTDOWN_SENSOR: {
                                                        "request": ShutdownSensor,
                                                        "response": ShutdownSensorResponse
                                                },
                                                cls.INDEX.MONITOR_TEST: {
                                                        "request": MonitorTest,
                                                        "response": MonitorTestResponse
                                                },
                                                cls.INDEX.START_CALIBRATION: {
                                                        "request": StartCalibration,
                                                        "response": StartCalibrationResponse
                                                },
                                                cls.INDEX.STOP_CALIBRATION: {
                                                        "request": StopCalibration,
                                                        "response": StopCalibrationResponse
                                                },
                                                cls.INDEX.READ_CALIBRATION: {
                                                        "request": ReadCalibration,
                                                        "response": ReadCalibrationResponse
                                                },
                                                cls.INDEX.WRITE_CALIBRATION: {
                                                        "request": WriteCalibration,
                                                        "response": WriteCalibrationResponse
                                                },
                                                cls.INDEX.CALIBRATE: {
                                                        "request": Calibrate,
                                                        "response": CalibrateResponse
                                                },
                                                cls.INDEX.MANAGE_DYN_CALL_PARAM: {
                                                        "request": ManageDynCallParam,
                                                        "response": ManageDynCallParamResponse
                                                }
                                        },
                                        "events": {
                                                cls.INDEX.MONITOR_REPORT_EVENT: {
                                                        "report": MonitorReportEvent
                                                }
                                        }
                                }
                        }
                }
        }
    # end def get_data_model
# end class MLX90393MultiSensorModel


class MLX90393MultiSensorFactory(FeatureFactory):
    """
    Factory which creates a MLX90393MultiSensor object from a given version
    """
    @staticmethod
    def create(version):
        """
        MLX90393MultiSensor object creation from version number

        :param version: MLX90393MultiSensor feature version
        :type version: ``int``

        :return: MLX90393MultiSensor object
        :rtype: ``MLX90393MultiSensorInterface``
        """
        return MLX90393MultiSensorModel.get_main_cls(version)()
    # end def create
# end class MLX90393MultiSensorFactory


class MLX90393MultiSensorInterface(FeatureInterface, ABC):
    """
    Interface to MLX90393MultiSensor feature

    Defines required interfaces for MLX90393MultiSensor classes
    """
    def __init__(self):
        # See ``FeatureInterface.__init__``

        # Requests
        self.read_sensor_register_cls = None
        self.write_sensor_register_cls = None
        self.reset_sensor_cls = None
        self.shutdown_sensor_cls = None
        self.monitor_test_cls = None
        self.start_calibration_cls = None
        self.stop_calibration_cls = None
        self.read_calibration_cls = None
        self.write_calibration_cls = None
        self.calibrate_cls = None
        self.manage_dyn_call_param_cls = None

        # Responses
        self.read_sensor_register_response_cls = None
        self.write_sensor_register_response_cls = None
        self.reset_sensor_response_cls = None
        self.shutdown_sensor_response_cls = None
        self.monitor_test_response_cls = None
        self.start_calibration_response_cls = None
        self.stop_calibration_response_cls = None
        self.read_calibration_response_cls = None
        self.write_calibration_response_cls = None
        self.calibrate_response_cls = None
        self.manage_dyn_call_param_response_cls = None

        # Events
        self.monitor_report_event_cls = None
    # end def __init__
# end class MLX90393MultiSensorInterface


class MLX90393MultiSensorV0(MLX90393MultiSensorInterface):
    """
    MLX90393MultiSensorV0

    This feature provides model and unit specific information for version 0

    [0] readSensorRegister(sensorId, regAddr) -> sensorId, regAddr, regVal

    [1] writeSensorRegister(sensorId, regAddr, regVal)-> sensorId, regAddr, regVal

    [2] resetSensor(sensorId) -> sensorId

    [3] shutdownSensor(sensorId) -> sensorId

    [4] monitorTest(sensorId, count, threshold) -> sensorId, count, threshold

    [5] startCalibration(sensorId) -> sensorId

    [6] stopCalibration(sensorId) -> sensorId, calibrationData

    [7] readCalibration(sensorId) -> sensorId, calibrationData

    [8] writeCalibration(sensorId, calibrationData) -> sensorId, calibrationData

    [9] calibrate(sensorId, refPointIndex, refPointOutValue)-> void

    [A] manageDynCalParam(GET/SET ¦ sensorId, parameters)-> sensorId, parameters
    """
    VERSION = 0

    def __init__(self):
        # See ``MLX90393MultiSensorInterface.__init__``

        super().__init__()
        index = MLX90393MultiSensorModel.INDEX
        # Requests
        self.read_sensor_register_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.READ_SENSOR_REGISTER)
        self.write_sensor_register_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.WRITE_SENSOR_REGISTER)
        self.reset_sensor_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.RESET_SENSOR)
        self.shutdown_sensor_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.SHUTDOWN_SENSOR)
        self.monitor_test_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.MONITOR_TEST)
        self.start_calibration_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.START_CALIBRATION)
        self.stop_calibration_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.STOP_CALIBRATION)
        self.read_calibration_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.READ_CALIBRATION)
        self.write_calibration_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.WRITE_CALIBRATION)
        self.calibrate_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.CALIBRATE)
        self.manage_dyn_call_param_cls = MLX90393MultiSensorModel.get_request_cls(
                self.VERSION, index.MANAGE_DYN_CALL_PARAM)

        # Responses
        self.read_sensor_register_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.READ_SENSOR_REGISTER)
        self.write_sensor_register_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.WRITE_SENSOR_REGISTER)
        self.reset_sensor_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.RESET_SENSOR)
        self.shutdown_sensor_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.SHUTDOWN_SENSOR)
        self.monitor_test_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.MONITOR_TEST)
        self.start_calibration_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.START_CALIBRATION)
        self.stop_calibration_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.STOP_CALIBRATION)
        self.read_calibration_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.READ_CALIBRATION)
        self.write_calibration_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.WRITE_CALIBRATION)
        self.calibrate_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.CALIBRATE)
        self.manage_dyn_call_param_response_cls = MLX90393MultiSensorModel.get_response_cls(
                self.VERSION, index.MANAGE_DYN_CALL_PARAM)

        # Events
        self.monitor_report_event_cls = MLX90393MultiSensorModel.get_report_cls(
                self.VERSION, index.MONITOR_REPORT_EVENT)
    # end def __init__

    def get_max_function_index(self):
        # See ``MLX90393MultiSensorInterface.get_max_function_index``
        return MLX90393MultiSensorModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class MLX90393MultiSensorV0


class ReadSensorRegister(MLX90393MultiSensor):
    """
    Read Sensor Register implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    RegisterAddress               8
    Padding                       8
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        REG_ADDR = SENSOR_ID - 1
        PADDING = REG_ADDR - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        REG_ADDR = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.REG_ADDR, length=LEN.REG_ADDR,
                     title="RegisterAddress", name="reg_addr",
                     checks=(CheckHexList(LEN.REG_ADDR // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_id, reg_addr, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param reg_addr: Register Address to be read
        :type reg_addr: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=ReadSensorRegisterResponse.FUNCTION_INDEX,
                         **kwargs)
        self.sensor_id = sensor_id
        self.reg_addr = reg_addr
    # end def __init__
# end class ReadSensorRegister


class ReadWriteSensorFormat(MLX90393MultiSensor):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    RegisterAddress               8
    RegisterValue                 16
    Padding                       96
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        REG_ADDR = SENSOR_ID - 1
        REG_VALUE = REG_ADDR - 1
        PADDING = REG_VALUE - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        REG_ADDR = 0x8
        REG_VALUE = 0x10
        PADDING = 0x60
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.REG_ADDR, length=LEN.REG_ADDR,
                     title="RegisterAddress", name="reg_addr",
                     checks=(CheckHexList(LEN.REG_ADDR // 8), CheckByte(),)),
            BitField(fid=FID.REG_VALUE, length=LEN.REG_VALUE,
                     title="RegisterValue", name="reg_value",
                     checks=(CheckHexList(LEN.REG_VALUE // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )
# end class ReadWriteSensorFormat


class ReadSensorRegisterResponse(ReadWriteSensorFormat):
    """
    ReadSensorRegisterResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadSensorRegister,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, sensor_id, reg_addr, reg_value, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param reg_addr: Register Address to be read
        :type reg_addr: ``int`` or ``HexList``
        :param reg_value: Value read from register
        :type reg_value: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.reg_addr = reg_addr
        self.reg_value = reg_value
    # end def __init__
# end class ReadSensorRegisterResponse


class WriteSensorRegister(ReadWriteSensorFormat):
    """
    WriteSensorRegister implementation class for version 0
    """
    def __init__(self, device_index, feature_index, sensor_id, reg_addr, reg_value, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param reg_addr: Register Address to be read
        :type reg_addr: ``int`` or ``HexList``
        :param reg_value: Value read from register
        :type reg_value: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=WriteSensorRegisterResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.reg_addr = reg_addr
        self.reg_value = reg_value
    # end def __init__
# end class WriteSensorRegister


class WriteSensorRegisterResponse(ReadWriteSensorFormat):
    """
    WriteSensorRegisterResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteSensorRegister,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, sensor_id, reg_addr, reg_value, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param reg_addr: Register Address to be read
        :type reg_addr: ``int`` or ``HexList``
        :param reg_value: Value read from register
        :type reg_value: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.reg_addr = reg_addr
        self.reg_value = reg_value
    # end def __init__
# end class WriteSensorRegisterResponse


class ResetShutdownSensorFormat(MLX90393MultiSensor):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    Padding                       16
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        PADDING = SENSOR_ID - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )
# end class ResetShutdownSensorFormat


class ResetShutdownStartResponseFormat(MLX90393MultiSensor):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    Padding                       120
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        PADDING = SENSOR_ID - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )
# end class ResetShutdownStartResponseFormat


class ResetSensor(ResetShutdownSensorFormat):
    """
    ResetSensor implementation class for version 0
    """
    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=ResetSensorResponse.FUNCTION_INDEX,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class ResetSensor


class ResetSensorResponse(ResetShutdownStartResponseFormat):
    """
    ResetSensorResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ResetSensor,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class ResetSensorResponse


class ShutdownSensor(ResetShutdownSensorFormat):
    """
    ShutdownSensor implementation class for version 0
    """
    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=ShutdownSensorResponse.FUNCTION_INDEX,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class ShutdownSensor


class ShutdownSensorResponse(ResetShutdownStartResponseFormat):
    """
    ShutdownSensorResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ShutdownSensor,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class ShutdownSensorResponse


class MonitorTestFormat(MLX90393MultiSensor):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    Count                         16
    Threshold                     8
    Padding                       96
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        COUNT = SENSOR_ID - 1
        THRESHOLD = COUNT - 1
        PADDING = THRESHOLD - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        COUNT = 0x10
        THRESHOLD = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.COUNT, length=LEN.COUNT,
                     title="MonitorSampleCount", name="count",
                     checks=(CheckHexList(LEN.COUNT // 8), CheckByte(),)),
            BitField(fid=FID.THRESHOLD, length=LEN.THRESHOLD,
                     title="MonitorThreshold", name="threshold",
                     checks=(CheckHexList(LEN.THRESHOLD // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )
# end class MonitorTestFormat


class MonitorTest(MonitorTestFormat):
    """
    MonitorTest implementation class for version 0
    """
    def __init__(self, device_index, feature_index, sensor_id, count, threshold, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param count: Monitor Mode Sample (counter)
        :type count: ``int`` or ``HexList``
        :param threshold: Monitor Mode Threshold
        :type threshold: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=MonitorTestResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.count = count
        self.threshold = threshold
    # end def __init__
# end class MonitorTest


class MonitorTestResponse(MonitorTestFormat):
    """
    MonitorTestResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (MonitorTest,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, sensor_id, count, threshold, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param count: Monitor Mode Sample (counter)
        :type count: ``int`` or ``HexList``
        :param threshold: Monitor Mode Threshold
        :type threshold: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.count = count
        self.threshold = threshold
    # end def __init__
# end class MonitorTestResponse


class StartStopReadCalibrationFormat(MLX90393MultiSensor):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    Padding                       16
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        PADDING = SENSOR_ID - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )
# end class StartStopReadCalibrationFormat


class StopReadWriteCalibrationResponseFormat(MLX90393MultiSensor):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    CalibrationData               32
    Padding                       88
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        CALIBRATION_DATA = SENSOR_ID - 1
        PADDING = CALIBRATION_DATA - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        CALIBRATION_DATA = 0x20
        PADDING = 0x58
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.CALIBRATION_DATA, length=LEN.CALIBRATION_DATA,
                     title="CalibrationData", name="calibration_data",
                     checks=(CheckHexList(LEN.CALIBRATION_DATA // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )
# end class StopReadWriteCalibrationResponseFormat


class StartCalibration(StartStopReadCalibrationFormat):
    """
    StartCalibration implementation class for version 0
    """
    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=StartCalibrationResponse.FUNCTION_INDEX,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class StartCalibration


class StartCalibrationResponse(ResetShutdownStartResponseFormat):
    """
    StartCalibrationResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class StartCalibrationResponse


class StopCalibration(StartStopReadCalibrationFormat):
    """
    StopCalibration implementation class for version 0
    """
    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=StopCalibrationResponse.FUNCTION_INDEX,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class StopCalibration


class StopCalibrationResponse(StopReadWriteCalibrationResponseFormat):
    """
    StopCalibrationResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StopCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

    def __init__(self, device_index, feature_index, sensor_id, calibration_data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param calibration_data: Calibration Data
        :type calibration_data: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.calibration_data = calibration_data
    # end def __init__
# end class StopCalibrationResponse


class ReadCalibration(StartStopReadCalibrationFormat):
    """
    ReadCalibration implementation class for version 0
    """
    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=ReadCalibrationResponse.FUNCTION_INDEX,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class ReadCalibration


class ReadCalibrationResponse(StopReadWriteCalibrationResponseFormat):
    """
    ReadCalibrationResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, sensor_id, calibration_data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param calibration_data: Calibration Data
        :type calibration_data: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.calibration_data = calibration_data
    # end def __init__
# end class ReadCalibrationResponse


class WriteCalibration(StopReadWriteCalibrationResponseFormat):
    """
    WriteCalibration implementation class for version 0
    """
    def __init__(self, device_index, feature_index, sensor_id, calibration_data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param calibration_data: Calibration Data
        :type calibration_data: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=WriteCalibrationResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.calibration_data = calibration_data
    # end def __init__
# end class WriteCalibration


class WriteCalibrationResponse(StopReadWriteCalibrationResponseFormat):
    """
    WriteCalibrationResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 8

    def __init__(self, device_index, feature_index, sensor_id, calibration_data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param calibration_data: Calibration Data
        :type calibration_data: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.calibration_data = calibration_data
    # end def __init__
# end class WriteCalibrationResponse


class Calibrate(MLX90393MultiSensor):
    """
    Calibrate implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    ReferencePointIndex           8
    referencePointOutValue        8
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        REF_POINT_ID = SENSOR_ID - 1
        REF_POINT_OUT_VALUE = REF_POINT_ID - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        REF_POINT_ID = 0x8
        REF_POINT_OUT_VALUE = 0x8
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.REF_POINT_ID, length=LEN.REF_POINT_ID,
                     title="ReferencePointIndex", name="ref_point_id",
                     checks=(CheckHexList(LEN.REF_POINT_ID // 8), CheckByte(),)),
            BitField(fid=FID.REF_POINT_OUT_VALUE, length=LEN.REF_POINT_OUT_VALUE,
                     title="ReferencePointOutValue", name="ref_point_out_value",
                     checks=(CheckHexList(LEN.REF_POINT_OUT_VALUE // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, sensor_id, ref_point_id, ref_point_out_value, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param ref_point_id: Reference Point Index
        :type ref_point_id: ``int`` or ``HexList``
        :param ref_point_out_value: Reference Point Out Value
        :type ref_point_out_value: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=CalibrateResponse.FUNCTION_INDEX,
                         **kwargs)
        self.sensor_id = sensor_id
        self.ref_point_id = ref_point_id
        self.ref_point_out_value = ref_point_out_value
    # end def __init__
# end class Calibrate


class CalibrateResponse(MLX90393MultiSensor):
    """
    CalibrateResponse implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (Calibrate,)
    VERSION = (0,)
    FUNCTION_INDEX = 9

    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        PADDING = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class CalibrateResponse


class ManageDynCallParamFormat(MLX90393MultiSensor):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Command                       1
    SensorId                      1
    Reserved                      6
    Parameters                    48
    Padding                       72
    ============================  ==========
    """
    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        COMMAND = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        SENSOR_ID = COMMAND - 1
        RESERVED = SENSOR_ID - 1
        PARAMETERS = RESERVED - 1
        PADDING = PARAMETERS - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        COMMAND = 0x1
        SENSOR_ID = 0x1
        RESERVED = 0x6
        PARAMETERS = 0x30
        PADDING = 0x48
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.COMMAND, length=LEN.COMMAND,
                     title="Command", name="command",
                     checks=(CheckInt(0, pow(2, LEN.COMMAND) - 1),)),
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckInt(0, pow(2, LEN.SENSOR_ID) - 1),)),
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=MLX90393MultiSensor.DEFAULT.RESERVED),
            BitField(fid=FID.PARAMETERS, length=LEN.PARAMETERS,
                     title="Parameters", name="parameters",
                     checks=(CheckHexList(LEN.PARAMETERS // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title="Padding", name="padding",
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
    )
# end class ManageDynCallParamFormat


class ManageDynCallParam(ManageDynCallParamFormat):
    """
    ManageDynCallParam implementation class for version 0
    """
    def __init__(self, device_index, feature_index, command, sensor_id, parameters, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param command: Command
        :type command: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param parameters: Dynamic Call Parameters
        :type parameters: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=ManageDynCallParamResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.command = command
        self.sensor_id = sensor_id
        self.parameters = parameters
    # end def __init__
# end class ManageDynCallParam


class ManageDynCallParamResponse(ManageDynCallParamFormat):
    """
    ManageDynCallParamResponse implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ManageDynCallParam,)
    VERSION = (0,)
    FUNCTION_INDEX = 10

    def __init__(self, device_index, feature_index, command, sensor_id, parameters, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param command: Command
        :type command: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param parameters: Dynamic Call Parameters
        :type parameters: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.command = command
        self.sensor_id = sensor_id
        self.parameters = parameters
    # end def __init__
# end class ManageDynCallParamResponse


class MonitorReportEvent(MLX90393MultiSensor):
    """
    Monitor Report event

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    AxisValueX                    16
    AxisValueY                    16
    AxisValueZ                    16
    TemperatureValue              16
    ArcTangentValue               16
    Reserved                      24
    Counter                       16
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 0
    VERSION = (0,)

    class FID(MLX90393MultiSensor.FID):
        """
        Fields identifiers
        """
        SENSOR_ID = MLX90393MultiSensor.FID.SOFTWARE_ID - 1
        AXIS_VALUE_X = SENSOR_ID - 1
        AXIS_VALUE_Y = AXIS_VALUE_X - 1
        AXIS_VALUE_Z = AXIS_VALUE_Y - 1
        TEMPERATURE_VALUE = AXIS_VALUE_Z - 1
        ARC_TANGENT_VALUE = TEMPERATURE_VALUE - 1
        RESERVED = ARC_TANGENT_VALUE - 1
        COUNTER = RESERVED - 1
    # end class FID

    class LEN(MLX90393MultiSensor.LEN):
        """
        Fields lengths in bits
        """
        SENSOR_ID = 0x8
        AXIS_VALUE_X = 0x10
        AXIS_VALUE_Y = 0x10
        AXIS_VALUE_Z = 0x10
        TEMPERATURE_VALUE = 0x10
        ARC_TANGENT_VALUE = 0x10
        RESERVED = 0x18
        COUNTER = 0x10
    # end class LEN

    FIELDS = MLX90393MultiSensor.FIELDS + (
            BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                     title="SensorId", name="sensor_id",
                     checks=(CheckHexList(LEN.SENSOR_ID // 8), CheckByte(),)),
            BitField(fid=FID.AXIS_VALUE_X, length=LEN.AXIS_VALUE_X,
                     title="AxisValueX", name="axis_value_x",
                     checks=(CheckInt(0, pow(2, LEN.AXIS_VALUE_X) - 1),)),
            BitField(fid=FID.AXIS_VALUE_Y, length=LEN.AXIS_VALUE_Y,
                     title="AxisValueY", name="axis_value_y",
                     checks=(CheckInt(0, pow(2, LEN.AXIS_VALUE_Y) - 1),)),
            BitField(fid=FID.AXIS_VALUE_Z, length=LEN.AXIS_VALUE_Z,
                     title="AxisValueZ", name="axis_value_z",
                     checks=(CheckInt(0, pow(2, LEN.AXIS_VALUE_Z) - 1),)),
            BitField(fid=FID.TEMPERATURE_VALUE, length=LEN.TEMPERATURE_VALUE,
                     title="TemperatureValue", name="temperature_value",
                     checks=(CheckHexList(LEN.TEMPERATURE_VALUE // 8), CheckByte(),)),
            BitField(fid=FID.ARC_TANGENT_VALUE, length=LEN.ARC_TANGENT_VALUE,
                     title="ArcTangentValue", name="arc_tangent_value",
                     checks=(CheckHexList(LEN.ARC_TANGENT_VALUE // 8), CheckByte(),)),
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                     default_value=MLX90393MultiSensor.DEFAULT.PADDING),
            BitField(fid=FID.COUNTER, length=LEN.COUNTER,
                     title="Counter", name="counter",
                     checks=(CheckHexList(LEN.COUNTER // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, sensor_id, axis_value_x, axis_value_y, axis_value_z,
                 temperature_value, arc_tangent_value, counter, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Desired feature Id
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param axis_value_x: Axis Value X
        :type axis_value_x: ``int`` or ``HexList``
        :param axis_value_y: Axis Value Y
        :type axis_value_y: ``int`` or ``HexList``
        :param axis_value_z: Axis Value Z
        :type axis_value_z: ``int`` or ``HexList``
        :param temperature_value: Temperature Value
        :type temperature_value: ``int`` or ``HexList``
        :param arc_tangent_value: Arc Tangent Value
        :type arc_tangent_value: ``int`` or ``HexList``
        :param counter: Counter
        :type counter: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.axis_value_x = axis_value_x
        self.axis_value_y = axis_value_y
        self.axis_value_z = axis_value_z
        self.temperature_value = temperature_value
        self.arc_tangent_value = arc_tangent_value
        self.counter = counter
    # end def __init__
# end class MonitorReportEvent

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
