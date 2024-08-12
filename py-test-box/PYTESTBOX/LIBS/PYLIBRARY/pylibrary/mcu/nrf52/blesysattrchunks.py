#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.nrf52.blenvschunks
:brief: NVS BLE System Attribute chunk definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/09/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import abc
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceBleUserServices(BitFieldContainerMixin, metaclass=abc.ABCMeta):  # pylint:disable=W0223
    """
    Define the format of the NVS_BLE_SYS_ATTR_USR_SRVCS_ID chunk

    typedef struct
    {
        uint32_t sys_cccd_bitfield;                     /**< CCCD BitField (NOTE: Size is 32 bits just to make struct size dividable by 4). */
        uint32_t sys_gatt_table_version;                /**< GATT table version for DFU purpose. */
        uint32_t sys_attr_len;                          /**< System attribute data size. */
        uint8_t  sys_attr[SYS_ATTR_USR_SRVCS_MAX_LEN];  /**< System attribute data. */
    } sys_attr_usr_srvcs_t;
    """

    class ReportingCapabilities(BitFieldContainerMixin):
        """
        Reporting capabilities, device specific

        Format:

        ============================    ==========
        Name                            Bit count
        ============================    ==========
        HoG call state report           1
        HoG power report                1
        HoG consumer control report     1
        (minimal)
        HoG consumer control report     1
        (generic)
        HoG mouse report                1
        HoG battery report              1
        HoG keyboard report             1
        BAS battery notification        1
        Reserved                        3
        HoG gamepad report              1
        BLE++ long                      1
        BLE++ short                     1
        HoG HID++ long                  1
        HoG HID++ short                 1
        ============================    ==========
        """
        class FID:
            """
            Field identifiers
            """
            HOG_CALL_STATE_REPORT = 0x0FF
            HOG_POWER_REPORT = HOG_CALL_STATE_REPORT - 1
            HOG_CONS_MIN_REPORT = HOG_POWER_REPORT - 1
            HOG_CONS_GEN_REPORT = HOG_CONS_MIN_REPORT - 1
            HOG_MOUSE_REPORT = HOG_CONS_GEN_REPORT - 1
            HOG_BATTERY_REPORT = HOG_MOUSE_REPORT - 1
            HOG_KEYBOARD_REPORT = HOG_BATTERY_REPORT - 1
            BAS_BATTERY_NOTIFICATION = HOG_KEYBOARD_REPORT - 1
            RESERVED = BAS_BATTERY_NOTIFICATION - 1
            HOG_GAMEPAD_REPORT = RESERVED - 1
            BLEPP_LONG_REPORT = HOG_GAMEPAD_REPORT - 1
            BLEPP_SHORT_REPORT = BLEPP_LONG_REPORT - 1
            HOG_HIDPP_LONG_REPORT = BLEPP_SHORT_REPORT - 1
            HOG_HIDPP_SHORT_REPORT = HOG_HIDPP_LONG_REPORT - 1
            PADDING = HOG_HIDPP_SHORT_REPORT - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            HOG_CALL_STATE_REPORT = 1
            HOG_POWER_REPORT = 1
            HOG_CONS_MIN_REPORT = 1
            HOG_CONS_GEN_REPORT = 1
            HOG_MOUSE_REPORT = 1
            HOG_BATTERY_REPORT = 1
            HOG_KEYBOARD_REPORT = 1
            BAS_BATTERY_NOTIFICATION = 1
            RESERVED = 3
            HOG_GAMEPAD_REPORT = 1
            BLEPP_LONG_REPORT = 1
            BLEPP_SHORT_REPORT = 1
            HOG_HIDPP_LONG_REPORT = 1
            HOG_HIDPP_SHORT_REPORT = 1
            PADDING = 0x10
        # end class LEN

        class DEFAULT:
            """
            Field default values
            """
            RESERVED = 0
            NOT_SUPPORTED = 0
            SUPPORTED = 1
            PADDING = 0
        # end class DEFAULT

        FIELDS = (
            BitField(FID.HOG_CALL_STATE_REPORT,
                     LEN.HOG_CALL_STATE_REPORT,
                     title='HoG call state report',
                     name='hog_call_state_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_CALL_STATE_REPORT) - 1),)),
            BitField(FID.HOG_POWER_REPORT,
                     LEN.HOG_POWER_REPORT,
                     title='HoG power report',
                     name='hog_power_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_POWER_REPORT) - 1),)),
            BitField(FID.HOG_CONS_MIN_REPORT,
                     LEN.HOG_CONS_MIN_REPORT,
                     title='HoG consumer control report (minimal)',
                     name='hog_cons_min_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_CONS_MIN_REPORT) - 1),)),
            BitField(FID.HOG_CONS_GEN_REPORT,
                     LEN.HOG_CONS_GEN_REPORT,
                     title='HoG consumer control report (generic)',
                     name='hog_cons_gen_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_CONS_GEN_REPORT) - 1),)),
            BitField(FID.HOG_MOUSE_REPORT,
                     LEN.HOG_MOUSE_REPORT,
                     title='HoG mouse report',
                     name='hog_mouse_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_MOUSE_REPORT) - 1),)),
            BitField(FID.HOG_BATTERY_REPORT,
                     LEN.HOG_BATTERY_REPORT,
                     title='HoG battery report',
                     name='hog_battery_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_BATTERY_REPORT) - 1),)),
            BitField(FID.HOG_KEYBOARD_REPORT,
                     LEN.HOG_KEYBOARD_REPORT,
                     title='HoG keyboard report',
                     name='hog_keyboard_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_KEYBOARD_REPORT) - 1),)),
            BitField(FID.BAS_BATTERY_NOTIFICATION,
                     LEN.BAS_BATTERY_NOTIFICATION,
                     title='BAS battery notification',
                     name='bas_battery_notification',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.BAS_BATTERY_NOTIFICATION) - 1),)),
            BitField(FID.RESERVED,
                     LEN.RESERVED,
                     title='Reserved',
                     name='reserved',
                     default_value=DEFAULT.RESERVED,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
            BitField(FID.HOG_GAMEPAD_REPORT,
                     LEN.HOG_GAMEPAD_REPORT,
                     title='HoG gamepad report',
                     name='hog_gamepad_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_GAMEPAD_REPORT) - 1),)),
            BitField(FID.BLEPP_LONG_REPORT,
                     LEN.BLEPP_LONG_REPORT,
                     title='BLE++ long report',
                     name='blepp_long_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.BLEPP_LONG_REPORT) - 1),)),
            BitField(FID.BLEPP_SHORT_REPORT,
                     LEN.BLEPP_SHORT_REPORT,
                     title='BLE++ short report',
                     name='blepp_short_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.BLEPP_SHORT_REPORT) - 1),)),
            BitField(FID.HOG_HIDPP_LONG_REPORT,
                     LEN.HOG_HIDPP_LONG_REPORT,
                     title='HoG HID++ long report',
                     name='hog_hidpp_long_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_HIDPP_LONG_REPORT) - 1),)),
            BitField(FID.HOG_HIDPP_SHORT_REPORT,
                     LEN.HOG_HIDPP_SHORT_REPORT,
                     title='HoG HID++ short report',
                     name='hog_hidpp_short_report',
                     default_value=DEFAULT.NOT_SUPPORTED,
                     checks=(CheckInt(0, pow(2, LEN.HOG_HIDPP_SHORT_REPORT) - 1),)),
            BitField(fid=FID.PADDING,
                     length=LEN.PADDING,
                     default_value=DEFAULT.PADDING,
                     title='Padding',
                     name='padding',
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),)),
        )
    # end class ReportingCapabilities

    class SystemAttribute(BitFieldContainerMixin):
        """
        System attribute data (user services)

        Format:

        ============================    ==========
        Name                            Bit count
        ============================    ==========
        Characteristic Descriptor 0     0 or 48
        Characteristic Descriptor 1     0 or 48
        Characteristic Descriptor 2     0 or 48
        Characteristic Descriptor 3     0 or 48
        Characteristic Descriptor 4     0 or 48
        Characteristic Descriptor 5     0 or 48
        Characteristic Descriptor 6     0 or 48
        Characteristic Descriptor 7     0 or 48
        Characteristic Descriptor 8     0 or 48
        Characteristic Descriptor 9     0 or 48
        Characteristic Descriptor 10    0 or 48
        Characteristic Descriptor 11    0 or 48
        Characteristic Descriptor 12    0 or 48
        Characteristic Descriptor 13    0 or 48
        Characteristic Descriptor 14    0 or 48
        CRC-16-CCITT                    16
        ============================    ==========
        """
        class FID:
            """
            Field identifiers
            """
            CHARACTERISTIC_DESC_0 = 0xFF
            CHARACTERISTIC_DESC_1 = CHARACTERISTIC_DESC_0 - 1
            CHARACTERISTIC_DESC_2 = CHARACTERISTIC_DESC_1 - 1
            CHARACTERISTIC_DESC_3 = CHARACTERISTIC_DESC_2 - 1
            CHARACTERISTIC_DESC_4 = CHARACTERISTIC_DESC_3 - 1
            CHARACTERISTIC_DESC_5 = CHARACTERISTIC_DESC_4 - 1
            CHARACTERISTIC_DESC_6 = CHARACTERISTIC_DESC_5 - 1
            CHARACTERISTIC_DESC_7 = CHARACTERISTIC_DESC_6 - 1
            CHARACTERISTIC_DESC_8 = CHARACTERISTIC_DESC_7 - 1
            CHARACTERISTIC_DESC_9 = CHARACTERISTIC_DESC_8 - 1
            CHARACTERISTIC_DESC_10 = CHARACTERISTIC_DESC_9 - 1
            CHARACTERISTIC_DESC_11 = CHARACTERISTIC_DESC_10 - 1
            CHARACTERISTIC_DESC_12 = CHARACTERISTIC_DESC_11 - 1
            CHARACTERISTIC_DESC_13 = CHARACTERISTIC_DESC_12 - 1
            CHARACTERISTIC_DESC_14 = CHARACTERISTIC_DESC_13 - 1
            CRC = CHARACTERISTIC_DESC_14 - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            CCCD_SUPPORTED = 0x30
            CCCD_NOT_SUPPORTED = 0x00
            CRC = 0x10
        # end class LEN

        FIELDS = (
            BitField(
                fid=FID.CHARACTERISTIC_DESC_0,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 0',
                name='characteristic_desc_0',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_1,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 1',
                name='characteristic_desc_1',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_2,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 2',
                name='characteristic_desc_2',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_3,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 3',
                name='characteristic_desc_3',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_4,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 4',
                name='characteristic_desc_4',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_5,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 5',
                name='characteristic_desc_5',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_6,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 6',
                name='characteristic_desc_6',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_7,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 7',
                name='characteristic_desc_7',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_8,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 8',
                name='characteristic_desc_8',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_9,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 9',
                name='characteristic_desc_9',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_10,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 10',
                name='characteristic_desc_10',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_11,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 11',
                name='characteristic_desc_11',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_12,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 12',
                name='characteristic_desc_12',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_13,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 13',
                name='characteristic_desc_13',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CHARACTERISTIC_DESC_14,
                length=LEN.CCCD_SUPPORTED,
                title='Client Characteristic Configuration Descriptor 14',
                name='characteristic_desc_14',
                checks=(CheckHexList(max_length=(LEN.CCCD_SUPPORTED // 8),
                                     min_length=(LEN.CCCD_NOT_SUPPORTED // 8), ),)),
            BitField(
                fid=FID.CRC,
                length=LEN.CRC,
                title='CRC-16-CCITT',
                name='crc',
                checks=(CheckHexList(LEN.CRC // 8),),),
        )

        def __init__(self, crc, characteristic_desc_0=None, characteristic_desc_1=None, characteristic_desc_2=None,
                     characteristic_desc_3=None, characteristic_desc_4=None, characteristic_desc_5=None,
                     characteristic_desc_6=None, characteristic_desc_7=None, characteristic_desc_8=None,
                     characteristic_desc_9=None, characteristic_desc_10=None, characteristic_desc_11=None,
                     characteristic_desc_12=None, characteristic_desc_13=None, characteristic_desc_14=None,
                     **kwargs):
            """
            :param characteristic_desc_0: Client Characteristic Configuration Descriptor 15
            :type characteristic_desc_0: ``HexList`` or ``None``
            :param characteristic_desc_1: Client Characteristic Configuration Descriptor 1
            :type characteristic_desc_1: ``HexList`` or ``None``
            :param characteristic_desc_2: Client Characteristic Configuration Descriptor 2
            :type characteristic_desc_2: ``HexList`` or ``None``
            :param characteristic_desc_3: Client Characteristic Configuration Descriptor 3
            :type characteristic_desc_3: ``HexList`` or ``None``
            :param characteristic_desc_4: Client Characteristic Configuration Descriptor 4
            :type characteristic_desc_4: ``HexList`` or ``None``
            :param characteristic_desc_5: Client Characteristic Configuration Descriptor 5
            :type characteristic_desc_5: ``HexList`` or ``None``
            :param characteristic_desc_6: Client Characteristic Configuration Descriptor 6
            :type characteristic_desc_6: ``HexList`` or ``None``
            :param characteristic_desc_7: Client Characteristic Configuration Descriptor 7
            :type characteristic_desc_7: ``HexList`` or ``None``
            :param characteristic_desc_8: Client Characteristic Configuration Descriptor 8
            :type characteristic_desc_8: ``HexList`` or ``None``
            :param characteristic_desc_9: Client Characteristic Configuration Descriptor 9
            :type characteristic_desc_9: ``HexList`` or ``None``
            :param characteristic_desc_10: Client Characteristic Configuration Descriptor 10
            :type characteristic_desc_10: ``HexList`` or ``None``
            :param characteristic_desc_11: Client Characteristic Configuration Descriptor 11
            :type characteristic_desc_11: ``HexList`` or ``None``
            :param characteristic_desc_12: Client Characteristic Configuration Descriptor 12
            :type characteristic_desc_12: ``HexList`` or ``None``
            :param characteristic_desc_13: Client Characteristic Configuration Descriptor 13
            :type characteristic_desc_13: ``HexList`` or ``None``
            :param characteristic_desc_14: Client Characteristic Configuration Descriptor 14
            :type characteristic_desc_14: ``HexList`` or ``None``
            :param crc: CRC-16-CCITT
            :type crc: ``HexList``
            :param kwargs: Potential future parameters
            :type kwargs: ``dict``
            """
            super().__init__(**kwargs)

            # Parameters initialization
            self.characteristic_desc_0 = characteristic_desc_0 if characteristic_desc_0 is not None else HexList()
            self.characteristic_desc_1 = characteristic_desc_1 if characteristic_desc_1 is not None else HexList()
            self.characteristic_desc_2 = characteristic_desc_2 if characteristic_desc_2 is not None else HexList()
            self.characteristic_desc_3 = characteristic_desc_3 if characteristic_desc_3 is not None else HexList()
            self.characteristic_desc_4 = characteristic_desc_4 if characteristic_desc_4 is not None else HexList()
            self.characteristic_desc_5 = characteristic_desc_5 if characteristic_desc_5 is not None else HexList()
            self.characteristic_desc_6 = characteristic_desc_6 if characteristic_desc_6 is not None else HexList()
            self.characteristic_desc_7 = characteristic_desc_7 if characteristic_desc_7 is not None else HexList()
            self.characteristic_desc_8 = characteristic_desc_8 if characteristic_desc_8 is not None else HexList()
            self.characteristic_desc_9 = characteristic_desc_9 if characteristic_desc_9 is not None else HexList()
            self.characteristic_desc_10 = characteristic_desc_10 if characteristic_desc_10 is not None else HexList()
            self.characteristic_desc_11 = characteristic_desc_11 if characteristic_desc_11 is not None else HexList()
            self.characteristic_desc_12 = characteristic_desc_12 if characteristic_desc_12 is not None else HexList()
            self.characteristic_desc_13 = characteristic_desc_13 if characteristic_desc_13 is not None else HexList()
            self.characteristic_desc_14 = characteristic_desc_14 if characteristic_desc_14 is not None else HexList()
            self.crc = crc
        # end def __init__
    # end class SystemAttribute

    class CCCD(BitFieldContainerMixin):
        """
        Client Characteristic Configuration Descriptor (CCCD)

        Format:

        ============================    ==========
        Name                            Bit count
        ============================    ==========
        CCCD handle                     16
        CCCD length                     16
        CCCD data                       16
        ============================    ==========
        """
        class FID:
            """
            Field identifiers
            """
            CCCD_HANDLE = 0x0FF
            CCCD_LENGTH = CCCD_HANDLE - 1
            CCCD_DATA = CCCD_LENGTH - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            CCCD_HANDLE = 0x10
            CCCD_LENGTH = 0x10
            CCCD_DATA = 0x10
            DATA = CCCD_HANDLE + CCCD_LENGTH + CCCD_DATA
        # end class LEN

        class NOTIFICATION:
            """
            CCCD data possible values
            """
            DISABLED = 0
            ENABLED = 1
        # end class NOTIFICATION

        FIELDS = (
            BitField(FID.CCCD_HANDLE,
                     LEN.CCCD_HANDLE,
                     title='CCCD handle (Little Endian)',
                     name='little_endian_cccd_handle',
                     checks=(CheckHexList(LEN.CCCD_HANDLE // 8),), ),
            BitField(FID.CCCD_LENGTH,
                     LEN.CCCD_LENGTH,
                     title='CCCD length (Little Endian)',
                     name='cccd_length',
                     checks=(CheckHexList(LEN.CCCD_LENGTH // 8),), ),
            BitField(FID.CCCD_DATA,
                     LEN.CCCD_DATA,
                     title='CCCD data (Little Endian)',
                     name='little_endian_cccd_data',
                     checks=(CheckHexList(LEN.CCCD_DATA // 8),), ),
        )

        def __init__(self, cccd_handle, cccd_data, **kwargs):
            """
            :param cccd_handle: CCCD handle
            :type cccd_handle: ``HexList``
            :param cccd_data: CCCD data
            :type cccd_data: ``HexList``
            :param kwargs: Potential future parameters
            :type kwargs: ``dict``
            """
            super().__init__(**kwargs)

            # Parameters initialization
            self.cccd_handle = cccd_handle
            self.cccd_length = HexList('0002')[::-1]
            self.cccd_data = cccd_data
        # end def __init__

        @property
        def cccd_handle(self):
            """
            Convert to big endian

            :return: CCCD handle value in big endian
            :rtype: ``HexList``
            """
            return self.little_endian_cccd_handle[::-1]

        # end getter def cccd_handle

        @cccd_handle.setter
        def cccd_handle(self, value):
            """
            Convert value to little endian

            :param value: CCCD handle value in big endian
            :type value: ``HexList``
            """
            self.little_endian_cccd_handle = value[::-1]
        # end setter def cccd_handle

        @property
        def cccd_data(self):
            """
            Convert to big endian

            :return: CCCD data value in big endian
            :rtype: ``HexList``
            """
            return self.little_endian_cccd_data[::-1]

        # end getter def cccd_data

        @cccd_data.setter
        def cccd_data(self, value):
            """
            Convert value to little endian

            :param value: CCCD data value in big endian
            :type value: ``HexList``
            """
            self.little_endian_cccd_data = value[::-1]
        # end setter def cccd_data
    # end class CCCD

    class LEN:
        """
        Field Lengths in bits
        """
        REPORTING_BITFIELD = 0x20
        GATT_TABLE_VERSION = 0x20
        SYSTEM_ATTRIBUTE_LENGTH = 0x20
        # System attribute data (user services) length in range [ 8 ..
        SYSTEM_ATTRIBUTE_DATA_MIN = 0x40  # 6 * 1 + 2 bytes
        SYSTEM_ATTRIBUTE_DATA_MAX = 0x2E0  # 6 * 15 + 2 bytes
        CRC = 0x10
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        REPORTING_BITFIELD = 0xFF
        GATT_TABLE_VERSION = REPORTING_BITFIELD - 1
        SYSTEM_ATTRIBUTE_LENGTH = GATT_TABLE_VERSION - 1
        SYSTEM_ATTRIBUTE_DATA = SYSTEM_ATTRIBUTE_LENGTH - 1
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.REPORTING_BITFIELD,
            length=LEN.REPORTING_BITFIELD,
            title='Reporting Bitfield',
            name='reporting_bitfield',
            checks=(CheckHexList(LEN.REPORTING_BITFIELD // 8),),),
        BitField(
            fid=FID.GATT_TABLE_VERSION,
            length=LEN.GATT_TABLE_VERSION,
            title='GATT Table Version (Little endian)',
            name='little_endian_gatt_table_version',
            checks=(CheckHexList(LEN.GATT_TABLE_VERSION // 8),),),
        BitField(
            fid=FID.SYSTEM_ATTRIBUTE_LENGTH,
            length=LEN.SYSTEM_ATTRIBUTE_LENGTH,
            title='System Attribute Length  (Little endian)',
            name='little_endian_system_attribute_length',
            checks=(CheckHexList(LEN.SYSTEM_ATTRIBUTE_LENGTH // 8),),),
        BitField(
            fid=FID.SYSTEM_ATTRIBUTE_DATA,
            length=LEN.SYSTEM_ATTRIBUTE_DATA_MAX,
            title='System Attribute Data',
            name='system_attribute_data',
            checks=(CheckHexList(max_length=(LEN.SYSTEM_ATTRIBUTE_DATA_MAX // 8),
                                 min_length=(LEN.SYSTEM_ATTRIBUTE_DATA_MIN // 8), ),)),
    )

    def __init__(self, reporting_bitfield, gatt_table_version, system_attribute_length, system_attribute_data,
                 ref=None, **kwargs):
        """
        :param reporting_bitfield: Reporting capabilities, device specific
        :type reporting_bitfield: ``HexList``
        :param gatt_table_version: GATT table version
        :type gatt_table_version: ``HexList``
        :param system_attribute_length: System attribute data length (user services)
        :type system_attribute_length: ``HexList``
        :param system_attribute_data: System attribute data (user services)
        :type system_attribute_data: ``HexList`` or ``SystemAttribute``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.reporting_bitfield = reporting_bitfield
        self.gatt_table_version = gatt_table_version
        self.system_attribute_length = system_attribute_length
        self.system_attribute_data = system_attribute_data
    # end def __init__

    @property
    def gatt_table_version(self):
        """
        Convert to big endian

        :return: GATT Table Version value in big endian
        :rtype: ``HexList``
        """
        return self.little_endian_gatt_table_version[::-1]
    # end getter def gatt_table_version

    @gatt_table_version.setter
    def gatt_table_version(self, value):
        """
        Convert value to little endian

        :param value: GATT Table Version value in big endian
        :type value: ``HexList``
        """
        self.little_endian_gatt_table_version = value[::-1]
    # end setter def gatt_table_version

    @property
    def system_attribute_length(self):
        """
        Convert to big endian

        :return: System Attribute Length value in big endian
        :rtype: ``HexList``
        """
        return self.little_endian_system_attribute_length[::-1]
    # end getter def system_attribute_length

    @system_attribute_length.setter
    def system_attribute_length(self, value):
        """
        Convert value to little endian

        :param value: System Attribute Length value in big endian
        :type value: ``HexList``
        """
        self.little_endian_system_attribute_length = value[::-1]
    # end setter def system_attribute_length

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``DeviceBleUserServices``
        """
        mixin = super().fromHexList(*args, **kwargs)
        mixin.reporting_bitfield = cls.ReportingCapabilities.fromHexList(mixin.reporting_bitfield)
        size = cls.CCCD.LEN.DATA // 8
        characteristics_count = to_int(mixin.system_attribute_length) // size
        data = cls.SystemAttribute(crc=mixin.system_attribute_data[-2:])
        for index in range(characteristics_count):
            data.setValue(data.getFidFromName(f'characteristic_desc_{index}'), cls.CCCD.fromHexList(
                mixin.system_attribute_data[index * size:(index+1) * size]))
        # end for
        mixin.system_attribute_data = data
        return mixin
    # end def fromHexList

    def is_all_cccd_disabled(self):
        """
        Check whether all supported CCCD are disabled

        :return: Flag indicating whether all supported CCCD are disabled
        :rtype: ``bool``
        """
        characteristics_count = to_int(self.system_attribute_length) // (self.CCCD.LEN.DATA // 8)
        for index in range(characteristics_count):
            descriptor = self.system_attribute_data.getValue(
                self.system_attribute_data.getFidFromName(f'characteristic_desc_{index}'))
            if to_int(descriptor.cccd_data) != self.CCCD.NOTIFICATION.DISABLED:
                return False
            # end if
        # end for
        return True
    # end def is_all_cccd_disabled
# end class DeviceBleUserServices

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
