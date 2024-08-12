#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.common.batterylevelscalibration

@brief  HID++ 2.0 Battery Levels Calibration command interface definition

@author Stanislas Cottard

@date   2019/07/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
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
from pylibrary.tools.docutils import DocUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class BatteryLevelsCalibration(HidppMessage):
    """
    Battery Levels Calibration implementation class

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Params                        24
    ============================  ==========
    """
    FEATURE_ID = 0x1861
    MAX_FUNCTION_INDEX_V0 = 4
    MAX_FUNCTION_INDEX_V1 = 5

    MAX_NUMBER_OF_CALIBRATION_POINTS = 7

    CUTOFF_ENABLE = 0
    CUTOFF_DISABLE = 1

    @DocUtils.copy_doc(HidppMessage.__init__)
    def __init__(self, device_index, feature_index, **kwargs):
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class BatteryLevelsCalibration


class BatteryLevelsCalibrationModel(FeatureModel):
    """
    BatteryLevelsCalibration feature model
    """
    class INDEX(object):
        """
        Functions index
        """
        GET_BATTERY_CALIBRATION_INFO = 0
        MEASURE_BATTERY = 1
        STORE_CALIBRATION = 2
        READ_CALIBRATION = 3
        CUT_OFF_CONTROL = 4
        SET_BATTERY_SOURCE_INFO = 5
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        BatteryLevelsCalibration feature data model
        """
        function_map_v0 = {
            cls.INDEX.GET_BATTERY_CALIBRATION_INFO: {
                    "request": GetBattCalibrationInfo, "response": GetBattCalibrationInfoResponse},
            cls.INDEX.MEASURE_BATTERY: {"request": MeasureBattery, "response": MeasureBatteryResponse},
            cls.INDEX.STORE_CALIBRATION: {
                "request": StoreCalibration, "response": StoreCalibrationResponse},
            cls.INDEX.READ_CALIBRATION: {
                "request": ReadCalibration, "response": ReadCalibrationResponse},
            cls.INDEX.CUT_OFF_CONTROL: {"request": CutOffControl, "response": CutOffControlResponse},
        }

        function_map_v1 = {
            cls.INDEX.SET_BATTERY_SOURCE_INFO: {
                "request": SetBatterySourceInfo, "response": SetBatterySourceInfoResponse},
        }
        function_map_v1.update(function_map_v0)

        return {
            "feature_base": BatteryLevelsCalibration,
            "versions": {
                BatteryLevelsCalibrationV0.VERSION: {
                    "main_cls": BatteryLevelsCalibrationV0,
                    "api": {
                        "functions": function_map_v0
                    }
                },
                BatteryLevelsCalibrationV1.VERSION: {
                    "main_cls": BatteryLevelsCalibrationV1,
                    "api": {
                        "functions": function_map_v1
                    }
                },
            }
        }
    # end def _get_data_model
# end class BatteryLevelsCalibrationModel


class BatteryLevelsCalibrationFactory(FeatureFactory):
    """
    Factory which creates a BatteryLevelsCalibration object from a given version
    """
    @staticmethod
    def create(version):
        """
        BatteryLevelsCalibration object creation from version number

        :param version: BatteryLevelsCalibration feature version
        :type version: ``int``
        :return: BatteryLevelsCalibration object
        :rtype: ``BatteryLevelsCalibrationInterface``
        """
        return BatteryLevelsCalibrationModel.get_main_cls(version)()
    # end def create
# end class BatteryLevelsCalibrationFactory


class BatteryLevelsCalibrationInterface(FeatureInterface, ABC):
    """
    Interface to BatteryLevelsCalibration feature

    Defines required interfaces for BatteryLevelsCalibration classes
    """
    def __init__(self):
        """
        Constructor
        """
        # Requests
        self.get_battery_calibration_info_cls = None
        self.measure_battery_cls = None
        self.store_calibration_cls = None
        self.read_calibration_cls = None
        self.cut_off_control_cls = None
        self.set_battery_source_info_cls = None

        # Responses
        self.get_battery_calibration_info_response_cls = None
        self.measure_battery_response_cls = None
        self.store_calibration_response_cls = None
        self.read_calibration_response_cls = None
        self.cut_off_control_response_cls = None
        self.set_battery_source_info_response_cls = None
    # end def __init__
# end class BatteryLevelsCalibrationInterface


class BatteryLevelsCalibrationV0(BatteryLevelsCalibrationInterface):
    """
    BatteryLevelsCalibrationV0

    This feature provides model and unit specific information for version 0

    [0] GetBattCalibrationInfo() -> CalibrationDesc
    [1] MeasureBattery() -> MeasuredVoltage
    [2] StoreCalibration(Calibration) -> void
    [3] ReadCalibration() -> Calibration
    [4] CutOffControl(cutoffControlByte) -> cutOffEnabled
    """
    VERSION = 0

    @DocUtils.copy_doc(BatteryLevelsCalibration.__init__)
    def __init__(self):
        super().__init__()
        index = BatteryLevelsCalibrationModel.INDEX
        # Requests
        self.get_battery_calibration_info_cls = BatteryLevelsCalibrationModel.get_request_cls(
                self.VERSION, index.GET_BATTERY_CALIBRATION_INFO)
        self.measure_battery_cls = BatteryLevelsCalibrationModel.get_request_cls(self.VERSION, index.MEASURE_BATTERY)
        self.store_calibration_cls = BatteryLevelsCalibrationModel.get_request_cls(
                self.VERSION, index.STORE_CALIBRATION)
        self.read_calibration_cls = BatteryLevelsCalibrationModel.get_request_cls(self.VERSION, index.READ_CALIBRATION)
        self.cut_off_control_cls = BatteryLevelsCalibrationModel.get_request_cls(self.VERSION, index.CUT_OFF_CONTROL)

        # Responses
        self.get_battery_calibration_info_response_cls = BatteryLevelsCalibrationModel.get_response_cls(
                self.VERSION, index.GET_BATTERY_CALIBRATION_INFO)
        self.measure_battery_response_cls = BatteryLevelsCalibrationModel.get_response_cls(
                self.VERSION, index.MEASURE_BATTERY)
        self.store_calibration_response_cls = BatteryLevelsCalibrationModel.get_response_cls(
                self.VERSION, index.STORE_CALIBRATION)
        self.read_calibration_response_cls = BatteryLevelsCalibrationModel.get_response_cls(
                self.VERSION, index.READ_CALIBRATION)
        self.cut_off_control_response_cls = BatteryLevelsCalibrationModel.get_response_cls(
                self.VERSION, index.CUT_OFF_CONTROL)
    # end def __init__

    @DocUtils.copy_doc(BatteryLevelsCalibrationInterface.get_max_function_index)
    def get_max_function_index(self):
        return BatteryLevelsCalibrationModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class BatteryLevelsCalibrationV0


class BatteryLevelsCalibrationV1(BatteryLevelsCalibrationV0):
    """
    BatteryLevelsCalibrationV1

    This feature provides model and unit specific information for version 1
    Version 1: adding capability for multi-sourcing battery support through setBatterySourceInfo())

    [5] setBatterySourceInfo(battery_source_index ) -> battery_source_index
    """
    VERSION = 1

    @DocUtils.copy_doc(BatteryLevelsCalibration.__init__)
    def __init__(self):
        super().__init__()
        # Requests
        self.set_battery_source_info_cls = BatteryLevelsCalibrationModel.get_request_cls(
            self.VERSION, BatteryLevelsCalibrationModel.INDEX.SET_BATTERY_SOURCE_INFO)

        # Responses
        self.set_battery_source_info_response_cls = BatteryLevelsCalibrationModel.get_response_cls(
                self.VERSION, BatteryLevelsCalibrationModel.INDEX.SET_BATTERY_SOURCE_INFO)
    # end def __init__

    @DocUtils.copy_doc(BatteryLevelsCalibrationInterface.get_max_function_index)
    def get_max_function_index(self):
        return BatteryLevelsCalibrationModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class BatteryLevelsCalibrationV1


class BatteryCalibrationFormat(BatteryLevelsCalibration):
    """
    BatteryLevelsCalibration Battery Calibration Format class

    This class is to be used as a base class for several messages in this feature.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    CalibrationPointsNb           8
    Reserved                      8
    CalibrationPoint0             16
    CalibrationPoint1             16
    CalibrationPoint2             16
    CalibrationPoint3             16
    CalibrationPoint4             16
    CalibrationPoint5             16
    CalibrationPoint6             16
    ============================  ==========
    """

    class FID(BatteryLevelsCalibration.FID):
        """
        Field Identifiers
        """
        CALIBRATION_POINTS_NB = 0xFA
        RESERVED = 0xF9
        CALIBRATION_POINT_0 = 0xF8
        CALIBRATION_POINT_1 = 0xF7
        CALIBRATION_POINT_2 = 0xF6
        CALIBRATION_POINT_3 = 0xF5
        CALIBRATION_POINT_4 = 0xF4
        CALIBRATION_POINT_5 = 0xF3
        CALIBRATION_POINT_6 = 0xF2
    # end class FID

    class LEN(BatteryLevelsCalibration.LEN):
        """
        Field Lengths
        """
        CALIBRATION_POINTS_NB = 0x08
        RESERVED = 0x08
        CALIBRATION_POINT_0 = 0x10
        CALIBRATION_POINT_1 = 0x10
        CALIBRATION_POINT_2 = 0x10
        CALIBRATION_POINT_3 = 0x10
        CALIBRATION_POINT_4 = 0x10
        CALIBRATION_POINT_5 = 0x10
        CALIBRATION_POINT_6 = 0x10
    # end class LEN

    FIELDS = BatteryLevelsCalibration.FIELDS + (
        BitField(FID.CALIBRATION_POINTS_NB,
                 LEN.CALIBRATION_POINTS_NB,
                 title='CalibrationPointsNb',
                 name='calibration_points_nb',
                 checks=(CheckHexList(length=LEN.CALIBRATION_POINTS_NB // 8), CheckByte(),),),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(length=LEN.RESERVED // 8), CheckByte(),),),
        BitField(FID.CALIBRATION_POINT_0,
                 LEN.CALIBRATION_POINT_0,
                 title='CalibrationPoint0',
                 name='calibration_point_0',
                 checks=(CheckHexList(length=LEN.CALIBRATION_POINT_0 // 8),
                         CheckInt(max_value=(1 << LEN.CALIBRATION_POINT_0) - 1),), ),
        BitField(FID.CALIBRATION_POINT_1,
                 LEN.CALIBRATION_POINT_1,
                 title='CalibrationPoint1',
                 name='calibration_point_1',
                 checks=(CheckHexList(length=LEN.CALIBRATION_POINT_1 // 8),
                         CheckInt(max_value=(1 << LEN.CALIBRATION_POINT_1) - 1),), ),
        BitField(FID.CALIBRATION_POINT_2,
                 LEN.CALIBRATION_POINT_2,
                 title='CalibrationPoint2',
                 name='calibration_point_2',
                 checks=(CheckHexList(length=LEN.CALIBRATION_POINT_2 // 8),
                         CheckInt(max_value=(1 << LEN.CALIBRATION_POINT_2) - 1),), ),
        BitField(FID.CALIBRATION_POINT_3,
                 LEN.CALIBRATION_POINT_3,
                 title='CalibrationPoint3',
                 name='calibration_point_3',
                 checks=(CheckHexList(length=LEN.CALIBRATION_POINT_3 // 8),
                         CheckInt(max_value=(1 << LEN.CALIBRATION_POINT_3) - 1),), ),
        BitField(FID.CALIBRATION_POINT_4,
                 LEN.CALIBRATION_POINT_4,
                 title='CalibrationPoint4',
                 name='calibration_point_4',
                 checks=(CheckHexList(length=LEN.CALIBRATION_POINT_4 // 8),
                         CheckInt(max_value=(1 << LEN.CALIBRATION_POINT_4) - 1),), ),
        BitField(FID.CALIBRATION_POINT_5,
                 LEN.CALIBRATION_POINT_5,
                 title='CalibrationPoint5',
                 name='calibration_point_5',
                 checks=(CheckHexList(length=LEN.CALIBRATION_POINT_5 // 8),
                         CheckInt(max_value=(1 << LEN.CALIBRATION_POINT_5) - 1),), ),
        BitField(FID.CALIBRATION_POINT_6,
                 LEN.CALIBRATION_POINT_6,
                 title='CalibrationPoint6',
                 name='calibration_point_6',
                 checks=(CheckHexList(length=LEN.CALIBRATION_POINT_6 // 8),
                         CheckInt(max_value=(1 << LEN.CALIBRATION_POINT_6) - 1),), ),
    )

    def __init__(self, device_index, feature_index, function_index, calibration_points_nb, calibration_point_0=0,
                 calibration_point_1=0, calibration_point_2=0, calibration_point_3=0, calibration_point_4=0,
                 calibration_point_5=0, calibration_point_6=0, **kwargs):
        """
        Constructor

        :param  device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param function_index: Function Index
        :type function_index: ``int`` or ``HexList``
        :param  calibration_points_nb: Number of Calibration Points (1 byte) Max 7 points
        :type calibration_points_nb: ``int``
        :param  calibration_point_0: Calibration point 0
        :type calibration_point_0: ``int``
        :param  calibration_point_1: Calibration point 1
        :type calibration_point_1: ``int``
        :param  calibration_point_2: Calibration point 2
        :type calibration_point_2: ``int``
        :param  calibration_point_3: Calibration point 3
        :type calibration_point_3: ``int``
        :param  calibration_point_4: Calibration point 4
        :type calibration_point_4: ``int``
        :param  calibration_point_5: Calibration point 5
        :type calibration_point_5: ``int``
        :param  calibration_point_6: Calibration point 6
        :type calibration_point_6: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, functionIndex=function_index, **kwargs)
        # The requests and responses are 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG

        self.calibration_points_nb = calibration_points_nb
        self.reserved = 0
        self.calibration_point_0 = calibration_point_0
        self.calibration_point_1 = calibration_point_1
        self.calibration_point_2 = calibration_point_2
        self.calibration_point_3 = calibration_point_3
        self.calibration_point_4 = calibration_point_4
        self.calibration_point_5 = calibration_point_5
        self.calibration_point_6 = calibration_point_6
    # end def __init__
