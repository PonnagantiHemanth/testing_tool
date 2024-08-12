#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.keyboard.lockkeystate
:brief: HID++ 2.0 ``LockKeyState`` command interface definition
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/03/18
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
class LockKeyState(HidppMessage):
    """
    | Define 0x4220 feature
    | The Lock Key State feature allows the software to display an OSD (on screen display)
    | when the keyboard's num lock, caps lock, scroll lock, compose or kana state changes.
    """
    FEATURE_ID = 0x4220
    MAX_FUNCTION_INDEX = 0

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

    class LockKeyStateMaskBitMap(BitFieldContainerMixin):
        """
        Define ``LockKeyStateMaskBitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      3
        Kana                          1
        Compose                       1
        Scroll Lock                   1
        Caps Lock                     1
        Num Lock                      1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            KANA = RESERVED - 1
            COMPOSE = KANA - 1
            SCROLL_LOCK = COMPOSE - 1
            CAPS_LOCK = SCROLL_LOCK - 1
            NUM_LOCK = CAPS_LOCK - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x3
            KANA = 0x1
            COMPOSE = 0x1
            SCROLL_LOCK = 0x1
            CAPS_LOCK = 0x1
            NUM_LOCK = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.KANA, length=LEN.KANA,
                     title="Kana", name="kana",
                     checks=(CheckInt(0, pow(2, LEN.KANA) - 1),)),
            BitField(fid=FID.COMPOSE, length=LEN.COMPOSE,
                     title="Compose", name="compose",
                     checks=(CheckInt(0, pow(2, LEN.COMPOSE) - 1),)),
            BitField(fid=FID.SCROLL_LOCK, length=LEN.SCROLL_LOCK,
                     title="ScrollLock", name="scroll_lock",
                     checks=(CheckInt(0, pow(2, LEN.SCROLL_LOCK) - 1),)),
            BitField(fid=FID.CAPS_LOCK, length=LEN.CAPS_LOCK,
                     title="CapsLock", name="caps_lock",
                     checks=(CheckInt(0, pow(2, LEN.CAPS_LOCK) - 1),)),
            BitField(fid=FID.NUM_LOCK, length=LEN.NUM_LOCK,
                     title="NumLock", name="num_lock",
                     checks=(CheckInt(0, pow(2, LEN.NUM_LOCK) - 1),)),
        )
    # end class LockKeyStateMaskBitMap
# end class LockKeyState


class LockKeyStateModel(FeatureModel):
    """
    Define ``LockKeyState`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_LOCK_KEY_STATE = 0

        # Event index
        LOCK_KEY_CHANGE = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``LockKeyState`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_LOCK_KEY_STATE: {
                    "request": GetLockKeyState,
                    "response": GetLockKeyStateResponse
                }
            },
            "events": {
                cls.INDEX.LOCK_KEY_CHANGE: {"report": LockKeyChangeEvent}
            }
        }

        return {
            "feature_base": LockKeyState,
            "versions": {
                LockKeyStateV0.VERSION: {
                    "main_cls": LockKeyStateV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class LockKeyStateModel


class LockKeyStateFactory(FeatureFactory):
    """
    Get ``LockKeyState`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``LockKeyState`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``LockKeyStateInterface``
        """
        return LockKeyStateModel.get_main_cls(version)()
    # end def create
# end class LockKeyStateFactory


class LockKeyStateInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``LockKeyState``
    """

    def __init__(self):
        # Requests
        self.get_lock_key_state_cls = None

        # Responses
        self.get_lock_key_state_response_cls = None

        # Events
        self.lock_key_change_event_cls = None
    # end def __init__
# end class LockKeyStateInterface


class LockKeyStateV0(LockKeyStateInterface):
    """
    Define ``LockKeyStateV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetLockKeyState() -> lockKeyStateMaskBitMap

    [Event 0] LockKeyChangeEvent -> lockKeyStateMaskBitMap
    """
    VERSION = 0

    def __init__(self):
        # See ``LockKeyState.__init__``
        super().__init__()
        index = LockKeyStateModel.INDEX

        # Requests
        self.get_lock_key_state_cls = LockKeyStateModel.get_request_cls(
            self.VERSION, index.GET_LOCK_KEY_STATE)

        # Responses
        self.get_lock_key_state_response_cls = LockKeyStateModel.get_response_cls(
            self.VERSION, index.GET_LOCK_KEY_STATE)

        # Events
        self.lock_key_change_event_cls = LockKeyStateModel.get_report_cls(
            self.VERSION, index.LOCK_KEY_CHANGE)
    # end def __init__

    def get_max_function_index(self):
        # See ``LockKeyStateInterface.get_max_function_index``
        return LockKeyStateModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class LockKeyStateV0


class ShortEmptyPacketDataFormat(LockKeyState):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetLockKeyState

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(LockKeyState.FID):
        # See ``LockKeyState.FID``
        PADDING = LockKeyState.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(LockKeyState.LEN):
        # See ``LockKeyState.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = LockKeyState.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LockKeyState.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LockKeyStateFormat(LockKeyState):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetLockKeyStateResponse
        - LockKeyChangeEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Lock Key State Mask Bit Map   8
    Padding                       120
    ============================  ==========
    """

    class FID(LockKeyState.FID):
        # See ``LockKeyState.FID``
        LOCK_KEY_STATE_MASK_BIT_MAP = LockKeyState.FID.SOFTWARE_ID - 1
        PADDING = LOCK_KEY_STATE_MASK_BIT_MAP - 1
    # end class FID

    class LEN(LockKeyState.LEN):
        # See ``LockKeyState.LEN``
        LOCK_KEY_STATE_MASK_BIT_MAP = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = LockKeyState.FIELDS + (
        BitField(fid=FID.LOCK_KEY_STATE_MASK_BIT_MAP, length=LEN.LOCK_KEY_STATE_MASK_BIT_MAP,
                 title="LockKeyStateMaskBitMap", name="lock_key_state_mask_bit_map",
                 checks=(CheckHexList(LEN.LOCK_KEY_STATE_MASK_BIT_MAP // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LockKeyState.DEFAULT.PADDING),
    )
# end class LockKeyStateFormat


class GetLockKeyState(ShortEmptyPacketDataFormat):
    """
    Define ``GetLockKeyState`` implementation class for version 0
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
                         functionIndex=GetLockKeyStateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetLockKeyState


class GetLockKeyStateResponse(LockKeyStateFormat):
    """
    Define ``GetLockKeyStateResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetLockKeyState,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, kana, compose, scroll_lock, caps_lock, num_lock, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kana: Kana Key
        :type kana: ``bool`` or ``HexList``
        :param compose: Compose Key
        :type compose: ``bool`` or ``HexList``
        :param scroll_lock: Scroll Lock Key
        :type scroll_lock: ``bool`` or ``HexList``
        :param caps_lock: Caps Lock Key
        :type caps_lock: ``bool`` or ``HexList``
        :param num_lock: Num Lock Key
        :type num_lock: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.lock_key_state_mask_bit_map = self.LockKeyStateMaskBitMap(kana=kana,
                                                                       compose=compose,
                                                                       scroll_lock=scroll_lock,
                                                                       caps_lock=caps_lock,
                                                                       num_lock=num_lock)
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
        :rtype: ``GetLockKeyStateResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.lock_key_state_mask_bit_map = cls.LockKeyStateMaskBitMap.fromHexList(
            inner_field_container_mixin.lock_key_state_mask_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetLockKeyStateResponse


class LockKeyChangeEvent(LockKeyStateFormat):
    """
    Define ``LockKeyChangeEvent`` implementation class for version 0
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, kana, compose, scroll_lock, caps_lock, num_lock, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kana: Kana Key
        :type kana: ``bool`` or ``HexList``
        :param compose: Compose Key
        :type compose: ``bool`` or ``HexList``
        :param scroll_lock: Scroll Lock Key
        :type scroll_lock: ``bool`` or ``HexList``
        :param caps_lock: Caps Lock Key
        :type caps_lock: ``bool`` or ``HexList``
        :param num_lock: Num Lock Key
        :type num_lock: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.lock_key_state_mask_bit_map = self.LockKeyStateMaskBitMap(kana=kana,
                                                                       compose=compose,
                                                                       scroll_lock=scroll_lock,
                                                                       caps_lock=caps_lock,
                                                                       num_lock=num_lock)
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
        :rtype: ``LockKeyChangeEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.lock_key_state_mask_bit_map = cls.LockKeyStateMaskBitMap.fromHexList(
            inner_field_container_mixin.lock_key_state_mask_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class LockKeyChangeEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
