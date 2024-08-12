#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.devicediscovery
    :brief: HID++ 1.0 Device Discovery event interface definition
    :author: Christophe Roquebert
    :date: 2020/03/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceDiscovery(Hidpp1Message):
    """
    This class defines the format of Device Discovery event.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || SUB ID                 || 8            ||
    || Notification counter   || 16           ||
    || Reserved               || 6            ||
    || Notification part      || 2            ||
    || Data                   || 112          ||
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.DEVICE_DISCOVERY

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        NOTIFICATION_COUNTER_LSB = Hidpp1Message.FID.SUB_ID - 1
        NOTIFICATION_COUNTER_MSB = NOTIFICATION_COUNTER_LSB - 1
        RESERVED = NOTIFICATION_COUNTER_MSB - 1
        NOTIFICATION_PART = RESERVED - 1
        DATA = NOTIFICATION_PART - 1
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        NOTIFICATION_COUNTER_LSB = 0x08
        NOTIFICATION_COUNTER_MSB = 0x08
        RESERVED = 0x06
        NOTIFICATION_PART = 0x02
        DATA = 0x70
    # end class LEN

    class DEFAULT(Hidpp1Message.DEFAULT):
        """
        Fields Default values
        """
        NOTIFICATION_COUNTER = 0x00
    # end class DEFAULT

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.NOTIFICATION_COUNTER_LSB,
                 LEN.NOTIFICATION_COUNTER_LSB,
                 title='NotificationCounterLsb',
                 name='notification_counter_lsb',
                 checks=(CheckHexList(LEN.NOTIFICATION_COUNTER_LSB // 8), CheckByte(),),
                 default_value=DEFAULT.NOTIFICATION_COUNTER),
        BitField(FID.NOTIFICATION_COUNTER_MSB,
                 LEN.NOTIFICATION_COUNTER_MSB,
                 title='NotificationCounterMsb',
                 name='notification_counter_msb',
                 checks=(CheckHexList(LEN.NOTIFICATION_COUNTER_MSB // 8), CheckByte(),),
                 default_value=DEFAULT.NOTIFICATION_COUNTER),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
        BitField(FID.NOTIFICATION_PART,
                 LEN.NOTIFICATION_PART,
                 title='NotificationPart',
                 name='notification_part',
                 checks=(CheckInt(0, pow(2, LEN.NOTIFICATION_PART) - 1),)),
        BitField(FID.DATA,
                 LEN.DATA,
                 title='Data',
                 name='data',
                 checks=(CheckHexList(LEN.DATA // 8), CheckByte()),),
    )

    class PART:
        """
        Notification Part values
        """
        CONFIGURATION = 0
        NAME_1 = 1
        NAME_2 = 2
        NAME_3 = 3
        RESERVED = 4
    # end class PART

    class DeviceDiscoveryPart0(BitFieldContainerMixin):
        """
        This class defines the format of Device Discovery Part 0 event.

        Format:
        || @b Name                || @b Bit count ||
        || Protocol Type          || 8            ||
        || Device Info reserved   || 4            ||
        || Device Type            || 4            ||
        || Bluetooth PID          || 16           ||
        || Bluetooth Address      || 48           ||
        || BLE Pro Version        || 8            ||
        || Product Specific Data  || 8            ||
        || Authentication method  || 8            ||
        || RSSI level             || 8            ||
        """
        BLE_PRO_PROTOCOL_TYPE = 0x10

        class FID:
            """
            Field Identifiers
            """
            PROTOCOL_TYPE = 0xFF
            DEVICE_INFO_RESERVED = PROTOCOL_TYPE - 1
            DEVICE_TYPE = DEVICE_INFO_RESERVED - 1
            BLUETOOTH_PID = DEVICE_TYPE - 1
            BLUETOOTH_ADDRESS = BLUETOOTH_PID - 1
            BLE_PRO_SERVICE_VERSION = BLUETOOTH_ADDRESS - 1
            PRODUCT_SPECIFIC_DATA = BLE_PRO_SERVICE_VERSION - 1
            PREPAIRING_AUTH_METHOD = PRODUCT_SPECIFIC_DATA - 1
            RESERVED_AUTH_METHOD = PREPAIRING_AUTH_METHOD - 1
            EMU_2BUTTONS_AUTH_METHOD = RESERVED_AUTH_METHOD - 1
            PASSKEY_AUTH_METHOD = EMU_2BUTTONS_AUTH_METHOD - 1
            RSSI_LEVEL = PASSKEY_AUTH_METHOD - 1
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            PROTOCOL_TYPE = 0x08
            DEVICE_INFO_RESERVED = 0x04
            DEVICE_TYPE = 0x04
            BLUETOOTH_PID = 0x10
            BLUETOOTH_ADDRESS = 0x30
            BLE_PRO_SERVICE_VERSION = 0x08
            PRODUCT_SPECIFIC_DATA = 0x08
            # Requested Authentication method
            PREPAIRING_AUTH_METHOD = 0x01
            RESERVED_AUTH_METHOD = 0x05
            EMU_2BUTTONS_AUTH_METHOD = 0x01
            PASSKEY_AUTH_METHOD = 0x01
            RSSI_LEVEL = 0x08
        # end class LEN

        class DEFAULT:
            """
            Field default value
            """
            RESERVED = 0x00
            PROTOCOL_TYPE = 0x10
        # end class DEFAULT

        FIELDS = (
            BitField(FID.PROTOCOL_TYPE,
                     LEN.PROTOCOL_TYPE,
                     title='ProtocolType',
                     name='protocol_type',
                     checks=(CheckHexList(LEN.PROTOCOL_TYPE // 8),
                             CheckByte(),),
                     default_value=DEFAULT.PROTOCOL_TYPE),
            BitField(FID.DEVICE_INFO_RESERVED,
                     LEN.DEVICE_INFO_RESERVED,
                     title='DeviceInfoReserved',
                     name='device_info_reserved',
                     default_value=DEFAULT.RESERVED,
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_INFO_RESERVED) - 1),), ),
            BitField(FID.DEVICE_TYPE,
                     LEN.DEVICE_TYPE,
                     title='DeviceType',
                     name='device_type',
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_TYPE) - 1),), ),
            BitField(FID.BLUETOOTH_PID,
                     LEN.BLUETOOTH_PID,
                     title='BluetoothPid',
                     name='bluetooth_pid',
                     checks=(CheckHexList(LEN.BLUETOOTH_PID // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.BLUETOOTH_PID) - 1),), ),
            BitField(FID.BLUETOOTH_ADDRESS,
                     LEN.BLUETOOTH_ADDRESS,
                     title='BluetoothAddress',
                     name='bluetooth_address',
                     checks=(CheckHexList(LEN.BLUETOOTH_ADDRESS // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.BLUETOOTH_ADDRESS) - 1),), ),
            BitField(FID.BLE_PRO_SERVICE_VERSION,
                     LEN.BLE_PRO_SERVICE_VERSION,
                     title='BLEProServiceVersion',
                     name='ble_pro_service_version',
                     checks=(CheckHexList(LEN.BLE_PRO_SERVICE_VERSION // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.BLE_PRO_SERVICE_VERSION) - 1),), ),
            BitField(FID.PRODUCT_SPECIFIC_DATA,
                     LEN.PRODUCT_SPECIFIC_DATA,
                     title='ProductSpecificData',
                     name='product_specific_data',
                     aliases=('extended_model_id',),
                     checks=(CheckHexList(LEN.PRODUCT_SPECIFIC_DATA // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_SPECIFIC_DATA) - 1),), ),
            BitField(FID.PREPAIRING_AUTH_METHOD,
                     LEN.PREPAIRING_AUTH_METHOD,
                     title='PrepairingAuthMethod',
                     name='prepairing_auth_method',
                     checks=(CheckHexList(LEN.PREPAIRING_AUTH_METHOD // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.PREPAIRING_AUTH_METHOD) - 1),),
                     default_value=0),
            BitField(FID.RESERVED_AUTH_METHOD,
                     LEN.RESERVED_AUTH_METHOD,
                     title='ReservedAuthMethod',
                     name='reserved_auth_method',
                     checks=(CheckHexList(LEN.RESERVED_AUTH_METHOD // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED_AUTH_METHOD) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(FID.EMU_2BUTTONS_AUTH_METHOD,
                     LEN.EMU_2BUTTONS_AUTH_METHOD,
                     title='Emu2ButtonsAuthMethod',
                     name='emu_2buttons_auth_method',
                     checks=(CheckHexList(LEN.EMU_2BUTTONS_AUTH_METHOD // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.EMU_2BUTTONS_AUTH_METHOD) - 1),),
                     default_value=0),
            BitField(FID.PASSKEY_AUTH_METHOD,
                     LEN.PASSKEY_AUTH_METHOD,
                     title='PassKeyAuthMethod',
                     name='passkey_auth_method',
                     checks=(CheckHexList(LEN.PASSKEY_AUTH_METHOD // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.PASSKEY_AUTH_METHOD) - 1),),
                     default_value=0),
            BitField(FID.RSSI_LEVEL,
                     LEN.RSSI_LEVEL,
                     title='RSSILevel',
                     name='rssi_level',
                     checks=(CheckHexList(LEN.RSSI_LEVEL // 8), CheckByte(),),),
        )
    # end class DeviceDiscoveryPart0

    class DeviceDiscoveryPart1(BitFieldContainerMixin):
        """
        This class defines the format of Device Discovery Part 1 event.

        Format:
        || @b Name                || @b Bit count ||
        || Device Name length     || 8            ||
        || Device Name start      || 104          ||
        """

        class FID:
            """
            Field Identifiers
            """
            DEVICE_NAME_LENGTH = 0xFF
            DEVICE_NAME_START = DEVICE_NAME_LENGTH - 1

        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            DEVICE_NAME_LENGTH = 0x08
            DEVICE_NAME_START = 0x68

        # end class LEN

        FIELDS = (
            BitField(FID.DEVICE_NAME_LENGTH,
                     LEN.DEVICE_NAME_LENGTH,
                     title='DeviceNameLength',
                     name='device_name_length',
                     checks=(CheckHexList(LEN.DEVICE_NAME_LENGTH // 8),
                             CheckByte(),), ),
            BitField(FID.DEVICE_NAME_START,
                     LEN.DEVICE_NAME_START,
                     title='DeviceNameStart',
                     name='device_name_start',
                     checks=(CheckHexList(LEN.DEVICE_NAME_START // 8),),
                     )
        )
    # end class DeviceDiscoveryPart1

    class DeviceDiscoveryPart2(BitFieldContainerMixin):
        """
        This class defines the format of Device Discovery Part 2 event.

        Format:
        || @b Name                || @b Bit count ||
        || Device Name Chunk      || 112          ||
        """

        class FID:
            """
            Field Identifiers
            """
            DEVICE_NAME_CHUNK = 0xFF
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            DEVICE_NAME_CHUNK = 0x70
        # end class LEN

        FIELDS = (
            BitField(FID.DEVICE_NAME_CHUNK,
                     LEN.DEVICE_NAME_CHUNK,
                     title='DeviceNameChunk',
                     name='device_name_chunk',
                     checks=(CheckHexList(LEN.DEVICE_NAME_CHUNK // 8),),
                     ),
        )
    # end class DeviceDiscoveryPart2

    class DeviceDiscoveryPart3(DeviceDiscoveryPart2):
        """
        This class defines the format of Device Discovery Part 3 event.

        Format:
        || @b Name                || @b Bit count ||
        || Device Name Chunk      || 112          ||
        """
    # end class DeviceDiscoveryPart3

    def __init__(self, device_index, notification_counter, notification_part, data):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param notification_counter: counter (restart at 0 after each device discovery)
        :type notification_counter: ``int``
        :param notification_part: Part of the notification in range [0..3]
        :type notification_part: ``int``
        :param data: Data content
        :type data: ``HexList | DeviceDiscovery.DeviceDiscoveryPart0 | DeviceDiscovery.DeviceDiscoveryPart1 |
                    DeviceDiscovery.DeviceDiscoveryPart2 | DeviceDiscovery.DeviceDiscoveryPart3``
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.notification_counter = notification_counter
        self.notification_counter_lsb = notification_counter & 0xFF
        self.notification_counter_msb = notification_counter >> 8
        self.notification_part = notification_part
        if self.notification_part == DeviceDiscovery.PART.CONFIGURATION:
            self.data = DeviceDiscovery.DeviceDiscoveryPart0.fromHexList(data)
        elif self.notification_part == DeviceDiscovery.PART.NAME_1:
            self.data = DeviceDiscovery.DeviceDiscoveryPart1.fromHexList(data)
        elif self.notification_part == DeviceDiscovery.PART.NAME_2:
            self.data = DeviceDiscovery.DeviceDiscoveryPart2.fromHexList(data)
        elif self.notification_part == DeviceDiscovery.PART.NAME_3:
            self.data = DeviceDiscovery.DeviceDiscoveryPart3.fromHexList(data)
        else:
            self.data = data
        # end if
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):                              # pylint:disable=R0912,W0613
        """
        Parsing from HexList instance

        :param args: Positional arguments.
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``

        :return:  parsed object
        :rtype: ``FieldContainerMixin``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)

        inner_field_container_mixin.notification_counter = (
            int(Numeral(inner_field_container_mixin.notification_counter_msb)) << 8) + \
            int(Numeral(inner_field_container_mixin.notification_counter_lsb))

        if inner_field_container_mixin.notification_part == DeviceDiscovery.PART.CONFIGURATION:
            inner_field_container_mixin.data = DeviceDiscovery.DeviceDiscoveryPart0.fromHexList(
                inner_field_container_mixin.data)
        elif inner_field_container_mixin.notification_part == DeviceDiscovery.PART.NAME_1:
            inner_field_container_mixin.data = DeviceDiscovery.DeviceDiscoveryPart1.fromHexList(
                inner_field_container_mixin.data)
        elif inner_field_container_mixin.notification_part == DeviceDiscovery.PART.NAME_2:
            inner_field_container_mixin.data = DeviceDiscovery.DeviceDiscoveryPart2.fromHexList(
                inner_field_container_mixin.data)
        elif inner_field_container_mixin.notification_part == DeviceDiscovery.PART.NAME_3:
            inner_field_container_mixin.data = DeviceDiscovery.DeviceDiscoveryPart3.fromHexList(
                inner_field_container_mixin.data)
        # end if
        return inner_field_container_mixin
# end class DeviceDiscovery
