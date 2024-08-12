#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.mouse.ratchetwheel
:brief: HID++ 2.0 ``RatchetWheel`` command interface definition
:author: Gautham S B  <gsb@logitech.com>
:date: 2022/11/30
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
class RatchetWheel(HidppMessage):
    """
    Diverting of wheel movement reporting to HID++ events for standard ratchet wheels.

    When reports are diverted to HID++ they are not reported on HID.
    """
    FEATURE_ID = 0x2130
    MAX_FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        # noinspection PyTypeChecker
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__

    class Flag(BitFieldContainerMixin):
        """
        Define ``Flag`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Divert                        1
        ============================  ==========
        """

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

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            DIVERT = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.DIVERT, length=LEN.DIVERT,
                     title="Divert", name="divert",
                     checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),),
                     default_value=DEFAULT.DIVERT),
        )
    # end class Flag

    class DIVERT:
        """
        Define ``RatchetWheel`` divert values for HID and HID++ reporting
        """
        HID = 0
        HIDPP = 1
    # end class DIVERT
# end class RatchetWheel


class RatchetWheelModel(FeatureModel):
    """
    Define ``RatchetWheel`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_WHEEL_MODE = 0
        SET_MODE_STATUS = 1

        # Event index
        WHEEL_MOVEMENT = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``RatchetWheel`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_WHEEL_MODE: {
                    "request": GetWheelMode,
                    "response": GetWheelModeResponse
                },
                cls.INDEX.SET_MODE_STATUS: {
                    "request": SetModeStatus,
                    "response": SetModeStatusResponse
                }
            },
            "events": {
                cls.INDEX.WHEEL_MOVEMENT: {"report": WheelMovementEvent}
            }
        }

        return {
            "feature_base": RatchetWheel,
            "versions": {
                RatchetWheelV0.VERSION: {
                    "main_cls": RatchetWheelV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class RatchetWheelModel


class RatchetWheelFactory(FeatureFactory):
    """
    Get ``RatchetWheel`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``RatchetWheel`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``RatchetWheelInterface``
        """
        return RatchetWheelModel.get_main_cls(version)()
    # end def create
# end class RatchetWheelFactory


class RatchetWheelInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``RatchetWheel``
    """

    def __init__(self):
        # Requests
        self.get_wheel_mode_cls = None
        self.set_mode_status_cls = None

        # Responses
        self.get_wheel_mode_response_cls = None
        self.set_mode_status_response_cls = None

        # Events
        self.wheel_movement_event_cls = None
    # end def __init__
# end class RatchetWheelInterface


class RatchetWheelV0(RatchetWheelInterface):
    """
    Define ``RatchetWheelV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetWheelMode() -> Flag

    [1] SetModeStatus(Flag) -> Flag

    [Event 0] WheelMovementEvent -> DeltaV, DeltaH
    """
    VERSION = 0

    def __init__(self):
        # See ``RatchetWheel.__init__``
        super().__init__()
        index = RatchetWheelModel.INDEX

        # Requests
        self.get_wheel_mode_cls = RatchetWheelModel.get_request_cls(
            self.VERSION, index.GET_WHEEL_MODE)
        self.set_mode_status_cls = RatchetWheelModel.get_request_cls(
            self.VERSION, index.SET_MODE_STATUS)

        # Responses
        self.get_wheel_mode_response_cls = RatchetWheelModel.get_response_cls(
            self.VERSION, index.GET_WHEEL_MODE)
        self.set_mode_status_response_cls = RatchetWheelModel.get_response_cls(
            self.VERSION, index.SET_MODE_STATUS)

        # Events
        self.wheel_movement_event_cls = RatchetWheelModel.get_report_cls(
            self.VERSION, index.WHEEL_MOVEMENT)
    # end def __init__

    def get_max_function_index(self):
        # See ``RatchetWheelInterface.get_max_function_index``
        return RatchetWheelModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class RatchetWheelV0


