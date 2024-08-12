#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.interfacedescriptors
:brief: USB interface descriptors definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/11
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckHexList
from pyhid.hid.blereportmap import HidGamingReportMap
from pyhid.hid.blereportmap import HidGamingMouseReportMap
from pyhid.hid.blereportmap import HidMouseReportMap
from pyhid.hid.blereportmap import HidReportMap
from pyhid.hid.descriptor import LongUsagePageReportDescriptor
from pyhid.hid.descriptor import LongUsageReportDescriptor
from pyhid.hid.descriptor import ReportDescriptor
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DescriptorDispatcher(TimestampedBitFieldContainerMixin):
    """
    This class defines the generic format of an interface usb descriptor
    """
    BITFIELD_LENGTH = 0  # Variable

    class LEN(IntEnum):
        """
        FIELDS length
        """
        DESCRIPTOR_DATA_MIN = 0xB8
        # Digitizer = 409 bytes + Margin = 25 bytes
        DESCRIPTOR_DATA_MAX = 0xD90
    # end class LEN

    class FID(IntEnum):
        """
        FIELDS identifier
        """
        DESCRIPTOR_DATA = 0xFF
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.DESCRIPTOR_DATA,
            length=LEN.DESCRIPTOR_DATA_MAX,
            title='Descriptor Data',
            name='descriptor_data',
            checks=(CheckHexList(max_length=(LEN.DESCRIPTOR_DATA_MAX // 8),
                                 min_length=(LEN.DESCRIPTOR_DATA_MIN // 8), ),)),
    )

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        dispatcher = super().fromHexList(*args, **kwargs)
        if dispatcher.descriptor_data[0] == ReportDescriptor.DEFAULT.GENERIC_USAGE_PAGE[0]:
            base_descriptor = ReportDescriptor.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
        elif dispatcher.descriptor_data[0:2] == LongUsagePageReportDescriptor.DEFAULT.HIDPP_RECEIVER_USAGE_PAGE[0:2]:
            base_descriptor = LongUsagePageReportDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                        timestamp=dispatcher.timestamp)
        elif dispatcher.descriptor_data[0:2] == LongUsageReportDescriptor.DEFAULT.HIDPP_USAGE_PAGE[0:2]:
            base_descriptor = LongUsageReportDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                    timestamp=dispatcher.timestamp)
        else:
            raise Exception(f'Unkown usage page tag & size: {dispatcher.descriptor_data[0]}')
        # end if
        if base_descriptor.usage == ReportDescriptor.DEFAULT.KEYBOARD_USAGE:
            if len(dispatcher.descriptor_data) == KeyboardBitmapKeyDescriptor.BITFIELD_LENGTH:
                return KeyboardBitmapKeyDescriptor.fromHexList(dispatcher.descriptor_data,
                                                               timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == KeyboardReceiverDescriptor.BITFIELD_LENGTH:
                return KeyboardReceiverDescriptor.fromHexList(dispatcher.descriptor_data,
                                                              timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == KeyboardDeviceDescriptor.BITFIELD_LENGTH:
                return KeyboardDeviceDescriptor.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == KeyboardInterfaceDescriptor.BITFIELD_LENGTH:
                return KeyboardInterfaceDescriptor.fromHexList(dispatcher.descriptor_data,
                                                               timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == KeyboardBitmapInterfaceDescriptor.BITFIELD_LENGTH:
                return KeyboardBitmapInterfaceDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                     timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == KeyboardBitmapReceiverDescriptor.BITFIELD_LENGTH:
                return KeyboardBitmapReceiverDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                    timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == HidReportMap.BITFIELD_LENGTH:
                return HidReportMap.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == HidGamingReportMap.BITFIELD_LENGTH:
                return HidGamingReportMap.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == HidGamingMouseReportMap.BITFIELD_LENGTH:
                return HidGamingMouseReportMap.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            # end if
        elif base_descriptor.usage == ReportDescriptor.DEFAULT.MOUSE_USAGE:
            if len(dispatcher.descriptor_data) == MouseKeyDescriptor.BITFIELD_LENGTH:
                return MouseKeyDescriptor.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == MouseNvidiaExtensionKeyDescriptor.BITFIELD_LENGTH:
                return MouseNvidiaExtensionKeyDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                     timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == MouseReceiverNvidiaExtensionKeyDescriptor.BITFIELD_LENGTH:
                return MouseReceiverNvidiaExtensionKeyDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                             timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == MouseInterfaceDescriptor.BITFIELD_LENGTH:
                return MouseInterfaceDescriptor.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == MouseReceiverInterfaceDescriptor.BITFIELD_LENGTH:
                return MouseReceiverInterfaceDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                    timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == HidMouseReportMap.BITFIELD_LENGTH:
                return HidMouseReportMap.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            else:
                return ReportDescriptor.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            # end if
        elif base_descriptor.usage == ReportDescriptor.DEFAULT.HIDPP7_USAGE:
            if len(dispatcher.descriptor_data) == HIDppInterfaceDescriptor.BITFIELD_LENGTH:
                return HIDppInterfaceDescriptor.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
            # end if
        elif base_descriptor.usage == ReportDescriptor.DEFAULT.CONSUMER_USAGE:
            if len(dispatcher.descriptor_data) == HIDppReceiverInterfaceDescriptor.BITFIELD_LENGTH:
                if dispatcher.descriptor_data[9:10] == HIDppShortMessageDescriptor.DEFAULT.HIDPP_REPORT_SIZE[0:1]:
                    return DrifterHIDppInterfaceDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                        timestamp=dispatcher.timestamp)
                else:
                    return HIDppReceiverInterfaceDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                    timestamp=dispatcher.timestamp)
                # end if
        elif base_descriptor.usage == VlpInterfaceDescriptor.DEFAULT.VLP_MODE_1A02_USAGE:
            return VlpInterfaceDescriptor.fromHexList(dispatcher.descriptor_data,
                                                      timestamp=dispatcher.timestamp)
            # end if
        elif base_descriptor.usage == ReportDescriptor.DEFAULT.TOUCHPAD_USAGE:
            if len(dispatcher.descriptor_data) == WindowsDigitizer5FingersDescriptor.BITFIELD_LENGTH:
                return WindowsDigitizer5FingersDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                      timestamp=dispatcher.timestamp)
            elif len(dispatcher.descriptor_data) == WindowsDigitizer3FingersDescriptor.BITFIELD_LENGTH:
                return WindowsDigitizer3FingersDescriptor.fromHexList(dispatcher.descriptor_data,
                                                                      timestamp=dispatcher.timestamp)
            # end if
        else:
            return ReportDescriptor.fromHexList(dispatcher.descriptor_data, timestamp=dispatcher.timestamp)
        # end if
    # end def fromHexList
# end class DescriptorDispatcher


# --------------
# USB Interfaces
# --------------
class ConsumerGenericKeyDescriptor(ReportDescriptor):
    """
    Define the USB Consumer Generic without Chrome OS support key descriptor.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.l1r4twz115go
    """
    BITFIELD_LENGTH = 25  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        CONS_GEN_USAGE_PAGE = 0xC0
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
        CONS_GEN_LOGICAL_MAXIMUM = 0x18
        CONS_GEN_USAGE_MAXIMUM = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        CONS_GEN_REPORT_COUNT = HexList("9502")
        CONS_GEN_REPORT_SIZE = HexList("7510")
        CONS_GEN_LOGICAL_MINIMUM = HexList("1501")
        CONS_GEN_LOGICAL_MAXIMUM = HexList("26FF02")
        CONS_GEN_USAGE_MINIMUM = HexList("1901")
        CONS_GEN_USAGE_MAXIMUM = HexList("2AFF02")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.CONS_GEN_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Consumer GenericUsage Page',
                 name='cons_gen_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE_PAGE),
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
        # TODO Check with DEFAULT.INPUT_DATA_ARY
        BitField(fid=FID.CONS_GEN_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Consumer GenericEnd Collection',
                 name='cons_gen_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class ConsumerGenericKeyDescriptor


class ConsumerGenericChromeOSKeyDescriptor(ConsumerGenericKeyDescriptor):
    """
    Define the USB Consumer Generic with Chrome OS support key descriptor.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=kix.kddwoi7zl0ou
    """
    BITFIELD_LENGTH = 26  # Bytes

    class LEN(ConsumerGenericKeyDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        CONS_GEN_CHROME_USAGE_PAGE = 0x18
    # end class LEN

    class DEFAULT(ConsumerGenericKeyDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        CONS_GEN_CHROME_USAGE_PAGE = HexList("060CFF")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=ConsumerGenericKeyDescriptor.FID.CONS_GEN_USAGE_PAGE,
                 length=LEN.CONS_GEN_CHROME_USAGE_PAGE,
                 title='Consumer Generic Chrome Usage Page',
                 name='cons_gen_chrome_usage_page',
                 checks=(CheckHexList(LEN.CONS_GEN_CHROME_USAGE_PAGE // 8),),
                 default_value=DEFAULT.CONS_GEN_CHROME_USAGE_PAGE),
             ) + ConsumerGenericKeyDescriptor.FIELDS[ConsumerGenericKeyDescriptor.FID.CONS_GEN_USAGE_PAGE -
                                                     ConsumerGenericKeyDescriptor.FID.CONS_GEN_USAGE:
                                                     ConsumerGenericKeyDescriptor.FID.CONS_GEN_USAGE_PAGE -
                                                     ConsumerGenericKeyDescriptor.FID.CONS_GEN_INPUT] + (
        BitField(fid=ConsumerGenericKeyDescriptor.FID.CONS_GEN_INPUT,
                 length=LEN.INPUT_DATA,
                 title='MultiMedia Input',
                 name='mm_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=ConsumerGenericKeyDescriptor.FID.CONS_GEN_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='MultiMedia End Collection',
                 name='mm_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class ConsumerGenericChromeOSKeyDescriptor


class GenericDesktopSystemControlKeyDescriptor(ReportDescriptor):
    """
    Define the USB Generic Desktop System Control Key descriptor.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.7ysta15v66yk
    """
    BITFIELD_LENGTH = 39  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        PWR_USAGE_PAGE = 0xB0
        PWR_USAGE = PWR_USAGE_PAGE - 1
        PWR_COLLECTION = PWR_USAGE - 1
        PWR_REPORT_ID = PWR_COLLECTION - 1
        PWR_REPORT_COUNT = PWR_REPORT_ID - 1
        PWR_REPORT_SIZE = PWR_REPORT_COUNT - 1
        PWR_LOGICAL_MINIMUM = PWR_REPORT_SIZE - 1
        PWR_LOGICAL_MAXIMUM = PWR_LOGICAL_MINIMUM - 1
        PWR_SLEEP_USAGE = PWR_LOGICAL_MAXIMUM - 1
        PWR_DOWN_USAGE = PWR_SLEEP_USAGE - 1
        PWR_WAKE_UP_USAGE = PWR_DOWN_USAGE - 1
        PWR_INPUT = PWR_WAKE_UP_USAGE - 1
        SYS_REPORT_SIZE = PWR_INPUT - 1
        SYS_LOGICAL_MINIMUM = SYS_REPORT_SIZE - 1
        SYS_LOGICAL_MAXIMUM = SYS_LOGICAL_MINIMUM - 1
        SYS_DISTURB_USAGE = SYS_LOGICAL_MAXIMUM - 1
        SYS_INPUT = SYS_DISTURB_USAGE - 1
        RSV_REPORT_SIZE = SYS_INPUT - 1
        RSV_INPUT = RSV_REPORT_SIZE - 1
        PWR_END_COLLECTION = RSV_INPUT - 1
    # end class FID

    LEN = ReportDescriptor.LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        PWR_REPORT_COUNT = HexList("9501")
        PWR_REPORT_SIZE = HexList("7502")
        PWR_LOGICAL_MINIMUM = HexList("1501")
        PWR_LOGICAL_MAXIMUM = HexList("2503")
        PWR_SLEEP_USAGE = HexList("0982")
        PWR_DOWN_USAGE = HexList("0981")
        PWR_WAKE_UP_USAGE = HexList("0983")
        SYS_REPORT_SIZE = HexList("7501")
        SYS_LOGICAL_MINIMUM = HexList("1500")
        SYS_LOGICAL_MAXIMUM = HexList("2501")
        SYS_DISTURB_USAGE = HexList("099B")
        RSV_REPORT_SIZE = HexList("7505")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.PWR_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Power Usage Page',
                 name='pwr_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.GENERIC_USAGE_PAGE),
        BitField(fid=FID.PWR_USAGE,
                 length=LEN.USAGE,
                 title='Power Usage',
                 name='pwr_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.POWER_USAGE),
        BitField(fid=FID.PWR_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Power Collection',
                 name='pwr_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.PWR_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Power Report Id',
                 name='pwr_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.PWR_REPORT_ID),
        BitField(fid=FID.PWR_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Power Report Count',
                 name='pwr_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.PWR_REPORT_COUNT),
        BitField(fid=FID.PWR_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Power Report Size',
                 name='pwr_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.PWR_REPORT_SIZE),
        BitField(fid=FID.PWR_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Power Logical Minimum',
                 name='pwr_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.PWR_LOGICAL_MINIMUM),
        BitField(fid=FID.PWR_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Power Logical Maximum',
                 name='pwr_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.PWR_LOGICAL_MAXIMUM),
        BitField(fid=FID.PWR_SLEEP_USAGE,
                 length=LEN.USAGE,
                 title='Power Sleep Usage',
                 name='pwr_sleep_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_SLEEP_USAGE),
        BitField(fid=FID.PWR_DOWN_USAGE,
                 length=LEN.USAGE,
                 title='Power Down Usage',
                 name='pwr_down_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_DOWN_USAGE),
        BitField(fid=FID.PWR_WAKE_UP_USAGE,
                 length=LEN.USAGE,
                 title='Power WakeUp Usage',
                 name='pwr_wake_up_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_WAKE_UP_USAGE),
        BitField(fid=FID.PWR_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Power Input',
                 name='pwr_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.SYS_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='System Report Size',
                 name='sys_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.SYS_REPORT_SIZE),
        BitField(fid=FID.SYS_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='System Logical Minimum',
                 name='sys_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.SYS_LOGICAL_MINIMUM),
        BitField(fid=FID.SYS_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='System Logical Maximum',
                 name='sys_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.SYS_LOGICAL_MAXIMUM),
        BitField(fid=FID.SYS_DISTURB_USAGE,
                 length=LEN.USAGE,
                 title='System Sleep Usage',
                 name='sys_sleep_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.SYS_DISTURB_USAGE),
        BitField(fid=FID.SYS_INPUT,
                 length=LEN.INPUT_DATA,
                 title='System Input',
                 name='sys_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_REL),
        BitField(fid=FID.RSV_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Reserved Report Size',
                 name='rsv_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.RSV_REPORT_SIZE),
        BitField(fid=FID.RSV_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Reserved Input',
                 name='rsv_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_CST),
        BitField(fid=FID.PWR_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Power End Collection',
                 name='pwr_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class GenericDesktopSystemControlKeyDescriptor


class GenericDesktopSystemControlKeyboardV14Descriptor(GenericDesktopSystemControlKeyDescriptor):
    """
    Define the USB Generic Desktop System Control Key descriptor for keyboard supporting the version 1.4.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.7ysta15v66yk
    """
    BITFIELD_LENGTH = 45  # Bytes

    class FID(GenericDesktopSystemControlKeyDescriptor.FID):
        # See ``GenericDesktopSystemControlKeyDescriptor.FID``
        SYS_REPORT_COUNT = GenericDesktopSystemControlKeyDescriptor.FID.PWR_INPUT - 1
        SYS_REPORT_SIZE = SYS_REPORT_COUNT - 1
        SYS_LOGICAL_MINIMUM = SYS_REPORT_SIZE - 1
        SYS_LOGICAL_MAXIMUM = SYS_LOGICAL_MINIMUM - 1
        SYS_DISTURB_USAGE = SYS_LOGICAL_MAXIMUM - 1
        SYS_MICROPHONE_MUTE = SYS_DISTURB_USAGE - 1
        SYS_INPUT = SYS_MICROPHONE_MUTE - 1
        RSV_REPORT_COUNT = SYS_INPUT - 1
        RSV_REPORT_SIZE = RSV_REPORT_COUNT - 1
        RSV_INPUT = RSV_REPORT_SIZE - 1
        PWR_END_COLLECTION = RSV_INPUT - 1
    # end class FID

    LEN = GenericDesktopSystemControlKeyDescriptor.LEN

    class DEFAULT(GenericDesktopSystemControlKeyDescriptor.DEFAULT):
        # See ``GenericDesktopSystemControlKeyDescriptor.DEFAULT``
        SYS_REPORT_COUNT = HexList("9502")
        SYS_MICROPHONE_MUTE = HexList("09A9")
        RSV_REPORT_COUNT = HexList("9501")
        RSV_REPORT_SIZE = HexList("7504")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.PWR_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Power Usage Page',
                 name='pwr_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.GENERIC_USAGE_PAGE),
        BitField(fid=FID.PWR_USAGE,
                 length=LEN.USAGE,
                 title='Power Usage',
                 name='pwr_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.POWER_USAGE),
        BitField(fid=FID.PWR_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Power Collection',
                 name='pwr_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.PWR_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Power Report Id',
                 name='pwr_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.PWR_REPORT_ID),
        BitField(fid=FID.PWR_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Power Report Count',
                 name='pwr_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.PWR_REPORT_COUNT),
        BitField(fid=FID.PWR_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Power Report Size',
                 name='pwr_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.PWR_REPORT_SIZE),
        BitField(fid=FID.PWR_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Power Logical Minimum',
                 name='pwr_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.PWR_LOGICAL_MINIMUM),
        BitField(fid=FID.PWR_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Power Logical Maximum',
                 name='pwr_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.PWR_LOGICAL_MAXIMUM),
        BitField(fid=FID.PWR_SLEEP_USAGE,
                 length=LEN.USAGE,
                 title='Power Sleep Usage',
                 name='pwr_sleep_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_SLEEP_USAGE),
        BitField(fid=FID.PWR_DOWN_USAGE,
                 length=LEN.USAGE,
                 title='Power Down Usage',
                 name='pwr_down_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_DOWN_USAGE),
        BitField(fid=FID.PWR_WAKE_UP_USAGE,
                 length=LEN.USAGE,
                 title='Power WakeUp Usage',
                 name='pwr_wake_up_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_WAKE_UP_USAGE),
        BitField(fid=FID.PWR_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Power Input',
                 name='pwr_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.SYS_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='System Report Count',
                 name='sys_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.SYS_REPORT_COUNT),
        BitField(fid=FID.SYS_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='System Report Size',
                 name='sys_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.SYS_REPORT_SIZE),
        BitField(fid=FID.SYS_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='System Logical Minimum',
                 name='sys_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.SYS_LOGICAL_MINIMUM),
        BitField(fid=FID.SYS_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='System Logical Maximum',
                 name='sys_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.SYS_LOGICAL_MAXIMUM),
        BitField(fid=FID.SYS_DISTURB_USAGE,
                 length=LEN.USAGE,
                 title='System Do Not Disturb',
                 name='sys_do_not_disturb',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.SYS_DISTURB_USAGE),
        BitField(fid=FID.SYS_MICROPHONE_MUTE,
                 length=LEN.USAGE,
                 title='System Microphone Mute',
                 name='sys_microphone_mute',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.SYS_MICROPHONE_MUTE),
        BitField(fid=FID.SYS_INPUT,
                 length=LEN.INPUT_DATA,
                 title='System Input',
                 name='sys_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_REL),
        BitField(fid=FID.RSV_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Reserved Report Count',
                 name='rsv_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.RSV_REPORT_COUNT),
        BitField(fid=FID.RSV_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Reserved Report Size',
                 name='rsv_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.RSV_REPORT_SIZE),
        BitField(fid=FID.RSV_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Reserved Input',
                 name='rsv_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_CST),
        BitField(fid=FID.PWR_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Power End Collection',
                 name='pwr_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class GenericDesktopSystemControlKeyboardV14Descriptor


class GenericDesktopSystemControlDescriptor(ReportDescriptor):
    """
    Define the USB Generic Desktop System Control descriptor, if the device is not a BOLT receiver or a Keyboard.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.7ysta15v66yk
    """
    BITFIELD_LENGTH = 29  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        PWR_USAGE_PAGE = 0xB0
        PWR_USAGE = PWR_USAGE_PAGE - 1
        PWR_COLLECTION = PWR_USAGE - 1
        PWR_REPORT_ID = PWR_COLLECTION - 1
        PWR_REPORT_COUNT = PWR_REPORT_ID - 1
        PWR_REPORT_SIZE = PWR_REPORT_COUNT - 1
        PWR_LOGICAL_MINIMUM = PWR_REPORT_SIZE - 1
        PWR_LOGICAL_MAXIMUM = PWR_LOGICAL_MINIMUM - 1
        PWR_SLEEP_USAGE = PWR_LOGICAL_MAXIMUM - 1
        PWR_DOWN_USAGE = PWR_SLEEP_USAGE - 1
        PWR_WAKE_UP_USAGE = PWR_DOWN_USAGE - 1
        PWR_INPUT = PWR_WAKE_UP_USAGE - 1
        RSV_REPORT_COUNT = PWR_INPUT - 1
        RSV_REPORT_SIZE = RSV_REPORT_COUNT - 1
        RSV_INPUT = RSV_REPORT_SIZE - 1
        PWR_END_COLLECTION = RSV_INPUT - 1
    # end class FID

    LEN = ReportDescriptor.LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        PWR_REPORT_COUNT = HexList("9501")
        PWR_REPORT_SIZE = HexList("7502")
        PWR_LOGICAL_MINIMUM = HexList("1501")
        PWR_LOGICAL_MAXIMUM = HexList("2503")
        PWR_SLEEP_USAGE = HexList("0982")
        PWR_DOWN_USAGE = HexList("0981")
        PWR_WAKE_UP_USAGE = HexList("0983")
        RSV_REPORT_SIZE = HexList("7506")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.PWR_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Power Usage Page',
                 name='pwr_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.GENERIC_USAGE_PAGE),
        BitField(fid=FID.PWR_USAGE,
                 length=LEN.USAGE,
                 title='Power Usage',
                 name='pwr_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.POWER_USAGE),
        BitField(fid=FID.PWR_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Power Collection',
                 name='pwr_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.PWR_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Power Report Id',
                 name='pwr_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.PWR_REPORT_ID),
        BitField(fid=FID.PWR_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Power Report Count',
                 name='pwr_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.PWR_REPORT_COUNT),
        BitField(fid=FID.PWR_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Power Report Size',
                 name='pwr_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.PWR_REPORT_SIZE),
        BitField(fid=FID.PWR_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Power Logical Minimum',
                 name='pwr_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.PWR_LOGICAL_MINIMUM),
        BitField(fid=FID.PWR_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Power Logical Maximum',
                 name='pwr_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.PWR_LOGICAL_MAXIMUM),
        BitField(fid=FID.PWR_SLEEP_USAGE,
                 length=LEN.USAGE,
                 title='Power Sleep Usage',
                 name='pwr_sleep_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_SLEEP_USAGE),
        BitField(fid=FID.PWR_DOWN_USAGE,
                 length=LEN.USAGE,
                 title='Power Down Usage',
                 name='pwr_down_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_DOWN_USAGE),
        BitField(fid=FID.PWR_WAKE_UP_USAGE,
                 length=LEN.USAGE,
                 title='Power WakeUp Usage',
                 name='pwr_wake_up_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.PWR_WAKE_UP_USAGE),
        BitField(fid=FID.PWR_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Power Input',
                 name='pwr_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.RSV_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Reserved Report Size',
                 name='rsv_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.RSV_REPORT_SIZE),
        BitField(fid=FID.RSV_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Reserved Input',
                 name='rsv_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_CST),
        BitField(fid=FID.PWR_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Power End Collection',
                 name='pwr_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class GenericDesktopSystemControlDescriptor


class GenericDesktopSystemControlDescriptorKeyboard(GenericDesktopSystemControlDescriptor):
    """
    Define the USB Generic Desktop System Control descriptor, if the device is a Keyboard.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.7ysta15v66yk
    """
    LEN = GenericDesktopSystemControlDescriptor.LEN

    class FID(GenericDesktopSystemControlDescriptor.FID):
        # See ``ReportDescriptor.FID``
        DND_REPORT_COUNT = GenericDesktopSystemControlDescriptor.FID.PWR_END_COLLECTION - 1
        DND_REPORT_SIZE = DND_REPORT_COUNT - 1
        DND_LOGICAL_MINIMUM = DND_REPORT_SIZE - 1
        DND_LOGICAL_MAXIMUM = DND_LOGICAL_MINIMUM - 1
        DND_USAGE_DND = DND_LOGICAL_MAXIMUM - 1
        DND_USAGE_MICROPHONE_MUTE = DND_USAGE_DND - 1
        DND_INPUT = DND_USAGE_MICROPHONE_MUTE - 1
    # end class FID

    class DEFAULT(GenericDesktopSystemControlDescriptor.DEFAULT):
        DND_REPORT_COUNT = HexList("9502")
        DND_REPORT_SIZE = HexList("7501")
        DND_LOGICAL_MINIMUM = HexList("1500")
        DND_LOGICAL_MAXIMUM = HexList("2501")
        DND_USAGE_DND = HexList("099B")
        DND_USAGE_MICROPHONE_MUTE = HexList("09A9")
        DND_INPUT = HexList("8106")
        RSV_REPORT_COUNT = HexList("9501")
        RSV_REPORT_SIZE = HexList("7504")
    # end class DEFAULT

    FIELDS = GenericDesktopSystemControlDescriptor.FIELDS[
             :(GenericDesktopSystemControlDescriptor.FID.PWR_USAGE_PAGE
               - GenericDesktopSystemControlDescriptor.FID.RSV_REPORT_COUNT)] \
             + (

             BitField(fid=FID.DND_REPORT_COUNT,
                      length=LEN.REPORT_COUNT,
                      title="Do Not Disturb Report Count",
                      name='dnd_report_count',
                      checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                      default_value=DEFAULT.DND_REPORT_COUNT),
             BitField(fid=FID.DND_REPORT_SIZE,
                     length=LEN.REPORT_SIZE,
                     title="Do Not Disturb Report SIZE",
                     name='dnd_report_size',
                     checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                     default_value=DEFAULT.DND_REPORT_SIZE),
             BitField(fid=FID.DND_LOGICAL_MINIMUM,
                     length=LEN.LOGICAL_MINIMUM,
                     title="Do Not Disturb Logical minimum",
                     name='dnd_logical_minimum',
                     checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                     default_value=DEFAULT.DND_LOGICAL_MINIMUM),
             BitField(fid=FID.DND_LOGICAL_MAXIMUM,
                      length=LEN.LOGICAL_MAXIMUM,
                      title="Do Not Disturb Logical maximum",
                      name='dnd_logical_maximum',
                      checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                      default_value=DEFAULT.DND_LOGICAL_MAXIMUM),
             BitField(fid=FID.DND_USAGE_DND,
                      length=LEN.USAGE,
                      title="Do Not Disturb usage",
                      name='dnd_usage_dnd',
                      checks=(CheckHexList(LEN.USAGE // 8),),
                      default_value=DEFAULT.DND_USAGE_DND),
             BitField(fid=FID.DND_USAGE_MICROPHONE_MUTE,
                      length=LEN.USAGE,
                      title="Do Not Disturb microphone mute usage",
                      name='dnd_usage_microphone_mute',
                      checks=(CheckHexList(LEN.USAGE // 8),),
                      default_value=DEFAULT.DND_USAGE_MICROPHONE_MUTE),
             BitField(fid=FID.DND_INPUT,
                      length=LEN.INPUT_DATA,
                      title="Do Not Disturb input",
                      name='dnd_input',
                      checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                      default_value=DEFAULT.DND_INPUT),
             BitField(fid=FID.RSV_REPORT_COUNT,
                      length=LEN.REPORT_SIZE,
                      title='Reserved Report Count',
                      name='rsv_report_count',
                      checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                      default_value=DEFAULT.RSV_REPORT_COUNT),
             BitField(fid=FID.RSV_REPORT_SIZE,
                      length=LEN.REPORT_SIZE,
                      title='Reserved Report Size',
                      name='rsv_report_size',
                      checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                      default_value=DEFAULT.RSV_REPORT_SIZE),
         )+ \
             GenericDesktopSystemControlDescriptor.FIELDS[
             (GenericDesktopSystemControlDescriptor.FID.PWR_USAGE_PAGE
              - GenericDesktopSystemControlDescriptor.FID.RSV_REPORT_SIZE)
             :]

# end class GenericDesktopSystemControlDescriptorKeyboard


class GenericDesktopCallStateControlKeyDescriptor(ReportDescriptor):
    """
    Define the USB Generic Desktop Call State management Control Key descriptor (version 1.2).

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=kix.ls1za5zevwkl
    """
    BITFIELD_LENGTH = 25  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        CALL_STATE_USAGE_PAGE = 0xB0
        CALL_STATE_USAGE = CALL_STATE_USAGE_PAGE - 1
        CALL_STATE_COLLECTION = CALL_STATE_USAGE - 1
        CALL_STATE_REPORT_ID = CALL_STATE_COLLECTION - 1
        CALL_STATE_REPORT_COUNT = CALL_STATE_REPORT_ID - 1
        CALL_STATE_REPORT_SIZE = CALL_STATE_REPORT_COUNT - 1
        CALL_STATE_LOGICAL_MINIMUM = CALL_STATE_REPORT_SIZE - 1
        CALL_STATE_LOGICAL_MAXIMUM = CALL_STATE_LOGICAL_MINIMUM - 1
        CALL_MUTE_TOGGLE_USAGE = CALL_STATE_LOGICAL_MAXIMUM - 1
        CALL_STATE_DOWN_USAGE = CALL_MUTE_TOGGLE_USAGE - 1
        CALL_STATE_WAKE_UP_USAGE = CALL_STATE_DOWN_USAGE - 1
        CALL_STATE_INPUT = CALL_STATE_WAKE_UP_USAGE - 1
        CALL_STATE_RSV_REPORT_SIZE = CALL_STATE_INPUT - 1
        CALL_STATE_RSV_INPUT = CALL_STATE_RSV_REPORT_SIZE - 1
        CALL_STATE_END_COLLECTION = CALL_STATE_RSV_INPUT - 1
    # end class FID

    LEN = ReportDescriptor.LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        CALL_STATE_REPORT_COUNT = HexList("9501")
        CALL_STATE_REPORT_SIZE = HexList("7501")
        CALL_STATE_LOGICAL_MINIMUM = HexList("1500")
        CALL_STATE_LOGICAL_MAXIMUM = HexList("2501")
        CALL_MUTE_TOGGLE_USAGE = HexList("09E1")
        CALL_STATE_RSV_REPORT_SIZE = HexList("750F")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.CALL_STATE_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Call State Usage Page',
                 name='call_state_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.GENERIC_USAGE_PAGE),
        BitField(fid=FID.CALL_STATE_USAGE,
                 length=LEN.USAGE,
                 title='Call State Usage',
                 name='call_state_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CALL_STATE_USAGE),
        BitField(fid=FID.CALL_STATE_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Call State Collection',
                 name='call_state_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.CALL_STATE_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Call State Report Id',
                 name='call_state_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.CALL_STATE_REPORT_ID),
        BitField(fid=FID.CALL_STATE_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Call State Report Count',
                 name='call_state_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.CALL_STATE_REPORT_COUNT),
        BitField(fid=FID.CALL_STATE_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Call State Report Size',
                 name='call_state_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.CALL_STATE_REPORT_SIZE),
        BitField(fid=FID.CALL_STATE_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Call State Logical Minimum',
                 name='call_state_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.CALL_STATE_LOGICAL_MINIMUM),
        BitField(fid=FID.CALL_STATE_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Call State Logical Maximum',
                 name='call_state_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.CALL_STATE_LOGICAL_MAXIMUM),
        BitField(fid=FID.CALL_MUTE_TOGGLE_USAGE,
                 length=LEN.USAGE,
                 title='Call State Mute Usage',
                 name='call_state_mute_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CALL_MUTE_TOGGLE_USAGE),
        BitField(fid=FID.CALL_STATE_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Call State Input',
                 name='call_state_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_REL),
        BitField(fid=FID.CALL_STATE_RSV_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Call State Reserved Report Size',
                 name='rsv_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.CALL_STATE_RSV_REPORT_SIZE),
        BitField(fid=FID.CALL_STATE_RSV_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Call State Reserved Input',
                 name='rsv_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_CST),
        BitField(fid=FID.CALL_STATE_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Call State End Collection',
                 name='call_state_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class GenericDesktopCallStateControlKeyDescriptor


class KeyboardDeviceDescriptor(ReportDescriptor):
    """
    Define the USB Keyboard interface descriptor.

    Note that the report id field is empty to match the configuration when there is only one report in the interface.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          16
    USAGE               16
    COLLECTION          16
    REPORT_ID            0
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     16
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    INPUT               16
    INPUT               16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     16
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    OUTPUT              16
    REPORT_COUNT        16
    REPORT_SIZE         0
    OUTPUT              16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     0
    LOGICAL_MAXIMUM     24
    USAGE               16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    INPUT               16
    END_COLLECTION       8
    ===========  =========
    """
    BITFIELD_LENGTH = 60  # Bytes

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
        MODIFIER_INPUT_CST = MODIFIER_INPUT_DATA - 1
        LED_REPORT_COUNT = MODIFIER_INPUT_CST - 1
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
        END_COLLECTION = KEY_INPUT - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        KEY_LOGICAL_MAXIMUM = 0x18
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
        LED_REPORT_SIZE = HexList("7501")
        LED_USAGE_MINIMUM = HexList("1901")
        LED_USAGE_MAXIMUM = HexList("2905")
        RSV_REPORT_COUNT = HexList("9503")
        RSV_REPORT_SIZE = HexList("7503")
        KEY_REPORT_COUNT = HexList("9506")
        KEY_REPORT_SIZE = HexList("7508")
        KEY_LOGICAL_MINIMUM = HexList("1500")
        KEY_LOGICAL_MAXIMUM = HexList("26FF00")
        KEY_USAGE_MINIMUM = HexList("1900")
        KEY_USAGE_MAXIMUM = HexList("29FF")
    # end class DEFAULT

    FIELDS = ReportDescriptor.FIELDS + (
        BitField(fid=FID.KEYBOARD_REPORT_ID,
                 length=LEN.EMPTY,
                 title='Keyboard Report Id',
                 name='keyboard_report_id',
                 checks=(CheckHexList(LEN.EMPTY),),
                 default_value=DEFAULT.EMPTY_REPORT_ID),
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
        BitField(fid=FID.MODIFIER_INPUT_CST,
                 length=LEN.INPUT_DATA,
                 title='Modifier Input Constant',
                 name='modifier_input_cst',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_CST),
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
                 default_value=DEFAULT.LED_REPORT_SIZE),
        BitField(fid=FID.LED_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='LED Logical Minimum',
                 name='led_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.MODIFIER_LOGICAL_MINIMUM),
        BitField(fid=FID.LED_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='LED Logical Maximum',
                 name='led_logical_maximum',
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
                 length=LEN.USAGE_MAXIMUM,
                 title='Key Usage Maximum',
                 name='key_usage_maximum',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.KEY_USAGE_MAXIMUM),
        BitField(fid=FID.KEY_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Key Input',
                 name='key_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='End Collection',
                 name='end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class KeyboardDeviceDescriptor


class KeyboardReceiverDescriptor(ReportDescriptor):
    """
    Define the USB Keyboard interface descriptor.

    Note that the report id field is empty to match the configuration when there is only one report in the interface.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          16
    USAGE               16
    COLLECTION          16
    REPORT_ID            0
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     16
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    INPUT               16
    INPUT               16
    REPORT_COUNT        16
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    OUTPUT              16
    REPORT_COUNT        16
    REPORT_SIZE         16
    OUTPUT              16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     24
    USAGE               16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       24
    INPUT               16
    END_COLLECTION       8
    ===========  =========
    """
    BITFIELD_LENGTH = 59  # Bytes

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
        MODIFIER_INPUT_CST = MODIFIER_INPUT_DATA - 1
        LED_REPORT_COUNT = MODIFIER_INPUT_CST - 1
        LED_USAGE_PAGE = LED_REPORT_COUNT - 1
        LED_USAGE_MINIMUM = LED_USAGE_PAGE - 1
        LED_USAGE_MAXIMUM = LED_USAGE_MINIMUM - 1
        LED_OUTPUT = LED_USAGE_MAXIMUM - 1
        RSV_REPORT_COUNT = LED_OUTPUT - 1
        RSV_REPORT_SIZE = RSV_REPORT_COUNT - 1
        RSV_OUTPUT = RSV_REPORT_SIZE - 1
        KEY_REPORT_COUNT = RSV_OUTPUT - 1
        KEY_REPORT_SIZE = KEY_REPORT_COUNT - 1
        KEY_LOGICAL_MINIMUM = KEY_REPORT_SIZE - 1
        KEY_LOGICAL_MAXIMUM = KEY_LOGICAL_MINIMUM - 1
        KEY_USAGE_PAGE = KEY_LOGICAL_MAXIMUM - 1
        KEY_USAGE_MINIMUM = KEY_USAGE_PAGE - 1
        KEY_USAGE_MAXIMUM = KEY_USAGE_MINIMUM - 1
        KEY_INPUT = KEY_USAGE_MAXIMUM - 1
        END_COLLECTION = KEY_INPUT - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        KEY_LOGICAL_MAXIMUM = 0x18
        KEY_USAGE_MAXIMUM = 0x18
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
        RSV_REPORT_COUNT = HexList("9501")
        RSV_REPORT_SIZE = HexList("7503")
        KEY_REPORT_COUNT = HexList("9506")
        KEY_REPORT_SIZE = HexList("7508")
        KEY_LOGICAL_MINIMUM = HexList("1500")
        KEY_LOGICAL_MAXIMUM = HexList("26FF00")
        KEY_USAGE_MINIMUM = HexList("1900")
        KEY_USAGE_MAXIMUM = HexList("2AFF00")
    # end class DEFAULT

    FIELDS = ReportDescriptor.FIELDS + (
        BitField(fid=FID.KEYBOARD_REPORT_ID,
                 length=LEN.EMPTY,
                 title='Keyboard Report Id',
                 name='keyboard_report_id',
                 checks=(CheckHexList(LEN.EMPTY),),
                 default_value=DEFAULT.EMPTY_REPORT_ID),
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
        BitField(fid=FID.MODIFIER_INPUT_CST,
                 length=LEN.INPUT_DATA,
                 title='Modifier Input Constant',
                 name='modifier_input_cst',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_CST),
        BitField(fid=FID.LED_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='LED Report Count',
                 name='led_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.LED_REPORT_COUNT),
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
        BitField(fid=FID.RSV_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Reserved Report Size',
                 name='rsv_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.RSV_REPORT_SIZE),
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
        BitField(fid=FID.KEY_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Key LOGICAL Minimum',
                 name='key_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.KEY_LOGICAL_MINIMUM),
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
        BitField(fid=FID.END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='End Collection',
                 name='end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class KeyboardReceiverDescriptor


class TopRawKeyDescriptor(ReportDescriptor):
    """
    Define the Top Raw logical collection.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.8ahvvyb76ay
    """
    BITFIELD_LENGTH = 29  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        TOP_RAW_LIST_USAGE = 0xFF
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
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        TOP_RAW_LOGICAL_MINIMUM = 0x28
        TOP_RAW_LOGICAL_MAXIMUM = 0x28
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        TOP_RAW_REPORT_COUNT = HexList("9500")
        TOP_RAW_REPORT_SIZE = HexList("7520")
        TOP_RAW_LOGICAL_MINIMUM = HexList("1700000080")
        TOP_RAW_LOGICAL_MAXIMUM = HexList("27FFFFFF7F")
        TOP_RAW_USAGE_PAGE = HexList("050A")
        TOP_RAW_USAGE_MINIMUM = HexList("1901")
        TOP_RAW_USAGE_MAXIMUM = HexList("2900")
        TOP_RAW_FEATURE = HexList("B103")
    # end class DEFAULT

    FIELDS = (
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
    )

    def __init__(self, cnt3=0, *args, **kwargs):
        """
        :param cnt3: Number of usages in the Top Row - OPTIONAL
        :type cnt3: ``int``
        :param args: Positional arguments
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(*args, **kwargs)

        self.top_raw_report_count = HexList(
            Numeral(self.DEFAULT.TOP_RAW_REPORT_COUNT, self.LEN.REPORT_COUNT // 8) + cnt3)
        self.top_raw_usage_maximum = HexList(
            Numeral(self.DEFAULT.TOP_RAW_USAGE_MAXIMUM, self.LEN.USAGE_MAXIMUM // 8) + cnt3)
    # end def __init__

    def update_usage_count(self, cnt3=0):
        """
        Update the number of usages in the Top Row descriptor

        :param cnt3: Number of usages in the Top Row - OPTIONAL
        :type cnt3: ``int``
        """
        self.top_raw_report_count = HexList(
            Numeral(self.DEFAULT.TOP_RAW_REPORT_COUNT, self.LEN.REPORT_COUNT // 8) + cnt3)
        self.top_raw_usage_maximum = HexList(
            Numeral(self.DEFAULT.TOP_RAW_USAGE_MAXIMUM, self.LEN.USAGE_MAXIMUM // 8) + cnt3)
    # end def update_usage_count
# end class TopRawKeyDescriptor


class KeyboardInterfaceDescriptor(KeyboardReceiverDescriptor):
    """
    Concatenate the Keyboard, MultiMedia and Power Key descriptors.

    Note that the report id field is filled to match the configuration when there is multiple reports in the interface.
    """
    FID = KeyboardReceiverDescriptor.FID

    BITFIELD_LENGTH = (KeyboardReceiverDescriptor.BITFIELD_LENGTH + 2 + ConsumerGenericKeyDescriptor.BITFIELD_LENGTH +
                       GenericDesktopSystemControlKeyDescriptor.BITFIELD_LENGTH)

    FIELDS = \
        KeyboardReceiverDescriptor.FIELDS[:FID.USAGE_PAGE - FID.KEYBOARD_REPORT_ID] + (
            BitField(fid=FID.KEYBOARD_REPORT_ID,
                     length=KeyboardReceiverDescriptor.LEN.REPORT_ID,
                     title='Keyboard Report Id',
                     name='keyboard_report_id',
                     checks=(CheckHexList(KeyboardReceiverDescriptor.LEN.REPORT_ID // 8),),
                     default_value=KeyboardReceiverDescriptor.DEFAULT.KEYBOARD_REPORT_ID), ) + \
        KeyboardReceiverDescriptor.FIELDS[FID.USAGE_PAGE - FID.MODIFIER_REPORT_COUNT:] + \
        ConsumerGenericKeyDescriptor.FIELDS + \
        GenericDesktopSystemControlKeyDescriptor.FIELDS
# end class KeyboardInterfaceDescriptor


class KeyboardBitmapKeyDescriptor(ReportDescriptor):
    """
    Define the USB Keyboard interface descriptor.

    Note that the report id field is empty to match the configuration when there is only one report in the interface.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          16
    USAGE               16
    COLLECTION          16
    REPORT_ID            0
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     16
    REPORT_SIZE         16
    REPORT_COUNT        16
    INPUT_DATA          16
    REPORT_COUNT        16
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    OUTPUT              16
    REPORT_COUNT        16
    REPORT_SIZE         16
    OUTPUT              16
    REPORT_COUNT        16
    REPORT_SIZE         16
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    INPUT               16
    REPORT_COUNT        16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    INPUT               16
    REPORT_COUNT        16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       24
    INPUT               16
    END_COLLECTION       8
    ===========  =========
    """
    BITFIELD_LENGTH = 67  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        KEYBOARD_REPORT_ID = ReportDescriptor.FID.APP_COLLECTION - 1
        KEYBOARD_USAGE_PAGE = KEYBOARD_REPORT_ID - 1
        MODIFIER_USAGE_MINIMUM = KEYBOARD_USAGE_PAGE - 1
        MODIFIER_USAGE_MAXIMUM = MODIFIER_USAGE_MINIMUM - 1
        MODIFIER_LOGICAL_MINIMUM = MODIFIER_USAGE_MAXIMUM - 1
        MODIFIER_LOGICAL_MAXIMUM = MODIFIER_LOGICAL_MINIMUM - 1
        MODIFIER_REPORT_SIZE = MODIFIER_LOGICAL_MAXIMUM - 1
        MODIFIER_REPORT_COUNT = MODIFIER_REPORT_SIZE - 1
        MODIFIER_INPUT_DATA = MODIFIER_REPORT_COUNT - 1
        LED_REPORT_COUNT = MODIFIER_INPUT_DATA - 1
        LED_USAGE_PAGE = LED_REPORT_COUNT - 1
        LED_USAGE_MINIMUM = LED_USAGE_PAGE - 1
        LED_USAGE_MAXIMUM = LED_USAGE_MINIMUM - 1
        LED_OUTPUT = LED_USAGE_MAXIMUM - 1
        RSV_REPORT_COUNT = LED_OUTPUT - 1
        RSV_REPORT_SIZE = RSV_REPORT_COUNT - 1
        RSV_OUTPUT = RSV_REPORT_SIZE - 1
        KEY_REPORT_COUNT = RSV_OUTPUT - 1
        KEY_REPORT_SIZE = KEY_REPORT_COUNT - 1
        KEY_USAGE_PAGE = KEY_REPORT_SIZE - 1
        KEY_USAGE_MINIMUM = KEY_USAGE_PAGE - 1
        KEY_USAGE_MAXIMUM = KEY_USAGE_MINIMUM - 1
        KEY_INPUT = KEY_USAGE_MAXIMUM - 1
        LANG_JP_REPORT_COUNT = KEY_INPUT - 1
        LANG_JP_USAGE_MINIMUM = LANG_JP_REPORT_COUNT - 1
        LANG_JP_USAGE_MAXIMUM = LANG_JP_USAGE_MINIMUM - 1
        LANG_JP_INPUT = LANG_JP_USAGE_MAXIMUM - 1
        LANG_KR_REPORT_COUNT = LANG_JP_INPUT - 1
        LANG_KR_USAGE_MINIMUM = LANG_KR_REPORT_COUNT - 1
        LANG_KR_USAGE_MAXIMUM = LANG_KR_USAGE_MINIMUM - 1
        LANG_KR_INPUT = LANG_KR_USAGE_MAXIMUM - 1
        END_COLLECTION = LANG_KR_INPUT - 1
    # end class FID

    LEN = ReportDescriptor.LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        MODIFIER_USAGE_MINIMUM = HexList("19E0")
        MODIFIER_USAGE_MAXIMUM = HexList("29E7")
        MODIFIER_LOGICAL_MINIMUM = HexList("1500")
        MODIFIER_LOGICAL_MAXIMUM = HexList("2501")
        MODIFIER_REPORT_SIZE = HexList("7501")
        MODIFIER_REPORT_COUNT = HexList("9508")
        LED_REPORT_COUNT = HexList("9505")
        LED_USAGE_MINIMUM = HexList("1901")
        LED_USAGE_MAXIMUM = HexList("2905")
        RSV_REPORT_COUNT = HexList("9501")
        RSV_REPORT_SIZE = HexList("7503")
        KEY_REPORT_COUNT = HexList("9570")
        KEY_REPORT_SIZE = HexList("7501")
        KEY_USAGE_MINIMUM = HexList("1904")
        KEY_USAGE_MAXIMUM = HexList("2973")
        LANG_JP_REPORT_COUNT = HexList("9505")
        LANG_JP_USAGE_MINIMUM = HexList("1987")
        LANG_JP_USAGE_MAXIMUM = HexList("298B")
        LANG_KR_REPORT_COUNT = HexList("9503")
        LANG_KR_USAGE_MINIMUM = HexList("1990")
        LANG_KR_USAGE_MAXIMUM = HexList("2992")
    # end class DEFAULT

    FIELDS = ReportDescriptor.FIELDS + (
        BitField(fid=FID.KEYBOARD_REPORT_ID,
                 length=LEN.EMPTY,
                 title='Keyboard Report Id',
                 name='keyboard_report_id',
                 checks=(CheckHexList(LEN.EMPTY),),
                 default_value=DEFAULT.EMPTY_REPORT_ID),
        BitField(fid=FID.KEYBOARD_USAGE_PAGE,
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
        BitField(fid=FID.MODIFIER_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Modifier Report Size',
                 name='modifier_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.MODIFIER_REPORT_SIZE),
        BitField(fid=FID.MODIFIER_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Modifier Report Count',
                 name='modifier_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.MODIFIER_REPORT_COUNT),
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
        BitField(fid=FID.RSV_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Reserved Report Size',
                 name='rsv_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.RSV_REPORT_SIZE),
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
                 length=LEN.USAGE_MAXIMUM,
                 title='Key Usage Maximum',
                 name='key_usage_maximum',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.KEY_USAGE_MAXIMUM),
        BitField(fid=FID.KEY_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Key Input',
                 name='key_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.LANG_JP_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Language (JP) Report Count',
                 name='lang_jp_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.LANG_JP_REPORT_COUNT),
        BitField(fid=FID.LANG_JP_USAGE_MINIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='Language (JP) Usage Minimum',
                 name='lang_jp_usage_minimum',
                 checks=(CheckHexList(LEN.USAGE_MINIMUM // 8),),
                 default_value=DEFAULT.LANG_JP_USAGE_MINIMUM),
        BitField(fid=FID.LANG_JP_USAGE_MAXIMUM,
                 length=LEN.USAGE_MAXIMUM,
                 title='Language (JP) Usage Maximum',
                 name='lang_jp_usage_maximum',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.LANG_JP_USAGE_MAXIMUM),
        BitField(fid=FID.LANG_JP_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Language (JP) Input',
                 name='lang_jp_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.LANG_KR_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Language (KR) Input',
                 name='lang_kr_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.LANG_KR_REPORT_COUNT),
        BitField(fid=FID.LANG_KR_USAGE_MINIMUM,
                 length=LEN.USAGE_MINIMUM,
                 title='Language (KR) Usage Minimum',
                 name='lang_kr_usage_minimum',
                 checks=(CheckHexList(LEN.USAGE_MINIMUM // 8),),
                 default_value=DEFAULT.LANG_KR_USAGE_MINIMUM),
        BitField(fid=FID.LANG_KR_USAGE_MAXIMUM,
                 length=LEN.USAGE_MAXIMUM,
                 title='Language (KR) Usage Maximum',
                 name='lang_kr_usage_maximum',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.LANG_KR_USAGE_MAXIMUM),
        BitField(fid=FID.LANG_KR_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Language (KR) Input',
                 name='lang_kr_input',
                 checks=(CheckHexList(LEN.USAGE_MAXIMUM // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='End Collection',
                 name='end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class KeyboardBitmapKeyDescriptor


class KeyboardBitmapInterfaceDescriptor(KeyboardBitmapKeyDescriptor):
    """
    Concatenate the Keyboard, MultiMedia and Power Key descriptors.

    Note that the report id field is filled to match the configuration when there is multiple reports in the interface.
    """

    FID = KeyboardBitmapKeyDescriptor.FID

    BITFIELD_LENGTH = (KeyboardBitmapKeyDescriptor.BITFIELD_LENGTH + 2 + ConsumerGenericKeyDescriptor.BITFIELD_LENGTH +
                       GenericDesktopSystemControlKeyDescriptor.BITFIELD_LENGTH)

    FIELDS = \
        KeyboardBitmapKeyDescriptor.FIELDS[:FID.USAGE_PAGE - FID.KEYBOARD_REPORT_ID] + (
            BitField(fid=FID.KEYBOARD_REPORT_ID,
                     length=KeyboardBitmapKeyDescriptor.LEN.REPORT_ID,
                     title='Keyboard Report Id',
                     name='keyboard_report_id',
                     checks=(CheckHexList(KeyboardBitmapKeyDescriptor.LEN.REPORT_ID // 8),),
                     default_value=KeyboardBitmapKeyDescriptor.DEFAULT.KEYBOARD_REPORT_ID), ) + \
        KeyboardBitmapKeyDescriptor.FIELDS[FID.USAGE_PAGE - FID.KEYBOARD_USAGE_PAGE:] + \
        ConsumerGenericKeyDescriptor.FIELDS + \
        GenericDesktopSystemControlKeyDescriptor.FIELDS
# end class KeyboardBitmapInterfaceDescriptor


class KeyboardBitmapReceiverDescriptor(KeyboardBitmapKeyDescriptor):
    """
    Concatenate the Keyboard, MultiMedia and Power Key descriptors.

    Note that the report id field is filled to match the configuration when there is multiple reports in the interface.
    """

    FID = KeyboardBitmapKeyDescriptor.FID

    BITFIELD_LENGTH = (KeyboardBitmapKeyDescriptor.BITFIELD_LENGTH + 2 + ConsumerGenericKeyDescriptor.BITFIELD_LENGTH +
                       GenericDesktopSystemControlDescriptor.BITFIELD_LENGTH)

    FIELDS = \
        KeyboardBitmapKeyDescriptor.FIELDS[:FID.USAGE_PAGE - FID.KEYBOARD_REPORT_ID] + (
            BitField(fid=FID.KEYBOARD_REPORT_ID,
                     length=KeyboardBitmapKeyDescriptor.LEN.REPORT_ID,
                     title='Keyboard Report Id',
                     name='keyboard_report_id',
                     checks=(CheckHexList(KeyboardBitmapKeyDescriptor.LEN.REPORT_ID // 8),),
                     default_value=KeyboardBitmapKeyDescriptor.DEFAULT.KEYBOARD_REPORT_ID), ) + \
        KeyboardBitmapKeyDescriptor.FIELDS[FID.USAGE_PAGE - FID.KEYBOARD_USAGE_PAGE:] + \
        ConsumerGenericKeyDescriptor.FIELDS + \
        GenericDesktopSystemControlDescriptor.FIELDS
# end class KeyboardBitmapReceiverDescriptor


class MouseCommonDescriptor(ReportDescriptor):
    """
    Define the Mouse key descriptor part which is common between Core and Gaming implementation .

    Note that the report id field is empty to match the configuration when there is only one report in the interface.
    """
    BITFIELD_LENGTH = 64  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        MOUSE_REPORT_ID = ReportDescriptor.FID.APP_COLLECTION - 1
        POINTER_USAGE = MOUSE_REPORT_ID - 1
        LINKED_COLLECTION = POINTER_USAGE - 1
        BUTTON_REPORT_COUNT = LINKED_COLLECTION - 1
        BUTTON_REPORT_SIZE = BUTTON_REPORT_COUNT - 1
        BUTTON_LOGICAL_MINIMUM = BUTTON_REPORT_SIZE - 1
        BUTTON_LOGICAL_MAXIMUM = BUTTON_LOGICAL_MINIMUM - 1
        BUTTON_USAGE_PAGE = BUTTON_LOGICAL_MAXIMUM - 1
        BUTTON_USAGE_MINIMUM = BUTTON_USAGE_PAGE - 1
        BUTTON_USAGE_MAXIMUM = BUTTON_USAGE_MINIMUM - 1
        BUTTON_INPUT_DATA = BUTTON_USAGE_MAXIMUM - 1
        AXIS_REPORT_COUNT = BUTTON_INPUT_DATA - 1
        AXIS_REPORT_SIZE = AXIS_REPORT_COUNT - 1
        AXIS_LOGICAL_MINIMUM = AXIS_REPORT_SIZE - 1
        AXIS_LOGICAL_MAXIMUM = AXIS_LOGICAL_MINIMUM - 1
        AXIS_USAGE_PAGE = AXIS_LOGICAL_MAXIMUM - 1
        AXIS_X_USAGE = AXIS_USAGE_PAGE - 1
        AXIS_Y_USAGE = AXIS_X_USAGE - 1
        AXIS_INPUT = AXIS_Y_USAGE - 1
        WHEEL_REPORT_COUNT = AXIS_INPUT - 1
        WHEEL_REPORT_SIZE = WHEEL_REPORT_COUNT - 1
        WHEEL_LOGICAL_MINIMUM = WHEEL_REPORT_SIZE - 1
        WHEEL_LOGICAL_MAXIMUM = WHEEL_LOGICAL_MINIMUM - 1
        WHEEL_USAGE = WHEEL_LOGICAL_MAXIMUM - 1
        WHEEL_INPUT = WHEEL_USAGE - 1
        ACPAN_REPORT_COUNT = WHEEL_INPUT - 1
        ACPAN_USAGE_PAGE = ACPAN_REPORT_COUNT - 1
        ACPAN_USAGE = ACPAN_USAGE_PAGE - 1
        ACPAN_INPUT = ACPAN_USAGE - 1
        END_LINKED_COLLECTION = ACPAN_INPUT - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        LINKED_COLLECTION = 0x10
        AXIS_LOGICAL_MINIMUM = 0x18
        AXIS_LOGICAL_MAXIMUM = 0x18
        ACPAN_USAGE = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        POINTER_USAGE = HexList("0901")
        LINKED_COLLECTION = HexList("A100")
        BUTTON_REPORT_COUNT = HexList("9510")
        BUTTON_REPORT_SIZE = HexList("7501")
        BUTTON_LOGICAL_MINIMUM = HexList("1500")
        BUTTON_LOGICAL_MAXIMUM = HexList("2501")
        BUTTON_USAGE_MINIMUM = HexList("1901")
        BUTTON_USAGE_MAXIMUM = HexList("2910")
        AXIS_REPORT_COUNT = HexList("9502")
        AXIS_REPORT_SIZE = HexList("7510")
        AXIS_LOGICAL_MINIMUM = HexList("160080")
        AXIS_LOGICAL_MAXIMUM = HexList("26FF7F")
        WHEEL_REPORT_COUNT = HexList("9501")
        WHEEL_REPORT_SIZE = HexList("7508")
        WHEEL_LOGICAL_MINIMUM = HexList("1580")
        WHEEL_LOGICAL_MAXIMUM = HexList("257F")
        ACPAN_USAGE = HexList("0A3802")
    # end class DEFAULT

    FIELDS = ReportDescriptor.FIELDS + (
        BitField(fid=FID.MOUSE_REPORT_ID,
                 length=LEN.EMPTY,
                 title='Mouse Report Id',
                 name='mouse_report_id',
                 checks=(CheckHexList(LEN.EMPTY),),
                 default_value=HexList()),
        BitField(fid=FID.POINTER_USAGE,
                 length=LEN.USAGE,
                 title='Pointer Usage',
                 name='pointer_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.POINTER_USAGE),
        BitField(fid=FID.LINKED_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Linked Collection',
                 name='linked_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.LINKED_COLLECTION),
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
        BitField(fid=FID.AXIS_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Axis Report Count',
                 name='axis_report_count',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.AXIS_REPORT_COUNT),
        BitField(fid=FID.AXIS_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Axis Report Count',
                 name='axis_report_count',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
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
        BitField(fid=FID.AXIS_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Axis Usage Page',
                 name='axis_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.GENERIC_USAGE_PAGE),
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
        BitField(fid=FID.ACPAN_REPORT_COUNT,
                 length=LEN.EMPTY,
                 title='AC Pan Report Count',
                 name='acpan_report_count',
                 checks=(CheckHexList(LEN.EMPTY),),
                 default_value=HexList()),
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
        BitField(fid=FID.END_LINKED_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='End Linked Collection',
                 name='end_linked_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usage = self.DEFAULT.MOUSE_USAGE
    # end def __init__
# end class MouseCommonDescriptor


class MouseKeyDescriptor(MouseCommonDescriptor):
    """
    Define the USB Mouse interface descriptor.

    Note that the report id field is empty to match the configuration when there is only one report in the interface.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          16
    USAGE               16
    COLLECTION          16
    REPORT_ID            0
    USAGE               16
    COLLECTION          16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     16
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    INPUT               16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     24
    LOGICAL_MAXIMUM     24
    USAGE_PAGE          16
    USAGE               16
    USAGE               16
    INPUT               16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     24
    LOGICAL_MAXIMUM     24
    USAGE               16
    INPUT               16
    REPORT_COUNT        16
    USAGE_PAGE          16
    USAGE               24
    INPUT               16
    END_COLLECTION       8
    END_COLLECTION       8
    ===========  =========
    """
    BITFIELD_LENGTH = MouseCommonDescriptor.BITFIELD_LENGTH + 1  # Bytes

    class FID(MouseCommonDescriptor.FID):
        # See ``MouseCommonDescriptor.FID``
        END_COLLECTION = MouseCommonDescriptor.FID.END_LINKED_COLLECTION - 1
    # end class FID

    FIELDS = MouseCommonDescriptor.FIELDS + (
        BitField(fid=FID.END_COLLECTION,
                 length=MouseCommonDescriptor.LEN.END_COLLECTION,
                 title='End Collection',
                 name='end_collection',
                 checks=(CheckHexList(MouseCommonDescriptor.LEN.END_COLLECTION // 8),),
                 default_value=MouseCommonDescriptor.DEFAULT.END_COLLECTION),
    )
# end class MouseKeyDescriptor


class MouseReceiverDescriptor(MouseKeyDescriptor):
    """
    Define the USB Mouse interface descriptor for a BOLT receiver.
    """
    BITFIELD_LENGTH = MouseKeyDescriptor.BITFIELD_LENGTH + 2  # Bytes

    class DEFAULT(MouseKeyDescriptor.DEFAULT):
        # See ``MouseKeyDescriptor.DEFAULT``
        AXIS_LOGICAL_MINIMUM = HexList("160180")
        WHEEL_LOGICAL_MINIMUM = HexList("1581")
        ACPAN_REPORT_COUNT = HexList("9501")
    # end class DEFAULT

    FIELDS = MouseKeyDescriptor.FIELDS[:(MouseKeyDescriptor.FID.USAGE_PAGE -
                                         MouseKeyDescriptor.FID.ACPAN_REPORT_COUNT)] + \
             (
                BitField(fid=MouseKeyDescriptor.FID.ACPAN_REPORT_COUNT,
                         length=MouseKeyDescriptor.LEN.REPORT_COUNT,
                         title='AC Pan Report Count',
                         name='acpan_report_count',
                         checks=(CheckHexList(MouseKeyDescriptor.LEN.REPORT_COUNT // 8),),
                         default_value=DEFAULT.ACPAN_REPORT_COUNT),
                     ) + \
             MouseKeyDescriptor.FIELDS[(MouseKeyDescriptor.FID.USAGE_PAGE -
                                         MouseKeyDescriptor.FID.ACPAN_REPORT_COUNT + 1):]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axis_logical_minimum = self.DEFAULT.AXIS_LOGICAL_MINIMUM
        self.wheel_logical_minimum = self.DEFAULT.WHEEL_LOGICAL_MINIMUM
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        mixin = super().fromHexList(*args, **kwargs)
        mixin.axis_logical_minimum = cls.DEFAULT.AXIS_LOGICAL_MINIMUM
        mixin.wheel_logical_minimum = cls.DEFAULT.WHEEL_LOGICAL_MINIMUM
        return mixin
    # end def fromHexList
# end class MouseReceiverDescriptor


class MouseNvidiaExtensionKeyDescriptor(MouseCommonDescriptor):
    """
    Define the USB Mouse interface descriptor with the Nvidia extension.
     - the Nvidia extension is added (+16 bytes)
     - the end collection field shall be the last item of the descriptor

    Note that the report id field is empty to match the configuration when there is only one report in the interface.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          16
    USAGE               16
    COLLECTION          16
    REPORT_ID            0
    USAGE               16
    COLLECTION          16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     16
    USAGE_PAGE          16
    USAGE_MINIMUM       16
    USAGE_MAXIMUM       16
    INPUT               16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     24
    LOGICAL_MAXIMUM     24
    USAGE_PAGE          16
    USAGE               16
    USAGE               16
    INPUT               16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     24
    LOGICAL_MAXIMUM     24
    USAGE               16
    INPUT               16
    REPORT_COUNT        16
    USAGE_PAGE          16
    USAGE               24
    INPUT               16
    END_COLLECTION       8
    USAGE_PAGE          24
    USAGE               16
    REPORT_SIZE         16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     24
    INPUT               16
    END_COLLECTION       8
    ===========  =========
    """
    BITFIELD_LENGTH = MouseCommonDescriptor.BITFIELD_LENGTH + 17  # Bytes

    class FID(MouseCommonDescriptor.FID):
        # See ``MouseCommonDescriptor.FID``
        NV_EXT_USAGE_PAGE = MouseCommonDescriptor.FID.END_LINKED_COLLECTION - 1
        NV_EXT_USAGE = NV_EXT_USAGE_PAGE - 1
        NV_EXT_REPORT_SIZE = NV_EXT_USAGE - 1
        NV_EXT_REPORT_COUNT = NV_EXT_REPORT_SIZE - 1
        NV_EXT_LOGICAL_MINIMUM = NV_EXT_REPORT_COUNT - 1
        NV_EXT_LOGICAL_MAXIMUM = NV_EXT_LOGICAL_MINIMUM - 1
        NV_EXT_INPUT_DATA = NV_EXT_LOGICAL_MAXIMUM - 1
        END_COLLECTION = NV_EXT_INPUT_DATA - 1
    # end class FID

    class LEN(MouseCommonDescriptor.LEN):
        # See ``MouseCommonDescriptor.LEN``
        NV_EXT_USAGE_PAGE = 0x18
        NV_EXT_LOGICAL_MAXIMUM = 0x18
    # end class LEN

    class DEFAULT(MouseCommonDescriptor.DEFAULT):
        # See ``MouseCommonDescriptor.DEFAULT``
        NV_EXT_USAGE_PAGE = HexList("0600FF")
        NV_EXT_USAGE = HexList("09F1")
        NV_EXT_REPORT_SIZE = HexList("7508")
        NV_EXT_REPORT_COUNT = HexList("9505")
        NV_EXT_LOGICAL_MINIMUM = HexList("1500")
        NV_EXT_LOGICAL_MAXIMUM = HexList("26FF00")
    # end class DEFAULT

    FIELDS = MouseCommonDescriptor.FIELDS + (
        BitField(fid=FID.NV_EXT_USAGE_PAGE,
                 length=LEN.NV_EXT_USAGE_PAGE,
                 title='Nvidia Extension UsagePage',
                 name='nv_ext_usage_page',
                 checks=(CheckHexList(LEN.NV_EXT_USAGE_PAGE // 8),),
                 default_value=DEFAULT.NV_EXT_USAGE_PAGE),
        BitField(fid=FID.NV_EXT_USAGE,
                 length=LEN.USAGE,
                 title='Nvidia Extension Usage',
                 name='nv_ext_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.NV_EXT_USAGE),
        BitField(fid=FID.NV_EXT_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Nvidia Extension Report Size',
                 name='nv_ext_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.NV_EXT_REPORT_SIZE),
        BitField(fid=FID.NV_EXT_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Nvidia Extension Report Count',
                 name='nv_ext_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.NV_EXT_REPORT_COUNT),
        BitField(fid=FID.NV_EXT_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Nvidia Extension Logical Minimum',
                 name='nv_ext_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.NV_EXT_LOGICAL_MINIMUM),
        BitField(fid=FID.NV_EXT_LOGICAL_MAXIMUM,
                 length=LEN.NV_EXT_LOGICAL_MAXIMUM,
                 title='Nvidia Extension Logical Maximum',
                 name='nv_ext_logical_maximum',
                 checks=(CheckHexList(LEN.NV_EXT_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.NV_EXT_LOGICAL_MAXIMUM),
        BitField(fid=FID.NV_EXT_INPUT_DATA,
                 length=LEN.INPUT_DATA,
                 title='Nvidia Extension Input',
                 name='nv_ext_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.END_COLLECTION,
                 length=MouseCommonDescriptor.LEN.END_COLLECTION,
                 title='End Collection',
                 name='end_collection',
                 checks=(CheckHexList(MouseCommonDescriptor.LEN.END_COLLECTION // 8),),
                 default_value=MouseCommonDescriptor.DEFAULT.END_COLLECTION),
    )
# end class MouseNvidiaExtensionKeyDescriptor


class MouseReceiverNvidiaExtensionKeyDescriptor(MouseNvidiaExtensionKeyDescriptor):
    """
    Define the USB Mouse interface descriptor for a receiver with the Nvidia extension, e.g. Savituck.
    See V1.2 of FW HID descriptors and reports overview
    (https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/view)
    """
    BITFIELD_LENGTH = MouseNvidiaExtensionKeyDescriptor.BITFIELD_LENGTH + 2  # Bytes

    class DEFAULT(MouseNvidiaExtensionKeyDescriptor.DEFAULT):
        # See ``MouseKeyDescriptor.DEFAULT``
        AXIS_LOGICAL_MINIMUM = HexList("160180")
        WHEEL_LOGICAL_MINIMUM = HexList("1581")
        ACPAN_REPORT_COUNT = HexList("9501")
    # end class DEFAULT

    FIELDS = MouseNvidiaExtensionKeyDescriptor.FIELDS[:(MouseNvidiaExtensionKeyDescriptor.FID.USAGE_PAGE -
                                                        MouseNvidiaExtensionKeyDescriptor.FID.ACPAN_REPORT_COUNT)] + \
             (
                 BitField(fid=MouseNvidiaExtensionKeyDescriptor.FID.ACPAN_REPORT_COUNT,
                          length=MouseNvidiaExtensionKeyDescriptor.LEN.REPORT_COUNT,
                          title='AC Pan Report Count',
                          name='acpan_report_count',
                          checks=(CheckHexList(MouseNvidiaExtensionKeyDescriptor.LEN.REPORT_COUNT // 8),),
                          default_value=DEFAULT.ACPAN_REPORT_COUNT),
             ) + \
             MouseNvidiaExtensionKeyDescriptor.FIELDS[(MouseNvidiaExtensionKeyDescriptor.FID.USAGE_PAGE -
                                                       MouseNvidiaExtensionKeyDescriptor.FID.ACPAN_REPORT_COUNT + 1):]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axis_logical_minimum = self.DEFAULT.AXIS_LOGICAL_MINIMUM
        self.wheel_logical_minimum = self.DEFAULT.WHEEL_LOGICAL_MINIMUM
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        mixin = super().fromHexList(*args, **kwargs)
        mixin.axis_logical_minimum = cls.DEFAULT.AXIS_LOGICAL_MINIMUM
        mixin.wheel_logical_minimum = cls.DEFAULT.WHEEL_LOGICAL_MINIMUM
        return mixin
    # end def fromHexList
# end class MouseReceiverNvidiaExtensionKeyDescriptor


class MouseInterfaceDescriptor(MouseKeyDescriptor):
    """
    Concatenate the Mouse, MultiMedia and Power Key descriptors.

    Note that the report id field is filled to match the configuration when there is multiple reports in the interface.
    """
    # 133 Bytes
    BITFIELD_LENGTH = (MouseKeyDescriptor.BITFIELD_LENGTH + 2 + ConsumerGenericKeyDescriptor.BITFIELD_LENGTH +
                       GenericDesktopSystemControlKeyboardV14Descriptor.BITFIELD_LENGTH)

    class FID(MouseKeyDescriptor.FID):
        # See ``MouseKeyDescriptor.FID``
        CONSUMER_GENERIC_DATA = MouseKeyDescriptor.FID.END_COLLECTION - 1
        SYSTEM_CONTROL_DATA = CONSUMER_GENERIC_DATA - 1
    # end class FID

    class LEN(MouseKeyDescriptor.LEN):
        # See ``MouseKeyDescriptor.LEN``
        CONSUMER_GENERIC_DATA = ConsumerGenericKeyDescriptor.BITFIELD_LENGTH * 8
        SYSTEM_CONTROL_DATA = GenericDesktopSystemControlKeyboardV14Descriptor.BITFIELD_LENGTH * 8
    # end class LEN

    FIELDS = \
        MouseKeyDescriptor.FIELDS[:FID.USAGE_PAGE - FID.MOUSE_REPORT_ID] + (
            BitField(fid=FID.MOUSE_REPORT_ID,
                     length=MouseKeyDescriptor.LEN.REPORT_ID,
                     title='Mouse Report Id',
                     name='mouse_report_id',
                     checks=(CheckHexList(MouseKeyDescriptor.LEN.REPORT_ID // 8),),
                     default_value=MouseKeyDescriptor.DEFAULT.MOUSE_REPORT_ID), ) + \
        MouseKeyDescriptor.FIELDS[FID.USAGE_PAGE - FID.POINTER_USAGE:] + (
                BitField(fid=FID.CONSUMER_GENERIC_DATA,
                         length=LEN.CONSUMER_GENERIC_DATA,
                         title='Consumer Generic Data',
                         name='consumer_generic_data',
                         checks=(CheckHexList(LEN.CONSUMER_GENERIC_DATA // 8),),),
                BitField(fid=FID.SYSTEM_CONTROL_DATA,
                         length=LEN.SYSTEM_CONTROL_DATA,
                         title='System Control Data',
                         name='system_control_data',
                         checks=(CheckHexList(LEN.SYSTEM_CONTROL_DATA // 8),),),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer_generic_data = ConsumerGenericKeyDescriptor()
        self.system_control_data = GenericDesktopSystemControlKeyboardV14Descriptor()
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        mixin = super().fromHexList(*args, **kwargs)
        mixin.consumer_generic_data = ConsumerGenericKeyDescriptor.fromHexList(mixin.consumer_generic_data)
        mixin.system_control_data = GenericDesktopSystemControlKeyboardV14Descriptor.fromHexList(mixin.system_control_data)
        return mixin
    # end def fromHexList
# end class MouseInterfaceDescriptor


class MouseReceiverInterfaceDescriptor(MouseReceiverDescriptor):
    """
    Concatenate the mouse 16 bits, generic desktop system control and Power Key descriptors.
    """
    #  Bytes
    BITFIELD_LENGTH = (MouseReceiverDescriptor.BITFIELD_LENGTH + 2 +
                       ConsumerGenericKeyDescriptor.BITFIELD_LENGTH +
                       GenericDesktopSystemControlKeyDescriptor.BITFIELD_LENGTH +
                       GenericDesktopCallStateControlKeyDescriptor.BITFIELD_LENGTH)

    class FID(MouseReceiverDescriptor.FID):
        # See ``MouseKeyDescriptor.FID``
        CONSUMER_GENERIC_DATA = MouseReceiverDescriptor.FID.END_COLLECTION - 1
        SYSTEM_CONTROL_DATA = CONSUMER_GENERIC_DATA - 1
        CALL_STATE_DATA = SYSTEM_CONTROL_DATA - 1
    # end class FID

    class LEN(MouseReceiverDescriptor.LEN):
        # See ``MouseKeyDescriptor.LEN``
        CONSUMER_GENERIC_DATA = ConsumerGenericKeyDescriptor.BITFIELD_LENGTH * 8
        SYSTEM_CONTROL_DATA = GenericDesktopSystemControlKeyDescriptor.BITFIELD_LENGTH * 8
        CALL_STATE_DATA = GenericDesktopCallStateControlKeyDescriptor.BITFIELD_LENGTH * 8
    # end class LEN

    FIELDS = \
        MouseReceiverDescriptor.FIELDS[:FID.USAGE_PAGE - FID.MOUSE_REPORT_ID] + (
            BitField(fid=FID.MOUSE_REPORT_ID,
                     length=MouseReceiverDescriptor.LEN.REPORT_ID,
                     title='Mouse Report Id',
                     name='mouse_report_id',
                     checks=(CheckHexList(MouseReceiverDescriptor.LEN.REPORT_ID // 8),),
                     default_value=MouseKeyDescriptor.DEFAULT.MOUSE_REPORT_ID), ) + \
        MouseReceiverDescriptor.FIELDS[FID.USAGE_PAGE - FID.POINTER_USAGE:] + (
                BitField(fid=FID.CONSUMER_GENERIC_DATA,
                         length=LEN.CONSUMER_GENERIC_DATA,
                         title='Consumer Generic Data',
                         name='consumer_generic_data',
                         checks=(CheckHexList(LEN.CONSUMER_GENERIC_DATA // 8),),),
                BitField(fid=FID.SYSTEM_CONTROL_DATA,
                         length=LEN.SYSTEM_CONTROL_DATA,
                         title='System Control Data',
                         name='system_control_data',
                         checks=(CheckHexList(LEN.SYSTEM_CONTROL_DATA // 8),),),
                BitField(fid=FID.CALL_STATE_DATA,
                         length=LEN.CALL_STATE_DATA,
                         title='Call State Data',
                         name='call_state_data',
                         checks=(CheckHexList(LEN.CALL_STATE_DATA // 8),),),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer_generic_data = ConsumerGenericKeyDescriptor()
        self.system_control_data = GenericDesktopSystemControlKeyDescriptor()
        self.call_state_data = GenericDesktopCallStateControlKeyDescriptor()
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        mixin = super().fromHexList(*args, **kwargs)
        mixin.consumer_generic_data = ConsumerGenericKeyDescriptor.fromHexList(mixin.consumer_generic_data)
        mixin.system_control_data = GenericDesktopSystemControlKeyDescriptor.fromHexList(mixin.system_control_data)
        mixin.call_state_data = GenericDesktopCallStateControlKeyDescriptor.fromHexList(mixin.call_state_data)
        return mixin
    # end def fromHexList
# end class MouseReceiverInterfaceDescriptor


class HIDppMessageDescriptor(ReportDescriptor):
    """
    Define the generic HID++ messages descriptor.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          24
    USAGE               16
    COLLECTION          16
    REPORT_ID           16
    REPORT_COUNT        16
    REPORT_SIZE         16
    LOGICAL_MINIMUM     16
    LOGICAL_MAXIMUM     24
    USAGE               16
    INPUT               16
    USAGE               16
    OUTPUT              16
    END_COLLECTION       8
    ===========  =========
    """

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        HIDPP_USAGE_PAGE = 0x18
        HIDPP_LOGICAL_MAXIMUM = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        HIDPP_REPORT_SIZE = HexList("7508")
        HIDPP_LOGICAL_MINIMUM = HexList("1500")
        HIDPP_LOGICAL_MAXIMUM = HexList("26FF00")
    # end class DEFAULT
# end class HIDppMessageDescriptor


class HIDppShortMessageDescriptor(HIDppMessageDescriptor):
    """
    Define the HID++ short-messages descriptor.
    """
    BITFIELD_LENGTH = 28  # Bytes

    class FID(HIDppMessageDescriptor.FID):
        # See ``HIDppMessageDescriptor.FID``
        HIDPP7_USAGE_PAGE = 0xFF
        HIDPP7_USAGE = HIDPP7_USAGE_PAGE - 1
        HIDPP7_APP_COLLECTION = HIDPP7_USAGE - 1
        HIDPP7_REPORT_ID = HIDPP7_APP_COLLECTION - 1
        HIDPP7_REPORT_COUNT = HIDPP7_REPORT_ID - 1
        HIDPP7_REPORT_SIZE = HIDPP7_REPORT_COUNT - 1
        HIDPP7_LOGICAL_MINIMUM = HIDPP7_REPORT_SIZE - 1
        HIDPP7_LOGICAL_MAXIMUM = HIDPP7_LOGICAL_MINIMUM - 1
        HIDPP7_INPUT_USAGE = HIDPP7_LOGICAL_MAXIMUM - 1
        HIDPP7_INPUT_DATA = HIDPP7_INPUT_USAGE - 1
        HIDPP7_OUTPUT_USAGE = HIDPP7_INPUT_DATA - 1
        HIDPP7_OUTPUT_DATA = HIDPP7_OUTPUT_USAGE - 1
        HIDPP7_END_COLLECTION = HIDPP7_OUTPUT_DATA - 1
    # end class FID

    LEN = HIDppMessageDescriptor.LEN

    class DEFAULT(HIDppMessageDescriptor.DEFAULT):
        # See ``HIDppMessageDescriptor.DEFAULT``
        HIDPP7_REPORT_COUNT = HexList("9506")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.HIDPP7_USAGE_PAGE,
                 length=LEN.HIDPP_USAGE_PAGE,
                 title='HIDPP7 UsagePage',
                 name='hidpp7_usage_page',
                 checks=(CheckHexList(LEN.HIDPP_USAGE_PAGE // 8),),
                 default_value=DEFAULT.HIDPP_USAGE_PAGE),
        BitField(fid=FID.HIDPP7_USAGE,
                 length=LEN.LONG_USAGE,
                 title='HIDPP7 Usage',
                 name='hidpp7_usage',
                 aliases=('usage',),
                 checks=(CheckHexList(min_length=LEN.USAGE // 8, max_length=LEN.LONG_USAGE // 8),),
                 default_value=DEFAULT.HIDPP7_USAGE),
        BitField(fid=FID.HIDPP7_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='HIDPP7 Application Collection',
                 name='hidpp7_app_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.HIDPP7_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='HIDPP7 Report Id',
                 name='hidpp7_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.HIDPP7_REPORT_ID),
        BitField(fid=FID.HIDPP7_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='HIDPP7 Report Count',
                 name='hidpp7_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.HIDPP7_REPORT_COUNT),
        BitField(fid=FID.HIDPP7_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='HIDPP7 Report Size',
                 name='hidpp7_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.HIDPP_REPORT_SIZE),
        BitField(fid=FID.HIDPP7_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='HIDPP7 Logical Minimum',
                 name='hidpp7_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MINIMUM),
        BitField(fid=FID.HIDPP7_LOGICAL_MAXIMUM,
                 length=LEN.HIDPP_LOGICAL_MAXIMUM,
                 title='HIDPP7 Logical Maximum',
                 name='hidpp7_logical_maximum',
                 checks=(CheckHexList(LEN.HIDPP_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MAXIMUM),
        BitField(fid=FID.HIDPP7_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='HIDPP7 Input Usage',
                 name='hidpp7_input_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.HIDPP7_INPUT_DATA,
                 length=LEN.INPUT_DATA,
                 title='HIDPP7 Input',
                 name='hidpp7_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA_ABS),
        BitField(fid=FID.HIDPP7_OUTPUT_USAGE,
                 length=LEN.USAGE,
                 title='HIDPP7 Output Usage',
                 name='hidpp7_out_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.HIDPP7_OUTPUT_DATA,
                 length=LEN.OUTPUT_DATA,
                 title='HIDPP7 Output',
                 name='hidpp7_output_data',
                 checks=(CheckHexList(LEN.OUTPUT_DATA // 8),),
                 default_value=DEFAULT.OUTPUT_DATA_ABS),
        BitField(fid=FID.HIDPP7_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='HIDPP7 End Collection',
                 name='hidpp7_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class HIDppShortMessageDescriptor


class SdataMessageDescriptor(HIDppMessageDescriptor):
    """
    Define the SDATA messages descriptor.
    """
    BITFIELD_LENGTH = 33  # Bytes

    class FID(HIDppMessageDescriptor.FID):
        # See ``HIDppMessageDescriptor.FID``
        SDATA_USAGE_PAGE = 0xFF
        SDATA_USAGE = SDATA_USAGE_PAGE - 1
        SDATA_APP_COLLECTION = SDATA_USAGE - 1
        SDATA_REPORT_ID = SDATA_APP_COLLECTION - 1
        SDATA_INPUT_USAGE = SDATA_REPORT_ID - 1
        SDATA_LOGICAL_MINIMUM = SDATA_INPUT_USAGE - 1
        SDATA_LOGICAL_MAXIMUM = SDATA_LOGICAL_MINIMUM - 1
        SDATA_IN_REPORT_SIZE = SDATA_LOGICAL_MAXIMUM - 1
        SDATA_IN_REPORT_COUNT = SDATA_IN_REPORT_SIZE - 1
        SDATA_INPUT_DATA = SDATA_IN_REPORT_COUNT - 1
        SDATA_OUTPUT_USAGE = SDATA_INPUT_DATA - 1
        SDATA_OUT_REPORT_SIZE = SDATA_OUTPUT_USAGE - 1
        SDATA_OUT_REPORT_COUNT = SDATA_OUT_REPORT_SIZE - 1
        SDATA_OUTPUT_DATA = SDATA_OUT_REPORT_COUNT - 1
        SDATA_END_COLLECTION = SDATA_OUTPUT_DATA - 1
    # end class FID

    class LEN(HIDppMessageDescriptor.LEN):
        # See ``HIDppMessageDescriptor.LEN``
        VLP1_REPORT_COUNT = 0x18

    class DEFAULT(HIDppMessageDescriptor.DEFAULT):
        HIDPP_REPORT_SIZE = HexList("7508")
        HIDPP_LOGICAL_MINIMUM = HexList("1500")
        HIDPP_LOGICAL_MAXIMUM = HexList("26FF00")
        VLP_NORMAL_REPORT_COUNT = HexList("961F00")
        VLP_EXTENDED_REPORT_COUNT = HexList("96FE0F")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.SDATA_USAGE_PAGE,
                 length=LEN.HIDPP_USAGE_PAGE,
                 title='SDATA UsagePage',
                 name='sdata_usage_page',
                 checks=(CheckHexList(LEN.HIDPP_USAGE_PAGE // 8),),
                 default_value=DEFAULT.SDATAWAY_USAGE_PAGE),
        BitField(fid=FID.SDATA_USAGE,
                 length=LEN.USAGE,
                 title='SDATA Usage',
                 name='sdata_usage',
                 aliases=('usage',),
                 checks=(CheckHexList(min_length=LEN.USAGE // 8, max_length=LEN.LONG_USAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.SDATA_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='SDATA Application Collection',
                 name='sdata_app_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.SDATA_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='SDATA Report Id',
                 name='sdata_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.FEATURE_REPORT_ID),
        BitField(fid=FID.SDATA_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='SDATA Input Usage',
                 name='sdata_input_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.SDATA_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='SDATA Logical Minimum',
                 name='sdata_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MINIMUM),
        BitField(fid=FID.SDATA_LOGICAL_MAXIMUM,
                 length=LEN.HIDPP_LOGICAL_MAXIMUM,
                 title='SDATA Logical Maximum',
                 name='sdata_logical_maximum',
                 checks=(CheckHexList(LEN.HIDPP_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MAXIMUM),
        BitField(fid=FID.SDATA_IN_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='SDATA Input Report Size',
                 name='sdata_input_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.HIDPP_REPORT_SIZE),
        BitField(fid=FID.SDATA_IN_REPORT_COUNT,
                 length=LEN.LONG_USAGE,
                 title='SDATA Input Report Count',
                 name='sdata_input_report_count',
                 checks=(CheckHexList(LEN.LONG_USAGE // 8),),
                 default_value=DEFAULT.FEATURE_IN_REPORT_COUNT),
        BitField(fid=FID.SDATA_INPUT_DATA,
                 length=LEN.INPUT_DATA,
                 title='SDATA Input',
                 name='sdata_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.SDATA_OUTPUT_USAGE,
                 length=LEN.USAGE,
                 title='SDATA Output Usage',
                 name='sdata_out_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.SDATA_OUT_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='SDATA Output Report Size',
                 name='sdata_output_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.HIDPP_REPORT_SIZE),
        BitField(fid=FID.SDATA_OUT_REPORT_COUNT,
                 length=LEN.LONG_USAGE,
                 title='SDATA Output Report Count',
                 name='sdata_output_report_count',
                 checks=(CheckHexList(LEN.LONG_USAGE // 8),),
                 default_value=DEFAULT.FEATURE_OUT_REPORT_COUNT),
        BitField(fid=FID.SDATA_OUTPUT_DATA,
                 length=LEN.OUTPUT_DATA,
                 title='SDATA Output',
                 name='sdata_output_data',
                 checks=(CheckHexList(LEN.OUTPUT_DATA // 8),),
                 default_value=DEFAULT.OUTPUT_DATA),
        BitField(fid=FID.SDATA_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='SDATA End Collection',
                 name='sdata_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class SdataMessageDescriptor


class HIDppLongMessageDescriptor(HIDppMessageDescriptor):
    """
    Define the HID++ long-messages descriptor.
    """
    BITFIELD_LENGTH = 28  # Bytes

    class FID(HIDppMessageDescriptor.FID):
        # See ``HIDppMessageDescriptor.FID``
        HIDPP20_USAGE_PAGE = HIDppShortMessageDescriptor.FID.HIDPP7_END_COLLECTION - 1
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

    LEN = HIDppMessageDescriptor.LEN

    class DEFAULT(HIDppMessageDescriptor.DEFAULT):
        # See ``HIDppMessageDescriptor.DEFAULT``
        HIDPP20_USAGE = HexList("0A0203")
        HIDPP20_REPORT_COUNT = HexList("9513")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.HIDPP20_USAGE_PAGE,
                 length=LEN.HIDPP_USAGE_PAGE,
                 title='HIDPP20 UsagePage',
                 name='hidpp20_usage_page',
                 checks=(CheckHexList(LEN.HIDPP_USAGE_PAGE // 8),),
                 default_value=DEFAULT.HIDPP_USAGE_PAGE),
        BitField(fid=FID.HIDPP20_USAGE,
                 length=LEN.LONG_USAGE,
                 title='HIDPP20 Usage',
                 name='hidpp20_usage',
                 checks=(CheckHexList(min_length=LEN.USAGE // 8, max_length=LEN.LONG_USAGE // 8),),
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
                 default_value=DEFAULT.HIDPP_REPORT_SIZE),
        BitField(fid=FID.HIDPP20_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='HIDPP20 Logical Minimum',
                 name='hidpp20_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MINIMUM),
        BitField(fid=FID.HIDPP20_LOGICAL_MAXIMUM,
                 length=LEN.HIDPP_LOGICAL_MAXIMUM,
                 title='HIDPP20 Logical Maximum',
                 name='hidpp20_logical_maximum',
                 checks=(CheckHexList(LEN.HIDPP_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MAXIMUM),
        BitField(fid=FID.HIDPP20_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='HIDPP20 Input Usage',
                 name='hidpp20_input_usage',
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
# end class HIDppLongMessageDescriptor


class VLPLongMessageDescriptor(HIDppMessageDescriptor):
    """
    Define the HID++ long-messages descriptor.
    """
    BITFIELD_LENGTH = 28  # Bytes

    class FID(HIDppMessageDescriptor.FID):
        # See ``HIDppMessageDescriptor.FID``
        HIDPP20_USAGE_PAGE = 0xFF
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

    LEN = HIDppMessageDescriptor.LEN

    class DEFAULT(HIDppMessageDescriptor.DEFAULT):
        # See ``HIDppMessageDescriptor.DEFAULT``
        HIDPP20_USAGE = HexList("0A0203")
        HIDPP20_REPORT_COUNT = HexList("9513")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.HIDPP20_USAGE_PAGE,
                 length=LEN.HIDPP_USAGE_PAGE,
                 title='HIDPP20 UsagePage',
                 name='hidpp20_usage_page',
                 checks=(CheckHexList(LEN.HIDPP_USAGE_PAGE // 8),),
                 default_value=DEFAULT.HIDPP_USAGE_PAGE),
        BitField(fid=FID.HIDPP20_USAGE,
                 length=LEN.LONG_USAGE,
                 title='HIDPP20 Usage',
                 name='hidpp20_usage',
                 checks=(CheckHexList(min_length=LEN.USAGE // 8, max_length=LEN.LONG_USAGE // 8),),
                 default_value=DEFAULT.VLP_MODE_1A02_USAGE),
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
                 default_value=DEFAULT.HIDPP_REPORT_SIZE),
        BitField(fid=FID.HIDPP20_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='HIDPP20 Logical Minimum',
                 name='hidpp20_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MINIMUM),
        BitField(fid=FID.HIDPP20_LOGICAL_MAXIMUM,
                 length=LEN.HIDPP_LOGICAL_MAXIMUM,
                 title='HIDPP20 Logical Maximum',
                 name='hidpp20_logical_maximum',
                 checks=(CheckHexList(LEN.HIDPP_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MAXIMUM),
        BitField(fid=FID.HIDPP20_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='HIDPP20 Input Usage',
                 name='hidpp20_input_usage',
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
# end class VLPLongMessageDescriptor


class VLPNormalMessageDescriptor(HIDppMessageDescriptor):
    """
    Define the HID++ short-messages descriptor.
    """
    BITFIELD_LENGTH = 31  # Bytes

    class FID(HIDppMessageDescriptor.FID):
        # See ``HIDppMessageDescriptor.FID``
        VLP1_USAGE_PAGE = VLPLongMessageDescriptor.FID.HIDPP20_END_COLLECTION - 1
        VLP1_USAGE = VLP1_USAGE_PAGE - 1
        VLP1_APP_COLLECTION = VLP1_USAGE - 1
        VLP1_REPORT_ID = VLP1_APP_COLLECTION - 1
        VLP1_REPORT_COUNT = VLP1_REPORT_ID - 1
        VLP1_REPORT_SIZE = VLP1_REPORT_COUNT - 1
        VLP1_LOGICAL_MINIMUM = VLP1_REPORT_SIZE - 1
        VLP1_LOGICAL_MAXIMUM = VLP1_LOGICAL_MINIMUM - 1
        VLP1_INPUT_USAGE = VLP1_LOGICAL_MAXIMUM - 1
        VLP1_INPUT_DATA = VLP1_INPUT_USAGE - 1
        VLP1_OUTPUT_USAGE = VLP1_INPUT_DATA - 1
        VLP1_OUTPUT_DATA = VLP1_OUTPUT_USAGE - 1
        VLP1_END_COLLECTION = VLP1_OUTPUT_DATA - 1
    # end class FID

    class LEN(HIDppMessageDescriptor.LEN):
        # See ``HIDppMessageDescriptor.LEN``
        VLP1_REPORT_COUNT = 0x18
        VLP_INPUT_DATA = 0x18
        VLP_OUTPUT_DATA = 0x18

    class DEFAULT(HIDppMessageDescriptor.DEFAULT):
        HIDPP_REPORT_SIZE = HexList("7508")
        HIDPP_LOGICAL_MINIMUM = HexList("1500")
        HIDPP_LOGICAL_MAXIMUM = HexList("26FF00")
        VLP_NORMAL_REPORT_COUNT = HexList("961F00")
        VLP_EXTENDED_REPORT_COUNT = HexList("96FE0F")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.VLP1_USAGE_PAGE,
                 length=LEN.HIDPP_USAGE_PAGE,
                 title='VLP1 Normal UsagePage',
                 name='vlp1_normal_usage_page',
                 checks=(CheckHexList(LEN.HIDPP_USAGE_PAGE // 8),),
                 default_value=DEFAULT.HIDPP_USAGE_PAGE),
        BitField(fid=FID.VLP1_USAGE,
                 length=LEN.LONG_USAGE,
                 title='VLP1 Normal Usage',
                 name='vlp1_normal_usage',
                 aliases=('usage',),
                 checks=(CheckHexList(min_length=LEN.USAGE // 8, max_length=LEN.LONG_USAGE // 8),),
                 default_value=DEFAULT.VLP_NORMAL_USAGE),
        BitField(fid=FID.VLP1_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='VLP1 Normal Application Collection',
                 name='vlp1_normal_app_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.VLP1_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='VLP1 Normal Report Id',
                 name='vlp1_normal_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.VLP_NORMAL_REPORT_ID),
        BitField(fid=FID.VLP1_REPORT_COUNT,
                 length=LEN.VLP1_REPORT_COUNT,
                 title='VLP1 Normal Report Count',
                 name='vlp1_normal_report_count',
                 checks=(CheckHexList(LEN.VLP1_REPORT_COUNT // 8),),
                 default_value=DEFAULT.VLP_NORMAL_REPORT_COUNT),
        BitField(fid=FID.VLP1_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='VLP1 Normal Report Size',
                 name='vlp1_normal_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.HIDPP_REPORT_SIZE),
        BitField(fid=FID.VLP1_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='VLP1 Normal Logical Minimum',
                 name='vlp1_normal_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MINIMUM),
        BitField(fid=FID.VLP1_LOGICAL_MAXIMUM,
                 length=LEN.HIDPP_LOGICAL_MAXIMUM,
                 title='VLP1 Normal Logical Maximum',
                 name='vlp1_normal_logical_maximum',
                 checks=(CheckHexList(LEN.HIDPP_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MAXIMUM),
        BitField(fid=FID.VLP1_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='VLP1 Normal Input Usage',
                 name='vlp1_normal_input_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.VLP_NORMAL_IN_OUT_USAGE),
        BitField(fid=FID.VLP1_INPUT_DATA,
                 length=LEN.VLP_INPUT_DATA,
                 title='VLP1 Normal Input',
                 name='vlp1_normal_input_data',
                 checks=(CheckHexList(LEN.VLP_INPUT_DATA // 8),),
                 default_value=DEFAULT.VLP1_DATA_ABS),
        BitField(fid=FID.VLP1_OUTPUT_USAGE,
                 length=LEN.USAGE,
                 title='VLP1 Normal Output Usage',
                 name='vlp1_normal_out_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.VLP_NORMAL_IN_OUT_USAGE),
        BitField(fid=FID.VLP1_OUTPUT_DATA,
                 length=LEN.VLP_OUTPUT_DATA,
                 title='VLP1 Normal Output',
                 name='vlp1_normal_output_data',
                 checks=(CheckHexList(LEN.VLP_OUTPUT_DATA // 8),),
                 default_value=DEFAULT.VLP1_OUT_DATA_ABS),
        BitField(fid=FID.VLP1_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='VLP1 Normal End Collection',
                 name='vlp1_normal_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class VLPNormalMessageDescriptor


class VLPExtendedMessageDescriptor(VLPNormalMessageDescriptor):
    """
    Define the HID++ short-messages descriptor.
    """
    BITFIELD_LENGTH = 26  # Bytes

    class FID(HIDppMessageDescriptor.FID):
        # See ``HIDppMessageDescriptor.FID``
        VLP1_USAGE_PAGE = VLPNormalMessageDescriptor.FID.VLP1_END_COLLECTION - 1
        VLP1_USAGE = VLP1_USAGE_PAGE - 1
        VLP1_APP_COLLECTION = VLP1_USAGE - 1
        VLP1_REPORT_ID = VLP1_APP_COLLECTION - 1
        VLP1_REPORT_COUNT = VLP1_REPORT_ID - 1
        VLP1_REPORT_SIZE = VLP1_REPORT_COUNT - 1
        VLP1_LOGICAL_MINIMUM = VLP1_REPORT_SIZE - 1
        VLP1_LOGICAL_MAXIMUM = VLP1_LOGICAL_MINIMUM - 1
        VLP1_INPUT_USAGE = VLP1_LOGICAL_MAXIMUM - 1
        VLP1_INPUT_DATA = VLP1_INPUT_USAGE - 1
        VLP1_OUTPUT_USAGE = VLP1_INPUT_DATA - 1
        VLP1_OUTPUT_DATA = VLP1_OUTPUT_USAGE - 1
        VLP1_END_COLLECTION = VLP1_OUTPUT_DATA - 1

    # end class FID

    LEN = VLPNormalMessageDescriptor.LEN
    DEFAULT = VLPNormalMessageDescriptor.DEFAULT

    FIELDS = (
        BitField(fid=FID.VLP1_USAGE_PAGE,
                 length=LEN.HIDPP_USAGE_PAGE,
                 title='VLP1 Extended UsagePage',
                 name='vlp1_extended_usage_page',
                 checks=(CheckHexList(LEN.HIDPP_USAGE_PAGE // 8),),
                 default_value=DEFAULT.HIDPP_USAGE_PAGE),
        BitField(fid=FID.VLP1_USAGE,
                 length=LEN.LONG_USAGE,
                 title='VLP1 Extended Usage',
                 name='vlp1_extended_usage',
                 aliases=('usage',),
                 checks=(CheckHexList(min_length=LEN.USAGE // 8, max_length=LEN.LONG_USAGE // 8),),
                 default_value=DEFAULT.VLP_EXTENDED_USAGE),
        BitField(fid=FID.VLP1_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='VLP1 Extended Application Collection',
                 name='vlp1_extended_app_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.VLP1_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='VLP1 Extended Report Id',
                 name='vlp1_extended_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.VLP_EXTENDED_REPORT_ID),
        BitField(fid=FID.VLP1_REPORT_COUNT,
                 length=LEN.VLP1_REPORT_COUNT,
                 title='VLP1 Extended Report Count',
                 name='vlp1_extended_report_count',
                 checks=(CheckHexList(LEN.VLP1_REPORT_COUNT // 8),),
                 default_value=DEFAULT.VLP_EXTENDED_REPORT_COUNT),
        BitField(fid=FID.VLP1_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='VLP1 Extended Report Size',
                 name='vlp1_extended_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.HIDPP_REPORT_SIZE),
        BitField(fid=FID.VLP1_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='VLP1 Extended Logical Minimum',
                 name='vlp1_extended_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MINIMUM),
        BitField(fid=FID.VLP1_LOGICAL_MAXIMUM,
                 length=LEN.HIDPP_LOGICAL_MAXIMUM,
                 title='VLP1 Extended Logical Maximum',
                 name='vlp1_extended_logical_maximum',
                 checks=(CheckHexList(LEN.HIDPP_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.HIDPP_LOGICAL_MAXIMUM),
        BitField(fid=FID.VLP1_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='VLP1 Extended Input Usage',
                 name='vlp1_extended_input_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.VLP_EXTENDED_IN_OUT_USAGE),
        BitField(fid=FID.VLP1_OUTPUT_DATA,
                 length=LEN.VLP_OUTPUT_DATA,
                 title='VLP1 Extended Output',
                 name='vlp1_extended_output_data',
                 checks=(CheckHexList(LEN.VLP_OUTPUT_DATA // 8),),
                 default_value=DEFAULT.VLP1_OUT_DATA_ABS),
        BitField(fid=FID.VLP1_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='VLP1 Extended End Collection',
                 name='vlp1_extended_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class VLPExtendedMessageDescriptor


class ConsumerGenericLexendKeyDescriptor(ConsumerGenericKeyDescriptor):
    """
    Define the USB Consumer Generic with Lexend support key descriptor.
    """
    BITFIELD_LENGTH = 26

    class FID(ConsumerGenericKeyDescriptor.FID):
        CON_GEN_USAGE_PAGE = VLPExtendedMessageDescriptor.FID.VLP1_END_COLLECTION - 1
        CONS_GEN_USAGE = CON_GEN_USAGE_PAGE - 1
        CONS_GEN_APP_COLLECTION = CONS_GEN_USAGE - 1
        CONS_GEN_REPORT_ID = CONS_GEN_APP_COLLECTION - 1
        CONS_GEN_REPORT_COUNT = CONS_GEN_REPORT_ID - 1
        CONS_GEN_REPORT_SIZE = CONS_GEN_REPORT_COUNT - 1
        CONS_GEN_LOGICAL_MINIMUM = CONS_GEN_REPORT_SIZE - 1
        CONS_GEN_LOGICAL_MAXIMUM = CONS_GEN_LOGICAL_MINIMUM - 1
        CON_AC_BACK_USAGE = CONS_GEN_LOGICAL_MAXIMUM - 1
        CON_GEN_INPUT_DATA = CON_AC_BACK_USAGE - 1
        CON_GEN_IN_REPORT_COUNT = CON_GEN_INPUT_DATA - 1
        CON_GEN_INPUT_USAGE = CON_GEN_IN_REPORT_COUNT - 1
        CON_GEN_END_COLLECTION = CON_GEN_INPUT_USAGE - 1

    class LEN(ConsumerGenericKeyDescriptor.LEN):
        CON_AC_BACK_USAGE = 0x18

    class DEFAULT(ConsumerGenericKeyDescriptor.DEFAULT):
        CONSUMER_GEN_REPORT_COUNT = HexList("9501")
        CONS_GEN_REPORT_SIZE = HexList("7501")
        CONS_GEN_LOGICAL_MINIMUM = HexList("1500")
        CONS_GEN_LOGICAL_MAXIMUM = HexList("2501")
        CON_AC_BACK_USAGE = HexList("0A2402")

    FIELDS = (
        BitField(fid=FID.CON_GEN_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Consumer Generic Usage Page',
                 name='cons_gen_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE_PAGE),
        BitField(fid=FID.CONS_GEN_USAGE,
                 length=LEN.USAGE,
                 title='Consumer Generic Usage',
                 name='cons_gen_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONSUMER_USAGE),
        BitField(fid=FID.CONS_GEN_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Consumer Generic App Collection',
                 name='cons_gen_app_collection',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.CONS_GEN_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Consumer Generic Report ID',
                 name='cons_gen_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.CONS_MIN_REPORT_ID),
        BitField(fid=FID.CONS_GEN_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Consumer Generic Report Count',
                 name='cons_gen_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.CONSUMER_GEN_REPORT_COUNT),
        BitField(fid=FID.CONS_GEN_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Consumer Generic Report Size',
                 name='cons_gen_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.CONS_GEN_REPORT_SIZE),
        BitField(fid=FID.CONS_GEN_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Consumer Generic Logical Minimum',
                 name='cons_gen_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.CONS_GEN_LOGICAL_MINIMUM),
        BitField(fid=FID.CONS_GEN_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Consumer Generic Logical Minimum',
                 name='cons_gen_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.CONS_GEN_LOGICAL_MAXIMUM),
        BitField(fid=FID.CON_AC_BACK_USAGE,
                 length=LEN.CON_AC_BACK_USAGE,
                 title='Consumer Generic AC Back Usage',
                 name='cons_gen_ac_back_usage',
                 checks=(CheckHexList(LEN.CON_AC_BACK_USAGE // 8),),
                 default_value=DEFAULT.CON_AC_BACK_USAGE),
        BitField(fid=FID.CON_GEN_INPUT_DATA,
                 length=LEN.INPUT_DATA,
                 title='Consumer Generic Input Data',
                 name='cons_gen_input_data',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.CON_GEN_IN_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Consumer Generic Input Report Count',
                 name='cons_gen_in_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.CONS_MIN_RSV_REPORT_ID),
        BitField(fid=FID.CON_GEN_INPUT_USAGE,
                 length=LEN.USAGE,
                 title='Consumer Generic Input Usage',
                 name='cons_gen_in_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.INPUT_CST),
        BitField(fid=FID.CON_GEN_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Consumer Generic End Collection',
                 name='cons_gen_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class ConsumerGenericLexendKeyDescriptor


class HIDppInterfaceDescriptor(ReportDescriptor):
    """
    Concatenate the HID++ Short and Long messages descriptors.
    """
    # 56 Bytes
    BITFIELD_LENGTH = (HIDppShortMessageDescriptor.BITFIELD_LENGTH + HIDppLongMessageDescriptor.BITFIELD_LENGTH)

    FIELDS = HIDppShortMessageDescriptor.FIELDS + HIDppLongMessageDescriptor.FIELDS
# end class HIDppInterfaceDescriptor


class VlpInterfaceDescriptor(HIDppInterfaceDescriptor):
    """
    Concatenate the VLP normal and extended messages descriptors.
    """
    # 111 Bytes
    BITFIELD_LENGTH = (VLPLongMessageDescriptor.BITFIELD_LENGTH +
                       VLPNormalMessageDescriptor.BITFIELD_LENGTH +
                       VLPExtendedMessageDescriptor.BITFIELD_LENGTH +
                       GenericDesktopSystemControlDescriptor.BITFIELD_LENGTH)

    FIELDS = VLPLongMessageDescriptor.FIELDS + \
        VLPNormalMessageDescriptor.FIELDS + \
        VLPExtendedMessageDescriptor.FIELDS + \
        GenericDesktopSystemControlDescriptor.FIELDS
# end class VlpInterfaceDescriptor


class HIDppReceiverInterfaceDescriptor(HIDppInterfaceDescriptor):
    """
    Concatenate the HID++ Short and Long messages descriptors applicable BOLT receiver and some old products.
    """
    # 54 Bytes
    BITFIELD_LENGTH = HIDppInterfaceDescriptor.BITFIELD_LENGTH - 2

    class DEFAULT(HIDppInterfaceDescriptor.DEFAULT):
        """
        FIELDS Default values
        """
        HIDPP_RECEIVER_USAGE_PAGE = HexList("0600FF")
    # end class DEFAULT

    FIELDS = (
            BitField(fid=HIDppShortMessageDescriptor.FID.HIDPP7_USAGE_PAGE,
                     length=HIDppMessageDescriptor.LEN.HIDPP_USAGE_PAGE,
                     title='HIDPP7 UsagePage',
                     name='hidpp7_usage_page',
                     checks=(CheckHexList(HIDppMessageDescriptor.LEN.HIDPP_USAGE_PAGE // 8),),
                     default_value=DEFAULT.HIDPP_RECEIVER_USAGE_PAGE),
            BitField(fid=HIDppShortMessageDescriptor.FID.HIDPP7_USAGE,
                     length=HIDppInterfaceDescriptor.LEN.USAGE,
                     title='HIDPP7 Usage',
                     name='hidpp7_usage',
                     aliases=('usage',),
                     checks=(CheckHexList(HIDppInterfaceDescriptor.LEN.USAGE // 8),),
                     default_value=ReportDescriptor.DEFAULT.CONSUMER_USAGE),
        ) + \
        HIDppInterfaceDescriptor.FIELDS[(HIDppShortMessageDescriptor.FID.HIDPP7_USAGE_PAGE -
                                         HIDppShortMessageDescriptor.FID.HIDPP7_APP_COLLECTION):
                                        (HIDppShortMessageDescriptor.FID.HIDPP7_USAGE_PAGE -
                                         HIDppLongMessageDescriptor.FID.HIDPP20_USAGE_PAGE)] + \
        (
            BitField(fid=HIDppLongMessageDescriptor.FID.HIDPP20_USAGE_PAGE,
                     length=HIDppMessageDescriptor.LEN.HIDPP_USAGE_PAGE,
                     title='HIDPP20 UsagePage',
                     name='hidpp20_usage_page',
                     checks=(CheckHexList(HIDppMessageDescriptor.LEN.HIDPP_USAGE_PAGE // 8),),
                     default_value=DEFAULT.HIDPP_RECEIVER_USAGE_PAGE),
            BitField(fid=HIDppLongMessageDescriptor.FID.HIDPP20_USAGE,
                     length=HIDppMessageDescriptor.LEN.USAGE,
                     title='HIDPP20 Usage',
                     name='hidpp20_usage',
                     checks=(CheckHexList(HIDppMessageDescriptor.LEN.USAGE // 8),),
                     default_value=ReportDescriptor.DEFAULT.MOUSE_USAGE),
        ) + \
        HIDppInterfaceDescriptor.FIELDS[(HIDppShortMessageDescriptor.FID.HIDPP7_USAGE_PAGE -
                                         HIDppLongMessageDescriptor.FID.HIDPP20_APP_COLLECTION):]
# end class HIDppReceiverInterfaceDescriptor

class DrifterHIDppInterfaceDescriptor(HIDppInterfaceDescriptor):
    """
    Concatenate the HID++ Short and Long messages descriptors applicable for Drifter(Simulation)

    Differences with the base interface (i.e. HIDppInterfaceDescriptor)
     - Report count and report size fields are flipped for both HID++ 7 and 20 bytes long messages
    """
    # 54 Bytes
    BITFIELD_LENGTH = HIDppInterfaceDescriptor.BITFIELD_LENGTH - 2

    class DEFAULT(HIDppInterfaceDescriptor.DEFAULT):
        """
        FIELDS Default values
        """
        HIDPP_RECEIVER_USAGE_PAGE = HexList("0600FF")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=HIDppShortMessageDescriptor.FID.HIDPP7_USAGE_PAGE,
                 length=HIDppMessageDescriptor.LEN.HIDPP_USAGE_PAGE,
                 title='HIDPP7 UsagePage',
                 name='hidpp7_usage_page',
                 checks=(CheckHexList(HIDppMessageDescriptor.LEN.HIDPP_USAGE_PAGE // 8),),
                 default_value=DEFAULT.HIDPP_RECEIVER_USAGE_PAGE),
        BitField(fid=HIDppShortMessageDescriptor.FID.HIDPP7_USAGE,
                 length=HIDppInterfaceDescriptor.LEN.USAGE,
                 title='HIDPP7 Usage',
                 name='hidpp7_usage',
                 aliases=('usage',),
                 checks=(CheckHexList(HIDppInterfaceDescriptor.LEN.USAGE // 8),),
                 default_value=ReportDescriptor.DEFAULT.CONSUMER_USAGE),
        BitField(fid=HIDppShortMessageDescriptor.FID.HIDPP7_APP_COLLECTION,
                 length=HIDppShortMessageDescriptor.LEN.COLLECTION,
                 title='HIDPP7 Application Collection',
                 name='hidpp7_app_collection',
                 checks=(CheckHexList(HIDppShortMessageDescriptor.LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=HIDppShortMessageDescriptor.FID.HIDPP7_REPORT_ID,
                 length=HIDppShortMessageDescriptor.LEN.REPORT_ID,
                 title='HIDPP7 Report Id',
                 name='hidpp7_report_id',
                 checks=(CheckHexList(HIDppShortMessageDescriptor.LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.HIDPP7_REPORT_ID),
        BitField(fid=HIDppShortMessageDescriptor.FID.HIDPP7_REPORT_SIZE,
                 length=HIDppShortMessageDescriptor.LEN.REPORT_SIZE,
                 title='HIDPP7 Report Size',
                 name='hidpp7_report_size',
                 checks=(CheckHexList(HIDppShortMessageDescriptor.LEN.REPORT_SIZE // 8),),
                 default_value=HIDppShortMessageDescriptor.DEFAULT.HIDPP_REPORT_SIZE),
        BitField(fid=HIDppShortMessageDescriptor.FID.HIDPP7_REPORT_COUNT,
                 length=HIDppShortMessageDescriptor.LEN.REPORT_COUNT,
                 title='HIDPP7 Report Count',
                 name='hidpp7_report_count',
                 checks=(CheckHexList(HIDppShortMessageDescriptor.LEN.REPORT_COUNT // 8),),
                 default_value=HIDppShortMessageDescriptor.DEFAULT.HIDPP7_REPORT_COUNT),
         ) + \
        HIDppInterfaceDescriptor.FIELDS[(HIDppShortMessageDescriptor.FID.HIDPP7_USAGE_PAGE -
                                         HIDppShortMessageDescriptor.FID.HIDPP7_LOGICAL_MINIMUM):
                                        (HIDppShortMessageDescriptor.FID.HIDPP7_USAGE_PAGE -
                                         HIDppLongMessageDescriptor.FID.HIDPP20_USAGE_PAGE)] + \
         (
                  BitField(fid=HIDppLongMessageDescriptor.FID.HIDPP20_USAGE_PAGE,
                          length=HIDppMessageDescriptor.LEN.HIDPP_USAGE_PAGE,
                          title='HIDPP20 UsagePage',
                          name='hidpp20_usage_page',
                          checks=(CheckHexList(HIDppMessageDescriptor.LEN.HIDPP_USAGE_PAGE // 8),),
                          default_value=DEFAULT.HIDPP_RECEIVER_USAGE_PAGE),
                  BitField(fid=HIDppLongMessageDescriptor.FID.HIDPP20_USAGE,
                           length=HIDppMessageDescriptor.LEN.USAGE,
                           title='HIDPP20 Usage',
                           name='hidpp20_usage',
                           checks=(CheckHexList(HIDppMessageDescriptor.LEN.USAGE // 8),),
                           default_value=DEFAULT.MOUSE_USAGE),
                  BitField(fid=HIDppLongMessageDescriptor.FID.HIDPP20_APP_COLLECTION,
                           length=HIDppMessageDescriptor.LEN.COLLECTION,
                           title='HIDPP20 Application Collection',
                           name='hidpp20_app_collection',
                           checks=(CheckHexList(HIDppMessageDescriptor.LEN.COLLECTION // 8),),
                           default_value=DEFAULT.APP_COLLECTION),
                  BitField(fid=HIDppLongMessageDescriptor.FID.HIDPP20_REPORT_ID,
                           length=HIDppLongMessageDescriptor.LEN.REPORT_ID,
                           title='HIDPP20 Report Id',
                           name='hidpp20_report_id',
                           checks=(CheckHexList(HIDppLongMessageDescriptor.LEN.REPORT_ID // 8),),
                           default_value=DEFAULT.HIDPP20_REPORT_ID),
                 BitField(fid=HIDppLongMessageDescriptor.FID.HIDPP20_REPORT_SIZE,
                          length=HIDppLongMessageDescriptor.LEN.REPORT_SIZE,
                          title='HIDPP20 Report Size',
                          name='hidpp20_report_size',
                          checks=(CheckHexList(HIDppLongMessageDescriptor.LEN.REPORT_SIZE // 8),),
                          default_value=HIDppLongMessageDescriptor.DEFAULT.HIDPP_REPORT_SIZE),
                 BitField(fid=HIDppLongMessageDescriptor.FID.HIDPP20_REPORT_COUNT,
                          length=HIDppLongMessageDescriptor.LEN.REPORT_COUNT,
                          title='HIDPP20 Report Count',
                          name='hidpp20_report_count',
                          checks=(CheckHexList(HIDppLongMessageDescriptor.LEN.REPORT_COUNT // 8),),
                          default_value=HIDppLongMessageDescriptor.DEFAULT.HIDPP20_REPORT_COUNT),
         ) + \
        HIDppInterfaceDescriptor.FIELDS[-(HIDppLongMessageDescriptor.FID.HIDPP20_REPORT_SIZE -
                                         HIDppLongMessageDescriptor.FID.HIDPP20_END_COLLECTION):]
# end class DrifterHIDppInterfaceDescriptor


class FingerCollection(ReportDescriptor):
    """
    Define the Finger collection included in the Windows digitizer descriptor.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.qp9s1wvysdjz
    """
    BITFIELD_LENGTH = 70  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        FINGER_USAGE = 0xFF
        FINGER_LOGICAL_COLLECTION = FINGER_USAGE - 1
        FINGER_REPORT_COUNT = FINGER_LOGICAL_COLLECTION - 1
        FINGER_REPORT_SIZE = FINGER_REPORT_COUNT - 1
        FINGER_LOGICAL_MINIMUM = FINGER_REPORT_SIZE - 1
        FINGER_LOGICAL_MAXIMUM = FINGER_LOGICAL_MINIMUM - 1
        FINGER_USAGE_TOUCH = FINGER_LOGICAL_MAXIMUM - 1
        FINGER_USAGE_TIP_SWITCH = FINGER_USAGE_TOUCH - 1
        FINGER_INPUT = FINGER_USAGE_TIP_SWITCH - 1
        FINGER_CONTACT_REPORT_COUNT = FINGER_INPUT - 1
        FINGER_CONTACT_REPORT_SIZE = FINGER_CONTACT_REPORT_COUNT - 1
        FINGER_CONTACT_LOGICAL_MAXIMUM = FINGER_CONTACT_REPORT_SIZE - 1
        FINGER_CONTACT_USAGE = FINGER_CONTACT_LOGICAL_MAXIMUM - 1
        FINGER_CONTACT_INPUT = FINGER_CONTACT_USAGE - 1
        FINGER_PRESSURE_REPORT_SIZE = FINGER_CONTACT_INPUT - 1
        FINGER_PRESSURE_LOGICAL_MAXIMUM = FINGER_PRESSURE_REPORT_SIZE - 1
        FINGER_PRESSURE_USAGE = FINGER_PRESSURE_LOGICAL_MAXIMUM - 1
        FINGER_PRESSURE_INPUT = FINGER_PRESSURE_USAGE - 1
        FINGER_PUSH = FINGER_PRESSURE_INPUT - 1
        FINGER_X_REPORT_SIZE = FINGER_PUSH - 1
        FINGER_X_LOGICAL_MAXIMUM = FINGER_X_REPORT_SIZE - 1
        FINGER_X_PHYSICAL_MINIMUM = FINGER_X_LOGICAL_MAXIMUM - 1
        FINGER_X_PHYSICAL_MAXIMUM = FINGER_X_PHYSICAL_MINIMUM - 1
        FINGER_X_EXPONENT = FINGER_X_PHYSICAL_MAXIMUM - 1
        FINGER_X_UNIT = FINGER_X_EXPONENT - 1
        FINGER_X_USAGE_PAGE = FINGER_X_UNIT - 1
        FINGER_X_USAGE = FINGER_X_USAGE_PAGE - 1
        FINGER_X_INPUT = FINGER_X_USAGE - 1
        FINGER_Y_LOGICAL_MAXIMUM = FINGER_X_INPUT - 1
        FINGER_Y_PHYSICAL_MAXIMUM = FINGER_Y_LOGICAL_MAXIMUM - 1
        FINGER_Y_USAGE = FINGER_Y_PHYSICAL_MAXIMUM - 1
        FINGER_Y_INPUT = FINGER_Y_USAGE - 1
        FINGER_POP = FINGER_Y_INPUT - 1
        FINGER_END_COLECTION = FINGER_POP - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        FINGER_PUSH = 0x08
        FINGER_POP = 0x08
        FINGER_X_LOGICAL_MAXIMUM = 0x18
        FINGER_X_PHYSICAL_MAXIMUM = 0x18
        FINGER_Y_LOGICAL_MAXIMUM = 0x18
        FINGER_Y_PHYSICAL_MAXIMUM = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        FINGER_REPORT_COUNT = HexList("9502")
        FINGER_REPORT_SIZE = HexList("7501")
        FINGER_LOGICAL_MINIMUM = HexList("1500")
        FINGER_LOGICAL_MAXIMUM = HexList("2501")
        FINGER_CONTACT_REPORT_COUNT = HexList("9501")
        FINGER_CONTACT_REPORT_SIZE = HexList("7506")
        FINGER_CONTACT_LOGICAL_MAXIMUM = HexList("2504")
        FINGER_PRESSURE_REPORT_SIZE = HexList("7508")
        FINGER_PRESSURE_LOGICAL_MAXIMUM = HexList("26FF00")
        FINGER_PUSH = HexList("A4")
        FINGER_X_REPORT_SIZE = HexList("750C")
        FINGER_X_LOGICAL_MAXIMUM = HexList("26D70A")
        FINGER_X_PHYSICAL_MINIMUM = HexList("3500")
        FINGER_X_PHYSICAL_MAXIMUM = HexList("469204")
        FINGER_X_EXPONENT = HexList("550E")
        FINGER_X_UNIT = HexList("6511")
        FINGER_Y_LOGICAL_MAXIMUM = HexList("26FA06")
        FINGER_Y_PHYSICAL_MAXIMUM = HexList("46F302")
        FINGER_POP = HexList("B4")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.FINGER_USAGE,
                 length=LEN.USAGE_PAGE,
                 title='Finger Usage Page',
                 name='finger_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.FINGER_USAGE),
        BitField(fid=FID.FINGER_LOGICAL_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Finger Logical Collection',
                 name='finger_logical_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.LOGICAL_COLLECTION),
        BitField(fid=FID.FINGER_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Finger Report Count',
                 name='finger_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.FINGER_REPORT_COUNT),
        BitField(fid=FID.FINGER_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Finger Report Size',
                 name='finger_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.FINGER_REPORT_SIZE),
        BitField(fid=FID.FINGER_LOGICAL_MINIMUM,
                 length=LEN.LOGICAL_MINIMUM,
                 title='Finger Logical Minimum',
                 name='finger_logical_minimum',
                 checks=(CheckHexList(LEN.LOGICAL_MINIMUM // 8),),
                 default_value=DEFAULT.FINGER_LOGICAL_MINIMUM),
        BitField(fid=FID.FINGER_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Finger Logical Maximum',
                 name='finger_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.FINGER_LOGICAL_MAXIMUM),
        BitField(fid=FID.FINGER_USAGE_TOUCH,
                 length=LEN.USAGE,
                 title='Finger Touch Valid Usage',
                 name='finger_usage_touch',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.TOUCH_VALID_USAGE),
        BitField(fid=FID.FINGER_USAGE_TIP_SWITCH,
                 length=LEN.USAGE,
                 title='Finger Tip Switch Usage',
                 name='finger_usage_tip_switch',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.TIP_SWITCH_USAGE),
        BitField(fid=FID.FINGER_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Finger Input',
                 name='finger_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.FINGER_CONTACT_REPORT_COUNT,
                 length=LEN.REPORT_COUNT,
                 title='Finger Contact Report Count',
                 name='finger_contact_report_count',
                 checks=(CheckHexList(LEN.REPORT_COUNT // 8),),
                 default_value=DEFAULT.FINGER_CONTACT_REPORT_COUNT),
        BitField(fid=FID.FINGER_CONTACT_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Finger Contact Report Size',
                 name='finger_contact_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.FINGER_CONTACT_REPORT_SIZE),
        BitField(fid=FID.FINGER_CONTACT_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Finger Contact Logical Maximum',
                 name='finger_contact_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.FINGER_CONTACT_LOGICAL_MAXIMUM),
        BitField(fid=FID.FINGER_CONTACT_USAGE,
                 length=LEN.USAGE,
                 title='Finger Contact Identifier Usage',
                 name='finger_contact_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONTACT_IDENTIFIER_USAGE),
        BitField(fid=FID.FINGER_CONTACT_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Finger Contact Input',
                 name='finger_contact_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.FINGER_PRESSURE_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Finger Pressure Report Size',
                 name='finger_pressure_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.FINGER_PRESSURE_REPORT_SIZE),
        BitField(fid=FID.FINGER_PRESSURE_LOGICAL_MAXIMUM,
                 length=LEN.LONG_LOGICAL_MAXIMUM,
                 title='Finger Pressure Logical Maximum',
                 name='finger_pressure_logical_maximum',
                 checks=(CheckHexList(LEN.LONG_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.FINGER_PRESSURE_LOGICAL_MAXIMUM),
        BitField(fid=FID.FINGER_PRESSURE_USAGE,
                 length=LEN.USAGE,
                 title='Finger Tip Pressure Usage',
                 name='finger_pressure_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.TIP_PRESSURE_USAGE),
        BitField(fid=FID.FINGER_PRESSURE_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Finger Tip Pressure Input',
                 name='finger_pressure_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.FINGER_PUSH,
                 length=LEN.FINGER_PUSH,
                 title='Finger Push',
                 name='finger_push',
                 checks=(CheckHexList(LEN.FINGER_PUSH // 8),),
                 default_value=DEFAULT.FINGER_PUSH),
        BitField(fid=FID.FINGER_X_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Finger Report Size',
                 name='finger_x_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.FINGER_X_REPORT_SIZE),
        BitField(fid=FID.FINGER_X_LOGICAL_MAXIMUM,
                 length=LEN.FINGER_X_LOGICAL_MAXIMUM,
                 title='Finger X Logical Maximum',
                 name='finger_x_logical_maximum',
                 checks=(CheckHexList(LEN.FINGER_X_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.FINGER_X_LOGICAL_MAXIMUM),
        BitField(fid=FID.FINGER_X_PHYSICAL_MINIMUM,
                 length=LEN.PHYSICAL_MINIMUM,
                 title='Finger X Physical Minimum',
                 name='finger_x_physical_minimum',
                 checks=(CheckHexList(LEN.PHYSICAL_MINIMUM // 8),),
                 default_value=DEFAULT.FINGER_X_PHYSICAL_MINIMUM),
        BitField(fid=FID.FINGER_X_PHYSICAL_MAXIMUM,
                 length=LEN.FINGER_X_PHYSICAL_MAXIMUM,
                 title='Finger X Physical Maximum',
                 name='finger_x_physical_maximum',
                 checks=(CheckHexList(LEN.FINGER_X_PHYSICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.FINGER_X_PHYSICAL_MAXIMUM),
        BitField(fid=FID.FINGER_X_EXPONENT,
                 length=LEN.UNIT,
                 title='Finger X Unit Exponent',
                 name='finger_x_exponent',
                 checks=(CheckHexList(LEN.UNIT // 8),),
                 default_value=DEFAULT.FINGER_X_EXPONENT),
        BitField(fid=FID.FINGER_X_UNIT,
                 length=LEN.UNIT,
                 title='Finger X Unit',
                 name='finger_x_unit',
                 checks=(CheckHexList(LEN.UNIT // 8),),
                 default_value=DEFAULT.FINGER_X_UNIT),
        BitField(fid=FID.FINGER_X_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Finger X Usage Page',
                 name='finger_x_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.GENERIC_USAGE_PAGE),
        BitField(fid=FID.FINGER_X_USAGE,
                 length=LEN.USAGE,
                 title='Finger X Usage',
                 name='finger_x_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.AXIS_X_USAGE),
        BitField(fid=FID.FINGER_X_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Finger X Input',
                 name='finger_x_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.FINGER_Y_LOGICAL_MAXIMUM,
                 length=LEN.FINGER_Y_LOGICAL_MAXIMUM,
                 title='Finger Y Logical Maximum',
                 name='finger_y_logical_maximum',
                 checks=(CheckHexList(LEN.FINGER_Y_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.FINGER_Y_LOGICAL_MAXIMUM),
        BitField(fid=FID.FINGER_Y_PHYSICAL_MAXIMUM,
                 length=LEN.FINGER_Y_PHYSICAL_MAXIMUM,
                 title='Finger Y Physical Maximum',
                 name='finger_y_physical_maximum',
                 checks=(CheckHexList(LEN.FINGER_Y_PHYSICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.FINGER_Y_PHYSICAL_MAXIMUM),
        BitField(fid=FID.FINGER_Y_USAGE,
                 length=LEN.USAGE,
                 title='Finger Y Usage',
                 name='finger_y_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.AXIS_Y_USAGE),
        BitField(fid=FID.FINGER_Y_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Finger Y Input',
                 name='finger_y_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.FINGER_POP,
                 length=LEN.FINGER_POP,
                 title='Finger Pop',
                 name='finger_pop',
                 checks=(CheckHexList(LEN.FINGER_POP // 8),),
                 default_value=DEFAULT.FINGER_POP),
        BitField(fid=FID.FINGER_END_COLECTION,
                 length=LEN.END_COLLECTION,
                 title='Finger End Collection',
                 name='finger_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )
# end class FingerCollection


class WindowsDeviceCapabilitiesFeature(ReportDescriptor):
    """
    Define the Windows device capabilities Feature.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.xybj7auaykq4
    """
    BITFIELD_LENGTH = 10  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        WIN_DEV_CAP_REPORT_ID = 0xFF
        WIN_DEV_CAP_REPORT_SIZE = WIN_DEV_CAP_REPORT_ID - 1
        WIN_DEV_CAP_LOGICAL_MAXIMUM = WIN_DEV_CAP_REPORT_SIZE - 1
        WIN_DEV_CAP_CONTACT_COUNT_USAGE = WIN_DEV_CAP_LOGICAL_MAXIMUM - 1
        WIN_DEV_CAP_FEATURE = WIN_DEV_CAP_CONTACT_COUNT_USAGE - 1
    # end class FID

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        WIN_DEV_CAP_REPORT_SIZE = HexList("7508")
        WIN_DEV_CAP_LOGICAL_MAXIMUM = HexList("250F")
        WIN_DEV_CAP_CONTACT_COUNT_USAGE = HexList("0955")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.WIN_DEV_CAP_REPORT_ID,
                 length=ReportDescriptor.LEN.USAGE,
                 title='Windows Device Capabilities Report Id',
                 name='win_dev_cap_report_id',
                 checks=(CheckHexList(ReportDescriptor.LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.WIN_DEV_CAP_REPORT_ID),
        BitField(fid=FID.WIN_DEV_CAP_REPORT_SIZE,
                 length=ReportDescriptor.LEN.REPORT_SIZE,
                 title='Windows Device Capabilities Report Size',
                 name='win_dev_cap_report_size',
                 checks=(CheckHexList(ReportDescriptor.LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.WIN_DEV_CAP_REPORT_SIZE),
        BitField(fid=FID.WIN_DEV_CAP_LOGICAL_MAXIMUM,
                 length=ReportDescriptor.LEN.LOGICAL_MAXIMUM,
                 title='Windows Device Capabilities Logical Maximum',
                 name='win_dev_cap_logical_maximum',
                 checks=(CheckHexList(ReportDescriptor.LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.WIN_DEV_CAP_LOGICAL_MAXIMUM),
        BitField(fid=FID.WIN_DEV_CAP_CONTACT_COUNT_USAGE,
                 length=ReportDescriptor.LEN.USAGE,
                 title='Windows Device Capabilities Contact Count Usage',
                 name='win_dev_cap_contact_count_usage',
                 checks=(CheckHexList(ReportDescriptor.LEN.USAGE // 8),),
                 default_value=DEFAULT.WIN_DEV_CAP_CONTACT_COUNT_USAGE),
        BitField(fid=FID.WIN_DEV_CAP_FEATURE,
                 length=ReportDescriptor.LEN.INPUT_DATA,
                 title='Windows Device Capabilities Feature',
                 name='win_dev_cap_input',
                 checks=(CheckHexList(ReportDescriptor.LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.FEATURE_DATA),
    )
# end class WindowsDeviceCapabilitiesFeature


class WindowsDeviceCertificationStatusFeature(ReportDescriptor):
    """
    Define the Windows device certification status Feature.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.ei1nsig4hqk2
    """
    BITFIELD_LENGTH = 15  # Bytes

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        WIN_DEV_CER_REPORT_ID = 0xFF
        WIN_DEV_CER_REPORT_COUNT = WIN_DEV_CER_REPORT_ID - 1
        WIN_DEV_CER_LOGICAL_MAXIMUM = WIN_DEV_CER_REPORT_COUNT - 1
        WIN_DEV_CER_VENDOR_USAGE_PAGE = WIN_DEV_CER_LOGICAL_MAXIMUM - 1
        WIN_DEV_CER_VENDOR_USAGE = WIN_DEV_CER_VENDOR_USAGE_PAGE - 1
        WIN_DEV_CER_FEATURE = WIN_DEV_CER_VENDOR_USAGE - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        WIN_DEV_CER_REPORT_COUNT = 0x18
        WIN_DEV_CER_VENDOR_USAGE_PAGE = 0x18
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        WIN_DEV_CER_REPORT_COUNT = HexList("960001")
        WIN_DEV_CER_LOGICAL_MAXIMUM = HexList("26FF00")
        WIN_DEV_CER_VENDOR_USAGE_PAGE = HexList("0600FF")
        WIN_DEV_CER_VENDOR_USAGE = HexList("09C5")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.WIN_DEV_CER_REPORT_ID,
                 length=LEN.USAGE,
                 title='Windows Device Certification Report Id',
                 name='win_dev_cer_report_id',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.WIN_DEV_CER_REPORT_ID),
        BitField(fid=FID.WIN_DEV_CER_REPORT_COUNT,
                 length=LEN.WIN_DEV_CER_REPORT_COUNT,
                 title='Windows Device Certification Report Count',
                 name='win_dev_cer_report_count',
                 checks=(CheckHexList(LEN.WIN_DEV_CER_REPORT_COUNT // 8),),
                 default_value=DEFAULT.WIN_DEV_CER_REPORT_COUNT),
        BitField(fid=FID.WIN_DEV_CER_LOGICAL_MAXIMUM,
                 length=LEN.LONG_LOGICAL_MAXIMUM,
                 title='Windows Device Certification Logical Maximum',
                 name='win_dev_cer_logical_maximum',
                 checks=(CheckHexList(LEN.LONG_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.WIN_DEV_CER_LOGICAL_MAXIMUM),
        BitField(fid=FID.WIN_DEV_CER_VENDOR_USAGE_PAGE,
                 length=LEN.WIN_DEV_CER_VENDOR_USAGE_PAGE,
                 title='Windows Device Certification Vendor Usage Page',
                 name='win_dev_cer_vendor_usage_page',
                 checks=(CheckHexList(LEN.WIN_DEV_CER_VENDOR_USAGE_PAGE // 8),),
                 default_value=DEFAULT.WIN_DEV_CER_VENDOR_USAGE_PAGE),
        BitField(fid=FID.WIN_DEV_CER_VENDOR_USAGE,
                 length=LEN.USAGE,
                 title='Windows Device Certification Vendor Usage',
                 name='win_dev_cer_vendor_usage_page',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.WIN_DEV_CER_VENDOR_USAGE),
        BitField(fid=FID.WIN_DEV_CER_FEATURE,
                 length=LEN.INPUT_DATA,
                 title='Windows Device Certification Feature',
                 name='win_dev_cer_feature',
                 checks=(CheckHexList(ReportDescriptor.LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.FEATURE_DATA),
    )
# end class WindowsDeviceCertificationStatusFeature


class WindowsDigitizer5FingersDescriptor(ReportDescriptor):
    """
    Define the receiver windows digitizer descriptor supporting 5 fingers.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.qp9s1wvysdjz
    """
    # 413 Bytes
    BITFIELD_LENGTH = (54 + (5 * FingerCollection.BITFIELD_LENGTH) + WindowsDeviceCapabilitiesFeature.BITFIELD_LENGTH
                       + WindowsDeviceCertificationStatusFeature.BITFIELD_LENGTH)

    class FID(ReportDescriptor.FID):
        # See ``ReportDescriptor.FID``
        WIN_DIG_USAGE_PAGE = 0xFF
        WIN_DIG_USAGE = WIN_DIG_USAGE_PAGE - 1
        WIN_DIG_APP_COLLECTION = WIN_DIG_USAGE - 1
        WIN_DIG_REPORT_ID = WIN_DIG_APP_COLLECTION - 1
        WIN_DIG_FINGER_1 = WIN_DIG_REPORT_ID - 1
        WIN_DIG_FINGER_2 = WIN_DIG_FINGER_1 - 1
        WIN_DIG_FINGER_3 = WIN_DIG_FINGER_2 - 1
        WIN_DIG_FINGER_4 = WIN_DIG_FINGER_3 - 1
        WIN_DIG_FINGER_5 = WIN_DIG_FINGER_4 - 1
        WIN_DIG_CONTACT_REPORT_SIZE = WIN_DIG_FINGER_5 - 1
        WIN_DIG_CONTACT_LOGICAL_MAXIMUM = WIN_DIG_CONTACT_REPORT_SIZE - 1
        WIN_DIG_CONTACT_USAGE = WIN_DIG_CONTACT_LOGICAL_MAXIMUM - 1
        WIN_DIG_CONTACT_INPUT = WIN_DIG_CONTACT_USAGE - 1
        WIN_DIG_BUTTON_REPORT_SIZE = WIN_DIG_CONTACT_INPUT - 1
        WIN_DIG_BUTTON_LOGICAL_MAXIMUM = WIN_DIG_BUTTON_REPORT_SIZE - 1
        WIN_DIG_BUTTON_USAGE_PAGE = WIN_DIG_BUTTON_LOGICAL_MAXIMUM - 1
        WIN_DIG_BUTTON_USAGE = WIN_DIG_BUTTON_USAGE_PAGE - 1
        WIN_DIG_BUTTON_INPUT = WIN_DIG_BUTTON_USAGE - 1
        WIN_DIG_SCAN_TIME_REPORT_SIZE = WIN_DIG_BUTTON_INPUT - 1
        WIN_DIG_SCAN_TIME_LOGICAL_MAXIMUM = WIN_DIG_SCAN_TIME_REPORT_SIZE - 1
        WIN_DIG_SCAN_TIME_PHYSICAL_MAXIMUM = WIN_DIG_SCAN_TIME_LOGICAL_MAXIMUM - 1
        WIN_DIG_SCAN_TIME_EXPONENT = WIN_DIG_SCAN_TIME_PHYSICAL_MAXIMUM - 1
        WIN_DIG_SCAN_TIME_UNIT = WIN_DIG_SCAN_TIME_EXPONENT - 1
        WIN_DIG_SCAN_TIME_USAGE_PAGE = WIN_DIG_SCAN_TIME_UNIT - 1
        WIN_DIG_SCAN_TIME_USAGE = WIN_DIG_SCAN_TIME_USAGE_PAGE - 1
        WIN_DIG_SCAN_TIME_INPUT = WIN_DIG_SCAN_TIME_USAGE - 1
        WIN_DIG_UNIT = WIN_DIG_SCAN_TIME_INPUT - 1
        WIN_DIG_EXPONENT = WIN_DIG_UNIT - 1
        WIN_DIG_CAPABILITIES_FEATURE = WIN_DIG_EXPONENT - 1
        WIN_DIG_CERTIFICATION_FEATURE = WIN_DIG_CAPABILITIES_FEATURE - 1
        WIN_DIG_END_COLLECTION = WIN_DIG_CERTIFICATION_FEATURE - 1
    # end class FID

    class LEN(ReportDescriptor.LEN):
        # See ``ReportDescriptor.LEN``
        WIN_DIG_FINGER = FingerCollection.BITFIELD_LENGTH * 8
        WIN_DIG_SCAN_TIME_LOGICAL_MAXIMUM = 0x28
        WIN_DIG_SCAN_TIME_PHYSICAL_MAXIMUM = 0x28
        WIN_DIG_SCAN_TIME_UNIT = 0x18
        WIN_DIG_CAPABILITIES_FEATURE = WindowsDeviceCapabilitiesFeature.BITFIELD_LENGTH * 8
        WIN_DIG_CERTIFICATION_FEATURE = WindowsDeviceCertificationStatusFeature.BITFIELD_LENGTH * 8
    # end class LEN

    class DEFAULT(ReportDescriptor.DEFAULT):
        # See ``ReportDescriptor.DEFAULT``
        WIN_DIG_CONTACT_REPORT_SIZE = HexList("7507")
        WIN_DIG_CONTACT_LOGICAL_MAXIMUM = HexList("2505")
        WIN_DIG_BUTTON_REPORT_SIZE = HexList("7501")
        WIN_DIG_BUTTON_LOGICAL_MAXIMUM = HexList("2501")
        WIN_DIG_BUTTON_USAGE = HexList("0901")
        WIN_DIG_SCAN_TIME_REPORT_SIZE = HexList("7510")
        WIN_DIG_SCAN_TIME_LOGICAL_MAXIMUM = HexList("27FFFF0000")
        WIN_DIG_SCAN_TIME_PHYSICAL_MAXIMUM = HexList("47FFFF0000")
        WIN_DIG_SCAN_TIME_EXPONENT = HexList("550C")
        WIN_DIG_SCAN_TIME_UNIT = HexList("660110")
        WIN_DIG_UNIT = HexList("6500")
        WIN_DIG_EXPONENT = HexList("5500")
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.WIN_DIG_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Windows Digitizer Usage Page',
                 name='win_dig_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.DIGITIZER_USAGE_PAGE),
        BitField(fid=FID.WIN_DIG_USAGE,
                 length=LEN.USAGE,
                 title='Windows Digitizer Usage',
                 name='win_dig_usage',
                 aliases=('usage',),
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.TOUCHPAD_USAGE),
        BitField(fid=FID.WIN_DIG_APP_COLLECTION,
                 length=LEN.COLLECTION,
                 title='Windows Digitizer Application Collection',
                 name='win_dig_app_collection',
                 checks=(CheckHexList(LEN.COLLECTION // 8),),
                 default_value=DEFAULT.APP_COLLECTION),
        BitField(fid=FID.WIN_DIG_REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Windows Digitizer Report Id',
                 name='win_dig_report_id',
                 checks=(CheckHexList(LEN.REPORT_ID // 8),),
                 default_value=DEFAULT.WIN_DIGIT_REPORT_ID),
        BitField(fid=FID.WIN_DIG_FINGER_1,
                 length=LEN.WIN_DIG_FINGER,
                 title='Windows Digitizer Finger Collection 1',
                 name='win_dig_finger_1',
                 checks=(CheckHexList(LEN.WIN_DIG_FINGER // 8),),),
        BitField(fid=FID.WIN_DIG_FINGER_2,
                 length=LEN.WIN_DIG_FINGER,
                 title='Windows Digitizer Finger Collection 2',
                 name='win_dig_finger_2',
                 checks=(CheckHexList(LEN.WIN_DIG_FINGER // 8),),),
        BitField(fid=FID.WIN_DIG_FINGER_3,
                 length=LEN.WIN_DIG_FINGER,
                 title='Windows Digitizer Finger Collection 3',
                 name='win_dig_finger_3',
                 checks=(CheckHexList(LEN.WIN_DIG_FINGER // 8),),),
        BitField(fid=FID.WIN_DIG_FINGER_4,
                 length=LEN.WIN_DIG_FINGER,
                 title='Windows Digitizer Finger Collection 4',
                 name='win_dig_finger_4',
                 checks=(CheckHexList(LEN.WIN_DIG_FINGER // 8),),),
        BitField(fid=FID.WIN_DIG_FINGER_5,
                 length=LEN.WIN_DIG_FINGER,
                 title='Windows Digitizer Finger Collection 5',
                 name='win_dig_finger_5',
                 checks=(CheckHexList(LEN.WIN_DIG_FINGER // 8),),),
        BitField(fid=FID.WIN_DIG_CONTACT_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Windows Digitizer Report Size',
                 name='win_dig_contact_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.WIN_DIG_CONTACT_REPORT_SIZE),
        BitField(fid=FID.WIN_DIG_CONTACT_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Windows Digitizer Logical Maximum',
                 name='win_dig_contact_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.WIN_DIG_CONTACT_LOGICAL_MAXIMUM),
        BitField(fid=FID.WIN_DIG_CONTACT_USAGE,
                 length=LEN.USAGE,
                 title='Windows Digitizer Contact Count Usage',
                 name='win_dig_contact_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.CONTACT_COUNT_USAGE),
        BitField(fid=FID.WIN_DIG_CONTACT_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Windows Digitizer Contact Input Data',
                 name='win_dig_contact_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.WIN_DIG_BUTTON_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Windows Digitizer Button Report Size',
                 name='win_dig_button_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.WIN_DIG_BUTTON_REPORT_SIZE),
        BitField(fid=FID.WIN_DIG_BUTTON_LOGICAL_MAXIMUM,
                 length=LEN.LOGICAL_MAXIMUM,
                 title='Windows Digitizer Button Logical Maximum',
                 name='win_dig_button_logical_maximum',
                 checks=(CheckHexList(LEN.LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.WIN_DIG_BUTTON_LOGICAL_MAXIMUM),
        BitField(fid=FID.WIN_DIG_BUTTON_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Windows Digitizer Button Usage Page',
                 name='win_dig_button_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.BUTTON_USAGE_PAGE),
        BitField(fid=FID.WIN_DIG_BUTTON_USAGE,
                 length=LEN.USAGE,
                 title='Windows Digitizer Button Usage',
                 name='win_dig_button_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.WIN_DIG_BUTTON_USAGE),
        BitField(fid=FID.WIN_DIG_BUTTON_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Windows Digitizer Button Input Data',
                 name='win_dig_button_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.WIN_DIG_SCAN_TIME_REPORT_SIZE,
                 length=LEN.REPORT_SIZE,
                 title='Windows Digitizer Scan Time Report Size',
                 name='win_dig_scan_time_report_size',
                 checks=(CheckHexList(LEN.REPORT_SIZE // 8),),
                 default_value=DEFAULT.WIN_DIG_SCAN_TIME_REPORT_SIZE),
        BitField(fid=FID.WIN_DIG_SCAN_TIME_LOGICAL_MAXIMUM,
                 length=LEN.WIN_DIG_SCAN_TIME_LOGICAL_MAXIMUM,
                 title='Windows Digitizer Scan Time Logical Maximum',
                 name='win_dig_scan_time_logical_maximum',
                 checks=(CheckHexList(LEN.WIN_DIG_SCAN_TIME_LOGICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.WIN_DIG_SCAN_TIME_LOGICAL_MAXIMUM),
        BitField(fid=FID.WIN_DIG_SCAN_TIME_PHYSICAL_MAXIMUM,
                 length=LEN.WIN_DIG_SCAN_TIME_PHYSICAL_MAXIMUM,
                 title='Windows Digitizer Scan Time Physical Maximum',
                 name='win_dig_scan_time_physical_maximum',
                 checks=(CheckHexList(LEN.WIN_DIG_SCAN_TIME_PHYSICAL_MAXIMUM // 8),),
                 default_value=DEFAULT.WIN_DIG_SCAN_TIME_PHYSICAL_MAXIMUM),
        BitField(fid=FID.WIN_DIG_SCAN_TIME_EXPONENT,
                 length=LEN.UNIT,
                 title='Windows Digitizer Scan Time Unit Exponent',
                 name='win_dig_scan_time_exponent',
                 checks=(CheckHexList(LEN.UNIT // 8),),
                 default_value=DEFAULT.WIN_DIG_SCAN_TIME_EXPONENT),
        BitField(fid=FID.WIN_DIG_SCAN_TIME_UNIT,
                 length=LEN.WIN_DIG_SCAN_TIME_UNIT,
                 title='Windows Digitizer Scan Time Unit',
                 name='win_dig_scan_time_unit',
                 checks=(CheckHexList(LEN.WIN_DIG_SCAN_TIME_UNIT // 8),),
                 default_value=DEFAULT.WIN_DIG_SCAN_TIME_UNIT),
        BitField(fid=FID.WIN_DIG_SCAN_TIME_USAGE_PAGE,
                 length=LEN.USAGE_PAGE,
                 title='Windows Digitizer Scan Time Usage Page',
                 name='win_dig_scan_time_usage_page',
                 checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                 default_value=DEFAULT.DIGITIZER_USAGE_PAGE),
        BitField(fid=FID.WIN_DIG_SCAN_TIME_USAGE,
                 length=LEN.USAGE,
                 title='Windows Digitizer Scan Time Usage',
                 name='win_dig_scan_time_usage',
                 checks=(CheckHexList(LEN.USAGE // 8),),
                 default_value=DEFAULT.SCAN_TIME_USAGE),
        BitField(fid=FID.WIN_DIG_SCAN_TIME_INPUT,
                 length=LEN.INPUT_DATA,
                 title='Windows Digitizer Scan Time Input',
                 name='win_dig_scan_time_input',
                 checks=(CheckHexList(LEN.INPUT_DATA // 8),),
                 default_value=DEFAULT.INPUT_DATA),
        BitField(fid=FID.WIN_DIG_UNIT,
                 length=LEN.UNIT,
                 title='Windows Digitizer Unit',
                 name='win_dig_unit',
                 checks=(CheckHexList(LEN.UNIT // 8),),
                 default_value=DEFAULT.WIN_DIG_UNIT),
        BitField(fid=FID.WIN_DIG_EXPONENT,
                 length=LEN.UNIT,
                 title='Windows Digitizer Unit Exponent',
                 name='win_dig_exponent',
                 checks=(CheckHexList(LEN.UNIT // 8),),
                 default_value=DEFAULT.WIN_DIG_EXPONENT),
        BitField(fid=FID.WIN_DIG_CAPABILITIES_FEATURE,
                 length=LEN.WIN_DIG_CAPABILITIES_FEATURE,
                 title='Windows Device Capabilities Feature',
                 name='win_dig_capabilities_feature',
                 checks=(CheckHexList(LEN.WIN_DIG_CAPABILITIES_FEATURE // 8),),),
        BitField(fid=FID.WIN_DIG_CERTIFICATION_FEATURE,
                 length=LEN.WIN_DIG_CERTIFICATION_FEATURE,
                 title='Windows Device Certification Feature',
                 name='win_dig_certification_feature',
                 checks=(CheckHexList(LEN.WIN_DIG_CERTIFICATION_FEATURE // 8),),),
        BitField(fid=FID.WIN_DIG_END_COLLECTION,
                 length=LEN.END_COLLECTION,
                 title='Windows Digitizer End Collection',
                 name='win_dig_end_collection',
                 checks=(CheckHexList(LEN.END_COLLECTION // 8),),
                 default_value=DEFAULT.END_COLLECTION),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.win_dig_finger_1 = FingerCollection()
        self.win_dig_finger_2 = FingerCollection()
        self.win_dig_finger_3 = FingerCollection()
        self.win_dig_finger_4 = FingerCollection()
        self.win_dig_finger_5 = FingerCollection()
        self.win_dig_capabilities_feature = WindowsDeviceCapabilitiesFeature()
        self.win_dig_certification_feature = WindowsDeviceCertificationStatusFeature()
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        mixin = super().fromHexList(*args, **kwargs)
        mixin.win_dig_finger_1 = FingerCollection.fromHexList(mixin.win_dig_finger_1)
        mixin.win_dig_finger_2 = FingerCollection.fromHexList(mixin.win_dig_finger_2)
        mixin.win_dig_finger_3 = FingerCollection.fromHexList(mixin.win_dig_finger_3)
        mixin.win_dig_finger_4 = FingerCollection.fromHexList(mixin.win_dig_finger_4)
        mixin.win_dig_finger_5 = FingerCollection.fromHexList(mixin.win_dig_finger_5)
        mixin.win_dig_capabilities_feature = WindowsDeviceCapabilitiesFeature.fromHexList(
            mixin.win_dig_capabilities_feature)
        mixin.win_dig_certification_feature = WindowsDeviceCertificationStatusFeature.fromHexList(
            mixin.win_dig_certification_feature)
        return mixin
    # end def fromHexList
# end class WindowsDigitizer5FingersDescriptor


class WindowsDigitizer3FingersDescriptor(WindowsDigitizer5FingersDescriptor):
    """
    Define the device windows digitizer descriptor supporting 3 fingers.

    cf https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.qp9s1wvysdjz
    """
    # 279 Bytes
    BITFIELD_LENGTH = (54 + (3 * FingerCollection.BITFIELD_LENGTH) + WindowsDeviceCapabilitiesFeature.BITFIELD_LENGTH
                       + WindowsDeviceCertificationStatusFeature.BITFIELD_LENGTH)
    FIELDS = \
        WindowsDigitizer5FingersDescriptor.FIELDS[:(WindowsDigitizer5FingersDescriptor.FID.WIN_DIG_USAGE_PAGE -
                                                    WindowsDigitizer5FingersDescriptor.FID.WIN_DIG_FINGER_4)] + \
        WindowsDigitizer5FingersDescriptor.FIELDS[WindowsDigitizer5FingersDescriptor.FID.WIN_DIG_USAGE_PAGE -
                                                  WindowsDigitizer5FingersDescriptor.FID.WIN_DIG_CONTACT_REPORT_SIZE:]

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        mixin = super(WindowsDigitizer5FingersDescriptor, cls).fromHexList(*args, **kwargs)
        mixin.win_dig_finger_1 = FingerCollection.fromHexList(mixin.win_dig_finger_1)
        mixin.win_dig_finger_2 = FingerCollection.fromHexList(mixin.win_dig_finger_2)
        mixin.win_dig_finger_3 = FingerCollection.fromHexList(mixin.win_dig_finger_3)
        mixin.win_dig_capabilities_feature = WindowsDeviceCapabilitiesFeature.fromHexList(
            mixin.win_dig_capabilities_feature)
        mixin.win_dig_certification_feature = WindowsDeviceCertificationStatusFeature.fromHexList(
            mixin.win_dig_certification_feature)
        return mixin
    # end def fromHexList

# end class WindowsDigitizer3FingersDescriptor

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
