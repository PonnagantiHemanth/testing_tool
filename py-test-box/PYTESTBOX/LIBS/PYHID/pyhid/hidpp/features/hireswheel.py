#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.hireswheel
:brief: HID++ 2.0 HiResWheel command interface definition
:author: Andy Su
:date: 2019/3/25
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
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HiResWheel(HidppMessage):
    """
    High Resolution Wheel implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x2121
    MAX_FUNCTION_INDEX = 3
    MAX_FUNCTION_INDEX_V1 = 4

    # Target values
    HID = 0
    HIDPP = 1
    TARGETS = [HID, HIDPP]

    # Resolution values
    LOW_RESOLUTION = 0
    HIGH_RESOLUTION = 1
    RESOLUTIONS = [LOW_RESOLUTION, HIGH_RESOLUTION]

    # Invert values
    NOT_INVERT = 0
    INVERT = 1
    INVERTS = [NOT_INVERT, INVERT]

    # Analytics
    NON_ANALYTIC = 0
    ANALYTIC = 1
    ANALYTICS = [NON_ANALYTIC, ANALYTIC]

    # Reserved value
    DEFAULT_RESERVED = 0

    # Ratchet state values
    FREE_WHEEL = 0
    RATCHET_ENGAGED = 1
    STATES = [FREE_WHEEL, RATCHET_ENGAGED]

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  feature Index
        """
        super(HiResWheel, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
# end class HiResWheel


class HiResWheelModel(FeatureModel):
    """
    High Resolution Wheel feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_WHEEL_CAPABILITY = 0
        GET_WHEEL_MODE = 1
        SET_WHEEL_MODE = 2
        GET_RATCHET_SWITCH = 3
        GET_ANALYTICS_DATA = 4

        WHEEL_MOVEMENT_EVENT = 0
        RATCHET_SWITCH_EVENT = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        High Resolution Wheel feature data model
        """
        return {
            "feature_base": HiResWheel,
            "versions": {
                HiResWheelV0.VERSION: {
                    "main_cls": HiResWheelV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_WHEEL_CAPABILITY: {"request": GetWheelCapability,
                                                             "response": GetWheelCapabilityResponse},
                            cls.INDEX.GET_WHEEL_MODE: {"request": GetWheelMode, "response": GetWheelModeResponse},
                            cls.INDEX.SET_WHEEL_MODE: {"request": SetWheelModev0, "response": SetWheelModev0Response},
                            cls.INDEX.GET_RATCHET_SWITCH: {"request": GetRatchetSwitchState,
                                                           "response": GetRatchetSwitchStateResponse},
                        },
                        "events": {
                            cls.INDEX.WHEEL_MOVEMENT_EVENT: {"report": WheelMovementEvent},
                            cls.INDEX.RATCHET_SWITCH_EVENT: {"report": RatchetSwitchEvent}
                        }
                    }
                },
                HiResWheelV1.VERSION: {
                    "main_cls": HiResWheelV1,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_WHEEL_CAPABILITY: {"request": GetWheelCapability,
                                                             "response": GetWheelCapabilityv1Response},
                            cls.INDEX.GET_WHEEL_MODE: {"request": GetWheelMode, "response": GetWheelModev1Response},
                            cls.INDEX.SET_WHEEL_MODE: {"request": SetWheelModev1, "response": SetWheelModev1Response},
                            cls.INDEX.GET_RATCHET_SWITCH: {"request": GetRatchetSwitchState,
                                                           "response": GetRatchetSwitchStateResponse},
                            cls.INDEX.GET_ANALYTICS_DATA: {"request": GetAnalyticsData,
                                                           "response": GetAnalyticsDataResponse}
                        },
                        "events": {
                            cls.INDEX.WHEEL_MOVEMENT_EVENT: {"report": WheelMovementEvent},
                            cls.INDEX.RATCHET_SWITCH_EVENT: {"report": RatchetSwitchEvent}
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class HiResWheelModel


class HiResWheelFactory(FeatureFactory):
    """
    High Resolution Wheel factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        High Resolution Wheel object creation from version number

        :param version: High Resolution Wheel feature version
        :type version: ``int``
        :return: High Resolution Wheel object
        :rtype: ``HiResWheelInterface``
        """
        return HiResWheelModel.get_main_cls(version)()
    # end def create
# end class HiResWheelFactory


class HiResWheelInterface(FeatureInterface, ABC):
    """
    Interface to High Resolution Wheel

    Defines required interfaces for High Resolution Wheel classes
    """
    def __init__(self):
        """
        Constructor
        """
        # Requests
        self.get_wheel_capability_cls = None
        self.get_wheel_mode_cls = None
        self.set_wheel_mode_cls = None
        self.get_ratchet_switch_state_cls = None
        self.get_analytics_data_cls = None

        # Responses
        self.get_wheel_capability_response_cls = None
        self.get_wheel_mode_response_cls = None
        self.set_wheel_mode_response_cls = None
        self.get_ratchet_switch_state_response_cls = None
        self.get_analytics_data_response_cls = None

        # Events
        self.wheel_movement_event_cls = None
        self.ratchet_switch_event_cls = None
    # end def __init__
# end class HiResWheelInterface


class HiResWheelV0(HiResWheelInterface):
    """
    High resolution wheel

    [0] getWheelCapability() -> multiplier, hasSwitch, hasInvert
    [1] getWheelMode() -> target, resolution, invert
    [2] setWheelMode(target,resolution, invert) -> target, resolution, invert
    [3] getRatchetSwitchState() -> state
    [event0] wheelMovement() -> resolution, periods, deltaV
    [event1] ratchetSwitch() -> state
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`HiResWheelInterface.__init__`
        """
        super().__init__()
        # Requests
        self.get_wheel_capability_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_WHEEL_CAPABILITY)
        self.get_wheel_mode_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_WHEEL_MODE)
        self.set_wheel_mode_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.SET_WHEEL_MODE)
        self.get_ratchet_switch_state_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_RATCHET_SWITCH)

        # Responses
        self.get_wheel_capability_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_WHEEL_CAPABILITY)
        self.get_wheel_mode_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_WHEEL_MODE)
        self.set_wheel_mode_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.SET_WHEEL_MODE)
        self.get_ratchet_switch_state_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_RATCHET_SWITCH)

        # Events
        self.wheel_movement_event_cls = HiResWheelModel.get_report_cls(
            self.VERSION, HiResWheelModel.INDEX.WHEEL_MOVEMENT_EVENT)
        self.ratchet_switch_event_cls = HiResWheelModel.get_report_cls(
            self.VERSION, HiResWheelModel.INDEX.RATCHET_SWITCH_EVENT)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`HiResWheelInterface.get_max_function_index`
        """
        return HiResWheelModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class HiResWheelV0


class HiResWheelV1(HiResWheelInterface):
    """
    High resolution wheel

    [0] getWheelCapability() -> multiplier, hasSwitch, hasInvert, hasAnalyticsData, ratchetsPerRotation, wheelDiameter
    [1] getWheelMode() -> target, resolution, invert, analytics
    [2] setWheelMode(target,resolution, invert, analytics) -> target, resolution, invert, analytics
    [3] getRatchetSwitchState() -> state
    [4] getAnalyticsData() -> analyticsData
    [event0] wheelMovement() -> resolution, periods, deltaV
    [event1] ratchetSwitch() -> state
    """
    VERSION = 1

    def __init__(self):
        """
        See :any:`HiResWheelInterface.__init__`
        """
        super().__init__()
        # Requests
        self.get_wheel_capability_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_WHEEL_CAPABILITY)
        self.get_wheel_mode_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_WHEEL_MODE)
        self.set_wheel_mode_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.SET_WHEEL_MODE)
        self.get_ratchet_switch_state_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_RATCHET_SWITCH)
        self.get_analytics_data_cls = HiResWheelModel.get_request_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_ANALYTICS_DATA)

        # Responses
        self.get_wheel_capability_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_WHEEL_CAPABILITY)
        self.get_wheel_mode_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_WHEEL_MODE)
        self.set_wheel_mode_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.SET_WHEEL_MODE)
        self.get_ratchet_switch_state_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_RATCHET_SWITCH)
        self.get_analytics_data_response_cls = HiResWheelModel.get_response_cls(
            self.VERSION, HiResWheelModel.INDEX.GET_ANALYTICS_DATA)

        # Events
        self.wheel_movement_event_cls = HiResWheelModel.get_report_cls(
            self.VERSION, HiResWheelModel.INDEX.WHEEL_MOVEMENT_EVENT)
        self.ratchet_switch_event_cls = HiResWheelModel.get_report_cls(
            self.VERSION, HiResWheelModel.INDEX.RATCHET_SWITCH_EVENT)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`HiResWheelInterface.get_max_function_index`
        """
        return HiResWheelModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index

    def get_analytics_data_product_specific_cls(self, product_ref):
        """
        Get project specific analytics data if available

        :param product_ref: Product reference
        :type product_ref: ``str``

        :return: Product specific analytics data, if available
        :rtype: ``GetAnalyticsDataResponse``
        """
        project_map = {
            "MPM19": GetAnalyticsDataHERZOGResponse
        }

        return project_map[product_ref] if product_ref in project_map.keys() else self.get_analytics_data_cls
    # end def get_analytics_data_product_specific_cls
