#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.peripheral.mlx903xx
:brief: HID++ 2.0 ``MLX903xx`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2023/04/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
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
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MLX903xx(HidppMessage):
    """
    Test interface for the Hall effect sensor MLX90393 from Melexis.
    """
    FEATURE_ID = 0x9205
    MAX_FUNCTION_INDEX_V0 = 11

    # Touch Status
    class Touch(object):
        """
        Define touch status of proximity sensor
        """
        UNTOUCHED_STATE = 0
        TOUCHED_STATE = 1
    # end class Touch

    # Test mode
    class TestMode(object):
        """
        Define roller test modes
        """
        NATIVE = 0
        DIVERTED = 1
    # end class TestMode

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class MLX903xx


# noinspection DuplicatedCode
class MLX903xxModel(FeatureModel):
    """
    Define ``MLX903xx`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        READ_SENSOR_REGISTER = 0
        WRITE_SENSOR_REGISTER = 1
        RESET_SENSOR = 2
        SHUTDOWN_SENSOR = 3
        MONITOR_TEST = 4
        START_CALIBRATION = 5
        STOP_CALIBRATION = 6
        READ_CALIBRATION = 7
        WRITE_CALIBRATION = 8
        READ_TOUCH_STATUS = 9
        SET_ROLLER_TEST = 10
        READ_EPM_IQS624_REGISTER = 11

        # Event index
        MONITOR_REPORT = 0
        ROLLER_TEST = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``MLX903xx`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
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
                cls.INDEX.READ_TOUCH_STATUS: {
                    "request": ReadTouchStatus,
                    "response": ReadTouchStatusResponse
                },
                cls.INDEX.SET_ROLLER_TEST: {
                    "request": SetRollerTest,
                    "response": SetRollerTestResponse
                },
                cls.INDEX.READ_EPM_IQS624_REGISTER: {
                    "request": ReadEPMIQS624Register,
                    "response": ReadEPMIQS624RegisterResponse
                }
            },
            "events": {
                cls.INDEX.MONITOR_REPORT: {"report": MonitorReportEvent},
                cls.INDEX.ROLLER_TEST: {"report": RollerTestEvent}
            }
        }

        return {
            "feature_base": MLX903xx,
            "versions": {
                MLX903xxV0.VERSION: {
                    "main_cls": MLX903xxV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class MLX903xxModel


# noinspection DuplicatedCode
class MLX903xxFactory(FeatureFactory):
    """
    Get ``MLX903xx`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``MLX903xx`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``MLX903xxInterface``
        """
        return MLX903xxModel.get_main_cls(version)()
    # end def create
# end class MLX903xxFactory


class MLX903xxInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``MLX903xx``
    """

    def __init__(self):
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
        self.read_touch_status_cls = None
        self.set_roller_test_cls = None
        self.read_epm_iqs624_register_cls = None

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
        self.read_touch_status_response_cls = None
        self.set_roller_test_response_cls = None
        self.read_epm_iqs624_register_response_cls = None

        # Events
        self.monitor_report_event_cls = None
        self.roller_test_event_cls = None
    # end def __init__
# end class MLX903xxInterface


class MLX903xxV0(MLX903xxInterface):
    """
    Define ``MLX903xxV0`` feature

    This feature provides model and unit specific information for version 0

    [0] readSensorRegister(registerAddress) -> registerAddress, registerValue

    [1] writeSensorRegister(registerAddress, registerValue) -> None

    [2] resetSensor() -> None

    [3] shutdownSensor() -> None

    [4] monitorTest(count, threshold) -> None

    [5] startCalibration() -> None

    [6] stopCalibration() -> nbTurns, minX, maxX, minY, maxY

    [7] readCalibration() -> nbTurns, minX, maxX, minY, maxY

    [8] writeCalibration(nbTurns, minX, maxX, minY, maxY) -> None

    [9] readTouchStatus() -> status

    [10] setRollerTest(multiplier, testMode) -> None

    [11] readEPMIQS624Register(registerAddress) -> registerAddress, registerValue

    [Event 0] MonitorReportEvent -> fieldX, fieldY, fieldZ, temperature, angle, slot, ratchet, angleOffset,
    angleRatchetNumber, counter

    [Event 1] RollerTestEvent -> accumulator, timestampValue
    """
    VERSION = 0

    def __init__(self):
        # See ``MLX903xx.__init__``
        super().__init__()
        index = MLX903xxModel.INDEX

        # Requests
        self.read_sensor_register_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.READ_SENSOR_REGISTER)
        self.write_sensor_register_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.WRITE_SENSOR_REGISTER)
        self.reset_sensor_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.RESET_SENSOR)
        self.shutdown_sensor_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.SHUTDOWN_SENSOR)
        self.monitor_test_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.MONITOR_TEST)
        self.start_calibration_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.START_CALIBRATION)
        self.stop_calibration_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.STOP_CALIBRATION)
        self.read_calibration_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.READ_CALIBRATION)
        self.write_calibration_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.WRITE_CALIBRATION)
        self.read_touch_status_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.READ_TOUCH_STATUS)
        self.set_roller_test_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.SET_ROLLER_TEST)
        self.read_epm_iqs624_register_cls = MLX903xxModel.get_request_cls(
            self.VERSION, index.READ_EPM_IQS624_REGISTER)

        # Responses
        self.read_sensor_register_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.READ_SENSOR_REGISTER)
        self.write_sensor_register_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.WRITE_SENSOR_REGISTER)
        self.reset_sensor_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.RESET_SENSOR)
        self.shutdown_sensor_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.SHUTDOWN_SENSOR)
        self.monitor_test_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.MONITOR_TEST)
        self.start_calibration_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.START_CALIBRATION)
        self.stop_calibration_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.STOP_CALIBRATION)
        self.read_calibration_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.READ_CALIBRATION)
        self.write_calibration_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.WRITE_CALIBRATION)
        self.read_touch_status_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.READ_TOUCH_STATUS)
        self.set_roller_test_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.SET_ROLLER_TEST)
        self.read_epm_iqs624_register_response_cls = MLX903xxModel.get_response_cls(
            self.VERSION, index.READ_EPM_IQS624_REGISTER)

        # Events
        self.monitor_report_event_cls = MLX903xxModel.get_report_cls(
            self.VERSION, index.MONITOR_REPORT)
        self.roller_test_event_cls = MLX903xxModel.get_report_cls(
            self.VERSION, index.ROLLER_TEST)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``MLX903xxInterface.get_max_function_index``
        return MLX903xxModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class MLX903xxV0


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(MLX903xx):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - ReadCalibration
        - ReadTouchStatus
        - ResetSensor
        - ShutdownSensor
        - StartCalibration
        - StopCalibration

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        PADDING = MLX903xx.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(MLX903xx):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - MonitorTestResponse
        - ResetSensorResponse
        - SetRollerTestResponse
        - ShutdownSensorResponse
        - StartCalibrationResponse
        - WriteCalibrationResponse
        - WriteSensorRegisterResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        PADDING = MLX903xx.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


# noinspection DuplicatedCode
class RegisterAddressHead(MLX903xx):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - ReadEPMIQS624Register
        - ReadSensorRegister

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Register Address              8
    Padding                       16
    ============================  ==========
    """

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        REGISTER_ADDRESS = MLX903xx.FID.SOFTWARE_ID - 1
        PADDING = REGISTER_ADDRESS - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        REGISTER_ADDRESS = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.REGISTER_ADDRESS, length=LEN.REGISTER_ADDRESS,
                 title="RegisterAddress", name="register_address",
                 checks=(CheckHexList(LEN.REGISTER_ADDRESS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),
    )
# end class RegisterAddressHead


class RegisterAddressRegisterValueHead(MLX903xx):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - ReadEPMIQS624RegisterResponse
        - ReadSensorRegisterResponse
        - WriteSensorRegister

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Register Address              8
    Register Value                16
    ============================  ==========
    """

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        REGISTER_ADDRESS = MLX903xx.FID.SOFTWARE_ID - 1
        REGISTER_VALUE = REGISTER_ADDRESS - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        REGISTER_ADDRESS = 0x8
        REGISTER_VALUE = 0x10
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.REGISTER_ADDRESS, length=LEN.REGISTER_ADDRESS,
                 title="RegisterAddress", name="register_address",
                 checks=(CheckHexList(LEN.REGISTER_ADDRESS // 8), CheckByte(),)),
        BitField(fid=FID.REGISTER_VALUE, length=LEN.REGISTER_VALUE,
                 title="RegisterValue", name="register_value",
                 checks=(CheckHexList(LEN.REGISTER_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REGISTER_VALUE) - 1),)),
    )
# end class RegAddressRegValueHead


class CalibrationData(MLX903xx):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - ReadCalibrationResponse
        - StopCalibrationResponse
        - WriteCalibration

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Nb Turns                      8
    Min X                         16
    Max X                         16
    Min Y                         16
    Max Y                         16
    Padding                       56
    ============================  ==========
    """

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        NB_TURNS = MLX903xx.FID.SOFTWARE_ID - 1
        MIN_X = NB_TURNS - 1
        MAX_X = MIN_X - 1
        MIN_Y = MAX_X - 1
        MAX_Y = MIN_Y - 1
        PADDING = MAX_Y - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        NB_TURNS = 0x8
        MIN_X = 0x10
        MAX_X = 0x10
        MIN_Y = 0x10
        MAX_Y = 0x10
        PADDING = 0x38
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.NB_TURNS, length=LEN.NB_TURNS,
                 title="NbTurns", name="nb_turns",
                 checks=(CheckHexList(LEN.NB_TURNS // 8), CheckByte(),)),
        BitField(fid=FID.MIN_X, length=LEN.MIN_X,
                 title="MinX", name="min_x",
                 checks=(CheckHexList(LEN.MIN_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MIN_X) - 1),)),
        BitField(fid=FID.MAX_X, length=LEN.MAX_X,
                 title="MaxX", name="max_x",
                 checks=(CheckHexList(LEN.MAX_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAX_X) - 1),)),
        BitField(fid=FID.MIN_Y, length=LEN.MIN_Y,
                 title="MinY", name="min_y",
                 checks=(CheckHexList(LEN.MIN_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MIN_Y) - 1),)),
        BitField(fid=FID.MAX_Y, length=LEN.MAX_Y,
                 title="MaxY", name="max_y",
                 checks=(CheckHexList(LEN.MAX_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAX_Y) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),
    )
# end class CalibrationData


class ReadSensorRegister(RegisterAddressHead):
    """
    Define ``ReadSensorRegister`` implementation class
    """

    def __init__(self, device_index, feature_index, register_address, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_address: The register address
        :type register_address: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadSensorRegisterResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        numeral_size = self.LEN.REGISTER_ADDRESS // 8
        register_address = HexList(Numeral(register_address, numeral_size))
        self.register_address = register_address
    # end def __init__
# end class ReadSensorRegister


class WriteSensorRegister(RegisterAddressRegisterValueHead):
    """
    Define ``WriteSensorRegister`` implementation class
    """

    def __init__(self, device_index, feature_index, register_address, register_value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_address: The register address
        :type register_address: ``int | HexList``
        :param register_value: The register value
        :type register_value: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=WriteSensorRegisterResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        numeral_size = self.LEN.REGISTER_ADDRESS // 8
        register_address = HexList(Numeral(register_address, numeral_size))
        self.register_address = register_address

        numeral_size = self.LEN.REGISTER_VALUE // 8
        register_value = HexList(Numeral(register_value, numeral_size))
        self.register_value = register_value
    # end def __init__
# end class WriteSensorRegister


class ResetSensor(ShortEmptyPacketDataFormat):
    """
    Define ``ResetSensor`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ResetSensorResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ResetSensor


