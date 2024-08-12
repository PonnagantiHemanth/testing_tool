#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: pyraspi.bus.test.fpgabus_test
:brief: Test of ``FpgaBus`` class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/03/19
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from datetime import datetime
from string import hexdigits
from typing import Iterable
from unittest import TestCase
from unittest import skipIf

from pyraspi.bus.fpgabus import FpgaBus
from pyraspi.bus.fpgabus import Link
from pyraspi.raspi import UNSUPPORTED_SETUP_ERR_MSG
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.protocol.generated.messages import MSG_CMD_REPLY_FLAG
from pyraspi.services.kosmos.protocol.generated.messages import MSG_FRAME_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA_CMD_HW_REV_READ
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_BRANCH_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_BRANCH_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_HASH_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_HASH_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_VERSION
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CMD_WRITE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PES_CMD_WRITE_7
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL_CMD_GIT_BRANCH_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL_CMD_GIT_BRANCH_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL_CMD_GIT_DESCRIBE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL_CMD_GIT_DESCRIBE_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL_CMD_GIT_HASH_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL_CMD_GIT_HASH_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL_CMD_INVALID
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL_CMD_VERSION
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PWR_BAT
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PWR_BAT_CMD_WRITE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PWR_USB
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PWR_USB_CMD_WRITE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SEQUENCER
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SEQUENCER_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_STATUS_CMD_REPLY
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST_CMD_LOOPBACK
from pyraspi.services.kosmos.protocol.generated.messages import MSG_PAYLOAD_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_REPLY_RETURN_CODE_NOT_IMPLEMENTED
from pyraspi.services.kosmos.protocol.generated.messages import MSG_REPLY_RETURN_CODE_SUCCESS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_REPLY_RETURN_CODE_UNKNOWN_MSG_CMD
from pyraspi.services.kosmos.protocol.generated.messages import MSG_REPLY_RETURN_CODE_UNKNOWN_MSG_ID
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_WAIT
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_IDLE
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RESET_DONE
from pyraspi.services.kosmos.protocol.generated.messages import fpga_hw_rev_t
from pyraspi.services.kosmos.protocol.generated.messages import msg_reply_return_code_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_wait_t
from pyraspi.services.kosmos.protocol.generated.messages import sequencer_status_t
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@skipIf(not Daemon.is_host_kosmos(), UNSUPPORTED_SETUP_ERR_MSG)
class FPGATestCase(TestCase):
    """
    Unit Test for ``FpgaBus`` class
    """
    # ``FpgaBus`` class object to be tested
    _fpga_bus: FpgaBus = None

    @classmethod
    def setUpClass(cls):
        """
        Open FpgaBus interface
        """
        cls._fpga_bus = FpgaBus()
    # end def setUpClass

    def _send_control_message(self, msg_id, msg_cmd):
        """
        Helper function: Send a control message built using only Message ID and CMD fields.

        :param msg_id: The message ID field value. Refer to ``msg_id_e__enumvalues``.
        :type msg_id: ``msg_id_e or int``
        :param msg_cmd: The message CMD field value. Refer to ``msg_cmd_e__enumvalues``.
        :type msg_cmd: ``msg_cmd_e or int``

        :return: Reply message's payload
        :rtype: ``msg_payload_t``
        """
        tx_frame = MessageFrame()
        tx_frame.frame.id = msg_id
        tx_frame.frame.cmd = msg_cmd
        rx, tx = self._send_message_frames([tx_frame], Link.CONTROL)[0]
        return rx.get_payload()
    # end def _send_control_message

    def _send_message_frames(self, tx_frames, link):
        """
        Helper function: sends, receives and validates messages.

        :param tx_frames: ``MessageFrame`` to be sent
        :type tx_frames: ``MessageFrame or Iterable[MessageFrame]``
        :param link: SPI bus to be used for the transaction
        :type link: ``Link``

        :return: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :rtype: ``list[tuple[MessageFrame, MessageFrame]]``

        :raise ``AssertionError``: if a RX ``MessageFrame`` is invalid
        """

        # Send datagram and get reply
        txrx_frames = self._fpga_bus.send_datagram(tx_frames, link)
        self.assertIsInstance(txrx_frames, list,
                              msg=f'Reply should be a list of tuple, got {type(txrx_frames)} instead.')

        # Check result
        for (tx_frame, rx_frame) in txrx_frames:
            # Get string representation
            str_tx = 'TX: ' + tx_frame.__str__(padding='    ', complete=False)
            str_rx = 'RX: ' + rx_frame.__str__(padding='    ', complete=False)

            # Test Frame ID
            self.assertIn(rx_frame.frame.id, [tx_frame.frame.id, MSG_ID_STATUS],
                          msg='RX frame ID should match either TX frame ID or `MSG_ID_STATUS`: '
                              f'got tx:{tx_frame.frame.id:#04x} and rx:{rx_frame.frame.id:#04x}\n'
                              + str_tx + str_rx)

            # Test Frame CMD
            self.assertFalse(tx_frame.frame.cmd & MSG_CMD_REPLY_FLAG,
                             msg='The TX frame should have the `MSG_CMD_REPLY_FLAG` bit cleared in CMD field.\n'
                                 + str_tx + str_rx)
            self.assertTrue(rx_frame.frame.cmd & MSG_CMD_REPLY_FLAG,
                            msg='The RX frame should have the `MSG_CMD_REPLY_FLAG` bit set in CMD field.\n'
                                + str_tx + str_rx)

            # Test CRC
            self.assertTrue(tx_frame.is_crc_valid(),
                            msg='TX frame CRC is not valid: '
                                f'got {tx_frame.frame.crc:#04x}, '
                                f'expected {tx_frame.compute_crc() :#04x}.\n'
                                + str_tx + str_rx)
            self.assertTrue(rx_frame.is_crc_valid(),
                            msg='RX frame CRC is not valid: '
                                f'got {rx_frame.frame.crc:#04x}, '
                                f'expected {rx_frame.compute_crc() :#04x}.\n'
                                + str_tx + str_rx)
        # end for

        return txrx_frames
    # end def _send_message_frames

    def _assert_return_code(self, rx_frame, return_code):
        """
        Validate that given return code was set in reply sent by remote device.

        :param rx_frame: MessageFrame to be checked for return code
        :type rx_frame: ``MessageFrame``
        :param return_code: expected return code
        :type return_code: ``msg_reply_return_code_e``

        :raise ``AssertionError``: if a RX ``MessageFrame`` is invalid
                                    or if return code is not as expected
        """
        self.assertEqual(rx_frame.frame.id, MSG_ID_STATUS)
        self.assertEqual(rx_frame.frame.cmd, MSG_ID_STATUS_CMD_REPLY | MSG_CMD_REPLY_FLAG)

        rcode = rx_frame.frame.payload.msg_reply.return_code

        # Find string representations of the enum
        rcode_str = return_code_str = ''
        if rcode in msg_reply_return_code_e__enumvalues:
            rcode_str = msg_reply_return_code_e__enumvalues[rcode]
        # end if
        if return_code in msg_reply_return_code_e__enumvalues:
            return_code_str = msg_reply_return_code_e__enumvalues[return_code]
        # end if

        self.assertEqual(rcode, return_code,
                         msg='Wrong error code:\n'
                             f'got {rcode:#04x} [{rcode_str}]\n'
                             f'expected {return_code:#04x} [{return_code_str}]\n')
    # end def _assert_return_code

    def _reset(self):
        """
        Reset Sequencer module and its associated modules (hardware FIFOs and software buffers reset).
        """
        status = self._send_control_message(msg_id=MSG_ID_SEQUENCER, msg_cmd=MSG_ID_FPGA_CMD_RESET)
        self._assert_reset(status)
    # end def _reset

    def _assert_reset(self, status=None):
        """
        Assert reset of Sequencer module and its associated modules.

        :param status: Sequencer Status message to use, defaults to None (get new Sequencer status) - OPTIONAL
        :type status: ``sequencer_status_t``

        :raise ``AssertionError``: Status error
        """
        if status is None:
            status = self._send_control_message(msg_id=MSG_ID_SEQUENCER, msg_cmd=MSG_ID_SEQUENCER_CMD_STATUS)
        # end if

        self.assertIsInstance(status, sequencer_status_t, msg=status)
        self.assertIn(status.state, [SEQUENCER_STATE_IDLE, SEQUENCER_STATE_RESET_DONE], msg=status)
        self.assertEqual(0, status.pes.fifo_count, msg=status)
        self.assertEqual(0, status.pes.buffer_count, msg=status)
        self.assertEqual(0, status.pes_cpu.buffer_count, msg=status)
        self.assertEqual(0, status.kbd_matrix.fifo_count, msg=status)
        self.assertEqual(0, status.kbd_matrix.buffer_count, msg=status)
        self.assertEqual(0, status.bas.fifo_count, msg=status)
        self.assertEqual(0, status.bas.buffer_count, msg=status)
    # end def _assert_reset

    def test_reset(self):
        """
        Validate Reset of Sequencer module and its associated modules.
        """
        self._reset()
    # end def test_reset

    def test_multiple_instances(self):
        """
        Validate multiple instances of FpgaBus are allowed
        """
        FpgaBus()
    # end def test_multiple_instances

    def test_one_message_frame(self):
        """
        Test Case: Send 10 datagrams composed of one ``MessageFrame``.
        (fixed minimal datagram length)
        """
        # Prepare TX frame with arbitrary payload content
        tx_frame = MessageFrame()
        tx_frame.frame.id = MSG_ID_TEST
        tx_frame.frame.cmd = MSG_ID_TEST_CMD_LOOPBACK
        marker = ord('A')
        payload = bytes([marker] * MSG_PAYLOAD_SIZE)
        tx_frame.set_payload(payload)

        # Repeat test a few times
        for repeat in range(0, 10):
            with self.subTest(repeat=repeat):
                # Send frame and validate reply
                txrx_frames = self._send_message_frames(tx_frame, Link.CONTROL)

                (tx_frame, rx_frame) = txrx_frames[0]
                self.assertListEqual(list(tx_frame.frame.payload.raw.byte), list(payload))
                self.assertListEqual(list(rx_frame.frame.payload.raw.byte), list(payload))
            # end with
        # end for

        # Reset FpgaBus status before exiting the test
        self._reset()
    # end def test_one_message_frame

    def test_multiple_message_frames(self):
        """
        Test Case: Send 10 datagrams composed of zero to nine ``MessageFrame``.
        (variable datagram length)
        """
        for frame_count in range(0, 10):
            with self.subTest(frame_count=frame_count):
                # Prepare TX frames with arbitrary content
                tx_frames = []
                for i in range(frame_count):
                    marker = ord('A') + i
                    frame = MessageFrame(buffer=bytes([marker] * MSG_FRAME_SIZE))
                    frame.frame.id = MSG_ID_TEST
                    frame.frame.cmd = MSG_ID_TEST_CMD_LOOPBACK
                    tx_frames.append(frame)
                # end for

                # Send frames and validate replies
                self._send_message_frames(tx_frames, Link.CONTROL)
            # end with
        # end for

        # Reset FpgaBus status before exiting the test
        self._reset()
    # end def test_multiple_message_frames

    def test_message_id_protocol_cmd_invalid(self):
        """
        Test Case: MessageFrame ID:MSG_ID_PROTOCOL, CMD:MSG_ID_PROTOCOL_CMD_INVALID
        """
        # Send request, expect no reply
        with self.assertRaises(TimeoutError):
            self._send_control_message(msg_id=MSG_ID_PROTOCOL, msg_cmd=MSG_ID_PROTOCOL_CMD_INVALID)
        # end with

        # Check FpgaBus status before exiting the test
        self._assert_reset()
    # end def test_message_id_protocol_cmd_invalid

    def test_message_id_unknown(self):
        """
        Test Case: MessageFrame ID: unknown (0xFF), CMD: don't care (0x00)
        """
        # Create an invalid request
        tx_frame = MessageFrame()
        tx_frame.frame.id = 0xFF
        tx_frame.frame.cmd = 0x00

        # Send request, expect return code
        (tx_frame, rx_frame) = self._send_message_frames(tx_frame, Link.CONTROL)[0]
        self._assert_return_code(rx_frame, MSG_REPLY_RETURN_CODE_UNKNOWN_MSG_ID)

        # Check FpgaBus status before exiting the test
        self._assert_reset()
    # end def test_message_id_unknown

    def test_message_id_test_cmd_unknown(self):
        """
        Test Case: MessageFrame ID:MSG_ID_TEST, CMD: unknown (0x7F)
        """
        # Create an invalid request
        tx_frame = MessageFrame()
        tx_frame.frame.id = MSG_ID_TEST
        tx_frame.frame.cmd = 0x7F

        # Send request, expect return code
        (tx_frame, rx_frame) = self._send_message_frames(tx_frame, Link.CONTROL)[0]
        self._assert_return_code(rx_frame, MSG_REPLY_RETURN_CODE_UNKNOWN_MSG_CMD)

        # Check FpgaBus status before exiting the test
        self._assert_reset()
    # end def test_message_id_test_cmd_unknown

    def test_message_id_fpga_cmd_hw_rev(self):
        """
        Test Case: MessageFrame ID:MSG_ID_FPGA, CMD:MSG_ID_FPGA_CMD_HW_REV_READ

        """
        # Create request
        tx_frame = MessageFrame()
        tx_frame.frame.id = MSG_ID_FPGA
        tx_frame.frame.cmd = MSG_ID_FPGA_CMD_HW_REV_READ

        # Send request and validate reply
        (tx_frame, rx_frame) = self._send_message_frames(tx_frame, Link.CONTROL)[0]

        # Check the value returned by the FpgaBus
        hw_rev = rx_frame.frame.payload.fpga_hw_rev
        self.assertTrue(hw_rev.version.major == 2, msg=hw_rev.version)
        self.assertTrue(0 <= hw_rev.version.minor <= 0xFF, msg=hw_rev.version)
        self.assertTrue(0 <= hw_rev.version.patch <= 0xFF, msg=hw_rev.version)

        # Check FpgaBus status before exiting the test
        self._assert_reset()
    # end def test_message_id_fpga_cmd_hw_rev

    def test_cmd_git(self):
        """
        Test Case: Validates that MSG_ID_KOSMOS and MSG_ID_PROTOCOL share the same message commands
        """
        self.assertNotEqual(MSG_ID_PROTOCOL, MSG_ID_KOSMOS)
        self.assertEqual(MSG_ID_PROTOCOL_CMD_VERSION, MSG_ID_KOSMOS_CMD_VERSION)
        self.assertEqual(MSG_ID_PROTOCOL_CMD_GIT_DESCRIBE_1, MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_1)
        self.assertEqual(MSG_ID_PROTOCOL_CMD_GIT_DESCRIBE_2, MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_2)
        self.assertEqual(MSG_ID_PROTOCOL_CMD_GIT_BRANCH_1, MSG_ID_KOSMOS_CMD_GIT_BRANCH_1)
        self.assertEqual(MSG_ID_PROTOCOL_CMD_GIT_BRANCH_2, MSG_ID_KOSMOS_CMD_GIT_BRANCH_2)
        self.assertEqual(MSG_ID_PROTOCOL_CMD_GIT_HASH_1, MSG_ID_KOSMOS_CMD_GIT_HASH_1)
        self.assertEqual(MSG_ID_PROTOCOL_CMD_GIT_HASH_2, MSG_ID_KOSMOS_CMD_GIT_HASH_2)
    # end def test_cmd_git

    def test_message_id_protocol_cmd_git_version(self):
        """
        Test Case: MessageFrame ID:MSG_ID_PROTOCOL, CMD:MSG_ID_PROTOCOL_CMD_VERSION
        """
        self._test_cmd_git_version(frame_id=MSG_ID_PROTOCOL)
    # end def test_message_id_protocol_cmd_git_version

    def test_message_id_protocol_cmd_git_info(self):
        """
        Test Case: MessageFrame ID:MSG_ID_PROTOCOL, CMD:MSG_ID_PROTOCOL_CMD_GIT_*
        """
        self._test_cmd_git_info(frame_id=MSG_ID_PROTOCOL)
    # end def test_message_id_protocol_cmd_git_info

    def test_message_id_kosmos_cmd_git_version(self):
        """
        Test Case: MessageFrame ID:MSG_ID_KOSMOS, CMD:MSG_ID_KOSMOS_CMD_VERSION
        """
        self._test_cmd_git_version(frame_id=MSG_ID_KOSMOS)
    # end def test_message_id_kosmos_cmd_git_version

    def test_message_id_kosmos_cmd_git_info(self):
        """
        Test Case: MessageFrame ID:MSG_ID_KOSMOS, CMD:MSG_ID_KOSMOS_CMD_GIT_*
        """
        self._test_cmd_git_info(frame_id=MSG_ID_KOSMOS)
    # end def test_message_id_kosmos_cmd_git_info

    def _test_cmd_git_version(self, frame_id):
        """
        Test Case common method for MessageFrame's git_version payload

        Steps:
          - Send a message asking to read Git version
          - Validate message reply
          - Validate message content

        :param frame_id: Select which Git module to read from
        :type frame_id: ``MSG_ID_KOSMOS or MSG_ID_PROTOCOL``

        :raise ``AssertionError``: for any failed step
        """
        # Prepare message request
        tx_frame = MessageFrame()
        tx_frame.frame.id = frame_id
        tx_frame.frame.cmd = MSG_ID_KOSMOS_CMD_VERSION

        # Send message request and get reply
        (tx_frame, rx_frame) = self._send_message_frames(tx_frame, Link.CONTROL)[0]

        # Parse message reply
        self.assertEqual(rx_frame.frame.id, frame_id)
        self.assertEqual(rx_frame.frame.cmd, MSG_ID_KOSMOS_CMD_VERSION | MSG_CMD_REPLY_FLAG)
        git_hash = ''.join([chr(c) for c in rx_frame.frame.payload.git_version.hash])
        git_timestamp = rx_frame.frame.payload.git_version.timestamp
        git_date = datetime.utcfromtimestamp(git_timestamp)
        git_dirty = rx_frame.frame.payload.git_version.is_dirty
        mode_debug = rx_frame.frame.payload.git_version.is_debug

        # Validate
        self.assertTrue(all(c in hexdigits for c in git_hash),
                        msg="Git hash contains some non-hexadecimal characters:\n" +
                            "\n".join([f"'{c}' {hex(ord(c))}" for c in git_hash]))
        self.assertLess(git_date, datetime.utcnow(), msg="Git date is in the future.")
        self.assertGreater(git_date, datetime(year=2021, month=1, day=1), msg="Git date is too old.")
        self.assertIn(git_dirty, [0, 1], msg="Git Dirty should be a boolean flag")
        self.assertIn(mode_debug, [0, 1], msg="Debug mode should be a boolean flag")
    # end def _test_cmd_git_version

    def _test_cmd_git_info(self, frame_id):
        """
        Test Case common method for MessageFrame's git_info payload

        Steps:
          - Send messages asking to read all Git info fields
          - Validate message replies
          - Validate message content

        :param frame_id: Select which Git module to read from
        :type frame_id: ``MSG_ID_KOSMOS or MSG_ID_PROTOCOL``

        :raise ``AssertionError``: for any failed step
        """
        # Prepare message requests
        commands = {MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_1: 'DESCRIBE_1',
                    MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_2: 'DESCRIBE_2',
                    MSG_ID_KOSMOS_CMD_GIT_BRANCH_1: 'BRANCH_1',
                    MSG_ID_KOSMOS_CMD_GIT_BRANCH_2: 'BRANCH_2',
                    MSG_ID_KOSMOS_CMD_GIT_HASH_1: 'HASH_1',
                    MSG_ID_KOSMOS_CMD_GIT_HASH_2: 'HASH_2'}
        tx_frames = []
        for frame_cmd in commands.keys():
            tx_frame = MessageFrame()
            tx_frame.frame.id = frame_id
            tx_frame.frame.cmd = frame_cmd
            tx_frames.append(tx_frame)
        # end for

        # Send message requests and get replies
        rxtx_frames = self._send_message_frames(tx_frames, Link.CONTROL)

        # Parse message replies
        for (tx_frame, rx_frame), command in zip(rxtx_frames, commands):
            with self.subTest(command=commands[command]):
                self.assertEqual(rx_frame.frame.id, frame_id)
                self.assertEqual(rx_frame.frame.cmd, command | MSG_CMD_REPLY_FLAG)

                git_info = ''.join([chr(x) for x in rx_frame.frame.payload.git_info.value if x])

                if command in [MSG_ID_KOSMOS_CMD_GIT_HASH_1, MSG_ID_KOSMOS_CMD_GIT_HASH_2]:
                    self.assertTrue(all(c in hexdigits for c in git_info),
                                    msg="Git hash contains some non-hexadecimal characters:\n" +
                                        "\n".join([f"'{c}' {hex(ord(c))}" for c in git_info]))
                # end if
            # end with
        # end for
    # end def _test_cmd_git_info

    def test_message_id_pes_write_example(self):
        """
        Test Case: MessageFrame ID:MSG_ID_PES, CMD:MSG_ID_PES_CMD_WRITE_7

        Coding example taken from the Google Document "Programmable Event SequencerModule".
        https://docs.google.com/document/d/1FzrnFcy_0Fy4edVqQQXLtfVlnJQbWFOtY-f4cpIdCNM/edit#heading=h.y98hn3ru3bgq
        Section 6.1.A Simple Script Example

        Perform simple operations like:
            1. Send the Global Time Mark (action channel #0)
            2. Switch On the Power button (action channel #12)
            3. Wait for 16.000 milliseconds
            4. Make Key 123 (action channel #1)
            5. Make Key 567 (action channel #1)
            6. Wait for 20.0 milliseconds
            7. Break Key 123 (action channel #1)
            8. Break Key 567 (action channel #1)
            9. Wait for KBD action finished
        """
        raw_instructions = [
            0x00000001,  # Execute 0x0001. Send the global time stamp from channel #1
            0x00001000,  # Execute 0x1000. Switch on the power button.
            0x2FA00002,  # Delay 4000d*2^2 = (0x2<<(12+16)) | (0xFA0<<16) | 0x0002; Press Key 123
            # Action is already done in the previous step
            0x00000002,  # Execute action vector=0x0002; Press Key 567
            0x39C40002,  # Delay 2500d*2^3 = (0x3<<(12+16)) | (0x9C4<<16) | 0x0002; Release Key 123
            # Action is already done in the previous step
            0x00000002,  # Execute action vector=0x0002; Release Key 567
            0xFFFF0002,  # Wait for KBD_MATRIX action finished
        ]
        self.assertEqual(len(raw_instructions), MSG_ID_PES_CMD_WRITE_7)

        tx_frame = MessageFrame()
        tx_frame.frame.id = MSG_ID_PES
        tx_frame.frame.cmd = MSG_ID_PES_CMD_WRITE_7
        for i, instructions in enumerate(raw_instructions):
            tx_frame.frame.payload.pes[i].raw = instructions
        # end for

        (tx_frame, rx_frame) = self._send_message_frames(tx_frame, Link.CONTROL)[0]
        self._assert_return_code(rx_frame, MSG_REPLY_RETURN_CODE_SUCCESS)

        # Reset FpgaBus status before exiting the test
        self._reset()
    # end def test_message_id_pes_write_example

    def test_message_id_pes_write(self):
        """
        Test Case: MessageFrame ID:MSG_ID_PES, CMD:MSG_ID_PES_CMD_WRITE_1 to _7
        """
        for cmd in range(MSG_ID_PES_CMD_WRITE_1, MSG_ID_PES_CMD_WRITE_7 + 1):
            with self.subTest(cmd=cmd):
                tx_frame = MessageFrame()
                tx_frame.frame.id = MSG_ID_PES
                tx_frame.frame.cmd = cmd

                for i in range(cmd):
                    wait = pes_instruction_wait_t()
                    wait.opcode = PES_OPCODE_WAIT
                    wait.resume_event = 0x00
                    tx_frame.frame.payload.pes[i].wait = wait
                # end for

                (tx_frame, rx_frame) = self._send_message_frames(tx_frame, Link.CONTROL)[0]
                self._assert_return_code(rx_frame, MSG_REPLY_RETURN_CODE_SUCCESS)
            # end with
        # end for

        # Reset FpgaBus status before exiting the test
        self._reset()
    # end def test_message_id_pes_write

    def test_message_id_pwr_usb_write(self):
        """
        Test Case: MessageFrame ID:MSG_ID_PWR_USB, CMD:MSG_ID_PWR_USB_CMD_WRITE
        """
        tx_frame = MessageFrame()
        tx_frame.frame.id = MSG_ID_PWR_USB
        tx_frame.frame.cmd = MSG_ID_PWR_USB_CMD_WRITE

        # FIXME: Not yet implemented
        (tx_frame, rx_frame) = self._send_message_frames(tx_frame, Link.CONTROL)[0]
        self._assert_return_code(rx_frame, MSG_REPLY_RETURN_CODE_NOT_IMPLEMENTED)

        # Reset FpgaBus status before exiting the test
        self._reset()
    # end def test_message_id_pwr_usb_write

    def test_message_id_pwr_bat_write(self):
        """
        Test Case: MessageFrame ID:MSG_ID_PWR_BAT, CMD:MSG_ID_PWR_BAT_CMD_WRITE
        """
        tx_frame = MessageFrame()
        tx_frame.frame.id = MSG_ID_PWR_BAT
        tx_frame.frame.cmd = MSG_ID_PWR_BAT_CMD_WRITE

        # FIXME: Not yet implemented
        (tx_frame, rx_frame) = self._send_message_frames(tx_frame, Link.CONTROL)[0]
        self._assert_return_code(rx_frame, MSG_REPLY_RETURN_CODE_NOT_IMPLEMENTED)

        # Reset FpgaBus status before exiting the test
        self._reset()
    # end def test_message_id_pwr_bat_write

    def test_send_control_message(self):
        """
        Test Case: function ''FpgaBus.send_control_message()''
        """
        fpga_hw_rev = self._send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ)

        # Check reply message payload type
        self.assertIsInstance(fpga_hw_rev, fpga_hw_rev_t)
    # end def test_send_control_message

# end class FPGATestCase


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
    Entry point of the ``FpgaBus`` Unit Test class.
    """
    from unittest import main
    main()
# end if


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
