#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.devicerecovery
    :brief: HID++ 1.0 Device Recovery notification interface definition
    :author: Christophe Roquebert
    :date: 2020/03/17
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
class DeviceRecovery(Hidpp1Message):
    """
    This class defines the format of Device Recovery notification.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    NotificationCounterLsb        8
    NotificationCounterMsb        8
    Reserved                      6
    NotificationPart              2
    Data                          112
    ============================  ==========
    """
    SUB_ID = Hidpp1Data.Hidpp1NotificationSubId.DEVICE_RECOVERY

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

    class DeviceRecoveryPart0(BitFieldContainerMixin):
        """
        This class defines the Data field format of Device Recovery Part 0 notification.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ProtocolType                  8
        BluetoothPid                  16
        BluetoothAddress              48
        BleProServiceVersion          8
        UnitId                        32
        ============================  ==========
        """
        BLE_PRO_PROTOCOL_TYPE = 0x10

        class FID:
            """
            Field Identifiers
            """
            PROTOCOL_TYPE = 0xFF
            BLUETOOTH_PID = PROTOCOL_TYPE - 1
            BLUETOOTH_ADDRESS = BLUETOOTH_PID - 1
            BLE_PRO_SERVICE_VERSION = BLUETOOTH_ADDRESS - 1
            UNIT_ID = BLE_PRO_SERVICE_VERSION - 1
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            PROTOCOL_TYPE = 0x08
            BLUETOOTH_PID = 0x10
            BLUETOOTH_ADDRESS = 0x30
            BLE_PRO_SERVICE_VERSION = 0x08
            UNIT_ID = 0x20
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
            BitField(FID.BLUETOOTH_PID,
                     LEN.BLUETOOTH_PID,
                     title='BluetoothPid',
                     name='bluetooth_pid',
                     # BluetoothPid has LSB first so only HexList is checked
                     checks=(CheckHexList(LEN.BLUETOOTH_PID // 8),)),
            BitField(FID.BLUETOOTH_ADDRESS,
                     LEN.BLUETOOTH_ADDRESS,
                     title='BluetoothAddress',
                     name='bluetooth_address',
                     # BluetoothAddress has LSB first so only HexList is checked
                     checks=(CheckHexList(LEN.BLUETOOTH_ADDRESS // 8),)),
            BitField(FID.BLE_PRO_SERVICE_VERSION,
                     LEN.BLE_PRO_SERVICE_VERSION,
                     title='BLEProServiceVersion',
                     name='ble_pro_service_version',
                     checks=(CheckHexList(LEN.BLE_PRO_SERVICE_VERSION // 8),
                             CheckByte(),)),
            BitField(FID.UNIT_ID,
                     LEN.UNIT_ID,
                     title='UnitId',
                     name='unit_id',
                     checks=(CheckHexList(LEN.UNIT_ID // 8),)),
        )
    # end class DeviceRecoveryPart0

    class DeviceRecoveryPart1(BitFieldContainerMixin):
        """
        This class defines the Data field format of Device Recovery Part 1 notification.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        DeviceNameLength              8
        DeviceNameStart               104
        ============================  ==========
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
                             CheckByte(),)),
            BitField(FID.DEVICE_NAME_START,
                     LEN.DEVICE_NAME_START,
                     title='DeviceNameStart',
                     name='device_name_start',
                     checks=(CheckHexList(LEN.DEVICE_NAME_START // 8),)),
        )
    # end class DeviceRecoveryPart1

    class DeviceRecoveryPart2(BitFieldContainerMixin):
        """
        This class defines the Data field format of Device Recovery Part 2 notification.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        DeviceNameChunk               112
        ============================  ==========
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
                     checks=(CheckHexList(LEN.DEVICE_NAME_CHUNK // 8),)),
        )
    # end class DeviceRecoveryPart2

    class DeviceRecoveryPart3(DeviceRecoveryPart2):
        """
        This class defines the Data field format of Device Recovery Part 3 notification.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        DeviceNameChunk               112
        ============================  ==========
        """
    # end class DeviceRecoveryPart3

    def __init__(self, device_index, notification_counter, notification_part, data):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param notification_counter: counter (restart at 0 after each device discovery)
        :type notification_counter: ``int``
        :param notification_part: Part of the notification in range [0..3]
        :type notification_part: ``int``
        :param data: Data content
        :type data: ``HexList``
        """
        super().__init__()

        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.notification_counter = notification_counter
        self.notification_part = notification_part
        if self.notification_part == DeviceRecovery.PART.CONFIGURATION:
            self.data = DeviceRecovery.DeviceRecoveryPart0.fromHexList(data)
        elif self.notification_part == DeviceRecovery.PART.NAME_1:
            self.data = DeviceRecovery.DeviceRecoveryPart1.fromHexList(data)
        elif self.notification_part == DeviceRecovery.PART.NAME_2:
            self.data = DeviceRecovery.DeviceRecoveryPart2.fromHexList(data)
        elif self.notification_part == DeviceRecovery.PART.NAME_3:
            self.data = DeviceRecovery.DeviceRecoveryPart3.fromHexList(data)
        else:
            self.data = data
        # end if
    # end def __init__

    @property
    def notification_counter(self):
        return (int(Numeral(self.notification_counter_msb)) << 8) + int(Numeral(self.notification_counter_lsb))
    # end def property getter notification_counter

    @notification_counter.setter
    def notification_counter(self, value):
        self.notification_counter_lsb = value & 0xFF
        self.notification_counter_msb = value >> 8
    # end def property setter notification_counter

    @classmethod
    def fromHexList(cls, *args, **kwargs):                           # pylint:disable=R0912,W0613

        """
        Parsing from HexList instance

        :param \*args: List of arguments
        :type \*args: list
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict

        :return:  parsed object
        :rtype: ``FieldContainerMixin``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)

        if inner_field_container_mixin.notification_part == DeviceRecovery.PART.CONFIGURATION:
            inner_field_container_mixin.data = DeviceRecovery.DeviceRecoveryPart0.fromHexList(
                inner_field_container_mixin.data)
        elif inner_field_container_mixin.notification_part == DeviceRecovery.PART.NAME_1:
            inner_field_container_mixin.data = DeviceRecovery.DeviceRecoveryPart1.fromHexList(
                inner_field_container_mixin.data)
        elif inner_field_container_mixin.notification_part == DeviceRecovery.PART.NAME_2:
            inner_field_container_mixin.data = DeviceRecovery.DeviceRecoveryPart2.fromHexList(
                inner_field_container_mixin.data)
        elif inner_field_container_mixin.notification_part == DeviceRecovery.PART.NAME_3:
            inner_field_container_mixin.data = DeviceRecovery.DeviceRecoveryPart3.fromHexList(
                inner_field_container_mixin.data)
        # end if
        return inner_field_container_mixin
    # end def fromHexList
# end class DeviceRecovery