class ShutdownSensor(ShortEmptyPacketDataFormat):
    """
    Define ``ShutdownSensor`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ShutdownSensorResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ShutdownSensor


# noinspection DuplicatedCode
class MonitorTest(MLX903xx):
    """
    Define ``MonitorTest`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Count                         16
    Threshold                     8
    ============================  ==========
    """

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        COUNT = MLX903xx.FID.SOFTWARE_ID - 1
        THRESHOLD = COUNT - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        COUNT = 0x10
        THRESHOLD = 0x8
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNT) - 1),)),
        BitField(fid=FID.THRESHOLD, length=LEN.THRESHOLD,
                 title="Threshold", name="threshold",
                 checks=(CheckHexList(LEN.THRESHOLD // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, count, threshold, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param count: The total number of events requested
        :type count: ``int | HexList``
        :param threshold: The minimum, absolute, variation on X or Y field values so that a new report be generated
        :type threshold: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=MonitorTestResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        numeral_size = self.LEN.COUNT // 8
        count = HexList(Numeral(count, numeral_size))
        self.count = count

        numeral_size = self.LEN.THRESHOLD // 8
        threshold = HexList(Numeral(threshold, numeral_size))
        self.threshold = threshold
    # end def __init__
# end class MonitorTest


class StartCalibration(ShortEmptyPacketDataFormat):
    """
    Define ``StartCalibration`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=StartCalibrationResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class StartCalibration


