#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.mouse.extendedadjustabledpi
:brief: HID++ 2.0 ``ExtendedAdjustableDpi`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
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


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableDpi(HidppMessage):
    """
    This feature handles the resolution on motion sensors (mainly optical for mice, but could be 3D)
    """
    FEATURE_ID = 0x2202
    MAX_FUNCTION_INDEX = 10
    CALIBRATION_FAILED = 0x8000

    class Direction:
        """
        XY Direction
        """
        X = 0
        Y = 1
    # end class Direction

    class LodLevel:
        """
        LOD (Lift Off Distance) Level
        """
        NOT_SUPPORTED = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
    # end class LodLevel

    class LedHoldType:
        """
        LED hold types
        """
        TIMER_BASED = 0
        EVENT_BASED = 1
        SW_CONTROL_ON = 2
        SW_CONTROL_OFF = 3
    # end class LedHoldType

    class CalibType:
        """
        The type of DPI calibration
        """
        HW = 0
        SW = 1
    # end class CalibType

    class RevertCommand:
        """
        Revert command for DPI calibration
        """
        TO_CURRENT_PROFILE = HexList(0x8000.to_bytes(2, 'big'))
        TO_OOB_PROFILE = HexList(0x0000.to_bytes(2, 'big'))
    # end class RevertCommand

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class ExtendedAdjustableDpi


class ExtendedAdjustableDpiModel(FeatureModel):
    """
    Define ``ExtendedAdjustableDpi`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_SENSOR_COUNT = 0
        GET_SENSOR_CAPABILITIES = 1
        GET_SENSOR_DPI_RANGES = 2
        GET_SENSOR_DPI_LIST = 3
        GET_SENSOR_LOD_LIST = 4
        GET_SENSOR_DPI_PARAMETERS = 5
        SET_SENSOR_DPI_PARAMETERS = 6
        SHOW_SENSOR_DPI_STATUS = 7
        GET_DPI_CALIBRATION_INFO = 8
        START_DPI_CALIBRATION = 9
        SET_DPI_CALIBRATION = 10

        # Event index
        SENSOR_DPI_PARAMETERS = 0
        DPI_CALIBRATION_COMPLETED = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ExtendedAdjustableDpi`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_SENSOR_COUNT: {
                    "request": GetSensorCount,
                    "response": GetSensorCountResponse
                },
                cls.INDEX.GET_SENSOR_CAPABILITIES: {
                    "request": GetSensorCapabilities,
                    "response": GetSensorCapabilitiesResponse
                },
                cls.INDEX.GET_SENSOR_DPI_RANGES: {
                    "request": GetSensorDpiRanges,
                    "response": GetSensorDpiRangesResponse
                },
                cls.INDEX.GET_SENSOR_DPI_LIST: {
                    "request": GetSensorDpiList,
                    "response": GetSensorDpiListResponse
                },
                cls.INDEX.GET_SENSOR_LOD_LIST: {
                    "request": GetSensorLodList,
                    "response": GetSensorLodListResponse
                },
                cls.INDEX.GET_SENSOR_DPI_PARAMETERS: {
                    "request": GetSensorDpiParameters,
                    "response": GetSensorDpiParametersResponse
                },
                cls.INDEX.SET_SENSOR_DPI_PARAMETERS: {
                    "request": SetSensorDpiParameters,
                    "response": SetSensorDpiParametersResponse
                },
                cls.INDEX.SHOW_SENSOR_DPI_STATUS: {
                    "request": ShowSensorDpiStatus,
                    "response": ShowSensorDpiStatusResponse
                },
                cls.INDEX.GET_DPI_CALIBRATION_INFO: {
                    "request": GetDpiCalibrationInfo,
                    "response": GetDpiCalibrationInfoResponse
                },
                cls.INDEX.START_DPI_CALIBRATION: {
                    "request": StartDpiCalibration,
                    "response": StartDpiCalibrationResponse
                },
                cls.INDEX.SET_DPI_CALIBRATION: {
                    "request": SetDpiCalibration,
                    "response": SetDpiCalibrationResponse
                }
            },
            "events": {
                cls.INDEX.SENSOR_DPI_PARAMETERS: {"report": SensorDpiParametersEvent},
                cls.INDEX.DPI_CALIBRATION_COMPLETED: {"report": DpiCalibrationCompletedEvent}
            }
        }

        return {
            "feature_base": ExtendedAdjustableDpi,
            "versions": {
                ExtendedAdjustableDpiV0.VERSION: {
                    "main_cls": ExtendedAdjustableDpiV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class ExtendedAdjustableDpiModel


class ExtendedAdjustableDpiFactory(FeatureFactory):
    """
    Get ``ExtendedAdjustableDpi`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ExtendedAdjustableDpi`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``ExtendedAdjustableDpiInterface``
        """
        return ExtendedAdjustableDpiModel.get_main_cls(version)()
    # end def create
# end class ExtendedAdjustableDpiFactory


class ExtendedAdjustableDpiInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ExtendedAdjustableDpi``
    """

    def __init__(self):
        # Requests
        self.get_sensor_count_cls = None
        self.get_sensor_capabilities_cls = None
        self.get_sensor_dpi_ranges_cls = None
        self.get_sensor_dpi_list_cls = None
        self.get_sensor_lod_list_cls = None
        self.get_sensor_dpi_parameters_cls = None
        self.set_sensor_dpi_parameters_cls = None
        self.show_sensor_dpi_status_cls = None
        self.get_dpi_calibration_info_cls = None
        self.start_dpi_calibration_cls = None
        self.set_dpi_calibration_cls = None

        # Responses
        self.get_sensor_count_response_cls = None
        self.get_sensor_capabilities_response_cls = None
        self.get_sensor_dpi_ranges_response_cls = None
        self.get_sensor_dpi_list_response_cls = None
        self.get_sensor_lod_list_response_cls = None
        self.get_sensor_dpi_parameters_response_cls = None
        self.set_sensor_dpi_parameters_response_cls = None
        self.show_sensor_dpi_status_response_cls = None
        self.get_dpi_calibration_info_response_cls = None
        self.start_dpi_calibration_response_cls = None
        self.set_dpi_calibration_response_cls = None

        # Events
        self.sensor_dpi_parameters_event_cls = None
        self.dpi_calibration_completed_event_cls = None
    # end def __init__
# end class ExtendedAdjustableDpiInterface


class ExtendedAdjustableDpiV0(ExtendedAdjustableDpiInterface):
    """
    Define ``ExtendedAdjustableDpiV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetSensorCount() -> numSensor

    [1] GetSensorCapabilities(sensorIdx) -> sensorIdx, numDpiLevels, profileSupported, calibrationSupported,
        lodSupported, dpiYSupported

    [2] GetSensorDpiRanges(sensorIdx, direction, dpiRangeReqIdx) -> sensorIdx, direction, dpiRangeReqIdx, dpiRanges1,
        dpiRanges2, dpiRanges3, dpiRanges4, dpiRanges5, dpiRanges6, dpiRanges7MSB

    [3] GetSensorDpiList(sensorIdx, direction) -> sensorIdx, direction, dpiList1, dpiList2, dpiList3, dpiList4,
        dpiList5, dpiList6

    [4] GetSensorLodList(sensorIdx) -> sensorIdx, lod1, lod2, lod3, lod4, lod5

    [5] GetSensorDpiParameters(sensorIdx) -> sensorIdx, dpiX, defaultDpiX, dpiY, defaultDpiY, lod

    [6] SetSensorDpiParameters(sensorIdx, dpiX, dpiY, lod) -> sensorIdx, dpiX, dpiY, lod

    [7] ShowSensorDpiStatus(sensorIdx, dpiLevel, ledHoldType, buttonNum) -> sensorIdx, dpiLevel, ledHoldType,
        buttonNum

    [8] GetDpiCalibrationInfo(sensorIdx) -> sensorIdx, mouseWidth, mouseLength, calibDpiX, calibDpiY

    [9] StartDpiCalibration(sensorIdx, direction, expectedCount, calibType, calibStartTimeout, calibHWProcessTimeout,
        calibSWProcessTimeout) -> sensorIdx, direction, expectedCount, calibType, calibStartTimeout,
        calibHWProcessTimeout, calibSWProcessTimeout

    [10] SetDpiCalibration(sensorIdx, direction, calibCor) -> sensorIdx, direction, calibCor

    [Event 0] SensorDpiParametersEvent -> sensorIdx, dpiX, dpiY, lod

    [Event 1] DpiCalibrationCompletedEvent -> sensorIdx, direction, calibCor, calibDelta
    """
    VERSION = 0

    def __init__(self):
        # See ``ExtendedAdjustableDpi.__init__``
        super().__init__()
        index = ExtendedAdjustableDpiModel.INDEX

        # Requests
        self.get_sensor_count_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.GET_SENSOR_COUNT)
        self.get_sensor_capabilities_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.GET_SENSOR_CAPABILITIES)
        self.get_sensor_dpi_ranges_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.GET_SENSOR_DPI_RANGES)
        self.get_sensor_dpi_list_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.GET_SENSOR_DPI_LIST)
        self.get_sensor_lod_list_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.GET_SENSOR_LOD_LIST)
        self.get_sensor_dpi_parameters_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.GET_SENSOR_DPI_PARAMETERS)
        self.set_sensor_dpi_parameters_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.SET_SENSOR_DPI_PARAMETERS)
        self.show_sensor_dpi_status_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.SHOW_SENSOR_DPI_STATUS)
        self.get_dpi_calibration_info_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.GET_DPI_CALIBRATION_INFO)
        self.start_dpi_calibration_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.START_DPI_CALIBRATION)
        self.set_dpi_calibration_cls = ExtendedAdjustableDpiModel.get_request_cls(
            self.VERSION, index.SET_DPI_CALIBRATION)

        # Responses
        self.get_sensor_count_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.GET_SENSOR_COUNT)
        self.get_sensor_capabilities_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.GET_SENSOR_CAPABILITIES)
        self.get_sensor_dpi_ranges_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.GET_SENSOR_DPI_RANGES)
        self.get_sensor_dpi_list_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.GET_SENSOR_DPI_LIST)
        self.get_sensor_lod_list_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.GET_SENSOR_LOD_LIST)
        self.get_sensor_dpi_parameters_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.GET_SENSOR_DPI_PARAMETERS)
        self.set_sensor_dpi_parameters_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.SET_SENSOR_DPI_PARAMETERS)
        self.show_sensor_dpi_status_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.SHOW_SENSOR_DPI_STATUS)
        self.get_dpi_calibration_info_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.GET_DPI_CALIBRATION_INFO)
        self.start_dpi_calibration_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.START_DPI_CALIBRATION)
        self.set_dpi_calibration_response_cls = ExtendedAdjustableDpiModel.get_response_cls(
            self.VERSION, index.SET_DPI_CALIBRATION)

        # Events
        self.sensor_dpi_parameters_event_cls = ExtendedAdjustableDpiModel.get_report_cls(
            self.VERSION, index.SENSOR_DPI_PARAMETERS)
        self.dpi_calibration_completed_event_cls = ExtendedAdjustableDpiModel.get_report_cls(
            self.VERSION, index.DPI_CALIBRATION_COMPLETED)
    # end def __init__

    def get_max_function_index(self):
        # See ``ExtendedAdjustableDpiInterface.get_max_function_index``
        return ExtendedAdjustableDpiModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ExtendedAdjustableDpiV0


class ShortEmptyPacketDataFormat(ExtendedAdjustableDpi):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetSensorCount

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        PADDING = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class SensorDataFormat(ExtendedAdjustableDpi):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetSensorCapabilities
        - GetSensorLodList
        - GetSensorDpiParameters
        - GetDpiCalibrationInfo

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    Padding                       16
    ============================  ==========
    """

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        PADDING = SENSOR_IDX - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.PADDING),
    )
# end class SensorDataFormat


class SensorDpiDataFormat(ExtendedAdjustableDpi):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - SetSensorDpiParameters
        - SetSensorDpiParametersResponse
        - SensorDpiParametersEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    dpi x                         16
    dpi y                         16
    lod                           8
    ============================  ==========
    """

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DPI_X = SENSOR_IDX - 1
        DPI_Y = DPI_X - 1
        LOD = DPI_Y - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DPI_X = 0x10
        DPI_Y = 0x10
        LOD = 0x8
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DPI_X, length=LEN.DPI_X,
                 title="DpiX", name="dpi_x",
                 checks=(CheckHexList(LEN.DPI_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_X) - 1),)),
        BitField(fid=FID.DPI_Y, length=LEN.DPI_Y,
                 title="DpiY", name="dpi_y",
                 checks=(CheckHexList(LEN.DPI_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_Y) - 1),)),
        BitField(fid=FID.LOD, length=LEN.LOD,
                 title="Lod", name="lod",
                 checks=(CheckHexList(LEN.LOD // 8),
                         CheckByte(),)),
    )
# end class SensorDpiDataFormat


class ShowSensorDPIStatusDataFormat(ExtendedAdjustableDpi):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - ShowSensorDpiStatus
        - ShowSensorDpiStatusResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    dpi level                     8
    led hold type                 8
    button num                    8
    ============================  ==========
    """

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DPI_LEVEL = SENSOR_IDX - 1
        LED_HOLD_TYPE = DPI_LEVEL - 1
        BUTTON_NUM = LED_HOLD_TYPE - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DPI_LEVEL = 0x8
        LED_HOLD_TYPE = 0x8
        BUTTON_NUM = 0x8
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DPI_LEVEL, length=LEN.DPI_LEVEL,
                 title="DpiLevel", name="dpi_level",
                 checks=(CheckHexList(LEN.DPI_LEVEL // 8),
                         CheckByte(),)),
        BitField(fid=FID.LED_HOLD_TYPE, length=LEN.LED_HOLD_TYPE,
                 title="LedHoldType", name="led_hold_type",
                 checks=(CheckHexList(LEN.LED_HOLD_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.BUTTON_NUM, length=LEN.BUTTON_NUM,
                 title="ButtonNum", name="button_num",
                 checks=(CheckHexList(LEN.BUTTON_NUM // 8),
                         CheckByte(),)),
    )
# end class ShowSensorDPIStatusDataFormat


class StartDpiCalibrationDataFormat(ExtendedAdjustableDpi):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - StartDpiCalibration
        - StartDpiCalibrationResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    expected count                16
    calib type                    8
    calib start timeout           8
    calib HW process timeout      8
    calib SW process timeout      8
    ============================  ==========
    """

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DIRECTION = SENSOR_IDX - 1
        EXPECTED_COUNT = DIRECTION - 1
        CALIB_TYPE = EXPECTED_COUNT - 1
        CALIB_START_TIMEOUT = CALIB_TYPE - 1
        CALIB_HW_PROCESS_TIMEOUT = CALIB_START_TIMEOUT - 1
        CALIB_SW_PROCESS_TIMEOUT = CALIB_HW_PROCESS_TIMEOUT - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DIRECTION = 0x8
        EXPECTED_COUNT = 0x10
        CALIB_TYPE = 0x8
        CALIB_START_TIMEOUT = 0x8
        CALIB_HW_PROCESS_TIMEOUT = 0x8
        CALIB_SW_PROCESS_TIMEOUT = 0x8
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DIRECTION, length=LEN.DIRECTION,
                 title="Direction", name="direction",
                 checks=(CheckHexList(LEN.DIRECTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.EXPECTED_COUNT, length=LEN.EXPECTED_COUNT,
                 title="ExpectedCount", name="expected_count",
                 checks=(CheckHexList(LEN.EXPECTED_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EXPECTED_COUNT) - 1),)),
        BitField(fid=FID.CALIB_TYPE, length=LEN.CALIB_TYPE,
                 title="CalibType", name="calib_type",
                 checks=(CheckHexList(LEN.CALIB_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.CALIB_START_TIMEOUT, length=LEN.CALIB_START_TIMEOUT,
                 title="CalibStartTimeout", name="calib_start_timeout",
                 checks=(CheckHexList(LEN.CALIB_START_TIMEOUT // 8),
                         CheckByte(),)),
        BitField(fid=FID.CALIB_HW_PROCESS_TIMEOUT, length=LEN.CALIB_HW_PROCESS_TIMEOUT,
                 title="CalibHwProcessTimeout", name="calib_hw_process_timeout",
                 checks=(CheckHexList(LEN.CALIB_HW_PROCESS_TIMEOUT // 8),
                         CheckByte(),)),
        BitField(fid=FID.CALIB_SW_PROCESS_TIMEOUT, length=LEN.CALIB_SW_PROCESS_TIMEOUT,
                 title="CalibSwProcessTimeout", name="calib_sw_process_timeout",
                 checks=(CheckHexList(LEN.CALIB_SW_PROCESS_TIMEOUT // 8),
                         CheckByte(),)),
    )
# end class StartDpiCalibrationDataFormat


class SetDpiCalibrationDataFormat(ExtendedAdjustableDpi):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - SetDpiCalibration
        - SetDpiCalibrationResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    calib cor                     16
    ============================  ==========
    """

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DIRECTION = SENSOR_IDX - 1
        CALIB_COR = DIRECTION - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DIRECTION = 0x8
        CALIB_COR = 0x10
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DIRECTION, length=LEN.DIRECTION,
                 title="Direction", name="direction",
                 checks=(CheckHexList(LEN.DIRECTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.CALIB_COR, length=LEN.CALIB_COR,
                 title="CalibCor", name="calib_cor",
                 checks=(CheckHexList(LEN.CALIB_COR // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CALIB_COR) - 1),)),
    )
# end class SetDpiCalibrationDataFormat


class GetSensorCount(ShortEmptyPacketDataFormat):
    """
    Define ``GetSensorCount`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetSensorCountResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetSensorCount


class GetSensorCountResponse(ExtendedAdjustableDpi):
    """
    Define ``GetSensorCountResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    num sensor                    8
    reserved                      120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorCount,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        NUM_SENSOR = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        RESERVED = NUM_SENSOR - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        NUM_SENSOR = 0x8
        RESERVED = 0x78
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.NUM_SENSOR, length=LEN.NUM_SENSOR,
                 title="NumSensor", name="num_sensor",
                 checks=(CheckHexList(LEN.NUM_SENSOR // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, num_sensor, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param num_sensor: Number of sensors in device
        :type num_sensor: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.num_sensor = num_sensor
    # end def __init__
# end class GetSensorCountResponse


class GetSensorCapabilities(SensorDataFormat):
    """
    Define ``GetSensorCapabilities`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, sensor_idx, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetSensorCapabilitiesResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.sensor_idx = sensor_idx
    # end def __init__
# end class GetSensorCapabilities


class GetSensorCapabilitiesResponse(ExtendedAdjustableDpi):
    """
    Define ``GetSensorCapabilitiesResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    num dpi levels                8
    reserved                      4
    profile supported             1
    calibration supported         1
    lod supported                 1
    dpi y supported               1
    reserved                      104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        NUM_DPI_LEVELS = SENSOR_IDX - 1
        RESERVED_4BITS = NUM_DPI_LEVELS - 1
        PROFILE_SUPPORTED = RESERVED_4BITS - 1
        CALIBRATION_SUPPORTED = PROFILE_SUPPORTED - 1
        LOD_SUPPORTED = CALIBRATION_SUPPORTED - 1
        DPI_Y_SUPPORTED = LOD_SUPPORTED - 1
        RESERVED = DPI_Y_SUPPORTED - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        NUM_DPI_LEVELS = 0x8
        RESERVED_4BITS = 0x4
        PROFILE_SUPPORTED = 0x1
        CALIBRATION_SUPPORTED = 0x1
        LOD_SUPPORTED = 0x1
        DPI_Y_SUPPORTED = 0x1
        RESERVED = 0x68
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.NUM_DPI_LEVELS, length=LEN.NUM_DPI_LEVELS,
                 title="NumDpiLevels", name="num_dpi_levels",
                 checks=(CheckHexList(LEN.NUM_DPI_LEVELS // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED_4BITS, length=LEN.RESERVED_4BITS,
                 title="Reserved4Bits", name="reserved_4bits",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED_4BITS) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
        BitField(fid=FID.PROFILE_SUPPORTED, length=LEN.PROFILE_SUPPORTED,
                 title="ProfileSupported", name="profile_supported",
                 checks=(CheckInt(0, pow(2, LEN.PROFILE_SUPPORTED) - 1),)),
        BitField(fid=FID.CALIBRATION_SUPPORTED, length=LEN.CALIBRATION_SUPPORTED,
                 title="CalibrationSupported", name="calibration_supported",
                 checks=(CheckInt(0, pow(2, LEN.CALIBRATION_SUPPORTED) - 1),)),
        BitField(fid=FID.LOD_SUPPORTED, length=LEN.LOD_SUPPORTED,
                 title="LodSupported", name="lod_supported",
                 checks=(CheckInt(0, pow(2, LEN.LOD_SUPPORTED) - 1),)),
        BitField(fid=FID.DPI_Y_SUPPORTED, length=LEN.DPI_Y_SUPPORTED,
                 title="DpiYSupported", name="dpi_y_supported",
                 checks=(CheckInt(0, pow(2, LEN.DPI_Y_SUPPORTED) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, num_dpi_levels, profile_supported,
                 calibration_supported, lod_supported, dpi_y_supported, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param num_dpi_levels: Number of DPI levels [0..N]
        :type num_dpi_levels: ``int`` or ``HexList``
        :param profile_supported: Indicate whether Profile related to DPI is supported or not
        :type profile_supported: ``bool`` or ``HexList``
        :param calibration_supported: Indicate whether DPI calibration is supported or not
        :type calibration_supported: ``bool`` or ``HexList``
        :param lod_supported: Indicate whether LOD (Lift Off Distance) is supported or not
        :type lod_supported: ``bool`` or ``HexList``
        :param dpi_y_supported: Indicate whether DPI Y direction is supported or not
        :type dpi_y_supported: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.num_dpi_levels = num_dpi_levels
        self.profile_supported = profile_supported
        self.calibration_supported = calibration_supported
        self.lod_supported = lod_supported
        self.dpi_y_supported = dpi_y_supported
    # end def __init__
# end class GetSensorCapabilitiesResponse


class GetSensorDpiRanges(ExtendedAdjustableDpi):
    """
    Define ``GetSensorDpiRanges`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    dpi range req idx             8
    ============================  ==========
    """

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DIRECTION = SENSOR_IDX - 1
        DPI_RANGE_REQ_IDX = DIRECTION - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DIRECTION = 0x8
        DPI_RANGE_REQ_IDX = 0x8
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DIRECTION, length=LEN.DIRECTION,
                 title="Direction", name="direction",
                 checks=(CheckHexList(LEN.DIRECTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.DPI_RANGE_REQ_IDX, length=LEN.DPI_RANGE_REQ_IDX,
                 title="DpiRangeReqIdx", name="dpi_range_req_idx",
                 checks=(CheckHexList(LEN.DPI_RANGE_REQ_IDX // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, dpi_range_req_idx, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param dpi_range_req_idx: The index of DPI range request. This index starts from 0 and needs to be incremented
                                  by "1" till end of list received.
        :type dpi_range_req_idx: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetSensorDpiRangesResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
        self.dpi_range_req_idx = dpi_range_req_idx
    # end def __init__
# end class GetSensorDpiRanges


class GetSensorDpiRangesResponse(ExtendedAdjustableDpi):
    """
    Define ``GetSensorDpiRangesResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    dpi range req idx             8
    dpi ranges 1                  16
    dpi ranges 2                  16
    dpi ranges 3                  16
    dpi ranges 4                  16
    dpi ranges 5                  16
    dpi ranges 6                  16
    dpi ranges 7 MSB              8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorDpiRanges,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DIRECTION = SENSOR_IDX - 1
        DPI_RANGE_REQ_IDX = DIRECTION - 1
        DPI_RANGES_1 = DPI_RANGE_REQ_IDX - 1
        DPI_RANGES_2 = DPI_RANGES_1 - 1
        DPI_RANGES_3 = DPI_RANGES_2 - 1
        DPI_RANGES_4 = DPI_RANGES_3 - 1
        DPI_RANGES_5 = DPI_RANGES_4 - 1
        DPI_RANGES_6 = DPI_RANGES_5 - 1
        DPI_RANGES_7_MSB = DPI_RANGES_6 - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DIRECTION = 0x8
        DPI_RANGE_REQ_IDX = 0x8
        DPI_RANGES_1 = 0x10
        DPI_RANGES_2 = 0x10
        DPI_RANGES_3 = 0x10
        DPI_RANGES_4 = 0x10
        DPI_RANGES_5 = 0x10
        DPI_RANGES_6 = 0x10
        DPI_RANGES_7_MSB = 0x8
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DIRECTION, length=LEN.DIRECTION,
                 title="Direction", name="direction",
                 checks=(CheckHexList(LEN.DIRECTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.DPI_RANGE_REQ_IDX, length=LEN.DPI_RANGE_REQ_IDX,
                 title="DpiRangeReqIdx", name="dpi_range_req_idx",
                 checks=(CheckHexList(LEN.DPI_RANGE_REQ_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DPI_RANGES_1, length=LEN.DPI_RANGES_1,
                 title="DpiRanges1", name="dpi_ranges_1",
                 checks=(CheckHexList(LEN.DPI_RANGES_1 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_RANGES_1) - 1),)),
        BitField(fid=FID.DPI_RANGES_2, length=LEN.DPI_RANGES_2,
                 title="DpiRanges2", name="dpi_ranges_2",
                 checks=(CheckHexList(LEN.DPI_RANGES_2 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_RANGES_2) - 1),)),
        BitField(fid=FID.DPI_RANGES_3, length=LEN.DPI_RANGES_3,
                 title="DpiRanges3", name="dpi_ranges_3",
                 checks=(CheckHexList(LEN.DPI_RANGES_3 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_RANGES_3) - 1),)),
        BitField(fid=FID.DPI_RANGES_4, length=LEN.DPI_RANGES_4,
                 title="DpiRanges4", name="dpi_ranges_4",
                 checks=(CheckHexList(LEN.DPI_RANGES_4 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_RANGES_4) - 1),)),
        BitField(fid=FID.DPI_RANGES_5, length=LEN.DPI_RANGES_5,
                 title="DpiRanges5", name="dpi_ranges_5",
                 checks=(CheckHexList(LEN.DPI_RANGES_5 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_RANGES_5) - 1),)),
        BitField(fid=FID.DPI_RANGES_6, length=LEN.DPI_RANGES_6,
                 title="DpiRanges6", name="dpi_ranges_6",
                 checks=(CheckHexList(LEN.DPI_RANGES_6 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_RANGES_6) - 1),)),
        BitField(fid=FID.DPI_RANGES_7_MSB, length=LEN.DPI_RANGES_7_MSB,
                 title="DpiRanges7MSB", name="dpi_ranges_7_msb",
                 checks=(CheckHexList(LEN.DPI_RANGES_7_MSB // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, dpi_range_req_idx, dpi_ranges_1,
                 dpi_ranges_2, dpi_ranges_3, dpi_ranges_4, dpi_ranges_5, dpi_ranges_6, dpi_ranges_7_msb, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param dpi_range_req_idx: The index of DPI range request. This index starts from 0 and needs to be incremented
                                  by "1" till end of list received.
        :type dpi_range_req_idx: ``int`` or ``HexList``
        :param dpi_ranges_1: DPI: 1..0xDFFF, Step: 0xE001..0xFFFF, Unused: 0xE000, End: 0x0000
        :type dpi_ranges_1: ``int`` or ``HexList``
        :param dpi_ranges_2: DPI: 1..0xDFFF, Step: 0xE001..0xFFFF, Unused: 0xE000, End: 0x0000
        :type dpi_ranges_2: ``int`` or ``HexList``
        :param dpi_ranges_3: DPI: 1..0xDFFF, Step: 0xE001..0xFFFF, Unused: 0xE000, End: 0x0000
        :type dpi_ranges_3: ``int`` or ``HexList``
        :param dpi_ranges_4: DPI: 1..0xDFFF, Step: 0xE001..0xFFFF, Unused: 0xE000, End: 0x0000
        :type dpi_ranges_4: ``int`` or ``HexList``
        :param dpi_ranges_5: DPI: 1..0xDFFF, Step: 0xE001..0xFFFF, Unused: 0xE000, End: 0x0000
        :type dpi_ranges_5: ``int`` or ``HexList``
        :param dpi_ranges_6: DPI: 1..0xDFFF, Step: 0xE001..0xFFFF, Unused: 0xE000, End: 0x0000
        :type dpi_ranges_6: ``int`` or ``HexList``
        :param dpi_ranges_7_msb: DPI: 1..0xDFFF, Step: 0xE001..0xFFFF, Unused: 0xE000, End: 0x0000
        :type dpi_ranges_7_msb: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
        self.dpi_range_req_idx = dpi_range_req_idx
        self.dpi_ranges_1 = dpi_ranges_1
        self.dpi_ranges_2 = dpi_ranges_2
        self.dpi_ranges_3 = dpi_ranges_3
        self.dpi_ranges_4 = dpi_ranges_4
        self.dpi_ranges_5 = dpi_ranges_5
        self.dpi_ranges_6 = dpi_ranges_6
        self.dpi_ranges_7_msb = dpi_ranges_7_msb
    # end def __init__
# end class GetSensorDpiRangesResponse


class GetSensorDpiList(ExtendedAdjustableDpi):
    """
    Define ``GetSensorDpiList`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    Padding                       8
    ============================  ==========
    """

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DIRECTION = SENSOR_IDX - 1
        PADDING = DIRECTION - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DIRECTION = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DIRECTION, length=LEN.DIRECTION,
                 title="Direction", name="direction",
                 checks=(CheckHexList(LEN.DIRECTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetSensorDpiListResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
    # end def __init__
# end class GetSensorDpiList


class GetSensorDpiListResponse(ExtendedAdjustableDpi):
    """
    Define ``GetSensorDpiListResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    dpi list 1                    16
    dpi list 2                    16
    dpi list 3                    16
    dpi list 4                    16
    dpi list 5                    16
    dpi list 6                    16
    reserved                      16
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorDpiList,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DIRECTION = SENSOR_IDX - 1
        DPI_LIST_1 = DIRECTION - 1
        DPI_LIST_2 = DPI_LIST_1 - 1
        DPI_LIST_3 = DPI_LIST_2 - 1
        DPI_LIST_4 = DPI_LIST_3 - 1
        DPI_LIST_5 = DPI_LIST_4 - 1
        DPI_LIST_6 = DPI_LIST_5 - 1
        RESERVED = DPI_LIST_6 - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DIRECTION = 0x8
        DPI_LIST_1 = 0x10
        DPI_LIST_2 = 0x10
        DPI_LIST_3 = 0x10
        DPI_LIST_4 = 0x10
        DPI_LIST_5 = 0x10
        DPI_LIST_6 = 0x10
        RESERVED = 0x10
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DIRECTION, length=LEN.DIRECTION,
                 title="Direction", name="direction",
                 checks=(CheckHexList(LEN.DIRECTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.DPI_LIST_1, length=LEN.DPI_LIST_1,
                 title="DpiList1", name="dpi_list_1",
                 checks=(CheckHexList(LEN.DPI_LIST_1 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_LIST_1) - 1),)),
        BitField(fid=FID.DPI_LIST_2, length=LEN.DPI_LIST_2,
                 title="DpiList2", name="dpi_list_2",
                 checks=(CheckHexList(LEN.DPI_LIST_2 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_LIST_2) - 1),)),
        BitField(fid=FID.DPI_LIST_3, length=LEN.DPI_LIST_3,
                 title="DpiList3", name="dpi_list_3",
                 checks=(CheckHexList(LEN.DPI_LIST_3 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_LIST_3) - 1),)),
        BitField(fid=FID.DPI_LIST_4, length=LEN.DPI_LIST_4,
                 title="DpiList4", name="dpi_list_4",
                 checks=(CheckHexList(LEN.DPI_LIST_4 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_LIST_4) - 1),)),
        BitField(fid=FID.DPI_LIST_5, length=LEN.DPI_LIST_5,
                 title="DpiList5", name="dpi_list_5",
                 checks=(CheckHexList(LEN.DPI_LIST_5 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_LIST_5) - 1),)),
        BitField(fid=FID.DPI_LIST_6, length=LEN.DPI_LIST_6,
                 title="DpiList6", name="dpi_list_6",
                 checks=(CheckHexList(LEN.DPI_LIST_6 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_LIST_6) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, dpi_list_1, dpi_list_2, dpi_list_3,
                 dpi_list_4, dpi_list_5, dpi_list_6, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param dpi_list_1: The DPI value in the 1st DPI slot in the profile
        :type dpi_list_1: ``int`` or ``HexList``
        :param dpi_list_2: The DPI value in the 2nd DPI slot in the profile
        :type dpi_list_2: ``int`` or ``HexList``
        :param dpi_list_3: The DPI value in the 3rd DPI slot in the profile
        :type dpi_list_3: ``int`` or ``HexList``
        :param dpi_list_4: The DPI value in the 4rth DPI slot in the profile
        :type dpi_list_4: ``int`` or ``HexList``
        :param dpi_list_5: The DPI value in the 5th DPI slot in the profile
        :type dpi_list_5: ``int`` or ``HexList``
        :param dpi_list_6: The DPI value in the 6th DPI slot. (Up to Profile Format v6, it supports 5 DPI slots only)
        :type dpi_list_6: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
        self.dpi_list_1 = dpi_list_1
        self.dpi_list_2 = dpi_list_2
        self.dpi_list_3 = dpi_list_3
        self.dpi_list_4 = dpi_list_4
        self.dpi_list_5 = dpi_list_5
        self.dpi_list_6 = dpi_list_6
    # end def __init__
# end class GetSensorDpiListResponse


class GetSensorLodList(SensorDataFormat):
    """
    Define ``GetSensorLodList`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, sensor_idx, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetSensorLodListResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.sensor_idx = sensor_idx
    # end def __init__
# end class GetSensorLodList


class GetSensorLodListResponse(ExtendedAdjustableDpi):
    """
    Define ``GetSensorLodListResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    lod 1                         8
    lod 2                         8
    lod 3                         8
    lod 4                         8
    lod 5                         8
    reserved                      80
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorLodList,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        LOD_1 = SENSOR_IDX - 1
        LOD_2 = LOD_1 - 1
        LOD_3 = LOD_2 - 1
        LOD_4 = LOD_3 - 1
        LOD_5 = LOD_4 - 1
        RESERVED = LOD_5 - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        LOD_1 = 0x8
        LOD_2 = 0x8
        LOD_3 = 0x8
        LOD_4 = 0x8
        LOD_5 = 0x8
        RESERVED = 0x50
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.LOD_1, length=LEN.LOD_1,
                 title="Lod1", name="lod_1",
                 checks=(CheckHexList(LEN.LOD_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.LOD_2, length=LEN.LOD_2,
                 title="Lod2", name="lod_2",
                 checks=(CheckHexList(LEN.LOD_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.LOD_3, length=LEN.LOD_3,
                 title="Lod3", name="lod_3",
                 checks=(CheckHexList(LEN.LOD_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.LOD_4, length=LEN.LOD_4,
                 title="Lod4", name="lod_4",
                 checks=(CheckHexList(LEN.LOD_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.LOD_5, length=LEN.LOD_5,
                 title="Lod5", name="lod_5",
                 checks=(CheckHexList(LEN.LOD_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, lod_1, lod_2, lod_3, lod_4, lod_5, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param lod_1: The 1st LOD (Lift Off distance)
        :type lod_1: ``int`` or ``HexList``
        :param lod_2: The 2nd LOD
        :type lod_2: ``int`` or ``HexList``
        :param lod_3: The 3rd LOD
        :type lod_3: ``int`` or ``HexList``
        :param lod_4: The 4th LOD
        :type lod_4: ``int`` or ``HexList``
        :param lod_5: The 5th LOD
        :type lod_5: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.lod_1 = lod_1
        self.lod_2 = lod_2
        self.lod_3 = lod_3
        self.lod_4 = lod_4
        self.lod_5 = lod_5
    # end def __init__
# end class GetSensorLodListResponse


class GetSensorDpiParameters(SensorDataFormat):
    """
    Define ``GetSensorDpiParameters`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, sensor_idx, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetSensorDpiParametersResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.sensor_idx = sensor_idx
    # end def __init__
# end class GetSensorDpiParameters


class GetSensorDpiParametersResponse(ExtendedAdjustableDpi):
    """
    Define ``GetSensorDpiParametersResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    dpi x                         16
    default dpi x                 16
    dpi y                         16
    default dpi y                 16
    lod                           8
    reserved                      48
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorDpiParameters,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DPI_X = SENSOR_IDX - 1
        DEFAULT_DPI_X = DPI_X - 1
        DPI_Y = DEFAULT_DPI_X - 1
        DEFAULT_DPI_Y = DPI_Y - 1
        LOD = DEFAULT_DPI_Y - 1
        RESERVED = LOD - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DPI_X = 0x10
        DEFAULT_DPI_X = 0x10
        DPI_Y = 0x10
        DEFAULT_DPI_Y = 0x10
        LOD = 0x8
        RESERVED = 0x30
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DPI_X, length=LEN.DPI_X,
                 title="DpiX", name="dpi_x",
                 checks=(CheckHexList(LEN.DPI_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_X) - 1),)),
        BitField(fid=FID.DEFAULT_DPI_X, length=LEN.DEFAULT_DPI_X,
                 title="DefaultDpiX", name="default_dpi_x",
                 checks=(CheckHexList(LEN.DEFAULT_DPI_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEFAULT_DPI_X) - 1),)),
        BitField(fid=FID.DPI_Y, length=LEN.DPI_Y,
                 title="DpiY", name="dpi_y",
                 checks=(CheckHexList(LEN.DPI_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DPI_Y) - 1),)),
        BitField(fid=FID.DEFAULT_DPI_Y, length=LEN.DEFAULT_DPI_Y,
                 title="DefaultDpiY", name="default_dpi_y",
                 checks=(CheckHexList(LEN.DEFAULT_DPI_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEFAULT_DPI_Y) - 1),)),
        BitField(fid=FID.LOD, length=LEN.LOD,
                 title="Lod", name="lod",
                 checks=(CheckHexList(LEN.LOD // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi_x, default_dpi_x, dpi_y, default_dpi_y, lod,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi_x: The current DPI X direction numeric value (1 - 57343)
        :type dpi_x: ``int`` or ``HexList``
        :param default_dpi_x: The default DPI X direction numeric value
        :type default_dpi_x: ``int`` or ``HexList``
        :param dpi_y: The current DPI Y direction numeric value (1 - 57343)
        :type dpi_y: ``int`` or ``HexList``
        :param default_dpi_y: The default DPI Y direction numeric value
        :type default_dpi_y: ``int`` or ``HexList``
        :param lod: The current LOD
        :type lod: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.dpi_x = dpi_x
        self.default_dpi_x = default_dpi_x
        self.dpi_y = dpi_y
        self.default_dpi_y = default_dpi_y
        self.lod = lod
    # end def __init__
# end class GetSensorDpiParametersResponse


class SetSensorDpiParameters(SensorDpiDataFormat):
    """
    Define ``SetSensorDpiParameters`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    dpi x                         16
    dpi y                         16
    lod                           8
    padding                       80
    ============================  ==========
    """

    class FID(SensorDpiDataFormat.FID):
        # See ``SetSensorDpiDataFormat.FID``
        PADDING = SensorDpiDataFormat.FID.LOD - 1
    # end class FID

    class LEN(SensorDpiDataFormat.LEN):
        # See ``SetSensorDpiDataFormat.LEN``
        PADDING = 0x50
    # end class LEN

    FIELDS = SensorDpiDataFormat.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi_x, dpi_y, lod, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi_x: The new DPI X direction numeric value (1 - 57343) for the current slot
        :type dpi_x: ``int`` or ``HexList``
        :param dpi_y: The new DPI Y direction numeric value (1 - 57343) for the current slot
        :type dpi_y: ``int`` or ``HexList``
        :param lod: The new LOD for the current slot
        :type lod: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetSensorDpiParametersResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.dpi_x = dpi_x
        self.dpi_y = dpi_y
        self.lod = lod
    # end def __init__
# end class SetSensorDpiParameters


class SetSensorDpiParametersResponse(SensorDpiDataFormat):
    """
    Define ``SetSensorDpiParametersResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    dpi x                         16
    dpi y                         16
    lod                           8
    reserved                      80
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetSensorDpiParameters,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

    class FID(SensorDpiDataFormat.FID):
        # See ``SetSensorDpiDataFormat.FID``
        RESERVED = SensorDpiDataFormat.FID.LOD - 1
    # end class FID

    class LEN(SensorDpiDataFormat.LEN):
        # See ``SetSensorDpiDataFormat.LEN``
        RESERVED = 0x50
    # end class LEN

    FIELDS = SensorDpiDataFormat.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi_x, dpi_y, lod, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi_x: The new DPI X direction numeric value (1 - 57343) for the current slot
        :type dpi_x: ``int`` or ``HexList``
        :param dpi_y: The new DPI Y direction numeric value (1 - 57343) for the current slot
        :type dpi_y: ``int`` or ``HexList``
        :param lod: The new LOD for the current slot
        :type lod: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.dpi_x = dpi_x
        self.dpi_y = dpi_y
        self.lod = lod
    # end def __init__
# end class SetSensorDpiParametersResponse


class ShowSensorDpiStatus(ShowSensorDPIStatusDataFormat):
    """
    Define ``ShowSensorDpiStatus`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    dpi level                     8
    led hold type                 8
    button num                    8
    padding                       96
    ============================  ==========
    """

    class FID(ShowSensorDPIStatusDataFormat.FID):
        # See ``ShowSensorDPIStatusDataFormat.FID``
        PADDING = ShowSensorDPIStatusDataFormat.FID.BUTTON_NUM - 1
    # end class FID

    class LEN(ShowSensorDPIStatusDataFormat.LEN):
        # See ``ShowSensorDPIStatusDataFormat.LEN``
        PADDING = 0x60
    # end class LEN

    FIELDS = ShowSensorDPIStatusDataFormat.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi_level, led_hold_type, button_num, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi_level: The dpi level to be shown [1..N]. The N is determined by NumDpiLevels
                          from getSensorCapabilities
        :type dpi_level: ``int`` or ``HexList``
        :param led_hold_type: This parameter indicates the LED hold type.
        :type led_hold_type: ``int`` or ``HexList``
        :param button_num: The HID button number which initiates the DPI level change
        :type button_num: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ShowSensorDpiStatusResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.dpi_level = dpi_level
        self.led_hold_type = led_hold_type
        self.button_num = button_num
    # end def __init__
# end class ShowSensorDpiStatus


class ShowSensorDpiStatusResponse(ShowSensorDPIStatusDataFormat):
    """
    Define ``ShowSensorDpiStatusResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    dpi level                     8
    led hold type                 8
    button num                    8
    reserved                      96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ShowSensorDpiStatus,)
    VERSION = (0,)
    FUNCTION_INDEX = 7

    class FID(ShowSensorDPIStatusDataFormat.FID):
        # See ``ShowSensorDPIStatusDataFormat.FID``
        RESERVED = ShowSensorDPIStatusDataFormat.FID.BUTTON_NUM - 1
    # end class FID

    class LEN(ShowSensorDPIStatusDataFormat.LEN):
        # See ``ShowSensorDPIStatusDataFormat.LEN``
        RESERVED = 0x60
    # end class LEN

    FIELDS = ShowSensorDPIStatusDataFormat.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi_level, led_hold_type, button_num, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi_level: The dpi level to be shown [1..N]. The N is determined by NumDpiLevels from
                          getSensorCapabilities
        :type dpi_level: ``int`` or ``HexList``
        :param led_hold_type: This parameter indicates the LED hold type.
        :type led_hold_type: ``int`` or ``HexList``
        :param button_num: The HID button number which initiates the DPI level change
        :type button_num: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.dpi_level = dpi_level
        self.led_hold_type = led_hold_type
        self.button_num = button_num
    # end def __init__
# end class ShowSensorDpiStatusResponse


class GetDpiCalibrationInfo(SensorDataFormat):
    """
    Define ``GetDpiCalibrationInfo`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, sensor_idx, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetDpiCalibrationInfoResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.sensor_idx = sensor_idx
    # end def __init__
# end class GetDpiCalibrationInfo


class GetDpiCalibrationInfoResponse(ExtendedAdjustableDpi):
    """
    Define ``GetDpiCalibrationInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    mouse width                   8
    mouse length                  16
    calib dpi x                   16
    calib dpi y                   16
    reserved                      64
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDpiCalibrationInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 8

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        MOUSE_WIDTH = SENSOR_IDX - 1
        MOUSE_LENGTH = MOUSE_WIDTH - 1
        CALIB_DPI_X = MOUSE_LENGTH - 1
        CALIB_DPI_Y = CALIB_DPI_X - 1
        RESERVED = CALIB_DPI_Y - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        MOUSE_WIDTH = 0x8
        MOUSE_LENGTH = 0x10
        CALIB_DPI_X = 0x10
        CALIB_DPI_Y = 0x10
        RESERVED = 0x40
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.MOUSE_WIDTH, length=LEN.MOUSE_WIDTH,
                 title="MouseWidth", name="mouse_width",
                 checks=(CheckHexList(LEN.MOUSE_WIDTH // 8),
                         CheckByte(),)),
        BitField(fid=FID.MOUSE_LENGTH, length=LEN.MOUSE_LENGTH,
                 title="MouseLength", name="mouse_length",
                 checks=(CheckHexList(LEN.MOUSE_LENGTH // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MOUSE_LENGTH) - 1),)),
        BitField(fid=FID.CALIB_DPI_X, length=LEN.CALIB_DPI_X,
                 title="CalibDpiX", name="calib_dpi_x",
                 checks=(CheckHexList(LEN.CALIB_DPI_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CALIB_DPI_X) - 1),)),
        BitField(fid=FID.CALIB_DPI_Y, length=LEN.CALIB_DPI_Y,
                 title="CalibDpiY", name="calib_dpi_y",
                 checks=(CheckHexList(LEN.CALIB_DPI_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CALIB_DPI_Y) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, mouse_width, mouse_length, calib_dpi_x, calib_dpi_y,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param mouse_width: Mouse width (unit: mm, the value is device dependent)
        :type mouse_width: ``int`` or ``HexList``
        :param mouse_length: Mouse length (unit: mm, the value is device dependent)
        :type mouse_length: ``int`` or ``HexList``
        :param calib_dpi_x: DPI X configured in the sensor for the calibration (1 - 57343)
        :type calib_dpi_x: ``int`` or ``HexList``
        :param calib_dpi_y: DPI Y configured in the sensor for the calibration (1 - 57343)
        :type calib_dpi_y: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.mouse_width = mouse_width
        self.mouse_length = mouse_length
        self.calib_dpi_x = calib_dpi_x
        self.calib_dpi_y = calib_dpi_y
    # end def __init__
# end class GetDpiCalibrationInfoResponse


class StartDpiCalibration(StartDpiCalibrationDataFormat):
    """
    Define ``StartDpiCalibration`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    expected count                16
    calib type                    8
    calib start timeout           8
    calib HW process timeout      8
    calib SW process timeout      8
    padding                       64
    ============================  ==========
    """

    class FID(StartDpiCalibrationDataFormat.FID):
        # See ``StartDpiCalibrationDataFormat.FID``
        PADDING = StartDpiCalibrationDataFormat.FID.CALIB_SW_PROCESS_TIMEOUT - 1
    # end class FID

    class LEN(StartDpiCalibrationDataFormat.LEN):
        # See ``StartDpiCalibrationDataFormat.LEN``
        PADDING = 0x40
    # end class LEN

    FIELDS = StartDpiCalibrationDataFormat.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, expected_count, calib_type,
                 calib_start_timeout, calib_hw_process_timeout, calib_sw_process_timeout, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param expected_count: The expected pixel counts for mouse movement
        :type expected_count: ``int`` or ``HexList``
        :param calib_type: 0: HW, 1: SW
        :type calib_type: ``int`` or ``HexList``
        :param calib_start_timeout: Timeout (unit: second) used for HW calibration process. This timeout is
                                    limited to 60 sec.
        :type calib_start_timeout: ``int`` or ``HexList``
        :param calib_hw_process_timeout: Timeout (unit: second) used for HW calibration process. This timeout is
                                         limited to 60 sec.
        :type calib_hw_process_timeout: ``int`` or ``HexList``
        :param calib_sw_process_timeout: Timeout (unit: second) used for SW calibration process. This timeout is
                                         limited to 60 sec.
        :type calib_sw_process_timeout: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=StartDpiCalibrationResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
        self.expected_count = expected_count
        self.calib_type = calib_type
        self.calib_start_timeout = calib_start_timeout
        self.calib_hw_process_timeout = calib_hw_process_timeout
        self.calib_sw_process_timeout = calib_sw_process_timeout
    # end def __init__
# end class StartDpiCalibration


class StartDpiCalibrationResponse(StartDpiCalibrationDataFormat):
    """
    Define ``StartDpiCalibrationResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    expected count                16
    calib type                    8
    calib start timeout           8
    calib HW process timeout      8
    calib SW process timeout      8
    reserved                      64
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartDpiCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 9

    class FID(StartDpiCalibrationDataFormat.FID):
        # See ``StartDpiCalibrationDataFormat.FID``
        RESERVED = StartDpiCalibrationDataFormat.FID.CALIB_SW_PROCESS_TIMEOUT - 1
    # end class FID

    class LEN(StartDpiCalibrationDataFormat.LEN):
        # See ``StartDpiCalibrationDataFormat.LEN``
        RESERVED = 0x40
    # end class LEN

    FIELDS = StartDpiCalibrationDataFormat.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, expected_count, calib_type,
                 calib_start_timeout, calib_hw_process_timeout, calib_sw_process_timeout, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param expected_count: The expected pixel counts for mouse movement
        :type expected_count: ``int`` or ``HexList``
        :param calib_type: 0: HW, 1: SW
        :type calib_type: ``int`` or ``HexList``
        :param calib_start_timeout: Timeout (unit: second) used for HW calibration process. This timeout is
                                    limited to 60 sec.
        :type calib_start_timeout: ``int`` or ``HexList``
        :param calib_hw_process_timeout: Timeout (unit: second) used for HW calibration process. This timeout is
                                         limited to 60 sec.
        :type calib_hw_process_timeout: ``int`` or ``HexList``
        :param calib_sw_process_timeout: Timeout (unit: second) used for SW calibration process. This timeout is
                                         limited to 60 sec.
        :type calib_sw_process_timeout: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
        self.expected_count = expected_count
        self.calib_type = calib_type
        self.calib_start_timeout = calib_start_timeout
        self.calib_hw_process_timeout = calib_hw_process_timeout
        self.calib_sw_process_timeout = calib_sw_process_timeout
    # end def __init__
# end class StartDpiCalibrationResponse


class SetDpiCalibration(SetDpiCalibrationDataFormat):
    """
    Define ``SetDpiCalibration`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    calib cor                     16
    padding                       96
    ============================  ==========
    """

    class FID(SetDpiCalibrationDataFormat.FID):
        # See ``SetDpiCalibrationDataFormat.FID``
        PADDING = SetDpiCalibrationDataFormat.FID.CALIB_COR - 1
    # end class FID

    class LEN(SetDpiCalibrationDataFormat.LEN):
        # See ``SetDpiCalibrationDataFormat.LEN``
        PADDING = 0x60
    # end class LEN

    FIELDS = SetDpiCalibrationDataFormat.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, calib_cor, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param calib_cor: The correction value, given by a previous dpiCalibrationCompletedEvent or computed by SW.
        :type calib_cor: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetDpiCalibrationResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
        self.calib_cor = calib_cor
    # end def __init__
# end class SetDpiCalibration


class SetDpiCalibrationResponse(SetDpiCalibrationDataFormat):
    """
    Define ``SetDpiCalibrationResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    calib cor                     16
    reserved                      96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDpiCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 10

    class FID(SetDpiCalibrationDataFormat.FID):
        # See ``SetDpiCalibrationDataFormat.FID``
        RESERVED = SetDpiCalibrationDataFormat.FID.CALIB_COR - 1
    # end class FID

    class LEN(SetDpiCalibrationDataFormat.LEN):
        # See ``SetDpiCalibrationDataFormat.LEN``
        RESERVED = 0x60
    # end class LEN

    FIELDS = SetDpiCalibrationDataFormat.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, calib_cor, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param calib_cor: The correction value, given by a previous dpiCalibrationCompletedEvent or computed by SW.
        :type calib_cor: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
        self.calib_cor = calib_cor
    # end def __init__
# end class SetDpiCalibrationResponse


class SensorDpiParametersEvent(SensorDpiDataFormat):
    """
    Define ``SensorDpiParametersEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    dpi x                         16
    dpi y                         16
    lod                           8
    reserved                      80
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(SensorDpiDataFormat.FID):
        # See ``SetSensorDpiDataFormat.FID``
        RESERVED = SensorDpiDataFormat.FID.LOD - 1
    # end class FID

    class LEN(SensorDpiDataFormat.LEN):
        # See ``SetSensorDpiDataFormat.LEN``
        RESERVED = 0x50
    # end class LEN

    FIELDS = SensorDpiDataFormat.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi_x, dpi_y, lod, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi_x: The new DPI X direction numeric value (1 - 57343) for the current slot
        :type dpi_x: ``int`` or ``HexList``
        :param dpi_y: The new DPI Y direction numeric value (1 - 57343) for the current slot
        :type dpi_y: ``int`` or ``HexList``
        :param lod: The new LOD for the current slot
        :type lod: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.dpi_x = dpi_x
        self.dpi_y = dpi_y
        self.lod = lod
    # end def __init__
# end class SensorDpiParametersEvent


class DpiCalibrationCompletedEvent(ExtendedAdjustableDpi):
    """
    Define ``DpiCalibrationCompletedEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    sensor idx                    8
    direction                     8
    calib cor                     16
    calib delta                   16
    reserved                      80
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(ExtendedAdjustableDpi.FID):
        # See ``ExtendedAdjustableDpi.FID``
        SENSOR_IDX = ExtendedAdjustableDpi.FID.SOFTWARE_ID - 1
        DIRECTION = SENSOR_IDX - 1
        CALIB_COR = DIRECTION - 1
        CALIB_DELTA = CALIB_COR - 1
        RESERVED = CALIB_DELTA - 1
    # end class FID

    class LEN(ExtendedAdjustableDpi.LEN):
        # See ``ExtendedAdjustableDpi.LEN``
        SENSOR_IDX = 0x8
        DIRECTION = 0x8
        CALIB_COR = 0x10
        CALIB_DELTA = 0x10
        RESERVED = 0x50
    # end class LEN

    FIELDS = ExtendedAdjustableDpi.FIELDS + (
        BitField(fid=FID.SENSOR_IDX, length=LEN.SENSOR_IDX,
                 title="SensorIdx", name="sensor_idx",
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DIRECTION, length=LEN.DIRECTION,
                 title="Direction", name="direction",
                 checks=(CheckHexList(LEN.DIRECTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.CALIB_COR, length=LEN.CALIB_COR,
                 title="CalibCor", name="calib_cor",
                 checks=(CheckHexList(LEN.CALIB_COR // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CALIB_COR) - 1),)),
        BitField(fid=FID.CALIB_DELTA, length=LEN.CALIB_DELTA,
                 title="CalibDelta", name="calib_delta",
                 checks=(CheckHexList(LEN.CALIB_DELTA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CALIB_DELTA) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ExtendedAdjustableDpi.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, sensor_idx, direction, calib_cor, calib_delta, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The index of the sensor
        :type sensor_idx: ``int`` or ``HexList``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``int`` or ``HexList``
        :param calib_cor: The DPI calibration correction value of the configured direction in startDpiCalibration
        :type calib_cor: ``int`` or ``HexList``
        :param calib_delta: The displacement (unit: pixel counts) of perpendicular direction configured in
                            startDpiCalibration
        :type calib_delta: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_idx = sensor_idx
        self.direction = direction
        self.calib_cor = calib_cor
        self.calib_delta = calib_delta
    # end def __init__
# end class DpiCalibrationCompletedEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