# end class BatteryCalibrationFormat


class BatteryLevelsCalibrationRequest(BatteryLevelsCalibration):
    """
    BatteryLevelsCalibration Basic request implementation class

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       24
    ============================  ==========
    """

    class FID(BatteryLevelsCalibration.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(BatteryLevelsCalibration.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = BatteryLevelsCalibration.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(length=LEN.PADDING // 8), CheckByte(),),
                 default_value=BatteryLevelsCalibration.DEFAULT.PADDING),
    )

    @DocUtils.copy_doc(BatteryLevelsCalibration.__init__)
    def __init__(self, device_index, feature_index, function_index, **kwargs):
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=function_index, **kwargs)
    # end def __init__
# end class BatteryLevelsCalibrationRequest


@DocUtils.copy_doc(BatteryLevelsCalibrationRequest)
class GetBattCalibrationInfo(BatteryLevelsCalibrationRequest):

    @DocUtils.copy_doc(BatteryLevelsCalibrationRequest.__init__)
    def __init__(self, device_index, feature_index, **kwargs):
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetBattCalibrationInfoResponse.FUNCTION_INDEX, **kwargs)
    # end def __init__
# end class GetBattCalibrationInfo


@DocUtils.copy_doc(BatteryCalibrationFormat)
class GetBattCalibrationInfoResponse(BatteryCalibrationFormat):

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBattCalibrationInfo,)
    FUNCTION_INDEX = 0
    VERSION = (0, 1,)

    @DocUtils.copy_doc(BatteryCalibrationFormat.__init__)
    def __init__(self, device_index, feature_index, calibration_points_nb, calibration_point_0=0, calibration_point_1=0,
                 calibration_point_2=0, calibration_point_3=0, calibration_point_4=0, calibration_point_5=0,
                 calibration_point_6=0, **kwargs):
        super().__init__(device_index=device_index, feature_index=feature_index, function_index=self.FUNCTION_INDEX,
                         calibration_points_nb=calibration_points_nb, calibration_point_0=calibration_point_0,
                         calibration_point_1=calibration_point_1, calibration_point_2=calibration_point_2,
                         calibration_point_3=calibration_point_3, calibration_point_4=calibration_point_4,
                         calibration_point_5=calibration_point_5, calibration_point_6=calibration_point_6, **kwargs)
    # end def __init__
