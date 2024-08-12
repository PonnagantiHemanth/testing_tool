#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.i2cspy
:brief: Kosmos I2C SPY Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/12/01
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from ctypes import c_uint8
from dataclasses import dataclass

from pyraspi.services.kosmos.i2cspyparser import I2cSpyFrameParser
from pyraspi.services.kosmos.i2cspyparser import I2cSpyRawParser
from pyraspi.services.kosmos.module.devicetree import DeviceTreeGenericModuleBaseClass
from pyraspi.services.kosmos.module.module import DownloadModuleBaseClass
from pyraspi.services.kosmos.module.module import DownloadModuleSettings
from pyraspi.services.kosmos.module.module import ProducerModuleBaseClass
from pyraspi.services.kosmos.module.module import ProducerModuleSettings
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEvent
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventMapInterface
from pyraspi.services.kosmos.module.pescpuevents import PesCpuEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesActionEvent
from pyraspi.services.kosmos.module.pesevents import PesEventMapInterface
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_BUFFER_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_FIFO_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_MODE_FRAME
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_MODE_RAW
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_REG_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_STATE_RESET_OR_STOP
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_STATE_STARTED
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_CMD_MODE_FRAME
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_CMD_MODE_RAW
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_CMD_READ_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_CMD_READ_MAX
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_CMD_START
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_CMD_STOP
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_FRAME_CMD_READ_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_I2C_SPY_FRAME_CMD_READ_MAX
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_I2C_SPY_FIFO_FLUSH
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_mode_e
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_mode_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_reg_t
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_state_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_status_t

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

I2C_SPY_MODE_TO_MSG_CMD_MAP = {I2C_SPY_MODE_RAW: MSG_ID_I2C_SPY_CMD_MODE_RAW,
                               I2C_SPY_MODE_FRAME: MSG_ID_I2C_SPY_CMD_MODE_FRAME}

I2C_SPY_MODE_TO_PARSER_MAP = {I2C_SPY_MODE_RAW: I2cSpyRawParser,
                              I2C_SPY_MODE_FRAME: I2cSpyFrameParser}


@dataclass(frozen=True)
class I2cSpyActionEvent(PesEventMapInterface):
    """
    PES Action Events for I2C SPY module
    """
    RESET: PesActionEvent = None
    START: PesActionEvent = None
    STOP: PesActionEvent = None
# end class I2cSpyActionEvent


@dataclass(frozen=True)
class I2cSpyResumeEvent(PesEventMapInterface):
    """
    PES Resume Events for I2C SPY module
    """
    pass
# end class I2cSpyResumeEvent


@dataclass(frozen=True)
class I2cSpyCpuEvent(PesCpuEventMapInterface):
    """
    PES-CPU Events for I2C SPY module
    """
    FLUSH_FIFO: PesCpuEvent = PES_CPU_ACTION_I2C_SPY_FIFO_FLUSH