class StopCalibration(ShortEmptyPacketDataFormat):
    """
    Define ``StopCalibration`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=StopCalibrationResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class StopCalibration


class ReadCalibration(ShortEmptyPacketDataFormat):
    """
    Define ``ReadCalibration`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadCalibrationResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ReadCalibration


class WriteCalibration(CalibrationData):
    """
    Define ``WriteCalibration`` implementation class
    """

    def __init__(self, device_index, feature_index, nb_turns, min_x, max_x, min_y, max_y, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param nb_turns: The number of complete turns affected
        :type nb_turns: ``int | HexList``
        :param min_x: X field minimum value
        :type min_x: ``HexList``
        :param max_x: X field maximum value
        :type max_x: ``HexList``
        :param min_y: Y field minimum value
        :type min_y: ``HexList``
        :param max_y: Y field maximum value
        :type max_y: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=WriteCalibrationResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        numeral_size = self.LEN.NB_TURNS // 8
        nb_turns = HexList(Numeral(nb_turns, numeral_size))
        self.nb_turns = nb_turns

        numeral_size = self.LEN.MIN_X // 8
        min_x = HexList(Numeral(min_x, numeral_size))
        self.min_x = min_x

        numeral_size = self.LEN.MAX_X // 8
        max_x = HexList(Numeral(max_x, numeral_size))
        self.max_x = max_x

        numeral_size = self.LEN.MIN_Y // 8
        min_y = HexList(Numeral(min_y, numeral_size))
        self.min_y = min_y

        numeral_size = self.LEN.MAX_Y // 8
        max_y = HexList(Numeral(max_y, numeral_size))
        self.max_y = max_y
    # end def __init__
# end class WriteCalibration


class ReadTouchStatus(ShortEmptyPacketDataFormat):
    """
    Define ``ReadTouchStatus`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadTouchStatusResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ReadTouchStatus


