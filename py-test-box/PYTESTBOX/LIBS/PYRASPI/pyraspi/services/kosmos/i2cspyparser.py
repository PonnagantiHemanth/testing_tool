#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.i2cspyparser
:brief: Kosmos I2C SPY PARSER Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/05/01
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Iterable
from ctypes import sizeof
from enum import IntEnum
from enum import auto
from enum import unique
from typing import List
from typing import Optional

from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_ACK
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_DATA
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_IDLE
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_INIT
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_NACK
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_START
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_STOP
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_frame_header_t
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_reg_t
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_sm_state_e__enumvalues


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class I2cSpyFrame(bytearray):
    """
    I2C SPY Frame class: data representation of an I2C frame
    """
    time: float
    nack: bool

    def __init__(self, data=None, time=0., nack=False):
        """
        :param data: byte sequence representing the complete I2C Frame data - OPTIONAL
        :type data: ``bytearray or bytes or Iterable or None``
        :param time: time taken at the beginning of the I2C Frame, in seconds - OPTIONAL
        :type time: ``float``
        :param nack: flag raised if one or more NACKs occurred during the I2C Frame transfer - OPTIONAL
        :type nack: ``bool``

        :raise ``AssertionError``: wrong parameter type or invalid value
        """
        assert isinstance(time, float) and time >= 0., time
        self.time = time

        assert isinstance(nack, bool), nack
        self.nack = nack

        if data is None:
            super().__init__()
        else:
            super().__init__(data)
        # end if
    # end def __init__

    def __str__(self):
        """
        Return the string representation of the I2C Frame.

        Example outputs:
          [1.123456] AB CD 12 34
          [2.345678] NACK AB CD 12 34

        :return: String representation of the I2C Frame
        :rtype: ``str``
        """
        str_out = f'[{self.time:.6f}] '
        if self.nack:
            str_out += r'NACK '
        # end if
        str_out += r' '.join(f'{byte:02x}' for byte in self)
        return str_out
    # end def __str__
# end class I2cSpyFrame


class I2cSpyFrameRun(List):
    """
    I2C SPY Frame Run class: this represents a sequence of I2C Frames
    """
    time: float

    def __init__(self, time=0., frames=None):
        """
        :param time: time taken at the beginning of the I2C Frame Run, in seconds - OPTIONAL
        :type time: ``float``
        :param frames: Sequence of I2C Frames that composes an I2C Frame Run - OPTIONAL
        :type frames: ``List or Iterable or None``

        :raise ``AssertionError``: wrong parameter type or invalid value
        """
        assert isinstance(time, float) and time >= 0., time
        self.time = time

        if frames is None:
            super().__init__()
        else:
            assert all(isinstance(f, I2cSpyFrame) for f in frames), frames
            super().__init__(frames)
        # end if
    # end def __init__

    def __str__(self):
        """
        Return the short string representation of the I2C Frame Run (header).

        Example output:
          RUN: 12 frames, from 0.123456 to 4.567891, total 4.444435

        :return: Short string representation of the I2C Frame Run
        :rtype: ``str``
        """
        start = self.time
        end = self[-1].time if len(self) else start
        total = (end - start)
        return f'RUN: {len(self)} frames, ' \
               f'from {start:.6f} s to {end:.6f} s, ' \
               f'total {total:.6f} s.'
    # end def __str__

    def __repr__(self):
        """
        Return the full string representation of the I2C Frame Run (header + data).

        Example output:
          RUN: 3 frames, from 0.123456 to 6.789123, total 6.665667
          [000][0.123456] AB CD 12 34
          [001][4.567891] NACK AB CD 12 34
          [001][6.789123] 45 56 78 EF AC 45

        :return: Full string representation of the I2C Frame Run
        :rtype: ``str``
        """
        return '\n'.join(self.to_str_list(print_header=True))
    # end def __repr__

    def to_str_list(self, run_index=None, print_header=False):
        """
        Return a list of strings representing the I2C Frame Run.

        :param run_index: prefix number to be added in front of each line - OPTIONAL
        :type run_index: ``int or None``
        :param print_header: select if the I2C Frame Run header should be included in the list - OPTIONAL
        :type print_header: ``bool``

        :return: list of strings representing the I2C Frame Run
        :rtype: ``list[str]``
        """
        header = [str(self)] if print_header else []
        run_idx = f'[{run_index:03d}]' if isinstance(run_index, int) else r''
        frames = [f'{run_idx}[{i:04d}]{str(frame)}' for i, frame in enumerate(self)]
        return header + frames
    # end def to_str_list
