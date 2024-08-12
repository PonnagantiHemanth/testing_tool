#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.i2cspyparser_test
:brief: Tests for Kosmos I2C SPY Parser class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/08/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase

from pyraspi.services.kosmos.i2cspyparser import I2cSpyFrame
from pyraspi.services.kosmos.i2cspyparser import I2cSpyFrameParser
from pyraspi.services.kosmos.i2cspyparser import I2cSpyRawParser
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_ACK
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_DATA
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_IDLE
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_INIT
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_NACK
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_START
from pyraspi.services.kosmos.protocol.generated.messages import I2C_SPY_SM_STATE_STOP
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_frame_header_t
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_reg_t

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
VERBOSE = False
FREQ = (1 << 12)  # Hz, arbitrary


def i2c_ctrl(state=I2C_SPY_SM_STATE_INIT, timestamp=0):
    """
    Utility function for KosmosI2cSpyRawParserTestCase

    :param state: I2C SPY state, defaults to `I2C_SPY_SM_STATE_INIT` - OPTIONAL
    :type state: ``int``
    :param timestamp: timestamp , defaults to 0 - OPTIONAL
    :type timestamp: ``int``

    :return: I2C SPY data structure
    :rtype: ``i2c_spy_reg_t``
    """
    reg = i2c_spy_reg_t()
    reg.field.state = state
    reg.timestamp = timestamp
    return reg
# end def i2c_ctrl


def i2c_data(data=0x00):
    """
    Utility function for KosmosI2cSpyRawParserTestCase

    :param data: I2C SPY data, defaults to 0x00 - OPTIONAL
    :type data: ``int``

    :return: I2C SPY data structure
    :rtype: ``i2c_spy_reg_t``
    """
    reg = i2c_spy_reg_t()
    reg.field.state = I2C_SPY_SM_STATE_DATA
    reg.field.data = data
    return reg
# end def i2c_data


def i2c_frame(timestamp, data, nack=False):
    """
    Utility function for KosmosI2cSpyFrameParserTestCase

    :param timestamp: timestamp , defaults to 0 - OPTIONAL
    :type timestamp: ``int``
    :param data: I2C SPY data
    :type data: ``bytes or list[int]``
    :param nack: I2C SPY NACK status, defaults to False - OPTIONAL
    :type nack: ``bool``

    :return: I2C SPY FRAME header structure
    :rtype: ``i2c_spy_frame_header_t``
    """
    header = i2c_spy_frame_header_t()
    header.field.timestamp = timestamp
    header.field.length = len(data)
    header.field.nack = nack
    return bytes(header.raw) + bytes(data)
# end def i2c_frame


class KosmosI2cSpyFrameTestCase(TestCase):
    """
    Unitary Test for Kosmos I2C SPY class
    """

    def test_i2c_spy_frame_class(self):
        """
        Validate I2cSpyFrame class.
        """
        # Default init
        frame = I2cSpyFrame()
        self.assertEqual(0, frame.time)
        self.assertFalse(frame.nack)
        self.assertEqual('[0.000000] ', str(frame))

        # Init with arguments
        frame = I2cSpyFrame(data=bytes.fromhex('AC1312AB'), time=1.123456789, nack=False)
        self.assertEqual(1.123456789, frame.time)
        self.assertFalse(frame.nack)
        self.assertEqual('[1.123457] ac 13 12 ab', str(frame))  # time is rounded up properly

        # Init with arguments
        frame = I2cSpyFrame(data=bytes.fromhex('1234'), time=9.87654321, nack=True)
        self.assertEqual(9.87654321, frame.time)
        self.assertTrue(frame.nack)
        self.assertEqual('[9.876543] NACK 12 34', str(frame))
    # end def test_i2c_spy_frame_class
# end class KosmosI2cSpyFrameTestCase


