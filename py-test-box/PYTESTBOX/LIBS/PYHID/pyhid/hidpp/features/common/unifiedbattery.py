#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.unifiedbattery
    :brief: HID++ 2.0 UnifiedBattery command interface definition
    :author: Stanislas Cottard
    :date: 2019/10/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum
from enum import unique

from pyhid.bitfield import BitField
from pyhid.field import CheckBool
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class UnifiedBattery(HidppMessage):
    """
    UnifiedBattery implementation class

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
    FEATURE_ID = 0x1004
    MAX_FUNCTION_INDEX_V0 = 1
    MAX_FUNCTION_INDEX_V1_TO_V5 = 2

    BATTERY_LEVELS_V0ToV5 = ['full', 'good', 'low', 'critical']

    class ChargingStatus:
        DISCHARGING = 0
        CHARGING = 1
        CHARGING_AT_SLOW_RATE = 2
        CHARGE_COMPLETE = 3
        CHARGE_ERROR = 4
    # end class ChargingStatus

    class ExternalPowerStatus:
        NO_POWER = 0
        WIRED = 1
        WIRELESS = 2
    # end class ExternalPowerStatus

    class FastChargingStatus:
        NO_FAST_CHARGE = 0
        FAST_CHARGE = 1
    # end class FastChargingStatus

    class RemovableBatteryStatus:
        NOT_REMOVED = 0
        REMOVED = 1
    # end class RemovableBatteryStatus

    @unique
    class Flags(IntEnum):
        """
        Bit index of capability flags
        """
        RECHARGEABLE = 0
        STATE_OF_CHARGE = 1
        SHOW_BATTERY_STATUS = 2
        BATTERY_SOURCE_INDEX = 3
        FAST_CHARGING = 4
        REMOVABLE_BATTERY = 5
    # end class Flags

    def __init__(self, device_index, feature_index):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        """
        super().__init__()

        self.deviceIndex = device_index
        self.featureIndex = feature_index
# end class UnifiedBattery


