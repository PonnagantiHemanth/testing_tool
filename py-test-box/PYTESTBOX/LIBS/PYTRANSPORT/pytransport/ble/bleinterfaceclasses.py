#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.ble.bleinterfaceclasses
:brief: BLE interface classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import Enum
from enum import auto
from statistics import mean
from struct import pack
from struct import unpack
from threading import RLock
from typing import List

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pylibrary.system.tracelogger import TIMESTAMP_UNIT_DIVIDER_MAP
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pytransport.ble.bleconstants import BleAdvertisingDataType
from pytransport.ble.bleconstants import BleAdvertisingPduType
from pytransport.ble.bleconstants import BleGapAddressType
from pytransport.ble.bleconstants import BleGenericIntConstant
from pytransport.ble.bleconstants import BleUuid128bits
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardDeclaration
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.bleconstants import BleUuidStandardService


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleGapAddress:
    """
    Structure representing a BLE GAP address.
    """

    def __init__(self, address_type, address):
        """
        :param address_type: Address types, should be in enumeration BleGapAddressType
        :type address_type: ``BleGapAddressType`` or ``int``
        :param address: String representation of the 6 bytes long BLE address of the device in big endian
        :type address: ``str``
        """
        assert address_type in BleGapAddressType, \
            f"address_type should be in BleGapAddressType, {address_type} is not"
        assert isinstance(address, str) and len(address) == BleGenericIntConstant.BLE_ADDRESS_LENGTH*2, \
            f"address should be a string of length 12 (representation of the 6 bytes), {address} is not"

        if isinstance(address_type, int):
            address_type = BleGapAddressType(address_type)
        # end if

        self.address_type = address_type
        self.address = address
    # end def __init__

    def __str__(self):
        return f"{type(self).__name__}(address_type({self.address_type.name}, {self.address_type.value}), " \
               f"address({self.address}))"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def __eq__(self, other):
        if not isinstance(other, BleGapAddress):
            return False
        # end if
        return self.address_type == other.address_type and self.address == other.address
    # end def __eq__

    def __hash__(self):
        # This hash is done in a way that two classes with the same address type and address will have the same hash
        # to be able to be the same in a dictionary. A +1 is added to the type to avoid multiplying by 0.
        return (self.address_type.value + 1) * int(self.address, 16)
    # end def __hash__
# end class BleGapAddress


