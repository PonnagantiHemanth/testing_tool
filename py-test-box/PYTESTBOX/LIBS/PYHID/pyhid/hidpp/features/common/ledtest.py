#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.ledtest
:brief: HID++ 2.0 ``LEDTest`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/05
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
class LEDTest(HidppMessage):
    """
    Test LED's implemented in a project
    """
    FEATURE_ID = 0x18A1
    MAX_FUNCTION_INDEX_V0 = 2

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

    # noinspection DuplicatedCode

    class LEDMask1BitMap(BitFieldContainerMixin):
        """
        Define ``LEDMaskBitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Battery Green LED             1
        Battery Red LED               1
        Roller LED                    1
        Caps Lock LED                 1
        Backlight LED                 1
        RGB                           1
        Reserved                      2
        ============================  ==========
        """
        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            RGB = RESERVED - 1
            BACKLIGHT_LED = RGB - 1
            CAPS_LOCK_LED = BACKLIGHT_LED - 1
            ROLLER_LED = CAPS_LOCK_LED - 1
            BATTERY_RED_LED = ROLLER_LED - 1
            BATTERY_GREEN_LED = BATTERY_RED_LED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x2
            RGB = 0x1
            BACKLIGHT_LED = 0x1
            CAPS_LOCK_LED = 0x1
            ROLLER_LED = 0x1
            BATTERY_RED_LED = 0x1
            BATTERY_GREEN_LED = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            RGB = 0x0
            BACKLIGHT_LED = 0x0
            CAPS_LOCK_LED = 0x0
            ROLLER_LED = 0x0
            BATTERY_RED_LED = 0x0
            BATTERY_GREEN_LED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.RGB, length=LEN.RGB,
                     title="Rgb", name="rgb",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RGB) - 1),),
                     default_value=DEFAULT.RGB),
            BitField(fid=FID.BACKLIGHT_LED, length=LEN.BACKLIGHT_LED,
                     title="BacklightLed", name="backlight_led",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BACKLIGHT_LED) - 1),),
                     default_value=DEFAULT.BACKLIGHT_LED),
            BitField(fid=FID.CAPS_LOCK_LED, length=LEN.CAPS_LOCK_LED,
                     title="CapsLockLed", name="caps_lock_led",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.CAPS_LOCK_LED) - 1),),
                     default_value=DEFAULT.CAPS_LOCK_LED),
            BitField(fid=FID.ROLLER_LED, length=LEN.ROLLER_LED,
                     title="RollerLed", name="roller_led",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ROLLER_LED) - 1),),
                     default_value=DEFAULT.ROLLER_LED),
            BitField(fid=FID.BATTERY_RED_LED, length=LEN.BATTERY_RED_LED,
                     title="BatteryRedLed", name="battery_red_led",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BATTERY_RED_LED) - 1),),
                     default_value=DEFAULT.BATTERY_RED_LED),
            BitField(fid=FID.BATTERY_GREEN_LED, length=LEN.BATTERY_GREEN_LED,
                     title="BatteryGreenLed", name="battery_green_led",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BATTERY_GREEN_LED) - 1),),
                     default_value=DEFAULT.BATTERY_GREEN_LED),
        )
    # end class LEDMask1BitMap

    # noinspection DuplicatedCode
    class LEDGenericMask1BitMap(BitFieldContainerMixin):
        """
        Define ``LEDGenericMask1BitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Product Specific LED 0        1
        Product Specific LED 1        1
        Product Specific LED 2        1
        Product Specific LED 3        1
        Product Specific LED 4        1
        Product Specific LED 5        1
        Product Specific LED 6        1
        Product Specific LED 7        1
        ============================  ==========
        """
        class FID(object):
            """
            Field identifiers
            """
            PRODUCT_SPECIFIC_LED_7 = 0xFF
            PRODUCT_SPECIFIC_LED_6 = PRODUCT_SPECIFIC_LED_7 - 1
            PRODUCT_SPECIFIC_LED_5 = PRODUCT_SPECIFIC_LED_6 - 1
            PRODUCT_SPECIFIC_LED_4 = PRODUCT_SPECIFIC_LED_5 - 1
            PRODUCT_SPECIFIC_LED_3 = PRODUCT_SPECIFIC_LED_4 - 1
            PRODUCT_SPECIFIC_LED_2 = PRODUCT_SPECIFIC_LED_3 - 1
            PRODUCT_SPECIFIC_LED_1 = PRODUCT_SPECIFIC_LED_2 - 1
            PRODUCT_SPECIFIC_LED_0 = PRODUCT_SPECIFIC_LED_1 - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            PRODUCT_SPECIFIC_LED_7 = 0x1
            PRODUCT_SPECIFIC_LED_6 = 0x1
            PRODUCT_SPECIFIC_LED_5 = 0x1
            PRODUCT_SPECIFIC_LED_4 = 0x1
            PRODUCT_SPECIFIC_LED_3 = 0x1
            PRODUCT_SPECIFIC_LED_2 = 0x1
            PRODUCT_SPECIFIC_LED_1 = 0x1
            PRODUCT_SPECIFIC_LED_0 = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            PRODUCT_SPECIFIC_LED_7 = 0x0
            PRODUCT_SPECIFIC_LED_6 = 0x0
            PRODUCT_SPECIFIC_LED_5 = 0x0
            PRODUCT_SPECIFIC_LED_4 = 0x0
            PRODUCT_SPECIFIC_LED_3 = 0x0
            PRODUCT_SPECIFIC_LED_2 = 0x0
            PRODUCT_SPECIFIC_LED_1 = 0x0
            PRODUCT_SPECIFIC_LED_0 = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_7, length=LEN.PRODUCT_SPECIFIC_LED_7,
                     title="ProductSpecificLed7", name="product_specific_led_7",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_7) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_7),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_6, length=LEN.PRODUCT_SPECIFIC_LED_6,
                     title="ProductSpecificLed6", name="product_specific_led_6",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_6) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_6),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_5, length=LEN.PRODUCT_SPECIFIC_LED_5,
                     title="ProductSpecificLed5", name="product_specific_led_5",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_5) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_5),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_4, length=LEN.PRODUCT_SPECIFIC_LED_4,
                     title="ProductSpecificLed4", name="product_specific_led_4",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_4) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_4),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_3, length=LEN.PRODUCT_SPECIFIC_LED_3,
                     title="ProductSpecificLed3", name="product_specific_led_3",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_3) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_3),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_2, length=LEN.PRODUCT_SPECIFIC_LED_2,
                     title="ProductSpecificLed2", name="product_specific_led_2",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_2) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_2),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_1, length=LEN.PRODUCT_SPECIFIC_LED_1,
                     title="ProductSpecificLed1", name="product_specific_led_1",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_1) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_1),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_0, length=LEN.PRODUCT_SPECIFIC_LED_0,
                     title="ProductSpecificLed0", name="product_specific_led_0",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_0) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_0),
        )
    # end class LEDGenericMask1BitMap

    # noinspection DuplicatedCode
    class LEDGenericMask2BitMap(BitFieldContainerMixin):
        """
        Define ``LEDGenericMask2BitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Product Specific LED 8        1
        Product Specific LED 9        1
        Product Specific LED 10       1
        Product Specific LED 11       1
        Product Specific LED 12       1
        Product Specific LED 13       1
        Product Specific LED 14       1
        Product Specific LED 15       1
        ============================  ==========
        """
        class FID(object):
            """
            Field identifiers
            """
            PRODUCT_SPECIFIC_LED_15 = 0xFF
            PRODUCT_SPECIFIC_LED_14 = PRODUCT_SPECIFIC_LED_15 - 1
            PRODUCT_SPECIFIC_LED_13 = PRODUCT_SPECIFIC_LED_14 - 1
            PRODUCT_SPECIFIC_LED_12 = PRODUCT_SPECIFIC_LED_13 - 1
            PRODUCT_SPECIFIC_LED_11 = PRODUCT_SPECIFIC_LED_12 - 1
            PRODUCT_SPECIFIC_LED_10 = PRODUCT_SPECIFIC_LED_11 - 1
            PRODUCT_SPECIFIC_LED_9 = PRODUCT_SPECIFIC_LED_10 - 1
            PRODUCT_SPECIFIC_LED_8 = PRODUCT_SPECIFIC_LED_9 - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            PRODUCT_SPECIFIC_LED_15 = 0x1
            PRODUCT_SPECIFIC_LED_14 = 0x1
            PRODUCT_SPECIFIC_LED_13 = 0x1
            PRODUCT_SPECIFIC_LED_12 = 0x1
            PRODUCT_SPECIFIC_LED_11 = 0x1
            PRODUCT_SPECIFIC_LED_10 = 0x1
            PRODUCT_SPECIFIC_LED_9 = 0x1
            PRODUCT_SPECIFIC_LED_8 = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            PRODUCT_SPECIFIC_LED_15 = 0x0
            PRODUCT_SPECIFIC_LED_14 = 0x0
            PRODUCT_SPECIFIC_LED_13 = 0x0
            PRODUCT_SPECIFIC_LED_12 = 0x0
            PRODUCT_SPECIFIC_LED_11 = 0x0
            PRODUCT_SPECIFIC_LED_10 = 0x0
            PRODUCT_SPECIFIC_LED_9 = 0x0
            PRODUCT_SPECIFIC_LED_8 = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_15, length=LEN.PRODUCT_SPECIFIC_LED_15,
                     title="ProductSpecificLed15", name="product_specific_led_15",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_15) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_15),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_14, length=LEN.PRODUCT_SPECIFIC_LED_14,
                     title="ProductSpecificLed14", name="product_specific_led_14",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_14) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_14),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_13, length=LEN.PRODUCT_SPECIFIC_LED_13,
                     title="ProductSpecificLed13", name="product_specific_led_13",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_13) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_13),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_12, length=LEN.PRODUCT_SPECIFIC_LED_12,
                     title="ProductSpecificLed12", name="product_specific_led_12",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_12) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_12),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_11, length=LEN.PRODUCT_SPECIFIC_LED_11,
                     title="ProductSpecificLed11", name="product_specific_led_11",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_11) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_11),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_10, length=LEN.PRODUCT_SPECIFIC_LED_10,
                     title="ProductSpecificLed10", name="product_specific_led_10",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_10) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_10),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_9, length=LEN.PRODUCT_SPECIFIC_LED_9,
                     title="ProductSpecificLed9", name="product_specific_led_9",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_9) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_9),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_8, length=LEN.PRODUCT_SPECIFIC_LED_8,
                     title="ProductSpecificLed8", name="product_specific_led_8",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_8) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_8),
        )
    # end class LEDGenericMask2BitMap

    # noinspection DuplicatedCode
    class LEDGenericMask3BitMap(BitFieldContainerMixin):
        """
        Define ``LEDGenericMask3BitMap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Product Specific LED 16       1
        Product Specific LED 17       1
        Product Specific LED 18       1
        Product Specific LED 19       1
        Product Specific LED 20       1
        Product Specific LED 21       1
        Product Specific LED 22       1
        Product Specific LED 23       1
        ============================  ==========
        """
        class FID(object):
            """
            Field identifiers
            """
            PRODUCT_SPECIFIC_LED_23 = 0xFF
            PRODUCT_SPECIFIC_LED_22 = PRODUCT_SPECIFIC_LED_23 - 1
            PRODUCT_SPECIFIC_LED_21 = PRODUCT_SPECIFIC_LED_22 - 1
            PRODUCT_SPECIFIC_LED_20 = PRODUCT_SPECIFIC_LED_21 - 1
            PRODUCT_SPECIFIC_LED_19 = PRODUCT_SPECIFIC_LED_20 - 1
            PRODUCT_SPECIFIC_LED_18 = PRODUCT_SPECIFIC_LED_19 - 1
            PRODUCT_SPECIFIC_LED_17 = PRODUCT_SPECIFIC_LED_18 - 1
            PRODUCT_SPECIFIC_LED_16 = PRODUCT_SPECIFIC_LED_17 - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            PRODUCT_SPECIFIC_LED_23 = 0x1
            PRODUCT_SPECIFIC_LED_22 = 0x1
            PRODUCT_SPECIFIC_LED_21 = 0x1
            PRODUCT_SPECIFIC_LED_20 = 0x1
            PRODUCT_SPECIFIC_LED_19 = 0x1
            PRODUCT_SPECIFIC_LED_18 = 0x1
            PRODUCT_SPECIFIC_LED_17 = 0x1
            PRODUCT_SPECIFIC_LED_16 = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            PRODUCT_SPECIFIC_LED_23 = 0x0
            PRODUCT_SPECIFIC_LED_22 = 0x0
            PRODUCT_SPECIFIC_LED_21 = 0x0
            PRODUCT_SPECIFIC_LED_20 = 0x0
            PRODUCT_SPECIFIC_LED_19 = 0x0
            PRODUCT_SPECIFIC_LED_18 = 0x0
            PRODUCT_SPECIFIC_LED_17 = 0x0
            PRODUCT_SPECIFIC_LED_16 = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_23, length=LEN.PRODUCT_SPECIFIC_LED_23,
                     title="ProductSpecificLed23", name="product_specific_led_23",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_23) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_23),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_22, length=LEN.PRODUCT_SPECIFIC_LED_22,
                     title="ProductSpecificLed22", name="product_specific_led_22",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_22) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_22),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_21, length=LEN.PRODUCT_SPECIFIC_LED_21,
                     title="ProductSpecificLed21", name="product_specific_led_21",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_21) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_21),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_20, length=LEN.PRODUCT_SPECIFIC_LED_20,
                     title="ProductSpecificLed20", name="product_specific_led_20",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_20) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_20),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_19, length=LEN.PRODUCT_SPECIFIC_LED_19,
                     title="ProductSpecificLed19", name="product_specific_led_19",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_19) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_19),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_18, length=LEN.PRODUCT_SPECIFIC_LED_18,
                     title="ProductSpecificLed18", name="product_specific_led_18",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_18) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_18),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_17, length=LEN.PRODUCT_SPECIFIC_LED_17,
                     title="ProductSpecificLed17", name="product_specific_led_17",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_17) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_17),
            BitField(fid=FID.PRODUCT_SPECIFIC_LED_16, length=LEN.PRODUCT_SPECIFIC_LED_16,
                     title="ProductSpecificLed16", name="product_specific_led_16",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_LED_16) - 1),),
                     default_value=DEFAULT.PRODUCT_SPECIFIC_LED_16),
        )
    # end class LEDGenericMask3Bitmap

    # noinspection DuplicatedCode
    class LEDMaskPresence1BitMap(LEDMask1BitMap):
        """
        Define ``LEDMaskPresence1BitMap`` information
        """
    # end class LEDMaskPresence1BitMap

    # noinspection DuplicatedCode
    class LEDGenericMaskPresence1BitMap(LEDGenericMask1BitMap):
        """
        Define ``LEDGenericMaskPresence1BitMap`` information
        """
    # end class LEDGenericMaskPresence1BitMap

    # noinspection DuplicatedCode
    class LEDGenericMaskPresence2BitMap(LEDGenericMask2BitMap):
        """
        Define ``LEDGenericMaskPresence2BitMap`` information
        """
    # end class LEDGenericMaskPresence2BitMap

    # noinspection DuplicatedCode
    class LEDGenericMaskPresence3BitMap(LEDGenericMask3BitMap):
        """
        Define ``LEDGenericMaskPresence3BitMap`` information
        """
    # end class LEDGenericMaskPresence3BitMap

    # noinspection DuplicatedCode
    class LEDMaskState1BitMap(LEDMask1BitMap):
        """
        Define ``LEDMaskState1BitMap`` information
        """
    # end class LEDMaskState1BitMap

    # noinspection DuplicatedCode
    class LEDGenericMaskState1BitMap(LEDGenericMask1BitMap):
        """
        Define ``LEDGenericMaskState1BitMap`` information
        """
    # end class LEDGenericMaskState1BitMap

    # noinspection DuplicatedCode
    class LEDGenericMaskState2BitMap(LEDGenericMask2BitMap):
        """
        Define ``LEDGenericMaskState2BitMap`` information
        """
    # end class LEDGenericMaskState2BitMap

    # noinspection DuplicatedCode
    class LEDGenericMaskState3BitMap(LEDGenericMask3BitMap):
        """
        Define ``LEDGenericMaskState3BitMap`` information
        """
    # end class LEDGenericMaskState3BitMap
# end class LEDTest


# noinspection DuplicatedCode
class LEDTestModel(FeatureModel):
    """
    Define ``LEDTest`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_LED_LIST = 0
        GET_LED_TEST_MODE = 1
        SET_LED_TEST_MODE = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``LEDTest`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_LED_LIST: {
                    "request": GetLEDList,
                    "response": GetLEDListResponse
                },
                cls.INDEX.GET_LED_TEST_MODE: {
                    "request": GetLEDTestMode,
                    "response": GetLEDTestModeResponse
                },
                cls.INDEX.SET_LED_TEST_MODE: {
                    "request": SetLEDTestMode,
                    "response": SetLEDTestModeResponse
                }
            }
        }

        return {
            "feature_base": LEDTest,
            "versions": {
                LEDTestV0.VERSION: {
                    "main_cls": LEDTestV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class LEDTestModel


class LEDTestFactory(FeatureFactory):
    """
    Get ``LEDTest`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``LEDTest`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``LEDTestInterface``
        """
        return LEDTestModel.get_main_cls(version)()
    # end def create
# end class LEDTestFactory


class LEDTestInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``LEDTest``
    """

    def __init__(self):
        # Requests
        self.get_led_list_cls = None
        self.get_led_test_mode_cls = None
        self.set_led_test_mode_cls = None

        # Responses
        self.get_led_list_response_cls = None
        self.get_led_test_mode_response_cls = None
        self.set_led_test_mode_response_cls = None
    # end def __init__
# end class LEDTestInterface


class LEDTestV0(LEDTestInterface):
    """
    Define ``LEDTestV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getLEDList() -> ledMaskPresence1, ledGenericMaskPresence1, ledGenericMaskPresence2, ledGenericMaskPresence3

    [1] getLEDTestMode() -> ledMaskState1, ledGenericMaskState1, ledGenericMaskState2, ledGenericMaskState3

    [2] setLEDTestMode(ledMaskState1, ledGenericMaskState1, ledGenericMaskState2,
    ledGenericMaskState3) -> ledMaskState1, ledGenericMaskState1, ledGenericMaskState2, ledGenericMaskState3
    """
    VERSION = 0

    def __init__(self):
        # See ``LEDTest.__init__``
        super().__init__()
        index = LEDTestModel.INDEX

        # Requests
        self.get_led_list_cls = LEDTestModel.get_request_cls(
            self.VERSION, index.GET_LED_LIST)
        self.get_led_test_mode_cls = LEDTestModel.get_request_cls(
            self.VERSION, index.GET_LED_TEST_MODE)
        self.set_led_test_mode_cls = LEDTestModel.get_request_cls(
            self.VERSION, index.SET_LED_TEST_MODE)

        # Responses
        self.get_led_list_response_cls = LEDTestModel.get_response_cls(
            self.VERSION, index.GET_LED_LIST)
        self.get_led_test_mode_response_cls = LEDTestModel.get_response_cls(
            self.VERSION, index.GET_LED_TEST_MODE)
        self.set_led_test_mode_response_cls = LEDTestModel.get_response_cls(
            self.VERSION, index.SET_LED_TEST_MODE)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``LEDTestInterface.get_max_function_index``
        return LEDTestModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class LEDTestV0


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(LEDTest):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetLEDList
        - GetLEDTestMode

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(LEDTest.FID):
        # See ``LEDTest.FID``
        PADDING = LEDTest.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(LEDTest.LEN):
        # See ``LEDTest.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = LEDTest.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LEDTest.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(LEDTest):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - SetLEDTestModeResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(LEDTest.FID):
        """
        Define field identifier(s)
        """
        PADDING = LEDTest.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(LEDTest.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = LEDTest.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LEDTest.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class LEDTestModeState(LEDTest):
    """
    Define ``LEDTestModeState`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    LED Mask State 1              8
    Reserved LED Mask State 2     8
    LED Generic Mask State 1      8
    LED Generic Mask  State  2    8
    LED Generic Mask State 3      8
    Padding                       88
    ============================  ==========
    """
    class FID(LEDTest.FID):
        # See ``LEDTest.FID``
        LED_MASK_STATE_1 = LEDTest.FID.SOFTWARE_ID - 1
        RESERVED_LED_MASK_STATE_2 = LED_MASK_STATE_1 - 1
        LED_GENERIC_MASK_STATE_1 = RESERVED_LED_MASK_STATE_2 - 1
        LED_GENERIC_MASK_STATE_2 = LED_GENERIC_MASK_STATE_1 - 1
        LED_GENERIC_MASK_STATE_3 = LED_GENERIC_MASK_STATE_2 - 1
        PADDING = LED_GENERIC_MASK_STATE_3 - 1
    # end class FID

    class LEN(LEDTest.LEN):
        # See ``LEDTest.LEN``
        LED_MASK_STATE_1 = 0x8
        RESERVED_LED_MASK_STATE_2 = 0x8
        LED_GENERIC_MASK_STATE_1 = 0x8
        LED_GENERIC_MASK_STATE_2 = 0x8
        LED_GENERIC_MASK_STATE_3 = 0x8
        PADDING = 0x58
    # end class LEN

    FIELDS = LEDTest.FIELDS + (
        BitField(fid=FID.LED_MASK_STATE_1, length=LEN.LED_MASK_STATE_1,
                 title="LedMaskState1", name="led_mask_state_1",
                 checks=(CheckHexList(LEN.LED_MASK_STATE_1 // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED_LED_MASK_STATE_2, length=LEN.RESERVED_LED_MASK_STATE_2,
                 title="ReservedLedMaskState2", name="reserved_led_mask_state_2",
                 checks=(CheckHexList(LEN.RESERVED_LED_MASK_STATE_2 // 8), CheckByte(),),
                 default_value=LEDTest.DEFAULT.PADDING),
        BitField(fid=FID.LED_GENERIC_MASK_STATE_1, length=LEN.LED_GENERIC_MASK_STATE_1,
                 title="LedGenericMaskState1", name="led_generic_mask_state_1",
                 checks=(CheckHexList(LEN.LED_GENERIC_MASK_STATE_1 // 8), CheckByte(),)),
        BitField(fid=FID.LED_GENERIC_MASK_STATE_2, length=LEN.LED_GENERIC_MASK_STATE_2,
                 title="LedGenericMaskState2", name="led_generic_mask_state_2",
                 checks=(CheckHexList(LEN.LED_GENERIC_MASK_STATE_2 // 8), CheckByte(),)),
        BitField(fid=FID.LED_GENERIC_MASK_STATE_3, length=LEN.LED_GENERIC_MASK_STATE_3,
                 title="LedGenericMaskState3", name="led_generic_mask_state_3",
                 checks=(CheckHexList(LEN.LED_GENERIC_MASK_STATE_3 // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LEDTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, battery_green_led=0, battery_red_led=0, roller_led=0,
                 caps_lock_led=0, backlight_led=0, rgb=0, product_specific_led_0=0, product_specific_led_1=0,
                 product_specific_led_2=0, product_specific_led_3=0, product_specific_led_4=0,
                 product_specific_led_5=0, product_specific_led_6=0, product_specific_led_7=0,
                 product_specific_led_8=0, product_specific_led_9=0, product_specific_led_10=0,
                 product_specific_led_11=0, product_specific_led_12=0, product_specific_led_13=0,
                 product_specific_led_14=0, product_specific_led_15=0, product_specific_led_16=0,
                 product_specific_led_17=0, product_specific_led_18=0, product_specific_led_19=0,
                 product_specific_led_20=0, product_specific_led_21=0, product_specific_led_22=0,
                 product_specific_led_23=0, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param battery_green_led: 0=> Battery Green LED is in OFF state. 1=> Battery Green LED is in ON state -
            OPTIONAL.
        :type battery_green_led: ``int``
        :param battery_red_led: 0=> Battery Red LED is in OFF state. 1=> Battery Red LED is in ON state - OPTIONAL.
        :type battery_red_led: ``int``
        :param roller_led: 0=> Roller LED is in OFF state. 1=> Roller LED is in ON state - OPTIONAL.
        :type roller_led: ``int``
        :param caps_lock_led: 0=> Caps Lock LED is in OFF state. 1=> Caps Lock LED is in ON state - OPTIONAL.
        :type caps_lock_led: ``int``
        :param backlight_led: 0=> Backlight LED is in OFF state. 1=> Backlight LED is in ON state - OPTIONAL.
        :type backlight_led: ``int``
        :param rgb: 0=> RGB LED is in ON state. 1=> RGB LED is present in the device - OPTIONAL.
        :type rgb: ``int``
        :param product_specific_led_0: 0=> Product Specific LED 0 is in OFF state.
                                       1=> Product Specific LED 0 is in ON state - OPTIONAL.
        :type product_specific_led_0: ``int``
        :param product_specific_led_1: 0=> Product Specific LED 1 is in OFF state.
                                       1=> Product Specific LED 1 is in ON state - OPTIONAL.
        :type product_specific_led_1: ``int``
        :param product_specific_led_2: 0=> Product Specific LED 2 is in ON state.
                                       1=> Product Specific LED 2 is in OFF state - OPTIONAL.
        :type product_specific_led_2: ``int``
        :param product_specific_led_3: 0=> Product Specific LED 3 is in OFF state.
                                       1=> Product Specific LED 3 is ON state - OPTIONAL.
        :type product_specific_led_3: ``int``
        :param product_specific_led_4: 0=> Product Specific LED 4 is in OFF state.
                                       1=> Product Specific LED 4 is in ON state - OPTIONAL.
        :type product_specific_led_4: ``int``
        :param product_specific_led_5: 0=> Product Specific LED 5 is in OFF state.
                                       1=> Product Specific LED 5 is in ON state - OPTIONAL.
        :type product_specific_led_5: ``int``
        :param product_specific_led_6: 0=> Product Specific LED 6 is in OFF state.
                                       1=> Product Specific LED 6 is in ON state - OPTIONAL.
        :type product_specific_led_6: ``int``
        :param product_specific_led_7: 0=> Product Specific LED 7 is in OFF state.
                                       1=> Product Specific LED 7 is in ON state - OPTIONAL.
        :type product_specific_led_7: ``int``
        :param product_specific_led_8: 0=> Product Specific LED 8 is in OFF state.
                                       1=> Product Specific LED 8 is in ON state - OPTIONAL.
        :type product_specific_led_8: ``int``
        :param product_specific_led_9: 0=> Product Specific LED 9 is in OFF state.
                                       1=> Product Specific LED 9 is in ON state - OPTIONAL.
        :type product_specific_led_9: ``int``
        :param product_specific_led_10: 0=> Product Specific LED 10 is in OFF state.
                                        1=> Product Specific LED 10 is in ON state - OPTIONAL.
        :type product_specific_led_10: ``int``
        :param product_specific_led_11: 0=> Product Specific LED 11 is in OFF state.
                                        1=> Product Specific LED 11 is in ON state - OPTIONAL.
        :type product_specific_led_11: ``int``
        :param product_specific_led_12: 0=> Product Specific LED 12 is in OFF state.
                                        1=> Product Specific LED 12 is in ON state - OPTIONAL.
        :type product_specific_led_12: ``int``
        :param product_specific_led_13: 0=> Product Specific LED 13 is in OFF state.
                                        1=> Product Specific LED 13 is in ON state - OPTIONAL.
        :type product_specific_led_13: ``int``
        :param product_specific_led_14: 0=> Product Specific LED 14 is in OFF state.
                                        1=> Product Specific LED 14 is in ON state - OPTIONAL.
        :type product_specific_led_14: ``int``
        :param product_specific_led_15: 0=> Product Specific LED 15 is in OFF state.
                                        1=> Product Specific LED 15 is in ON state - OPTIONAL.
        :type product_specific_led_15: ``int``
        :param product_specific_led_16: 0=> Product Specific LED 16 is in OFF state.
                                        1=> Product Specific LED 16 is in ON state - OPTIONAL.
        :type product_specific_led_16: ``int``
        :param product_specific_led_17: 0=> Product Specific LED 17 is in OFF state.
                                        1=> Product Specific LED 17 is in ON state - OPTIONAL.
        :type product_specific_led_17: ``int``
        :param product_specific_led_18: 0=> Product Specific LED 18 is in OFF state.
                                        1=> Product Specific LED 18 is in ON state - OPTIONAL.
        :type product_specific_led_18: ``int``
        :param product_specific_led_19: 0=> Product Specific LED 19 is in OFF state.
                                        1=> Product Specific LED 19 is in ON state - OPTIONAL.
        :type product_specific_led_19: ``int``
        :param product_specific_led_20: 0=> Product Specific LED 20 is in OFF state.
                                        1=> Product Specific LED 20 is in ON state - OPTIONAL.
        :type product_specific_led_20: ``int``
        :param product_specific_led_21: 0=> Product Specific LED 21 is in OFF state.
                                        1=> Product Specific LED 21 is in ON state - OPTIONAL.
        :type product_specific_led_21: ``int``
        :param product_specific_led_22: 0=> Product Specific LED 22 is in OFF state.
                                        1=> Product Specific LED 22 is in ON state - OPTIONAL.
        :type product_specific_led_22: ``int``
        :param product_specific_led_23: 0=> Product Specific LED 23 is in OFF state.
                                        1=> Product Specific LED 23 is in ON state - OPTIONAL.
        :type product_specific_led_23: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.led_mask_state_1 = self.LEDMaskState1BitMap(battery_green_led=battery_green_led,
                                                         battery_red_led=battery_red_led,
                                                         roller_led=roller_led,
                                                         caps_lock_led=caps_lock_led,
                                                         backlight_led=backlight_led,
                                                         rgb=rgb)

        self.led_generic_mask_state_1 = self.LEDGenericMaskState1BitMap(product_specific_led_0=product_specific_led_0,
                                                                        product_specific_led_1=product_specific_led_1,
                                                                        product_specific_led_2=product_specific_led_2,
                                                                        product_specific_led_3=product_specific_led_3,
                                                                        product_specific_led_4=product_specific_led_4,
                                                                        product_specific_led_5=product_specific_led_5,
                                                                        product_specific_led_6=product_specific_led_6,
                                                                        product_specific_led_7=product_specific_led_7)

        self.led_generic_mask_state_2 = self.LEDGenericMaskState2BitMap(product_specific_led_8=product_specific_led_8,
                                                                        product_specific_led_9=product_specific_led_9,
                                                                        product_specific_led_10=product_specific_led_10,
                                                                        product_specific_led_11=product_specific_led_11,
                                                                        product_specific_led_12=product_specific_led_12,
                                                                        product_specific_led_13=product_specific_led_13,
                                                                        product_specific_led_14=product_specific_led_14,
                                                                        product_specific_led_15=product_specific_led_15)

        self.led_generic_mask_state_3 = self.LEDGenericMaskState3BitMap(product_specific_led_16=product_specific_led_16,
                                                                        product_specific_led_17=product_specific_led_17,
                                                                        product_specific_led_18=product_specific_led_18,
                                                                        product_specific_led_19=product_specific_led_19,
                                                                        product_specific_led_20=product_specific_led_20,
                                                                        product_specific_led_21=product_specific_led_21,
                                                                        product_specific_led_22=product_specific_led_22,
                                                                        product_specific_led_23=product_specific_led_23)
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
        :rtype: ``SetLEDTestModeResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.led_mask_state_1 = cls.LEDMaskState1BitMap.fromHexList(
            inner_field_container_mixin.led_mask_state_1)
        inner_field_container_mixin.led_generic_mask_state_1 = cls.LEDGenericMaskState1BitMap.fromHexList(
            inner_field_container_mixin.led_generic_mask_state_1)
        inner_field_container_mixin.led_generic_mask_state_2 = cls.LEDGenericMaskState2BitMap.fromHexList(
            inner_field_container_mixin.led_generic_mask_state_2)
        inner_field_container_mixin.led_generic_mask_state_3 = cls.LEDGenericMaskState3BitMap.fromHexList(
            inner_field_container_mixin.led_generic_mask_state_3)
        return inner_field_container_mixin
    # end def fromHexList
# end class LEDTestModeState

class GetLEDList(ShortEmptyPacketDataFormat):
    """
    Define ``GetLEDList`` implementation class
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
                         function_index=GetLEDListResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetLEDList

class GetLEDTestMode(ShortEmptyPacketDataFormat):
    """
    Define ``GetLEDTestMode`` implementation class
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
                         function_index=GetLEDTestModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetLEDTestMode


class SetLEDTestMode(LEDTestModeState):
    """
    Define ``SetLEDTestMode`` implementation class
    """

    def __init__(self, device_index, feature_index, battery_green_led=0, battery_red_led=0, roller_led=0,
                 caps_lock_led=0, backlight_led=0, rgb=0, product_specific_led_0=0, product_specific_led_1=0,
                 product_specific_led_2=0, product_specific_led_3=0, product_specific_led_4=0,
                 product_specific_led_5=0, product_specific_led_6=0, product_specific_led_7=0,
                 product_specific_led_8=0, product_specific_led_9=0, product_specific_led_10=0,
                 product_specific_led_11=0, product_specific_led_12=0, product_specific_led_13=0,
                 product_specific_led_14=0, product_specific_led_15=0, product_specific_led_16=0,
                 product_specific_led_17=0, product_specific_led_18=0, product_specific_led_19=0,
                 product_specific_led_20=0, product_specific_led_21=0, product_specific_led_22=0,
                 product_specific_led_23=0, **kwargs):
        # See ``LEDTestModeState

        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetLEDTestModeResponse.FUNCTION_INDEX,
                         battery_green_led=battery_green_led, battery_red_led=battery_red_led, roller_led=roller_led,
                         caps_lock_led=caps_lock_led, backlight_led=backlight_led, rgb=rgb,
                         product_specific_led_0=product_specific_led_0, product_specific_led_1=product_specific_led_1,
                         product_specific_led_2=product_specific_led_2, product_specific_led_3=product_specific_led_3,
                         product_specific_led_4=product_specific_led_4, product_specific_led_5=product_specific_led_5,
                         product_specific_led_6=product_specific_led_6, product_specific_led_7=product_specific_led_7,
                         product_specific_led_8=product_specific_led_8, product_specific_led_9=product_specific_led_9,
                         product_specific_led_10=product_specific_led_10,
                         product_specific_led_11=product_specific_led_11,
                         product_specific_led_12=product_specific_led_12,
                         product_specific_led_13=product_specific_led_13,
                         product_specific_led_14=product_specific_led_14,
                         product_specific_led_15=product_specific_led_15,
                         product_specific_led_16=product_specific_led_16,
                         product_specific_led_17=product_specific_led_17,
                         product_specific_led_18=product_specific_led_18,
                         product_specific_led_19=product_specific_led_19,
                         product_specific_led_20=product_specific_led_20,
                         product_specific_led_21=product_specific_led_21,
                         product_specific_led_22=product_specific_led_22,
                         product_specific_led_23=product_specific_led_23, **kwargs)
    # end def __init__
# end class SetLEDTestMode

class GetLEDListResponse(LEDTest):
    """
    Define ``GetLEDListResponse`` implementation class

    Format:
    =============================  ==========
    Name                           Bit count
    =============================  ==========
    LED Mask Presence 1            8
    Reserved LED Mask Presence 2   8
    LED Generic Mask Presence 1    8
    LED Generic Mask  Presence 2   8
    LED Generic Mask Presence 3    8
    Padding                        88
    =============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetLEDList,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(LEDTest.FID):
        # See ``LEDTest.FID``
        LED_MASK_PRESENCE_1 = LEDTest.FID.SOFTWARE_ID - 1
        RESERVED_LED_MASK_PRESENCE_2 = LED_MASK_PRESENCE_1 - 1
        LED_GENERIC_MASK_PRESENCE_1 = RESERVED_LED_MASK_PRESENCE_2 - 1
        LED_GENERIC_MASK_PRESENCE_2 = LED_GENERIC_MASK_PRESENCE_1 - 1
        LED_GENERIC_MASK_PRESENCE_3 = LED_GENERIC_MASK_PRESENCE_2 - 1
        PADDING = LED_GENERIC_MASK_PRESENCE_3 - 1
    # end class FID

    class LEN(LEDTest.LEN):
        # See ``LEDTest.LEN``
        LED_MASK_PRESENCE_1 = 0x8
        RESERVED_LED_MASK_PRESENCE_2 = 0x8
        LED_GENERIC_MASK_PRESENCE_1 = 0x8
        LED_GENERIC_MASK_PRESENCE_2 = 0x8
        LED_GENERIC_MASK_PRESENCE_3 = 0x8
        PADDING = 0x58
    # end class LEN

    FIELDS = LEDTest.FIELDS + (
        BitField(fid=FID.LED_MASK_PRESENCE_1, length=LEN.LED_MASK_PRESENCE_1,
                 title="LedMaskPresence1", name="led_mask_presence_1",
                 checks=(CheckHexList(LEN.LED_MASK_PRESENCE_1 // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED_LED_MASK_PRESENCE_2, length=LEN.RESERVED_LED_MASK_PRESENCE_2,
                 title="ReservedLedMaskPresence2", name="reserved_led_mask_presence_2",
                 checks=(CheckHexList(LEN.RESERVED_LED_MASK_PRESENCE_2 // 8), CheckByte(),),
                 default_value=LEDTest.DEFAULT.PADDING),
        BitField(fid=FID.LED_GENERIC_MASK_PRESENCE_1, length=LEN.LED_GENERIC_MASK_PRESENCE_1,
                 title="LedGenericMaskPresence1", name="led_generic_mask_presence_1",
                 checks=(CheckHexList(LEN.LED_GENERIC_MASK_PRESENCE_1 // 8), CheckByte(),)),
        BitField(fid=FID.LED_GENERIC_MASK_PRESENCE_2, length=LEN.LED_GENERIC_MASK_PRESENCE_2,
                 title="LedGenericMaskPresence2", name="led_generic_mask_presence_2",
                 checks=(CheckHexList(LEN.LED_GENERIC_MASK_PRESENCE_2 // 8), CheckByte(),)),
        BitField(fid=FID.LED_GENERIC_MASK_PRESENCE_3, length=LEN.LED_GENERIC_MASK_PRESENCE_3,
                 title="LedGenericMaskPresence3", name="led_generic_mask_presence_3",
                 checks=(CheckHexList(LEN.LED_GENERIC_MASK_PRESENCE_3 // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LEDTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, battery_green_led=0, battery_red_led=0, roller_led=0,
                 caps_lock_led=0, backlight_led=0, rgb=0, product_specific_led_0=0, product_specific_led_1=0,
                 product_specific_led_2=0, product_specific_led_3=0, product_specific_led_4=0,
                 product_specific_led_5=0, product_specific_led_6=0, product_specific_led_7=0,
                 product_specific_led_8=0, product_specific_led_9=0, product_specific_led_10=0,
                 product_specific_led_11=0, product_specific_led_12=0, product_specific_led_13=0,
                 product_specific_led_14=0, product_specific_led_15=0, product_specific_led_16=0,
                 product_specific_led_17=0, product_specific_led_18=0, product_specific_led_19=0,
                 product_specific_led_20=0, product_specific_led_21=0, product_specific_led_22=0,
                 product_specific_led_23=0, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param battery_green_led: 0=> Battery Green LED is not present in the device.
                                  1=> Battery Green LED is present in the device - OPTIONAL.
        :type battery_green_led: ``int``
        :param battery_red_led: 0=> Battery Red LED is not present in the device.
                                1=> Battery Red LED is present in the device - OPTIONAL.
        :type battery_red_led: ``int``
        :param roller_led: 0=> Roller LED is not present in the device.
                            1=> Roller LED is present in the device - OPTIONAL.
        :type roller_led: ``int``
        :param caps_lock_led: 0=> Caps Lock LED is not present in the device.
                               1=> Caps Lock LED is present in the device - OPTIONAL.
        :type caps_lock_led: ``int``
        :param backlight_led: 0=> Backlight LED is not present in the device.
                               1=> Backlight LED is present in the device - OPTIONAL.
        :type backlight_led: ``int``
        :param rgb: 0=> RGB LED is not present in the device. 1=> RGB LED is present in the device - OPTIONAL.
        :type rgb: ``int``
        :param product_specific_led_0: 0=> Product Specific LED 0 is not present in the device.
                                       1=> Product Specific LED 0 is present in the device - OPTIONAL.
        :type product_specific_led_0: ``int``
        :param product_specific_led_1: 0=> Product Specific LED 1 is not present in the device.
                                       1=> Product Specific LED 1 is present in the device - OPTIONAL.
        :type product_specific_led_1: ``int``
        :param product_specific_led_2: 0=> Product Specific LED 2 is not present in the device.
                                       1=> Product Specific LED 2 is present in the device - OPTIONAL.
        :type product_specific_led_2: ``int``
        :param product_specific_led_3: 0=> Product Specific LED 3 is not present in the device.
                                       1=> Product Specific LED 3 is present in the device - OPTIONAL.
        :type product_specific_led_3: ``int``
        :param product_specific_led_4: 0=> Product Specific LED 4 is not present in the device.
                                       1=> Product Specific LED 4 is present in the device - OPTIONAL.
        :type product_specific_led_4: ``int``
        :param product_specific_led_5: 0=> Product Specific LED 5 is not present in the device.
                                       1=> Product Specific LED 5 is present in the device - OPTIONAL.
        :type product_specific_led_5: ``int``
        :param product_specific_led_6: 0=> Product Specific LED 6 is not present in the device.
                                       1=> Product Specific LED 6 is present in the device - OPTIONAL.
        :type product_specific_led_6: ``int``
        :param product_specific_led_7: 0=> Product Specific LED 7 is not present in the device.
                                       1=> Product Specific LED 7 is present in the device - OPTIONAL.
        :type product_specific_led_7: ``int``
        :param product_specific_led_8: 0=> Product Specific LED 8 is not present in the device.
                                       1=> Product Specific LED 8 is present in the device - OPTIONAL.
        :type product_specific_led_8: ``int``
        :param product_specific_led_9: 0=> Product Specific LED 9 is not present in the device.
                                       1=> Product Specific LED 9 is present in the device - OPTIONAL.
        :type product_specific_led_9: ``int``
        :param product_specific_led_10: 0=> Product Specific LED 10 is not present in the device.
                                        1=> Product Specific LED 10 is present in the device - OPTIONAL.
        :type product_specific_led_10: ``int``
        :param product_specific_led_11: 0=> Product Specific LED 11 is not present in the device.
                                        1=> Product Specific LED 11 is present in the device - OPTIONAL.
        :type product_specific_led_11: ``int``
        :param product_specific_led_12: 0=> Product Specific LED 12 is not present in the device.
                                        1=> Product Specific LED 12 is present in the device - OPTIONAL.
        :type product_specific_led_12: ``int``
        :param product_specific_led_13: 0=> Product Specific LED 13 is not present in the device.
                                        1=> Product Specific LED 13 is present in the device - OPTIONAL.
        :type product_specific_led_13: ``int``
        :param product_specific_led_14: 0=> Product Specific LED 14 is not present in the device.
                                        1=> Product Specific LED 14 is present in the device - OPTIONAL.
        :type product_specific_led_14: ``int``
        :param product_specific_led_15: 0=> Product Specific LED 15 is not present in the device.
                                        1=> Product Specific LED 15 is present in the device - OPTIONAL.
        :type product_specific_led_15: ``int``
        :param product_specific_led_16: 0=> Product Specific LED 16 is not present in the device.
                                        1=> Product Specific LED 16 is present in the device - OPTIONAL.
        :type product_specific_led_16: ``int``
        :param product_specific_led_17: 0=> Product Specific LED 17 is not present in the device.
                                        1=> Product Specific LED 17 is present in the device - OPTIONAL.
        :type product_specific_led_17: ``int``
        :param product_specific_led_18: 0=> Product Specific LED 18 is not present in the device.
                                        1=> Product Specific LED 18 is present in the device - OPTIONAL.
        :type product_specific_led_18: ``int``
        :param product_specific_led_19: 0=> Product Specific LED 19 is not present in the device.
                                        1=> Product Specific LED 19 is present in the device - OPTIONAL.
        :type product_specific_led_19: ``int``
        :param product_specific_led_20: 0=> Product Specific LED 20 is not present in the device.
                                        1=> Product Specific LED 20 is present in the device - OPTIONAL.
        :type product_specific_led_20: ``int``
        :param product_specific_led_21: 0=> Product Specific LED 21 is not present in the device.
                                        1=> Product Specific LED 21 is present in the device - OPTIONAL.
        :type product_specific_led_21: ``int``
        :param product_specific_led_22: 0=> Product Specific LED 22 is not present in the device.
                                        1=> Product Specific LED 22 is present in the device - OPTIONAL.
        :type product_specific_led_22: ``int``
        :param product_specific_led_23: 0=> Product Specific LED 23 is not present in the device.
                                        1=> Product Specific LED 23 is present in the device - OPTIONAL.
        :type product_specific_led_23: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.led_mask_presence_1 = self.LEDMaskPresence1BitMap(battery_green_led=battery_green_led,
                                                               battery_red_led=battery_red_led,
                                                               roller_led=roller_led,
                                                               caps_lock_led=caps_lock_led,
                                                               backlight_led=backlight_led,
                                                               rgb=rgb)

        self.led_generic_mask_presence_1 = self.LEDGenericMaskPresence1BitMap(
            product_specific_led_0=product_specific_led_0,
            product_specific_led_1=product_specific_led_1,
            product_specific_led_2=product_specific_led_2,
            product_specific_led_3=product_specific_led_3,
            product_specific_led_4=product_specific_led_4,
            product_specific_led_5=product_specific_led_5,
            product_specific_led_6=product_specific_led_6,
            product_specific_led_7=product_specific_led_7)

        self.led_generic_mask_presence_2 = self.LEDGenericMaskPresence2BitMap(
            product_specific_led_8=product_specific_led_8,
            product_specific_led_9=product_specific_led_9,
            product_specific_led_10=product_specific_led_10,
            product_specific_led_11=product_specific_led_11,
            product_specific_led_12=product_specific_led_12,
            product_specific_led_13=product_specific_led_13,
            product_specific_led_14=product_specific_led_14,
            product_specific_led_15=product_specific_led_15)

        self.led_generic_mask_presence_3 = self.LEDGenericMaskPresence3BitMap(
            product_specific_led_16=product_specific_led_16,
            product_specific_led_17=product_specific_led_17,
            product_specific_led_18=product_specific_led_18,
            product_specific_led_19=product_specific_led_19,
            product_specific_led_20=product_specific_led_20,
            product_specific_led_21=product_specific_led_21,
            product_specific_led_22=product_specific_led_22,
            product_specific_led_23=product_specific_led_23)
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
        :rtype: ``GetLEDListResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.led_mask_presence_1 = cls.LEDMaskPresence1BitMap.fromHexList(
            inner_field_container_mixin.led_mask_presence_1)
        inner_field_container_mixin.led_generic_mask_presence_1 = cls.LEDGenericMaskPresence1BitMap.fromHexList(
            inner_field_container_mixin.led_generic_mask_presence_1)
        inner_field_container_mixin.led_generic_mask_presence_2 = cls.LEDGenericMaskPresence2BitMap.fromHexList(
            inner_field_container_mixin.led_generic_mask_presence_2)
        inner_field_container_mixin.led_generic_mask_presence_3 = cls.LEDGenericMaskPresence3BitMap.fromHexList(
            inner_field_container_mixin.led_generic_mask_presence_3)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetLEDListResponse


class GetLEDTestModeResponse(LEDTestModeState):
    """
    Define ``GetLEDTestModeResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetLEDTestMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, battery_green_led=0, battery_red_led=0, roller_led=0,
                 caps_lock_led=0, backlight_led=0, rgb=0, product_specific_led_0=0, product_specific_led_1=0,
                 product_specific_led_2=0, product_specific_led_3=0, product_specific_led_4=0,
                 product_specific_led_5=0, product_specific_led_6=0, product_specific_led_7=0,
                 product_specific_led_8=0, product_specific_led_9=0, product_specific_led_10=0,
                 product_specific_led_11=0, product_specific_led_12=0, product_specific_led_13=0,
                 product_specific_led_14=0, product_specific_led_15=0, product_specific_led_16=0,
                 product_specific_led_17=0, product_specific_led_18=0, product_specific_led_19=0,
                 product_specific_led_20=0, product_specific_led_21=0, product_specific_led_22=0,
                 product_specific_led_23=0, **kwargs):
        # See ``LEDTestModeState``

        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         battery_green_led=battery_green_led, battery_red_led=battery_red_led, roller_led=roller_led,
                         caps_lock_led=caps_lock_led, backlight_led=backlight_led, rgb=rgb,
                         product_specific_led_0=product_specific_led_0, product_specific_led_1=product_specific_led_1,
                         product_specific_led_2=product_specific_led_2, product_specific_led_3=product_specific_led_3,
                         product_specific_led_4=product_specific_led_4, product_specific_led_5=product_specific_led_5,
                         product_specific_led_6=product_specific_led_6, product_specific_led_7=product_specific_led_7,
                         product_specific_led_8=product_specific_led_8, product_specific_led_9=product_specific_led_9,
                         product_specific_led_10=product_specific_led_10,
                         product_specific_led_11=product_specific_led_11,
                         product_specific_led_12=product_specific_led_12,
                         product_specific_led_13=product_specific_led_13,
                         product_specific_led_14=product_specific_led_14,
                         product_specific_led_15=product_specific_led_15,
                         product_specific_led_16=product_specific_led_16,
                         product_specific_led_17=product_specific_led_17,
                         product_specific_led_18=product_specific_led_18,
                         product_specific_led_19=product_specific_led_19,
                         product_specific_led_20=product_specific_led_20,
                         product_specific_led_21=product_specific_led_21,
                         product_specific_led_22=product_specific_led_22,
                         product_specific_led_23=product_specific_led_23, **kwargs)

    # end def __init__
# end class GetLEDTestModeResponse


class SetLEDTestModeResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetLEDTestModeResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetLEDTestMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

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
                         function_index=SetLEDTestModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetLEDTestModeResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
