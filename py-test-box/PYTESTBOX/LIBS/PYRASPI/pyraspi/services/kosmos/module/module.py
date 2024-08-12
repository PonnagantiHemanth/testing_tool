#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.module
:brief: Kosmos Module Package
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/12/14
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from ctypes import Array as ctypes_Array
from ctypes import Structure as ctypes_Structure
from ctypes import Union as ctypes_Union
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from math import ceil

from pyraspi.services.kosmos.fpgatransport import ExtractPayloadError
from pyraspi.services.kosmos.fpgatransport import FPGATransport
from pyraspi.services.kosmos.module.devicetree import DeviceTreeModuleBaseClass
from pyraspi.services.kosmos.module.devicetree import DeviceTreeModuleSettings
from pyraspi.services.kosmos.module.error import KosmosFatalErrorException
from pyraspi.services.kosmos.protocol.generated.messages import MSG_CMD_REPLY_FLAG
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_DYN_BASE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_DYN_END
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_STATUS_CMD_REPLY
from pyraspi.services.kosmos.protocol.generated.messages import msg_cmd_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import msg_id_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import msg_reply_return_code_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import pes_timer_t
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

###################################
# Module Error class definition
###################################

class ModuleStatusSanityChecksError(KosmosFatalErrorException):
    """
    Module Status sanity checks Exception class.
    """
    pass
# end class ModuleStatusSanityChecksError


###################################
# Module Settings class definition
###################################


@dataclass(frozen=True)
class ModuleSettings(DeviceTreeModuleSettings):
    """
    Dataclass constructor arguments (+ refer to base class(es) arguments):
    ``msg_id``: Message identifier.
    """
    msg_id: int

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()

        assert MSG_ID_DYN_BASE <= self.msg_id <= MSG_ID_DYN_END or \
               (self.msg_id < MSG_ID_DYN_BASE and self.msg_id in msg_id_e__enumvalues), \
               f'Unknown or Out-of-range message id {self.msg_id:#04x}'
        # end if
    # end def __post_init__
# end class ModuleSettings


@dataclass(frozen=True)
class StatusResetModuleSettings(ModuleSettings):
    """
    Dataclass constructor arguments (+ refer to base class(es) arguments):
    ``msg_cmd_reset``: Reset Message CMD. Refer to `msg_cmd_e__enumvalues`
    ``msg_cmd_status``: Status Message CMD. Refer to `msg_cmd_e__enumvalues`
    ``status_type``: Status message object type
    """
    msg_cmd_reset: int
    msg_cmd_status: int
    status_type: Type[Union[ctypes_Structure, ctypes_Union, ctypes_Array]]

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()
        assert self.msg_cmd_reset in msg_cmd_e__enumvalues, f'Unknown Reset Message CMD: {self.msg_cmd_reset:#04x}.'
        assert issubclass(self.status_type, (ctypes_Structure, ctypes_Union, ctypes_Array)), self.status_type
        assert self.msg_cmd_status in msg_cmd_e__enumvalues, f'Unknown Status Message CMD: {self.msg_cmd_status:#04x}.'
    # end def __post_init__
# end class StatusResetModuleSettings


@dataclass(frozen=True)
class BufferModuleSettings(StatusResetModuleSettings):
    """
    Dataclass constructor arguments (+ refer to base class(es) arguments):
    ``buffer_size``: Remote buffer allocated size (max entry count is one item less than buffer size)
    ``fifo_size``: Remote FIFO allocated size (max entry count is one item less than FIFO size)
    ``data_type``: Module payload, FIFO and buffer data type
    """
    buffer_size: int
    fifo_size: Optional[int]
    data_type: Any

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()
        assert self.buffer_size > 0, r'Buffer size must be strictly positive.'
        assert self.fifo_size is None or self.fifo_size > 0, r'FIFO size must be strictly positive.'
    # end def __post_init__
# end class BufferModuleSettings


