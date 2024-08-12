#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.fpgatransport
:brief: FPGA Transport implementation Class
:author: Alexandre Lafaye<alafaye@logitech.com>, Lila Viollette <lviollette@logitech.com>
:date: 2021/04/09
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

from pyraspi.bus.fpgabus import FpgaBus
from pyraspi.bus.fpgabus import Link
from pyraspi.services.kosmos.module.devicetree import DeviceTreeModuleBaseClass
from pyraspi.services.kosmos.module.devicetree import DeviceTreeModuleSettings
from pyraspi.services.kosmos.module.error import KosmosFatalErrorException
from pyraspi.services.kosmos.protocol.generated.messages import MSG_CMD_REPLY_FLAG
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA_CMD_HWCFG
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA_CMD_HW_REV_READ
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_STATUS_CMD_REPLY
from pyraspi.services.kosmos.protocol.generated.messages import MSG_REPLY_RETURN_CODE_BUFFER_OVERRUN
from pyraspi.services.kosmos.protocol.generated.messages import MSG_REPLY_RETURN_CODE_BUFFER_UNDERRUN
from pyraspi.services.kosmos.protocol.generated.messages import MSG_REPLY_RETURN_CODE_SUCCESS
from pyraspi.services.kosmos.protocol.generated.messages import fpga_hw_rev_t
from pyraspi.services.kosmos.protocol.generated.messages import fpga_hwcfg_t
from pyraspi.services.kosmos.protocol.generated.messages import msg_cmd_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import msg_id_e__enumvalues
from pyraspi.services.kosmos.protocol.generated.messages import msg_reply_return_code_e
from pyraspi.services.kosmos.protocol.generated.messages import msg_reply_return_code_e__enumvalues
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class FpgaTransportError(KosmosFatalErrorException, Exception):
    """
    Exception base class for Fpga Transport errors.
    """
    pass
# end class FpgaTransportError


class MessageReplyError(FpgaTransportError):
    """
    Exception emitted when a message reply with an error code set is received.
    """
    pass
# end class MessageReplyError


class OutOfSequenceError(FpgaTransportError):
    """
    Exception emitted when a message reply with different message sequence number is received.
    """
    pass
# end class OutOfSequenceError


class SendPayloadError(FpgaTransportError):
    """
    Exception emitted when an error occurs in `send_payload` method.
    """
    pass
# end class SendPayloadError


class ExtractPayloadError(FpgaTransportError):
    """
    Exception emitted when an error occurs during parsing payload received from remote.
    """
    pass
# end class ExtractPayloadError


class OverrunPayloadError(FpgaTransportError):
    """
    Exception emitted when an error occurs during parsing payload received from remote.
    """
    pass
# end class OverrunPayloadError


class UnderrunPayloadError(FpgaTransportError):
    """
    Exception emitted when an error occurs during parsing payload received from remote.
    """
    pass
# end class UnderrunPayloadError


