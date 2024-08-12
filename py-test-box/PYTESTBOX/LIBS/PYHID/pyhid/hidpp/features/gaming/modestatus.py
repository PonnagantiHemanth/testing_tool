#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.gaming.modestatus
:brief: HID++ 2.0 ``ModeStatus`` command interface definition
:author: YY Liu <yliu5@logitech.com>
:date: 2022/09/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
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
class ModeStatus(HidppMessage):
    """
    This interface is used to notify and be queried Device status of modes by software.
    """
    FEATURE_ID = 0x8090
    MAX_FUNCTION_INDEX_V0 = 0
    MAX_FUNCTION_INDEX_V1_TO_V3 = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__

    class ModeStatus0(BitFieldContainerMixin):
        """
        Define ``ModeStatus0`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Mode Status 0                 1
        ============================  ==========
        """
        ENDURANCE_MODE = 0
        PERFORMANCE_MODE = 1

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            MODE_STATUS_0 = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            MODE_STATUS_0 = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            MODE_STATUS_0 = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.MODE_STATUS_0, length=LEN.MODE_STATUS_0,
                     title="ModeStatus0", name="mode_status_0",
                     checks=(CheckInt(0, pow(2, LEN.MODE_STATUS_0) - 1),),
                     default_value=DEFAULT.MODE_STATUS_0),
        )
    # end class ModeStatus0

    class ModeStatus1(BitFieldContainerMixin):
        """
        Define ``ModeStatus1`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        Force Gaming Surface Mode     1
        Power Mode                    1
        ============================  ==========
        """
        class PowerMode:
            """
            Define the supported power modes
            """
            LOW_LATENCY_MODE = 0
            POWER_SAVE_MODE = 1
        # end class PowerMode

        class GamingSurfaceMode:
            """
            Define the supported surface modes
            """
            NON_GAMING_SURFACE = 0
            GAMING_SURFACE = 1
        # end class GamingSurfaceMode

        class Mask:
            """
            Define the ModeStatus1 bit mask
            """
            POWER_MODE = 1
            SURFACE_MODE = 2
        # end class Mask

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            FORCE_GAMING_SURFACE_MODE = RESERVED - 1
            POWER_MODE = FORCE_GAMING_SURFACE_MODE - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            FORCE_GAMING_SURFACE_MODE = 0x1
            POWER_MODE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            FORCE_GAMING_SURFACE_MODE = 0x1
            POWER_MODE = 0x1
        # end class DEFAULT

        class POS(object):
            """
            ModeStatus1 bit field position
            """
            GAMING_SURFACE = 1
            POWER_MODE = 0
        # end class POS

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.FORCE_GAMING_SURFACE_MODE, length=LEN.FORCE_GAMING_SURFACE_MODE,
                     title="ForceGamingSurfaceMode", name="force_gaming_surface_mode",
                     checks=(CheckInt(0, pow(2, LEN.FORCE_GAMING_SURFACE_MODE) - 1),),
                     default_value=DEFAULT.FORCE_GAMING_SURFACE_MODE),
            BitField(fid=FID.POWER_MODE, length=LEN.POWER_MODE,
                     title="PowerMode", name="power_mode",
                     checks=(CheckInt(0, pow(2, LEN.POWER_MODE) - 1),),
                     default_value=DEFAULT.POWER_MODE),
        )
    # end class ModeStatus1

    class ModeStatus1V3(ModeStatus1):
        """
        Define ``ModeStatus1V3`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      5
        Force Gaming Surface Mode     2
        Power Mode                    1
        ============================  ==========
        """
        class GamingSurfaceMode:
            """
            Define the supported surface modes
            """
            AUTOMATIC_DETECTION = 0
            FORCE_GAMING = 1
            FORCE_COMPATIBILITY = 2
        # end class GamingSurfaceMode

        class FID(object):
            # See ``ModeStatus1.FID``
            RESERVED = 0xFF
            FORCE_GAMING_SURFACE_MODE = RESERVED - 1
            POWER_MODE = FORCE_GAMING_SURFACE_MODE - 1
        # end class FID

        class LEN(object):
            # See ``ModeStatus1.LEN``
            RESERVED = 0x5
            FORCE_GAMING_SURFACE_MODE = 0x2
            POWER_MODE = 0x1
        # end class LEN

        class DEFAULT(object):
            # See ``ModeStatus1.DEFAULT``
            RESERVED = 0x0
            FORCE_GAMING_SURFACE_MODE = 0x1
            POWER_MODE = 0x1
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.FORCE_GAMING_SURFACE_MODE, length=LEN.FORCE_GAMING_SURFACE_MODE,
                     title="ForceGamingSurfaceMode", name="force_gaming_surface_mode",
                     checks=(CheckInt(0, pow(2, LEN.FORCE_GAMING_SURFACE_MODE) - 1),),
                     default_value=DEFAULT.FORCE_GAMING_SURFACE_MODE),
            BitField(fid=FID.POWER_MODE, length=LEN.POWER_MODE,
                     title="PowerMode", name="power_mode",
                     checks=(CheckInt(0, pow(2, LEN.POWER_MODE) - 1),),
                     default_value=DEFAULT.POWER_MODE),
        )
    # end class ModeStatus1V3

    class DevCapabilityV1(BitFieldContainerMixin):
        """
        Define ``DevCapabilityV1`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      14
        Mode Status 0 Changed by SW   1
        Mode Status 0 Changed by HW   1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            MODE_STATUS_0_CHANGED_BY_SW = RESERVED - 1
            MODE_STATUS_0_CHANGED_BY_HW = MODE_STATUS_0_CHANGED_BY_SW - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0xE
            MODE_STATUS_0_CHANGED_BY_SW = 0x1
            MODE_STATUS_0_CHANGED_BY_HW = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            MODE_STATUS_0_CHANGED_BY_SW = 0x0
            MODE_STATUS_0_CHANGED_BY_HW = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.MODE_STATUS_0_CHANGED_BY_SW, length=LEN.MODE_STATUS_0_CHANGED_BY_SW,
                     title="ModeStatus0ChangedBySw", name="mode_status_0_changed_by_sw",
                     checks=(CheckInt(0, pow(2, LEN.MODE_STATUS_0_CHANGED_BY_SW) - 1),),
                     default_value=DEFAULT.MODE_STATUS_0_CHANGED_BY_SW),
            BitField(fid=FID.MODE_STATUS_0_CHANGED_BY_HW, length=LEN.MODE_STATUS_0_CHANGED_BY_HW,
                     title="ModeStatus0ChangedByHw", name="mode_status_0_changed_by_hw",
                     checks=(CheckInt(0, pow(2, LEN.MODE_STATUS_0_CHANGED_BY_HW) - 1),),
                     default_value=DEFAULT.MODE_STATUS_0_CHANGED_BY_HW),
        )
    # end class DevCapabilityV1

    class DevCapabilityV2ToV3(BitFieldContainerMixin):
        """
        Define ``DevCapabilityV2ToV3`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      12
        Surface Mode                  1
        Power Save Mode               1
        Mode Status 0 Changed by SW   1
        Mode Status 0 Changed by HW   1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            SURFACE_MODE = RESERVED - 1
            POWER_SAVE_MODE = SURFACE_MODE - 1
            MODE_STATUS_0_CHANGED_BY_SW = POWER_SAVE_MODE - 1
            MODE_STATUS_0_CHANGED_BY_HW = MODE_STATUS_0_CHANGED_BY_SW - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0xc
            SURFACE_MODE = 0x1
            POWER_SAVE_MODE = 0x1
            MODE_STATUS_0_CHANGED_BY_SW = 0x1
            MODE_STATUS_0_CHANGED_BY_HW = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            SURFACE_MODE = 0x0
            POWER_SAVE_MODE = 0x0
            MODE_STATUS_0_CHANGED_BY_SW = 0x0
            MODE_STATUS_0_CHANGED_BY_HW = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.SURFACE_MODE, length=LEN.SURFACE_MODE,
                     title="SurfaceMode", name="surface_mode",
                     checks=(CheckInt(0, pow(2, LEN.SURFACE_MODE) - 1),),
                     default_value=DEFAULT.SURFACE_MODE),
            BitField(fid=FID.POWER_SAVE_MODE, length=LEN.POWER_SAVE_MODE,
                     title="PowerSaveMode", name="power_save_mode",
                     checks=(CheckInt(0, pow(2, LEN.POWER_SAVE_MODE) - 1),),
                     default_value=DEFAULT.POWER_SAVE_MODE),
            BitField(fid=FID.MODE_STATUS_0_CHANGED_BY_SW, length=LEN.MODE_STATUS_0_CHANGED_BY_SW,
                     title="ModeStatus0ChangedBySw", name="mode_status_0_changed_by_sw",
                     checks=(CheckInt(0, pow(2, LEN.MODE_STATUS_0_CHANGED_BY_SW) - 1),),
                     default_value=DEFAULT.MODE_STATUS_0_CHANGED_BY_SW),
            BitField(fid=FID.MODE_STATUS_0_CHANGED_BY_HW, length=LEN.MODE_STATUS_0_CHANGED_BY_HW,
                     title="ModeStatus0ChangedByHw", name="mode_status_0_changed_by_hw",
                     checks=(CheckInt(0, pow(2, LEN.MODE_STATUS_0_CHANGED_BY_HW) - 1),),
                     default_value=DEFAULT.MODE_STATUS_0_CHANGED_BY_HW),
        )
    # end class DevCapabilityV2ToV3
# end class ModeStatus


class ModeStatusModel(FeatureModel):
    """
    Define ``ModeStatus`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_MODE_STATUS = 0
        SET_MODE_STATUS = 1
        GET_DEV_CONFIG = 2

        # Event index
        MODE_STATUS_BROADCASTING = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ModeStatus`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_MODE_STATUS: {
                    "request": GetModeStatus,
                    "response": GetModeStatusResponse
                }
            },
            "events": {
                cls.INDEX.MODE_STATUS_BROADCASTING: {"report": ModeStatusBroadcastingEvent}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_MODE_STATUS: {
                    "request": GetModeStatus,
                    "response": GetModeStatusResponse
                },
                cls.INDEX.SET_MODE_STATUS: {
                    "request": SetModeStatus,
                    "response": SetModeStatusResponse
                },
                cls.INDEX.GET_DEV_CONFIG: {
                    "request": GetDevConfig,
                    "response": GetDevConfigResponseV1
                }
            },
            "events": {
                cls.INDEX.MODE_STATUS_BROADCASTING: {"report": ModeStatusBroadcastingEvent}
            }
        }

        function_map_v2 = {
            "functions": {
                cls.INDEX.GET_MODE_STATUS: {
                    "request": GetModeStatus,
                    "response": GetModeStatusResponse
                },
                cls.INDEX.SET_MODE_STATUS: {
                    "request": SetModeStatus,
                    "response": SetModeStatusResponse
                },
                cls.INDEX.GET_DEV_CONFIG: {
                    "request": GetDevConfig,
                    "response": GetDevConfigResponseV2ToV3
                }
            },
            "events": {
                cls.INDEX.MODE_STATUS_BROADCASTING: {"report": ModeStatusBroadcastingEvent}
            }
        }

        function_map_v3 = {
            "functions": {
                cls.INDEX.GET_MODE_STATUS: {
                    "request": GetModeStatus,
                    "response": GetModeStatusResponseV3
                },
                cls.INDEX.SET_MODE_STATUS: {
                    "request": SetModeStatus,
                    "response": SetModeStatusResponse
                },
                cls.INDEX.GET_DEV_CONFIG: {
                    "request": GetDevConfig,
                    "response": GetDevConfigResponseV2ToV3
                }
            },
            "events": {
                cls.INDEX.MODE_STATUS_BROADCASTING: {"report": ModeStatusBroadcastingEvent}
            }
        }

        return {
            "feature_base": ModeStatus,
            "versions": {
                ModeStatusV0.VERSION: {
                    "main_cls": ModeStatusV0,
                    "api": function_map_v0
                },
                ModeStatusV1.VERSION: {
                    "main_cls": ModeStatusV1,
                    "api": function_map_v1
                },
                ModeStatusV2.VERSION: {
                    "main_cls": ModeStatusV2,
                    "api": function_map_v2
                },
                ModeStatusV3.VERSION: {
                    "main_cls": ModeStatusV3,
                    "api": function_map_v3
                }
            }
        }
    # end def _get_data_model
# end class ModeStatusModel


class ModeStatusFactory(FeatureFactory):
    """
    Get ``ModeStatus`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ModeStatus`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``ModeStatusInterface``
        """
        return ModeStatusModel.get_main_cls(version)()
    # end def create
# end class ModeStatusFactory


class ModeStatusInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ModeStatus``
    """

    def __init__(self):
        # Requests
        self.get_mode_status_cls = None
        self.set_mode_status_cls = None
        self.get_dev_config_cls = None

        # Responses
        self.get_mode_status_response_cls = None
        self.set_mode_status_response_cls = None
        self.get_dev_config_response_cls = None

        # Events
        self.mode_status_broadcasting_event_cls = None
    # end def __init__
# end class ModeStatusInterface


class ModeStatusV0(ModeStatusInterface):
    """
    Define ``ModeStatusV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetModeStatus() -> modeStatus0, modeStatus1

    [Event 0] ModeStatusBroadcastingEvent -> modeStatus0, modeStatus1, changedMask0, changedMask1
    """
    VERSION = 0

    def __init__(self):
        # See ``ModeStatus.__init__``
        super().__init__()
        index = ModeStatusModel.INDEX

        # Requests
        self.get_mode_status_cls = ModeStatusModel.get_request_cls(
            self.VERSION, index.GET_MODE_STATUS)

        # Responses
        self.get_mode_status_response_cls = ModeStatusModel.get_response_cls(
            self.VERSION, index.GET_MODE_STATUS)

        # Events
        self.mode_status_broadcasting_event_cls = ModeStatusModel.get_report_cls(
            self.VERSION, index.MODE_STATUS_BROADCASTING)
    # end def __init__

    def get_max_function_index(self):
        # See ``ModeStatusInterface.get_max_function_index``
        return ModeStatusModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class ModeStatusV0


class ModeStatusV1(ModeStatusV0):
    """
    Define ``ModeStatusV1`` feature

    This feature provides model and unit specific information for version 1

    [0] GetModeStatus() -> modeStatus0, modeStatus1

    [1] SetModeStatus(modeStatus0, modeStatus1, changedMask0, changedMask1) -> None

    [2] GetDevConfig() -> devCapability

    [Event 0] ModeStatusBroadcastingEvent -> modeStatus0, modeStatus1, changedMask0, changedMask1
    """
    VERSION = 1

    def __init__(self):
        # See ``ModeStatus.__init__``
        super().__init__()
        index = ModeStatusModel.INDEX

        # Requests
        self.set_mode_status_cls = ModeStatusModel.get_request_cls(
            self.VERSION, index.SET_MODE_STATUS)
        self.get_dev_config_cls = ModeStatusModel.get_request_cls(
            self.VERSION, index.GET_DEV_CONFIG)

        # Responses
        self.set_mode_status_response_cls = ModeStatusModel.get_response_cls(
            self.VERSION, index.SET_MODE_STATUS)
        self.get_dev_config_response_cls = ModeStatusModel.get_response_cls(
            self.VERSION, index.GET_DEV_CONFIG)
    # end def __init__

    def get_max_function_index(self):
        # See ``ModeStatusInterface.get_max_function_index``
        return ModeStatusModel.get_base_cls().MAX_FUNCTION_INDEX_V1_TO_V3
    # end def get_max_function_index
# end class ModeStatusV1


class ModeStatusV2(ModeStatusV1):
    """
    Define ``ModeStatusV2`` feature

    This feature provides model and unit specific information for version 2

    [0] GetModeStatus() -> modeStatus0, modeStatus1

    [1] SetModeStatus(modeStatus0, modeStatus1, changedMask0, changedMask1) -> None

    [2] GetDevConfig() -> devCapability

    [Event 0] ModeStatusBroadcastingEvent -> modeStatus0, modeStatus1, changedMask0, changedMask1
    """
    VERSION = 2
# end class ModeStatusV2


class ModeStatusV3(ModeStatusV2):
    """
    Define ``ModeStatusV3`` feature

    This feature provides model and unit specific information for version 3

    [0] GetModeStatus() -> modeStatus0, modeStatus1

    [1] SetModeStatus(modeStatus0, modeStatus1, changedMask0, changedMask1) -> None

    [2] GetDevConfig() -> devCapability

    [Event 0] ModeStatusBroadcastingEvent -> modeStatus0, modeStatus1, changedMask0, changedMask1
    """
    VERSION = 3
# end class ModeStatusV3


class ShortEmptyPacketDataFormat(ModeStatus):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetModeStatus
        - GetDevConfig

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ModeStatus.FID):
        # See ``ModeStatus.FID``
        PADDING = ModeStatus.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ModeStatus.LEN):
        # See ``ModeStatus.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ModeStatus.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ModeStatus.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(ModeStatus):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetModeStatusResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(ModeStatus.FID):
        # See ``ModeStatus.FID``
        PADDING = ModeStatus.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ModeStatus.LEN):
        # See ``ModeStatus.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = ModeStatus.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ModeStatus.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class GetModeStatus(ShortEmptyPacketDataFormat):
    """
    Define ``GetModeStatus`` implementation class for version 0, 1, 2, 3
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetModeStatusResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetModeStatus


class GetModeStatusResponse(ModeStatus):
    """
    Define ``GetModeStatusResponse`` implementation class for version 0, 1, 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Mode Status 0                 8
    Mode Status 1                 8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetModeStatus,)
    VERSION = (0, 1, 2,)
    FUNCTION_INDEX = 0

    class FID(ModeStatus.FID):
        # See ``ModeStatus.FID``
        MODE_STATUS_0 = ModeStatus.FID.SOFTWARE_ID - 1
        MODE_STATUS_1 = MODE_STATUS_0 - 1
        PADDING = MODE_STATUS_1 - 1
    # end class FID

    class LEN(ModeStatus.LEN):
        # See ``ModeStatus.LEN``
        MODE_STATUS_0 = 0x8
        MODE_STATUS_1 = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = ModeStatus.FIELDS + (
        BitField(fid=FID.MODE_STATUS_0, length=LEN.MODE_STATUS_0,
                 title="ModeStatus0", name="mode_status_0",
                 checks=(CheckHexList(LEN.MODE_STATUS_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.MODE_STATUS_1, length=LEN.MODE_STATUS_1,
                 title="ModeStatus1", name="mode_status_1",
                 checks=(CheckHexList(LEN.MODE_STATUS_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ModeStatus.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mode_status_0, power_mode, force_gaming_surface_mode, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param mode_status_0: Mode Status 0
        :type mode_status_0: ``bool|HexList``
        :param power_mode: Power Mode
        :type power_mode: ``int|HexList``
        :param force_gaming_surface_mode: Force Gaming Surface Mode
        :type force_gaming_surface_mode: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mode_status_0 = self.ModeStatus0(mode_status_0=mode_status_0)
        self.mode_status_1 = self.ModeStatus1(power_mode=power_mode,
                                              force_gaming_surface_mode=force_gaming_surface_mode)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetModeStatusResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.mode_status_0 = cls.ModeStatus0.fromHexList(
            inner_field_container_mixin.mode_status_0)
        inner_field_container_mixin.mode_status_1 = cls.ModeStatus1.fromHexList(
            inner_field_container_mixin.mode_status_1)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetModeStatusResponse


class GetModeStatusResponseV3(GetModeStatusResponse):
    """
    Define ``GetModeStatusResponse`` implementation class for version 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Mode Status 0                 8
    Mode Status 1                 8
    Padding                       112
    ============================  ==========
    """
    VERSION = (3,)

    def __init__(self, device_index, feature_index, mode_status_0, power_mode, force_gaming_surface_mode, **kwargs):
        # See ``GetModeStatusResponse.__init__``
        super().__init__(device_index=device_index, feature_index=feature_index,
                         mode_status_0=mode_status_0, power_mode=power_mode,
                         force_gaming_surface_mode=force_gaming_surface_mode, **kwargs)
        self.mode_status_0 = self.ModeStatus0(mode_status_0=mode_status_0)
        self.mode_status_1 = self.ModeStatus1V3(power_mode=power_mode,
                                                force_gaming_surface_mode=force_gaming_surface_mode)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetModeStatusResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.mode_status_1 = cls.ModeStatus1V3.fromHexList(
            inner_field_container_mixin.mode_status_1.__hexlist__())
        return inner_field_container_mixin
    # end def fromHexList
# end class GetModeStatusResponseV3


class SetModeStatus(ModeStatus):
    """
    Define ``SetModeStatus`` implementation class for version 1, 2, 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Mode Status 0                 8
    Mode Status 1                 8
    Changed Mask 0                8
    Changed Mask 1                8
    Padding                       96
    ============================  ==========
    """

    class FID(ModeStatus.FID):
        # See ``ModeStatus.FID``
        MODE_STATUS_0 = ModeStatus.FID.SOFTWARE_ID - 1
        MODE_STATUS_1 = MODE_STATUS_0 - 1
        CHANGED_MASK_0 = MODE_STATUS_1 - 1
        CHANGED_MASK_1 = CHANGED_MASK_0 - 1
        PADDING = CHANGED_MASK_1 - 1
    # end class FID

    class LEN(ModeStatus.LEN):
        # See ``ModeStatus.LEN``
        MODE_STATUS_0 = 0x8
        MODE_STATUS_1 = 0x8
        CHANGED_MASK_0 = 0x8
        CHANGED_MASK_1 = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = ModeStatus.FIELDS + (
        BitField(fid=FID.MODE_STATUS_0, length=LEN.MODE_STATUS_0,
                 title="ModeStatus0", name="mode_status_0",
                 checks=(CheckHexList(LEN.MODE_STATUS_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.MODE_STATUS_1, length=LEN.MODE_STATUS_1,
                 title="ModeStatus1", name="mode_status_1",
                 checks=(CheckHexList(LEN.MODE_STATUS_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.CHANGED_MASK_0, length=LEN.CHANGED_MASK_0,
                 title="ChangedMask0", name="changed_mask_0",
                 checks=(CheckHexList(LEN.CHANGED_MASK_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.CHANGED_MASK_1, length=LEN.CHANGED_MASK_1,
                 title="ChangedMask1", name="changed_mask_1",
                 checks=(CheckHexList(LEN.CHANGED_MASK_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ModeStatus.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mode_status_0, mode_status_1, changed_mask_0, changed_mask_1,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param mode_status_0: Mode Status 0
        :type mode_status_0: ``int|HexList``
        :param mode_status_1: Mode Status 1
        :type mode_status_1: ``int|HexList``
        :param changed_mask_0: Changed Mask 0
        :type changed_mask_0: ``int|HexList``
        :param changed_mask_1: Changed Mask 1
        :type changed_mask_1: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetModeStatusResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mode_status_0 = self.ModeStatus0.fromHexList(HexList(mode_status_0))
        self.mode_status_1 = self.ModeStatus1.fromHexList(HexList(mode_status_1))
        self.changed_mask_0 = changed_mask_0
        self.changed_mask_1 = changed_mask_1
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``SetModeStatus``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.mode_status_0 = cls.ModeStatus0.fromHexList(
            inner_field_container_mixin.mode_status_0)
        inner_field_container_mixin.mode_status_1 = cls.ModeStatus1.fromHexList(
            inner_field_container_mixin.mode_status_1)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetModeStatus


class SetModeStatusResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetModeStatusResponse`` implementation class for version 1, 2, 3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetModeStatus,)
    VERSION = (1, 2, 3,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetModeStatusResponse


class GetDevConfig(ShortEmptyPacketDataFormat):
    """
    Define ``GetDevConfig`` implementation class for version 1, 2, 3
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetDevConfigResponseV1.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetDevConfig


class GetDevConfigResponseV1(ModeStatus):
    """
    Define ``GetDevConfigResponseV1`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Dev Capability                16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDevConfig,)
    VERSION = (1,)
    FUNCTION_INDEX = 2

    class FID(ModeStatus.FID):
        # See ``ModeStatus.FID``
        DEV_CAPABILITY = ModeStatus.FID.SOFTWARE_ID - 1
        PADDING = DEV_CAPABILITY - 1
    # end class FID

    class LEN(ModeStatus.LEN):
        # See ``ModeStatus.LEN``
        DEV_CAPABILITY = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = ModeStatus.FIELDS + (
        BitField(fid=FID.DEV_CAPABILITY, length=LEN.DEV_CAPABILITY,
                 title="DevCapability", name="dev_capability",
                 checks=(CheckHexList(LEN.DEV_CAPABILITY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEV_CAPABILITY) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ModeStatus.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mode_status_0_changed_by_sw,
                 mode_status_0_changed_by_hw, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param mode_status_0_changed_by_sw: Mode Status 0 Changed by SW
        :type mode_status_0_changed_by_sw: ``bool|HexList``
        :param mode_status_0_changed_by_hw: Mode Status 0 Changed by HW
        :type mode_status_0_changed_by_hw: ``bool|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.dev_capability = self.DevCapabilityV1(mode_status_0_changed_by_sw=mode_status_0_changed_by_sw,
                                                   mode_status_0_changed_by_hw=mode_status_0_changed_by_hw)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetDevConfigResponseV1``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.dev_capability = cls.DevCapabilityV1.fromHexList(
            inner_field_container_mixin.dev_capability)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetDevConfigResponseV1


class GetDevConfigResponseV2ToV3(ModeStatus):
    """
    Define ``GetDevConfigResponseV2ToV3`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Dev Capability                16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDevConfig,)
    VERSION = (2, 3,)
    FUNCTION_INDEX = 2

    class FID(ModeStatus.FID):
        # See ``ModeStatus.FID``
        DEV_CAPABILITY = ModeStatus.FID.SOFTWARE_ID - 1
        PADDING = DEV_CAPABILITY - 1
    # end class FID

    class LEN(ModeStatus.LEN):
        # See ``ModeStatus.LEN``
        DEV_CAPABILITY = 0x10
        PADDING = 0x70

    # end class LEN

    FIELDS = ModeStatus.FIELDS + (
        BitField(fid=FID.DEV_CAPABILITY, length=LEN.DEV_CAPABILITY,
                 title="DevCapability", name="dev_capability",
                 checks=(CheckHexList(LEN.DEV_CAPABILITY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEV_CAPABILITY) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ModeStatus.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, surface_mode, power_save_mode,
                 mode_status_0_changed_by_sw, mode_status_0_changed_by_hw, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param surface_mode: Surface mode supported
        :type surface_mode: ``bool|HexList``
        :param power_save_mode: Power Save Mode Supported
        :type power_save_mode: ``bool|HexList``
        :param mode_status_0_changed_by_sw: Mode Status 0 Changed by SW
        :type mode_status_0_changed_by_sw: ``bool|HexList``
        :param mode_status_0_changed_by_hw: Mode Status 0 Changed by HW
        :type mode_status_0_changed_by_hw: ``bool|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.dev_capability = self.DevCapabilityV2ToV3(surface_mode=surface_mode,
                                                       power_save_mode=power_save_mode,
                                                       mode_status_0_changed_by_sw=mode_status_0_changed_by_sw,
                                                       mode_status_0_changed_by_hw=mode_status_0_changed_by_hw)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetDevConfigResponseV2ToV3``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.dev_capability = cls.DevCapabilityV2ToV3.fromHexList(
            inner_field_container_mixin.dev_capability)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetDevConfigResponseV2ToV3


class ModeStatusBroadcastingEvent(ModeStatus):
    """
    Define ``ModeStatusBroadcastingEvent`` implementation class for version 0, 1, 2, 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Mode Status 0                 8
    Mode Status 1                 8
    Changed Mask 0                8
    Changed Mask 1                8
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1, 2, 3,)
    FUNCTION_INDEX = 0

    class FID(ModeStatus.FID):
        # See ``ModeStatus.FID``
        MODE_STATUS_0 = ModeStatus.FID.SOFTWARE_ID - 1
        MODE_STATUS_1 = MODE_STATUS_0 - 1
        CHANGED_MASK_0 = MODE_STATUS_1 - 1
        CHANGED_MASK_1 = CHANGED_MASK_0 - 1
        PADDING = CHANGED_MASK_1 - 1
    # end class FID

    class LEN(ModeStatus.LEN):
        # See ``ModeStatus.LEN``
        MODE_STATUS_0 = 0x8
        MODE_STATUS_1 = 0x8
        CHANGED_MASK_0 = 0x8
        CHANGED_MASK_1 = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = ModeStatus.FIELDS + (
        BitField(fid=FID.MODE_STATUS_0, length=LEN.MODE_STATUS_0,
                 title="ModeStatus0", name="mode_status_0",
                 checks=(CheckHexList(LEN.MODE_STATUS_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.MODE_STATUS_1, length=LEN.MODE_STATUS_1,
                 title="ModeStatus1", name="mode_status_1",
                 checks=(CheckHexList(LEN.MODE_STATUS_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.CHANGED_MASK_0, length=LEN.CHANGED_MASK_0,
                 title="ChangedMask0", name="changed_mask_0",
                 checks=(CheckHexList(LEN.CHANGED_MASK_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.CHANGED_MASK_1, length=LEN.CHANGED_MASK_1,
                 title="ChangedMask1", name="changed_mask_1",
                 checks=(CheckHexList(LEN.CHANGED_MASK_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ModeStatus.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mode_status_0, power_mode, force_gaming_surface_mode,
                 changed_mask_0, changed_mask_1, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param mode_status_0: Mode Status 0
        :type mode_status_0: ``bool|HexList``
        :param power_mode: Power Mode
        :type power_mode: ``int|HexList``
        :param force_gaming_surface_mode: Force Gaming Surface Mode
        :type force_gaming_surface_mode: ``int|HexList``
        :param changed_mask_0: Changed Mask 0
        :type changed_mask_0: ``int|HexList``
        :param changed_mask_1: Changed Mask 1
        :type changed_mask_1: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mode_status_0 = self.ModeStatus0(mode_status_0=mode_status_0)
        self.mode_status_1 = self.ModeStatus1(power_mode=power_mode,
                                              force_gaming_surface_mode=force_gaming_surface_mode)
        self.changed_mask_0 = changed_mask_0
        self.changed_mask_1 = changed_mask_1
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``ModeStatusBroadcastingEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.mode_status_0 = cls.ModeStatus0.fromHexList(
            inner_field_container_mixin.mode_status_0)
        inner_field_container_mixin.mode_status_1 = cls.ModeStatus1.fromHexList(
            inner_field_container_mixin.mode_status_1)
        return inner_field_container_mixin
    # end def fromHexList
# end class ModeStatusBroadcastingEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