class ShortEmptyPacketDataFormat(RatchetWheel):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetWheelMode

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(RatchetWheel.FID):
        # See ``RatchetWheel.FID``
        PADDING = RatchetWheel.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(RatchetWheel.LEN):
        # See ``RatchetWheel.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = RatchetWheel.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RatchetWheel.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class WheelModeResponseHead(RatchetWheel):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetWheelModeResponse
        - SetModeStatusResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Flag                          8
    Padding                       120
    ============================  ==========
    """

    class FID(RatchetWheel.FID):
        # See ``RatchetWheel.FID``
        FLAG = RatchetWheel.FID.SOFTWARE_ID - 1
        PADDING = FLAG - 1
    # end class FID

    class LEN(RatchetWheel.LEN):
        # See ``RatchetWheel.LEN``
        FLAG = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = RatchetWheel.FIELDS + (
        BitField(fid=FID.FLAG, length=LEN.FLAG,
                 title="Flag", name="flag",
                 checks=(CheckHexList(LEN.FLAG // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RatchetWheel.DEFAULT.PADDING),
    )
# end class MixedContainer1


class GetWheelMode(ShortEmptyPacketDataFormat):
    """
    Define ``GetWheelMode`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetWheelModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetWheelMode


class GetWheelModeResponse(WheelModeResponseHead):
    """
    Define ``GetWheelModeResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetWheelMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, divert, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param divert: Divert
        :type divert: ``bool | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.flag = self.Flag(divert=divert)
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
        :rtype: ``GetWheelModeResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.flag = cls.Flag.fromHexList(
            inner_field_container_mixin.flag)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetWheelModeResponse


class SetModeStatus(RatchetWheel):
    """
    Define ``SetModeStatus`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Flag                          8
    Padding                       16
    ============================  ==========
    """

    class FID(RatchetWheel.FID):
        # See ``RatchetWheel.FID``
        FLAG = RatchetWheel.FID.SOFTWARE_ID - 1
        PADDING = FLAG - 1
    # end class FID

    class LEN(RatchetWheel.LEN):
        # See ``RatchetWheel.LEN``
        FLAG = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = RatchetWheel.FIELDS + (
        BitField(fid=FID.FLAG, length=LEN.FLAG,
                 title="Flag", name="flag",
                 checks=(CheckHexList(LEN.FLAG // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RatchetWheel.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, divert, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param divert: Divert
        :type divert: ``bool | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetModeStatusResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.flag = self.Flag(divert=divert)
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
        inner_field_container_mixin.flag = cls.Flag.fromHexList(
            inner_field_container_mixin.flag)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetModeStatus


class SetModeStatusResponse(WheelModeResponseHead):
    """
    Define ``SetModeStatusResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetModeStatus,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, divert, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param divert: Divert
        :type divert: ``bool | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.flag = self.Flag(divert=divert)
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
        :rtype: ``SetModeStatusResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.flag = cls.Flag.fromHexList(
            inner_field_container_mixin.flag)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetModeStatusResponse


class WheelMovementEvent(RatchetWheel):
    """
    Define ``WheelMovementEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Delta V                       8
    Delta H                       8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(RatchetWheel.FID):
        # See ``RatchetWheel.FID``
        DELTA_V = RatchetWheel.FID.SOFTWARE_ID - 1
        DELTA_H = DELTA_V - 1
        PADDING = DELTA_H - 1
    # end class FID

    class LEN(RatchetWheel.LEN):
        # See ``RatchetWheel.LEN``
        DELTA_V = 0x8
        DELTA_H = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = RatchetWheel.FIELDS + (
        BitField(fid=FID.DELTA_V, length=LEN.DELTA_V,
                 title="DeltaV", name="delta_v",
                 checks=(CheckHexList(LEN.DELTA_V // 8),
                         CheckByte(),)),
        BitField(fid=FID.DELTA_H, length=LEN.DELTA_H,
                 title="DeltaH", name="delta_h",
                 checks=(CheckHexList(LEN.DELTA_H // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RatchetWheel.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, delta_v, delta_h, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param delta_v: Vertical wheel motion delta. Moving away from the user produces positive values.
        :type delta_v: ``int | HexList``
        :param delta_h: Horizontal wheel motion delta. Moving to the right produces positive values.
        :type delta_h: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.delta_v = delta_v
        self.delta_h = delta_h
    # end def __init__
# end class WheelMovementEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