class KosmosI2cSpyRawParserTestCase(TestCase):
    """
    Unitary Test for Kosmos I2C SPY class
    """

    i2c_buffer_init_0 = [i2c_ctrl(state=I2C_SPY_SM_STATE_INIT, timestamp=0)]

    i2c_buffer_ack = [i2c_ctrl(state=I2C_SPY_SM_STATE_START, timestamp=1),
                      i2c_data(data=0xAB),
                      i2c_ctrl(state=I2C_SPY_SM_STATE_ACK, timestamp=3),
                      i2c_data(data=0xCD),
                      i2c_ctrl(state=I2C_SPY_SM_STATE_ACK, timestamp=5),
                      i2c_data(data=0xEF),
                      i2c_ctrl(state=I2C_SPY_SM_STATE_ACK, timestamp=7),
                      i2c_ctrl(state=I2C_SPY_SM_STATE_STOP, timestamp=8)]

    i2c_buffer_init_1 = [i2c_ctrl(state=I2C_SPY_SM_STATE_INIT, timestamp=20)]

    i2c_buffer_nack = [i2c_ctrl(state=I2C_SPY_SM_STATE_START, timestamp=21),
                       i2c_data(data=0x12),
                       i2c_ctrl(state=I2C_SPY_SM_STATE_ACK, timestamp=23),
                       i2c_data(data=0x34),
                       i2c_ctrl(state=I2C_SPY_SM_STATE_NACK, timestamp=25),
                       i2c_ctrl(state=I2C_SPY_SM_STATE_STOP, timestamp=26)]

    def setUp(self):
        """
        Setup Test Case
        """
        super().setUp()
        self.parser = I2cSpyRawParser(fpga_clock_freq_hz=FREQ)
    # end def setUp

    def test_i2c_spy_raw_parser_ack(self):
        """
        Validate I2cSpyRawParser class.
        """
        count = self.parser.parse(self.i2c_buffer_ack)
        self.assertEqual(1, count)

        self.assertEqual(1, len(self.parser.frame_runs))
        frame_run = self.parser.frame_runs[0]
        self.assertEqual(1, len(frame_run))
        frame = frame_run[0]
        self.assertEqual(3, len(frame))

        debug_print(repr(self.parser))
        self.assertEqual('I2C PARSER: 1 runs, 1 frames, running for 0.000000 s.', str(self.parser))
        self.assertEqual('[1.000000] ab cd ef', str(frame))
    # end def test_i2c_spy_raw_parser_ack

    def test_i2c_spy_raw_parser_nack(self):
        """
        Validate I2cSpyRawParser class.
        """
        count = self.parser.parse(self.i2c_buffer_nack)
        self.assertEqual(1, count)

        self.assertEqual(1, len(self.parser.frame_runs))
        frame_run = self.parser.frame_runs[0]
        self.assertEqual(1, len(frame_run))
        frame = frame_run[0]
        self.assertEqual(2, len(frame))

        debug_print(repr(self.parser))
        self.assertEqual('I2C PARSER: 1 runs, 1 frames, running for 0.000000 s.', str(self.parser))
        self.assertEqual('[21.000000] NACK 12 34', str(frame))
    # end def test_i2c_spy_raw_parser_nack

    def test_i2c_spy_raw_parser_init(self):
        """
        Validate I2cSpyRawParser class.
        """
        count = self.parser.parse(self.i2c_buffer_init_0 + self.i2c_buffer_ack +
                                  self.i2c_buffer_init_1 + self.i2c_buffer_nack)
        self.assertEqual(2, count)

        self.assertEqual(2, len(self.parser.frame_runs))

        debug_print(repr(self.parser))
        self.assertEqual('I2C PARSER: 2 runs, 2 frames, running for 21.000000 s.\n'
                         'RUN: 1 frames, from 0.000000 s to 1.000000 s, total 1.000000 s.\n'
                         '[000][0000][1.000000] ab cd ef\n'
                         'RUN: 1 frames, from 20.000000 s to 21.000000 s, total 1.000000 s.\n'
                         '[001][0000][21.000000] NACK 12 34',
                         repr(self.parser))
    # end def test_i2c_spy_raw_parser_init

    def test_i2c_spy_raw_parser_init_empty(self):
        """
        Validate I2cSpyRawParser class.
        """
        count = self.parser.parse(self.i2c_buffer_init_0 + self.i2c_buffer_init_1)
        self.assertEqual(0, count)

        self.assertEqual(2, len(self.parser.frame_runs))

        debug_print(repr(self.parser))
        self.assertEqual('I2C PARSER: 2 runs, 0 frames, running for 20.000000 s.\n'
                         'RUN: 0 frames, from 0.000000 s to 0.000000 s, total 0.000000 s.\n'
                         'RUN: 0 frames, from 20.000000 s to 20.000000 s, total 0.000000 s.',
                         repr(self.parser))
    # end def test_i2c_spy_raw_parser_init_empty

    def test_i2c_spy_raw_parser_multiple_calls(self):
        """
        Validate I2cSpyRawParser class.
        """
        i2c_buffer = self.i2c_buffer_ack + self.i2c_buffer_nack

        # Call parser repeatedly with partial amount of data
        for i, data in enumerate(i2c_buffer):
            count = self.parser.parse([i2c_buffer[i]])
            self.assertEqual(i in [len(self.i2c_buffer_ack) - 1, len(i2c_buffer) - 1],
                             count, msg=f'Fail at i={i}, count={count}, data={data}.')
        # end for

        self.assertEqual(1, len(self.parser.frame_runs))
        frame_run = self.parser.frame_runs[0]
        self.assertEqual(2, len(frame_run))

        debug_print(repr(self.parser))
        self.assertEqual('I2C PARSER: 1 runs, 2 frames, running for 20.000000 s.\n'
                         'RUN: 2 frames, from 1.000000 s to 21.000000 s, total 20.000000 s.\n'
                         '[000][0000][1.000000] ab cd ef\n'
                         '[000][0001][21.000000] NACK 12 34',
                         repr(self.parser))
    # end def test_i2c_spy_raw_parser_multiple_calls

    def test_i2c_spy_raw_parser_invalid_timestamp(self):
        """
        Validate I2cSpyRawParser class.
        """
        i2c_buffer = [i2c_ctrl(state=I2C_SPY_SM_STATE_START, timestamp=10),
                      i2c_data(data=0x12),
                      i2c_ctrl(state=I2C_SPY_SM_STATE_ACK, timestamp=9),  # this timestamp should be flagged as invalid
                      i2c_ctrl(state=I2C_SPY_SM_STATE_STOP, timestamp=13)]

        with self.assertRaisesRegex(AssertionError, r'\[2\] Current timestamp 0x00000009 \(9.000000 s\) is smaller than'
                                                    r' previous timestamp 0x0000000a \(10.000000 s\).'):
            self.parser.parse(i2c_buffer)
        # end with
    # end def test_i2c_spy_raw_parser_invalid_timestamp

    def test_i2c_spy_raw_parser_empty_frame(self):
        """
        Validate I2cSpyRawParser class.
        """
        i2c_buffer = [i2c_ctrl(state=I2C_SPY_SM_STATE_START, timestamp=1),
                      i2c_ctrl(state=I2C_SPY_SM_STATE_STOP, timestamp=2)]

        with self.assertRaisesRegex(AssertionError, r'Empty I2C frame is invalid.'):
            self.parser.parse(i2c_buffer)
        # end with
    # end def test_i2c_spy_raw_parser_empty_frame

    def test_i2c_spy_raw_parser_unknown_state(self):
        """
        Validate I2cSpyRawParser class.
        """
        i2c_buffer = [i2c_ctrl(state=7, timestamp=0)]

        with self.assertRaisesRegex(AssertionError, r'Unknown I2C register state 7.'):
            self.parser.parse(i2c_buffer)
        # end with
    # end def test_i2c_spy_raw_parser_unknown_state

    def test_i2c_spy_raw_parser_invalid_state_idle(self):
        """
        Validate I2cSpyRawParser class.
        """
        i2c_buffer = [i2c_ctrl(state=I2C_SPY_SM_STATE_IDLE, timestamp=0)]

        with self.assertRaisesRegex(AssertionError, r'Invalid I2C register state I2C_SPY_SM_STATE_IDLE.'):
            self.parser.parse(i2c_buffer)
        # end with
    # end def test_i2c_spy_raw_parser_invalid_state_idle

    def test_i2c_spy_raw_parser_unexpected_state_0(self):
        """
        Validate I2cSpyRawParser class.
        """
        i2c_buffer = [i2c_ctrl(state=I2C_SPY_SM_STATE_START, timestamp=10),
                      i2c_data(data=0x12),
                      i2c_data(data=0x34),  # this state should be either ACK or NACK
                      i2c_ctrl(state=I2C_SPY_SM_STATE_STOP, timestamp=13)]

        with self.assertRaisesRegex(ValueError, r'Unexpected I2C register state \<I2C_SPY_SM_STATE_DATA: 3\>, '
                                                r'for parser state \<STATE.WAIT_FOR_ACK_NACK: 3\>.'):
            self.parser.parse(i2c_buffer)
        # end with
    # end def test_i2c_spy_raw_parser_unexpected_state_0

    def test_i2c_spy_raw_parser_unexpected_state_1(self):
        """
        Validate I2cSpyRawParser class.
        """
        i2c_buffer = [i2c_ctrl(state=I2C_SPY_SM_STATE_START, timestamp=10),
                      i2c_ctrl(state=I2C_SPY_SM_STATE_ACK, timestamp=11),  # ACK state should only come after DATA state
                      i2c_ctrl(state=I2C_SPY_SM_STATE_STOP, timestamp=12)]

        with self.assertRaisesRegex(ValueError, r'Unexpected I2C register state \<I2C_SPY_SM_STATE_ACK: 4\>, '
                                                r'for parser state \<STATE.WAIT_FOR_DATA_STOP_RESTART: 2\>.'):
            self.parser.parse(i2c_buffer)
        # end with
    # end def test_i2c_spy_raw_parser_unexpected_state_1

    def test_i2c_spy_raw_parser_garbage_at_start(self):
        """
        Validate I2cSpyRawParser class.
        """
        i2c_buffer = [i2c_ctrl(state=I2C_SPY_SM_STATE_ACK, timestamp=1),    # should ignore garbage before INIT/START
                      i2c_ctrl(state=I2C_SPY_SM_STATE_NACK, timestamp=2),   # should ignore garbage before INIT/START
                      i2c_data(data=0xEE),                                  # should ignore garbage before INIT/START
                      i2c_ctrl(state=I2C_SPY_SM_STATE_STOP, timestamp=4)    # should ignore garbage before INIT/START
                      ] + self.i2c_buffer_init_1 + self.i2c_buffer_nack

        self.parser.parse(i2c_buffer)

        frame = self.parser.frame_runs[0][0]
        self.assertEqual('[21.000000] NACK 12 34', str(frame))
    # end def test_i2c_spy_raw_parser_garbage_at_start