class BleUuid:
    """
    Structure representing a BLE UUID. It includes standards values.
    """
    STANDARDS = (BleUuidStandardDeclaration,
                 BleUuidStandardService,
                 BleUuidStandardCharacteristicAndObjectType,
                 BleUuidStandardDescriptor,)

    def __init__(self, value, is_16_bits_uuid=True, uuid_base=None):
        """
        :param value: Value of the 16bit part of the UUID
        :type value: ``BleUuidStandardDeclaration`` or ``BleUuidStandardService`` or
                     ``BleUuidStandardCharacteristicAndObjectType`` or ``BleUuidStandardDescriptor`` or ``int``
        :param is_16_bits_uuid: Flag indicating if this UUID is one of the standard 16 bits UUID, this will force using
                                the standard base, thus ignoring ``uuid_base`` - OPTIONAL
        :type is_16_bits_uuid: ``bool``
        :param uuid_base: The UUID base to have the complete 128 bit UUID, the byte 2 and 3 will be forced to 0 because
                          it represents the two bytes of ``value``, copies when used - OPTIONAL
        :type uuid_base: ``list[int]`` or ``None``
        """
        self.is_16_bits_uuid = is_16_bits_uuid
        if is_16_bits_uuid:
            self.base = list.copy(BleUuid128bits.BLE_BASE_16_BITS_UUID)

            if isinstance(value, BleUuid.STANDARDS):
                self.value = value
                return
            # end if

            for standard in BleUuid.STANDARDS:
                # noinspection PyProtectedMember
                if value in standard._value2member_map_:
                    self.value = standard(value)
                    return
                # end if
            # end for
        else:
            self.base = list.copy(uuid_base)
            # Force the two bytes that will be used by the uuid 16bits to 0 in the base array
            self.base[2] = 0x00
            self.base[3] = 0x00
        # end if

        # If the run arrives here it means that the value is not standard
        # (or that the standards in this lib are not up-to-date)
        self.value = value
    # end def __init__

    def __str__(self):
        if isinstance(self.value, BleUuid.STANDARDS):
            return f"{type(self).__name__}(0x{self.value.value:04X} (BLE standard uuid type, {self.value.name}))"
        else:
            if self.base is not None:
                str_to_return = f"{type(self).__name__}(0x{self.base[0]:02X}{self.base[1]:02X}{self.value:04X}"
                for i in range(4, len(self.base)):
                    str_to_return += f"{self.base[i]:02X}"
                # end for
                str_to_return += " (vendor specific uuid))"
                return str_to_return
            else:
                return f"{type(self).__name__}(0x{self.value:04X} (vendor specific uuid, base not found))"
            # end if
        # end if
    # end def __str__

    __repr__ = __str__
    def short_string(self):
        """
        Return a minimal string representation of the uuid, either just the name or the value

        :return: the string representation
        :rtype: ``str``
        """
        if isinstance(self.value, BleUuid.STANDARDS):
            return self.value.name
        else:
            if self.base is not None:
                str_to_return = f"{type(self).__name__}(0x{self.base[0]:02X}{self.base[1]:02X}{self.value:04X}"
                for i in range(4, len(self.base)):
                    str_to_return += f"{self.base[i]:02X}"
                # end for
                return str_to_return
            else:
                return f"0x{self.value:04X}"
            # end if
        # end if
    # end def short_string

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def __eq__(self, other):
        """
        Standard method for equality testing.

        :param other: Other BLE UUID to test equality with
        :type other: ``BleUuid``

        :return: Flag indicating if those BLE UUID are equal
        :rtype: ``bool``
        """
        if not isinstance(other, BleUuid):
            return False
        # end if
        return (self.value == other.value) and (self.base == other.base)
    # end def __eq__

    def __hash__(self):
        """
        Standard method for hash computation.

        :return: Hash of the object
        :rtype: ``int``
        """
        return hash(self.value * sum(self.base))
    # end def __hash__

    def to_array(self):
        """
        Get an array format of a ``BleUuid``

        :return: The format of the ``BleUuid``
        :rtype: ``list[int]``
        """
        array_to_return = self.base.copy()
        array_to_return[2] = pack('>H', self.value)[0]
        array_to_return[3] = pack('>H', self.value)[1]
        return array_to_return
    # end def to_array

    @classmethod
    def from_array(cls, uuid_array):
        """
        Get a ``BleUuid`` from an array

        :param uuid_array: BLE UUID in array format, it should be in big endian
        :type uuid_array: ``list[int]``

        :return: The BLE UUID object
        :rtype: ``BleUuid``
        """
        assert len(uuid_array) == 2 or len(uuid_array) == 16, "UUID Should be either 16bits or 128bits"

        if len(uuid_array) == 2:
            return cls(value=unpack('>H', bytes(uuid_array))[0])
        # end if

        return cls(value=unpack('>H', bytes(uuid_array[2:4]))[0], is_16_bits_uuid=False, uuid_base=uuid_array)
    # end def from_array
# end class BleUuid


class BleCharacteristicProperties:
    """
    Structure representing a BLE characteristic properties.
    """

    def __init__(self, broadcast=False, read=False, write_wo_resp=False, write=False, notify=False, indicate=False,
                 auth_signed_wr=False):
        """
        :param broadcast: Broadcast capability - OPTIONAL
        :type broadcast: ``bool``
        :param read: Read capability - OPTIONAL
        :type read: ``bool``
        :param write_wo_resp: Write without response capability - OPTIONAL
        :type write_wo_resp: ``bool``
        :param write: Write capability - OPTIONAL
        :type write: ``bool``
        :param notify: Notify capability - OPTIONAL
        :type notify: ``bool``
        :param indicate: Indicate capability - OPTIONAL
        :type indicate: ``bool``
        :param auth_signed_wr: Authentication signed write capability - OPTIONAL
        :type auth_signed_wr: ``bool``
        """
        self.broadcast = broadcast
        self.read = read
        self.write_wo_resp = write_wo_resp
        self.write = write
        self.notify = notify
        self.indicate = indicate
        self.auth_signed_wr = auth_signed_wr
    # end def __init__

    def __str__(self):
        return f"{type(self).__name__}(broadcast({self.broadcast}), read({self.read}), " \
               f"write_wo_resp({self.write_wo_resp}, write({self.write}), notify({self.notify}), " \
               f"indicate({self.indicate}), auth_signed_wr({self.auth_signed_wr}))"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def __eq__(self, other):
        """
        Test the equality of this ``BleGattCharacteristicProperties`` instance with another one.

        :param other: Other ``BleGattCharacteristicProperties`` instance
        :type other: ``BleGattCharacteristicProperties``

        :return: Comparison result
        :rtype: ``bool``
        """
        return self.broadcast == other.broadcast and\
            self.read == other.read and\
            self.write_wo_resp == other.write_wo_resp and\
            self.write == other.write and\
            self.notify == other.notify and\
            self.indicate == other.indicate and\
            self.auth_signed_wr == other.auth_signed_wr
    # end def __eq__