@dataclass(frozen=True)
class DownloadModuleSettings(BufferModuleSettings):
    """
    Dataclass constructor arguments (+ refer to base class(es) arguments):
    ``msg_cmd_read_one``: Read_1 Message CMD. Refer to `msg_cmd_e__enumvalues`
    ``msg_cmd_read_max``: Read_Max Message CMD. Refer to `msg_cmd_e__enumvalues`
    """
    msg_cmd_read_one: int
    msg_cmd_read_max: int

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()
        assert self.msg_cmd_read_one in msg_cmd_e__enumvalues, self.msg_cmd_read_one
        assert self.msg_cmd_read_max in msg_cmd_e__enumvalues, self.msg_cmd_read_max
        assert self.msg_cmd_read_one < self.msg_cmd_read_max, (self.msg_cmd_read_one, self.msg_cmd_read_max)
    # end def __post_init__
# end class DownloadModuleSettings


@dataclass(frozen=True)
class UploadModuleSettings(BufferModuleSettings):
    """
    Dataclass constructor arguments (+ refer to base class(es) arguments):
    ``msg_payload_name``: name of the payload field in `MessageFrame`
    ``msg_cmd_write_one``: Read_1 Message CMD. Refer to `msg_cmd_e__enumvalues`
    ``msg_cmd_write_max``: Read_Max Message CMD. Refer to `msg_cmd_e__enumvalues`
    """
    msg_payload_name: str
    msg_cmd_write_one: int
    msg_cmd_write_max: int

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()
        m = MessageFrame()
        assert getattr(m.frame.payload, self.msg_payload_name, False), \
            f'Cannot find payload name "{self.msg_payload_name}" in message payload structure'
        assert self.msg_cmd_write_one in msg_cmd_e__enumvalues, self.msg_cmd_write_one
        assert self.msg_cmd_write_max in msg_cmd_e__enumvalues, self.msg_cmd_write_max
        assert self.msg_cmd_write_one < self.msg_cmd_write_max, (self.msg_cmd_write_one, self.msg_cmd_write_max)
    # end def __post_init__
# end class UploadModuleSettings


@dataclass(frozen=True)
class ConsumerModuleSettings(UploadModuleSettings):
    """
    ConsumerModuleSettings Dataclass
    """
    pass
# end class ConsumerModuleSettings


@dataclass(frozen=True)
class ProducerModuleSettings(DownloadModuleSettings):
    """
    Dataclass constructor arguments (+ refer to base class(es) arguments):
    ``msg_cmd_start``: Start Message CMD. Refer to `msg_cmd_e__enumvalues`
    ``msg_cmd_stop``: Stop Message CMD. Refer to `msg_cmd_e__enumvalues`
    ``status_state_reset_or_stop``: 'Reset or Stop' state value
    ``status_state_started``: 'Started' state value
    ``status_state_enumvalues``: state enumeration (key-value dictionary)
    """
    msg_cmd_start: int
    msg_cmd_stop: int
    status_state_reset_or_stop: int
    status_state_started: int
    status_state_enumvalues: Dict[int, str]

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        super().__post_init__()
        assert self.msg_cmd_start in msg_cmd_e__enumvalues, self.msg_cmd_start
        assert self.msg_cmd_stop in msg_cmd_e__enumvalues, self.msg_cmd_stop
        assert self.status_state_reset_or_stop in self.status_state_enumvalues, self.status_state_reset_or_stop
        assert self.status_state_started in self.status_state_enumvalues, self.status_state_started
    # end def __post_init__
# end class ProducerModuleSettings


###################################
# Module Base class definition
###################################


class ModuleBaseClass(DeviceTreeModuleBaseClass, metaclass=ABCMeta):
    """
    Generic Kosmos Module base class
    """

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Module settings dataclass object
        :type module_settings: ``ModuleSettings``

        :raise ``AssertionError``: invalid argument types
        """
        assert isinstance(module_settings, ModuleSettings), module_settings
        super().__init__(module_settings=module_settings)
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only settings dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``ModuleSettings``
        """
        return self._settings
    # end def property getter settings
# end class ModuleBaseClass