# end class GetBattCalibrationInfoResponse


@DocUtils.copy_doc(BatteryLevelsCalibrationRequest)
class MeasureBattery(BatteryLevelsCalibrationRequest):

    @DocUtils.copy_doc(BatteryLevelsCalibrationRequest.__init__)
    def __init__(self, device_index, feature_index, **kwargs):
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=MeasureBatteryResponse.FUNCTION_INDEX, **kwargs)
    # end def __init__
# end class MeasureBattery


class MeasureBatteryResponse(BatteryLevelsCalibration):
    """
    BatteryLevelsCalibration MeasureBattery response implementation class

    Measurement's result of battery voltage.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Measure                       16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (MeasureBattery,)
    FUNCTION_INDEX = 1
    VERSION = (0, 1,)

    class FID(BatteryLevelsCalibration.FID):
        """
        Field Identifiers
        """
        MEASURE = 0xFA
        PADDING = 0xF9

    # end class FID

    class LEN(BatteryLevelsCalibration.LEN):
        """
        Field Lengths
        """
        MEASURE = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = BatteryLevelsCalibration.FIELDS + (
        BitField(FID.MEASURE,
                 LEN.MEASURE,
                 title='Measure',
                 name='measure',
                 checks=(CheckHexList(length=LEN.MEASURE // 8), CheckInt(max_value=(1 << LEN.MEASURE) - 1),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(length=LEN.PADDING // 8), CheckByte(),),
                 default_value=BatteryLevelsCalibration.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, measure, **kwargs):
        """
        Constructor

        :param  device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param  measure: The battery voltage measure
        :type measure: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=MeasureBatteryResponse.FUNCTION_INDEX,
                         **kwargs)
        self.measure = measure
    # end def __init__
