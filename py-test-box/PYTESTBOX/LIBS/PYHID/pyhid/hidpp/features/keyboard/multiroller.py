#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.keyboard.multiroller
:brief: HID++ 2.0 ``MultiRoller`` command interface definition
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/06
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
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRoller(HidppMessage):
    """
    Diversion of one or more roller (or Dial) movement reports via HIDPP events. When reports are diverted via HIDPP they are not reported via HID.
    """
    FEATURE_ID = 0x4610
    MAX_FUNCTION_INDEX_V0_TO_V1 = 3

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
# end class MultiRoller


class NumRoller(BitFieldContainerMixin):
    """
    Define ``NumRoller`` information

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      4
    Num Rollers                   4
    ============================  ==========
    """

    class FID(object):
        """
        Field identifiers
        """
        RESERVED = 0xFF
        NUM_ROLLERS = RESERVED - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        RESERVED = 0x4
        NUM_ROLLERS = 0x4
    # end class LEN

    class DEFAULT:
        """
        Field default values
        """
        RESERVED = 0x0
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=DEFAULT.RESERVED),
        BitField(fid=FID.NUM_ROLLERS, length=LEN.NUM_ROLLERS,
                 title="NumRollers", name="num_rollers",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.NUM_ROLLERS) - 1),)),
    )
# end class NumRoller


class RollerId(BitFieldContainerMixin):
    """
    Define ``RollerId`` information

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      4
    Roller Id                     4
    ============================  ==========
    """

    class FID(object):
        """
        Field identifiers
        """
        RESERVED = 0xFF
        ROLLER_ID = RESERVED - 1

    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        RESERVED = 0x4
        ROLLER_ID = 0x4

    # end class LEN

    class DEFAULT:
        """
        Field default values
        """
        RESERVED = 0x0

    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=DEFAULT.RESERVED),
        BitField(fid=FID.ROLLER_ID, length=LEN.ROLLER_ID,
                 title="RollerId", name="roller_id",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ROLLER_ID) - 1),)),
    )
# end class RollerId


class CapabilitiesV0(BitFieldContainerMixin):
    """
    Define ``CapabilitiesV0`` information

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      4
    Lightbar Id                   4
    ============================  ==========
    """

    class FID(object):
        """
        Field identifiers
        """
        RESERVED = 0xFF
        LIGHTBAR_ID = RESERVED - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        RESERVED = 0x4
        LIGHTBAR_ID = 0x4
    # end class LEN

    class DEFAULT:
        """
        Field default values
        """
        RESERVED = 0x0
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=DEFAULT.RESERVED),
        BitField(fid=FID.LIGHTBAR_ID, length=LEN.LIGHTBAR_ID,
                 title="LightbarId", name="lightbar_id",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.LIGHTBAR_ID) - 1),)),
    )
# end class CapabilitiesV0


class CapabilitiesV1(CapabilitiesV0):
    """
    Define ``CapabilitiesV1`` information

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      3
    Timestamp Report              1
    Lightbar Id                   4
    ============================  ==========
    """

    class FID(CapabilitiesV0.FID):
        # See ``CapabilitiesV0.FID``
        TIMESTAMP_REPORT = CapabilitiesV0.FID.RESERVED - 1
        LIGHTBAR_ID = TIMESTAMP_REPORT - 1
    # end class FID

    class LEN(CapabilitiesV0.LEN):
        # See ``CapabilitiesV0.LEN``
        RESERVED = 0x3
        TIMESTAMP_REPORT = 0x1
    # end class LEN

    FIELDS = (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=CapabilitiesV0.DEFAULT.RESERVED),
        BitField(fid=FID.TIMESTAMP_REPORT, length=LEN.TIMESTAMP_REPORT,
                 title="TimestampReport", name="timestamp_report",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TIMESTAMP_REPORT) - 1),)),
        BitField(fid=FID.LIGHTBAR_ID, length=LEN.LIGHTBAR_ID,
                 title="LightbarId", name="lightbar_id",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.LIGHTBAR_ID) - 1),)),
    )