class UnifiedBatteryModel(FeatureModel):
    """
    Configurable device properties feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_STATUS = 1
        SHOW_BATTERY_STATUS = 2

        # Event index
        BATTERY_STATUS = 0
    # end class

    @classmethod
    def _get_data_model(cls):
        """
        Configurable device properties feature data model
        """
        return {
            "feature_base": UnifiedBattery,
            "versions": {
                UnifiedBatteryV0.VERSION: {
                    "main_cls": UnifiedBatteryV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilitiesV0ToV5,
                                                         "response": GetCapabilitiesResponseV0ToV1},
                            cls.INDEX.GET_STATUS: {"request": GetStatusV0ToV5, "response": GetStatusResponseV0ToV3},
                        },
                        "events": {
                            cls.INDEX.BATTERY_STATUS: {"report": BatteryStatusEventV0ToV3}
                        }
                    },
                },
                UnifiedBatteryV1.VERSION: {
                    "main_cls": UnifiedBatteryV1,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilitiesV0ToV5,
                                                         "response": GetCapabilitiesResponseV0ToV1},
                            cls.INDEX.GET_STATUS: {"request": GetStatusV0ToV5, "response": GetStatusResponseV0ToV3},
                            cls.INDEX.SHOW_BATTERY_STATUS: {"request": ShowBatteryStatusV1ToV5,
                                                            "response": ShowBatteryStatusResponseV1ToV5},
                        },
                        "events": {
                            cls.INDEX.BATTERY_STATUS: {"report": BatteryStatusEventV0ToV3}
                        }
                    },
                },
                UnifiedBatteryV2.VERSION: {
                    "main_cls": UnifiedBatteryV2,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilitiesV0ToV5,
                                                         "response": GetCapabilitiesResponseV2},
                            cls.INDEX.GET_STATUS: {"request": GetStatusV0ToV5, "response": GetStatusResponseV0ToV3},
                            cls.INDEX.SHOW_BATTERY_STATUS: {"request": ShowBatteryStatusV1ToV5,
                                                            "response": ShowBatteryStatusResponseV1ToV5},
                        },
                        "events": {
                            cls.INDEX.BATTERY_STATUS: {"report": BatteryStatusEventV0ToV3}
                        }
                    },
                },
                UnifiedBatteryV3.VERSION: {
                    "main_cls": UnifiedBatteryV3,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilitiesV0ToV5,
                                                         "response": GetCapabilitiesResponseV3},
                            cls.INDEX.GET_STATUS: {"request": GetStatusV0ToV5, "response": GetStatusResponseV0ToV3},
                            cls.INDEX.SHOW_BATTERY_STATUS: {"request": ShowBatteryStatusV1ToV5,
                                                            "response": ShowBatteryStatusResponseV1ToV5},
                        },
                        "events": {
                            cls.INDEX.BATTERY_STATUS: {"report": BatteryStatusEventV0ToV3}
                        }
                    },
                },
                UnifiedBatteryV4.VERSION: {
                    "main_cls": UnifiedBatteryV4,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilitiesV0ToV5,
                                                         "response": GetCapabilitiesResponseV4},
                            cls.INDEX.GET_STATUS: {"request": GetStatusV0ToV5, "response": GetStatusResponseV4},
                            cls.INDEX.SHOW_BATTERY_STATUS: {"request": ShowBatteryStatusV1ToV5,
                                                            "response": ShowBatteryStatusResponseV1ToV5},
                        },
                        "events": {
                            cls.INDEX.BATTERY_STATUS: {"report": BatteryStatusEventV4}
                        }
                    },
                },
                UnifiedBatteryV5.VERSION: {
                    "main_cls": UnifiedBatteryV5,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilitiesV0ToV5,
                                                         "response": GetCapabilitiesResponseV5},
                            cls.INDEX.GET_STATUS: {"request": GetStatusV0ToV5, "response": GetStatusResponseV5},
                            cls.INDEX.SHOW_BATTERY_STATUS: {"request": ShowBatteryStatusV1ToV5,
                                                            "response": ShowBatteryStatusResponseV1ToV5},
                        },
                        "events": {
                            cls.INDEX.BATTERY_STATUS: {"report": BatteryStatusEventV5}
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class UnifiedBatteryModel


class UnifiedBatteryFactory(FeatureFactory):
    """
    Unified Battery factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        Unified battery object creation from version number

        :param version: Unified battery feature version
        :type version: ``int``

        :return: Unified Battery object
        :rtype: ``UnifiedBatteryInterface``
        """
        return UnifiedBatteryModel.get_main_cls(version)()
    # end def create
# end class UnifiedBatteryFactory


class UnifiedBatteryInterface(FeatureInterface, ABC):
    """
    Interface to Unified battery

    Defines required interfaces for Unified battery classes
    """
    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_status_cls = None
        self.show_battery_status_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_status_response_cls = None
        self.show_battery_status_response_cls = None

        # Events
        self.battery_status_event_cls = None
    # end def __init__
# end class UnifiedBatteryInterface


class UnifiedBatteryV0(UnifiedBatteryInterface):
    """
    Define ``UnifiedBatteryV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> supportedLevelFull, supportedLevelGood, supportedLevelLow, supportedLevelCritical,
    socCapabilityFlag, rchgCapabilityFlag

    [1] getStatus() -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus

    [Event 0] BatteryStatusEvent -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus
    """
    VERSION = 0

    def __init__(self):
        # See ``UnifiedBattery.__init__``
        super().__init__()
        index = UnifiedBatteryModel.INDEX

        # Requests
        self.get_capabilities_cls = UnifiedBatteryModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_status_cls = UnifiedBatteryModel.get_request_cls(
            self.VERSION, index.GET_STATUS)

        # Responses
        self.get_capabilities_response_cls = UnifiedBatteryModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_status_response_cls = UnifiedBatteryModel.get_response_cls(
            self.VERSION, index.GET_STATUS)

        # Events
        self.battery_status_event_cls = UnifiedBatteryModel.get_report_cls(
            self.VERSION, index.BATTERY_STATUS)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``UnifiedBatteryInterface.get_max_function_index``
        return UnifiedBatteryModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class UnifiedBatteryV0


class UnifiedBatteryV1(UnifiedBatteryV0):
    """
    Define ``UnifiedBatteryV1`` feature

    This feature provides model and unit specific information for version 1

    [0] getCapabilities() -> supportedLevelFull, supportedLevelGood, supportedLevelLow, supportedLevelCritical,
    socCapabilityFlag, rchgCapabilityFlag

    [1] getStatus() -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus

    [2] showBatteryStatus() -> None

    [Event 0] BatteryStatusEvent -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus
    """
    VERSION = 1

    def __init__(self):
        # See ``UnifiedBattery.__init__``
        super().__init__()
        index = UnifiedBatteryModel.INDEX

        # Requests
        self.show_battery_status_cls = UnifiedBatteryModel.get_request_cls(
            self.VERSION, index.SHOW_BATTERY_STATUS)

        # Responses
        self.show_battery_status_response_cls = UnifiedBatteryModel.get_response_cls(
            self.VERSION, index.SHOW_BATTERY_STATUS)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``UnifiedBatteryInterface.get_max_function_index``
        return UnifiedBatteryModel.get_base_cls().MAX_FUNCTION_INDEX_V1_TO_V5
    # end def get_max_function_index
# end class UnifiedBatteryV1


class UnifiedBatteryV2(UnifiedBatteryV1):
    """
    Define ``UnifiedBatteryV2`` feature

    This feature provides model and unit specific information for version 2

    [0] getCapabilities() -> supportedLevelFull, supportedLevelGood, supportedLevelLow, supportedLevelCritical,
    showCapabilityFlag, socCapabilityFlag, rchgCapabilityFlag

    [1] getStatus() -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus

    [2] showBatteryStatus() -> None

    [Event 0] BatteryStatusEvent -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus
    """
    VERSION = 2
# end class UnifiedBatteryV2


class UnifiedBatteryV3(UnifiedBatteryV1):
    """
    Define ``UnifiedBatteryV3`` feature

    This feature provides model and unit specific information for version 3

    [0] getCapabilities() -> supportedLevelFull, supportedLevelGood, supportedLevelLow, supportedLevelCritical,
    batterySrcIdxCapabilityFlag, showCapabilityFlag, socCapabilityFlag, rchgCapabilityFlag, batterySourceIndex

    [1] getStatus() -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus

    [2] showBatteryStatus() -> None

    [Event 0] BatteryStatusEvent -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus
    """
    VERSION = 3
# end class UnifiedBatteryV3


class UnifiedBatteryV4(UnifiedBatteryV1):
    """
    Define ``UnifiedBatteryV4`` feature

    This feature provides model and unit specific information for version 4

    [0] getCapabilities() -> supportedLevelFull, supportedLevelGood, supportedLevelLow, supportedLevelCritical,
    fastChargingCapabilityFlag, batterySrcIdxCapabilityFlag, showCapabilityFlag, socCapabilityFlag, rchgCapabilityFlag,
    batterySourceIndex

    [1] getStatus() -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus, fastChargingStatus

    [2] showBatteryStatus() -> None

    [Event 0] BatteryStatusEvent -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus, fastChargingStatus
    """
    VERSION = 4
# end class UnifiedBatteryV4


class UnifiedBatteryV5(UnifiedBatteryV1):
    """
    Define ``UnifiedBatteryV5`` feature

    This feature provides model and unit specific information for version 5

    [0] getCapabilities() -> supportedLevelFull, supportedLevelGood, supportedLevelLow, supportedLevelCritical,
    removableBatteryCapabilityFlag, fastChargingCapabilityFlag, batterySrcIdxCapabilityFlag, showCapabilityFlag,
    socCapabilityFlag, rchgCapabilityFlag, batterySourceIndex

    [1] getStatus() -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus, fastChargingStatus, removableBatteryStatus

    [2] showBatteryStatus() -> None

    [Event 0] BatteryStatusEvent -> stateOfCharge, supportedLevelFull, supportedLevelGood, supportedLevelLow,
    supportedLevelCritical, chargingStatus, externalPowerStatus, fastChargingStatus, removableBatteryStatus
    """
    VERSION = 5
# end class UnifiedBatteryV5


class GetCapabilitiesV0ToV5(UnifiedBattery):
    """
    UnifiedBattery GetCapabilities implementation class for version 0 to version 5

    Request the static capability information about the device.

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

    class FID(UnifiedBattery.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(UnifiedBattery.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = UnifiedBattery.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = GetCapabilitiesResponseV0ToV1.FUNCTION_INDEX
    # end def __init__
# end class GetCapabilitiesV0ToV5


class GetCapabilitiesResponseV0ToV1(UnifiedBattery):
    """
    UnifiedBattery GetCapabilities response implementation class for version 0 and version 1

    Returns the static capability information about the device.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Rfu1                          4
    SupportedLevelFull            1
    SupportedLevelGood            1
    SupportedLevelLow             1
    SupportedLevelCritical        1
    Rfu2                          6
    SocCapabilityFlag             1
    RchgCapabilityFlag            1
    Params                        112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilitiesV0ToV5,)
    FUNCTION_INDEX = 0
    VERSION = (0, 1,)

    class FID(UnifiedBattery.FID):
        """
        Field Identifiers
        """
        RFU_1 = 0xFA
        SUPPORTED_LEVEL_FULL = 0xF9
        SUPPORTED_LEVEL_GOOD = 0xF8
        SUPPORTED_LEVEL_LOW = 0xF7
        SUPPORTED_LEVEL_CRITICAL = 0xF6
        RFU_2 = 0xF5
        SOC_CAPABILITY_FLAG = 0xF4
        RCHG_CAPABILITY_FLAG = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(UnifiedBattery.LEN):
        """
        Field Lengths
        """
        RFU_1 = 0x04
        SUPPORTED_LEVEL_FULL = 0x01
        SUPPORTED_LEVEL_GOOD = 0x01
        SUPPORTED_LEVEL_LOW = 0x01
        SUPPORTED_LEVEL_CRITICAL = 0x01
        RFU_2 = 0x06
        SOC_CAPABILITY_FLAG = 0x01
        RCHG_CAPABILITY_FLAG = 0x01
        PADDING = 0x70
    # end class LEN

    FIELDS = UnifiedBattery.FIELDS + (
        BitField(FID.RFU_1,
                 LEN.RFU_1,
                 title='Rfu1',
                 name='rfu_1',
                 checks=(CheckHexList(LEN.RFU_1 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_1) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.SUPPORTED_LEVEL_FULL,
                 LEN.SUPPORTED_LEVEL_FULL,
                 title='SupportedLevelFull',
                 name='supported_level_full',
                 checks=(CheckHexList(LEN.SUPPORTED_LEVEL_FULL // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SUPPORTED_LEVEL_GOOD,
                 LEN.SUPPORTED_LEVEL_GOOD,
                 title='SupportedLevelGood',
                 name='supported_level_good',
                 checks=(CheckHexList(LEN.SUPPORTED_LEVEL_GOOD // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SUPPORTED_LEVEL_LOW,
                 LEN.SUPPORTED_LEVEL_LOW,
                 title='SupportedLevelLow',
                 name='supported_level_low',
                 checks=(CheckHexList(LEN.SUPPORTED_LEVEL_LOW // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SUPPORTED_LEVEL_CRITICAL,
                 LEN.SUPPORTED_LEVEL_CRITICAL,
                 title='SupportedLevelCritical',
                 name='supported_level_critical',
                 checks=(CheckHexList(LEN.SUPPORTED_LEVEL_CRITICAL // 8), CheckBool(),
                         CheckInt(min_value=0, max_value=1)), ),
        BitField(FID.RFU_2,
                 LEN.RFU_2,
                 title='Rfu2',
                 name='rfu_2',
                 checks=(CheckHexList(LEN.RFU_2 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_2) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.SOC_CAPABILITY_FLAG,
                 LEN.SOC_CAPABILITY_FLAG,
                 title='SocCapabilityFlag',
                 name='soc_capability_flag',
                 checks=(CheckHexList(LEN.SOC_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.RCHG_CAPABILITY_FLAG,
                 LEN.RCHG_CAPABILITY_FLAG,
                 title='RchgCapabilityFlag',
                 name='rchg_capability_flag',
                 checks=(CheckHexList(LEN.RCHG_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, supported_level_full=False, supported_level_good=False,
                 supported_level_low=False, supported_level_critical=False, soc_capability_flag=False,
                 rchg_capability_flag=False):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  supported_level_full: The level full is supported or not - OPTIONAL
        :type supported_level_full: ``bool | int | HexList``
        :param  supported_level_good: The level good is supported or not - OPTIONAL
        :type supported_level_good: ``bool | int | HexList``
        :param  supported_level_low: The level low is supported or not - OPTIONAL
        :type supported_level_low: ``bool | int | HexList``
        :param  supported_level_critical: The level critical is supported or not - OPTIONAL
        :type supported_level_critical: ``bool | int | HexList``
        :param  soc_capability_flag: The rechargeable capability flag - OPTIONAL
        :type soc_capability_flag: ``bool | int | HexList``
        :param  rchg_capability_flag: The state_of_charge capability flag - OPTIONAL
        :type rchg_capability_flag: ``bool | int | HexList``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.supported_level_full = supported_level_full
        self.supported_level_good = supported_level_good
        self.supported_level_low = supported_level_low
        self.supported_level_critical = supported_level_critical
        self.soc_capability_flag = soc_capability_flag
        self.rchg_capability_flag = rchg_capability_flag
    # end def __init__
# end class GetCapabilitiesResponseV0ToV1


class GetCapabilitiesResponseV2(GetCapabilitiesResponseV0ToV1):
    """
    UnifiedBattery GetCapabilities response implementation class for version 2
    Version 2: adding capability bit [show] for showBatteryStatus function support

    Returns the static capability information about the device.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Rfu1                          4
    SupportedLevelFull            1
    SupportedLevelGood            1
    SupportedLevelLow             1
    SupportedLevelCritical        1
    Rfu2                          5
    ShowCapabilityFlag            1
    SocCapabilityFlag             1
    RchgCapabilityFlag            1
    Params                        112
    ============================  ==========
    """
    VERSION = (2,)

    class FID(GetCapabilitiesResponseV0ToV1.FID):
        """
        Field Identifiers
        """
        SHOW_CAPABILITY_FLAG = 0xF4
        SOC_CAPABILITY_FLAG = 0xF3
        RCHG_CAPABILITY_FLAG = 0xF2
        PADDING = 0xF1
    # end class FID

    class LEN(GetCapabilitiesResponseV0ToV1.LEN):
        """
        Field Lengths
        """
        RFU_2 = 0x05
        SHOW_CAPABILITY_FLAG = 0x01
    # end class LEN

    FIELDS = GetCapabilitiesResponseV0ToV1.FIELDS[:-4] + (  # Remove the flags and padding fields of the parent class
        BitField(FID.RFU_2,
                 LEN.RFU_2,
                 title='Rfu2',
                 name='rfu_2',
                 checks=(CheckHexList(LEN.RFU_2 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_2) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.SHOW_CAPABILITY_FLAG,
                 LEN.SHOW_CAPABILITY_FLAG,
                 title='ShowCapabilityFlag',
                 name='show_capability_flag',
                 checks=(CheckHexList(LEN.SHOW_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SOC_CAPABILITY_FLAG,
                 LEN.SOC_CAPABILITY_FLAG,
                 title='SocCapabilityFlag',
                 name='soc_capability_flag',
                 checks=(CheckHexList(LEN.SOC_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.RCHG_CAPABILITY_FLAG,
                 LEN.RCHG_CAPABILITY_FLAG,
                 title='RchgCapabilityFlag',
                 name='rchg_capability_flag',
                 checks=(CheckHexList(LEN.RCHG_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, supported_level_full=False, supported_level_good=False,
                 supported_level_low=False, supported_level_critical=False, show_capability_flag=False,
                 soc_capability_flag=False, rchg_capability_flag=False):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  supported_level_full: The level full is supported or not - OPTIONAL
        :type supported_level_full: ``bool | int | HexList``
        :param  supported_level_good: The level good is supported or not - OPTIONAL
        :type supported_level_good: ``bool | int | HexList``
        :param  supported_level_low: The level low is supported or not - OPTIONAL
        :type supported_level_low: ``bool | int | HexList``
        :param  supported_level_critical: The level critical is supported or not - OPTIONAL
        :type supported_level_critical: ``bool | int | HexList``
        :param  show_capability_flag: The show battery status capability flag - OPTIONAL
        :type show_capability_flag: ``bool | int | HexList``
        :param  soc_capability_flag: The rechargeable capability flag - OPTIONAL
        :type soc_capability_flag: ``bool | int | HexList``
        :param  rchg_capability_flag: The state_of_charge capability flag - OPTIONAL
        :type rchg_capability_flag: ``bool | int | HexList``
        """
        super().__init__(device_index, feature_index, supported_level_full, supported_level_good,
                         supported_level_low, supported_level_critical, soc_capability_flag, rchg_capability_flag)

        self.show_capability_flag = show_capability_flag
    # end def __init__
# end class GetCapabilitiesResponseV2


class GetCapabilitiesResponseV3(GetCapabilitiesResponseV2):
    """
    UnifiedBattery GetCapabilities response implementation class for version 3
    Version 3: adding capability for multi-sourcing battery support

    Returns the static capability information about the device.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Rfu1                          4
    SupportedLevelFull            1
    SupportedLevelGood            1
    SupportedLevelLow             1
    SupportedLevelCritical        1
    Rfu2                          4
    BatterySrcIdxCapabilityFlag   1
    ShowCapabilityFlag            1
    SocCapabilityFlag             1
    RchgCapabilityFlag            1
    BatterySourceIndex            8
    Padding                       104
    ============================  ==========
    """
    VERSION = (3,)

    class FID(GetCapabilitiesResponseV2.FID):
        """
        Field Identifiers
        """
        BATTERY_SRC_IDX_CAPABILITY_FLAG = 0xF4
        SHOW_CAPABILITY_FLAG = 0xF3
        SOC_CAPABILITY_FLAG = 0xF2
        RCHG_CAPABILITY_FLAG = 0xF1
        BATTERY_SOURCE_INDEX = 0xF0
        PADDING = 0xEF
    # end class FID

    class LEN(GetCapabilitiesResponseV2.LEN):
        """
        Field Lengths
        """
        RFU_2 = 0x04
        BATTERY_SRC_IDX_CAPABILITY_FLAG = 0x01
        BATTERY_SOURCE_INDEX = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = GetCapabilitiesResponseV2.FIELDS[:-5] + (  # Remove the flags and padding fields of the parent class
        BitField(FID.RFU_2,
                 LEN.RFU_2,
                 title='Rfu2',
                 name='rfu_2',
                 checks=(CheckHexList(LEN.RFU_2 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_2) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.BATTERY_SRC_IDX_CAPABILITY_FLAG,
                 LEN.BATTERY_SRC_IDX_CAPABILITY_FLAG,
                 title='BatterySrcIdxCapabilityFlag',
                 name='battery_src_idx_capability_flag',
                 checks=(CheckHexList(LEN.BATTERY_SRC_IDX_CAPABILITY_FLAG // 8),
                         CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SHOW_CAPABILITY_FLAG,
                 LEN.SHOW_CAPABILITY_FLAG,
                 title='ShowCapabilityFlag',
                 name='show_capability_flag',
                 checks=(CheckHexList(LEN.SHOW_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SOC_CAPABILITY_FLAG,
                 LEN.SOC_CAPABILITY_FLAG,
                 title='SocCapabilityFlag',
                 name='soc_capability_flag',
                 checks=(CheckHexList(LEN.SOC_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.RCHG_CAPABILITY_FLAG,
                 LEN.RCHG_CAPABILITY_FLAG,
                 title='RchgCapabilityFlag',
                 name='rchg_capability_flag',
                 checks=(CheckHexList(LEN.RCHG_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.BATTERY_SOURCE_INDEX,
                 LEN.BATTERY_SOURCE_INDEX,
                 title='BatterySourceIndex',
                 name='battery_source_index',
                 checks=(CheckHexList(LEN.BATTERY_SOURCE_INDEX // 8), CheckByte()),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, supported_level_full=False, supported_level_good=False,
                 supported_level_low=False, supported_level_critical=False,
                 battery_src_idx_capability_flag=False, show_capability_flag=False,
                 soc_capability_flag=False, rchg_capability_flag=False, battery_source_index=0):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  supported_level_full: The level full is supported or not - OPTIONAL
        :type supported_level_full: ``bool | int | HexList``
        :param  supported_level_good: The level good is supported or not - OPTIONAL
        :type supported_level_good: ``bool | int | HexList``
        :param  supported_level_low: The level low is supported or not - OPTIONAL
        :type supported_level_low: ``bool | int | HexList``
        :param  supported_level_critical: The level critical is supported or not - OPTIONAL
        :type supported_level_critical: ``bool | int | HexList``
        :param  battery_src_idx_capability_flag: Ability of the device to provide its battery source index - OPTIONAL
        :type battery_src_idx_capability_flag: ``bool | int | HexList``
        :param  show_capability_flag: The show battery status capability flag - OPTIONAL
        :type show_capability_flag: ``bool | int | HexList``
        :param  soc_capability_flag: The rechargeable capability flag - OPTIONAL
        :type soc_capability_flag: ``bool | int | HexList``
        :param  rchg_capability_flag: The state_of_charge capability flag - OPTIONAL
        :type rchg_capability_flag: ``bool | int | HexList``
        :param  battery_source_index: Identifies the battery used in case of battery multi-sourcing support - OPTIONAL
        :type battery_source_index: ``int | HexList``
        """
        super().__init__(device_index, feature_index, supported_level_full, supported_level_good,
                         supported_level_low, supported_level_critical, show_capability_flag, soc_capability_flag,
                         rchg_capability_flag)

        self.battery_src_idx_capability_flag = battery_src_idx_capability_flag
        self.battery_source_index = battery_source_index
    # end def __init__
# end class GetCapabilitiesResponseV3


class GetCapabilitiesResponseV4(GetCapabilitiesResponseV3):
    """
    UnifiedBattery GetCapabilities response implementation class for version 4
    Version 4: adding capability for fast charging

    Returns the static capability information about the device.

    Format:
    =================================  ==========
    Name                               Bit count
    =================================  ==========
    ReportID                           8
    DeviceIndex                        8
    FeatureIndex                       8
    FunctionID                         4
    SoftwareID                         4
    Rfu1                               4
    SupportedLevelFull                 1
    SupportedLevelGood                 1
    SupportedLevelLow                  1
    SupportedLevelCritical             1
    Rfu2                               3
    FastChargingCapabilityFlag         1
    BatterySrcIdxCapabilityFlag        1
    ShowCapabilityFlag                 1
    SocCapabilityFlag                  1
    RchgCapabilityFlag                 1
    BatterySourceIndex                 8
    Padding                            104
    =================================  ==========
    """
    VERSION = (4,)

    class FID(GetCapabilitiesResponseV3.FID):
        """
        Field Identifiers
        """
        FAST_CHARGING_CAPABILITY_FLAG = 0xF4
        BATTERY_SRC_IDX_CAPABILITY_FLAG = 0xF3
        SHOW_CAPABILITY_FLAG = 0xF2
        SOC_CAPABILITY_FLAG = 0xF1
        RCHG_CAPABILITY_FLAG = 0xF0
        BATTERY_SOURCE_INDEX = 0xEF
        PADDING = 0xEE
    # end class FID

    class LEN(GetCapabilitiesResponseV3.LEN):
        """
        Field Lengths
        """
        RFU_2 = 0x03
        FAST_CHARGING_CAPABILITY_FLAG = 0x1
    # end class LEN

    FIELDS = GetCapabilitiesResponseV2.FIELDS[:-5] + (  # Remove the flags and padding fields of the parent class
        BitField(FID.RFU_2,
                 LEN.RFU_2,
                 title='Rfu2',
                 name='rfu_2',
                 checks=(CheckHexList(LEN.RFU_2 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_2) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.FAST_CHARGING_CAPABILITY_FLAG,
                 LEN.FAST_CHARGING_CAPABILITY_FLAG,
                 title="FastChargingCapabilityFlag",
                 name="fast_charging_capability_flag",
                 checks=(CheckHexList(LEN.FAST_CHARGING_CAPABILITY_FLAG // 8), CheckBool(),
                         CheckInt(min_value=0, max_value=1))),
        BitField(FID.BATTERY_SRC_IDX_CAPABILITY_FLAG,
                 LEN.BATTERY_SRC_IDX_CAPABILITY_FLAG,
                 title='BatterySrcIdxCapabilityFlag',
                 name='battery_src_idx_capability_flag',
                 checks=(CheckHexList(LEN.BATTERY_SRC_IDX_CAPABILITY_FLAG // 8),
                         CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SHOW_CAPABILITY_FLAG,
                 LEN.SHOW_CAPABILITY_FLAG,
                 title='ShowCapabilityFlag',
                 name='show_capability_flag',
                 checks=(CheckHexList(LEN.SHOW_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SOC_CAPABILITY_FLAG,
                 LEN.SOC_CAPABILITY_FLAG,
                 title='SocCapabilityFlag',
                 name='soc_capability_flag',
                 checks=(CheckHexList(LEN.SOC_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.RCHG_CAPABILITY_FLAG,
                 LEN.RCHG_CAPABILITY_FLAG,
                 title='RchgCapabilityFlag',
                 name='rchg_capability_flag',
                 checks=(CheckHexList(LEN.RCHG_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.BATTERY_SOURCE_INDEX,
                 LEN.BATTERY_SOURCE_INDEX,
                 title='BatterySourceIndex',
                 name='battery_source_index',
                 checks=(CheckHexList(LEN.BATTERY_SOURCE_INDEX // 8), CheckByte()),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, supported_level_full=False, supported_level_good=False,
                 supported_level_low=False, supported_level_critical=False, fast_charging_capability_flag=False,
                 battery_src_idx_capability_flag=False, show_capability_flag=False, soc_capability_flag=False,
                 rchg_capability_flag=False, battery_source_index=0):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  supported_level_full: The level full is supported or not - OPTIONAL
        :type supported_level_full: ``bool | int | HexList``
        :param  supported_level_good: The level good is supported or not - OPTIONAL
        :type supported_level_good: ``bool | int | HexList``
        :param  supported_level_low: The level low is supported or not - OPTIONAL
        :type supported_level_low: ``bool | int | HexList``
        :param  supported_level_critical: The level critical is supported or not - OPTIONAL
        :type supported_level_critical: ``bool | int | HexList``
        :param fast_charging_capability_flag: Fast Charging Capability Flag - OPTIONAL
        :type fast_charging_capability_flag: ``bool | int | HexList``
        :param  battery_src_idx_capability_flag: Ability of the device to provide its battery source index - OPTIONAL
        :type battery_src_idx_capability_flag: ``bool | int | HexList``
        :param  show_capability_flag: The show battery status capability flag - OPTIONAL
        :type show_capability_flag: ``bool | int | HexList``
        :param  soc_capability_flag: The rechargeable capability flag - OPTIONAL
        :type soc_capability_flag: ``bool | int | HexList``
        :param  rchg_capability_flag: The state_of_charge capability flag - OPTIONAL
        :type rchg_capability_flag: ``bool | int | HexList``
        :param  battery_source_index: Identifies the battery used in case of battery multi-sourcing support - OPTIONAL
        :type battery_source_index: ``int | HexList``
        """
        super().__init__(device_index, feature_index, supported_level_full, supported_level_good,
                         supported_level_low, supported_level_critical, battery_src_idx_capability_flag,
                         show_capability_flag, soc_capability_flag, rchg_capability_flag, battery_source_index)
        self.fast_charging_capability_flag = fast_charging_capability_flag
    # end def __init__
# end class GetCapabilitiesResponseV4


class GetCapabilitiesResponseV5(GetCapabilitiesResponseV4):
    """
    UnifiedBattery GetCapabilities response implementation class for version 4
    Version 4: adding capability for fast charging

    Returns the static capability information about the device.

    Format:
    =================================  ==========
    Name                               Bit count
    =================================  ==========
    ReportID                           8
    DeviceIndex                        8
    FeatureIndex                       8
    FunctionID                         4
    SoftwareID                         4
    Rfu1                               4
    SupportedLevelFull                 1
    SupportedLevelGood                 1
    SupportedLevelLow                  1
    SupportedLevelCritical             1
    Rfu2                               2
    RemovableBatteryCapabilityFlag     1
    FastChargingCapabilityFlag         1
    BatterySrcIdxCapabilityFlag        1
    ShowCapabilityFlag                 1
    SocCapabilityFlag                  1
    RchgCapabilityFlag                 1
    BatterySourceIndex                 8
    Padding                            104
    =================================  ==========
    """
    VERSION = (5,)

    class FID(GetCapabilitiesResponseV4.FID):
        """
        Field Identifiers
        """
        REMOVABLE_BATTERY_CAPABILITY_FLAG = 0xF4
        FAST_CHARGING_CAPABILITY_FLAG = 0xF3
        BATTERY_SRC_IDX_CAPABILITY_FLAG = 0xF2
        SHOW_CAPABILITY_FLAG = 0xF1
        SOC_CAPABILITY_FLAG = 0xF0
        RCHG_CAPABILITY_FLAG = 0xEF
        BATTERY_SOURCE_INDEX = 0xEE
        PADDING = 0xED
    # end class FID

    class LEN(GetCapabilitiesResponseV4.LEN):
        """
        Field Lengths
        """
        RFU_2 = 0x02
        REMOVABLE_BATTERY_CAPABILITY_FLAG = 0x1
    # end class LEN

    FIELDS = GetCapabilitiesResponseV2.FIELDS[:-5] + (  # Remove the flags and padding fields of the parent class
        BitField(FID.RFU_2,
                 LEN.RFU_2,
                 title='Rfu2',
                 name='rfu_2',
                 checks=(CheckHexList(LEN.RFU_2 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_2) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.REMOVABLE_BATTERY_CAPABILITY_FLAG,
                 LEN.REMOVABLE_BATTERY_CAPABILITY_FLAG,
                 title="RemovableBatteryCapabilityFlag",
                 name="removable_battery_capability_flag",
                 checks=(CheckHexList(LEN.REMOVABLE_BATTERY_CAPABILITY_FLAG // 8), CheckBool(),
                         CheckInt(min_value=0, max_value=1))),
        BitField(FID.FAST_CHARGING_CAPABILITY_FLAG,
                 LEN.FAST_CHARGING_CAPABILITY_FLAG,
                 title="FastChargingCapabilityFlag",
                 name="fast_charging_capability_flag",
                 checks=(CheckHexList(LEN.FAST_CHARGING_CAPABILITY_FLAG // 8), CheckBool(),
                         CheckInt(min_value=0, max_value=1))),
        BitField(FID.BATTERY_SRC_IDX_CAPABILITY_FLAG,
                 LEN.BATTERY_SRC_IDX_CAPABILITY_FLAG,
                 title='BatterySrcIdxCapabilityFlag',
                 name='battery_src_idx_capability_flag',
                 checks=(CheckHexList(LEN.BATTERY_SRC_IDX_CAPABILITY_FLAG // 8),
                         CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SHOW_CAPABILITY_FLAG,
                 LEN.SHOW_CAPABILITY_FLAG,
                 title='ShowCapabilityFlag',
                 name='show_capability_flag',
                 checks=(CheckHexList(LEN.SHOW_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.SOC_CAPABILITY_FLAG,
                 LEN.SOC_CAPABILITY_FLAG,
                 title='SocCapabilityFlag',
                 name='soc_capability_flag',
                 checks=(CheckHexList(LEN.SOC_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.RCHG_CAPABILITY_FLAG,
                 LEN.RCHG_CAPABILITY_FLAG,
                 title='RchgCapabilityFlag',
                 name='rchg_capability_flag',
                 checks=(CheckHexList(LEN.RCHG_CAPABILITY_FLAG // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.BATTERY_SOURCE_INDEX,
                 LEN.BATTERY_SOURCE_INDEX,
                 title='BatterySourceIndex',
                 name='battery_source_index',
                 checks=(CheckHexList(LEN.BATTERY_SOURCE_INDEX // 8), CheckByte()),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, supported_level_full=False, supported_level_good=False,
                 supported_level_low=False, supported_level_critical=False, removable_battery_capability_flag=False,
                 fast_charging_capability_flag=False, battery_src_idx_capability_flag=False, show_capability_flag=False,
                 soc_capability_flag=False, rchg_capability_flag=False, battery_source_index=0):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  supported_level_full: The level full is supported or not - OPTIONAL
        :type supported_level_full: ``bool | int | HexList``
        :param  supported_level_good: The level good is supported or not - OPTIONAL
        :type supported_level_good: ``bool | int | HexList``
        :param  supported_level_low: The level low is supported or not - OPTIONAL
        :type supported_level_low: ``bool | int | HexList``
        :param  supported_level_critical: The level critical is supported or not - OPTIONAL
        :type supported_level_critical: ``bool | int | HexList``
        :param removable_battery_capability_flag: Removable Battery Capability Flag - OPTIONAL
        :type removable_battery_capability_flag: ``bool | int | HexList``
        :param fast_charging_capability_flag: Fast Charging Capability Flag - OPTIONAL
        :type fast_charging_capability_flag: ``bool | int | HexList``
        :param  battery_src_idx_capability_flag: Ability of the device to provide its battery source index - OPTIONAL
        :type battery_src_idx_capability_flag: ``bool | int | HexList``
        :param  show_capability_flag: The show battery status capability flag - OPTIONAL
        :type show_capability_flag: ``bool | int | HexList``
        :param  soc_capability_flag: The rechargeable capability flag - OPTIONAL
        :type soc_capability_flag: ``bool | int | HexList``
        :param  rchg_capability_flag: The state_of_charge capability flag - OPTIONAL
        :type rchg_capability_flag: ``bool | int | HexList``
        :param  battery_source_index: Identifies the battery used in case of battery multi-sourcing support - OPTIONAL
        :type battery_source_index: ``int | HexList``
        """
        super().__init__(device_index, feature_index, supported_level_full, supported_level_good,
                         supported_level_low, supported_level_critical, fast_charging_capability_flag,
                         battery_src_idx_capability_flag, show_capability_flag, soc_capability_flag,
                         rchg_capability_flag, battery_source_index)
        self.removable_battery_capability_flag = removable_battery_capability_flag
    # end def __init__
# end class GetCapabilitiesResponseV5


class GetStatusV0ToV5(UnifiedBattery):
    """
    UnifiedBattery GetStatus implementation class for version 0

    Returns the battery status of the device.

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

    class FID(UnifiedBattery.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(UnifiedBattery.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = UnifiedBattery.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = GetStatusResponseV0ToV3.FUNCTION_INDEX
    # end def __init__
# end class GetStatusV0ToV3


class _GetStatusResponseEventV0ToV3(UnifiedBattery):
    """
    UnifiedBattery GetStatus response and event base implementation class for version 0 to version 3

    Returns the device battery status.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    StateOfCharge                 8
    Rfu1                          4
    BatteryLevelFull              1
    BatteryLevelGood              1
    BatteryLevelLow               1
    BatteryLevelCritical          1
    ChargingStatus                8
    ExternalPowerStatus           8
    Params                        96
    ============================  ==========
    """
    VERSION = (0, 1, 2, 3, )

    class FID(UnifiedBattery.FID):
        """
        Field Identifiers
        """
        STATE_OF_CHARGE = 0xFA
        RFU_1 = 0xF9
        BATTERY_LEVEL_FULL = 0xF8
        BATTERY_LEVEL_GOOD = 0xF7
        BATTERY_LEVEL_LOW = 0xF6
        BATTERY_LEVEL_CRITICAL = 0xF5
        CHARGING_STATUS = 0xF4
        EXTERNAL_POWER_STATUS = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(UnifiedBattery.LEN):
        """
        Field Lengths
        """
        STATE_OF_CHARGE = 0x08
        RFU_1 = 0x04
        BATTERY_LEVEL_FULL = 0x01
        BATTERY_LEVEL_GOOD = 0x01
        BATTERY_LEVEL_LOW = 0x01
        BATTERY_LEVEL_CRITICAL = 0x01
        CHARGING_STATUS = 0x08
        EXTERNAL_POWER_STATUS = 0x08
        PADDING = 0x60
    # end class LEN

    FIELDS = UnifiedBattery.FIELDS + (
        BitField(FID.STATE_OF_CHARGE,
                 LEN.STATE_OF_CHARGE,
                 0x00,
                 0x00,
                 title='StateOfCharge',
                 name='state_of_charge',
                 checks=(CheckHexList(LEN.STATE_OF_CHARGE // 8), CheckByte())),
        BitField(FID.RFU_1,
                 LEN.RFU_1,
                 0x00,
                 0x00,
                 title='Rfu1',
                 name='rfu_1',
                 checks=(CheckHexList(LEN.RFU_1 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_1) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.BATTERY_LEVEL_FULL,
                 LEN.BATTERY_LEVEL_FULL,
                 0x00,
                 0x00,
                 title='BatteryLevelFull',
                 name='battery_level_full',
                 checks=(CheckHexList(LEN.BATTERY_LEVEL_FULL // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.BATTERY_LEVEL_GOOD,
                 LEN.BATTERY_LEVEL_GOOD,
                 0x00,
                 0x00,
                 title='BatteryLevelGood',
                 name='battery_level_good',
                 checks=(CheckHexList(LEN.BATTERY_LEVEL_GOOD // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.BATTERY_LEVEL_LOW,
                 LEN.BATTERY_LEVEL_LOW,
                 0x00,
                 0x00,
                 title='BatteryLevelLow',
                 name='battery_level_low',
                 checks=(CheckHexList(LEN.BATTERY_LEVEL_LOW // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(FID.BATTERY_LEVEL_CRITICAL,
                 LEN.BATTERY_LEVEL_CRITICAL,
                 0x00,
                 0x00,
                 title='BatteryLevelCritical',
                 name='battery_level_critical',
                 checks=(CheckHexList(LEN.BATTERY_LEVEL_CRITICAL // 8), CheckBool(),
                         CheckInt(min_value=0, max_value=1))),
        BitField(FID.CHARGING_STATUS,
                 LEN.CHARGING_STATUS,
                 0x00,
                 0x00,
                 title='ChargingStatus',
                 name='charging_status',
                 checks=(CheckHexList(LEN.CHARGING_STATUS // 8), CheckByte())),
        BitField(FID.EXTERNAL_POWER_STATUS,
                 LEN.EXTERNAL_POWER_STATUS,
                 0x00,
                 0x00,
                 title='ExternalPowerStatus',
                 name='external_power_status',
                 checks=(CheckHexList(LEN.EXTERNAL_POWER_STATUS // 8), CheckByte())),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte()),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                 battery_level_low, battery_level_critical, charging_status, external_power_status):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  state_of_charge: The soc is an indicator of the amount of energy available in the battery (in %).
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full.
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good.
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low.
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical.
        :type battery_level_critical: ``bool | int | HexList``
        :param  charging_status: The charging status of the device.
        :type charging_status: ``int | HexList``
        :param  external_power_status: The power source reported by the device
        :type external_power_status: ``int | HexList``
        """
        super().__init__(device_index, feature_index)

        self.state_of_charge = state_of_charge
        self.battery_level_full = battery_level_full
        self.battery_level_good = battery_level_good
        self.battery_level_low = battery_level_low
        self.battery_level_critical = battery_level_critical
        self.charging_status = charging_status
        self.external_power_status = external_power_status
    # end def __init__
# end class _GetStatusResponseEventV0ToV3


class _GetStatusResponseEventV4(_GetStatusResponseEventV0ToV3):
    """
    UnifiedBattery GetStatus response and event base implementation class for version 4

    Returns the device battery status.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    StateOfCharge                 8
    Rfu1                          4
    BatteryLevelFull              1
    BatteryLevelGood              1
    BatteryLevelLow               1
    BatteryLevelCritical          1
    ChargingStatus                8
    ExternalPowerStatus           8
    Rfu2                          7
    FastChargingStatus            1
    Params                        88
    ============================  ==========
    """
    VERSION = (4,)

    class FID(_GetStatusResponseEventV0ToV3.FID):
        """
        Field Identifiers
        """
        RFU_2 = 0xF2
        FAST_CHARGING_STATUS = 0xF1
        PADDING = 0xF0
    # end class FID

    class LEN(_GetStatusResponseEventV0ToV3.LEN):
        """
        Field Lengths
        """
        RFU_2 = 0x07
        FAST_CHARGING_STATUS = 0x01
        PADDING = 0x58
    # end class LEN

    FIELDS = _GetStatusResponseEventV0ToV3.FIELDS[:-1] + (
        BitField(fid=FID.RFU_2,
                 length=LEN.RFU_2,
                 title="Rfu2",
                 name="rfu_2",
                 checks=(CheckHexList(LEN.RFU_2 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_2) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(fid=FID.FAST_CHARGING_STATUS,
                 length=LEN.FAST_CHARGING_STATUS,
                 title="FastChargingStatus",
                 name="fast_charging_status",
                 checks=(CheckHexList(LEN.FAST_CHARGING_STATUS // 8), CheckBool(), CheckInt(min_value=0, max_value=1))),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                 battery_level_low, battery_level_critical, charging_status, external_power_status,
                 fast_charging_status):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  state_of_charge: The soc is an indicator of the amount of energy available in the battery (in %).
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full.
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good.
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low.
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical.
        :type battery_level_critical: ``bool | int | HexList``
        :param  charging_status: The charging status of the device.
        :type charging_status: ``int | HexList``
        :param  external_power_status: The power source reported by the device
        :type external_power_status: ``int | HexList``
        :param fast_charging_status: Fast Charging Status
        :type fast_charging_status: ``bool | HexList``
        """
        super().__init__(device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                         battery_level_low, battery_level_critical, charging_status, external_power_status)

        self.fast_charging_status = fast_charging_status
    # end def __init__
# end class _GetStatusResponseEventV4


class _GetStatusResponseEventV5(_GetStatusResponseEventV4):
    """
    UnifiedBattery GetStatus response and event base implementation class  for version 5

    Returns the device battery status.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    StateOfCharge                 8
    Rfu1                          4
    BatteryLevelFull              1
    BatteryLevelGood              1
    BatteryLevelLow               1
    BatteryLevelCritical          1
    ChargingStatus                8
    ExternalPowerStatus           8
    Rfu2                          7
    FastChargingStatus            1
    Rfu3                          7
    RemovableBatteryStatus        1
    Params                        80
    ============================  ==========
    """
    VERSION = (5,)

    class FID(_GetStatusResponseEventV4.FID):
        """
        Field Identifiers
        """
        RFU_3 = 0xF0
        REMOVABLE_BATTERY_STATUS = 0xEF
        PADDING = 0xEE
    # end class FID

    class LEN(_GetStatusResponseEventV4.LEN):
        """
        Field Lengths
        """
        RFU_3 = 0x07
        REMOVABLE_BATTERY_STATUS = 0x01
        PADDING = 0x50
    # end class LEN

    FIELDS = _GetStatusResponseEventV4.FIELDS[:-1] + (
        BitField(fid=FID.RFU_3,
                 length=LEN.RFU_3,
                 title="Rfu3",
                 name="rfu_3",
                 checks=(CheckHexList(LEN.RFU_3 // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU_3) - 1)),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(fid=FID.REMOVABLE_BATTERY_STATUS,
                 length=LEN.REMOVABLE_BATTERY_STATUS,
                 title="RemovableBatteryStatus",
                 name="removable_battery_status",
                 checks=(CheckHexList(LEN.REMOVABLE_BATTERY_STATUS // 8), CheckBool(),
                         CheckInt(min_value=0, max_value=1))),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=UnifiedBattery.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                 battery_level_low, battery_level_critical, charging_status, external_power_status,
                 fast_charging_status, removable_battery_status):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  state_of_charge: The soc is an indicator of the amount of energy available in the battery (in %).
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full.
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good.
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low.
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical.
        :type battery_level_critical: ``bool | int | HexList``
        :param  charging_status: The charging status of the device.
        :type charging_status: ``int | HexList``
        :param  external_power_status: The power source reported by the device
        :type external_power_status: ``int | HexList``
        :param fast_charging_status: Fast Charging Status
        :type fast_charging_status: ``bool | HexList``
        :param removable_battery_status: Removable Battery Status
        :type removable_battery_status: ``bool | HexList``
        """
        super().__init__(device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                         battery_level_low, battery_level_critical, charging_status, external_power_status,
                         fast_charging_status)

        self.removable_battery_status = removable_battery_status
    # end def __init__
# end class _GetStatusResponseEventV5


class GetStatusResponseV0ToV3(_GetStatusResponseEventV0ToV3):
    """
    See ``_GetStatusResponseEventV0ToV3``
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetStatusV0ToV5,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, state_of_charge=0, battery_level_full=False,
                 battery_level_good=False, battery_level_low=False, battery_level_critical=False, charging_status=0,
                 external_power_status=0):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  state_of_charge: The indicator of the amount of energy available in the battery in % - OPTIONAL
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full - OPTIONAL
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good - OPTIONAL
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low - OPTIONAL
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical - OPTIONAL
        :type battery_level_critical: ``bool | int | HexList``
        :param  charging_status: The charging status of the device - OPTIONAL
        :type charging_status: ``int | HexList``
        :param  external_power_status: The power source reported by the device - OPTIONAL
        :type external_power_status: ``int | HexList``
        """
        super().__init__(device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                         battery_level_low, battery_level_critical, charging_status, external_power_status)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class GetStatusResponseV0ToV3


class GetStatusResponseV4(_GetStatusResponseEventV4):
    """
    See ``_GetStatusResponseEventV4``
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetStatusV0ToV5,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, state_of_charge=0, battery_level_full=False,
                 battery_level_good=False, battery_level_low=False, battery_level_critical=False, charging_status=0,
                 external_power_status=0, fast_charging_status=False):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param state_of_charge: State Of Charge - OPTIONAL
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full - OPTIONAL
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good - OPTIONAL
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low - OPTIONAL
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical - OPTIONAL
        :type battery_level_critical: ``bool | int | HexList``
        :param charging_status: Charging Status - OPTIONAL
        :type charging_status: ``int | HexList``
        :param external_power_status: External Power Status - OPTIONAL
        :type external_power_status: ``int | HexList``
        :param fast_charging_status: Fast Charging Status - OPTIONAL
        :type fast_charging_status: ``bool | HexList``
        """
        super().__init__(device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                         battery_level_low, battery_level_critical, charging_status, external_power_status,
                         fast_charging_status)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class GetStatusResponseV4


class GetStatusResponseV5(_GetStatusResponseEventV5):
    """
    See ``_GetStatusResponseEventV5``
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetStatusV0ToV5,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, state_of_charge=0, battery_level_full=False,
                 battery_level_good=False, battery_level_low=False, battery_level_critical=False, charging_status=0,
                 external_power_status=0, fast_charging_status=False, removable_battery_status=False):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param state_of_charge: State Of Charge - OPTIONAL
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full - OPTIONAL
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good - OPTIONAL
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low - OPTIONAL
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical - OPTIONAL
        :type battery_level_critical: ``bool | int | HexList``
        :param charging_status: Charging Status - OPTIONAL
        :type charging_status: ``int | HexList``
        :param external_power_status: External Power Status - OPTIONAL
        :type external_power_status: ``int | HexList``
        :param fast_charging_status: Fast Charging Status - OPTIONAL
        :type fast_charging_status: ``bool | HexList``
        :param removable_battery_status: Removable Battery Status - OPTIONAL
        :type removable_battery_status: ``bool | HexList``
        """
        super().__init__(device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                         battery_level_low, battery_level_critical, charging_status, external_power_status,
                         fast_charging_status, removable_battery_status)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class GetStatusResponseV5


class ShowBatteryStatusV1ToV5(GetStatusV0ToV5):
    """
    UnifiedBattery ShowBatteryStatus implementation class for versions 1 & 2

    Upon reception of this command, the device displays the battery status information as at power-on.

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

    def __init__(self, device_index, feature_index):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = ShowBatteryStatusResponseV1ToV5.FUNCTION_INDEX
    # end def __init__
# end class ShowBatteryStatusV1ToV5


class ShowBatteryStatusResponseV1ToV5(UnifiedBattery):
    """
    UnifiedBattery ShowBatteryStatus response implementation class for versions 1 to 5

    Upon reception of this command, the device displays the battery status information as at power-on.

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
    REQUEST_LIST = (ShowBatteryStatusV1ToV5,)
    FUNCTION_INDEX = 2
    VERSION = (1, 2, 3, 4, 5,)

    class FID(UnifiedBattery.FID):
        """
        Field identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(UnifiedBattery.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = UnifiedBattery.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=UnifiedBattery.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        """
        super().__init__(device_index, feature_index)

        self.reportId = self.DEFAULT.REPORT_ID_LONG
        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class ShowBatteryStatusResponseV2


class BatteryStatusEventV0ToV3(_GetStatusResponseEventV0ToV3):
    """
    See ``_GetStatusResponseEventV0ToV3``
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, state_of_charge=0, battery_level_full=False,
                 battery_level_good=False, battery_level_low=False, battery_level_critical=False, charging_status=0,
                 external_power_status=0):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  state_of_charge: The indicator of the amount of energy available in the battery in % - OPTIONAL
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full - OPTIONAL
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good - OPTIONAL
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low - OPTIONAL
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical - OPTIONAL
        :type battery_level_critical: ``bool | int | HexList``
        :param  charging_status: The charging status of the device - OPTIONAL
        :type charging_status: ``int | HexList``
        :param  external_power_status: The power source reported by the device - OPTIONAL
        :type external_power_status: ``int | HexList``
        """
        super().__init__(device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                         battery_level_low, battery_level_critical, charging_status, external_power_status)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class BatteryStatusEventV0ToV3


class BatteryStatusEventV4(_GetStatusResponseEventV4):
    """
    See ``_GetStatusResponseEventV4``
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, state_of_charge=0, battery_level_full=False,
                 battery_level_good=False, battery_level_low=False, battery_level_critical=False, charging_status=0,
                 external_power_status=0, fast_charging_status=False):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  state_of_charge: The indicator of the amount of energy available in the battery in % - OPTIONAL
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full - OPTIONAL
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good - OPTIONAL
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low - OPTIONAL
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical - OPTIONAL
        :type battery_level_critical: ``bool | int | HexList``
        :param  charging_status: The charging status of the device - OPTIONAL
        :type charging_status: ``int | HexList``
        :param  external_power_status: The power source reported by the device - OPTIONAL
        :type external_power_status: ``int | HexList``
        """
        super().__init__(device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                         battery_level_low, battery_level_critical, charging_status, external_power_status,
                         fast_charging_status)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class BatteryStatusEventV4


class BatteryStatusEventV5(_GetStatusResponseEventV5):
    """
    See ``_GetStatusResponseEventV5``
    """
    MSG_TYPE = TYPE.EVENT
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, state_of_charge=0, battery_level_full=False,
                 battery_level_good=False, battery_level_low=False, battery_level_critical=False, charging_status=0,
                 external_power_status=0, fast_charging_status=False, removable_battery_status=False):
        """
        :param  device_index: Device Index
        :type device_index: ``int | HexList``
        :param  feature_index: Desired feature Id
        :type feature_index: ``int | HexList``
        :param  state_of_charge: The indicator of the amount of energy available in the battery in % - OPTIONAL
        :type state_of_charge: ``int | HexList``
        :param  battery_level_full: The Battery level is full - OPTIONAL
        :type battery_level_full: ``bool | int | HexList``
        :param  battery_level_good: The Battery level is good - OPTIONAL
        :type battery_level_good: ``bool | int | HexList``
        :param  battery_level_low: The Battery level is low - OPTIONAL
        :type battery_level_low: ``bool | int | HexList``
        :param  battery_level_critical: The Battery level is critical - OPTIONAL
        :type battery_level_critical: ``bool | int | HexList``
        :param  charging_status: The charging status of the device - OPTIONAL
        :type charging_status: ``int | HexList``
        :param  external_power_status: The power source reported by the device - OPTIONAL
        :type external_power_status: ``int | HexList``
        :param removable_battery_status: Removable Battery Status
        :type removable_battery_status: ``bool | HexList`` - OPTIONAL
        """
        super().__init__(device_index, feature_index, state_of_charge, battery_level_full, battery_level_good,
                         battery_level_low, battery_level_critical, charging_status, external_power_status,
                         fast_charging_status, removable_battery_status)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class BatteryStatusEventV5


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
