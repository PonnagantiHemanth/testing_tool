#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.memoryinterface
:brief: MCU memory manager interface classes.
:author: Christophe Roquebert <croquebert@logitech.com>
:date:   2020/06/15
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import abc

from pylibrary.tools.util import NotImplementedAbstractMethodError


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class NvsManagerInterface(object, metaclass=abc.ABCMeta):
    """
    Nvs Manager Interface.
    """
    @abc.abstractmethod
    def read_nvs(self, **kwargs):
        """
        Read NVS content using the debugger and create an NVS Parser object
        """
        raise NotImplementedError('users must implement the read_nvs function to use this base class')
    # end def read_nvs

    @abc.abstractmethod
    def load_nvs(self, **kwargs):
        """
        Store the modified NVS content on the target using the debugger
        """
        raise NotImplementedError('users must implement the load_nvs function to use this base class')
    # end def read_nvs

    @abc.abstractmethod
    def reset(self, **kwargs):
        """
        Reset the device using the debugger.
        """
        raise NotImplementedError('users must implement the reset function to use this base class')
    # end reset

    @abc.abstractmethod
    def invalidate_chunks(self, chunk_names=None, **kwargs):
        """
        Invalidate a chunk based on its name (and matching on in the chunk_id_map)

        :param chunk_names: list of chunk names as defined in the chunk id map
        :type chunk_names: ``list of str``

        :return: Number of invalidated chunk or None (if nvs_read() not called)
        :rtype: ``int or None``
        """
        raise NotImplementedError('users must implement the invalidate_chunks function to use this base class')
    # end invalidate_chunks

    @abc.abstractmethod
    def get_active_chunk_by_name(self, chunk_name, **kwargs):
        """
        Retrieve the current active chunk matching the given name and cast it into its python representation (if any)

        :param chunk_name: chunk name as defined in the chunk id map
        :type chunk_name: ``str``

        :return: python chunk representation
        :rtype: ``DeviceBleBondId or ReceiverBleBondId``
        """
        raise NotImplementedError('users must implement the get_active_chunk_by_name function to use this base class')
    # end def get_active_chunk_by_name

    @abc.abstractmethod
    def get_chunks_by_name(self, chunk_name, **kwargs):
        """
        Retrieve a list of chunks matching the given name and cast it into its python representation (if any)

        :param chunk_name: chunk name as defined in the chunk id map
        :type chunk_name: ``str``

        :return: list of python chunk representation
        :rtype: ``DeviceBleBondId or ReceiverBleBondId``
        """
        raise NotImplementedError('users must implement the get_chunks_by_name function to use this base class')
    # end get_chunks_by_name

    @abc.abstractmethod
    def get_ble_bond_id_chunks(self, pairing_slot=0, bluetooth_address=None, **kwargs):
        """
        Retrieve the NVS_BLE_BOND_ID chunks list from NVS by pairing slot and bluetooth address

        :param pairing_slot: device index - optional
        :type pairing_slot: ``int``
        :param bluetooth_address: central or peripheral bluetooth address
        :type bluetooth_address: ``HexList``
        """
        raise NotImplementedError('users must implement the get_ble_bond_id_chunks function to use this base class')
    # end get_ble_bond_id_chunks

    @abc.abstractmethod
    def get_bluetooth_addresses(self, pairing_slots=None, **kwargs):
        """
        Retrieve the bluetooth addresses from a given list of pairing slots

        Shall be overloaded by specific MCU implementation

        :param pairing_slots: device index - optional
        :type pairing_slots: ``list``

        :return: List of tuple (slot, bluetooth address (LSB))
        :rtype: ``list[tuple[int, HexList]]``
        """
        raise NotImplementedError('users must implement the get_bluetooth_address function to use this base class')
    # end get_bluetooth_addresses

    @abc.abstractmethod
    def clean_pairing_data(self):
        """
        Parse NVS content to clean pairing information.

        :return: Flag indicating if the NVS has been reloaded (inferring a device reset)
        :rtype: ``bool``
        """
        raise NotImplementedError('users must implement the clean_pairing_data function to use this base class')
    # end def clean_pairing_data

    def switch_to_host_id(self, host_id=0, is_test_setup=True, force_oob=False):
        """
        Switch to given host index

        :param host_id: Last connected host index - OPTIONAL
        :type host_id: ``int``
        :param is_test_setup: Clean pairing slot 2 & 3 if test setup - OPTIONAL
        :type is_test_setup: ``bool``
        :param force_oob: Flag to force the given host to OOB state - OPTIONAL
        :type force_oob: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def switch_to_host_id
# end class NvsManagerInterface


class UicrManagerInterface(object, metaclass=abc.ABCMeta):
    """
    UICR Manager Interface.
    """

    @abc.abstractmethod
    def is_nvs_encrypted(self):
        """
        Check the presence of a local NVS AES encryption key.
        """
        raise NotImplementedError('users must implement the is_nvs_encrypted function to use this base class')
    # end is_nvs_encrypted

    @abc.abstractmethod
    def get_nvs_encryption_key(self):
        """
        Extract the local NVS AES encryption key.
        """
        raise NotImplementedError('users must implement the get_nvs_encryption_key function to use this base class')
    # end get_nvs_encryption_key
# end class UicrManagerInterface


class FlashManagerInterface(object, metaclass=abc.ABCMeta):
    """
    Flash Manager Interface.
    """

# end class FlashManagerInterface

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