# end class I2cSpyFrameRun


class I2cSpyFrameParserMixin(metaclass=ABCMeta):
    """
    I2C SPY Frame Parser base interface class
    """
    frame_runs: List[I2cSpyFrameRun]
    _frame: Optional[I2cSpyFrame]
    _last_timestamp: int
    _fpga_clock_freq_hz: int

    def __init__(self, fpga_clock_freq_hz):
        """
        :param fpga_clock_freq_hz: FPGA clock frequency in Hertz
        :type fpga_clock_freq_hz: ``int``
        """
        self.frame_runs = []
        self._frame = None
        self._last_timestamp = 0
        self._fpga_clock_freq_hz = fpga_clock_freq_hz
    # end def __init__

    def timestamp_to_time(self, timestamp):
        """
        Convert a I2C SPY timestamp into a relative time expressed in seconds.

        :param timestamp:  I2C SPY timestamp, which tick unit is 2^12 FPGA clock ticks
        :type timestamp: ``int``

        :return: time expressed in seconds
        :rtype: ``float``
        """
        return (timestamp << 12) / self._fpga_clock_freq_hz
    # end def timestamp_to_time

    @abstractmethod
    def parse(self, array):
        """
        Convert I2C buffer content into I2C frames.

        :param array: I2C capture buffer
        :type array: ``Iterable``

        :return: parsed frame count
        :rtype: ``int``

        :raise ``AssertionError``: Unknown I2C state
        """
        raise NotImplementedError('User must define `parse` method to use this base class')
    # end def parse

    def __str__(self):
        """
        Return the short string representation of the I2C Frame Parser state (header).

        Example output:
          I2C PARSER: 12 runs, 6 frames, running for 1.123456 s.

        :return: Short string representation of the I2C Frame Parser
        :rtype: ``str``
        """
        start = end = 0
        if len(self.frame_runs):
            start = self.frame_runs[0].time
            if len(self.frame_runs[-1]):
                end = self.frame_runs[-1][-1].time
            else:
                end = self.frame_runs[-1].time
            # end if
        # end if
        total = (end - start)
        return r'I2C PARSER: ' \
               f'{len(self.frame_runs)} runs, ' \
               f'{sum([len(run) for run in self.frame_runs])} frames, ' \
               f'running for {total:.6f} s.'
    # end def __str__

    def __repr__(self):
        """
        Return the full string representation of the I2C Frame Runs (header + data).

        Example output:
          I2C PARSER: 2 runs, 5 frames, running for 7.665667 s.
          RUN: 3 frames, from 0.123456 to 6.789123, total 6.665667
          [0000][000][0.123456] AB CD 12 34
          [0000][001][4.567891] NACK AB CD 12 34
          [0000][001][6.789123] 45 56 78 EF AC 45
          RUN: 2 frames, from 7.123456 to 8.123456, total 1.000000
          [0001][000][7.123456] AB CD 12 34
          [0001][001][8.123456] NACK AB CD 12 34

        :return: Full string representation of the I2C Frame Runs
        :rtype: ``str``
        """
        return '\n'.join(self.to_str_list(print_header=True))
    # end def __repr__

    def to_str_list(self, print_header=False):
        """
        Return a list of strings representing the I2C Frame Runs.

        :param print_header: select if the I2C Frame Run & Parser headers should be included in the list - OPTIONAL
        :type print_header: ``bool``

        :return: list of strings representing the I2C Frame Runs
        :rtype: ``list[str]``
        """
        header = [str(self)] if print_header else []
        runs = []
        for i, run in enumerate(self.frame_runs):
            runs.extend(run.to_str_list(run_index=i, print_header=print_header))
        # end for
        return header + runs
    # end def to_str_list
# end class I2cSpyFrameParserMixin