# end class CapabilitiesV1


class RollerMode(BitFieldContainerMixin):
    """
    Define ``RollerMode`` information

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      7
    divert                        1
    ============================  ==========
    """
    DEFAULT_MODE = 0    # HID/Send to OS
    DIVERT = 1          # HID++/Divert to SW

    class FID(object):
        """
        Field identifiers
        """
        RESERVED = 0xFF
        DIVERT = RESERVED - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        RESERVED = 0x7
        DIVERT = 0x1
    # end class LEN

    class DEFAULT:
        """
        Field default values
        """
        RESERVED = 0x0
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=DEFAULT.RESERVED),
        BitField(fid=FID.DIVERT, length=LEN.DIVERT,
                 title="Divert", name="divert",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.DIVERT) - 1),)),
    )
# end class RollerMode


# noinspection DuplicatedCode
class MultiRollerModel(FeatureModel):
    """
    Define ``MultiRoller`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_ROLLER_CAPABILITIES = 1
        GET_MODE = 2
        SET_MODE = 3

        # Event index
        ROTATION = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``MultiRoller`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_ROLLER_CAPABILITIES: {
                    "request": GetRollerCapabilities,
                    "response": GetRollerCapabilitiesResponseV0
                },
                cls.INDEX.GET_MODE: {
                    "request": GetMode,
                    "response": GetModeResponse
                },
                cls.INDEX.SET_MODE: {
                    "request": SetMode,
                    "response": SetModeResponse
                }
            },
            "events": {
                cls.INDEX.ROTATION: {"report": RotationEventV0}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_ROLLER_CAPABILITIES: {
                    "request": GetRollerCapabilities,
                    "response": GetRollerCapabilitiesResponseV1
                },
                cls.INDEX.GET_MODE: {
                    "request": GetMode,
                    "response": GetModeResponse
                },
                cls.INDEX.SET_MODE: {
                    "request": SetMode,
                    "response": SetModeResponse
                }
            },
            "events": {
                cls.INDEX.ROTATION: {"report": RotationEventV1}
            }
        }

        return {
            "feature_base": MultiRoller,
            "versions": {
                MultiRollerV0.VERSION: {
                    "main_cls": MultiRollerV0,
                    "api": function_map_v0
                },
                MultiRollerV1.VERSION: {
                    "main_cls": MultiRollerV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class MultiRollerModel


class MultiRollerFactory(FeatureFactory):
    """
    Get ``MultiRoller`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``MultiRoller`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``MultiRollerInterface``
        """
        return MultiRollerModel.get_main_cls(version)()
    # end def create
# end class MultiRollerFactory


class MultiRollerInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``MultiRoller``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_roller_capabilities_cls = None
        self.get_mode_cls = None
        self.set_mode_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_roller_capabilities_response_cls = None
        self.get_mode_response_cls = None
        self.set_mode_response_cls = None

        # Events
        self.rotation_event_cls = None
    # end def __init__
# end class MultiRollerInterface


class MultiRollerV0(MultiRollerInterface):
    """
    Define ``MultiRollerV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> numRoller

    [1] getRollerCapabilities(rollerId) -> incrementsPerRotation, incrementsPerRatchet, capabilities

    [2] getMode(rollerId) -> rollerMode

    [3] setMode(rollerId, rollerMode) -> None

    [Event 0] RotationEvent -> rollerId, delta
    """
    VERSION = 0

    def __init__(self):
        # See ``MultiRoller.__init__``
        super().__init__()
        index = MultiRollerModel.INDEX

        # Requests
        self.get_capabilities_cls = MultiRollerModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_roller_capabilities_cls = MultiRollerModel.get_request_cls(
            self.VERSION, index.GET_ROLLER_CAPABILITIES)
        self.get_mode_cls = MultiRollerModel.get_request_cls(
            self.VERSION, index.GET_MODE)
        self.set_mode_cls = MultiRollerModel.get_request_cls(
            self.VERSION, index.SET_MODE)

        # Responses
        self.get_capabilities_response_cls = MultiRollerModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_roller_capabilities_response_cls = MultiRollerModel.get_response_cls(
            self.VERSION, index.GET_ROLLER_CAPABILITIES)
        self.get_mode_response_cls = MultiRollerModel.get_response_cls(
            self.VERSION, index.GET_MODE)
        self.set_mode_response_cls = MultiRollerModel.get_response_cls(
            self.VERSION, index.SET_MODE)

        # Events
        self.rotation_event_cls = MultiRollerModel.get_report_cls(
            self.VERSION, index.ROTATION)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``MultiRollerInterface.get_max_function_index``
        return MultiRollerModel.get_base_cls().MAX_FUNCTION_INDEX_V0_TO_V1
    # end def get_max_function_index
# end class MultiRollerV0


class MultiRollerV1(MultiRollerV0):
    """
    Define ``MultiRollerV1`` feature

    This feature provides model and unit specific information for version 1

    [1] getRollerCapabilities(rollerId) -> incrementsPerRotation, incrementsPerRatchet, capabilities

    [Event 0] RotationEvent -> rollerId, delta, reportTimestamp
    """
    VERSION = 1

    def __init__(self):
        # See ``MultiRoller.__init__``
        super().__init__()
        index = MultiRollerModel.INDEX

        # Requests
        self.get_roller_capabilities_cls = MultiRollerModel.get_request_cls(
            self.VERSION, index.GET_ROLLER_CAPABILITIES)

        # Responses
        self.get_roller_capabilities_response_cls = MultiRollerModel.get_response_cls(
            self.VERSION, index.GET_ROLLER_CAPABILITIES)
    # end def __init__
# end class MultiRollerV1


class ShortEmptyPacketDataFormat(MultiRoller):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        PADDING = MultiRoller.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(MultiRoller):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetModeResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        PADDING = MultiRoller.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class RollerIdContainer(MultiRoller):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetMode
        - GetRollerCapabilities

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      4
    Roller Id                     4
    Padding                       16
    ============================  ==========
    """

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        RESERVED = MultiRoller.FID.SOFTWARE_ID - 1
        ROLLER_ID = RESERVED - 1
        PADDING = ROLLER_ID - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        RESERVED = 0x4
        ROLLER_ID = 0x4
        PADDING = 0x10
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(fid=FID.ROLLER_ID, length=LEN.ROLLER_ID,
                 title="RollerId", name="roller_id",
                 checks=(CheckHexList(LEN.ROLLER_ID // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, function_index, roller_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param function_index: Function index
        :type function_index: ``int | HexList``
        :param roller_id: Roller Id
        :type roller_id: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=function_index,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.roller_id = roller_id
    # end def __init__
# end class RollerIdContainer


class GetCapabilities(ShortEmptyPacketDataFormat):
    """
    Define ``GetCapabilities`` implementation class
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
                         function_index=GetCapabilitiesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCapabilities


class GetRollerCapabilities(RollerIdContainer):
    """
    Define ``GetRollerCapabilities`` implementation class
    """
    def __init__(self, device_index, feature_index, roller_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param roller_id: Roller Id
        :type roller_id: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetRollerCapabilitiesResponseV0.FUNCTION_INDEX, roller_id=roller_id,
                         **kwargs)
    # end def __init__
# end class GetRollerCapabilities


class GetMode(RollerIdContainer):
    """
    Define ``GetMode`` implementation class
    """
    def __init__(self, device_index, feature_index, roller_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param roller_id: Roller Id
        :type roller_id: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetModeResponse.FUNCTION_INDEX, roller_id=roller_id,
                         **kwargs)
    # end def __init__
# end class GetMode


class SetMode(MultiRoller):
    """
    Define ``SetMode`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Roller Id                     8
    Roller Mode                   8
    Padding                       8
    ============================  ==========
    """

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        ROLLER_ID = MultiRoller.FID.SOFTWARE_ID - 1
        ROLLER_MODE = ROLLER_ID - 1
        PADDING = ROLLER_MODE - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        ROLLER_ID = 0x8
        ROLLER_MODE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.ROLLER_ID, length=LEN.ROLLER_ID,
                 title="RollerId", name="roller_id",
                 checks=(CheckHexList(LEN.ROLLER_ID // 8), CheckByte(),)),
        BitField(fid=FID.ROLLER_MODE, length=LEN.ROLLER_MODE,
                 title="RollerMode", name="roller_mode",
                 checks=(CheckHexList(LEN.ROLLER_MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, roller_id, divert, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param roller_id: Roller Id
        :type roller_id: ``int``
        :param divert: divert
        :type divert: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.roller_id = RollerId(reserved=roller_id >> RollerId.LEN.ROLLER_ID,
                                  roller_id=roller_id & (2 ** RollerId.LEN.ROLLER_ID - 1))
        self.roller_mode = RollerMode(reserved=divert >> RollerMode.LEN.DIVERT,
                                      divert=divert & (2 ** RollerMode.LEN.DIVERT - 1))
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``SetMode``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.roller_id = RollerId.fromHexList(
            inner_field_container_mixin.roller_id)
        inner_field_container_mixin.roller_mode = RollerMode.fromHexList(
            inner_field_container_mixin.roller_mode)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetMode


class GetCapabilitiesResponse(MultiRoller):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Num Roller                    8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        NUM_ROLLER = MultiRoller.FID.SOFTWARE_ID - 1
        PADDING = NUM_ROLLER - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        NUM_ROLLER = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.NUM_ROLLER, length=LEN.NUM_ROLLER,
                 title="NumRoller", name="num_roller",
                 checks=(CheckHexList(LEN.NUM_ROLLER // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, num_rollers, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param num_rollers: Num Rollers
        :type num_rollers: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.num_roller = NumRoller(num_rollers=num_rollers)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetCapabilitiesResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.num_roller = NumRoller.fromHexList(
            inner_field_container_mixin.num_roller)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetCapabilitiesResponse


class GetRollerCapabilitiesResponseV0(MultiRoller):
    """
    Define ``GetRollerCapabilitiesResponseV0`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Increments Per Rotation       8
    Increments Per Ratchet        8
    Capabilities                  8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRollerCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        INCREMENTS_PER_ROTATION = MultiRoller.FID.SOFTWARE_ID - 1
        INCREMENTS_PER_RATCHET = INCREMENTS_PER_ROTATION - 1
        CAPABILITIES = INCREMENTS_PER_RATCHET - 1
        PADDING = CAPABILITIES - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        INCREMENTS_PER_ROTATION = 0x8
        INCREMENTS_PER_RATCHET = 0x8
        CAPABILITIES = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.INCREMENTS_PER_ROTATION, length=LEN.INCREMENTS_PER_ROTATION,
                 title="IncrementsPerRotation", name="increments_per_rotation",
                 checks=(CheckHexList(LEN.INCREMENTS_PER_ROTATION // 8), CheckByte(),)),
        BitField(fid=FID.INCREMENTS_PER_RATCHET, length=LEN.INCREMENTS_PER_RATCHET,
                 title="IncrementsPerRatchet", name="increments_per_ratchet",
                 checks=(CheckHexList(LEN.INCREMENTS_PER_RATCHET // 8), CheckByte(),)),
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckHexList(LEN.CAPABILITIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CAPABILITIES) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, increments_per_rotation, increments_per_ratchet, lightbar_id,
                 **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param increments_per_rotation: Increments Per Rotation
        :type increments_per_rotation: ``int | HexList``
        :param increments_per_ratchet: Increments Per Ratchet
        :type increments_per_ratchet: ``int | HexList``
        :param lightbar_id: Lightbar Id
        :type lightbar_id: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.increments_per_rotation = HexList(Numeral(increments_per_rotation, self.LEN.INCREMENTS_PER_ROTATION // 8))
        self.increments_per_ratchet = HexList(Numeral(increments_per_ratchet, self.LEN.INCREMENTS_PER_RATCHET // 8))
        self.capabilities = CapabilitiesV0(lightbar_id=lightbar_id)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetRollerCapabilitiesResponseV0``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.capabilities = CapabilitiesV0.fromHexList(
            inner_field_container_mixin.capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetRollerCapabilitiesResponseV0


class GetRollerCapabilitiesResponseV1(MultiRoller):
    """
    Define ``GetRollerCapabilitiesResponseV1`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Increments Per Rotation       8
    Increments Per Ratchet        8
    Capabilities                  8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRollerCapabilities,)
    VERSION = (1,)
    FUNCTION_INDEX = 1

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        INCREMENTS_PER_ROTATION = MultiRoller.FID.SOFTWARE_ID - 1
        INCREMENTS_PER_RATCHET = INCREMENTS_PER_ROTATION - 1
        CAPABILITIES = INCREMENTS_PER_RATCHET - 1
        PADDING = CAPABILITIES - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        INCREMENTS_PER_ROTATION = 0x8
        INCREMENTS_PER_RATCHET = 0x8
        CAPABILITIES = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.INCREMENTS_PER_ROTATION, length=LEN.INCREMENTS_PER_ROTATION,
                 title="IncrementsPerRotation", name="increments_per_rotation",
                 checks=(CheckHexList(LEN.INCREMENTS_PER_ROTATION // 8), CheckByte(),)),
        BitField(fid=FID.INCREMENTS_PER_RATCHET, length=LEN.INCREMENTS_PER_RATCHET,
                 title="IncrementsPerRatchet", name="increments_per_ratchet",
                 checks=(CheckHexList(LEN.INCREMENTS_PER_RATCHET // 8), CheckByte(),)),
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckHexList(LEN.CAPABILITIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CAPABILITIES) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, increments_per_rotation, increments_per_ratchet, timestamp_report,
                 lightbar_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param increments_per_rotation: Increments Per Rotation
        :type increments_per_rotation: ``int | HexList``
        :param increments_per_ratchet: Increments Per Ratchet
        :type increments_per_ratchet: ``int | HexList``
        :param timestamp_report: Timestamp Report
        :type timestamp_report: ``int | HexList``
        :param lightbar_id: Lightbar Id
        :type lightbar_id: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.increments_per_rotation = HexList(Numeral(increments_per_rotation, self.LEN.INCREMENTS_PER_ROTATION // 8))
        self.increments_per_ratchet = HexList(Numeral(increments_per_ratchet, self.LEN.INCREMENTS_PER_RATCHET // 8))
        self.capabilities = CapabilitiesV1(timestamp_report=timestamp_report,
                                           lightbar_id=lightbar_id)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetRollerCapabilitiesResponseV1``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.capabilities = CapabilitiesV1.fromHexList(
            inner_field_container_mixin.capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetRollerCapabilitiesResponseV1


class GetModeResponse(MultiRoller):
    """
    Define ``GetModeResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Roller Mode                   8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetMode,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 2

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        ROLLER_MODE = MultiRoller.FID.SOFTWARE_ID - 1
        PADDING = ROLLER_MODE - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        ROLLER_MODE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.ROLLER_MODE, length=LEN.ROLLER_MODE,
                 title="RollerMode", name="roller_mode",
                 checks=(CheckHexList(LEN.ROLLER_MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, divert, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param divert: divert
        :type divert: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.roller_mode = RollerMode(divert=divert)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetModeResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.roller_mode = RollerMode.fromHexList(
            inner_field_container_mixin.roller_mode)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetModeResponse


class SetModeResponse(MultiRoller):
    """
    Define ``SetModeResponse`` implementation class
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Roller Id                     8
    Roller Mode                   8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetMode,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 3

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        ROLLER_ID = MultiRoller.FID.SOFTWARE_ID - 1
        ROLLER_MODE = ROLLER_ID - 1
        PADDING = ROLLER_MODE - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        ROLLER_ID = 0x8
        ROLLER_MODE = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.ROLLER_ID, length=LEN.ROLLER_ID,
                 title="RollerId", name="roller_id",
                 checks=(CheckHexList(LEN.ROLLER_ID // 8), CheckByte(),)),
        BitField(fid=FID.ROLLER_MODE, length=LEN.ROLLER_MODE,
                 title="RollerMode", name="roller_mode",
                 checks=(CheckHexList(LEN.ROLLER_MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, roller_id, divert, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param roller_id: Roller Id
        :type roller_id: ``int``
        :param divert: divert
        :type divert: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.roller_id = RollerId(reserved=roller_id >> RollerId.LEN.ROLLER_ID,
                                  roller_id=roller_id & (2 ** RollerId.LEN.ROLLER_ID - 1))
        self.roller_mode = RollerMode(reserved=divert >> RollerMode.LEN.DIVERT,
                                      divert=divert)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``SetModeResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.roller_id = RollerId.fromHexList(
            inner_field_container_mixin.roller_id)
        inner_field_container_mixin.roller_mode = RollerMode.fromHexList(
            inner_field_container_mixin.roller_mode)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetModeResponse


class RotationEventV0(MultiRoller):
    """
    Define ``RotationEventV0`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Roller Id                     8
    Delta                         8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(MultiRoller.FID):
        # See ``MultiRoller.FID``
        ROLLER_ID = MultiRoller.FID.SOFTWARE_ID - 1
        DELTA = ROLLER_ID - 1
        PADDING = DELTA - 1
    # end class FID

    class LEN(MultiRoller.LEN):
        # See ``MultiRoller.LEN``
        ROLLER_ID = 0x8
        DELTA = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = MultiRoller.FIELDS + (
        BitField(fid=FID.ROLLER_ID, length=LEN.ROLLER_ID,
                 title="RollerId", name="roller_id",
                 checks=(CheckHexList(LEN.ROLLER_ID // 8), CheckByte(),)),
        BitField(fid=FID.DELTA, length=LEN.DELTA,
                 title="Delta", name="delta",
                 checks=(CheckHexList(LEN.DELTA // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, roller_id, delta, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param roller_id: Roller Id
        :type roller_id: ``int | HexList``
        :param delta: Delta
        :type delta: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.roller_id = roller_id
        self.delta = HexList(Numeral(delta, self.LEN.DELTA // 8))
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``RotationEventV0``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.roller_id = RollerId.fromHexList(
            inner_field_container_mixin.roller_id)
        return inner_field_container_mixin
    # end def fromHexList
# end class RotationEventV0


class RotationEventV1(RotationEventV0):
    """
    Define ``RotationEventV1`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Roller Id                     8
    Delta                         8
    Report Timestamp              32
    Padding                       80
    ============================  ==========
    """
    VERSION = (1,)

    class FID(RotationEventV0.FID):
        # See ``MultiRoller.FID``
        REPORT_TIMESTAMP = RotationEventV0.FID.DELTA - 1
        PADDING = REPORT_TIMESTAMP - 1
    # end class FID

    class LEN(RotationEventV0.LEN):
        # See ``MultiRoller.LEN``
        REPORT_TIMESTAMP = 0x20
        PADDING = 0x50
    # end class LEN

    FIELDS = RotationEventV0.FIELDS[:-1] + (
        BitField(fid=FID.REPORT_TIMESTAMP, length=LEN.REPORT_TIMESTAMP,
                 title="ReportTimestamp", name="report_timestamp",
                 checks=(CheckHexList(LEN.REPORT_TIMESTAMP // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REPORT_TIMESTAMP) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MultiRoller.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, roller_id, delta, report_timestamp, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param roller_id: Roller Id
        :type roller_id: ``int | HexList``
        :param delta: Delta
        :type delta: ``int | HexList``
        :param report_timestamp: Report Timestamp
        :type report_timestamp: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         roller_id=roller_id, delta=delta,
                         **kwargs)

        report_timestamp_copy = HexList(report_timestamp.copy())
        report_timestamp_copy.addPadding(self.LEN.REPORT_TIMESTAMP // 8)
        self.report_timestamp = report_timestamp_copy
    # end def __init__
# end class RotationEventV1

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
