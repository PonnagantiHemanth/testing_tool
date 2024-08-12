#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.blereportmap
:brief: BLE report descriptor definition
        See https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit?usp=sharing
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/26
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.field import CheckHexList
from pyhid.hid.descriptor import ReportDescriptor
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class HidReportKeyboardLedTopRowDescriptor(ReportDescriptor):
    """
    Define the BLE Keyboard descriptor including the LED and the Top Row logical collection.

    cf HID_REPORT_DESCRIPTOR_KEYBOARD in lble_svc_hid_descriptor.h
    Case with HID_REPORT_KEYBOARD_LED_ENABLED & HID_REPORT_TOP_ROW_ENABLED enabled
    """
    BITFIELD_LENGTH = 92  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        KEYBOARD_REPORT_ID = ReportDescriptor.FID.APP_COLLECTION - 1
        MODIFIER_REPORT_COUNT = KEYBOARD_REPORT_ID - 1
        MODIFIER_REPORT_SIZE = MODIFIER_REPORT_COUNT - 1
        MODIFIER_LOGICAL_MINIMUM = MODIFIER_REPORT_SIZE - 1
        MODIFIER_LOGICAL_MAXIMUM = MODIFIER_LOGICAL_MINIMUM - 1
        MODIFIER_USAGE_PAGE = MODIFIER_LOGICAL_MAXIMUM - 1
        MODIFIER_USAGE_MINIMUM = MODIFIER_USAGE_PAGE - 1
        MODIFIER_USAGE_MAXIMUM = MODIFIER_USAGE_MINIMUM - 1
        MODIFIER_INPUT_DATA = MODIFIER_USAGE_MAXIMUM - 1
        LED_REPORT_COUNT = MODIFIER_INPUT_DATA - 1
        LED_REPORT_SIZE = LED_REPORT_COUNT - 1
        LED_LOGICAL_MINIMUM = LED_REPORT_SIZE - 1
        LED_LOGICAL_MAXIMUM = LED_LOGICAL_MINIMUM - 1
        LED_USAGE_PAGE = LED_LOGICAL_MAXIMUM - 1
        LED_USAGE_MINIMUM = LED_USAGE_PAGE - 1
        LED_USAGE_MAXIMUM = LED_USAGE_MINIMUM - 1
        LED_OUTPUT = LED_USAGE_MAXIMUM - 1
        RSV_REPORT_COUNT = LED_OUTPUT - 1
        RSV_OUTPUT = RSV_REPORT_COUNT - 1
        KEY_REPORT_COUNT = RSV_OUTPUT - 1
        KEY_REPORT_SIZE = KEY_REPORT_COUNT - 1
        KEY_LOGICAL_MAXIMUM = KEY_REPORT_SIZE - 1
        KEY_USAGE_PAGE = KEY_LOGICAL_MAXIMUM - 1
        KEY_USAGE_MINIMUM = KEY_USAGE_PAGE - 1
        KEY_USAGE_MAXIMUM = KEY_USAGE_MINIMUM - 1
        KEY_INPUT = KEY_USAGE_MAXIMUM - 1
        TOP_RAW_GOOGLE_USAGE_PAGE = KEY_INPUT - 1
        TOP_RAW_LIST_USAGE = TOP_RAW_GOOGLE_USAGE_PAGE - 1
        TOP_RAW_COLLECTION = TOP_RAW_LIST_USAGE - 1
        TOP_RAW_REPORT_ID = TOP_RAW_COLLECTION - 1
        TOP_RAW_REPORT_COUNT = TOP_RAW_REPORT_ID - 1
        TOP_RAW_REPORT_SIZE = TOP_RAW_REPORT_COUNT - 1
        TOP_RAW_LOGICAL_MINIMUM = TOP_RAW_REPORT_SIZE - 1
        TOP_RAW_LOGICAL_MAXIMUM = TOP_RAW_LOGICAL_MINIMUM - 1
        TOP_RAW_USAGE_PAGE = TOP_RAW_LOGICAL_MAXIMUM - 1
        TOP_RAW_USAGE_MINIMUM = TOP_RAW_USAGE_PAGE - 1
        TOP_RAW_USAGE_MAXIMUM = TOP_RAW_USAGE_MINIMUM - 1
        TOP_RAW_FEATURE = TOP_RAW_USAGE_MAXIMUM - 1
        TOP_RAW_END_COLLECTION = TOP_RAW_FEATURE - 1
        END_COLLECTION = TOP_RAW_END_COLLECTION - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        KEY_LOGICAL_MAXIMUM = 0x18
        KEY_USAGE_MAXIMUM = 0x10
        TOP_RAW_GOOGLE_USAGE_PAGE = 0x18
        TOP_RAW_LOGICAL_MINIMUM = 0x28
        TOP_RAW_LOGICAL_MAXIMUM = 0x28
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        MODIFIER_REPORT_COUNT = HexList("9508")
        MODIFIER_REPORT_SIZE = HexList("7501")
        MODIFIER_LOGICAL_MINIMUM = HexList("1500")
        MODIFIER_LOGICAL_MAXIMUM = HexList("2501")
        MODIFIER_USAGE_MINIMUM = HexList("19E0")
        MODIFIER_USAGE_MAXIMUM = HexList("29E7")
        LED_REPORT_COUNT = HexList("9505")
        LED_USAGE_MINIMUM = HexList("1901")
        LED_USAGE_MAXIMUM = HexList("2905")
        RSV_REPORT_COUNT = HexList("9503")
        KEY_REPORT_COUNT = HexList("9506")
        KEY_REPORT_SIZE = HexList("7508")
        KEY_LOGICAL_MAXIMUM = HexList("26FF00")
        KEY_USAGE_MINIMUM = HexList("1900")
        KEY_USAGE_MAXIMUM = HexList("29FF")
        TOP_RAW_GOOGLE_USAGE_PAGE = HexList("06D1FF")
        TOP_RAW_REPORT_COUNT = HexList("9500")
        TOP_RAW_REPORT_SIZE = HexList("7520")
        TOP_RAW_LOGICAL_MINIMUM = HexList("1700000080")
        TOP_RAW_LOGICAL_MAXIMUM = HexList("27FFFFFF7F")
        TOP_RAW_USAGE_PAGE = HexList("050A")
        TOP_RAW_USAGE_MINIMUM = HexList("1901")
        TOP_RAW_USAGE_MAXIMUM = HexList("2900")
        TOP_RAW_FEATURE = HexList("B103")
    # end class DEFAULT

    FIELDS = ReportDescriptor.FIELDS + (
        BitField(fid=FID.KEYBOARD_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Keyboard Report Id',
                 name='keyboard_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.KEYBOARD_REPORT_ID),
        BitField(fid=FID.MODIFIER_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Modifier Report Count',
                 name='modifier_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.MODIFIER_REPORT_COUNT),
        BitField(fid=FID.MODIFIER_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Modifier Report Size',
                 name='modifier_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.MODIFIER_REPORT_SIZE),
        BitField(fid=FID.MODIFIER_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Modifier Logical Minimum',
                 name='modifier_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.MODIFIER_LOGICAL_MINIMUM),
        BitField(fid=FID.MODIFIER_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Modifier Logical Maximum',
                 name='modifier_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.MODIFIER_LOGICAL_MAXIMUM),
        BitField(fid=FID.MODIFIER_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Keyboard Usage Page',
                 name='keyboard_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.KEYBOARD_USAGE_PAGE),
        BitField(fid=FID.MODIFIER_USAGE_MINIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='Modifier Usage Minimum',
                 name='modifier_usage_minimum',
                 checks=(CheckHexList(LEN.USAGE_MINIMUM // 8),),
                 default_value=DEFAULT.MODIFIER_USAGE_MINIMUM),
        BitField(fid=FID.MODIFIER_USAGE_MAXIMUM,
                 length=LEN.USAGE_MAXIMUM,
                 title='Modifier Usage Maximum',
                 name='modifier_usage_maximum',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.MODIFIER_USAGE_MAXIMUM),
        BitField(fid=FID.MODIFIER_INPUT_DATA,
                 length=LEN.INPUT_DATA,
                 title='Modifier Input Data',
                 name='modifier_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.LED_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='LED Report Count',
                 name='led_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.LED_REPORT_COUNT),
        BitField(fid=FID.LED_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='LED Report Size',
                 name='led_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.MODIFIER_REPORT_SIZE),
        BitField(fid=FID.LED_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='LED Logical Minimum',
                 name='led_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.MODIFIER_LOGICAL_MINIMUM),
        BitField(fid=FID.LED_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='LED Report Size',
                 name='led_report_size',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.MODIFIER_LOGICAL_MAXIMUM),
        BitField(fid=FID.LED_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='LED Usage Page',
                 name='led_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.LED_USAGE_PAGE),
        BitField(fid=FID.LED_USAGE_MINIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='LED Usage Minimum',
                 name='led_usage_minimum',
                 checks=(CheckHexList(LEN.USAGE_MINIMUM // 8),),
                 default_value=DEFAULT.LED_USAGE_MINIMUM),
        BitField(fid=FID.LED_USAGE_MAXIMUM,
                 length=LEN.USAGE_MAXIMUM,
                 title='LED Usage Maximum',
                 name='led_usage_maximum',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.LED_USAGE_MAXIMUM),
        BitField(fid=FID.LED_OUTPUT,
                 length=LEN.OUTPUT_DATA,
                 title='LED Output',
                 name='led_output',
                 checks=(CheckHexList(LEN.OUTPUT_DATA // 8),),
                 default_value=DEFAULT.OUTPUT_DATA),
        BitField(fid=FID.RSV_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Reserved Report Count',
                 name='rsv_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.RSV_REPORT_COUNT),
        BitField(fid=FID.RSV_OUTPUT,
                 length=LEN.OUTPUT_CST,
                 title='Reserved Output',
                 name='rsv_output',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.OUTPUT_CST),
        BitField(fid=FID.KEY_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Key Report Count',
                 name='key_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.KEY_REPORT_COUNT),
        BitField(fid=FID.KEY_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Key Report Size',
                 name='key_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.KEY_REPORT_SIZE),
        BitField(fid=FID.KEY_LOGICAL_MAXIMUM,
                 length=LEN.KEY_LOGICAL_MAXIMUM,
                 title='Key LOGICAL Maximum',
                 name='key_logical_maximum',
                 checks=(CheckHexList(LEN.KEY_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.KEY_LOGICAL_MAXIMUM),
        BitField(fid=FID.KEY_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Key Usage Page',
                 name='key_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.KEYBOARD_USAGE_PAGE),
        BitField(fid=FID.KEY_USAGE_MINIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='Key Usage Minimum',
                 name='key_usage_minimum',
                 checks=(CheckHexList(LEN.USAGE_MINIMUM // 8),),
                 default_value=DEFAULT.KEY_USAGE_MINIMUM),
        BitField(fid=FID.KEY_USAGE_MAXIMUM,
                 length=LEN.KEY_USAGE_MAXIMUM,
                 title='Key Usage Maximum',
                 name='key_usage_maximum',
                 checks=(CheckHexList(LEN.KEY_USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.KEY_USAGE_MAXIMUM),
        BitField(fid=FID.KEY_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Key Input',
                 name='key_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.TOP_RAW_GOOGLE_USAGE_PAGE,
                 length=LEN.TOP_RAW_GOOGLE_USAGE_PAGE,
                 title='Top Raw Google Usage Page',
                 name='top_raw_google_usage_page',
                 checks=(CheckHexList(LEN.TOP_RAW_GOOGLE_USAGE_PAGE // 8),),
                 default_value=DEFAULT.TOP_RAW_GOOGLE_USAGE_PAGE),
        BitField(fid=FID.TOP_RAW_LIST_USAGE,
                 length=LEN.USAGE,
                 title='Top Raw List Usage',
                 name='top_raw_list_usage',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.TOP_RAW_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Top Raw Collection',
                 name='top_raw_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.LOGICAL_COLLECTION),
        BitField(fid=FID.TOP_RAW_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Top Raw Report Id',
                 name='top_raw_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.TOP_RAW_REPORT_ID),
        BitField(fid=FID.TOP_RAW_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Top Raw Report Count',
                 name='top_raw_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.TOP_RAW_REPORT_COUNT),
        BitField(fid=FID.TOP_RAW_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Top Raw Report Size',
                 name='top_raw_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.TOP_RAW_REPORT_SIZE),
        BitField(fid=FID.TOP_RAW_LOGICAL_MINIMUM,
                 length=LEN.TOP_RAW_LOGICAL_MINIMUM,
                 title='Top Raw Logical Minimum',
                 name='top_raw_logical_minimum',
                 checks=(CheckHexList(LEN.TOP_RAW_LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.TOP_RAW_LOGICAL_MINIMUM),
        BitField(fid=FID.TOP_RAW_LOGICAL_MAXIMUM,
                 length=LEN.TOP_RAW_LOGICAL_MAXIMUM,
                 title='Top Raw Logical Maximum',
                 name='top_raw_logical_maximum',
                 checks=(CheckHexList(LEN.TOP_RAW_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.TOP_RAW_LOGICAL_MAXIMUM),
        BitField(fid=FID.TOP_RAW_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Top Raw Usage Page',
                 name='top_raw_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.TOP_RAW_USAGE_PAGE),
        BitField(fid=FID.TOP_RAW_USAGE_MINIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='Top Raw Usage Minimum',
                 name='top_raw_usage_minimum',
                 checks=(CheckHexList(LEN.USAGE_MINIMUM // 8),),
                 default_value=DEFAULT.TOP_RAW_USAGE_MINIMUM),
        BitField(fid=FID.TOP_RAW_USAGE_MAXIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='Top Raw Usage Maximum',
                 name='top_raw_usage_maximum',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.TOP_RAW_USAGE_MAXIMUM),
        BitField(fid=FID.TOP_RAW_FEATURE,
                 length=LEN.FEATURE,
                 title='Top Raw Feature',
                 name='top_raw_feature',
                 checks=(CheckHexList(LEN.FEATURE // 8),),
                 default_value=DEFAULT.TOP_RAW_FEATURE),
        BitField(fid=FID.TOP_RAW_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Top Raw Collection',
                 name='top_raw_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
        BitField(fid=FID.END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='End Collection',
                 name='end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class HidReportKeyboardLedTopRowDescriptor


class HidReportKeyboardLedDescriptor(HidReportKeyboardLedTopRowDescriptor):
    """
    Define the BLE Keyboard descriptor including the LED but without the Top Raw logical collection.

    cf HID_REPORT_DESCRIPTOR_KEYBOARD in lble_svc_hid_descriptor.h
    Case with HID_REPORT_KEYBOARD_LED_ENABLED enabled but HID_REPORT_TOP_ROW_ENABLED disabled.
    """
    BITFIELD_LENGTH = 60  # Bytes

    FIELDS = \
        HidReportKeyboardLedTopRowDescriptor.FIELDS[:(
                HidReportKeyboardLedTopRowDescriptor.FID.USAGE_PAGE -
                HidReportKeyboardLedTopRowDescriptor.FID.TOP_RAW_GOOGLE_USAGE_PAGE)] + \
        HidReportKeyboardLedTopRowDescriptor.FIELDS[(
                                                            HidReportKeyboardLedTopRowDescriptor.FID.USAGE_PAGE -
                                                            HidReportKeyboardLedTopRowDescriptor.FID.END_COLLECTION):]
# end class HidReportKeyboardLedDescriptor


class HidReportKeyboardDescriptor(HidReportKeyboardLedDescriptor):
    """
    Define the BLE Keyboard descriptor without the LED and without the Top Raw logical collection.

    cf HID_REPORT_DESCRIPTOR_KEYBOARD in lble_svc_hid_descriptor.h
    Case with HID_REPORT_KEYBOARD_LED_ENABLED disabled and HID_REPORT_TOP_ROW_ENABLED disabled.
    """
    BITFIELD_LENGTH = 40  # Bytes

    FIELDS = \
        HidReportKeyboardLedDescriptor.FIELDS[:(HidReportKeyboardLedDescriptor.FID.USAGE_PAGE -
                                                HidReportKeyboardLedDescriptor.FID.LED_REPORT_COUNT)] + \
        HidReportKeyboardLedDescriptor.FIELDS[(HidReportKeyboardLedDescriptor.FID.USAGE_PAGE -
                                               HidReportKeyboardLedDescriptor.FID.KEY_REPORT_COUNT):]
# end class HidReportKeyboardDescriptor


class HidReportMouse12Descriptor(ReportDescriptor):
    """
    Define the BLE HID report Mouse 12 bits descriptor.
    """
    BITFIELD_LENGTH = 69  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        MOUSE_USAGE_PAGE = HidReportKeyboardLedTopRowDescriptor.FID.END_COLLECTION - 1
        MOUSE_USAGE = MOUSE_USAGE_PAGE - 1
        MOUSE_APP_COLLECTION = MOUSE_USAGE - 1
        MOUSE_REPORT_ID = MOUSE_APP_COLLECTION - 1
        POINTER_USAGE = MOUSE_REPORT_ID - 1
        PHYSICAL_COLLECTION = POINTER_USAGE - 1
        BUTTON_REPORT_COUNT = PHYSICAL_COLLECTION - 1
        BUTTON_REPORT_SIZE = BUTTON_REPORT_COUNT - 1
        BUTTON_LOGICAL_MINIMUM = BUTTON_REPORT_SIZE - 1
        BUTTON_LOGICAL_MAXIMUM = BUTTON_LOGICAL_MINIMUM - 1
        BUTTON_USAGE_PAGE = BUTTON_LOGICAL_MAXIMUM - 1
        BUTTON_USAGE_MINIMUM = BUTTON_USAGE_PAGE - 1
        BUTTON_USAGE_MAXIMUM = BUTTON_USAGE_MINIMUM - 1
        BUTTON_INPUT_DATA = BUTTON_USAGE_MAXIMUM - 1
        AXIS_USAGE_PAGE = BUTTON_INPUT_DATA - 1
        AXIS_REPORT_PUSH = AXIS_USAGE_PAGE - 1
        AXIS_REPORT_COUNT = BUTTON_INPUT_DATA - 1
        AXIS_REPORT_SIZE = AXIS_REPORT_PUSH - 1
        AXIS_LOGICAL_MINIMUM = AXIS_REPORT_SIZE - 1
        AXIS_LOGICAL_MAXIMUM = AXIS_LOGICAL_MINIMUM - 1
        AXIS_X_USAGE = AXIS_LOGICAL_MAXIMUM - 1
        AXIS_Y_USAGE = AXIS_X_USAGE - 1
        AXIS_INPUT = AXIS_Y_USAGE - 1
        AXIS_REPORT_POP = AXIS_INPUT - 1
        WHEEL_REPORT_COUNT = AXIS_REPORT_POP - 1
        WHEEL_REPORT_SIZE = WHEEL_REPORT_COUNT - 1
        WHEEL_LOGICAL_MINIMUM = WHEEL_REPORT_SIZE - 1
        WHEEL_LOGICAL_MAXIMUM = WHEEL_LOGICAL_MINIMUM - 1
        WHEEL_USAGE = WHEEL_LOGICAL_MAXIMUM - 1
        WHEEL_INPUT = WHEEL_USAGE - 1
        ACPAN_USAGE_PAGE = WHEEL_INPUT - 1
        ACPAN_USAGE = ACPAN_USAGE_PAGE - 1
        ACPAN_INPUT = ACPAN_USAGE - 1
        END_PHYSICAL_COLLECTION = ACPAN_INPUT - 1
        MOUSE_END_COLLECTION = END_PHYSICAL_COLLECTION - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        PHYSICAL_COLLECTION = 0x10
        AXIS_LOGICAL_MINIMUM = 0x18
        AXIS_LOGICAL_MAXIMUM = 0x18
        ACPAN_USAGE = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        POINTER_USAGE = HexList("0901")
        PHYSICAL_COLLECTION = HexList("A100")
        BUTTON_REPORT_COUNT = HexList("9510")
        BUTTON_REPORT_SIZE = HexList("7501")
        BUTTON_LOGICAL_MINIMUM = HexList("1500")
        BUTTON_LOGICAL_MAXIMUM = HexList("2501")
        BUTTON_USAGE_MINIMUM = HexList("1901")
        BUTTON_USAGE_MAXIMUM = HexList("2910")
        AXIS_REPORT_COUNT = HexList("9502")
        AXIS_REPORT_PUSH = HexList("A4")
        AXIS_REPORT_SIZE = HexList("750C")
        AXIS_LOGICAL_MINIMUM = HexList("1600F8")
        AXIS_LOGICAL_MAXIMUM = HexList("26FF07")
        AXIS_X_USAGE = HexList("0930")
        AXIS_Y_USAGE = HexList("0931")
        AXIS_REPORT_POP = HexList("B4")
        WHEEL_LOGICAL_MINIMUM = HexList("1580")
        WHEEL_LOGICAL_MAXIMUM = HexList("257F")
        WHEEL_REPORT_SIZE = HexList("7508")
        WHEEL_REPORT_COUNT = HexList("9501")
        ACPAN_USAGE = HexList("0A3802")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.MOUSE_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Mouse UsagePage',
                 name='mouse_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.GENERIC_USAGE_PAGE),
        BitField(fid=FID.MOUSE_USAGE,
                 length=LEN.USAGE,
                 title='Mouse Usage',
                 name='mouse_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.MOUSE_USAGE),
        BitField(fid=FID.MOUSE_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Mouse Application Collection',
                 name='mouse_app_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.MOUSE_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Mouse Report Id',
                 name='mouse_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.MOUSE_REPORT_ID),
        BitField(fid=FID.POINTER_USAGE,
                 length=LEN.USAGE,
                 title='Pointer Usage',
                 name='pointer_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.POINTER_USAGE),
        BitField(fid=FID.PHYSICAL_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Linked Collection',
                 name='linked_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.PHYSICAL_COLLECTION),
        BitField(fid=FID.BUTTON_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Button Report Count',
                 name='button_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.BUTTON_REPORT_COUNT),
        BitField(fid=FID.BUTTON_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Button Report Size',
                 name='button_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.BUTTON_REPORT_SIZE),
        BitField(fid=FID.BUTTON_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Button Logical Minimum',
                 name='button_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.BUTTON_LOGICAL_MINIMUM),
        BitField(fid=FID.BUTTON_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Button Logical Maximum',
                 name='button_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.BUTTON_LOGICAL_MAXIMUM),
        BitField(fid=FID.BUTTON_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Button Usage Page',
                 name='button_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.BUTTON_USAGE_PAGE),
        BitField(fid=FID.BUTTON_USAGE_MINIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='Button Usage Minimum',
                 name='button_usage_minimum',
                 checks=(CheckHexList(LEN.USAGE_MINIMUM // 8),),
                 default_value=DEFAULT.BUTTON_USAGE_MINIMUM),
        BitField(fid=FID.BUTTON_USAGE_MAXIMUM,
                 length=LEN.USAGE_MAXIMUM,
                 title='Button Usage Maximum',
                 name='button_usage_maximum',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.BUTTON_USAGE_MAXIMUM),
        BitField(fid=FID.BUTTON_INPUT_DATA,
                 length=LEN.INPUT_DATA,
                 title='Button Input',
                 name='button_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.AXIS_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Axis Usage Page',
                 name='axis_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.GENERIC_USAGE_PAGE),
        BitField(fid=FID.AXIS_REPORT_PUSH,
                 length=LEN.PUSH,
                 title='Axis Push',
                 name='axis_push',
                 checks=(CheckHexList(LEN.PUSH // 8),),
                 default_value=DEFAULT.PUSH),
        BitField(fid=FID.AXIS_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Axis Report Count',
                 name='axis_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.AXIS_REPORT_COUNT),
        BitField(fid=FID.AXIS_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Axis Report Size',
                 name='axis_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.AXIS_REPORT_SIZE),
        BitField(fid=FID.AXIS_LOGICAL_MINIMUM,
                 length=LEN.AXIS_LOGICAL_MINIMUM,
                 title='Axis Logical Minimum',
                 name='axis_logical_minimum',
                 checks=(CheckHexList(LEN.AXIS_LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.AXIS_LOGICAL_MINIMUM),
        BitField(fid=FID.AXIS_LOGICAL_MAXIMUM,
                 length=LEN.AXIS_LOGICAL_MAXIMUM,
                 title='Axis Logical Maximum',
                 name='axis_logical_maximum',
                 checks=(CheckHexList(LEN.AXIS_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.AXIS_LOGICAL_MAXIMUM),
        BitField(fid=FID.AXIS_X_USAGE,
                 length=LEN.USAGE,
                 title='X Axis Usage',
                 name='axis_x_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.AXIS_X_USAGE),
        BitField(fid=FID.AXIS_Y_USAGE,
                 length=LEN.USAGE,
                 title='Y Axis Usage',
                 name='axis_y_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.AXIS_Y_USAGE),
        BitField(fid=FID.AXIS_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Axis Input',
                 name='axis_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_REL),
        BitField(fid=FID.AXIS_REPORT_POP,
                 length=LEN.POP,
                 title='Axis pop',
                 name='axis_pop',
                 checks=(CheckHexList(LEN.POP // 8),),
                 default_value=DEFAULT.POP),
        BitField(fid=FID.WHEEL_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Wheel Report Count',
                 name='wheel_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.WHEEL_REPORT_COUNT),
        BitField(fid=FID.WHEEL_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Wheel Report Size',
                 name='wheel_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.WHEEL_REPORT_SIZE),
        BitField(fid=FID.WHEEL_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Wheel Logical Minimum',
                 name='wheel_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.WHEEL_LOGICAL_MINIMUM),
        BitField(fid=FID.WHEEL_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Wheel Logical Maximum',
                 name='wheel_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.WHEEL_LOGICAL_MAXIMUM),
        BitField(fid=FID.WHEEL_USAGE,
                 length=LEN.USAGE,
                 title='Wheel Usage',
                 name='wheel_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.WHEEL_USAGE),
        BitField(fid=FID.WHEEL_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Wheel Input',
                 name='wheel_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_REL),
        BitField(fid=FID.ACPAN_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='AC Pan Usage Page',
                 name='acpan_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE_PAGE),
        BitField(fid=FID.ACPAN_USAGE,
                 length=LEN.ACPAN_USAGE,
                 title='AC Pan Usage',
                 name='acpan_usage',
                 checks=(CheckHexList(LEN.ACPAN_USAGE // 8),),
                 default_value=DEFAULT.ACPAN_USAGE),
        BitField(fid=FID.ACPAN_INPUT,
                 length=LEN.INPUT_DATA,
                 title='AC Pan Input',
                 name='acpan_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_REL),
        BitField(fid=FID.END_PHYSICAL_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='End Linked Collection',
                 name='end_linked_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
        BitField(fid=FID.MOUSE_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Mouse End Collection',
                 name='mouse_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class HidReportMouse12Descriptor


class HidReportMouse16Descriptor(HidReportMouse12Descriptor):
    """
    Define the BLE HID report Mouse 16 bits descriptor.
    """
    BITFIELD_LENGTH = 67  # Bytes

    class FID(HidReportMouse12Descriptor.FID):
        GENERIC_DESKTOP_USAGE_PAGE = HidReportMouse12Descriptor.FID.MOUSE_END_COLLECTION - 1


    class DEFAULT(HidReportMouse12Descriptor.DEFAULT):
        # See ``HidReportMouse12Descriptor.DEFAULT``
        AXIS_REPORT_SIZE = HexList("7510")
        AXIS_LOGICAL_MINIMUM = HexList("160080")
        AXIS_LOGICAL_MAXIMUM = HexList("26FF7F")
    # end class DEFAULT

    FIELDS = \
        HidReportMouse12Descriptor.FIELDS[
            :(HidReportMouse12Descriptor.FID.MOUSE_USAGE_PAGE - HidReportMouse12Descriptor.FID.MOUSE_REPORT_ID)] + \
        (
            BitField(fid=HidReportMouse12Descriptor.FID.MOUSE_REPORT_ID,
                     length=HidReportMouse12Descriptor.LEN.REPORT_ID,
                     title='Mouse Report Id',
                     name='mouse_report_id',
                     checks=(CheckHexList(HidReportMouse12Descriptor.LEN.REPORT_ID // 8),),
                     default_value=DEFAULT.MOUSE16_REPORT_ID),
        ) + \
        HidReportMouse12Descriptor.FIELDS[
            (HidReportMouse12Descriptor.FID.MOUSE_USAGE_PAGE - HidReportMouse12Descriptor.FID.MOUSE_REPORT_ID + 1)
            :(HidReportMouse12Descriptor.FID.MOUSE_USAGE_PAGE - HidReportMouse12Descriptor.FID.AXIS_USAGE_PAGE)] + \
        (
            BitField(fid=HidReportMouse12Descriptor.FID.AXIS_REPORT_SIZE,
                     length=HidReportMouse12Descriptor.LEN.REPORT_SIZE,
                     title='Axis Report Size',
                     name='axis_report_size',
                     checks=(CheckHexList(HidReportMouse12Descriptor.LEN.REPORT_SIZE // 8),),
                     default_value=DEFAULT.AXIS_REPORT_SIZE),
            BitField(fid=HidReportMouse12Descriptor.FID.AXIS_LOGICAL_MINIMUM,
                     length=HidReportMouse12Descriptor.LEN.AXIS_LOGICAL_MINIMUM,
                     title='Axis Logical Minimum',
                     name='axis_logical_minimum',
                     checks=(CheckHexList(HidReportMouse12Descriptor.LEN.AXIS_LOGICAL_MINIMUM // 8),),
                     default_value=DEFAULT.AXIS_LOGICAL_MINIMUM),
            BitField(fid=HidReportMouse12Descriptor.FID.AXIS_LOGICAL_MAXIMUM,
                     length=HidReportMouse12Descriptor.LEN.AXIS_LOGICAL_MAXIMUM,
                     title='Axis Logical Maximum',
                     name='axis_logical_maximum',
                     checks=(CheckHexList(HidReportMouse12Descriptor.LEN.AXIS_LOGICAL_MAXIMUM // 8),),
                     default_value=DEFAULT.AXIS_LOGICAL_MAXIMUM),
            BitField(fid=FID.GENERIC_DESKTOP_USAGE_PAGE,
                     length=HidReportMouse12Descriptor.LEN.USAGE_PAGE,
                     title='Generic Desktop Usage Page',
                     name='generic_desktop_usage_page',
                     checks=(CheckHexList(HidReportMouse12Descriptor.LEN.USAGE_PAGE // 8),),
                     default_value=DEFAULT.GENERIC_USAGE_PAGE),

        ) +\
        HidReportMouse12Descriptor.FIELDS[
            (HidReportMouse12Descriptor.FID.MOUSE_USAGE_PAGE -HidReportMouse12Descriptor.FID.AXIS_X_USAGE):
            (HidReportMouse12Descriptor.FID.MOUSE_USAGE_PAGE - HidReportMouse12Descriptor.FID.AXIS_INPUT+1)]+\
        HidReportMouse12Descriptor.FIELDS[
            (HidReportMouse12Descriptor.FID.MOUSE_USAGE_PAGE -HidReportMouse12Descriptor.FID.WHEEL_REPORT_COUNT):]
# end class HidReportMouse16Descriptor


class HidReportConsumerGenericWithChromeOSDescriptor(ReportDescriptor):
    """
    Define the BLE HID report Consumer generic descriptor with Chrome OS.
    """
    BITFIELD_LENGTH = 26  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        CONS_GEN_USAGE_PAGE = HidReportMouse12Descriptor.FID.MOUSE_END_COLLECTION - 1
        CONS_GEN_USAGE = CONS_GEN_USAGE_PAGE - 1
        CONS_GEN_COLLECTION = CONS_GEN_USAGE - 1
        CONS_GEN_REPORT_ID = CONS_GEN_COLLECTION - 1
        CONS_GEN_REPORT_COUNT = CONS_GEN_REPORT_ID - 1
        CONS_GEN_REPORT_SIZE = CONS_GEN_REPORT_COUNT - 1
        CONS_GEN_LOGICAL_MINIMUM = CONS_GEN_REPORT_SIZE - 1
        CONS_GEN_LOGICAL_MAXIMUM = CONS_GEN_LOGICAL_MINIMUM - 1
        CONS_GEN_USAGE_MINIMUM = CONS_GEN_LOGICAL_MAXIMUM - 1
        CONS_GEN_USAGE_MAXIMUM = CONS_GEN_USAGE_MINIMUM - 1
        CONS_GEN_INPUT = CONS_GEN_USAGE_MAXIMUM - 1
        CONS_GEN_END_COLLECTION = CONS_GEN_INPUT - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        CONS_GEN_USAGE_PAGE = 0x18
        CONS_GEN_LOGICAL_MAXIMUM = 0x18
        CONS_GEN_USAGE_MAXIMUM = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        CONS_GEN_USAGE_PAGE = HexList("060CFF")
        CONS_GEN_REPORT_COUNT = HexList("9502")
        CONS_GEN_REPORT_SIZE = HexList("7510")
        CONS_GEN_LOGICAL_MINIMUM = HexList("1501")
        CONS_GEN_LOGICAL_MAXIMUM = HexList("26FF02")
        CONS_GEN_USAGE_MINIMUM = HexList("1901")
        CONS_GEN_USAGE_MAXIMUM = HexList("2AFF02")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.CONS_GEN_USAGE_PAGE,
                 length=LEN.CONS_GEN_USAGE_PAGE,
                 title='Consumer Generic Usage Page',
                 name='cons_gen_usage_page',
                 checks=(CheckHexList(LEN.CONS_GEN_USAGE_PAGE // 8),),
                 default_value=DEFAULT.CONS_GEN_USAGE_PAGE),
        BitField(fid=FID.CONS_GEN_USAGE,
                 length=LEN.USAGE,
                 title='Consumer GenericUsage',
                 name='cons_gen_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.CONS_GEN_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Consumer GenericCollection',
                 name='cons_gen_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.CONS_GEN_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Consumer GenericReport Id',
                 name='cons_gen_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.CONS_GEN_REPORT_ID),
        BitField(fid=FID.CONS_GEN_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Consumer GenericReport Count',
                 name='cons_gen_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.CONS_GEN_REPORT_COUNT),
        BitField(fid=FID.CONS_GEN_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Consumer GenericReport Size',
                 name='cons_gen_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.CONS_GEN_REPORT_SIZE),
        BitField(fid=FID.CONS_GEN_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Consumer GenericLogical Minimum',
                 name='cons_gen_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.CONS_GEN_LOGICAL_MINIMUM),
        BitField(fid=FID.CONS_GEN_LOGICAL_MAXIMUM,
                 length=LEN.CONS_GEN_LOGICAL_MAXIMUM,
                 title='Consumer GenericLogical Maximum',
                 name='cons_gen_logical_maximum',
                 checks=(CheckHexList(LEN.CONS_GEN_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.CONS_GEN_LOGICAL_MAXIMUM),
        BitField(fid=FID.CONS_GEN_USAGE_MINIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='Consumer GenericUsage Minimum',
                 name='cons_gen_usage_minimum',
                 checks=(CheckHexList(LEN.USAGE_MINIMUM // 8),),
                 default_value=DEFAULT.CONS_GEN_USAGE_MINIMUM),
        BitField(fid=FID.CONS_GEN_USAGE_MAXIMUM,
                 length=LEN.CONS_GEN_USAGE_MAXIMUM,
                 title='Consumer GenericUsage Maximum',
                 name='cons_gen_usage_maximum',
                 checks=(CheckHexList(LEN.CONS_GEN_USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.CONS_GEN_USAGE_MAXIMUM),
        BitField(fid=FID.CONS_GEN_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Consumer GenericInput',
                 name='cons_gen_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.CONS_GEN_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Consumer GenericEnd Collection',
                 name='cons_gen_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class HidReportConsumerGenericWithChromeOSDescriptor


class HidReportConsumerGenericWithoutChromeOSDescriptor(HidReportConsumerGenericWithChromeOSDescriptor):
    """
    Define the BLE HID report Consumer generic descriptor without Chrome OS.
    """
    BITFIELD_LENGTH = 25  # Bytes

    FIELDS = \
        (
            BitField(fid=HidReportConsumerGenericWithChromeOSDescriptor.FID.CONS_GEN_USAGE_PAGE,
                     length=HidReportConsumerGenericWithChromeOSDescriptor.LEN.USAGE_PAGE,
                     title='Consumer Generic Usage Page',
                     name='cons_generic_usage_page',
                     checks=(CheckHexList(HidReportConsumerGenericWithChromeOSDescriptor.LEN.USAGE_PAGE // 8),),
                     default_value=HidReportConsumerGenericWithChromeOSDescriptor.DEFAULT.CONSUMER_USAGE_PAGE),
        ) + \
        HidReportConsumerGenericWithChromeOSDescriptor.FIELDS[
            (HidReportMouse12Descriptor.FID.MOUSE_END_COLLECTION -
             HidReportConsumerGenericWithChromeOSDescriptor.FID.CONS_GEN_USAGE_PAGE):]
# end class HidReportConsumerGenericWithoutChromeOSDescriptor


class HidReportConsumerMinimumDescriptor(ReportDescriptor):
    """
    Define the BLE HID report Consumer minimum descriptor.
    """
    BITFIELD_LENGTH = 26  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        CONS_MIN_USAGE_PAGE = HidReportConsumerGenericWithChromeOSDescriptor.FID.CONS_GEN_END_COLLECTION - 1
        CONS_MIN_USAGE = CONS_MIN_USAGE_PAGE - 1
        CONS_MIN_COLLECTION = CONS_MIN_USAGE - 1
        CONS_MIN_REPORT_ID = CONS_MIN_COLLECTION - 1
        CONS_MIN_REPORT_COUNT = CONS_MIN_REPORT_ID - 1
        CONS_MIN_REPORT_SIZE = CONS_MIN_REPORT_COUNT - 1
        CONS_MIN_LOGICAL_MINIMUM = CONS_MIN_REPORT_SIZE - 1
        CONS_MIN_LOGICAL_MAXIMUM = CONS_MIN_LOGICAL_MINIMUM - 1
        CONS_MIN_USAGE_LIST = CONS_MIN_LOGICAL_MAXIMUM - 1
        CONS_MIN_INPUT = CONS_MIN_USAGE_LIST - 1
        CONS_MIN_RSV_COUNT = CONS_MIN_INPUT - 1
        CONS_MIN_RSV_INPUT = CONS_MIN_RSV_COUNT - 1
        CONS_MIN_END_COLLECTION = CONS_MIN_RSV_INPUT - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        CONS_MIN_USAGE_LIST = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        CONS_MIN_USAGE_PAGE = HexList("050C")
        CONS_MIN_REPORT_SIZE = HexList("7501")
        CONS_MIN_REPORT_COUNT = HexList("9501")
        CONS_MIN_LOGICAL_MINIMUM = HexList("1500")
        CONS_MIN_LOGICAL_MAXIMUM = HexList("2501")
        CONS_MIN_USAGE_LIST = HexList("0AE200")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.CONS_MIN_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Consumer Minimum Usage Page',
                 name='cons_min_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.CONS_MIN_USAGE_PAGE),
        BitField(fid=FID.CONS_MIN_USAGE,
                 length=LEN.USAGE,
                 title='Consumer Minimum Usage',
                 name='cons_min_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.CONS_MIN_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Consumer Minimum Collection',
                 name='cons_min_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.CONS_MIN_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Consumer Minimum Report Id',
                 name='cons_min_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.CONS_MIN_REPORT_ID),
        BitField(fid=FID.CONS_MIN_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Consumer Minimum Report Count',
                 name='cons_min_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.CONS_MIN_REPORT_COUNT),
        BitField(fid=FID.CONS_MIN_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Consumer Minimum Report Size',
                 name='cons_min_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.CONS_MIN_REPORT_SIZE),
        BitField(fid=FID.CONS_MIN_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Consumer Minimum Logical Minimum',
                 name='cons_min_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.CONS_MIN_LOGICAL_MINIMUM),
        BitField(fid=FID.CONS_MIN_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Consumer Minimum Logical Maximum',
                 name='cons_min_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.CONS_MIN_LOGICAL_MAXIMUM),
        BitField(fid=FID.CONS_MIN_USAGE_LIST,
                 length=LEN.CONS_MIN_USAGE_LIST,
                 title='Consumer Minimum Usage List',
                 name='cons_min_usage_list',
                 default_value=DEFAULT.CONS_MIN_USAGE_LIST),
        BitField(fid=FID.CONS_MIN_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Consumer Minimum Input',
                 name='cons_min_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.CONS_MIN_RSV_COUNT,
                 length=LEN.REPORT_ID,
                 title='Consumer Minimum Reserved Report Id',
                 name='cons_min_rsv_count',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.CONS_MIN_RSV_REPORT_ID),
        BitField(fid=FID.CONS_MIN_RSV_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Consumer Minimum Input',
                 name='cons_min_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_CST),
        BitField(fid=FID.CONS_MIN_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Consumer Minimum End Collection',
                 name='cons_min_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class HidReportConsumerMinimumDescriptor


class HidReportConsumerMinimumDescriptorOptimizedInput(HidReportConsumerMinimumDescriptor):
    """
    Define the BLE HID report Consumer minimum descriptor with the input optimization required for counts modulo 8.
    """

    FIELDS = HidReportConsumerMinimumDescriptor.FIELDS\
    [:(HidReportConsumerMinimumDescriptor.FID.CONS_MIN_USAGE_PAGE
       - HidReportConsumerMinimumDescriptor.FID.CONS_MIN_RSV_COUNT)]\
    + HidReportConsumerMinimumDescriptor.FIELDS\
        [(HidReportConsumerMinimumDescriptor.FID.CONS_MIN_USAGE_PAGE
        - HidReportConsumerMinimumDescriptor.FID.CONS_MIN_END_COLLECTION):]
# end class HidReportConsumerMinimumDescriptorOptimizedInput


class HidReportHidppLongReportDescriptor(ReportDescriptor):
    """
    Define the HID++ long-messages descriptor.
    """
    BITFIELD_LENGTH = 28  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``HIDppMessageDescriptor.FID``
        HIDPP20_USAGE_PAGE = HidReportConsumerMinimumDescriptor.FID.CONS_MIN_END_COLLECTION - 1
        HIDPP20_USAGE = HIDPP20_USAGE_PAGE - 1
        HIDPP20_APP_COLLECTION = HIDPP20_USAGE - 1
        HIDPP20_REPORT_ID = HIDPP20_APP_COLLECTION - 1
        HIDPP20_REPORT_COUNT = HIDPP20_REPORT_ID - 1
        HIDPP20_REPORT_SIZE = HIDPP20_REPORT_COUNT - 1
        HIDPP20_LOGICAL_MINIMUM = HIDPP20_REPORT_SIZE - 1
        HIDPP20_LOGICAL_MAXIMUM = HIDPP20_LOGICAL_MINIMUM - 1
        HIDPP20_INPUT_USAGE = HIDPP20_LOGICAL_MAXIMUM - 1
        HIDPP20_INPUT_DATA = HIDPP20_INPUT_USAGE - 1
        HIDPP20_OUTPUT_USAGE = HIDPP20_INPUT_DATA - 1
        HIDPP20_OUTPUT_DATA = HIDPP20_OUTPUT_USAGE - 1
        HIDPP20_END_COLLECTION = HIDPP20_OUTPUT_DATA - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``HIDppMessageDescriptor.LEN``
        HIDPP20_USAGE_PAGE = 0x18
        HIDPP20_USAGE = 0x18
        HIDPP20_LOGICAL_MAXIMUM = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``HIDppMessageDescriptor.DEFAULT``
        HIDPP20_USAGE_PAGE = HexList("0643FF")
        HIDPP20_USAGE = HexList("0A0202")
        HIDPP20_REPORT_COUNT = HexList("9513")
        HIDPP20_REPORT_SIZE = HexList("7508")
        HIDPP20_LOGICAL_MINIMUM = HexList("1500")
        HIDPP20_LOGICAL_MAXIMUM = HexList("26FF00")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.HIDPP20_USAGE_PAGE,
                 length=LEN.HIDPP20_USAGE_PAGE,
                 title='HIDPP20 UsagePage',
                 name='hidpp20_usage_page',
                 checks=(CheckHexList(LEN.HIDPP20_USAGE_PAGE // 8),),
                 default_value=DEFAULT.HIDPP20_USAGE_PAGE),
        BitField(fid=FID.HIDPP20_USAGE,
                 length=LEN.HIDPP20_USAGE,
                 title='HIDPP20 Usage',
                 name='hidpp20_usage',
                 checks=(CheckHexList(LEN.HIDPP20_USAGE // 8),),
                 default_value=DEFAULT.HIDPP20_USAGE),
        BitField(fid=FID.HIDPP20_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='HIDPP20 Application Collection',
                 name='hidpp20_app_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.HIDPP20_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='HIDPP20 Report Id',
                 name='hidpp20_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.HIDPP20_REPORT_ID),
        BitField(fid=FID.HIDPP20_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='HIDPP20 Report Count',
                 name='hidpp20_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.HIDPP20_REPORT_COUNT),
        BitField(fid=FID.HIDPP20_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='HIDPP20 Report Size',
                 name='hidpp20_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.HIDPP20_REPORT_SIZE),
        BitField(fid=FID.HIDPP20_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='HIDPP20 Logical Minimum',
                 name='hidpp20_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.HIDPP20_LOGICAL_MINIMUM),
        BitField(fid=FID.HIDPP20_LOGICAL_MAXIMUM,
                 length=LEN.HIDPP20_LOGICAL_MAXIMUM,
                 title='HIDPP20 Logical Maximum',
                 name='hidpp20_logical_maximum',
                 checks=(CheckHexList(LEN.HIDPP20_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.HIDPP20_LOGICAL_MAXIMUM),
        BitField(fid=FID.HIDPP20_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='HIDPP20 Input Usage',
                 name='hidpp20_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.MOUSE_USAGE),
        BitField(fid=FID.HIDPP20_INPUT_DATA,
                 length=LEN.INPUT_DATA,
                 title='HIDPP20 Input',
                 name='hidpp20_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.HIDPP20_OUTPUT_USAGE,
                 length=LEN.USAGE,
                 title='HIDPP20 Output Usage',
                 name='hidpp20_out_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.MOUSE_USAGE),
        BitField(fid=FID.HIDPP20_OUTPUT_DATA,
                 length=LEN.OUTPUT_DATA,
                 title='HIDPP20 Output',
                 name='hidpp20_output_data',
                 checks=(CheckHexList(LEN.OUTPUT_DATA // 8),),
                 default_value=DEFAULT.OUTPUT_DATA_ABS),
        BitField(fid=FID.HIDPP20_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='HIDPP20 End Collection',
                 name='hidpp20_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class HidReportHidppLongReportDescriptor


class HidReportHidppLongReportDescriptorLegacy(ReportDescriptor):
    """
    Define the HID++ long-messages descriptor, old bytes ordering.
    """
    BITFIELD_LENGTH = 28  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``HIDppMessageDescriptor.FID``
        HIDPP20_USAGE_PAGE = HidReportConsumerMinimumDescriptor.FID.CONS_MIN_END_COLLECTION - 1
        HIDPP20_USAGE = HIDPP20_USAGE_PAGE - 1
        HIDPP20_APP_COLLECTION = HIDPP20_USAGE - 1
        HIDPP20_REPORT_ID = HIDPP20_APP_COLLECTION - 1
        HIDPP20_REPORT_SIZE = HIDPP20_REPORT_ID - 1
        HIDPP20_REPORT_COUNT = HIDPP20_REPORT_SIZE - 1
        HIDPP20_LOGICAL_MINIMUM = HIDPP20_REPORT_COUNT - 1
        HIDPP20_LOGICAL_MAXIMUM = HIDPP20_LOGICAL_MINIMUM - 1
        HIDPP20_INPUT_USAGE = HIDPP20_LOGICAL_MAXIMUM - 1
        HIDPP20_INPUT_DATA = HIDPP20_INPUT_USAGE - 1
        HIDPP20_OUTPUT_USAGE = HIDPP20_INPUT_DATA - 1
        HIDPP20_OUTPUT_DATA = HIDPP20_OUTPUT_USAGE - 1
        HIDPP20_END_COLLECTION = HIDPP20_OUTPUT_DATA - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``HIDppMessageDescriptor.LEN``
        HIDPP20_USAGE_PAGE = 0x18
        HIDPP20_USAGE = 0x18
        HIDPP20_LOGICAL_MAXIMUM = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``HIDppMessageDescriptor.DEFAULT``
        HIDPP20_USAGE_PAGE = HexList("0643FF")
        HIDPP20_USAGE = HexList("0A0202")
        HIDPP20_REPORT_COUNT = HexList("9513")
        HIDPP20_REPORT_SIZE = HexList("7508")
        HIDPP20_LOGICAL_MINIMUM = HexList("1500")
        HIDPP20_LOGICAL_MAXIMUM = HexList("26FF00")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.HIDPP20_USAGE_PAGE,
                 length=LEN.HIDPP20_USAGE_PAGE,
                 title='HIDPP20 UsagePage',
                 name='hidpp20_usage_page',
                 checks=(CheckHexList(LEN.HIDPP20_USAGE_PAGE // 8),),
                 default_value=DEFAULT.HIDPP20_USAGE_PAGE),
        BitField(fid=FID.HIDPP20_USAGE,
                 length=LEN.HIDPP20_USAGE,
                 title='HIDPP20 Usage',
                 name='hidpp20_usage',
                 checks=(CheckHexList(LEN.HIDPP20_USAGE // 8),),
                 default_value=DEFAULT.HIDPP20_USAGE),
        BitField(fid=FID.HIDPP20_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='HIDPP20 Application Collection',
                 name='hidpp20_app_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.HIDPP20_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='HIDPP20 Report Id',
                 name='hidpp20_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.HIDPP20_REPORT_ID),
        BitField(fid=FID.HIDPP20_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='HIDPP20 Report Size',
                 name='hidpp20_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.HIDPP20_REPORT_SIZE),
        BitField(fid=FID.HIDPP20_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='HIDPP20 Report Count',
                 name='hidpp20_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.HIDPP20_REPORT_COUNT),
        BitField(fid=FID.HIDPP20_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='HIDPP20 Logical Minimum',
                 name='hidpp20_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.HIDPP20_LOGICAL_MINIMUM),
        BitField(fid=FID.HIDPP20_LOGICAL_MAXIMUM,
                 length=LEN.HIDPP20_LOGICAL_MAXIMUM,
                 title='HIDPP20 Logical Maximum',
                 name='hidpp20_logical_maximum',
                 checks=(CheckHexList(LEN.HIDPP20_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.HIDPP20_LOGICAL_MAXIMUM),
        BitField(fid=FID.HIDPP20_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='HIDPP20 Input Usage',
                 name='hidpp20_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.MOUSE_USAGE),
        BitField(fid=FID.HIDPP20_INPUT_DATA,
                 length=LEN.INPUT_DATA,
                 title='HIDPP20 Input',
                 name='hidpp20_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.HIDPP20_OUTPUT_USAGE,
                 length=LEN.USAGE,
                 title='HIDPP20 Output Usage',
                 name='hidpp20_out_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.MOUSE_USAGE),
        BitField(fid=FID.HIDPP20_OUTPUT_DATA,
                 length=LEN.OUTPUT_DATA,
                 title='HIDPP20 Output',
                 name='hidpp20_output_data',
                 checks=(CheckHexList(LEN.OUTPUT_DATA // 8),),
                 default_value=DEFAULT.OUTPUT_DATA_ABS),
        BitField(fid=FID.HIDPP20_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='HIDPP20 End Collection',
                 name='hidpp20_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class HidReportHidppLongReportDescriptor


class HidReportLogiDescriptor(ReportDescriptor):
    """
    Define the Logitech Report
    """
    BITFIELD_LENGTH = 23

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        LOGI_USAGE_PAGE = HidReportConsumerGenericWithoutChromeOSDescriptor.FID.CONS_GEN_END_COLLECTION - 1
        LOGI_USAGE = LOGI_USAGE_PAGE - 1
        LOGI_COLLECTION = LOGI_USAGE - 1
        LOGI_REPORT_ID = LOGI_COLLECTION - 1
        LOGI_REPORT_COUNT = LOGI_REPORT_ID - 1
        LOGI_REPORT_SIZE = LOGI_REPORT_COUNT - 1
        LOGI_LOGICAL_MINIMUM = LOGI_REPORT_SIZE - 1
        LOGI_LOGICAL_MAXIMUM = LOGI_LOGICAL_MINIMUM - 1
        LOGI_FEATURE_USAGE = LOGI_LOGICAL_MAXIMUM - 1
        LOGI_FEATURE = LOGI_FEATURE_USAGE - 1
        LOGI_END_COLLECTION = LOGI_FEATURE - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``HIDppMessageDescriptor.LEN``
        pass
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``HIDppMessageDescriptor.DEFAULT``
        LOGI_USAGE_PAGE = HexList("0647FF")
        LOGI_USAGE = HexList("0901")
        LOGI_COLLECTION = HexList("A101")
        LOGI_REPORT_ID = HexList("85F0")
        LOGI_REPORT_COUNT = HexList("9504")
        LOGI_REPORT_SIZE = HexList("7508")
        LOGI_LOGICAL_MINIMUM = HexList("1500")
        LOGI_LOGICAL_MAXIMUM = HexList("26FF00")
        LOGI_FEATURE_USAGE = HexList("0901")
        LOGI_FEATURE = HexList("B102")
        LOGI_END_COLLECTION = HexList("C0")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.LOGI_USAGE_PAGE,
                 length=LEN.LONG_USAGE_PAGE,
                 title='Logi Usage Page',
                 name='logi_usage_page',
                 checks=(CheckHexList(LEN.LONG_USAGE_PAGE // 8),),
                 default_value=DEFAULT.LOGI_USAGE_PAGE),
        BitField(fid=FID.LOGI_USAGE,
                 length=LEN.USAGE,
                 title='Logi Usage',
                 name='logi_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.LOGI_USAGE),
        BitField(fid=FID.LOGI_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Logi Collection',
                 name='logi_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.LOGI_COLLECTION),
        BitField(fid=FID.LOGI_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Logi Report Id',
                 name='logi_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.LOGI_REPORT_ID),
        BitField(fid=FID.LOGI_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Logi Report Count',
                 name='logi_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.LOGI_REPORT_COUNT),
        BitField(fid=FID.LOGI_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Logi Report Size',
                 name='logi_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.LOGI_REPORT_SIZE),
        BitField(fid=FID.LOGI_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Logi Logical Minimum',
                 name='logi_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.LOGI_LOGICAL_MINIMUM),
        BitField(fid=FID.LOGI_LOGICAL_MAXIMUM,
                 length=LEN.LONG_LOGICAL_MAXIMUM,
                 title='Logi Logical Maximum',
                 name='logi_logical_maximum',
                 checks=(CheckHexList(LEN.LONG_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.LOGI_LOGICAL_MAXIMUM),
        BitField(fid=FID.LOGI_FEATURE_USAGE,
                 length=LEN.USAGE,
                 title='Logi Feature Usage',
                 name='logi_feature_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.LOGI_USAGE),
        BitField(fid=FID.LOGI_FEATURE,
                 length=LEN.FEATURE,
                 title='Logi Feature',
                 name='logi_feature',
                 checks=(CheckHexList(LEN.FEATURE // 8),),
                 default_value=DEFAULT.LOGI_FEATURE),
        BitField(fid=FID.LOGI_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Logi End Collection',
                 name='logi_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.LOGI_END_COLLECTION),
    )
# end class HidReportLogiDescriptor


class HidReportMap(ReportDescriptor):
    """
    Define the BLE Hid Report Map Value
    """
    # 207 bytes
    BITFIELD_LENGTH = \
        HidReportKeyboardLedDescriptor.BITFIELD_LENGTH + HidReportMouse12Descriptor.BITFIELD_LENGTH + \
        HidReportConsumerGenericWithChromeOSDescriptor.BITFIELD_LENGTH + \
        HidReportConsumerMinimumDescriptor.BITFIELD_LENGTH + HidReportHidppLongReportDescriptor.BITFIELD_LENGTH

    FIELDS = \
        HidReportKeyboardLedDescriptor.FIELDS + HidReportMouse12Descriptor.FIELDS + \
        HidReportConsumerGenericWithChromeOSDescriptor.FIELDS + HidReportConsumerMinimumDescriptor.FIELDS + \
        HidReportHidppLongReportDescriptor.FIELDS
# end class HidReportMap


class HidGamingReportMap(ReportDescriptor):
    """
    Define the BLE Hid Report Map Value
    """
    # 203 bytes
    BITFIELD_LENGTH = \
        HidReportKeyboardLedDescriptor.BITFIELD_LENGTH + HidReportMouse16Descriptor.BITFIELD_LENGTH + \
        HidReportConsumerGenericWithoutChromeOSDescriptor.BITFIELD_LENGTH + HidReportLogiDescriptor.BITFIELD_LENGTH + \
        HidReportHidppLongReportDescriptor.BITFIELD_LENGTH

    FIELDS = \
        HidReportKeyboardLedDescriptor.FIELDS + HidReportMouse16Descriptor.FIELDS + \
        HidReportConsumerGenericWithoutChromeOSDescriptor.FIELDS + HidReportLogiDescriptor.FIELDS + \
        HidReportHidppLongReportDescriptor.FIELDS
# end class HidGamingReportMap


class HidGamingMouseReportMap(ReportDescriptor):
    """
    Define the BLE Hid Report Map Value for a Gaming Mouse NPI or platform
    """
    # 158 bytes
    BITFIELD_LENGTH = \
        HidReportKeyboardDescriptor.BITFIELD_LENGTH + HidReportMouse16Descriptor.BITFIELD_LENGTH + \
        HidReportLogiDescriptor.BITFIELD_LENGTH + HidReportHidppLongReportDescriptor.BITFIELD_LENGTH

    FIELDS = \
        HidReportKeyboardDescriptor.FIELDS + HidReportMouse16Descriptor.FIELDS + \
        HidReportLogiDescriptor.FIELDS + HidReportHidppLongReportDescriptor.FIELDS
# end class HidGamingMouseReportMap


class HidMouseReportMap(ReportDescriptor):
    """
    Define the BLE Hid Report Map Value for a mouse
    """
    # 97 bytes
    BITFIELD_LENGTH = \
        HidReportMouse12Descriptor.BITFIELD_LENGTH + HidReportHidppLongReportDescriptor.BITFIELD_LENGTH

    FIELDS = \
        HidReportMouse12Descriptor.FIELDS + HidReportHidppLongReportDescriptor.FIELDS
# end class HidMouseReportMap

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