# end class MeasureBatteryResponse


@DocUtils.copy_doc(BatteryCalibrationFormat)
class StoreCalibration(BatteryCalibrationFormat):

    @DocUtils.copy_doc(BatteryCalibrationFormat.__init__)
    def __init__(self, device_index, feature_index, calibration_points_nb, calibration_point_0=0, calibration_point_1=0,
                 calibration_point_2=0, calibration_point_3=0, calibration_point_4=0, calibration_point_5=0,
                 calibration_point_6=0, **kwargs):
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=StoreCalibrationResponse.FUNCTION_INDEX,
                         calibration_points_nb=calibration_points_nb, calibration_point_0=calibration_point_0,
                         calibration_point_1=calibration_point_1, calibration_point_2=calibration_point_2,
                         calibration_point_3=calibration_point_3, calibration_point_4=calibration_point_4,
                         calibration_point_5=calibration_point_5, calibration_point_6=calibration_point_6, **kwargs)

    # end def __init__
# end class StoreCalibration


class StoreCalibrationResponse(BatteryLevelsCalibration):
    """
    BatteryLevelsCalibration StoreCalibration response implementation class

    Response that attest that the device has stored all the calibration data measured in non-volatile memory.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StoreCalibration,)
    FUNCTION_INDEX = 2
    VERSION = (0, 1,)

    class FID(BatteryLevelsCalibration.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(BatteryLevelsCalibration.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = BatteryLevelsCalibration.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(length=LEN.PADDING // 8), CheckByte(),),
                 default_value=BatteryLevelsCalibration.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param  device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=StoreCalibrationResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class StoreCalibrationResponse


@DocUtils.copy_doc(BatteryLevelsCalibrationRequest)
class ReadCalibration(BatteryLevelsCalibrationRequest):

    @DocUtils.copy_doc(BatteryLevelsCalibrationRequest.__init__)
    def __init__(self, device_index, feature_index, **kwargs):
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadCalibrationResponse.FUNCTION_INDEX, **kwargs)
    # end def __init__
# end class ReadCalibration


@DocUtils.copy_doc(BatteryCalibrationFormat)
class ReadCalibrationResponse(BatteryCalibrationFormat):

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadCalibration,)
    FUNCTION_INDEX = 3
    VERSION = (0, 1,)

    @DocUtils.copy_doc(BatteryCalibrationFormat.__init__)
    def __init__(self, device_index, feature_index, calibration_points_nb, calibration_point_0=0, calibration_point_1=0,
                 calibration_point_2=0, calibration_point_3=0, calibration_point_4=0, calibration_point_5=0,
                 calibration_point_6=0, **kwargs):
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadCalibrationResponse.FUNCTION_INDEX,
                         calibration_points_nb=calibration_points_nb, calibration_point_0=calibration_point_0,
                         calibration_point_1=calibration_point_1, calibration_point_2=calibration_point_2,
                         calibration_point_3=calibration_point_3, calibration_point_4=calibration_point_4,
                         calibration_point_5=calibration_point_5, calibration_point_6=calibration_point_6, **kwargs)
    # end def __init__
# end class ReadCalibrationResponse


class CutOffControl(BatteryLevelsCalibration):
    """
    BatteryLevelsCalibration CutOffControl implementation class

    Enables or disables the FW cutoff.

    When the cutoff is disabled, the device will not enter the FW cutoff mode even if battery voltage is below the
    cutoff threshold. This enables the test equipment to re-calibrate units that have been already calibrated
    without risking them to go into cutoff mode.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Reserved                      6
    CutoffChangeStateRequested    1
    CutoffDesiredState            1
    Padding                       16
    ============================  ==========
    """

    class FID(BatteryLevelsCalibration.FID):
        """
        Field Identifiers
        """
        RESERVED = 0xFA
        CUTOFF_CHANGE_STATE_REQUESTED = 0xF9
        CUTOFF_DESIRED_STATE = 0xF8
        PADDING = 0xF7
    # end class FID

    class LEN(BatteryLevelsCalibration.LEN):
        """
        Field Lengths
        """
        RESERVED = 0x06
        CUTOFF_CHANGE_STATE_REQUESTED = 0x01
        CUTOFF_DESIRED_STATE = 0x01
        PADDING = 0x10
    # end class LEN

    FIELDS = BatteryLevelsCalibration.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(max_value=(1 << LEN.RESERVED) - 1),)),
        BitField(FID.CUTOFF_CHANGE_STATE_REQUESTED,
                 LEN.CUTOFF_CHANGE_STATE_REQUESTED,
                 title='CutoffChangeStateRequested',
                 name='cutoff_change_state_requested',
                 checks=(CheckInt(max_value=(1 << LEN.CUTOFF_CHANGE_STATE_REQUESTED) - 1),)),
        BitField(FID.CUTOFF_DESIRED_STATE,
                 LEN.CUTOFF_DESIRED_STATE,
                 title='CutoffDesiredState',
                 name='cutoff_desired_state',
                 checks=(CheckInt(max_value=(1 << LEN.CUTOFF_DESIRED_STATE) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(length=LEN.PADDING // 8), CheckByte(),),
                 default_value=BatteryLevelsCalibration.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, cutoff_change_state_requested, cutoff_desired_state, **kwargs):
        """
        Constructor

        :param  device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param  cutoff_change_state_requested: Whether the cutoff state has to be changed
        :type cutoff_change_state_requested: ``int``
        :param  cutoff_desired_state: Desired cutoff state
        :type cutoff_desired_state: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=CutOffControlResponse.FUNCTION_INDEX,
                         **kwargs)
        self.reserved = 0
        self.cutoff_change_state_requested = cutoff_change_state_requested
        self.cutoff_desired_state = cutoff_desired_state
    # end def __init__
