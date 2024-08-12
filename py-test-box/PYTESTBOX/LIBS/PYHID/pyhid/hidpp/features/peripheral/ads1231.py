#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.peripheral.ads1231
:brief: HID++ 2.0 ``Ads1231`` command interface definition
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/07/26
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
class Ads1231(HidppMessage):
    """
    This feature allows to configure/calibrate the ADC and strain gauge.
    """

    FEATURE_ID = 0x9215
    MAX_FUNCTION_INDEX = 8

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class Ads1231


class Ads1231Model(FeatureModel):
    """
    Define ``Ads1231`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """

        # Function index
        RESET_SENSOR = 0
        SHUTDOWN_SENSOR = 1
        SET_MONITOR_MODE = 2
        CALIBRATE = 3
        READ_CALIBRATION = 4
        WRITE_CALIBRATION = 5
        READ_OTHER_NVS_DATA = 6
        WRITE_OTHER_NVS_DATA = 7
        MANAGE_DYNAMIC_CALIBRATION_PARAMETERS = 8

        # Event index
        MONITOR_REPORT = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``Ads1231`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.RESET_SENSOR: {
                    "request": ResetSensor,
                    "response": ResetSensorResponse
                },
                cls.INDEX.SHUTDOWN_SENSOR: {
                    "request": ShutdownSensor,
                    "response": ShutdownSensorResponse
                },
                cls.INDEX.SET_MONITOR_MODE: {
                    "request": SetMonitorMode,
                    "response": SetMonitorModeResponse
                },
                cls.INDEX.CALIBRATE: {
                    "request": Calibrate,
                    "response": CalibrateResponse
                },
                cls.INDEX.READ_CALIBRATION: {
                    "request": ReadCalibration,
                    "response": ReadCalibrationResponse
                },
                cls.INDEX.WRITE_CALIBRATION: {
                    "request": WriteCalibration,
                    "response": WriteCalibrationResponse
                },
                cls.INDEX.READ_OTHER_NVS_DATA: {
                    "request": ReadOtherNvsData,
                    "response": ReadOtherNvsDataResponse
                },
                cls.INDEX.WRITE_OTHER_NVS_DATA: {
                    "request": WriteOtherNvsData,
                    "response": WriteOtherNvsDataResponse
                },
                cls.INDEX.MANAGE_DYNAMIC_CALIBRATION_PARAMETERS: {
                    "request": ManageDynamicCalibrationParameters,
                    "response": ManageDynamicCalibrationParametersResponse
                }
            },
            "events": {
                cls.INDEX.MONITOR_REPORT: {"report": MonitorReportEvent}
            }
        }

        return {
            "feature_base": Ads1231,
            "versions": {
                Ads1231V0.VERSION: {
                    "main_cls": Ads1231V0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class Ads1231Model


# noinspection DuplicatedCode
class Ads1231Factory(FeatureFactory):
    """
    Get ``Ads1231`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``Ads1231`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``Ads1231Interface``
        """
        return Ads1231Model.get_main_cls(version)()
    # end def create
# end class Ads1231Factory


class Ads1231Interface(FeatureInterface, ABC):
    """
    Define required interfaces for ``Ads1231`` classes
    """

    def __init__(self):
        # Requests
        self.reset_sensor_cls = None
        self.shutdown_sensor_cls = None
        self.set_monitor_mode_cls = None
        self.calibrate_cls = None
        self.read_calibration_cls = None
        self.write_calibration_cls = None
        self.read_other_nvs_data_cls = None
        self.write_other_nvs_data_cls = None
        self.manage_dynamic_calibration_parameters_cls = None

        # Responses
        self.reset_sensor_response_cls = None
        self.shutdown_sensor_response_cls = None
        self.set_monitor_mode_response_cls = None
        self.calibrate_response_cls = None
        self.read_calibration_response_cls = None
        self.write_calibration_response_cls = None
        self.read_other_nvs_data_response_cls = None
        self.write_other_nvs_data_response_cls = None
        self.manage_dynamic_calibration_parameters_response_cls = None

        # Events
        self.monitor_report_event_cls = None
    # end def __init__
# end class Ads1231Interface


class Ads1231V0(Ads1231Interface):
    """
    Define ``Ads1231V0`` feature

    This feature provides model and unit specific information for version 0

    [0] resetSensor() -> None

    [1] shutdownSensor() -> None

    [2] setMonitorMode(count, threshold) -> None

    [3] calibrate(refPointIndex, refPointOutValue) -> None

    [4] readCalibration(refPointIndex) -> refPointIndex, refPointOutValue, refPointCalValue

    [5] writeCalibration(refPointIndex, refPointOutValue, refPointCalValue) -> refPointIndex, refPointOutValue,
    refPointCalValue

    [6] readOtherNvsData(dataFieldId) -> dataFieldId, data

    [7] writeOtherNvsData(dataFieldId, data) -> dataFieldId, data

    [8] manageDynamicCalibrationParameters(command, offsetExtension, offsetAdjustmentCount, dynamicThreshold) ->
    command, offsetExtension, offsetAdjustmentCount, dynamicThreshold

    [Event 0] monitorReportEvent -> outDataSample, offsetCalibration, counter
    """

    VERSION = 0

    def __init__(self):
        # See ``Ads1231.__init__``
        super().__init__()
        index = Ads1231Model.INDEX

        # Requests
        self.reset_sensor_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.RESET_SENSOR)
        self.shutdown_sensor_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.SHUTDOWN_SENSOR)
        self.set_monitor_mode_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.SET_MONITOR_MODE)
        self.calibrate_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.CALIBRATE)
        self.read_calibration_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.READ_CALIBRATION)
        self.write_calibration_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.WRITE_CALIBRATION)
        self.read_other_nvs_data_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.READ_OTHER_NVS_DATA)
        self.write_other_nvs_data_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.WRITE_OTHER_NVS_DATA)
        self.manage_dynamic_calibration_parameters_cls = Ads1231Model.get_request_cls(
            self.VERSION, index.MANAGE_DYNAMIC_CALIBRATION_PARAMETERS)

        # Responses
        self.reset_sensor_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.RESET_SENSOR)
        self.shutdown_sensor_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.SHUTDOWN_SENSOR)
        self.set_monitor_mode_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.SET_MONITOR_MODE)
        self.calibrate_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.CALIBRATE)
        self.read_calibration_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.READ_CALIBRATION)
        self.write_calibration_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.WRITE_CALIBRATION)
        self.read_other_nvs_data_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.READ_OTHER_NVS_DATA)
        self.write_other_nvs_data_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.WRITE_OTHER_NVS_DATA)
        self.manage_dynamic_calibration_parameters_response_cls = Ads1231Model.get_response_cls(
            self.VERSION, index.MANAGE_DYNAMIC_CALIBRATION_PARAMETERS)

        # Events
        self.monitor_report_event_cls = Ads1231Model.get_report_cls(
            self.VERSION, index.MONITOR_REPORT)
    # end def __init__

    def get_max_function_index(self):
        # See ``Ads1231Interface.get_max_function_index``
        return Ads1231Model.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class Ads1231V0


class ShortEmptyPacketDataFormat(Ads1231):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - ResetSensor
        - ShutdownSensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        PADDING = Ads1231.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        PADDING = 0x18
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Ads1231.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(Ads1231):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - ResetSensorResponse
        - ShutdownSensorResponse
        - SetMonitorModeResponse
        - CalibrateResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        PADDING = Ads1231.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        PADDING = 0x80
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Ads1231.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class MixedContainer1(Ads1231):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - ReadCalibrationResponse
        - WriteCalibration
        - WriteCalibrationResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RefPointIndex                 8
    RefPointOutValue              8
    RefPointCalValue              24
    Padding                       88
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        REF_POINT_INDEX = Ads1231.FID.SOFTWARE_ID - 1
        REF_POINT_OUT_VALUE = REF_POINT_INDEX - 1
        REF_POINT_CAL_VALUE = REF_POINT_OUT_VALUE - 1
        PADDING = REF_POINT_CAL_VALUE - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        REF_POINT_INDEX = 0x8
        REF_POINT_OUT_VALUE = 0x8
        REF_POINT_CAL_VALUE = 0x18
        PADDING = 0x58
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.REF_POINT_INDEX, length=LEN.REF_POINT_INDEX,
                 title="RefPointIndex", name="ref_point_index",
                 checks=(CheckHexList(LEN.REF_POINT_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.REF_POINT_OUT_VALUE, length=LEN.REF_POINT_OUT_VALUE,
                 title="RefPointOutValue", name="ref_point_out_value",
                 checks=(CheckHexList(LEN.REF_POINT_OUT_VALUE // 8),
                         CheckByte(),)),
        BitField(fid=FID.REF_POINT_CAL_VALUE, length=LEN.REF_POINT_CAL_VALUE,
                 title="RefPointCalValue", name="ref_point_cal_value",
                 checks=(CheckHexList(LEN.REF_POINT_CAL_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REF_POINT_CAL_VALUE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Ads1231.DEFAULT.PADDING),
    )
# end class MixedContainer1


class MixedContainer2(Ads1231):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - ReadOtherNvsDataResponse
        - WriteOtherNvsData
        - WriteOtherNvsDataResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    DataFieldId                   8
    Data                          120
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        DATA_FIELD_ID = Ads1231.FID.SOFTWARE_ID - 1
        DATA = DATA_FIELD_ID - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        DATA_FIELD_ID = 0x8
        DATA = 0x78
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.DATA_FIELD_ID, length=LEN.DATA_FIELD_ID,
                 title="DataFieldId", name="data_field_id",
                 checks=(CheckHexList(LEN.DATA_FIELD_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="Data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
    )
# end class MixedContainer2


class MixedContainer3(Ads1231):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - ManageDynamicCalibrationParameters
        - ManageDynamicCalibrationParametersResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Command                       8
    OffsetExtension               8
    OffsetAdjustmentCount         16
    DynamicThreshold              8
    Padding                       88
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        COMMAND = Ads1231.FID.SOFTWARE_ID - 1
        OFFSET_EXTENSION = COMMAND - 1
        OFFSET_ADJUSTMENT_COUNT = OFFSET_EXTENSION - 1
        DYNAMIC_THRESHOLD = OFFSET_ADJUSTMENT_COUNT - 1
        PADDING = DYNAMIC_THRESHOLD - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        COMMAND = 0x8
        OFFSET_EXTENSION = 0x8
        OFFSET_ADJUSTMENT_COUNT = 0x10
        DYNAMIC_THRESHOLD = 0x8
        PADDING = 0x58
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.COMMAND, length=LEN.COMMAND,
                 title="Command", name="command",
                 checks=(CheckHexList(LEN.COMMAND // 8),
                         CheckByte(),)),
        BitField(fid=FID.OFFSET_EXTENSION, length=LEN.OFFSET_EXTENSION,
                 title="OffsetExtension", name="offset_extension",
                 checks=(CheckHexList(LEN.OFFSET_EXTENSION // 8),
                         CheckByte(),)),
        BitField(fid=FID.OFFSET_ADJUSTMENT_COUNT, length=LEN.OFFSET_ADJUSTMENT_COUNT,
                 title="OffsetAdjustmentCount", name="offset_adjustment_count",
                 checks=(CheckHexList(LEN.OFFSET_ADJUSTMENT_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OFFSET_ADJUSTMENT_COUNT) - 1),)),
        BitField(fid=FID.DYNAMIC_THRESHOLD, length=LEN.DYNAMIC_THRESHOLD,
                 title="DynamicThreshold", name="dynamic_threshold",
                 checks=(CheckHexList(LEN.DYNAMIC_THRESHOLD // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Ads1231.DEFAULT.PADDING),
    )
# end class MixedContainer3


class ResetSensor(ShortEmptyPacketDataFormat):
    """
    Define ``ResetSensor`` implementation class for version 0
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
                         functionIndex=ResetSensorResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ResetSensor


class ResetSensorResponse(LongEmptyPacketDataFormat):
    """
    Define ``ResetSensorResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ResetSensor,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ResetSensorResponse


class ShutdownSensor(ShortEmptyPacketDataFormat):
    """
    Define ``ShutdownSensor`` implementation class for version 0
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
                         functionIndex=ShutdownSensorResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ShutdownSensor


class ShutdownSensorResponse(LongEmptyPacketDataFormat):
    """
    Define ``ShutdownSensorResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ShutdownSensor,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ShutdownSensorResponse


# noinspection DuplicatedCode
class SetMonitorMode(Ads1231):
    """
    Define ``SetMonitorMode`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Count                         16
    Threshold                     8
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        COUNT = Ads1231.FID.SOFTWARE_ID - 1
        THRESHOLD = COUNT - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        COUNT = 0x10
        THRESHOLD = 0x8
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNT) - 1),)),
        BitField(fid=FID.THRESHOLD, length=LEN.THRESHOLD,
                 title="Threshold", name="threshold",
                 checks=(CheckHexList(LEN.THRESHOLD // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, count, threshold, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param count: The total number of events requested
        :type count: ``int`` or ``HexList``
        :param threshold: The minimum, absolute, variation on X or Y field values so that a new report be generated
        :type threshold: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetMonitorModeResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.count = count
        self.threshold = threshold
    # end def __init__
# end class SetMonitorMode


class SetMonitorModeResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetMonitorModeResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetMonitorMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetMonitorModeResponse


class Calibrate(Ads1231):
    """
    Define ``Calibrate`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RefPointIndex                 8
    RefPointOutValue              8
    Padding                       8
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        REF_POINT_INDEX = Ads1231.FID.SOFTWARE_ID - 1
        REF_POINT_OUT_VALUE = REF_POINT_INDEX - 1
        PADDING = REF_POINT_OUT_VALUE - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        REF_POINT_INDEX = 0x8
        REF_POINT_OUT_VALUE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.REF_POINT_INDEX, length=LEN.REF_POINT_INDEX,
                 title="RefPointIndex", name="ref_point_index",
                 checks=(CheckHexList(LEN.REF_POINT_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.REF_POINT_OUT_VALUE, length=LEN.REF_POINT_OUT_VALUE,
                 title="RefPointOutValue", name="ref_point_out_value",
                 checks=(CheckHexList(LEN.REF_POINT_OUT_VALUE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Ads1231.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ref_point_index, ref_point_out_value, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ref_point_index: Index of the point in the sensor output curve that we want to measure and store
        :type ref_point_index: ``int`` or ``HexList``
        :param ref_point_out_value: Expected output value at reference point, expressed as the % of the max output value
        :type ref_point_out_value: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=CalibrateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.ref_point_index = ref_point_index
        self.ref_point_out_value = ref_point_out_value
    # end def __init__
# end class Calibrate


class CalibrateResponse(LongEmptyPacketDataFormat):
    """
    Define ``CalibrateResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (Calibrate,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class CalibrateResponse


class ReadCalibration(Ads1231):
    """
    Define ``ReadCalibration`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RefPointIndex                 8
    Padding                       16
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        REF_POINT_INDEX = Ads1231.FID.SOFTWARE_ID - 1
        PADDING = REF_POINT_INDEX - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        REF_POINT_INDEX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.REF_POINT_INDEX, length=LEN.REF_POINT_INDEX,
                 title="RefPointIndex", name="ref_point_index",
                 checks=(CheckHexList(LEN.REF_POINT_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Ads1231.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ref_point_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ref_point_index: Index of the point in the sensor output curve that we want to measure and store
        :type ref_point_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ReadCalibrationResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.ref_point_index = ref_point_index
    # end def __init__
# end class ReadCalibration


class ReadCalibrationResponse(MixedContainer1):
    """
    Define ``ReadCalibrationResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, ref_point_index, ref_point_out_value, ref_point_cal_value,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ref_point_index: Index of the point in the sensor output curve that we want to measure and store
        :type ref_point_index: ``int`` or ``HexList``
        :param ref_point_out_value: Expected output value at reference point, expressed as the % of the max output value
        :type ref_point_out_value: ``int`` or ``HexList``
        :param ref_point_cal_value: Calibration value for the reference point
        :type ref_point_cal_value: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.ref_point_index = ref_point_index
        self.ref_point_out_value = ref_point_out_value
        self.ref_point_cal_value = ref_point_cal_value
    # end def __init__
# end class ReadCalibrationResponse


class WriteCalibration(MixedContainer1):
    """
    Define ``WriteCalibration`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, ref_point_index, ref_point_out_value, ref_point_cal_value,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ref_point_index: Index of the point in the sensor output curve that we want to measure and store
        :type ref_point_index: ``int`` or ``HexList``
        :param ref_point_out_value: Expected output value at reference point, expressed as the % of the max output value
        :type ref_point_out_value: ``int`` or ``HexList``
        :param ref_point_cal_value: Calibration value for the reference point
        :type ref_point_cal_value: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=WriteCalibrationResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.ref_point_index = ref_point_index
        self.ref_point_out_value = ref_point_out_value
        self.ref_point_cal_value = ref_point_cal_value
    # end def __init__
# end class WriteCalibration


class WriteCalibrationResponse(MixedContainer1):
    """
    Define ``WriteCalibrationResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteCalibration,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, ref_point_index, ref_point_out_value, ref_point_cal_value,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ref_point_index: Index of the point in the sensor output curve that we want to measure and store
        :type ref_point_index: ``int`` or ``HexList``
        :param ref_point_out_value: Expected output value at reference point, expressed as the % of the max output value
        :type ref_point_out_value: ``int`` or ``HexList``
        :param ref_point_cal_value: Calibration value for the reference point
        :type ref_point_cal_value: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.ref_point_index = ref_point_index
        self.ref_point_out_value = ref_point_out_value
        self.ref_point_cal_value = ref_point_cal_value
    # end def __init__
# end class WriteCalibrationResponse


class ReadOtherNvsData(Ads1231):
    """
    Define ``ReadOtherNvsData`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    DataFieldId                   8
    Padding                       16
    ============================  ==========
    """

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        DATA_FIELD_ID = Ads1231.FID.SOFTWARE_ID - 1
        PADDING = DATA_FIELD_ID - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        DATA_FIELD_ID = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.DATA_FIELD_ID, length=LEN.DATA_FIELD_ID,
                 title="DataFieldId", name="data_field_id",
                 checks=(CheckHexList(LEN.DATA_FIELD_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Ads1231.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, data_field_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param data_field_id: Index of the data field to read Values: 0 to 255
        :type data_field_id: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ReadOtherNvsDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.data_field_id = data_field_id
    # end def __init__
# end class ReadOtherNvsData


class ReadOtherNvsDataResponse(MixedContainer2):
    """
    Define ``ReadOtherNvsDataResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadOtherNvsData,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

    def __init__(self, device_index, feature_index, data_field_id, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param data_field_id: Index of the data field to read Values: 0 to 255
        :type data_field_id: ``int`` or ``HexList``
        :param data: Data
        :type data: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data_field_id = data_field_id
        self.data = data
    # end def __init__
# end class ReadOtherNvsDataResponse


class WriteOtherNvsData(MixedContainer2):
    """
    Define ``WriteOtherNvsData`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, data_field_id, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param data_field_id: Index of the data field to read Values: 0 to 255
        :type data_field_id: ``int`` or ``HexList``
        :param data: Data
        :type data: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=WriteOtherNvsDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data_field_id = data_field_id
        self.data = data
    # end def __init__
# end class WriteOtherNvsData


class WriteOtherNvsDataResponse(MixedContainer2):
    """
    Define ``WriteOtherNvsDataResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteOtherNvsData,)
    VERSION = (0,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, data_field_id, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param data_field_id: Index of the data field to read Values: 0 to 255
        :type data_field_id: ``int`` or ``HexList``
        :param data: Data
        :type data: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data_field_id = data_field_id
        self.data = data
    # end def __init__
# end class WriteOtherNvsDataResponse


class ManageDynamicCalibrationParameters(MixedContainer3):
    """
    Define ``ManageDynamicCalibrationParameters`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index,
                 command, offset_extension, offset_adjustment_count, dynamic_threshold,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param command: Command
        :type command: ``int`` or ``HexList``
        :param offset_extension: Offset Extension
        :type offset_extension: ``int`` or ``HexList``
        :param offset_adjustment_count: Offset Adjustment Count
        :type offset_adjustment_count: ``int`` or ``HexList``
        :param dynamic_threshold: Dynamic Threshold
        :type dynamic_threshold: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ManageDynamicCalibrationParametersResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.command = command
        self.offset_extension = offset_extension
        self.offset_adjustment_count = offset_adjustment_count
        self.dynamic_threshold = dynamic_threshold
    # end def __init__
# end class ManageDynamicCalibrationParameters


class ManageDynamicCalibrationParametersResponse(MixedContainer3):
    """
    Define ``ManageDynamicCalibrationParametersResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ManageDynamicCalibrationParameters,)
    VERSION = (0,)
    FUNCTION_INDEX = 8

    def __init__(self, device_index, feature_index,
                 command, offset_extension, offset_adjustment_count, dynamic_threshold,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param command: Command
        :type command: ``int`` or ``HexList``
        :param offset_extension: Offset Extension
        :type offset_extension: ``int`` or ``HexList``
        :param offset_adjustment_count: Offset Adjustment Count
        :type offset_adjustment_count: ``int`` or ``HexList``
        :param dynamic_threshold: Dynamic Threshold
        :type dynamic_threshold: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.command = command
        self.offset_extension = offset_extension
        self.offset_adjustment_count = offset_adjustment_count
        self.dynamic_threshold = dynamic_threshold
    # end def __init__
# end class ManageDynamicCalibrationParametersResponse


class MonitorReportEvent(Ads1231):
    """
    Define ``MonitorReportEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    OutDataSample                 24
    OffsetCalibration             24
    Reserved                      64
    Counter                       16
    ============================  ==========
    """

    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(Ads1231.FID):
        """
        Define field identifier(s)
        """

        OUT_DATA_SAMPLE = Ads1231.FID.SOFTWARE_ID - 1
        OFFSET_CALIBRATION = OUT_DATA_SAMPLE - 1
        RESERVED = OFFSET_CALIBRATION - 1
        COUNTER = RESERVED - 1
    # end class FID

    class LEN(Ads1231.LEN):
        """
        Define field length(s)
        """

        OUT_DATA_SAMPLE = 0x18
        OFFSET_CALIBRATION = 0x18
        RESERVED = 0x40
        COUNTER = 0x10
    # end class LEN

    FIELDS = Ads1231.FIELDS + (
        BitField(fid=FID.OUT_DATA_SAMPLE, length=LEN.OUT_DATA_SAMPLE,
                 title="OutDataSample", name="out_data_sample",
                 checks=(CheckHexList(LEN.OUT_DATA_SAMPLE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OUT_DATA_SAMPLE) - 1),)),
        BitField(fid=FID.OFFSET_CALIBRATION, length=LEN.OFFSET_CALIBRATION,
                 title="OffsetCalibration", name="offset_calibration",
                 checks=(CheckHexList(LEN.OFFSET_CALIBRATION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OFFSET_CALIBRATION) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=Ads1231.DEFAULT.PADDING),
        BitField(fid=FID.COUNTER, length=LEN.COUNTER,
                 title="Counter", name="counter",
                 checks=(CheckHexList(LEN.COUNTER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNTER) - 1),)),
    )

    def __init__(self, device_index, feature_index, out_data_sample, offset_calibration, counter, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param out_data_sample: Out Data Sample
        :type out_data_sample: ``int`` or ``HexList``
        :param offset_calibration: Offset Calibration
        :type offset_calibration: ``int`` or ``HexList``
        :param counter: Number of samples sent since command start
        :type counter: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.out_data_sample = out_data_sample
        self.offset_calibration = offset_calibration
        self.counter = counter
    # end def __init__
# end class MonitorReportEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