class StatusResetModuleBaseClass(ModuleBaseClass, metaclass=ABCMeta):
    """
    Kosmos Module base class for modules having Status and Reset features.
    """

    # Post-reset callback: actions to be done after reset of module or system
    _reset_callbacks: List[Callable]

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Module settings dataclass object
        :type module_settings: ``StatusResetModuleSettings``

        :raise ``AssertionError``: invalid argument types
        """
        assert isinstance(module_settings, StatusResetModuleSettings), module_settings
        super().__init__(module_settings=module_settings)
        self._reset_callbacks = []
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``StatusResetModuleSettings``
        """
        return self._settings
    # end def property getter settings

    def reset_module(self, sanity_checks=True):
        """
        Reset the module:
          - Mask all interrupt sources
          - Clear FIFO and buffer content
          - Clear FIFO and buffer overrun status
          - Reset module's FPGA state machine

        :param sanity_checks: If True, run sanity checks on the status reply and raise an error if something is wrong.
                              If False, skip sanity checks. Defaults to True - OPTIONAL
        :type sanity_checks: ``bool``

        :return: module status after reset of the module.
        :rtype: ``self.settings.status_type``

        :raise ``ModuleStatusSanityChecksError``: Unexpected status values, after reset of the module
        """
        # Send request
        status = self._reset_module()

        # Sanity checks
        if sanity_checks:
            error_list = self.is_reset_reply_valid(status)
            if error_list:
                raise ModuleStatusSanityChecksError('\n'.join(error_list))
            # end if
        # end if

        # Post-reset callback: actions to be done after reset of module or system
        self._process_reset_callbacks()

        return status
    # end def reset_module

    def _reset_module(self):
        """
        Reset the module:
          - Mask all interrupt sources
          - Clear FIFO and buffer content
          - Clear FIFO and buffer overrun status
          - Reset module's FPGA state machine

        :return: module status after reset of the module.
        :rtype: ``self.settings.status_type``
        """
        # Send request
        return self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                           msg_cmd=self.settings.msg_cmd_reset)
    # end def _reset_module

    def register_reset_callback(self, callback):
        """
        Register a post-reset callback: actions to be done after reset of the module or the system.

        :param callback: Method to be called after reset of the module or the system
        :type callback: ``Callable``

        :raise ``AssertionError``: invalid callback type
        """
        assert isinstance(callback, Callable), callback
        self._reset_callbacks.append(callback)
    # end def register_reset_callback

    def _process_reset_callbacks(self):
        """
        Call post-reset callbacks: actions to be done after reset of the module or the system
        """
        for callback in self._reset_callbacks:
            callback()
        # end for
    # end def _process_reset_callbacks

    def status(self, sanity_checks=True):
        """
        Return the module's status.

        :param sanity_checks: If True, run sanity checks on the status reply and raise an error if something is wrong.
                              If False, skip sanity checks. Defaults to True - OPTIONAL
        :type sanity_checks: ``bool``

        :return: module's status.
        :rtype: ``self.settings.status_type``

        :raise ``ModuleStatusSanityChecksError``: Unexpected status values
        """
        # Send request and get reply
        status = self._status()

        # Sanity checks
        if sanity_checks:
            error_list = self.is_status_reply_valid(status)
            if error_list:
                raise ModuleStatusSanityChecksError('\n'.join(error_list))
            # end if
        # end if

        return status
    # end def status

    def _status(self):
        """
        Return the module's status.

        :return: module's status.
        :rtype: ``self.settings.status_type``
        """
        # Send request and get reply
        return self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                           msg_cmd=self.settings.msg_cmd_status)
    # end def _status

    @abstractmethod
    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``self.settings.status_type``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                 - (N/A) this base class method always returns an empty list.
        :rtype: ``list[str]``

        :raise ``AssertionError``: Invalid argument type
        """
        assert isinstance(status, self.settings.status_type), \
            f'Received {type(status)} but expected {self.settings.status_type}.\nstatus = {status}'
        error_list: List[str] = []
        return error_list
    # end def is_status_reply_valid

    def is_reset_reply_valid(self, status):
        """
        Validate Reset command's Status reply structure.

        :param status: Status structure
        :type status: ``self.settings.status_type``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                 - method `is_status_reply_valid()` returned a list of error
        :rtype: ``list[str]``
        """
        return self.is_status_reply_valid(status)
    # end def is_reset_reply_valid
# end class StatusResetModuleBaseClass


class BufferModuleBaseClass(StatusResetModuleBaseClass, metaclass=ABCMeta):
    """
    Kosmos Module base class for modules consuming data (Test Data => DUT)
    """

    # Set type hints
    _buffer: List

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Kosmos Consumer Module settings dataclass object
        :type module_settings: ``BufferModuleSettings``

        :raise ``AssertionError``: Invalid argument type
        """
        assert isinstance(module_settings, BufferModuleSettings), module_settings
        super().__init__(module_settings=module_settings)

        self._buffer = []
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``BufferModuleSettings``
        """
        return self._settings
    # end def property getter settings

    def append(self, data):
        """
        Append a data entry to the Module's local buffer.

        :param data: Data entry
        :type data: ``Any``

        :raise ``AssertionError``: Unexpected data type
        """
        assert isinstance(data, self.settings.data_type), (type(data), self.settings.data_type)
        self._buffer.append(data)
    # end def append

    def extend(self, data):
        """
        Append a list of data entries to the Module's local buffer.

        :param data: List of data entries
        :type data: ``list[Any]``

        :raise ``AssertionError``: Unexpected data type
        """
        assert isinstance(data, list), type(data)
        assert all([isinstance(d, self.settings.data_type) for d in data]), data
        self._buffer.extend(data)
    # end def extend

    def length(self):
        """
        Return the number of entries in the Module's local buffer.

        :return: number of entries in the Module's local buffer
        :rtype: ``int``
        """
        return len(self._buffer)
    # end def length

    def size(self):
        """
        Return the Module's remote buffer total capacity (max number of entries).

        :return: total capacity of Module's remote buffer
        :rtype: ``int``
        """
        return self.settings.buffer_size - 1
    # end def size

    def clear(self):
        """
        Empty the Module's local buffer.
        """
        self._buffer.clear()
    # end def clear

    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``self.settings.status_type``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - module FIFO count is out-of-bounds
                  - module Buffer count is out-of-bounds
        :rtype: ``list[str]``
        """
        error_list = super().is_status_reply_valid(status)

        if self.settings.fifo_size is not None and not (0 <= status.fifo_count <= self.settings.fifo_size):
            error_list.append(
                f'{self.name} FIFO count is out-of-bounds: got {status.fifo_count} items.')
        # end if

        if not (0 <= status.buffer_count <= self.settings.buffer_size):
            error_list.append(
                f'{self.name} Buffer count is out-of-bounds: got {status.buffer_count} items.')
        # end if

        return error_list
    # end def is_status_reply_valid

    def is_reset_reply_valid(self, status):
        """
        Validate Reset command's Status reply structure.

        :param status: Status structure
        :type status: ``self.settings.status_type``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - module FIFO is not empty
                  - module Buffer is not empty
        :rtype: ``list[str]``
        """
        error_list = super().is_reset_reply_valid(status)

        if self.settings.fifo_size is not None and status.fifo_count > 0:
            error_list.append(f'[{self.name}] FIFO is not empty: got {status.fifo_count} items.')
        # end if
        if status.buffer_count > 0:
            error_list.append(f'[{self.name}] Buffer is not empty: got {status.buffer_count} items.')
        # end if

        return error_list
    # end def is_reset_reply_valid