# end class I2cSpyCpuEvent

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class I2cSpyModule(PesEventModuleInterface,
                   PesCpuEventModuleInterface,
                   ProducerModuleBaseClass,
                   DeviceTreeGenericModuleBaseClass):
    """
    Kosmos I2C SPY module class (RAW model).
    """

    # PES Event maps related to the current module
    action_event = I2cSpyActionEvent
    resume_event = I2cSpyResumeEvent

    # PES CPU Event map related to the current module
    cpu_event = I2cSpyCpuEvent

    def __init__(self, msg_id, instance_id=None, name=r'I2C SPY'):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton - OPTIONAL
        :type instance_id: ``int``
        :param name: Module given name - OPTIONAL
        :type name: ``str``
        """
        module_settings = ProducerModuleSettings(
            name=name,
            instance_id=instance_id,
            optional=True,
            msg_id=msg_id,
            buffer_size=(I2C_SPY_BUFFER_SIZE - 1),
            fifo_size=(I2C_SPY_FIFO_SIZE - 1),
            status_type=i2c_spy_status_t,
            status_state_reset_or_stop=I2C_SPY_STATE_RESET_OR_STOP,
            status_state_started=I2C_SPY_STATE_STARTED,
            status_state_enumvalues=i2c_spy_state_e__enumvalues,
            msg_cmd_status=MSG_ID_I2C_SPY_CMD_STATUS,
            msg_cmd_reset=MSG_ID_I2C_SPY_CMD_RESET,
            msg_cmd_start=MSG_ID_I2C_SPY_CMD_START,
            msg_cmd_stop=MSG_ID_I2C_SPY_CMD_STOP,
            msg_cmd_read_one=MSG_ID_I2C_SPY_CMD_READ_1,
            msg_cmd_read_max=MSG_ID_I2C_SPY_CMD_READ_MAX,
            data_type=i2c_spy_reg_t,
        )
        super().__init__(module_settings=module_settings)
    # end def __init__

    def flush_fifo_to_buffer(self):
        """
        Add a PES CPU Action: flush all remote FIFO entries into the remote buffer.
        """
        self.dt.pes_cpu.action(self.cpu_event.FLUSH_FIFO)
    # end def flush_fifo_to_buffer
# end class I2cSpyModule


class I2cSpyFrameModule(DownloadModuleBaseClass):
    """
    Kosmos I2C SPY module class (FRAME model).
    """

    def __init__(self, msg_id, instance_id=None, name=r'I2C SPY FRAME'):
        """
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton - OPTIONAL
        :type instance_id: ``int``
        :param name: Module given name - OPTIONAL
        :type name: ``str``
        """
        module_settings = DownloadModuleSettings(
            name=name,
            instance_id=instance_id,
            msg_id=msg_id,
            optional=True,
            buffer_size=((I2C_SPY_BUFFER_SIZE - 1) * I2C_SPY_REG_SIZE),
            fifo_size=(I2C_SPY_FIFO_SIZE - 1),
            status_type=i2c_spy_status_t,
            msg_cmd_status=MSG_ID_I2C_SPY_CMD_STATUS,
            msg_cmd_reset=MSG_ID_I2C_SPY_CMD_RESET,
            msg_cmd_read_one=MSG_ID_I2C_SPY_FRAME_CMD_READ_1,
            msg_cmd_read_max=MSG_ID_I2C_SPY_FRAME_CMD_READ_MAX,
            data_type=c_uint8,
        )
        super().__init__(module_settings=module_settings)
    # end def __init__

    def download(self, count=None):
        """
        Download the remote buffer content (I2C frames), at a byte level.

        :param count: number of entries to be downloaded from remote buffer - OPTIONAL
                      If not provided, the whole buffer will be downloaded.
        :type count: ``int or None``

        :return: Byte array of raw I2C frames
        :rtype: ``bytearray``
        """
        return bytearray(super().download(count=count))
    # end def download
# end class I2cSpyFrameModule


class I2cSpyExtendedModule(I2cSpyModule):
    """
    Kosmos I2C SPY Extended module class.
    This class holds and addresses the two variants `I2cSpyModule`and `I2cSpyFrameModule`.

    Note: The module operating mode is `I2C_SPY_MODE_RAW` by default. Call `mode()` property to change it.
    """
    _mode: i2c_spy_mode_e
    _frame: I2cSpyFrameModule

    def __init__(self, fpga_clock_freq_hz, msg_id, instance_id=None, name=r'I2C SPY'):
        """
        :param fpga_clock_freq_hz: FPGA core frequency in Hz
        :type fpga_clock_freq_hz: ``int``
        :param msg_id: Protocol Message ID
        :type msg_id: ``int``
        :param instance_id: Module instance identifier number, None if singleton - OPTIONAL
        :type instance_id: ``int``
        :param name: Module given name - OPTIONAL
        :type name: ``str``
        """
        super().__init__(msg_id=msg_id, instance_id=instance_id, name=name)
        self._fpga_clock_freq_hz = fpga_clock_freq_hz
        self._frame = I2cSpyFrameModule(msg_id=msg_id, instance_id=instance_id, name=f'{name} FRAME')

        self.__reset_mode()
        self.register_reset_callback(self.__reset_mode)
    # end def __init__

    def init_device_tree(self, dt):
        """
        Set Device Tree in this I2cSpyModule instance and also in I2cSpyFrameModule sub-instance.

        :param dt: Kosmos Module Device Tree
        :type dt: ``DeviceTree``
        """
        super().init_device_tree(dt=dt)
        self._frame.init_device_tree(dt=dt)
    # end def init_device_tree

    def download(self, count=None):
        """
        Download the remote I2C buffer content.
        The return type depends on the module's mode of operation. Refer to ``mode`` property.

        :param count: number of entries to be downloaded from remote buffer - OPTIONAL
                      If not provided, the whole buffer will be downloaded.
        :type count: ``int or None``

        :return: List of I2C SPY register entries or a byte array of raw I2C frames
        :rtype: ``list[i2c_spy_reg_t] or bytearray``
        """
        if self.mode == I2C_SPY_MODE_RAW:
            return super().download(count=count)
        else:
            return self._frame.download(count=count)
        # end if
    # end def download

    def status(self, sanity_checks=True):
        """
        Return the module's status.

        :param sanity_checks: If True, run sanity checks on the status reply and raise an error if something is wrong.
                              If False, skip sanity checks. Defaults to True - OPTIONAL
        :type sanity_checks: ``bool``

        :return: module's status.
        :rtype: ``i2c_spy_status_t``
        """
        if self.mode == I2C_SPY_MODE_RAW:
            return super().status(sanity_checks=sanity_checks)
        else:
            return self._frame.status(sanity_checks=sanity_checks)
        # end if
    # end def status

    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``i2c_spy_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
                  - remote module mode does not match local module mode
        :rtype: ``list[str]``
        """
        error_list = super().is_status_reply_valid(status)

        if status.mode != self.mode:
            error_list.append(f'[{self.name}] MODE mismatch. '
                              f'Remote:{status.mode}:{i2c_spy_mode_e__enumvalues.get(status.mode, "?")}, '
                              f'Local:{self.mode}:{i2c_spy_mode_e__enumvalues.get(self.mode, "?")}.')
        # end if

        return error_list
    # end def is_status_reply_valid

    def size(self):
        """
        Return the Module's remote buffer total capacity (max number of entries).

        :return: total capacity of Module's remote buffer
        :rtype: ``int``
        """
        if self.mode == I2C_SPY_MODE_RAW:
            return super().size()
        else:
            return self._frame.size()
        # end if
    # end def size

    def get_parser(self):
        """
        Return an I2C SPY Frame parser depending on the current module operating mode.

        :return: I2C SPY Frame parser depending on the current module operating mode
        :rtype: ``I2cSpyRawParser or I2cSpyFrameParser``
        """
        parser = I2C_SPY_MODE_TO_PARSER_MAP[self.mode]
        return parser(fpga_clock_freq_hz=self._fpga_clock_freq_hz)
    # end def get_parser

    @property
    def mode(self):
        """
        Get the I2C SPY module mode: Raw or Frame.

        :return: I2C SPY module mode, refer to ``i2c_spy_mode_e__enumvalues``.
        :rtype: ``i2c_spy_mode_e``
        """
        return self._mode
    # end def property getter mode

    @mode.setter
    def mode(self, mode):
        """
        Set the I2C SPY module operating mode.

        :param mode: I2C SPY module mode, refer to ``i2c_spy_mode_e__enumvalues``.
        :type mode: ``i2c_spy_mode_e``

        :raise ``AssertionError``: Unexpected status values
        """
        assert mode in i2c_spy_mode_e__enumvalues, mode

        # Set local mode
        self._mode = mode

        # Send request to set remote mode
        status = self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                             msg_cmd=I2C_SPY_MODE_TO_MSG_CMD_MAP[mode])

        # Sanity checks
        error_list = self.is_status_reply_valid(status)
        assert not error_list, '\n'.join(error_list)
    # end def property setter mode

    # Private method declaration
    def __reset_mode(self):
        """
        Reset mode to default RAW mode.
        Note: NEVER call this method from anywhere else than this module's init method and reset callback.
        """
        self._mode = I2C_SPY_MODE_RAW
    # end def __reset_mode
# end class I2cSpyExtendedModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