# end class BleCharacteristicProperties


class BleAttribute:
    """
    Structure representing a BLE attribute.
    Handle to be added to the gatt table of the BLE context is optional.
    The value can also be empty if it matches the information gotten from the GATT table.
    """

    def __init__(self, uuid, handle=None, value=None):
        """
        :param uuid: BLE UUID of the attribute
        :type uuid: ``BleUuid``
        :param handle: Handle of the attribute - OPTIONAL
        :type handle: ``int`` or ``None``
        :param value: Value of the attribute - OPTIONAL
        :type value: ``HexList`` or ``None``
        """
        self.uuid = uuid
        self.handle = handle
        self.value = value
    # end def __init__

    def short_string(self):
        """
        Return a minimal string representation of the attribute

        :return: the string representation
        :rtype: ``str``
        """
        return f"{type(self).__name__}(handle({self.handle}) uuid({self.uuid.short_string()}))"
    # end def short_string
# end class BleAttribute


class BleService(BleAttribute):
    """
    Structure representing a BLE service.
    Handles to be added to the gatt table of the BLE context is optional.
    """

    def __init__(self, uuid, start_handle=None, end_handle=None):
        """
        :param uuid: BLE UUID of the service
        :type uuid: ``BleUuid``
        :param start_handle: The first attribute handle of this service - OPTIONAL
        :type start_handle: ``int`` or ``None``
        :param end_handle: The last attribute handle of this service - OPTIONAL
        :type end_handle: ``int`` or ``None``
        """
        super().__init__(uuid=uuid, handle=start_handle)
        self.end_handle = end_handle
        self.characteristics: List[BleCharacteristic] = list()
    # end def __init__

    def __str__(self):
        characteristics = "\n\t".join(["\n\t".join(str(characteristic).split("\n")) for characteristic in
                                       self.characteristics])
        return f"{type(self).__name__}(handle({self.handle}) Service uuid({self.uuid})), characteristics:\n" \
               f"\t{characteristics}"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def add_characteristic(self, characteristic):
        """
        Add a BLE characteristic to the service.

        :param characteristic: BLE Characteristic to add
        :type characteristic: ``BleCharacteristic``
        """
        self.characteristics.append(characteristic)
    # end def add_characteristic

    def get_characteristics(self, characteristic_uuid):
        """
        Get a BLE characteristic in the service using its UUID as filter.

        :param characteristic_uuid: UUID of the characteristic to get
        :type characteristic_uuid: ``BleUuid``

        :return: List of characteristics with the wanted UUID
        :rtype: ``list[BleCharacteristic]``
        """
        characteristics_to_return = []
        for characteristic in self.characteristics:
            if characteristic.uuid == characteristic_uuid:
                characteristics_to_return.append(characteristic)
            # end if
        # end for

        return characteristics_to_return
    # end def get_characteristics
# end class BleService


class BleCharacteristic(BleAttribute):
    """
    Structure representing a BLE characteristic.
    Handle to be added to the gatt table of the BLE context is optional.
    The value can also be empty if it matches the information gotten from the GATT table.
    """

    def __init__(self, uuid, properties, declaration_handle=None, value_handle=None, value=None):
        """
        :param uuid: BLE UUID of the characteristic
        :type uuid: ``BleUuid``
        :param properties: BLE properties of the characteristic
        :type properties: ``BleCharacteristicProperties``
        :param declaration_handle: The handle of the declaration - OPTIONAL
        :type declaration_handle: ``int`` or ``None``
        :param value_handle: The handle of the value - OPTIONAL
        :type value_handle: ``int`` or ``None``
        :param value: Value of the attribute - OPTIONAL
        :type value: ``HexList`` or ``None``
        """
        super().__init__(uuid=uuid, handle=value_handle, value=value)
        self.declaration = BleAttribute(
            uuid=BleUuid(value=BleUuidStandardDeclaration.CHARACTERISTIC_DECLARATION), handle=declaration_handle)
        self.properties = properties
        self.descriptors: List[BleDescriptor] = list()
    # end def __init__

    def __str__(self):
        return f"{type(self).__name__}(handle({self.declaration.handle}) Characteristic declaration " \
               f"uuid({self.declaration.uuid})\n" \
               f"\thandle({self.handle}) Characteristic value uuid({self.uuid}) properties({self.properties}) " \
               f"value({self.value}))"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def get_descriptors(self, descriptor_uuid):
        """
        Get a BLE characteristic in the service using its UUID as filter.

        :param descriptor_uuid: UUID of the descriptor to get
        :type descriptor_uuid: ``BleUuid``

        :return: List of descriptors with the wanted UUID
        :rtype: ``list[BleDescriptor]``
        """
        descriptors_to_return = []
        for descriptor in self.descriptors:
            if descriptor.uuid == descriptor_uuid:
                descriptors_to_return.append(descriptor)
            # end if
        # end for

        return descriptors_to_return
    # end def get_descriptors
