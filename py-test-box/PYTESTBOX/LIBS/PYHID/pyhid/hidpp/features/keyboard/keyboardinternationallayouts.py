#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.keyboard.keyboardinternationallayouts
:brief: HID++ 2.0 ``KeyboardInternationalLayouts`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyboardInternationalLayouts(HidppMessage):
    """
    This feature provides the ability to query for the keyboard international layout.
    """
    FEATURE_ID = 0x4540
    MAX_FUNCTION_INDEX = 0

    # Property identifier on nvs
    PROPERTY_ID = 2

    class LAYOUT(IntEnum):
        """
        Supported Keyboard Layouts

        https://github.com/Logitech/cpg-samarkand-hidpp-docs/blob/master/docs/x4540_keyboardinternationallayouts_v0.adoc
        """
        UNKNOWN = 0
        US = 1
        US_INTERNATIONAL_105_KEYS = 2
        UK = 3
        GERMAN = 4
        FRENCH = 5
        GERMAN_FRENCH = 6
        RUSSIAN = 7
        PAN_NORDIC = 8
        KOREAN = 9
        JAPANESE = 10
        CHINESE_TRADITIONAL = 11
        CHINESE_SIMPLIFIED = 12
        SWISS = 13
        TURKISH = 14
        SPANISH = 15
        ARABIC = 16
        BELGIAN = 17
        CANADIAN_BILINGUAL = 18
        CANADIAN_FRENCH = 19
        CZECH = 20
        DANISH = 21
        FINNISH = 22
        GREEK = 23
        HEBREW = 24
        HUNGARY = 25
        ITALIAN = 26
        LATIN_AMERICAN = 27
        NETHERLANDS_DUTCH = 28
        NORWEGIAN = 29
        POLAND = 30
        PORTUGUESE = 31
        SLOVAKIA = 32
        SWEDISH = 33
        SWISS_FRENCH = 34
        YUGOSLAVIA = 35
        TURKISH_F = 36
        ICELANDIC = 37
        ROMANIAN = 38
        LATVIAN = 39
        BULGARIAN = 40
        ESTONIAN = 41
        LITHUANIAN = 42
        SERBIAN_CYRILLIC = 43
        SLAVONIC_MULTILINGUAL = 44
        UKRAINIAN = 45
        KAZAKH = 46
        CHINESE_CANGJIE = 47
        CHINESE_ZHUYIN = 48
        CHINESE_DAYI = 49
        CHINESE_WUBI = 50
        THAI = 51
        VIETNAMESE = 52
        MALAYSIA = 53
        INDIA = 54
        US_INTERNATIONAL_104_KEYS = 55
        PORTUGUESE_BRAZILIAN = 56
        # Since V1
        FARSI = 57
        ARABIC_ANSI = 58
        RUSSIAN_ISO = 59
        BIJOY = 60
        JAPANESE_INTERNATIONAL = 61
        KOREAN_ANSI = 62
        GERMAN_GS = 63
        CROATIAN_SLOVENIAN = 64
        CZECH_SLOVAKIAN = 65
        HINDI = 66
    # end class LAYOUT

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class KeyboardInternationalLayouts


# noinspection DuplicatedCode
class KeyboardInternationalLayoutsModel(FeatureModel):
    """
    Define ``KeyboardInternationalLayouts`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_KEYBOARD_LAYOUT = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``KeyboardInternationalLayouts`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0_to_v1 = {
            "functions": {
                cls.INDEX.GET_KEYBOARD_LAYOUT: {
                    "request": GetKeyboardLayout,
                    "response": GetKeyboardLayoutResponse
                }
            }
        }

        return {
            "feature_base": KeyboardInternationalLayouts,
            "versions": {
                KeyboardInternationalLayoutsV0.VERSION: {
                    "main_cls": KeyboardInternationalLayoutsV0,
                    "api": function_map_v0_to_v1
                },
                KeyboardInternationalLayoutsV1.VERSION: {
                    "main_cls": KeyboardInternationalLayoutsV1,
                    "api": function_map_v0_to_v1
                },
            }
        }
    # end def _get_data_model
# end class KeyboardInternationalLayoutsModel


class KeyboardInternationalLayoutsFactory(FeatureFactory):
    """
    Get ``KeyboardInternationalLayouts`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``KeyboardInternationalLayouts`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``KeyboardInternationalLayoutsInterface``
        """
        return KeyboardInternationalLayoutsModel.get_main_cls(version)()
    # end def create
# end class KeyboardInternationalLayoutsFactory


class KeyboardInternationalLayoutsInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``KeyboardInternationalLayouts``
    """

    def __init__(self):
        # Requests
        self.get_keyboard_layout_cls = None

        # Responses
        self.get_keyboard_layout_response_cls = None
    # end def __init__
# end class KeyboardInternationalLayoutsInterface


class KeyboardInternationalLayoutsV0(KeyboardInternationalLayoutsInterface):
    """
    Define ``KeyboardInternationalLayoutsV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetKeyboardLayout() -> keyboardlayout
    """
    VERSION = 0

    def __init__(self):
        # See ``KeyboardInternationalLayouts.__init__``
        super().__init__()
        index = KeyboardInternationalLayoutsModel.INDEX

        # Requests
        self.get_keyboard_layout_cls = KeyboardInternationalLayoutsModel.get_request_cls(
            self.VERSION, index.GET_KEYBOARD_LAYOUT)

        # Responses
        self.get_keyboard_layout_response_cls = KeyboardInternationalLayoutsModel.get_response_cls(
            self.VERSION, index.GET_KEYBOARD_LAYOUT)
    # end def __init__

    def get_max_function_index(self):
        # See ``KeyboardInternationalLayoutsInterface.get_max_function_index``
        return KeyboardInternationalLayoutsModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index

    @staticmethod
    def get_max_layout_id():
        """
        Return the maximum layout id support by the feature version

        :return: Maximum supported keyboard layout
        :rtype: ``int``
        """
        return KeyboardInternationalLayouts.LAYOUT.PORTUGUESE_BRAZILIAN.value
    # end def get_max_layout_id
# end class KeyboardInternationalLayoutsV0


class KeyboardInternationalLayoutsV1(KeyboardInternationalLayoutsV0):
    """
    Define ``KeyboardInternationalLayoutsV1`` feature

    This feature provides model and unit specific information for version 1
    """
    VERSION = 1

    @staticmethod
    def get_max_layout_id():
        # See ``KeyboardInternationalLayoutsV0.get_max_layout_id``
        return KeyboardInternationalLayouts.LAYOUT.HINDI.value
    # end def get_max_layout_id
# end class KeyboardInternationalLayoutsV1


class ShortEmptyPacketDataFormat(KeyboardInternationalLayouts):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetKeyboardLayout

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(KeyboardInternationalLayouts.FID):
        # See ``KeyboardInternationalLayouts.FID``
        PADDING = KeyboardInternationalLayouts.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(KeyboardInternationalLayouts.LEN):
        # See ``KeyboardInternationalLayouts.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = KeyboardInternationalLayouts.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=KeyboardInternationalLayouts.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class GetKeyboardLayout(ShortEmptyPacketDataFormat):
    """
    Define ``GetKeyboardLayout`` implementation class for version 0
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
                         function_index=GetKeyboardLayoutResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetKeyboardLayout


class GetKeyboardLayoutResponse(KeyboardInternationalLayouts):
    """
    Define ``GetKeyboardLayoutResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    keyboard layout               8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetKeyboardLayout,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(KeyboardInternationalLayouts.FID):
        # See ``KeyboardInternationalLayouts.FID``
        KEYBOARD_LAYOUT = KeyboardInternationalLayouts.FID.SOFTWARE_ID - 1
        PADDING = KEYBOARD_LAYOUT - 1
    # end class FID

    class LEN(KeyboardInternationalLayouts.LEN):
        # See ``KeyboardInternationalLayouts.LEN``
        KEYBOARD_LAYOUT = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = KeyboardInternationalLayouts.FIELDS + (
        BitField(fid=FID.KEYBOARD_LAYOUT, length=LEN.KEYBOARD_LAYOUT,
                 title="KeyboardLayout", name="keyboard_layout",
                 checks=(CheckHexList(LEN.KEYBOARD_LAYOUT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=KeyboardInternationalLayouts.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, keyboard_layout, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param keyboard_layout: This feature provides the ability to query for the keyboard international layout.
        :type keyboard_layout: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.keyboard_layout = keyboard_layout
    # end def __init__
# end class GetKeyboardLayoutResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