# end class BufferModuleBaseClass


class UploadModuleBaseClass(BufferModuleBaseClass, metaclass=ABCMeta):
    """
    Kosmos Module base class for modules having a buffer that can be uploaded to.
    """

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Kosmos Consumer Module settings dataclass object
        :type module_settings: ``UploadModuleSettings``

        :raise ``AssertionError``: Invalid argument type
        """
        assert isinstance(module_settings, UploadModuleSettings), module_settings
        super().__init__(module_settings=module_settings)
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``UploadModuleSettings``
        """
        return self._settings
    # end def property getter settings

    def send(self, clear=False):
        """
        Send the content of the local instruction buffer to the remote buffer.

        Note that the message replies content is checked by `FPGATransport.check_status_message_replies()` and may
        raise an exception.

        :param clear: Clear the local module's buffer after successful transfer, defaults to False - OPTIONAL
        :type clear: ``bool``
        """

        # Skip sending operation if there is no data to send
        if self.length() == 0:
            return
        # end if

        # Generate list of message from the instruction buffer
        tx_frames = self.messages()

        # Send datagram and get reply
        txrx_frames = self.dt.fpga_transport.send_control_message_list(tx_frames)

        # Check replies
        FPGATransport.check_status_message_replies(txrx_frames)

        # Clear buffer at end of sending operation - optional
        if clear:
            self.clear()
        # end if
    # end def send

    def messages(self):
        """
        Convert list of instructions into a list of `MessageFrame`.

        :return: List of `MessageFrame` containing the instructions
        :rtype: ``list[MessageFrame]``

        :raise ``AssertionError``: if local buffer count will not fit the remote buffer size
        """
        # For now, we assume that all the test instructions must fit in the Microblaze RAM.
        assert len(self._buffer) < self.settings.buffer_size, \
            f'[{self.name}] Local buffer (count={len(self._buffer)}) will not fit ' \
            f'remote buffer (size={self.settings.buffer_size}).'

        tx_frames = []
        tx_frame = None
        payload = None
        payload_len = self.settings.msg_cmd_write_max - self.settings.msg_cmd_write_one + 1
        for i, entry in enumerate(self._buffer):
            payload_index = i % payload_len
            # Prepare empty MessageFrame
            if payload_index == 0:
                tx_frame = MessageFrame()
                payload = getattr(tx_frame.frame.payload, self.settings.msg_payload_name)
            # end if

            # Fill payload
            self._set_message_payload(payload, payload_index, entry)

            # Push frame if payload full or not more instructions
            if payload_index == (payload_len - 1) or i == (len(self._buffer) - 1):
                tx_frame.frame.id = self.settings.msg_id
                tx_frame.frame.cmd = self.settings.msg_cmd_write_one + payload_index
                tx_frames.append(tx_frame)
            # end if
        # end for

        return tx_frames
    # end def messages

    @staticmethod
    def _set_message_payload(payload, payload_index, data):
        """
        Sets data in the payload, at a specified array index.
        This method can be overloaded if the data or the payload argument requires a different treatment.

        :param payload: Ctypes Array
        :type payload: ``ctypes.Array``
        :param payload_index: index of payload array
        :type payload_index: ``int``
        :param data: instruction data to be set in the payload
        :type data: ``Any``
        """
        payload[payload_index] = data
    # end def _set_message_payload

    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``self.settings.status_type``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - module FIFO is underrun
        :rtype: ``list[str]``
        """
        error_list = super().is_status_reply_valid(status)

        # FIXME: FIFOs underrun may not always indicate an error.
        #        A PES FIFO underrun is expected at the of the test.
        #        This is commented out for the moment - to be fixed.
        # if self.settings.fifo_size is not None and status.fifo_underrun:
        #     error_list.append(f'[{self.name}] FIFO is underrun.')
        # # end if

        return error_list
    # end def is_status_reply_valid
# end class UploadModuleBaseClass


class DownloadModuleBaseClass(StatusResetModuleBaseClass, metaclass=ABCMeta):
    """
    Kosmos Module base class for modules having a buffer that can be downloaded from.
    """

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Kosmos Producer Module settings dataclass object
        :type module_settings: ``DownloadModuleSettings``

        :raise ``AssertionError``: Invalid argument type
        """
        assert isinstance(module_settings, DownloadModuleSettings), module_settings
        super().__init__(module_settings=module_settings)
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``DownloadModuleSettings``
        """
        return self._settings
    # end def property getter settings

    def size(self):
        """
        Return the Module's remote buffer total capacity (max number of entries).

        :return: total capacity of Module's remote buffer
        :rtype: ``int``
        """
        return self.settings.buffer_size
    # end def size

    def download(self, count=None):
        """
        Download the entries stored in the remote Module's buffer.

        :param count: number of entries to be downloaded from remote buffer - OPTIONAL
                      If not provided, the whole buffer will be downloaded.
        :type count: ``int or None``

        :return: The list of downloaded entries
        :rtype: ``list[pes_timer_t]``

        :raise ``AssertionError``: If one of the following conditions occurs:
                                    - Unexpected argument type
                                    - Requesting to download more entries than the remote buffer can hold.
        :raise ``ExtractPayloadError``: If one of the following conditions occurs:
                                         - Download message reply is invalid or returned a specific return code
                                         - Received entry count differs from expectation.
        """
        m = self.settings  # notation shortcut

        # Get number of item to download
        if count is None:
            status = self.status()
            count = status.buffer_count
        else:
            assert isinstance(count, int), count
        # end if

        # Abort download if not needed
        if count < 1:
            return []
        # end if

        # Sanity check
        assert count < m.buffer_size, \
            f'[{m.name}] Cannot request more than {m.buffer_size} entries. Got count={count}.'

        # Compute the number of messages to be sent
        read_max = m.msg_cmd_read_max - m.msg_cmd_read_one + 1
        message_count = ceil(count / read_max)

        # Message template
        tx_frame = MessageFrame()
        tx_frame.frame.id = m.msg_id
        tx_frame.frame.cmd = m.msg_cmd_read_max

        # Create list of identical messages
        # Only one MessageFrame instance is used and referenced across all the list (except the last item).
        # This saves on memory and processing time.
        tx_frames = [tx_frame] * message_count

        # Last message may be different: the number of requested entries differs
        remainder = count % read_max
        if remainder > 0:
            tx_frames[-1] = MessageFrame()  # Create a different instance
            tx_frames[-1].frame.id = m.msg_id
            tx_frames[-1].frame.cmd = (m.msg_cmd_read_one - 1) + remainder
        # end if

        # Send datagram and get reply
        txrx_frames = self.dt.fpga_transport.send_control_message_list(tx_frames)

        # Parse reply frames
        entries = []
        for i, (tx_frame, rx_frame) in enumerate(txrx_frames):
            # Sanity checks
            error_list = self._is_download_reply_valid(rx_frame)
            if error_list:
                error_list.append(f'TX[{i}]: {tx_frame.str_raw_memory()}')
                error_list.append(f'RX[{i}]: {rx_frame.str_raw_memory()}')
                raise ExtractPayloadError('\n'.join(error_list))
            # end if

            # Extract entries
            msg_cmd = rx_frame.frame.cmd & (~ MSG_CMD_REPLY_FLAG)  # Clear 'MSG_CMD_REPLY_FLAG' bit
            payload_entry_count = msg_cmd - (m.msg_cmd_read_one - 1)
            payload = rx_frame.get_payload()[0:payload_entry_count]
            entries.extend(payload)
        # end for

        # Sanity check
        if not count == len(entries):
            raise ExtractPayloadError(f'[{m.name}] Requested {count} entries, got {len(entries)}.')
        # end if

        return entries
    # end def download

    def _is_download_reply_valid(self, rx_frame):
        """
        Validate download message reply.

        :param rx_frame: Download message reply
        :type rx_frame: ``MessageFrame``

        :return: Empty list if message is valid; List of error strings if any of the following conditions is met:
                  - Unexpected MessageFrame ID
                  - Unexpected MessageFrame CMD
        :rtype: ``list[str]``

        :raise ``AssertionError``: Invalid argument type
        """
        assert isinstance(rx_frame, MessageFrame), rx_frame

        frame_cmd = rx_frame.frame.cmd
        frame_id = rx_frame.frame.id
        msg_cmd = frame_cmd & ~MSG_CMD_REPLY_FLAG  # Clear 'MSG_CMD_REPLY_FLAG' bit
        error_list = []

        if frame_id == MSG_ID_STATUS and msg_cmd == MSG_ID_STATUS_CMD_REPLY:
            return_code = rx_frame.frame.payload.msg_reply.return_code
            error_list.append(
                f'[{self.name}] Unexpected Status Message, with return code {return_code:#04x}:'
                f'{msg_reply_return_code_e__enumvalues.get(return_code, "?")}.')
        else:
            if frame_id != self.settings.msg_id:
                # FIXME: usage of msg_id_e__enumvalues is deprecated
                error_list.append(
                    f'[{self.name}] Unexpected MessageFrame ID, got {frame_id:#04x}:'
                    f'{msg_id_e__enumvalues.get(frame_id, "?")}, expected {self.settings.msg_id:#04x}:'
                    f'{msg_id_e__enumvalues.get(self.settings.msg_id, "?")}.')
            # end if
            if not (frame_cmd & MSG_CMD_REPLY_FLAG):
                error_list.append(
                    f'[{self.name}] Unexpected MessageFrame CMD, got {frame_cmd:#04x}, '
                    f'expected REPLY flag set.')
            elif not (self.settings.msg_cmd_read_one <= msg_cmd <= self.settings.msg_cmd_read_max):
                error_list.append(
                    f'[{self.name}] Unexpected MessageFrame CMD, got {msg_cmd:#04x}, '
                    f'expected value in [{self.settings.msg_cmd_read_one:#04x}, '
                    f'{self.settings.msg_cmd_read_max:#04x}] (ignoring REPLY flag).')
            # end if
        # end if

        return error_list
    # end def _is_download_reply_valid

    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``self.settings.status_type``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - module FIFO is overrun
                  - module Buffer is overrun
        :rtype: ``list[str]``
        """
        error_list = super().is_status_reply_valid(status)

        if self.settings.fifo_size is not None and status.fifo_overrun:
            error_list.append(f'[{self.name}] FIFO is overrun.')
        # end if
        if status.buffer_overrun:
            error_list.append(f'[{self.name}] Buffer is overrun.')
        # end if

        return error_list
    # end def is_status_reply_valid