class SetRollerTest(MLX903xx):
    """
    Define ``SetRollerTest`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Multiplier                    8
    Test Mode                     8
    Padding                       8
    ============================  ==========
    """

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        MULTIPLIER = MLX903xx.FID.SOFTWARE_ID - 1
        TEST_MODE = MULTIPLIER - 1
        PADDING = TEST_MODE - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        MULTIPLIER = 0x8
        TEST_MODE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.MULTIPLIER, length=LEN.MULTIPLIER,
                 title="Multiplier", name="multiplier",
                 checks=(CheckHexList(LEN.MULTIPLIER // 8), CheckByte(),)),
        BitField(fid=FID.TEST_MODE, length=LEN.TEST_MODE,
                 title="TestMode", name="test_mode",
                 checks=(CheckHexList(LEN.TEST_MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, multiplier, test_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param multiplier: The period multiplier
        :type multiplier: ``int | HexList``
        :param test_mode: The test mode HID/HIDPP
        :type test_mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetRollerTestResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        numeral_size = self.LEN.MULTIPLIER // 8
        multiplier = HexList(Numeral(multiplier, numeral_size))
        self.multiplier = multiplier

        numeral_size = self.LEN.TEST_MODE // 8
        test_mode = HexList(Numeral(test_mode, numeral_size))
        self.test_mode = test_mode
    # end def __init__
# end class SetRollerTest


class ReadEPMIQS624Register(RegisterAddressHead):
    """
    Define ``ReadEPMIQS624Register`` implementation class
    """

    def __init__(self, device_index, feature_index, register_address, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_address: The register address
        :type register_address: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadEPMIQS624RegisterResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        numeral_size = self.LEN.REGISTER_ADDRESS // 8
        register_address = HexList(Numeral(register_address, numeral_size))
        self.register_address = register_address
    # end def __init__
# end class ReadEPMIQS624Register


class ReadSensorRegisterResponse(RegisterAddressRegisterValueHead):
    """
    Define ``ReadSensorRegisterResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadSensorRegister,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(RegisterAddressRegisterValueHead.FID):
        # See ``RegisterAddressRegisterValueHead.FID``
        PADDING = RegisterAddressRegisterValueHead.FID.REGISTER_VALUE - 1
    # end class FID

    class LEN(RegisterAddressRegisterValueHead.LEN):
        # See ``RegisterAddressRegisterValueHead.LEN``
        PADDING = 0x68
    # end class LEN

    FIELDS = RegisterAddressRegisterValueHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, register_address, register_value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_address: The register address
        :type register_address: ``int | HexList``
        :param register_value: The register value
        :type register_value: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        numeral_size = self.LEN.REGISTER_ADDRESS // 8
        register_address = HexList(Numeral(register_address, numeral_size))
        self.register_address = register_address

        numeral_size = self.LEN.REGISTER_VALUE // 8
        register_value = HexList(Numeral(register_value, numeral_size))
        self.register_value = register_value
    # end def __init__
# end class ReadSensorRegisterResponse


class WriteSensorRegisterResponse(LongEmptyPacketDataFormat):
    """
    Define ``WriteSensorRegisterResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteSensorRegister,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class WriteSensorRegisterResponse


class ResetSensorResponse(LongEmptyPacketDataFormat):
    """
    Define ``ResetSensorResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ResetSensor,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ResetSensorResponse


class ShutdownSensorResponse(LongEmptyPacketDataFormat):
    """
    Define ``ShutdownSensorResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ShutdownSensor,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ShutdownSensorResponse


class MonitorTestResponse(LongEmptyPacketDataFormat):
    """
    Define ``MonitorTestResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (MonitorTest,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class MonitorTestResponse


class StartCalibrationResponse(LongEmptyPacketDataFormat):
    """
    Define ``StartCalibrationResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class StartCalibrationResponse


class StopCalibrationResponse(CalibrationData):
    """
    Define ``StopCalibrationResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StopCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

    def __init__(self, device_index, feature_index, nb_turns, min_x, max_x, min_y, max_y, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param nb_turns: The number of complete turns affected
        :type nb_turns: ``int | HexList``
        :param min_x: X field minimum value
        :type min_x: ``HexList``
        :param max_x: X field maximum value
        :type max_x: ``HexList``
        :param min_y: Y field minimum value
        :type min_y: ``HexList``
        :param max_y: Y field maximum value
        :type max_y: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        numeral_size = self.LEN.NB_TURNS // 8
        nb_turns = HexList(Numeral(nb_turns, numeral_size))
        self.nb_turns = nb_turns

        numeral_size = self.LEN.MIN_X // 8
        min_x = HexList(Numeral(min_x, numeral_size))
        self.min_x = min_x

        numeral_size = self.LEN.MAX_X // 8
        max_x = HexList(Numeral(max_x, numeral_size))
        self.max_x = max_x

        numeral_size = self.LEN.MIN_Y // 8
        min_y = HexList(Numeral(min_y, numeral_size))
        self.min_y = min_y

        numeral_size = self.LEN.MAX_Y // 8
        max_y = HexList(Numeral(max_y, numeral_size))
        self.max_y = max_y
    # end def __init__
# end class StopCalibrationResponse


class ReadCalibrationResponse(CalibrationData):
    """
    Define ``ReadCalibrationResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, nb_turns, min_x, max_x, min_y, max_y, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param nb_turns: The number of complete turns affected
        :type nb_turns: ``int | HexList``
        :param min_x: X field minimum value
        :type min_x: ``HexList``
        :param max_x: X field maximum value
        :type max_x: ``HexList``
        :param min_y: Y field minimum value
        :type min_y: ``HexList``
        :param max_y: Y field maximum value
        :type max_y: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        numeral_size = self.LEN.NB_TURNS // 8
        nb_turns = HexList(Numeral(nb_turns, numeral_size))
        self.nb_turns = nb_turns

        numeral_size = self.LEN.MIN_X // 8
        min_x = HexList(Numeral(min_x, numeral_size))
        self.min_x = min_x

        numeral_size = self.LEN.MAX_X // 8
        max_x = HexList(Numeral(max_x, numeral_size))
        self.max_x = max_x

        numeral_size = self.LEN.MIN_Y // 8
        min_y = HexList(Numeral(min_y, numeral_size))
        self.min_y = min_y

        numeral_size = self.LEN.MAX_Y // 8
        max_y = HexList(Numeral(max_y, numeral_size))
        self.max_y = max_y
    # end def __init__
# end class ReadCalibrationResponse


class WriteCalibrationResponse(LongEmptyPacketDataFormat):
    """
    Define ``WriteCalibrationResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 8

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class WriteCalibrationResponse


class ReadTouchStatusResponse(MLX903xx):
    """
    Define ``ReadTouchStatusResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Status                        8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadTouchStatus,)
    VERSION = (0,)
    FUNCTION_INDEX = 9

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        STATUS = MLX903xx.FID.SOFTWARE_ID - 1
        PADDING = STATUS - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        STATUS = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.STATUS, length=LEN.STATUS,
                 title="Status", name="status",
                 checks=(CheckHexList(LEN.STATUS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, status, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param status: The status. 0=> untouched state. 1=> touched state.
        :type status: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        numeral_size = self.LEN.STATUS // 8
        status = HexList(Numeral(status, numeral_size))
        self.status = status
    # end def __init__
# end class ReadTouchStatusResponse


class SetRollerTestResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetRollerTestResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRollerTest,)
    VERSION = (0,)
    FUNCTION_INDEX = 10

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetRollerTestResponse


class ReadEPMIQS624RegisterResponse(RegisterAddressRegisterValueHead):
    """
    Define ``ReadEPMIQS624RegisterResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadEPMIQS624Register,)
    VERSION = (0,)
    FUNCTION_INDEX = 11

    class FID(RegisterAddressRegisterValueHead.FID):
        # See ``RegisterAddressRegisterValueHead.FID``
        PADDING = RegisterAddressRegisterValueHead.FID.REGISTER_VALUE - 1
    # end class FID

    class LEN(RegisterAddressRegisterValueHead.LEN):
        # See ``RegisterAddressRegisterValueHead.LEN``
        PADDING = 0x68
    # end class LEN

    FIELDS = RegisterAddressRegisterValueHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, register_address, register_value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_address: The register address
        :type register_address: ``int | HexList``
        :param register_value: The register value
        :type register_value: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        numeral_size = self.LEN.REGISTER_ADDRESS // 8
        register_address = HexList(Numeral(register_address, numeral_size))
        self.register_address = register_address

        numeral_size = self.LEN.REGISTER_VALUE // 8
        register_value = HexList(Numeral(register_value, numeral_size))
        self.register_value = register_value
    # end def __init__
# end class ReadEPMIQS624RegisterResponse


class MonitorReportEvent(MLX903xx):
    """
    Define ``MonitorReportEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Field X                       16
    Field Y                       16
    Field Z                       16
    Temperature                   16
    Angle                         16
    Slot                          8
    Ratchet                       8
    Angle Offset                  8
    Angle Ratchet Number          8
    Counter                       16
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        FIELD_X = MLX903xx.FID.SOFTWARE_ID - 1
        FIELD_Y = FIELD_X - 1
        FIELD_Z = FIELD_Y - 1
        TEMPERATURE = FIELD_Z - 1
        ANGLE = TEMPERATURE - 1
        SLOT = ANGLE - 1
        RATCHET = SLOT - 1
        ANGLE_OFFSET = RATCHET - 1
        ANGLE_RATCHET_NUMBER = ANGLE_OFFSET - 1
        COUNTER = ANGLE_RATCHET_NUMBER - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        FIELD_X = 0x10
        FIELD_Y = 0x10
        FIELD_Z = 0x10
        TEMPERATURE = 0x10
        ANGLE = 0x10
        SLOT = 0x8
        RATCHET = 0x8
        ANGLE_OFFSET = 0x8
        ANGLE_RATCHET_NUMBER = 0x8
        COUNTER = 0x10
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.FIELD_X, length=LEN.FIELD_X,
                 title="FieldX", name="field_x",
                 checks=(CheckHexList(LEN.FIELD_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FIELD_X) - 1),)),
        BitField(fid=FID.FIELD_Y, length=LEN.FIELD_Y,
                 title="FieldY", name="field_y",
                 checks=(CheckHexList(LEN.FIELD_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FIELD_Y) - 1),)),
        BitField(fid=FID.FIELD_Z, length=LEN.FIELD_Z,
                 title="FieldZ", name="field_z",
                 checks=(CheckHexList(LEN.FIELD_Z // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FIELD_Z) - 1),)),
        BitField(fid=FID.TEMPERATURE, length=LEN.TEMPERATURE,
                 title="Temperature", name="temperature",
                 checks=(CheckHexList(LEN.TEMPERATURE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TEMPERATURE) - 1),)),
        BitField(fid=FID.ANGLE, length=LEN.ANGLE,
                 title="Angle", name="angle",
                 checks=(CheckHexList(LEN.ANGLE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ANGLE) - 1),)),
        BitField(fid=FID.SLOT, length=LEN.SLOT,
                 title="Slot", name="slot",
                 checks=(CheckHexList(LEN.SLOT // 8), CheckByte(),)),
        BitField(fid=FID.RATCHET, length=LEN.RATCHET,
                 title="Ratchet", name="ratchet",
                 checks=(CheckHexList(LEN.RATCHET // 8), CheckByte(),)),
        BitField(fid=FID.ANGLE_OFFSET, length=LEN.ANGLE_OFFSET,
                 title="AngleOffset", name="angle_offset",
                 checks=(CheckHexList(LEN.ANGLE_OFFSET // 8), CheckByte(),)),
        BitField(fid=FID.ANGLE_RATCHET_NUMBER, length=LEN.ANGLE_RATCHET_NUMBER,
                 title="AngleRatchetNumber", name="angle_ratchet_number",
                 checks=(CheckHexList(LEN.ANGLE_RATCHET_NUMBER // 8), CheckByte(),)),
        BitField(fid=FID.COUNTER, length=LEN.COUNTER,
                 title="Counter", name="counter",
                 checks=(CheckHexList(LEN.COUNTER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNTER) - 1),)),
    )

    def __init__(self, device_index, feature_index, field_x, field_y, field_z, temperature, angle, slot, ratchet,
                 angle_offset, angle_ratchet_number, counter, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param field_x: Magnetic field value along X
        :type field_x: ``int | HexList``
        :param field_y: Magnetic field value along Y
        :type field_y: ``int | HexList``
        :param field_z: Magnetic field value along Z
        :type field_z: ``int | HexList``
        :param temperature: Temperature
        :type temperature: ``int | HexList``
        :param angle: Angle (in degree)
        :type angle: ``HexList``
        :param slot: Slot number (Signed value)
        :type slot: ``HexList``
        :param ratchet: Ratchet number (Signed value)
        :type ratchet: ``HexList``
        :param angle_offset: Offset angle versus nearest mechanical ratchet (Signed value)
        :type angle_offset: ``HexList``
        :param angle_ratchet_number: Angle Ratchet Number
        :type angle_ratchet_number: ``HexList``
        :param counter: Number of samples sent since command start (Modulo 0xFFF)
        :type counter: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        numeral_size = self.LEN.FIELD_X // 8
        field_x = HexList(Numeral(field_x, numeral_size))
        self.field_x = field_x

        numeral_size = self.LEN.FIELD_Y // 8
        field_y = HexList(Numeral(field_y, numeral_size))
        self.field_y = field_y

        numeral_size = self.LEN.FIELD_Z // 8
        field_z = HexList(Numeral(field_z, numeral_size))
        self.field_z = field_z

        numeral_size = self.LEN.TEMPERATURE // 8
        temperature = HexList(Numeral(temperature, numeral_size))
        self.temperature = temperature

        numeral_size = self.LEN.ANGLE // 8
        angle = HexList(Numeral(angle, numeral_size))
        self.angle = angle

        numeral_size = self.LEN.SLOT // 8
        slot = HexList(Numeral(slot, numeral_size))
        self.slot = slot

        numeral_size = self.LEN.RATCHET // 8
        ratchet = HexList(Numeral(ratchet, numeral_size))
        self.ratchet = ratchet

        numeral_size = self.LEN.ANGLE_OFFSET // 8
        angle_offset = HexList(Numeral(angle_offset, numeral_size))
        self.angle_offset = angle_offset

        numeral_size = self.LEN.ANGLE_RATCHET_NUMBER // 8
        angle_ratchet_number = HexList(Numeral(angle_ratchet_number, numeral_size))
        self.angle_ratchet_number = angle_ratchet_number

        numeral_size = self.LEN.COUNTER // 8
        counter = HexList(Numeral(counter, numeral_size))
        self.counter = counter
    # end def __init__
# end class MonitorReportEvent


class RollerTestEvent(MLX903xx):
    """
    Define ``RollerTestEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Accumulator                   16
    Timestamp Value               32
    Padding                       80
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(MLX903xx.FID):
        # See ``MLX903xx.FID``
        ACCUMULATOR = MLX903xx.FID.SOFTWARE_ID - 1
        TIMESTAMP_VALUE = ACCUMULATOR - 1
        PADDING = TIMESTAMP_VALUE - 1
    # end class FID

    class LEN(MLX903xx.LEN):
        # See ``MLX903xx.LEN``
        ACCUMULATOR = 0x10
        TIMESTAMP_VALUE = 0x20
        PADDING = 0x50
    # end class LEN

    FIELDS = MLX903xx.FIELDS + (
        BitField(fid=FID.ACCUMULATOR, length=LEN.ACCUMULATOR,
                 title="Accumulator", name="accumulator",
                 checks=(CheckHexList(LEN.ACCUMULATOR // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ACCUMULATOR) - 1),)),
        BitField(fid=FID.TIMESTAMP_VALUE, length=LEN.TIMESTAMP_VALUE,
                 title="TimestampValue", name="timestamp_value",
                 checks=(CheckHexList(LEN.TIMESTAMP_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TIMESTAMP_VALUE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MLX903xx.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, accumulator, timestamp_value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param accumulator: The aggregated roller reports [1/10 degree]
        :type accumulator: ``HexList``
        :param timestamp_value: The timestamp [us]
        :type timestamp_value: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        numeral_size = self.LEN.ACCUMULATOR // 8
        accumulator = HexList(Numeral(accumulator, numeral_size))
        self.accumulator = accumulator

        numeral_size = self.LEN.TIMESTAMP_VALUE // 8
        timestamp_value = HexList(Numeral(timestamp_value, numeral_size))
        self.timestamp_value = timestamp_value
    # end def __init__
# end class RollerTestEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