class I2cSpyFrameParser(I2cSpyFrameParserMixin):
    """
    I2C SPY frame parser class, dedicated for input data arranged in sequence of frames (FRAME mode).
    """
    _header: i2c_spy_frame_header_t
    _header_index: int
    _data_index: int

    def __init__(self, fpga_clock_freq_hz):
        """
        :param fpga_clock_freq_hz: FPGA clock frequency in Hertz
        :type fpga_clock_freq_hz: ``int``
        """
        super().__init__(fpga_clock_freq_hz=fpga_clock_freq_hz)
        self._header = i2c_spy_frame_header_t()
        self._header_index = 0
        self._data_index = 0
    # end def __init__

    def parse(self, i2c_buffer):
        """
        Convert I2C buffer content into I2C frames.

        :param i2c_buffer: I2C capture buffer (FRAME mode)
        :type i2c_buffer: ``bytes or bytearray or Iterable``

        :return: parsed frame count
        :rtype: ``int``

        :raise ``AssertionError``: Unknown I2C state
        """
        frame_count = 0
        time = 0.

        for i, data in enumerate(i2c_buffer):
            assert 0 <= data <= 0xFF, f'Out of range data: {data:#08x}.'

            # Parse I2C Frame header
            if self._header_index < sizeof(i2c_spy_frame_header_t):
                self._header.raw[self._header_index] = data
                self._header_index += 1

                # Read header when its parsing is complete
                if self._header_index == sizeof(i2c_spy_frame_header_t):
                    # Convert time
                    time = self.timestamp_to_time(timestamp=self._header.field.timestamp)

                    # Detect timer wrap
                    assert self._header.field.timestamp >= self._last_timestamp, \
                        f'[{i}] Current timestamp {self._header.field.timestamp:#010x} ({time:.6f} s) is smaller ' \
                        f'than previous timestamp {self._last_timestamp:#010x} ' \
                        f'({self.timestamp_to_time(timestamp=self._last_timestamp):.6f} s).'
                    self._last_timestamp = self._header.field.timestamp

                    # Handle special INIT state
                    if self._header.field.length == 0:
                        assert not self._header.field.nack, str(self._header)
                        # Create new run with start time, but no frame
                        self.frame_runs.append(I2cSpyFrameRun(time=time))
                        self._header_index = 0
                        time = None
                    # end if
                # end if

            # Parse I2C Frame data
            else:
                # Append data to I2C frame
                if self._data_index < self._header.field.length:
                    if self._frame is None:
                        # Get time from header
                        time = self.timestamp_to_time(timestamp=self._header.field.timestamp)
                        # Create new Frame
                        self._frame = I2cSpyFrame(time=time, nack=bool(self._header.field.nack))
                    # end if
                    self._frame.append(data)
                    self._data_index += 1

                    # Save I2C frame if complete
                    if self._data_index == self._header.field.length:
                        if len(self.frame_runs) == 0:
                            # Create new run from current frame data and time.
                            self.frame_runs.append(I2cSpyFrameRun(frames=[self._frame], time=self._frame.time))
                        else:
                            # Append current frame to last run
                            self.frame_runs[-1].append(self._frame)
                        # end if
                        self._frame = None
                        self._header_index = 0
                        self._data_index = 0
                        frame_count += 1
                    # end if
                # end if
            # end if
        # end for

        return frame_count
    # end def parse
# end class I2cSpyFrameParser