class FPGATransport(DeviceTreeModuleBaseClass):
    """
    FPGA Transport module.
    """
    _fpga_bus: FpgaBus
    _hwcfg: fpga_hwcfg_t = None
    _fpga_revision: fpga_hw_rev_t = None

    def __init__(self):
        module_settings = DeviceTreeModuleSettings(
            name=r'FPGA Transport',
            instance_id=None,  # Module is a singleton
            optional=False,
        )
        super().__init__(module_settings=module_settings)
        self._fpga_bus = FpgaBus()
    # end def __init__

    def send_control_message_list(self, msg_list):
        """
        Send a list of message frames to FPGA, and return the list of associated reply message's payload.

        :param msg_list: list of MessageFrame
        :type msg_list: ``list[MessageFrame]``

        :return: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :rtype: ``list[tuple[MessageFrame, MessageFrame]]``

        :raise ``ValueError``: multiple source of error:
         - If the Request Message's ID or CMD field values are unknown
         - If the reply message's payload type is unknown, or if the reply itself is invalid
        :raise ``AssertionError``: If number of reply do not match the number of request
        """
        # Validate message fields
        assert isinstance(msg_list, list)
        for msg in msg_list:
            if not MessageFrame.is_valid_id(msg.frame.id):
                raise ValueError(f'Unknown Message ID {msg.frame.id:#04x}.\n{msg}')
            elif not MessageFrame.is_valid_id_cmd(msg.frame.id, msg.frame.cmd):
                raise ValueError(f'Unknown Message ID {msg.frame.id:#04x}, CMD {msg.frame.cmd:#04x}.\n{msg}')
            # end if
        # end for

        # Send request and get reply
        txrx_msg = self._fpga_bus.send_datagram(msg_list, Link.CONTROL)
        assert len(txrx_msg) == len(msg_list)

        self.check_message_replies(txrx_frames=txrx_msg)

        return txrx_msg
    # end def send_control_message_list

    def send_control_message(self, msg_id, msg_cmd):
        """
        Send a message frame to Fpga, and return the associated reply message's payload.

        :param msg_id: The message ID field value. Refer to ``msg_id_e__enumvalues``.
        :type msg_id: ``msg_id_e or int``
        :param msg_cmd: The message CMD field value. Refer to ``msg_cmd_e__enumvalues``.
        :type msg_cmd: ``msg_cmd_e or int``

        :return: Reply message's payload
        :rtype: ``msg_payload_t``

        :raise ``ValueError``: multiple source of error:
         - If the Request Message's ID or CMD field values are unknown
         - ``ValueError``: If the reply message's payload type is unknown, or if the reply itself is invalid
        :raise ``AssertionError``:  Less or more than 1 reply received
        """
        # Validate message fields
        if not MessageFrame.is_valid_id(msg_id):
            raise ValueError(f'Unknown Message ID {msg_id:#04x}.')
        elif not MessageFrame.is_valid_id_cmd(msg_id, msg_cmd):
            raise ValueError(f'Unknown Message ID {msg_id:#04x}, CMD {msg_cmd:#04x}.')
        # end if

        # Create request
        tx_frame = MessageFrame()
        tx_frame.frame.id = msg_id
        tx_frame.frame.cmd = msg_cmd

        # Send request and get reply
        txrx_frames = self.send_control_message_list([tx_frame])

        # Unpack reply datagram
        assert len(txrx_frames) == 1, txrx_frames
        (_, rx_frame) = txrx_frames[0]

        # Return typed payload
        return rx_frame.get_payload()
    # end def send_control_message

    @classmethod
    def check_message_replies(cls, txrx_frames):
        """
        Check MessageFrame transaction replies: check RX messages' ID and CMD fields values.

        :param txrx_frames: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :type txrx_frames: ``list[tuple[MessageFrame, MessageFrame]] or tuple[MessageFrame, MessageFrame]``

        :raise ``SendPayloadError``: if one of the following conditions is met:
                                      - Unexpected Rx MessageFrame ID
                                      - Unexpected Rx MessageFrame CMD (with REPLY flag set)
        :raise ``OutOfSequenceError``: Message sequence ID are received out-of-sequence
        :raise ``UnderrunPayloadError``: Buffer Underrun status bit is set in message reply
        :raise ``OverrunPayloadError``: Buffer Overrun status bit is set in message reply
        :raise ``MessageReplyError``: Unspecified error in Message reply
        """
        if not isinstance(txrx_frames, list):
            txrx_frames = [txrx_frames]
        # end if

        for i, (tx_frame, rx_frame) in enumerate(txrx_frames):
            rx_id, rx_cmd, rx_seq = cls._extract_header(rx_frame)
            tx_id, tx_cmd, tx_seq = cls._extract_header(tx_frame)

            if rx_seq != tx_seq:
                raise OutOfSequenceError('Different message sequence numbers: '
                                         f'rx_seq={rx_seq:#04x} tx_seq={tx_seq:#04x}\n'
                                         + cls.txrx_frames_error_str(txrx_frames, i))
            elif cls._is_status_reply_msg(rx_frame):
                reply_msg_ret_code = rx_frame.frame.payload.msg_reply.return_code
                if not reply_msg_ret_code == MSG_REPLY_RETURN_CODE_SUCCESS:
                    return_code = f'{reply_msg_ret_code}:' \
                                  f'{msg_reply_return_code_e__enumvalues.get(reply_msg_ret_code, "?")}'
                    error_msg = (f'Received reply message with error code {return_code}.\n'
                                 + cls.txrx_frames_error_str(txrx_frames, i))

                    if reply_msg_ret_code == MSG_REPLY_RETURN_CODE_BUFFER_OVERRUN:
                        raise OverrunPayloadError(error_msg)
                    elif reply_msg_ret_code == MSG_REPLY_RETURN_CODE_BUFFER_UNDERRUN:
                        raise UnderrunPayloadError(error_msg)
                    else:
                        raise MessageReplyError(error_msg)
                    # end if
                # end if
            elif rx_id != tx_id:
                raise SendPayloadError(f'Unexpected MessageFrame ID, got {rx_id:#04x}:'
                                       f'{msg_id_e__enumvalues.get(rx_id, "?")}, '
                                       f'expected {tx_id:#04x}:{msg_id_e__enumvalues.get(tx_id, "?")}.\n'
                                       + cls.txrx_frames_error_str(txrx_frames, i))
            elif (tx_cmd | MSG_CMD_REPLY_FLAG) != rx_cmd:
                raise SendPayloadError(f'Unexpected MessageFrame CMD, got {rx_cmd:#04x}, '
                                       f'expected {(tx_cmd | MSG_CMD_REPLY_FLAG):#04x}:'
                                       ' (with REPLY flag set).\n'
                                       + cls.txrx_frames_error_str(txrx_frames, i))
            # end if
        # end for
    # end def check_message_replies

    @classmethod
    def check_status_message_replies(cls, txrx_frames, return_code=MSG_REPLY_RETURN_CODE_SUCCESS):
        """
        Check MessageFrame transaction replies: expect status messages with specific return code.

        :param txrx_frames: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :type txrx_frames: ``list[tuple[MessageFrame, MessageFrame]] or tuple[MessageFrame, MessageFrame]``
        :param return_code: Expected Status Message's return code - OPTIONAL
                            Refer to ``msg_reply_return_code_e__enumvalues``.
        :type return_code: ``msg_reply_return_code_e``

        :raise ``SendPayloadError``: if one of the following conditions is met:
                                      - Rx MessageFrame ID is not ``MSG_ID_STATUS``
                                      - Rx MessageFrame CMD is not ``MSG_ID_STATUS_CMD_REPLY`` (with REPLY flag set)
                                      - Unexpected Status return code
        :raise ``UnderrunPayloadError``: Buffer Underrun status bit is set in message reply
        :raise ``OverrunPayloadError``: Buffer Overrun status bit is set in message reply
        """
        if not isinstance(txrx_frames, list):
            txrx_frames = [txrx_frames]
        # end if

        for i, (tx_frame, rx_frame) in enumerate(txrx_frames):
            rx_id = rx_frame.frame.id
            rx_cmd = rx_frame.frame.cmd
            rx_code = rx_frame.frame.payload.msg_reply.return_code

            if rx_id != MSG_ID_STATUS:
                raise SendPayloadError(f'Unexpected MessageFrame ID, got {rx_id:#04x}:'
                                       f'{msg_id_e__enumvalues.get(rx_id, "?")}, '
                                       f'expected {MSG_ID_STATUS:#04x}:MSG_ID_STATUS.\n'
                                       + cls.txrx_frames_error_str(txrx_frames, i))
            elif rx_cmd != (MSG_ID_STATUS_CMD_REPLY | MSG_CMD_REPLY_FLAG):
                raise SendPayloadError(f'Unexpected MessageFrame CMD, got {rx_cmd:#04x}:'
                                       f'{msg_cmd_e__enumvalues.get(rx_cmd, "?")}, '
                                       f'expected {(MSG_ID_STATUS_CMD_REPLY | MSG_CMD_REPLY_FLAG):#04x}:'
                                       'MSG_ID_STATUS_CMD_REPLY (with REPLY flag set).\n'
                                       + cls.txrx_frames_error_str(txrx_frames, i))
            elif rx_code != return_code:
                error_msg = (f'Unexpected return code, got {rx_code:#04x}:'
                             f'{msg_reply_return_code_e__enumvalues.get(rx_code, "?")}, '
                             f'expected {return_code:#04x}:'
                             f'{msg_reply_return_code_e__enumvalues.get(return_code, "?")}.\n'
                             + cls.txrx_frames_error_str(txrx_frames, i))
                if rx_code == list(msg_reply_return_code_e__enumvalues.values())\
                        .index('MSG_REPLY_RETURN_CODE_BUFFER_OVERRUN'):
                    raise OverrunPayloadError(error_msg)
                elif rx_code == list(msg_reply_return_code_e__enumvalues.values())\
                        .index('MSG_REPLY_RETURN_CODE_BUFFER_UNDERRUN'):
                    raise UnderrunPayloadError(error_msg)
                else:
                    raise SendPayloadError(error_msg)
                # end if
            # end if
        # end for
    # end def check_status_message_replies

    @classmethod
    def txrx_frames_error_str(cls, txrx_frames, frame_id=0):
        """
        Return a human-readable list of TX-RX message frames as text. Oldest frame first.
        Additionally, the frame of index ``frame_id`` will be printed on top.
        This is intended to be called in an exception or to give context to an error messages by exposing the
        problematic frame in a list of frames.

        :param txrx_frames: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :type txrx_frames: ``list[tuple[MessageFrame, MessageFrame]] or tuple[MessageFrame, MessageFrame]``

        :param frame_id: index of the frame that will be printed on top, defaults to 0 - OPTIONAL
        :type frame_id: ``int``

        :return: human-readable list of TX-RX message frames, with a specific frame pinned on top
        :rtype: ``str``

        :raise ``ValueError``: Out-of-bound frame id
        """
        txrx_frames = txrx_frames if isinstance(txrx_frames, list) else [txrx_frames]

        if frame_id >= len(txrx_frames):
            raise ValueError(f'frame_id {frame_id} >= frame count {len(txrx_frames)}')
        # end if

        all_traces = f'\nAll TXRX frames: \n{cls.txrx_frames_str(txrx_frames)}' if len(txrx_frames) > 1 else ''
        return (f'Current TXRX frame: \n'
                + f'{cls.txrx_frames_str(txrx_frames[frame_id], frame_id=frame_id)}'
                + all_traces)
    # end def txrx_frames_error_str

    @classmethod
    def txrx_frames_str(cls, txrx_frames, frame_id=0):
        """
        Return a human-readable indexed list of TX-RX message frames as text. Oldest frame first.

        :param txrx_frames: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :type txrx_frames: ``list[tuple[MessageFrame, MessageFrame]] or tuple[MessageFrame, MessageFrame]``

        :param frame_id: frame index start, corresponding to the first ``txrx_frames``, defaults to 0 - OPTIONAL
        :type frame_id: ``int``

        :return: human-readable list of TX-RX message frames
        :rtype: ``str``
        """
        txrx_frames = txrx_frames if isinstance(txrx_frames, list) else [txrx_frames]
        return '\n'.join(f'{i:02d} TX: {cls.frame_str(tx_frame)}\n'
                         f'{i:02d} RX: {cls.frame_str(rx_frame)}'
                         for i, (tx_frame, rx_frame) in enumerate(txrx_frames, start=frame_id))
    # end def txrx_frames_str

    @classmethod
    def frame_str(cls, frame):
        """
        Return a human-readable message frame representation.

        :param frame: Message frame
        :type frame: ``MessageFrame``

        :return: human-readable message frame representation
        :rtype: ``str``
        """
        msg_id, msg_cmd, msg_seq = cls._extract_header(frame)
        ret_str = ''
        if cls._is_status_reply_msg(frame):
            ret_code = frame.frame.payload.msg_reply.return_code
            ret_str = f'\tRET={ret_code:#04x}:{msg_reply_return_code_e__enumvalues.get(ret_code, "?")}'
        # end if
        return (f'{frame.str_raw_memory()} '
                f'SEQ={msg_seq:#04x} '
                f'ID={msg_id:#04x}:{msg_id_e__enumvalues.get(msg_id, "?")}\t'
                f'CMD={msg_cmd:#04x}'
                + ret_str)
    # end def frame_str

    @staticmethod
    def _extract_header(frame):
        """
        Return the frame ID, CMD and SEQ_ID values of a frame data structure.

        :param frame: Message frame
        :type frame: ``MessageFrame``

        :return: frame ID, CMD and SEQ_ID values
        :rtype: ``tuple[int, int, int]``
        """
        return frame.frame.id, frame.frame.cmd, frame.frame.seq_id
    # end def _extract_header

    @staticmethod
    def _is_status_reply_msg(frame):
        """
        Test if a frame is a status message reply.

        :param frame: Message frame
        :type frame: ``MessageFrame``

        :return: True if frame is a status message reply, False otherwise
        :rtype: ``bool``
        """
        return frame.frame.id == MSG_ID_STATUS and frame.frame.cmd == (MSG_ID_STATUS_CMD_REPLY | MSG_CMD_REPLY_FLAG)
    # end def _is_status_reply_msg

    @property
    def hwcfg(self):
        """
        Return the FPGA hardware config property (NB: value cached at first call).
        Hardware config: list of FPGA modules embedded in the design, as read from FPGA SYSC.HWCFG register.

        :return: FPGA SYSC.HWCFG register value
        :rtype: ``fpga_hwcfg_t``
        """
        if self._hwcfg is None:
            self._hwcfg = self.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HWCFG)
        # end if
        return self._hwcfg
    # end def property getter hwcfg

    @property
    def fpga_revision(self):
        """
        Return the FPGA revision property (NB: value cached at first call).

        :return: FPGA revision
        :rtype: ``fpga_hw_rev_t``
        """
        if self._fpga_revision is None:
            self._fpga_revision = self.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ)
        # end if
        return self._fpga_revision
    # end def property getter fpga_revision
# end class FPGATransport

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