# end class HiResWheelV1


class GetWheelCapability(HiResWheel):
    """
    HiResWheel GetWheelCapability implementation class

    Returns the static capability information about the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId):
        """
        Constructor
        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetWheelCapability, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetWheelCapabilityResponse.FUNCTION_INDEX
    # end def __init__
# end class GetWheelCapability


class GetWheelCapabilityResponse(HiResWheel):
    """
    HiResWheel GetWheelCapability response implementation class

    Returns the static capability information about the device.

    Format:
    || @b Name          || @b Bit count ||
    || ReportID         || 8            ||
    || DeviceIndex      || 8            ||
    || FeatureIndex     || 8            ||
    || FunctionID       || 4            ||
    || SoftwareID       || 4            ||
    || Multiplier       || 8            ||
    || Reserved 1       || 4            ||
    || HasInvert        || 1            ||
    || HasSwitch        || 1            ||
    || Reserved 2       || 2            ||
    || Padding          || 112          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetWheelCapability)
    FUNCTION_INDEX = 0
    VERSION = (0, )

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        MULTIPLIER  = 0xFA
        RESERVED1   = 0xF9
        HASINVERT   = 0xF8
        HASSWITCH   = 0xF7
        RESERVED2   = 0xF6
        PADDING     = 0xF5

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        MULTIPLIER  = 0x08
        RESERVED1   = 0x04
        HASINVERT   = 0x01
        HASSWITCH   = 0x01
        RESERVED2   = 0x02
        PADDING     = 0x70

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.MULTIPLIER,
                 LEN.MULTIPLIER,
                 0x00,
                 0x00,
                 title='Multiplier',
                 name='multiplier',
                 checks=(CheckHexList(LEN.MULTIPLIER // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.RESERVED1,
                 LEN.RESERVED1,
                 0x00,
                 0x00,
                 title='Reserved1',
                 name='reserved1',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED1) - 1),)),

        BitField(FID.HASINVERT,
                 LEN.HASINVERT,
                 0x00,
                 0x00,
                 title='HasInvert',
                 name='hasInvert',
                 checks=(CheckInt(0, pow(2, LEN.HASINVERT) - 1),)),

        BitField(FID.HASSWITCH,
                 LEN.HASSWITCH,
                 0x00,
                 0x00,
                 title='HasSwitch',
                 name='hasSwitch',
                 checks=(CheckInt(0, pow(2, LEN.HASSWITCH) - 1),)),

        BitField(FID.RESERVED2,
                 LEN.RESERVED2,
                 0x00,
                 0x00,
                 title='Reserved2',
                 name='reserved2',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED2) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex, featureId, multiplier, reserved1, hasInvert, hasSwitch, reserved2):
        """
        Constructor

        @param  deviceIndex   [in] (int)  Device Index
        @param  featureId     [in] (int)  desired feature Id
        @param  multiplier    [in] (int)  returned multiplier
        @param  reserved1     [in] (int)  returned reserved1 bits
        @param  hasInvert     [in] (int)  returned hasInvert
        @param  hasSwitch     [in] (int)  returned hasSwitch
        @param  reserved2     [in] (int)  returned reserved2 bits
        """
        super(GetWheelCapabilityResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.multiplier = multiplier
        self.reserved1 = reserved1
        self.hasInvert = hasInvert
        self.hasSwitch = hasSwitch
        self.reserved2 = reserved2
    # end def __init__
# end class GetWheelCapabilityResponse


class GetWheelCapabilityv1Response(GetWheelCapabilityResponse):
    """
    HiResWheel GetWheelCapability v1 response implementation class

    Returns the static capability information about the device.

    Format:
    || @b Name               || @b Bit count ||
    || ReportID              || 8            ||
    || DeviceIndex           || 8            ||
    || FeatureIndex          || 8            ||
    || FunctionID            || 4            ||
    || SoftwareID            || 4            ||
    || Multiplier            || 8            ||
    || Reserved 1            || 3            ||
    || HasAnalyticsData      || 1            ||
    || HasInvert             || 1            ||
    || HasSwitch             || 1            ||
    || Reserved 2            || 2            ||
    || RatchetsPerRotation   || 8            ||
    || WheelDiameter         || 8            ||
    || Padding               || 96           ||
    """
    VERSION = (1, )

    class FID(GetWheelCapabilityResponse.FID):
        """
        Field Identifiers
        """
        HASANALYTICSDATA    = 0xF8
        HASINVERT           = 0xF7
        HASSWITCH           = 0xF6
        RESERVED2           = 0xF5
        RATCHETSPERROTATION = 0XF4
        WHEELDIAMETER       = 0xF3
        PADDING             = 0xF2

    # end class FID

    class LEN(GetWheelCapabilityResponse.LEN):
        """
        Field Lengths
        """
        RESERVED1 = 0x03
        HASANALYTICSDATA = 0x01
        RATCHETSPERROTATION = 0X08
        WHEELDIAMETER = 0x08
        PADDING = 0x60

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.MULTIPLIER,
                 LEN.MULTIPLIER,
                 0x00,
                 0x00,
                 title='Multiplier',
                 name='multiplier',
                 checks=(CheckHexList(LEN.MULTIPLIER // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.RESERVED1,
                 LEN.RESERVED1,
                 0x00,
                 0x00,
                 title='Reserved1',
                 name='reserved1',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED1) - 1),)),

        BitField(FID.HASANALYTICSDATA,
                 LEN.HASANALYTICSDATA,
                 0x00,
                 0x00,
                 title='HasAnalyticsData',
                 name='hasAnalyticsData',
                 checks=(CheckInt(0, pow(2, LEN.HASANALYTICSDATA) - 1),)),

        BitField(FID.HASINVERT,
                 LEN.HASINVERT,
                 0x00,
                 0x00,
                 title='HasInvert',
                 name='hasInvert',
                 checks=(CheckInt(0, pow(2, LEN.HASINVERT) - 1),)),

        BitField(FID.HASSWITCH,
                 LEN.HASSWITCH,
                 0x00,
                 0x00,
                 title='HasSwitch',
                 name='hasSwitch',
                 checks=(CheckInt(0, pow(2, LEN.HASSWITCH) - 1),)),

        BitField(FID.RESERVED2,
                 LEN.RESERVED2,
                 0x00,
                 0x00,
                 title='Reserved2',
                 name='reserved2',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED2) - 1),)),

        BitField(FID.RATCHETSPERROTATION,
                 LEN.RATCHETSPERROTATION,
                 0x00,
                 0x00,
                 title='RatchetsPerRotation',
                 name='ratchetsPerRotation',
                 checks=(CheckHexList(LEN.RATCHETSPERROTATION // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.WHEELDIAMETER,
                 LEN.WHEELDIAMETER,
                 0x00,
                 0x00,
                 title='WheelDiameter',
                 name='wheelDiameter',
                 checks=(CheckHexList(LEN.WHEELDIAMETER // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId,
                        multiplier,
                        reserved1,
                        hasAnalyticsData,
                        hasInvert,
                        hasSwitch,
                        reserved2,
                        ratchetsPerRotation,
                        wheelDiameter):
        """
        Constructor

        @param  deviceIndex           [in] (int)  Device Index
        @param  featureId             [in] (int)  desired feature Id
        @param  multiplier            [in] (int)  returned multiplier
        @param  reserved1             [in] (int)  returned reserved1 bits
        @param  hasAnalyticsData      [in] (int)  returned hasAnalyticsData
        @param  hasInvert             [in] (int)  returned hasInvert
        @param  hasSwitch             [in] (int)  returned hasSwitch
        @param  reserved2             [in] (int)  returned reserved2 bits
        @param  ratchetsPerRotation   [in] (int)  returned ratchetsPerRotation bits
        @param  wheelDiameter         [in] (int)  returned wheelDiameter bits
        """
        super(GetWheelCapabilityv1Response, self).__init__(deviceIndex, featureId, multiplier, reserved1, hasInvert,
                                                           hasSwitch, reserved2)
        self.hasAnalyticsData = hasAnalyticsData
        self.ratchetsPerRotation = ratchetsPerRotation
        self.wheelDiameter = wheelDiameter
    # end def __init__
# end class GetWheelCapabilityv1Response


class GetWheelMode(HiResWheel):
    """
    HiResWheel GetWheelModev0 implementation class

    Returns the current wheel mode about the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetWheelMode, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetWheelModeResponse.FUNCTION_INDEX
    # end def __init__