class I2cSpyRawParser(I2cSpyFrameParserMixin):
    """
    I2C SPY frame parser class, dedicated for raw data input (RAW mode).
    """
    @unique
    class STATE(IntEnum):
        """
        States of I2C SPY (raw mode) state machine
        """
        WAIT_FOR_START = auto()
        WAIT_FOR_DATA_STOP_RESTART = auto()
        WAIT_FOR_ACK_NACK = auto()
    # end class STATE

    _parser_state: STATE
    _work_frame: Optional[I2cSpyFrame]

    def __init__(self, fpga_clock_freq_hz):
        """
        :param fpga_clock_freq_hz: FPGA clock frequency in Hertz
        :type fpga_clock_freq_hz: ``int``
        """
        super().__init__(fpga_clock_freq_hz=fpga_clock_freq_hz)
        self._parser_state = self.STATE.WAIT_FOR_START
        self._work_frame = None
    # end def __init__

    def parse(self, i2c_buffer):
        """
        Convert I2C buffer content into I2C frames.

        :param i2c_buffer: I2C capture buffer (RAW mode)
        :type i2c_buffer: ``List[i2c_spy_reg_t]``

        :return: parsed frame count
        :rtype: ``int``

        :raise ``AssertionError``: Unknown I2C state
        :raise ``IndexError``: Invalid I2C parser state
        :raise ``ValueError``: Unexpected I2C register state
        """
        frame_count = 0
        time = 0.

        for i, reg in enumerate(i2c_buffer):
            reg_state = reg.field.state
            assert reg_state in i2c_spy_sm_state_e__enumvalues, f'[{i}] Unknown I2C register state {reg_state}.'
            assert reg_state != I2C_SPY_SM_STATE_IDLE, f'[{i}] Invalid I2C register state I2C_SPY_SM_STATE_IDLE.'

            # Convert time
            if reg_state != I2C_SPY_SM_STATE_DATA:
                time = self.timestamp_to_time(timestamp=reg.timestamp)

                # Detect timer wrap
                assert reg.timestamp >= self._last_timestamp, \
                    f'[{i}] Current timestamp {reg.timestamp:#010x} ({time:.6f} s) is smaller than ' \
                    f'previous timestamp {self._last_timestamp:#010x} ' \
                    f'({self.timestamp_to_time(timestamp=self._last_timestamp):.6f} s).'
                self._last_timestamp = reg.timestamp
            # end if

            # Handle special INIT state
            if reg_state == I2C_SPY_SM_STATE_INIT:
                # Create new frame run with a start time, but no frame yet
                self.frame_runs.append(I2cSpyFrameRun(time=time))
                self._parser_state = self.STATE.WAIT_FOR_START
                continue
            # end if

            # I2C Register Parser state machine
            if self._parser_state == self.STATE.WAIT_FOR_START:
                if reg_state == I2C_SPY_SM_STATE_START:
                    self._frame = I2cSpyFrame(time=time)
                    self._parser_state = self.STATE.WAIT_FOR_DATA_STOP_RESTART
                else:
                    # Ignore reg entries that are not a START condition.
                    pass
                # end if

            elif self._parser_state == self.STATE.WAIT_FOR_DATA_STOP_RESTART:
                if reg_state == I2C_SPY_SM_STATE_DATA:
                    self._frame.append(reg.field.data)
                    self._parser_state = self.STATE.WAIT_FOR_ACK_NACK
                elif reg_state in [I2C_SPY_SM_STATE_START, I2C_SPY_SM_STATE_STOP]:
                    assert len(self._frame) > 0, f'[{i}] Empty I2C frame is invalid.'
                    # Save I2C frame in a frame run
                    if len(self.frame_runs) == 0:
                        # Create first frame run from current frame data and time.
                        self.frame_runs.append(I2cSpyFrameRun(frames=[self._frame], time=self._frame.time))
                    else:
                        # Append current frame to last frame run
                        self.frame_runs[-1].append(self._frame)
                    # end if
                    frame_count += 1

                    # Handle repeated start condition
                    if reg_state == I2C_SPY_SM_STATE_START:
                        self._frame = I2cSpyFrame(time=time)
                        self._parser_state = self.STATE.WAIT_FOR_DATA_STOP_RESTART
                    else:
                        self._parser_state = self.STATE.WAIT_FOR_START
                    # end if
                else:
                    raise ValueError(f'[{i}] Unexpected I2C register state '
                                     f'<{i2c_spy_sm_state_e__enumvalues.get(reg_state, "?")}: {reg_state}>, '
                                     f'for parser state {repr(self._parser_state)}.')
                # end if

            elif self._parser_state == self.STATE.WAIT_FOR_ACK_NACK:
                if reg_state == I2C_SPY_SM_STATE_ACK:
                    pass
                elif reg_state == I2C_SPY_SM_STATE_NACK:
                    self._frame.nack = True
                else:
                    raise ValueError(f'[{i}] Unexpected I2C register state '
                                     f'<{i2c_spy_sm_state_e__enumvalues.get(reg_state, "?")}: {reg_state}>, '
                                     f'for parser state {repr(self._parser_state)}.')
                # end if
                self._parser_state = self.STATE.WAIT_FOR_DATA_STOP_RESTART

            else:
                raise IndexError(f'[{i}] Invalid I2C parser state {repr(self._parser_state)}.')
            # end if
        # end for

        return frame_count
    # end def parse
# end class I2cSpyRawParser

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