# end class CutOffControl


class CutOffControlResponse(BatteryLevelsCalibration):
    """
    BatteryLevelsCalibration CutOffControl implementation class

    Response of CutOffControl that gives the current cutoff state.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Reserved                      7
    CutoffState                   1
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (CutOffControl,)
    FUNCTION_INDEX = 4
    VERSION = (0, 1,)

    class FID(BatteryLevelsCalibration.FID):
        """
        Field Identifiers
        """
        RESERVED = 0xFA
        CUTOFF_STATE = 0xF9
        PADDING = 0xF8
    # end class FID

    class LEN(BatteryLevelsCalibration.LEN):
        """
        Field Lengths
        """
        RESERVED = 0x07
        CUTOFF_STATE = 0x01
        PADDING = 0x78
    # end class LEN

    FIELDS = BatteryLevelsCalibration.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(max_value=(1 << LEN.RESERVED) - 1),)),
        BitField(FID.CUTOFF_STATE,
                 LEN.CUTOFF_STATE,
                 0x00,
                 0x00,
                 title='CutoffState',
                 name='cutoff_state',
                 checks=(CheckInt(max_value=(1 << LEN.CUTOFF_STATE) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(length=LEN.PADDING // 8), CheckByte(),),
                 default_value=BatteryLevelsCalibration.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, cutoff_state, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param cutoff_state: Current cutoff state
        :type cutoff_state: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
        self.reserved = 0
        self.cutoff_state = cutoff_state
    # end def __init__
# end class CutOffControlResponse


class SetBatterySourceInfo(BatteryLevelsCalibration):
    """
    BatteryLevelsCalibration SetBatterySourceInfo implementation class

    Use to set battery information in case of multi-sourcing support

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    BatterySourceIndex            8
    Padding                       16
    ============================  ==========
    """

    class FID(BatteryLevelsCalibration.FID):
        """
        Field Identifiers
        """
        BATTERY_SOURCE_INDEX = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(BatteryLevelsCalibration.LEN):
        """
        Field Lengths
        """
        BATTERY_SOURCE_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    class DEFAULT(BatteryLevelsCalibration.DEFAULT):
        """
        Default values
        """
        BATTERY_SOURCE_INDEX = 0x00
    # end class DEFAULT

    FIELDS = BatteryLevelsCalibration.FIELDS + (
        BitField(FID.BATTERY_SOURCE_INDEX,
                 LEN.BATTERY_SOURCE_INDEX,
                 title='BatterySourceIndex',
                 name='battery_source_index',
                 checks=(CheckHexList(length=LEN.BATTERY_SOURCE_INDEX // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(length=LEN.PADDING // 8), CheckByte(),),
                 default_value=BatteryLevelsCalibration.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, battery_source_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param battery_source_index: Index identifying the battery which shall be used in case of battery
                                     multi-sourcing support.
        :type battery_source_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=SetBatterySourceInfoResponse.FUNCTION_INDEX,
                         **kwargs)
        self.battery_source_index = battery_source_index
    # end def __init__
# end class SetBatterySourceInfo


@DocUtils.copy_doc(SetBatterySourceInfo)
class SetBatterySourceInfoResponse(SetBatterySourceInfo):

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetBatterySourceInfo,)
    FUNCTION_INDEX = 5
    VERSION = (1,)

    class LEN(SetBatterySourceInfo.LEN):
        """
        Field Lengths
        """
        PADDING = 0x78
    # end class LEN

    FIELDS = SetBatterySourceInfo.FIELDS[:-1] + (
        BitField(SetBatterySourceInfo.FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(length=LEN.PADDING // 8), CheckByte(),),
                 default_value=SetBatterySourceInfo.DEFAULT.PADDING),
    )
# end class SetBatterySourceInfoResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