# end class GetWheelMode


class GetWheelModeResponse(HiResWheel):
    """
    HiResWheel GetWheelMode response implementation class

    Returns the current wheel mode about the device.

    Format:
    || @b Name               || @b Bit count ||
    || ReportID              || 8            ||
    || DeviceIndex           || 8            ||
    || FeatureIndex          || 8            ||
    || FunctionID            || 4            ||
    || SoftwareID            || 4            ||
    || Reserved              || 5            ||
    || Invert                || 1            ||
    || Resolution            || 1            ||
    || target                || 1            ||
    || Padding               || 120          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetWheelMode)
    FUNCTION_INDEX = 1
    VERSION = (0, )

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        RESERVED    = 0xFA
        INVERT      = 0xF9
        RESOLUTION  = 0xF8
        TARGET      = 0xF7
        PADDING     = 0xF6

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        RESERVED    = 0x05
        INVERT      = 0x01
        RESOLUTION  = 0x01
        TARGET      = 0x01
        PADDING     = 0x78

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.INVERT,
                 LEN.INVERT,
                 0x00,
                 0x00,
                 title='Invert',
                 name='invert',
                 checks=(CheckInt(0, pow(2, LEN.INVERT) - 1),)),

        BitField(FID.RESOLUTION,
                 LEN.RESOLUTION,
                 0x00,
                 0x00,
                 title='Resolution',
                 name='resolution',
                 checks=(CheckInt(0, pow(2, LEN.RESOLUTION) - 1),)),

        BitField(FID.TARGET,
                 LEN.TARGET,
                 0x00,
                 0x00,
                 title='Target',
                 name='target',
                 checks=(CheckInt(0, pow(2, LEN.TARGET) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId,
                        reserved,
                        invert,
                        resolution,
                        target):
        """
        Constructor

        @param  deviceIndex       [in] (int)   Device Index
        @param  featureId         [in] (int)   desired feature Id
        @param  reserved          [in] (int)   returned reserved bits
        @param  invert            [in] (int)   returned invert
        @param  resolution        [in] (int)   returned resolution
        @param  target            [in] (int)   returned target
        """
        super(GetWheelModeResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.reserved = reserved
        self.invert = invert
        self.resolution = resolution
        self.target = target
    # end def __init__
# end class GetWheelModeResponse


class GetWheelModev1Response(GetWheelModeResponse):
    """
    HiResWheel GetWheelMode v1 response implementation class

    Returns the current wheel mode about the device.

    Format:
    || @b Name               || @b Bit count ||
    || ReportID              || 8            ||
    || DeviceIndex           || 8            ||
    || FeatureIndex          || 8            ||
    || FunctionID            || 4            ||
    || SoftwareID            || 4            ||
    || Reserved              || 4            ||
    || Analytics             || 1            ||
    || Invert                || 1            ||
    || Resolution            || 1            ||
    || target                || 1            ||
    || Padding               || 120          ||
    """
    VERSION = (1, )

    class FID(GetWheelModeResponse.FID):
        """
        Field Identifiers
        """
        ANALYTICS   = 0xF9
        INVERT      = 0xF8
        RESOLUTION  = 0xF7
        TARGET      = 0xF6
        PADDING     = 0xF5

    # end class FID

    class LEN(GetWheelModeResponse.LEN):
        """
        Field Lengths
        """
        RESERVED    = 0x04
        ANALYTICS   = 0x01

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.ANALYTICS,
                 LEN.ANALYTICS,
                 0x00,
                 0x00,
                 title='Analytics',
                 name='analytics',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS) - 1),)),

        BitField(FID.INVERT,
                 LEN.INVERT,
                 0x00,
                 0x00,
                 title='Invert',
                 name='invert',
                 checks=(CheckInt(0, pow(2, LEN.INVERT) - 1),)),

        BitField(FID.RESOLUTION,
                 LEN.RESOLUTION,
                 0x00,
                 0x00,
                 title='Resolution',
                 name='resolution',
                 checks=(CheckInt(0, pow(2, LEN.RESOLUTION) - 1),)),

        BitField(FID.TARGET,
                 LEN.TARGET,
                 0x00,
                 0x00,
                 title='Target',
                 name='target',
                 checks=(CheckInt(0, pow(2, LEN.TARGET) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId,
                        reserved,
                        analytics,
                        invert,
                        resolution,
                        target):
        """
        Constructor

        @param  deviceIndex       [in] (int)   Device Index
        @param  featureId         [in] (int)   desired feature Id
        @param  reserved          [in] (int)   returned reserved bits
        @param  analytics         [in] (int)   returned analytics
        @param  invert            [in] (int)   returned invert
        @param  resolution        [in] (int)   returned resolution
        @param  target            [in] (int)   returned target
        """
        super(GetWheelModev1Response, self).__init__(deviceIndex, featureId, reserved, invert, resolution, target)

        self.analytics = analytics
    # end def __init__
# end class GetWheelModev1Response


class SetWheelModev0(HiResWheel):
    """
    HiResWheel SetWheelModev0 implementation class

    Returns the setting wheel mode about the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Reserved               || 5            ||
    || Invert                 || 1            ||
    || Resolution             || 1            ||
    || Target                 || 1            ||
    || Padding                || 16           ||
    """

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        RESERVED    = 0xFA
        INVERT      = 0xF9
        RESOLUTION  = 0xF8
        TARGET      = 0xF7
        PADDING     = 0xF6

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        RESERVED    = 0x05
        INVERT      = 0x01
        RESOLUTION  = 0x01
        TARGET      = 0x01
        PADDING     = 0x10

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.INVERT,
                 LEN.INVERT,
                 0x00,
                 0x00,
                 title='Invert',
                 name='invert',
                 checks=(CheckInt(0, pow(2, LEN.INVERT) - 1),)),

        BitField(FID.RESOLUTION,
                 LEN.RESOLUTION,
                 0x00,
                 0x00,
                 title='Resolution',
                 name='resolution',
                 checks=(CheckInt(0, pow(2, LEN.RESOLUTION) - 1),)),

        BitField(FID.TARGET,
                 LEN.TARGET,
                 0x00,
                 0x00,
                 title='Target',
                 name='target',
                 checks=(CheckInt(0, pow(2, LEN.TARGET) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                       featureId,
                       reserved,
                       invert,
                       resolution,
                       target,
                       **kwargs):
        """
        Constructor

        @param  deviceIndex       [in] (int)  Device Index
        @param  featureId         [in] (int)  desired feature Id
        @param  reserved          [in] (int)  returned reserved bits
        @param  invert            [in] (int)  returned invert
        @param  resolution        [in] (int)  returned resolution
        @param  target            [in] (int)  returned target
        @param kwargs             [in] (dict | None) Potential future parameters
        """
        super(SetWheelModev0, self).__init__(deviceIndex, featureId)

        self.functionIndex = SetWheelModev0Response.FUNCTION_INDEX
        self.reserved = reserved
        self.invert = invert
        self.resolution = resolution
        self.target = target
    # end def __init__
# end class SetWheelModev0


class SetWheelModev0Response(HiResWheel):
    """
    HiResWheel SetWheelMode v0 response implementation class

    Returns the setting wheel mode about the device.

    Format:
    || @b Name               || @b Bit count ||
    || ReportID              || 8            ||
    || DeviceIndex           || 8            ||
    || FeatureIndex          || 8            ||
    || FunctionID            || 4            ||
    || SoftwareID            || 4            ||
    || Reserved              || 5            ||
    || Invert                || 1            ||
    || Resolution            || 1            ||
    || Target                || 1            ||
    || Padding               || 120          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetWheelModev0)
    FUNCTION_INDEX = 2
    VERSION = (0, )

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        RESERVED = 0xFA
        INVERT = 0xF9
        RESOLUTION = 0xF8
        TARGET = 0xF7
        PADDING = 0xF6

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        RESERVED = 0x05
        INVERT = 0x01
        RESOLUTION = 0x01
        TARGET = 0x01
        PADDING = 0x78

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.INVERT,
                 LEN.INVERT,
                 0x00,
                 0x00,
                 title='Invert',
                 name='invert',
                 checks=(CheckInt(0, pow(2, LEN.INVERT) - 1),)),

        BitField(FID.RESOLUTION,
                 LEN.RESOLUTION,
                 0x00,
                 0x00,
                 title='Resolution',
                 name='resolution',
                 checks=(CheckInt(0, pow(2, LEN.RESOLUTION) - 1),)),

        BitField(FID.TARGET,
                 LEN.TARGET,
                 0x00,
                 0x00,
                 title='Target',
                 name='target',
                 checks=(CheckInt(0, pow(2, LEN.TARGET) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                       featureId,
                       reserved,
                       invert,
                       resolution,
                       target):
        """
        Constructor

        @param  deviceIndex       [in] (int)  Device Index
        @param  featureId         [in] (int)  desired feature Id
        @param  reserved          [in] (int)  returned reserved bits
        @param  invert            [in] (int)  returned invert
        @param  resolution        [in] (int)  returned resolution
        @param  target            [in] (int)  returned target
        """
        super(SetWheelModev0Response, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.reserved = reserved
        self.invert = invert
        self.resolution = resolution
        self.target = target
    # end def __init__
# end class SetWheelModev0Response


class SetWheelModev1(HiResWheel):
    """
    HiResWheel SetWheelModev1 implementation class

    Returns the setting wheel mode about the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Reserved               || 4            ||
    || Analytics              || 1            ||
    || Invert                 || 1            ||
    || Resolution             || 1            ||
    || Target                 || 1            ||
    || Padding                || 16           ||
    """

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        RESERVED    = 0xFA
        ANALYTICS   = 0xF9
        INVERT      = 0xF8
        RESOLUTION  = 0xF7
        TARGET      = 0xF6
        PADDING     = 0xF5

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        RESERVED    = 0x04
        ANALYTICS   = 0x01
        INVERT      = 0x01
        RESOLUTION  = 0x01
        TARGET      = 0x01
        PADDING     = 0x10

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.ANALYTICS,
                 LEN.ANALYTICS,
                 0x00,
                 0x00,
                 title='Analytics',
                 name='analytics',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS) - 1),)),

        BitField(FID.INVERT,
                 LEN.INVERT,
                 0x00,
                 0x00,
                 title='Invert',
                 name='invert',
                 checks=(CheckInt(0, pow(2, LEN.INVERT) - 1),)),

        BitField(FID.RESOLUTION,
                 LEN.RESOLUTION,
                 0x00,
                 0x00,
                 title='Resolution',
                 name='resolution',
                 checks=(CheckInt(0, pow(2, LEN.RESOLUTION) - 1),)),

        BitField(FID.TARGET,
                 LEN.TARGET,
                 0x00,
                 0x00,
                 title='Target',
                 name='target',
                 checks=(CheckInt(0, pow(2, LEN.TARGET) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                       featureId,
                       reserved,
                       analytics,
                       invert,
                       resolution,
                       target):
        """
        Constructor

        @param  deviceIndex       [in] (int)  Device Index
        @param  featureId         [in] (int)  desired feature Id
        @param  reserved          [in] (int)  returned reserved bits
        @param  analytics         [in] (int)  returned analytics
        @param  invert            [in] (int)  returned invert
        @param  resolution        [in] (int)  returned resolution
        @param  target            [in] (int)  returned target
        """
        super(SetWheelModev1, self).__init__(deviceIndex, featureId)

        self.functionIndex = SetWheelModev0Response.FUNCTION_INDEX
        self.reserved = reserved
        self.analytics = analytics
        self.invert = invert
        self.resolution = resolution
        self.target = target
    # end def __init__
# end class SetWheelModev1


class SetWheelModev1Response(SetWheelModev0Response):
    """
    HiResWheel SetWheelMode v1 response implementation class

    Returns the setting wheel mode about the device.

    Format:
    || @b Name               || @b Bit count ||
    || ReportID              || 8            ||
    || DeviceIndex           || 8            ||
    || FeatureIndex          || 8            ||
    || FunctionID            || 4            ||
    || SoftwareID            || 4            ||
    || Reserved              || 4            ||
    || Analytics             || 1            ||
    || Invert                || 1            ||
    || Resolution            || 1            ||
    || Target                || 1            ||
    || Padding               || 120          ||
    """
    REQUEST_LIST = (SetWheelModev1)
    VERSION = (1, )

    class FID(SetWheelModev0Response.FID):
        """
        Field Identifiers
        """
        ANALYTICS = 0xF9
        INVERT = 0xF8
        RESOLUTION = 0xF7
        TARGET = 0xF6
        PADDING = 0xF5

    # end class FID

    class LEN(SetWheelModev0Response.LEN):
        """
        Field Lengths
        """
        RESERVED = 0x04
        ANALYTICS = 0x01

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.ANALYTICS,
                 LEN.ANALYTICS,
                 0x00,
                 0x00,
                 title='Analytics',
                 name='analytics',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS) - 1),)),

        BitField(FID.INVERT,
                 LEN.INVERT,
                 0x00,
                 0x00,
                 title='Invert',
                 name='invert',
                 checks=(CheckInt(0, pow(2, LEN.INVERT) - 1),)),

        BitField(FID.RESOLUTION,
                 LEN.RESOLUTION,
                 0x00,
                 0x00,
                 title='Resolution',
                 name='resolution',
                 checks=(CheckInt(0, pow(2, LEN.RESOLUTION) - 1),)),

        BitField(FID.TARGET,
                 LEN.TARGET,
                 0x00,
                 0x00,
                 title='Target',
                 name='target',
                 checks=(CheckInt(0, pow(2, LEN.TARGET) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                       featureId,
                       reserved,
                       analytics,
                       invert,
                       resolution,
                       target):
        """
        Constructor

        @param  deviceIndex       [in] (int)  Device Index
        @param  featureId         [in] (int)  desired feature Id
        @param  reserved          [in] (int)  returned reserved bits
        @param  analytics         [in] (int)  returned analytics
        @param  invert            [in] (int)  returned invert
        @param  resolution        [in] (int)  returned resolution
        @param  target            [in] (int)  returned target
        """
        super(SetWheelModev1Response, self).__init__(deviceIndex, featureId, reserved, invert, resolution, target)

        self.analytics = analytics
    # end def __init__
# end class SetWheelModev1Response


class GetRatchetSwitchState(HiResWheel):
    """
    HiResWheel GetRatchetSwitchState implementation class

    Returns the ratchet state about the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetRatchetSwitchState, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetRatchetSwitchStateResponse.FUNCTION_INDEX
    # end def __init__
# end class GetRatchetSwitchState


class GetRatchetSwitchStateResponse(HiResWheel):
    """
    HiResWheel GetRatchetSwitchState response implementation class

    Returns the ratchet state about the device.

    Format:
    || @b Name          || @b Bit count ||
    || ReportID         || 8            ||
    || DeviceIndex      || 8            ||
    || FeatureIndex     || 8            ||
    || FunctionID       || 4            ||
    || SoftwareID       || 4            ||
    || Reserved         || 7            ||
    || State            || 1            ||
    || Padding          || 120          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRatchetSwitchState)
    FUNCTION_INDEX = 3
    VERSION = (0, 1, )

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        RESERVED   = 0xFA
        STATE      = 0xF9
        PADDING    = 0xF8

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        RESERVED   = 0x07
        STATE      = 0x01
        PADDING    = 0x78

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.STATE,
                 LEN.STATE,
                 0x00,
                 0x00,
                 title='State',
                 name='state',
                 checks=(CheckInt(0, pow(2, LEN.STATE) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId,
                        reserved,
                        state):
        """
        Constructor

        @param  deviceIndex      [in] (int)  Device Index
        @param  featureId        [in] (int)  desired feature Id
        @param  reserved         [in] (int)  returned reserved bits
        @param  state            [in] (int)  returned state of ratchet
        """
        super(GetRatchetSwitchStateResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.reserved = reserved
        self.state = state
    # end def __init__
# end class GetRatchetSwitchStateResponse


class GetAnalyticsData(HiResWheel):
    """
    HiResWheel GetAnalyticsData implementation class

    Returns the analytics data about the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetAnalyticsData, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetAnalyticsDataResponse.FUNCTION_INDEX
    # end def __init__
# end class GetAnalyticsData


class GetAnalyticsDataResponse(HiResWheel):
    """
    HiResWheel GetAnalyticsData response implementation class

    Returns the analytics data about the device.

    Format:
    || @b Name                   || @b Bit count ||
    || ReportID                  || 8            ||
    || DeviceIndex               || 8            ||
    || FeatureIndex              || 8            ||
    || FunctionID                || 4            ||
    || SoftwareID                || 4            ||
    || AnalyticsData             || 128          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAnalyticsData)
    FUNCTION_INDEX = 4
    VERSION = (1, )

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        ANALYTICSDATA = 0xFA

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        ANALYTICSDATA = 0x80

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.ANALYTICSDATA,
                 LEN.ANALYTICSDATA,
                 0x00,
                 0x00,
                 title='AnalyticsData',
                 name='analyticsData',
                 checks=(CheckHexList(LEN.ANALYTICSDATA // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),
    )

    def __init__(self, deviceIndex,
                        featureId,
                        analyticsData):
        """
        Constructor

        @param  deviceIndex         [in] (int)  Device Index
        @param  featureId           [in] (int)  desired feature Id
        @param  analyticsData       [in] (int)  returned analytics data
        """
        super(GetAnalyticsDataResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.analyticsData = analyticsData
    # end def __init__
# end class GetAnalyticsDataResponse


class GetAnalyticsDataHERZOGResponse(GetAnalyticsDataResponse):
    """
    HiResWheel GetAnalyticsData response implementation class

    Returns the analytics data about the HERZOG.

    Format:
    || @b Name                   || @b Bit count ||
    || ReportID                  || 8            ||
    || DeviceIndex               || 8            ||
    || FeatureIndex              || 8            ||
    || FunctionID                || 4            ||
    || SoftwareID                || 4            ||
    || InitEpmChargeAdcBattLevel || 16           ||
    || EpmChargingTime           || 16           ||
    || EndEpmChargeAdcBattLevel  || 16           ||
    || Temperature               || 32           ||
    || Padding                   || 48           ||
    """

    class FID(GetAnalyticsDataResponse.FID):
        """
        Field Identifiers
        """
        INITEPMCHARGE = 0xFA
        EPMCHARGETIME = 0xF9
        ENDEPMCHARGE  = 0xF8
        TEMPERATURE   = 0xF7
        PADDING       = 0xF6

    # end class FID

    class LEN(GetAnalyticsDataResponse.LEN):
        """
        Field Lengths
        """
        INITEPMCHARGE = 0x10
        EPMCHARGETIME = 0x10
        ENDEPMCHARGE  = 0x10
        TEMPERATURE   = 0x20
        PADDING       = 0x30

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.INITEPMCHARGE,
                 LEN.INITEPMCHARGE,
                 0x00,
                 0x00,
                 title='InitEpmChargeAdcBattLevel',
                 name='initEpmChargeAdcBattLevel',
                 checks=(CheckHexList(LEN.INITEPMCHARGE // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.EPMCHARGETIME,
                 LEN.EPMCHARGETIME,
                 0x00,
                 0x00,
                 title='EpmChargingTime',
                 name='epmChargingTime',
                 checks=(CheckHexList(LEN.EPMCHARGETIME // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.ENDEPMCHARGE,
                 LEN.ENDEPMCHARGE,
                 0x00,
                 0x00,
                 title='EndEpmChargeAdcBattLevel',
                 name='endEpmChargeAdcBattLevel',
                 checks=(CheckHexList(LEN.ENDEPMCHARGE // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.TEMPERATURE,
                 LEN.TEMPERATURE,
                 0x00,
                 0x00,
                 title='Temperature',
                 name='temperature',
                 checks=(CheckHexList(LEN.TEMPERATURE // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                        featureId,
                        initEpmChargeAdcBattLevel,
                        epmChargingTime,
                        endEpmChargeAdcBattLevel,
                        temperature):
        """
        Constructor

        @param  deviceIndex                [in] (int)  Device Index
        @param  featureId                  [in] (int)  desired feature Id
        @param  initEpmChargeAdcBattLevel  [in] (int)  returned ADC battery level at the beginning of the EPM charge
        @param  epmChargingTime            [in] (int)  returned the duration of the EPM charging process
        @param  endEpmChargeAdcBattLevel   [in] (int)  returned ADC battery level at the end of the EPM charge
        @param  temperature                [in] (int)  returned die temperature
        """
        super(GetAnalyticsDataHERZOGResponse, self).__init__(deviceIndex, featureId, analyticsData=0)

        self.initEpmChargeAdcBattLevel = initEpmChargeAdcBattLevel
        self.epmChargingTime = epmChargingTime
        self.endEpmChargeAdcBattLevel = endEpmChargeAdcBattLevel
        self.temperature = temperature
    # end def __init__
# end class GetAnalyticsDataHERZOGResponse


class WheelMovementEvent(HiResWheel):
    """
    HiResWheel WheelMovement Event implementation class

    Reported when "target" bit is set to 1 (HID++ notification).

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Reserved               || 3            ||
    || Resolution             || 1            ||
    || Periods                || 4            ||
    || DeltaV                 || 16           ||
    || Padding                || 104          ||
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 0
    VERSION = (0, 1, )

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        RESERVED    = 0xFA
        RESOLUTION  = 0xF9
        PERIODS     = 0xF8
        DELTA_V     = 0xF7
        PADDING     = 0xF6

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        RESERVED    = 0x03
        RESOLUTION  = 0x01
        PERIODS     = 0x04
        DELTA_V     = 0x10
        PADDING     = 0x68

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.RESOLUTION,
                 LEN.RESOLUTION,
                 0x00,
                 0x00,
                 title='Resolution',
                 name='resolution',
                 checks=(CheckInt(0, pow(2, LEN.RESOLUTION) - 1),)),

        BitField(FID.PERIODS,
                 LEN.PERIODS,
                 0x00,
                 0x00,
                 title='Periods',
                 name='periods',
                 checks=(CheckInt(0, pow(2, LEN.PERIODS) - 1),)),

        BitField(FID.DELTA_V,
                 LEN.DELTA_V,
                 0x00,
                 0x00,
                 title='DeltaV',
                 name='deltaV',
                 checks=(CheckHexList(LEN.DELTA_V // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                       featureId,
                       reserved,
                       resolution,
                       periods,
                       deltaV):
        """
        Constructor

        @param  deviceIndex           [in] (int)  Device Index
        @param  featureId             [in] (int)  desired feature Id
        @param  reserved              [in] (int)  returned reserved bits
        @param  resolution            [in] (int)  returned resolution
        @param  periods               [in] (int)  returned periods
        @param  deltaV                [in] (int)  returned the vertical wheel motion delta
        """
        super(WheelMovementEvent, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.reserved = reserved
        self.resolution = resolution
        self.periods = periods
        self.deltaV = deltaV
    # end def __init__
# end class WheelMovement


class RatchetSwitchEvent(HiResWheel):
    """
    HiResWheel RatchetSwitch Event implementation class

    Reported when ratchet switch state changes.

    Format:
    || @b Name                    || @b Bit count ||
    || ReportID                   || 8            ||
    || DeviceIndex                || 8            ||
    || FeatureIndex               || 8            ||
    || FunctionID                 || 4            ||
    || SoftwareID                 || 4            ||
    || Reserved                   || 7            ||
    || State                      || 1            ||
    || Padding                    || 120          ||
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 1
    VERSION = (0, 1, )

    class FID(HiResWheel.FID):
        """
        Field Identifiers
        """
        RESERVED    = 0xFA
        STATE       = 0xF9
        PADDING     = 0xF8

    # end class FID

    class LEN(HiResWheel.LEN):
        """
        Field Lengths
        """
        RESERVED    = 0x07
        STATE       = 0x01
        PADDING     = 0x78

    # end class LEN

    FIELDS = HiResWheel.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),

        BitField(FID.STATE,
                 LEN.STATE,
                 0x00,
                 0x00,
                 title='State',
                 name='state',
                 checks=(CheckInt(0, pow(2, LEN.STATE) - 1),)),

        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=HiResWheel.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                       featureId,
                       reserved,
                       state):
        """
        Constructor

        @param  deviceIndex      [in] (int)  Device Index
        @param  featureId        [in] (int)  desired feature Id
        @param  reserved         [in] (int)  returned reserved bits
        @param  state            [in] (int)  returned state of ratchet
        """
        super(RatchetSwitchEvent, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.reserved = reserved
        self.state = state
    # end def __init__
# end class RatchetSwitch

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