# end class BleCharacteristic


class BleDescriptor(BleAttribute):
    """
    Structure representing a BLE descriptor.
    Handle to be added to the gatt table of the BLE context is optional.
    """

    def __str__(self):
        return f"{type(self).__name__}(handle({self.handle}) Descriptor uuid({self.uuid}))"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__
# end class BleDescriptor


class BleAdvertisingData:
    """
    Structure representing a BLE advertising data (no header of the payload is in this structure).
    """

    def __init__(self, records, timestamp):
        """
        :param records: Mapping of type and data in the advertising packet.
        :type records: ``dict``
        :param timestamp: The timestamp of the first packet in nanosecond
        :type timestamp: ``int``
        """
        # According to Supplement to Bluetooth Core Specification | CSS v9 page 9
        # Table 1.1: Permitted usages for data types, some types can appear more than once in a block so for
        # one type k, there can be multiple elements therefore the value in the dictionary for the key k should be a
        # list. This behavior seems to be depending on the data type but for ease of use all values are lists.
        self.records = records
        self._timestamps = [timestamp]
        self._action_lock = RLock()
    # end def __init__

    @synchronize_with_object_inner_lock("_action_lock")
    def add_timestamp(self, timestamp):
        """
        Add a timestamp of the next advertising packet to the list.

        :param timestamp: The timestamp of the next packet in nanosecond
        :type timestamp: ``int``
        """
        assert timestamp > self._timestamps[-1], "Cannot add a timestamp smaller than the previous one"
        self._timestamps.append(timestamp)
    # end def add_timestamp

    @synchronize_with_object_inner_lock("_action_lock")
    def get_timestamps(self):
        """
        Get the copy of the list of timestamps in nanosecond.

        :return: The copy of the list of timestamps
        :rtype: ``list[int]``
        """
        return self._timestamps.copy()
    # end def get_timestamps

    @synchronize_with_object_inner_lock("_action_lock")
    def to_list(self):
        """
        Get advertising packet as a list

        :return: List format of the advertising packet
        :rtype: ``list[int]``
        """
        data_list = []
        for record in self.records:
            for elements in self.records[record]:
                data_list.append(len(elements) + 1)  # add type length

                if isinstance(record, BleAdvertisingDataType):
                    data_list.append(record.value)
                elif isinstance(record, int):
                    data_list.append(record)
                else:
                    raise ValueError(f"Data type {record} is not of the right class. It should be either an int or a "
                                     f"BleAdvertisingDataType but it is {type(record)}")
                # end if

                if isinstance(elements, str):
                    data_list.extend([ord(c) for c in elements])
                elif isinstance(elements, (list, tuple)):
                    data_list.extend(elements)
                else:
                    raise ValueError(f"Data {elements} is not of the right class. It should be either a str or a "
                                     f"list but it is {type(elements)}")
                # end if
            # end for
        # end for
        return data_list
    # end def to_list

    @classmethod
    def from_list(cls, advertising_data_list, timestamp):
        """
        Get advertising packet object from a list

        :param advertising_data_list: List format of the advertising packet
        :type advertising_data_list: ``list[int]``
        :param timestamp: The timestamp of the first packet in nanosecond
        :type timestamp: ``int``
        """
        counter = 0
        data_offset = 2
        advertising_data = cls(records={}, timestamp=timestamp)
        while counter < len(advertising_data_list):
            record_length = advertising_data_list[counter]
            if record_length == 0:
                counter += 1
                continue
            # end if
            record_id = advertising_data_list[counter + 1]
            if record_id in BleAdvertisingDataType:
                record_id = BleAdvertisingDataType(record_id)
            # end if
            record_data = advertising_data_list[counter + data_offset:counter + record_length + 1]
            if record_id not in advertising_data.records:
                advertising_data.records[record_id] = [record_data]
            else:
                advertising_data.records[record_id].append(record_data)
            # end if
            counter += record_length + 1
        # end while
        return advertising_data
    # end def from_list

    @synchronize_with_object_inner_lock("_action_lock")
    def __str__(self):
        data_str = f"{type(self).__name__}("
        data_list = []
        # Parse records in the packet
        for record in self.records:
            # Parse elements in each record. Each record can have more than one occurrence in the packet
            for elements in self.records[record]:
                # Add data length in the data list but not in the data string
                data_list.append(len(elements) + 1)

                # Add data type
                if isinstance(record, BleAdvertisingDataType):
                    data_str += f"{record.name}(0x{record.value:02X}): "
                    data_list.append(record.value)
                elif isinstance(record, int):
                    data_str += f"Unknown AD type(0x{record:02X}): "
                    data_list.append(record)
                else:
                    raise ValueError(f"Data type {record} is not of the right class. It should be either an int or a "
                                     f"BleAdvertisingDataType but it is {type(record)}")
                # end if

                # Add the data itself
                if isinstance(elements, str):
                    data_str += elements + ", "
                    data_list.extend([ord(c) for c in elements])
                elif isinstance(elements, (list, tuple)):
                    # If the element is a name, print it as a string and not data list
                    if record == BleAdvertisingDataType.SHORT_LOCAL_NAME or \
                            record == BleAdvertisingDataType.COMPLETE_LOCAL_NAME:
                        data_str += str(bytes(elements))
                    else:
                        for element in elements:
                            data_str += f"{element:02X}"
                        # end for
                    # end if
                    data_str += ", "
                    data_list.extend(elements)
                else:
                    raise ValueError(f"Data {elements} is not of the right class. It should be either a str or a "
                                     f"list but it is {type(elements)}")
                # end if
            # end for
        # end for

        # Add full packet data list (and average interval when applicable)
        if len(self._timestamps) > 1:
            average_window = int(mean([self._timestamps[i+1] - self._timestamps[i]
                                       for i in range(len(self._timestamps) - 1)]) // TIMESTAMP_UNIT_DIVIDER_MAP['ms'])
            prefix = f"Average advertising window {average_window}ms, "
        else:
            prefix = ""
        # end if

        data_str = prefix + f"Data(Raw packet: {HexList(data_list)}, " + data_str
        # The -2 of the string is to remove the last ", " and close the Data parenthesis
        data_str = data_str[:-2] + "))"
        return data_str
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def __eq__(self, other):
        """
        Test the equality of this ``BleAdvertisingData`` instance with another one.

        :param other: Other ``BleAdvertisingData`` instance
        :type other: ``BleAdvertisingData``

        :return: Comparison result
        :rtype: ``bool``
        """
        if not isinstance(other, BleAdvertisingData):
            return False
        # end if
        return self.to_list() == other.to_list()
    # end def __eq__
# end class BleAdvertisingData


class BleAdvertising:
    """
    Structure representing a BLE advertising.
    """

    def __init__(self, advertising_type, advertising_data):
        """
        :param advertising_type: The advertising type
        :type advertising_type: ``BleAdvertisingPduType``
        :param advertising_data: The advertising data
        :type advertising_data: ``BleAdvertisingData``
        """
        self.advertising_type = advertising_type
        self.advertising_data = advertising_data
    # end def __init__
# end class BleAdvertising


class BleDeviceBondingStates(Enum):
    """
    Enum of the states of a device Bonding
    """
    NO_BONDING = auto()
    STARTED = auto()
    KEY_PASS_BONDING = auto()
    KEY_PASS_BONDING_COMPLETE = auto()  # The pass key was confirmed by the user pending bonding complete
    BONDED = auto()
    FAILED = auto()  # Pairing failed for a know reason
    ERROR = auto() # Internal error in the bonding procedure
# end class BleDeviceBondingStates


class BleGapConnectionParameters:
    """
    Parameters for a BLE GAP connection
    """

    def __init__(self, min_connection_interval, max_connection_interval, supervision_timeout, slave_latency):
        """
        :param min_connection_interval: Minimal connection interval in milliseconds
        :type min_connection_interval: ``int`` or ``float``
        :param max_connection_interval: Maximal connection interval in milliseconds
        :type max_connection_interval: ``int`` or ``float``
        :param supervision_timeout: Connection supervision timeout in milliseconds
        :type supervision_timeout: ``int`` or ``float``
        :param slave_latency: Slave latency parameter in number of connection events
        :type slave_latency: ``int``
        """
        self.min_connection_interval = min_connection_interval
        self.max_connection_interval = max_connection_interval
        self.supervision_timeout = supervision_timeout
        self.slave_latency = slave_latency
    # end def __init__

    def __str__(self):
        return f"{type(self).__name__}(min_connection_interval({self.min_connection_interval}ms), " \
               f"max_connection_interval({self.max_connection_interval}ms), " \
               f"supervision_timeout({self.supervision_timeout}ms), slave_latency({self.slave_latency}))"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def __eq__(self, other):
        """
        Standard equal function

        :param other: the other connection parameter
        :type other: ``BleGapConnectionParameters``
        :return: Flag indicating the equality
        :rtype: ``bool``
        """
        return self.min_connection_interval == other.min_connection_interval and \
            self.max_connection_interval == other.max_connection_interval and \
            self.supervision_timeout == other.supervision_timeout and \
            self.slave_latency == other.slave_latency
    # end def __eq__
# end class BleGapConnectionParameters


class BleGapConnectionParametersRange:
    """
    Parameters range for a BLE GAP connection
    """

    def __init__(self, min_connection_interval, max_connection_interval, min_supervision_timeout,
                 max_supervision_timeout, min_slave_latency, max_slave_latency):
        """
        :param min_connection_interval: Minimal connection interval in milliseconds
        :type min_connection_interval: ``int`` or ``float``
        :param max_connection_interval: Maximal connection interval in milliseconds
        :type max_connection_interval: ``int`` or ``float``
        :param min_supervision_timeout: Minimal Connection supervision timeout in milliseconds
        :type min_supervision_timeout: ``int`` or ``float``
        :param max_supervision_timeout: Maximal Connection supervision timeout in milliseconds
        :type max_supervision_timeout: ``int`` or ``float``
        :param min_slave_latency: Minimal Slave latency parameter in number of connection events
        :type min_slave_latency: ``int``
        :param max_slave_latency: Maximal Slave latency parameter in number of connection events
        :type max_slave_latency: ``int``
        """
        self.min_connection_interval = min_connection_interval
        self.max_connection_interval = max_connection_interval
        self.min_supervision_timeout = min_supervision_timeout
        self.max_supervision_timeout = max_supervision_timeout
        self.min_slave_latency = min_slave_latency
        self.max_slave_latency = max_slave_latency
    # end def __init__

    def __str__(self):
        return f"{type(self).__name__}(min_connection_interval({self.min_connection_interval}ms), " \
               f"max_connection_interval({self.max_connection_interval}ms), " \
               f"min_supervision_timeout({self.min_supervision_timeout}ms), " \
               f"max_supervision_timeout({self.max_supervision_timeout}ms), " \
               f"min_slave_latency({self.min_slave_latency}), max_slave_latency({self.max_slave_latency}))"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def in_range(self, parameters):
        """
        check if the given connection parameters are in the range of this connection parameter range
        :param parameters: the connection parameter to check
        :type parameters: ``BleGapConnectionParameters``
        :return: flag indicating whether the connection parameter is in range
        :rtype: ``bool``
        """
        # true if both connection interval range overlap
        in_connection_interval_range = parameters.min_connection_interval <= self.max_connection_interval and \
            parameters.max_connection_interval >= self.min_connection_interval
        in_slave_latency_range = self.min_slave_latency <= parameters.slave_latency <= self.max_slave_latency
        in_supervision_timeout_range = self.min_supervision_timeout <= parameters.supervision_timeout \
            <= self.max_supervision_timeout
        return in_connection_interval_range and in_slave_latency_range and in_supervision_timeout_range
    # end def in_range
# end class BleGapConnectionParametersRange


class BleGapConnectionSecurityParameters:
    """
    Security parameters for a BLE GAP connection
    """

    def __init__(self, encrypted=False, mitm=False, lesc=False, signed=False, encryption_key_size=None, bonded=False):
        """
        :param encrypted: Flag indicating that the connection is encrypted - OPTIONAL
        :type encrypted: ``bool``
        :param mitm: Flag indicating that the connection has a Man In The Middle protection - OPTIONAL
        :type mitm: ``bool``
        :param lesc: Flag indicating that the connection is a LE Secure Connection - OPTIONAL
        :type lesc: ``bool``
        :param signed: Flag indicating that the connection is signed - OPTIONAL
        :type signed: ``bool``
        :param encryption_key_size: Size of the encryption key, only applicable for bonding (``None`` if not
                                    applicable) - OPTIONAL
        :type encryption_key_size: ``int`` or ``None``
        :param bonded: Flag indicating that the connection is bonded - OPTIONAL
        :type bonded: ``bool``
        """
        self.encrypted = encrypted
        self.mitm = mitm
        self.lesc = lesc
        self.signed = signed
        self.encryption_key_size = encryption_key_size
        self.bonded = bonded
    # end def __init__

    def __str__(self):
        return f"{type(self).__name__}(encrypted({self.encrypted}), mitm({self.mitm}), lesc({self.lesc}), " \
               f"signed({self.signed}), encryption_key_size({self.encryption_key_size}), bonded({self.bonded}))"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__
# end class BleGapConnectionSecurityParameters


class PnPId(BitFieldContainerMixin):
    """
     Define PnP ID (DIS service) bitfield structure
    """

    class FID:
        """
        Field Identifiers
        """
        VENDOR_ID_SRC = 0xFF
        VENDOR_ID = VENDOR_ID_SRC - 1
        PRODUCT_ID = VENDOR_ID - 1
        FW_BUILD = PRODUCT_ID - 1
    # end class FID

    class LEN:
        """
        Field length in bits
        """
        VENDOR_ID_SRC = 8
        VENDOR_ID = 16
        PRODUCT_ID = 16
        FW_BUILD = 16
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.VENDOR_ID_SRC,
            length=LEN.VENDOR_ID_SRC,
            title='VendorIdSrc',
            name='vendor_id_src',
            aliases=('vid_src',),
            checks=(CheckHexList(LEN.VENDOR_ID_SRC // 8), CheckByte(),), ),
        BitField(
            fid=FID.VENDOR_ID,
            length=LEN.VENDOR_ID,
            title='VendorId',
            name='vendor_id',
            aliases=('vid', 'usb_vid', 'bt_vid',),
            checks=(CheckHexList(LEN.VENDOR_ID // 8), CheckInt(min_value=0, max_value=pow(2, LEN.VENDOR_ID) - 1),), ),
        BitField(
            fid=FID.PRODUCT_ID,
            length=LEN.PRODUCT_ID,
            title='ProductId',
            name='product_id',
            aliases=('pid', 'bt_pid',),
            checks=(CheckHexList(LEN.PRODUCT_ID // 8), CheckInt(min_value=0, max_value=pow(2, LEN.PRODUCT_ID) - 1),), ),
        BitField(
            fid=FID.FW_BUILD,
            length=LEN.FW_BUILD,
            title='FwBuild',
            name='fw_build',
            checks=(CheckHexList(LEN.FW_BUILD // 8), CheckInt(min_value=0, max_value=pow(2, LEN.FW_BUILD) - 1),), ),
    )
# end class PnPId


class HIDInformation(BitFieldContainerMixin):
    """
     Define HID information (HIDS service) bitfield structure
    """

    class FID:
        """
        Field Identifiers
        """
        BCD_HID = 0xFF
        COUNTRY_CODE = BCD_HID - 1
        FLAGS = COUNTRY_CODE - 1
    # end class FID

    class LEN:
        """
        Field length in bits
        """
        BCD_HID = 16
        COUNTRY_CODE = 8
        FLAGS = 8
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.BCD_HID,
            length=LEN.BCD_HID,
            title='BcdHID',
            name='bcd_hid',
            aliases=('bcdHID',),
            checks=(CheckHexList(LEN.BCD_HID // 8), CheckInt(min_value=0, max_value=pow(2, LEN.BCD_HID) - 1),), ),

        BitField(
            fid=FID.COUNTRY_CODE,
            length=LEN.COUNTRY_CODE,
            title='bCountryCode',
            name='country_code',
            aliases=('b_country_code',),
            checks=(CheckHexList(LEN.COUNTRY_CODE // 8), CheckByte(),), ),
        BitField(
            fid=FID.FLAGS,
            length=LEN.FLAGS,
            title='Flags',
            name='flags',
            aliases=(),
            checks=(CheckHexList(LEN.FLAGS // 8), CheckByte(),), ),
    )
# end class HIDInformation


class BatteryLevelStatus(BitFieldContainerMixin):
    """
    Define Battery Level Status (BAS) bitfield structure, ordered in the BLE little endian
    """

    class FID:
        """
        Field identifiers
        """
        FLAGS = 0xFF
        BATTERY_PRESENT = FLAGS-1
        WIRED_EXTERNAL_POWER_SOURCE_CONNECTED = BATTERY_PRESENT-1
        WIRELESS_EXTERNAL_POWER_SOURCE_CONNECTED = WIRED_EXTERNAL_POWER_SOURCE_CONNECTED-1
        BATTERY_CHARGE_STATE = WIRELESS_EXTERNAL_POWER_SOURCE_CONNECTED - 1
        BATTERY_CHARGE_LEVEL = BATTERY_CHARGE_STATE - 1
        CHARGING_TYPE = BATTERY_CHARGE_LEVEL - 1
        CHARGING_FAULT_REASONS = CHARGING_TYPE - 1 
        RFU = CHARGING_FAULT_REASONS - 1
    # end class FID
    
    class LEN:
        FLAGS = 8
        BATTERY_PRESENT = 1 
        WIRED_EXTERNAL_POWER_SOURCE_CONNECTED =  2
        WIRELESS_EXTERNAL_POWER_SOURCE_CONNECTED = 2 
        BATTERY_CHARGE_STATE = 2
        BATTERY_CHARGE_LEVEL = 2
        CHARGING_TYPE = 3
        CHARGING_FAULT_REASONS = 3 
        RFU = 1
    # end class LEN
    
    FIELDS = (
        BitField(
            fid=FID.RFU,
            length=LEN.RFU,
            title='RFU',
            name='rfu',
            aliases=(),
            checks=(CheckHexList(LEN.RFU // 8), CheckInt(min_value=0, max_value=pow(2, LEN.RFU) - 1),), ),
        BitField(
            fid=FID.CHARGING_FAULT_REASONS,
            length=LEN.CHARGING_FAULT_REASONS,
            title='Charging_Fault_Reasons',
            name='charging_fault_reasons',
            aliases=(),
            checks=(CheckHexList(LEN.CHARGING_FAULT_REASONS // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.CHARGING_FAULT_REASONS) - 1),), ),
        BitField(
            fid=FID.CHARGING_TYPE,
            length=LEN.CHARGING_TYPE,
            title='Charging_Type',
            name='charging_type',
            aliases=(),
            checks=(
            CheckHexList(LEN.CHARGING_TYPE // 8), CheckInt(min_value=0, max_value=pow(2, LEN.CHARGING_TYPE) - 1),), ),
        BitField(
            fid=FID.BATTERY_CHARGE_LEVEL,
            length=LEN.BATTERY_CHARGE_LEVEL,
            title='Battery_Charge_Level',
            name='battery_charge_level',
            aliases=(),
            checks=(CheckHexList(LEN.BATTERY_CHARGE_LEVEL // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.BATTERY_CHARGE_LEVEL) - 1),), ),
        BitField(
            fid=FID.BATTERY_CHARGE_STATE,
            length=LEN.BATTERY_CHARGE_STATE,
            title='Battery_Charge_State',
            name='battery_charge_state',
            aliases=(),
            checks=(CheckHexList(LEN.BATTERY_CHARGE_STATE // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.BATTERY_CHARGE_STATE) - 1),), ),
        BitField(
            fid=FID.WIRELESS_EXTERNAL_POWER_SOURCE_CONNECTED,
            length=LEN.WIRELESS_EXTERNAL_POWER_SOURCE_CONNECTED,
            title='Wireless_External_Power_Source_Connected',
            name='wireless_external_power_source_connected',
            aliases=(),
            checks=(CheckHexList(LEN.WIRELESS_EXTERNAL_POWER_SOURCE_CONNECTED // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.WIRELESS_EXTERNAL_POWER_SOURCE_CONNECTED) - 1),), ),
        BitField(
            fid=FID.WIRED_EXTERNAL_POWER_SOURCE_CONNECTED,
            length=LEN.WIRED_EXTERNAL_POWER_SOURCE_CONNECTED,
            title='Wired_External_Power_Source_Connected',
            name='wired_external_power_source_connected',
            aliases=(),
            checks=(CheckHexList(LEN.WIRED_EXTERNAL_POWER_SOURCE_CONNECTED // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.WIRED_EXTERNAL_POWER_SOURCE_CONNECTED) - 1),), ),
        BitField(
            fid=FID.BATTERY_PRESENT,
            length=LEN.BATTERY_PRESENT,
            title='Battery_Present',
            name='battery_present',
            aliases=(),
            checks=(CheckHexList(LEN.BATTERY_PRESENT // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.BATTERY_PRESENT) - 1),), ),
        BitField(
            fid=FID.FLAGS,
            length=LEN.FLAGS,
            title='Flags',
            name='flags',
            aliases=(),
            checks=(CheckHexList(LEN.FLAGS // 8), CheckInt(min_value=0, max_value=pow(2, LEN.FLAGS) - 1),), ),
    )
# end class BatteryLevelStatus
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