# end class KosmosI2cSpyRawParserTestCase


class KosmosI2cSpyFrameParserTestCase(TestCase):
    """
    Unitary Test for Kosmos I2C SPY class
    """

    def setUp(self):
        """
        Setup Test Case
        """
        super().setUp()
        self.parser = I2cSpyFrameParser(fpga_clock_freq_hz=FREQ)
    # end def setUp

    def test_i2c_spy_frame_parser_ack_nack(self):
        """
        Validate I2cSpyFrame class.
        """
        i2c_buffer = (i2c_frame(timestamp=1, data=bytes.fromhex('AC1312AB'), nack=False)
                      + i2c_frame(timestamp=10, data=bytes.fromhex('CAFE'), nack=True))
        count = self.parser.parse(i2c_buffer)
        self.assertEqual(2, count)

        debug_print(repr(self.parser))
        self.assertEqual('I2C PARSER: 1 runs, 2 frames, running for 9.000000 s.\n'
                         'RUN: 2 frames, from 1.000000 s to 10.000000 s, total 9.000000 s.\n'
                         '[000][0000][1.000000] ac 13 12 ab\n'
                         '[000][0001][10.000000] NACK ca fe',
                         repr(self.parser))
    # end def test_i2c_spy_frame_parser_ack_nack

    def test_i2c_spy_frame_parser_init(self):
        """
        Validate I2cSpyFrame class.
        """
        i2c_buffer = (i2c_frame(timestamp=1, data=bytes.fromhex('AC1312AB'), nack=False)
                      + i2c_frame(timestamp=5, data=[], nack=False)
                      + i2c_frame(timestamp=10, data=bytes.fromhex('CAFE'), nack=True)
                      + i2c_frame(timestamp=20, data=[], nack=False))
        count = self.parser.parse(i2c_buffer)
        self.assertEqual(2, count)

        debug_print(repr(self.parser))
        self.assertEqual('I2C PARSER: 3 runs, 2 frames, running for 19.000000 s.\n'
                         'RUN: 1 frames, from 1.000000 s to 1.000000 s, total 0.000000 s.\n'
                         '[000][0000][1.000000] ac 13 12 ab\n'
                         'RUN: 1 frames, from 5.000000 s to 10.000000 s, total 5.000000 s.\n'
                         '[001][0000][10.000000] NACK ca fe\n'
                         'RUN: 0 frames, from 20.000000 s to 20.000000 s, total 0.000000 s.',
                         repr(self.parser))
    # end def test_i2c_spy_frame_parser_init

    def test_i2c_spy_frame_parser_multiple_calls(self):
        """
        Validate I2cSpyRawParser class.
        """
        frame_ack = i2c_frame(timestamp=1, data=bytes.fromhex('AC1312AB'), nack=False)
        frame_init = i2c_frame(timestamp=5, data=[], nack=False)
        frame_nack = i2c_frame(timestamp=10, data=bytes.fromhex('CAFE'), nack=True)
        i2c_buffer = frame_ack + frame_init + frame_nack

        # Call parser repeatedly with partial amount of data
        for i, data in enumerate(i2c_buffer):
            count = self.parser.parse([i2c_buffer[i]])
            self.assertEqual(i in [len(frame_ack) - 1,
                                   len(frame_ack) + len(frame_init) + len(frame_nack) - 1],
                             count,  msg=f'Fail at i={i}, count={count}, data={data:#04x}.')
        # end for

        debug_print(repr(self.parser))
        self.assertEqual('I2C PARSER: 2 runs, 2 frames, running for 9.000000 s.\n'
                         'RUN: 1 frames, from 1.000000 s to 1.000000 s, total 0.000000 s.\n'
                         '[000][0000][1.000000] ac 13 12 ab\n'
                         'RUN: 1 frames, from 5.000000 s to 10.000000 s, total 5.000000 s.\n'
                         '[001][0000][10.000000] NACK ca fe',
                         repr(self.parser))
    # end def test_i2c_spy_frame_parser_multiple_calls
# end class KosmosI2cSpyFrameParserTestCase


def debug_print(*args, **kwargs):
    """
    Print text to console if `VERBOSE` mode is enabled.

    :param args: arguments to be passed to `print()` function
    :type args: ``tuple[Any]``
    :param kwargs: arguments to be passed to `print()` function
    :type kwargs: ``dict[str, Any]``
    """
    if VERBOSE:
        print(*args, **kwargs)
    # end if
# end def debug_print

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