# end class DownloadModuleBaseClass


class ConsumerModuleBaseClass(UploadModuleBaseClass, metaclass=ABCMeta):
    """
    Kosmos Module base class for modules consuming data (Test Data => DUT)
    """

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Kosmos Consumer Module settings dataclass object
        :type module_settings: ``ConsumerModuleSettings``

        :raise ``AssertionError``: Invalid argument type
        """
        assert isinstance(module_settings, ConsumerModuleSettings), module_settings
        super().__init__(module_settings=module_settings)
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``ConsumerModuleSettings``
        """
        return self._settings
    # end def property getter settings
# end class ConsumerModuleBaseClass


class ProducerModuleBaseClass(DownloadModuleBaseClass, metaclass=ABCMeta):
    """
    Kosmos Module base class for modules producing data (Test Data <= DUT)
    """

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Kosmos Producer Module settings dataclass object
        :type module_settings: ``ProducerModuleSettings``

        :raise ``AssertionError``: Invalid argument type
        """
        assert isinstance(module_settings, ProducerModuleSettings), module_settings
        super().__init__(module_settings=module_settings)
    # end def __init__

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``ProducerModuleSettings``
        """
        return self._settings
    # end def property getter settings

    def start_capture(self):
        """
        Start the module capture immediately, bypassing Sequencer module.

        Actions:
          - Unmask all module interrupt sources
          - Enable module FPGA state machine

        :return: Module's status after start of the module.
        :rtype: ``self.settings.status_type``

        :raise ``AssertionError``: Invalid or unexpected status values, after start of the module
        """
        # Send request
        status = self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                             msg_cmd=self.settings.msg_cmd_start)

        # Sanity checks
        error_list = self.is_status_reply_valid(status)
        if not status.state == self.settings.status_state_started:
            error_list.append(
                f'[{self.name}] Unexpected module state: {status.state:#04x}:'
                f'{self.settings.status_state_enumvalues.get(status.state, "?")}.')
        # end if
        assert not error_list, '\n'.join(error_list)

        return status
    # end def start_capture

    def stop_capture(self):
        """
        Stop the module capture immediately, bypassing Sequencer module.

        Actions:
          - Reset & hold internal module FPGA state machine
          - Preserve module buffer and FIFO content
          - Preserve module interrupt source state

        :return: Module's status after stop of the module.
        :rtype: ``self.settings.status_type``

        :raise ``AssertionError``: Invalid or unexpected status values, after stop of the module
        """
        # Send request
        status = self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                             msg_cmd=self.settings.msg_cmd_stop)

        # Sanity checks
        error_list = self.is_status_reply_valid(status)
        if not status.state == self.settings.status_state_reset_or_stop:
            error_list.append(
                f'[{self.name}] Unexpected module state: {status.state:#04x}:'
                f'{self.settings.status_state_enumvalues.get(status.state, "?")}.')
        # end if
        assert not error_list, '\n'.join(error_list)

        return status
    # end def stop_capture
# end class ProducerModuleBaseClass


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
