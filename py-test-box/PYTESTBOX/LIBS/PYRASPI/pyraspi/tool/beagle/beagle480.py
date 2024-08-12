#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.tool.beagle.beagle480
:brief: Beagle 480 USB analyser classes
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os import F_OK
from os import access
from os import makedirs
from os.path import join
from sys import stdout
from uuid import uuid4

from pylibrary.tools.hexlist import HexList
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_KEEP_ALIVE
from pyraspi.tool.beagle.beagle_py import BG_OK
from pyraspi.tool.beagle.beagle_py import BG_PROTOCOL_USB
from pyraspi.tool.beagle.beagle_py import BG_READ_TIMEOUT
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_END_OF_CAPTURE
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_BAD_PID
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_BAD_SIGNALS
from pyraspi.tool.beagle.beagle_py import BG_USB2_AUTO_SPEED_DETECT
from pyraspi.tool.beagle.beagle_py import BG_USB2_CAPTURE_DELAYED_DOWNLOAD
from pyraspi.tool.beagle.beagle_py import BG_USB2_CAPTURE_REALTIME
from pyraspi.tool.beagle.beagle_py import BG_USB2_DATA_MATCH_DATA0
from pyraspi.tool.beagle.beagle_py import BG_USB2_DATA_MATCH_DATA1
from pyraspi.tool.beagle.beagle_py import BG_USB2_DIGITAL_OUT_ENABLE_PIN4
from pyraspi.tool.beagle.beagle_py import BG_USB2_DIGITAL_OUT_MATCH_PIN4
from pyraspi.tool.beagle.beagle_py import BG_USB2_DIGITAL_OUT_PIN4_ACTIVE_HIGH
from pyraspi.tool.beagle.beagle_py import BG_USB2_HIGH_SPEED
from pyraspi.tool.beagle.beagle_py import BG_USB2_HW_FILTER_PID_IN
from pyraspi.tool.beagle.beagle_py import BG_USB2_HW_FILTER_PID_PING
from pyraspi.tool.beagle.beagle_py import BG_USB2_HW_FILTER_PID_PRE
from pyraspi.tool.beagle.beagle_py import BG_USB2_HW_FILTER_PID_SOF
from pyraspi.tool.beagle.beagle_py import BG_USB2_HW_FILTER_PID_SPLIT
from pyraspi.tool.beagle.beagle_py import BG_USB2_HW_FILTER_SELF
from pyraspi.tool.beagle.beagle_py import BG_USB2_MATCH_TYPE_EQUAL
from pyraspi.tool.beagle.beagle_py import BG_USB_CAPTURE_USB2
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_ACK
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA0
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA1
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA2
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_EXT
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_IN
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_MDATA
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_NAK
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_NYET
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_OUT
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_PING
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_PRE
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_SETUP
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_SOF
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_SPLIT
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_STALL
from pyraspi.tool.beagle.beagle_py import BG_USB_TRIGGER_MODE_IMMEDIATE
from pyraspi.tool.beagle.beagle_py import BeagleUsb2DataMatch
from pyraspi.tool.beagle.beagle_py import BeagleUsb2PacketMatch
from pyraspi.tool.beagle.beagle_py import array
from pyraspi.tool.beagle.beagle_py import bg_close
from pyraspi.tool.beagle.beagle_py import bg_disable
from pyraspi.tool.beagle.beagle_py import bg_enable
from pyraspi.tool.beagle.beagle_py import bg_find_devices_ext
from pyraspi.tool.beagle.beagle_py import bg_host_buffer_used
from pyraspi.tool.beagle.beagle_py import bg_host_ifce_speed
from pyraspi.tool.beagle.beagle_py import bg_latency
from pyraspi.tool.beagle.beagle_py import bg_open
from pyraspi.tool.beagle.beagle_py import bg_samplerate
from pyraspi.tool.beagle.beagle_py import bg_status_string
from pyraspi.tool.beagle.beagle_py import bg_timeout
from pyraspi.tool.beagle.beagle_py import bg_usb2_capture_buffer_config_query
from pyraspi.tool.beagle.beagle_py import bg_usb2_capture_config
from pyraspi.tool.beagle.beagle_py import bg_usb2_capture_status
from pyraspi.tool.beagle.beagle_py import bg_usb2_digital_out_config
from pyraspi.tool.beagle.beagle_py import bg_usb2_digital_out_match
from pyraspi.tool.beagle.beagle_py import bg_usb2_hw_filter_config
from pyraspi.tool.beagle.beagle_py import bg_usb2_read
from pyraspi.tool.beagle.beagle_py import bg_usb2_target_config
from pyraspi.tool.beagle.beagle_py import bg_usb_configure
from pyraspi.tool.beagle.beagle_py import bg_version
from pyraspi.tool.beagle.usbpacket import UsbPacket
from pyraspi.tool.beagle.utils import CollapseInfo
from pyraspi.tool.beagle.utils import IDLE
from pyraspi.tool.beagle.utils import IDLE_THRESHOLD
from pyraspi.tool.beagle.utils import IN
from pyraspi.tool.beagle.utils import IN_ACK
from pyraspi.tool.beagle.utils import IN_NAK
from pyraspi.tool.beagle.utils import KEEP_ALIVE
from pyraspi.tool.beagle.utils import PING
from pyraspi.tool.beagle.utils import PING_NAK
from pyraspi.tool.beagle.utils import PacketQueue
from pyraspi.tool.beagle.utils import SOF
from pyraspi.tool.beagle.utils import SPLIT
from pyraspi.tool.beagle.utils import SPLIT_IN
from pyraspi.tool.beagle.utils import SPLIT_IN_ACK
from pyraspi.tool.beagle.utils import SPLIT_IN_NAK
from pyraspi.tool.beagle.utils import SPLIT_IN_NYET
from pyraspi.tool.beagle.utils import SPLIT_OUT
from pyraspi.tool.beagle.utils import SPLIT_OUT_NYET
from pyraspi.tool.beagle.utils import SPLIT_SETUP
from pyraspi.tool.beagle.utils import SPLIT_SETUP_NYET
from pyraspi.tool.beagle.utils import collapse
from pyraspi.tool.beagle.utils import timestamp_to_ns

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
# Disable COMBINE_SPLITS by setting to False.
# Disabling will show individual split counts for each group (such as SPLIT/IN/ACK, SPLIT/IN/NYET, ...).
# Enabling will show all the collapsed split counts combined.
COMBINE_SPLITS = True

BG_USB_PID_LIST = [BG_USB_PID_OUT, BG_USB_PID_IN, BG_USB_PID_SOF, BG_USB_PID_SETUP, BG_USB_PID_DATA0,
                   BG_USB_PID_DATA1, BG_USB_PID_DATA2, BG_USB_PID_MDATA, BG_USB_PID_ACK, BG_USB_PID_NAK,
                   BG_USB_PID_STALL, BG_USB_PID_NYET, BG_USB_PID_PRE, BG_USB_PID_SPLIT, BG_USB_PID_PING, BG_USB_PID_EXT]
# Maximum number of packets that could be collected during a 10s capture
MAX_PACKET_NUMBER = 300_000

# Logging configuration
# Enable logs on console
ENABLE_STDOUT = False
# Set the flag to True to enable saving data on a file.
SAVE_ON_FILE = False


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BeagleChannel:
    """
    Beagle Channel
    """
    USB = 0
    WIRELESS = 1
# end class BeagleChannel


class Beagle480:
    """
    Define some methods to interact with the Beagle 480 USB Analyser

    documentation: https://www.totalphase.com/support/articles/200472426-beagle-protocol-analyzer-user-manual/
    """

    def __init__(self, test_case, channel_type=None):
        """
        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel_type: The type of channel on which the Beagle is connected, defaults to None - OPTIONAL
        :type channel_type: ``BeagleChannel or None``

        :raise ``Exception``: Too few or too many Beagle devices found on this test setup
        """
        self.port = 0           # open port 0 by default
        self.samplerate = 0     # in kHz (query)
        # See Capture Latency and Timeout Value information in:
        # https://www.totalphase.com/support/articles/200472426-beagle-protocol-analyzer-user-manual/#s6.4.1
        # NB: The latency time should be set to a value shorter than the timeout time.
        self.timeout = 20000  # in milliseconds
        self.latency = 10000  # in milliseconds

        self._usb_packets = None
        self._filtered_packets = None

        self.log_file = None
        if SAVE_ON_FILE:
            # Creation of beagle trace directory
            beagle_trace_dir = join(test_case.getContext().getOutputDir(),
                                    test_case.getContext().getCurrentTarget(), 'beagle')
            if not access(beagle_trace_dir, F_OK):
                makedirs(beagle_trace_dir)
            # end if
            self.log_file = open(join(beagle_trace_dir, f"{test_case.id()}{uuid4()}.txt"), "w")
        # end if

        # Search for devices
        (beagle_device_count, ports, unique_ids) = bg_find_devices_ext(16, 16)
        if beagle_device_count == 0 or beagle_device_count > 2:
            raise Exception(f"{beagle_device_count} Beagle device(s) found on this test setup. 1 or max 2 expected\n")
        elif beagle_device_count == 2:
            if channel_type is not None:
                # Beagle analyser selection strategy in case of multiple units detected rely on its unique identifier
                # - the lower number shall be connected to the USB channel
                # - the second-largest number shall be connected to the Wireless channel
                device_index = channel_type if (unique_ids[0] < unique_ids[1]) else (1 - int(channel_type))
                self.port = ports[device_index]
                self.print_to_output(f"Beagle device on port {self.port} with unique id={unique_ids[device_index]}")
            else:
                raise Exception(f"{beagle_device_count} Beagle devices found. Please select the correct channel type")
            # end if
        # end if

        # Open the device
        self.beagle = bg_open(self.port)
        if self.beagle <= 0:
            stdout.write(f"Unable to open Beagle device on port {self.port}\n")
            raise Exception(f"Error code = {self.beagle}\n")
        # end if
        self.print_to_output(f"Opened Beagle device on port {self.port}")
        self.print_to_output(f"Beagle version {bg_version(self.beagle)}")

        # Query the sample rate since Beagle USB has a fixed sampling rate
        self.samplerate = bg_samplerate(self.beagle, self.samplerate)
        if self.samplerate < 0:
            raise Exception(f"Error when fetching the sample rate. Error code = {bg_status_string(self.samplerate)}\n")
        # end if
        self.print_to_output(f"Sampling rate set to {self.samplerate} KHz")

        # Set the idle timeout.
        # The Beagle read functions will return in the specified time if there is no data available on the bus.
        bg_timeout(self.beagle, self.timeout)
        self.print_to_output(f"Idle timeout set to {self.timeout} ms")

        # Set the latency.
        # The latency parameter allows the programmer to balance the tradeoff between host side buffering and
        # the latency to receive a packet when calling one of the Beagle read functions.
        bg_latency(self.beagle, self.latency)
        self.print_to_output(f"Latency set to {self.latency} ms")
        self.print_to_output(f"Host interface is {(bg_host_ifce_speed(self.beagle) and 'high speed' or 'full speed')}")
        stdout.flush()
    # end def __init__

    def close(self):
        """
        Close the log file and the Beagle device
        """
        if self.log_file is not None:
            self.log_file.close()
        # end if
        if self.beagle is not None:
            # Stop the capture
            bg_disable(self.beagle)
            # Close the device
            bg_close(self.beagle)
        # end if
    # end def close

    def __del__(self):
        if self.beagle is not None:
            # Close the device
            self.close()
            self.beagle = None
        # end if
    # end def __del__

    def start_capture(self, immediate=False, enable_filtering=True):
        """
        Start the capture of the USB traffic

        :param immediate: Flag indicating if the beagle tool is configured for realtime or delayed download - OPTIONAL
        :type immediate: ``bool``
        :param enable_filtering: Flag enabling the HW filtering mechanism - OPTIONAL
        :type enable_filtering: ``bool``

        :raise ``Exception``: Delayed-download is not supported by this model of Beagle 480 protocol analyzer
        """
        if immediate:
            # Configure Beagle 480 for realtime capture
            bg_usb2_capture_config(self.beagle, BG_USB2_CAPTURE_REALTIME)
            bg_usb2_target_config(self.beagle, BG_USB2_AUTO_SPEED_DETECT)
            bg_usb_configure(self.beagle, BG_USB_CAPTURE_USB2, BG_USB_TRIGGER_MODE_IMMEDIATE)
        else:
            # Configure Beagle 480 for delayed download capture
            if bg_usb2_capture_config(self.beagle, BG_USB2_CAPTURE_DELAYED_DOWNLOAD) != BG_OK:
                raise Exception("Delayed-download is not supported by this model of Beagle 480 protocol analyzer.\n")
            # end if

            bg_usb2_target_config(self.beagle, BG_USB2_HIGH_SPEED)
        # end if

        if enable_filtering:
            # Enable the hardware filtering.  This will filter out packets with the same device address
            # as the Beagle analyzer and also filter the PID packet groups listed below.
            bg_usb2_hw_filter_config(self.beagle,
                                     BG_USB2_HW_FILTER_SELF |
                                     BG_USB2_HW_FILTER_PID_SOF |
                                     BG_USB2_HW_FILTER_PID_IN |
                                     BG_USB2_HW_FILTER_PID_PING |
                                     BG_USB2_HW_FILTER_PID_PRE |
                                     BG_USB2_HW_FILTER_PID_SPLIT)
        else:
            # Filter out our own packets.  This is only relevant when one host controller is used.
            bg_usb2_hw_filter_config(self.beagle, BG_USB2_HW_FILTER_SELF)
        # end if

        # Start the capture by calling the bg_enable() function.
        if bg_enable(self.beagle, BG_PROTOCOL_USB) != BG_OK:
            raise Exception(f"Error: could not start USB capture\n")
        # end if
    # end def start_capture

    def print_buffer_usage(self):
        """
        Save internal Beagle buffer usage in logs
        """
        _, _, buffer_size = bg_usb2_capture_buffer_config_query(self.beagle)
        buffer_size *= 1024

        # Poll the hardware buffer status
        (ret, status, _, _, buffer_usage, _) = bg_usb2_capture_status(self.beagle)

        # Store the buffer usage
        self.print_to_output(f"buffer_usage ={buffer_usage}")
        self.print_to_output(f"buffer_size ={buffer_size}")
        self.print_to_output(f"percentage  ={buffer_usage/buffer_size * 100}")
    # end def print_buffer_usage

    def parse(self):
        """
        Parse the packet received during the capture, check for communication errors and add the valid packets
        to the usb packet queue

        NB: ``self._usb_packets`` variable is used to store the parsing result
        """
        self._usb_packets = []
        # Collapsing counts and the time the collapsing started
        collapse_info = CollapseInfo()

        # Packets are saved during the collapsing process
        pkt_q = PacketQueue()

        signal_errors = 0
        packet_number = 0

        # Collapsing packets is handled through a state machine. IDLE is the initial state.
        state = IDLE

        idle_samples = IDLE_THRESHOLD * self.samplerate

        # Start decoding packets
        while packet_number < MAX_PACKET_NUMBER:
            # Info for the current packet
            cur_packet = pkt_q.tail

            (cur_packet.length, cur_packet.status, cur_packet.events, cur_packet.time_sop, cur_packet.time_duration,
             cur_packet.time_dataoffset, cur_packet.data) = bg_usb2_read(self.beagle, cur_packet.data)

            cur_packet.time_sop_ns = timestamp_to_ns(cur_packet.time_sop, self.samplerate)

            # Exit if observed end of capture
            if cur_packet.status & BG_READ_USB_END_OF_CAPTURE:
                collapse_info.clear()
                break
            # end if

            # Check for invalid packet or Beagle error
            if cur_packet.length < 0:
                error_status = "error=%d" % cur_packet.length
                self.get_packet(packet_number, cur_packet, error_status)
                break
            # end if

            # Check for USB error
            if cur_packet.status == BG_READ_USB_ERR_BAD_SIGNALS:
                signal_errors += 1
            # end if

            # Set the PID for collapsing state machine below.  Treat KEEP_ALIVEs as packets.
            if cur_packet.length > 0:
                pid = cur_packet.data[0]
            elif cur_packet.events & BG_EVENT_USB_KEEP_ALIVE and \
                    not cur_packet.status & BG_READ_USB_ERR_BAD_PID:
                pid = KEEP_ALIVE
            else:
                pid = 0
            # end if

            # Collapse these packets appropriately:
            # SOF* (IN (ACK|NAK))* (PING NAK)* (SPLIT (OUT|SETUP) NYET)* (SPLIT IN (ACK|NYET|NACK))*

            # If the time elapsed since collapsing began is greater than the threshold, zero out the counters.
            if cur_packet.time_sop - collapse_info.time_sop >= idle_samples:
                (packet_number, signal_errors) = self.get_summary_packet(packet_number, collapse_info, signal_errors)
            # end if

            re_run = True
            while re_run:
                re_run = False
                if state == IDLE:
                    # The initial state of the state machine. Collapse SOFs and KEEP_ALIVEs.
                    # Save IN, PING, or SPLIT packets and move to the next state for the next packet.
                    # Otherwise, update the collapsed packet counts and the current packet.
                    if pid == KEEP_ALIVE:
                        collapse(KEEP_ALIVE, collapse_info, pkt_q)
                    elif pid == BG_USB_PID_SOF:
                        collapse(SOF, collapse_info, pkt_q)
                    elif pid == BG_USB_PID_IN:
                        pkt_q.save_packet()
                        state = IN
                    elif pid == BG_USB_PID_PING:
                        pkt_q.save_packet()
                        state = PING
                    elif pid == BG_USB_PID_SPLIT:
                        pkt_q.save_packet()
                        state = SPLIT
                    else:
                        (packet_number, signal_errors) = (
                            self.get_summary_packet(packet_number, collapse_info, signal_errors))
                        collapse_info.clear()

                        if (cur_packet.length > 0 or cur_packet.events or
                                (cur_packet.status != 0 and cur_packet.status != BG_READ_TIMEOUT)):
                            self.get_packet(packet_number, cur_packet, 0)
                            packet_number += 1
                        # end if
                    # end if
                elif state == IN:
                    # Collapsing IN+ACK or IN+NAK.
                    # Otherwise, output any saved packets and rerun the collapsing state machine on the current packet.
                    state = IDLE
                    if pid == BG_USB_PID_ACK:
                        collapse(IN_ACK, collapse_info, pkt_q)
                    elif pid == BG_USB_PID_NAK:
                        collapse(IN_NAK, collapse_info, pkt_q)
                    else:
                        re_run = True
                    # end if
                elif state == PING:
                    # Collapsing PING+NAK
                    state = IDLE
                    if pid == BG_USB_PID_NAK:
                        collapse(PING_NAK, collapse_info, pkt_q)
                    else:
                        re_run = True
                    # end if
                elif state == SPLIT:
                    # Expecting an IN, OUT, or SETUP
                    if pid == BG_USB_PID_IN:
                        pkt_q.save_packet()
                        state = SPLIT_IN
                    elif pid == BG_USB_PID_OUT:
                        pkt_q.save_packet()
                        state = SPLIT_OUT
                    elif pid == BG_USB_PID_SETUP:
                        pkt_q.save_packet()
                        state = SPLIT_SETUP
                    else:
                        state = IDLE
                        re_run = True
                    # end if
                elif state == SPLIT_IN:
                    # Collapsing SPLIT+IN+NYET, SPLIT+IN+NAK, SPLIT+IN+ACK
                    state = IDLE
                    if pid == BG_USB_PID_NYET:
                        collapse(SPLIT_IN_NYET, collapse_info, pkt_q)
                    elif pid == BG_USB_PID_NAK:
                        collapse(SPLIT_IN_NAK, collapse_info, pkt_q)
                    elif pid == BG_USB_PID_ACK:
                        collapse(SPLIT_IN_ACK, collapse_info, pkt_q)
                    else:
                        re_run = True
                    # end if
                elif state == SPLIT_OUT:
                    # Collapsing SPLIT+OUT+NYET
                    state = IDLE
                    if pid == BG_USB_PID_NYET:
                        collapse(SPLIT_OUT_NYET, collapse_info, pkt_q)
                    else:
                        re_run = True
                    # end if
                elif state == SPLIT_SETUP:
                    # Collapsing SPLIT+SETUP+NYET
                    state = IDLE
                    if pid == BG_USB_PID_NYET:
                        collapse(SPLIT_SETUP_NYET, collapse_info, pkt_q)
                    else:
                        re_run = True
                    # end if
                # end if

                if not re_run:
                    break
                # end if

                # The state machine is about to be re-run.
                # This means that a complete packet sequence wasn't collapsed and there are packets in the queue
                # that need to be output before we can process the current packet.
                (packet_number, signal_errors) = self.output_saved(packet_number, signal_errors, collapse_info, pkt_q)
            # end while
        # end while

        self.print_to_output(f'packet_number = {packet_number}')
    # end def parse

    def empty_queue(self):
        """
        Empty the internal buffer of the Beagle 480 USB analyzer while a capture is already in progress.
        """
        # Packets to be discarded
        pkt_q = PacketQueue()

        # Start decoding packets
        while bg_host_buffer_used(self.beagle) != 0:
            # Info for the current packet
            cur_packet = pkt_q.tail

            (cur_packet.length, _, _, _, _, _, cur_packet.data) = bg_usb2_read(self.beagle, cur_packet.data)
            packet_data = self.get_data_packet(cur_packet.data, cur_packet.length)

            self.print_to_output(f"Empty queue: packet received with data = {packet_data}")
        # end while
    # end def empty_queue

    def filter(self, pid_filtering_list=None, report_filtering_list=None):
        """
        Filter the captured packets by packet PID or report length

        NB: ``self._filtered_packets`` variable is used to store the filtering result

        :param pid_filtering_list: List of valid packet identifiers
                                   ex: [BG_USB_PID_DATA0, BG_USB_PID_DATA1] - OPTIONAL
        :type pid_filtering_list: ``list[int]`` or ``None``
        :param report_filtering_list: List of valid packet identifiers
                                      ex: [BG_USB_PID_DATA0, BG_USB_PID_DATA1] - OPTIONAL
        :type report_filtering_list: ``list[TimestampedBitFieldContainerMixin]`` or ``None``
        """
        self._filtered_packets = []
        for usb_packet in self._usb_packets:
            data_length = len(usb_packet.data) if usb_packet.data is not None else 0
            if usb_packet.pid not in pid_filtering_list:
                continue
            elif (usb_packet.data == "" or
                  (report_filtering_list is not None and
                   data_length not in [x.BITFIELD_LENGTH for x in report_filtering_list])):
                continue
            elif report_filtering_list is not None:
                for report in report_filtering_list:
                    if data_length == report.BITFIELD_LENGTH:
                        self._filtered_packets.append(report.fromHexList(HexList(usb_packet.data),
                                                                         timestamp=usb_packet.timestamp))
                        break
                    # end if
                # end for
            # end if
        # end for
    # end def filter

    def get_packet(self, packet_number, packet, error_status):
        """
        Process and log a USB packet.

        :param packet_number: The current packet number
        :type packet_number: ``int``
        :param packet:  The packet data
        :type packet: ``PacketInfo``
        :param error_status: The error status of the packet
        :type error_status: ``int``
        """
        if error_status == 0 and packet.length >= 3:
            error_status = ""
            packet_data = self.get_data_packet(packet.data, packet.length)
            usb_packet = UsbPacket(pid=packet_data[0],
                                   data=packet_data[1:packet.length-2] if packet.length > 3 else None,
                                   crc=packet_data[packet.length-2:packet.length], timestamp=packet.time_sop_ns)
            usb_packet.status = packet.status
            usb_packet.event = packet.events

            self._usb_packets.append(usb_packet)
        else:
            packet_data = ""
        # end if

        self.print_to_output(f"{packet_number},{packet.time_sop_ns},USB,({error_status} "
                             f"{UsbPacket.general_status_to_str(packet.status)} "
                             f"{UsbPacket.usb_status_to_str(packet.status)}"
                             f"{UsbPacket.usb_events_to_str(packet.events)}),{str(packet_data)}")
    # end def get_packet

    @staticmethod
    def get_data_packet(packet, length):
        """
        Convert packet data to a hexadecimal string

        :param packet:  The packet data
        :type packet: ``PacketInfo``
        :param length:  The length of the packet data
        :type length: ``int``

        :return: A HexList object containing the hexadecimal string representation of the packet data
        :rtype: ``HexList``
        """
        packet_string = ""

        # Get the packet data
        for n in range(length):
            packet_string += f"{packet[n]:02X}"
        # end for
        return HexList(packet_string)
    # end def get_data_packet

    def get_summary_packet(self, packet_number, collapse_info, signal_errors):
        """
        Generate a summary of USB packet information and log it

        :param packet_number: The current packet number
        :type packet_number: ``int``
        :param collapse_info: The collapse information
        :type collapse_info: ``CollapseInfo``
        :param signal_errors: The signal errors count
        :type signal_errors: ``int``

        :return: A tuple containing the updated packet number and 0 for signal errors count
        :rtype: ``tuple[int, int]``
        """
        offset = 0
        summary = ""

        counts = [collapse_info.count[key] for key in collapse_info.count if collapse_info.count[key] > 0]

        if len(counts) > 0:
            summary += "COLLAPSED "

            if collapse_info.count[KEEP_ALIVE] > 0:
                summary += f"[{collapse_info.count[KEEP_ALIVE]} KEEP-ALIVE] "
            # end if

            if collapse_info.count[SOF] > 0:
                summary += f"[{collapse_info.count[SOF]} SOF] "
            # end if

            if collapse_info.count[IN_ACK] > 0:
                summary += f"[{collapse_info.count[IN_ACK]} IN/ACK] "
            # end if

            if collapse_info.count[IN_NAK] > 0:
                summary += f"[{collapse_info.count[IN_NAK]} IN/NAK] "
            # end if

            if collapse_info.count[PING_NAK] > 0:
                summary += f"[{collapse_info.count[PING_NAK]} PING/NAK] "
            # end if

            if COMBINE_SPLITS:
                split_count = collapse_info.count[SPLIT_IN_ACK] + \
                              collapse_info.count[SPLIT_IN_NYET] + \
                              collapse_info.count[SPLIT_IN_NAK] + \
                              collapse_info.count[SPLIT_OUT_NYET] + \
                              collapse_info.count[SPLIT_SETUP_NYET]

                if split_count > 0:
                    summary += f"[{split_count} SPLITS] "
                # end if
            else:
                if collapse_info.count[SPLIT_IN_ACK] > 0:
                    summary += f"[{collapse_info.count[SPLIT_IN_ACK]} SPLIT/IN/ACK] "
                # end if

                if collapse_info.count[SPLIT_IN_NYET] > 0:
                    summary += f"[{collapse_info.count[SPLIT_IN_NYET]} SPLIT/IN/NYET] "
                # end if

                if collapse_info.count[SPLIT_IN_NAK] > 0:
                    summary += f"[{collapse_info.count[SPLIT_IN_NAK]} SPLIT/IN/NAK] "
                # end if

                if collapse_info.count[SPLIT_OUT_NYET] > 0:
                    summary += f"[{collapse_info.count[SPLIT_OUT_NYET]} SPLIT/OUT/NYET] "
                # end if

                if collapse_info.count[SPLIT_SETUP_NYET] > 0:
                    summary += f"[{collapse_info.count[SPLIT_SETUP_NYET]} SPLIT/SETUP/NYET] "
                # end if
            # end if
            self.log_summary(packet_number+offset, collapse_info.time_sop, summary)
            offset += 1
        # end if

        # Output any signal errors
        if signal_errors > 0:
            summary += f"<{signal_errors} SIGNAL ERRORS>"
            self.log_summary(packet_number+offset, collapse_info.time_sop, summary)
            offset += 1
        # end if

        collapse_info.clear()
        return packet_number + offset, 0
    # end def get_summary_packet

    def log_summary(self, i, count_sop, summary):
        """
        Log a summary of USB packet information

        :param i: The index of the packet
        :type i: ``int``
        :param count_sop: The count of start of packet occurrences.
        :type count_sop: ``int``
        :param summary: The summary of USB packet information.
        :type summary: ``str``
        """
        count_sop_ns = timestamp_to_ns(count_sop, self.samplerate)
        self.print_to_output(f"{i},{count_sop_ns},USB,( ),{summary}")
    # end def log_summary

    def output_saved(self, packet_number, signal_errors, collapse_info, pkt_q):
        """
        Process and output saved packets with additional information.

        This function processes and outputs the saved packets with additional information such as packet number and
        signal errors count.

        :param packet_number: The current packet number
        :type packet_number: ``int``
        :param signal_errors: The signal errors count
        :type signal_errors: ``int``
        :param collapse_info: The collapse information
        :type collapse_info: ``CollapseInfo``
        :param pkt_q: The packet queue
        :type pkt_q: ``PacketQueue``

        :return: A tuple containing the updated packet number and signal errors count
        :rtype: ``tuple[int, int]``
        """
        (packet_number, signal_errors) = self.get_summary_packet(packet_number, collapse_info, signal_errors)
        collapse_info.clear()

        packets = pkt_q.clear(dequeue=True)

        for pkt in packets:
            self.get_packet(packet_number, pkt, 0)
            packet_number += 1
        # end for

        return packet_number, signal_errors
    # end def output_saved

    def get_filtered_packets(self):
        """
        Retrieve the filtered packets

        This function returns the filtered packets stored in the object instance

        :return: The filtered packets.
        :rtype: ``list[TimestampedBitFieldContainerMixin]``
        """
        return self._filtered_packets
    # end def get_filtered_packets

    def setup_digital_output(self, device_address=None, endpoint=None, data=None, data_valid=None):
        """
        Configure the digital output pin 4 to trig on a specific match on a particular bus data

        :param device_address: 	The device address on which to match - OPTIONAL
        :type device_address: ``int`` or ``None``
        :param endpoint: The endpoint number on which to match - OPTIONAL
        :type endpoint: ``int`` or ``None``
        :param data: The data array determines which values the user would like to match The first byte of this array
                     would correlate to the first byte of the packet- OPTIONAL
        :type data: ``list[int]`` or ``None``
        :param data_valid: Determines which of those bytes in the data array are valid for matching. Setting a byte to
                           zero in the data_valid array means that byte is a dont-care condition for the matching
                           algorithm - OPTIONAL
        :type data_valid: ``list[int]`` or ``None``

        :raise ``AssertionError``: length of ``data`` and ``data_valid`` are not equal
        """
        # The packet_match structure is initialized to zero so only the fields that we want enabled need to be set.
        packet_match = BeagleUsb2PacketMatch()
        if device_address is not None:
            packet_match.dev_match_type = BG_USB2_MATCH_TYPE_EQUAL
            packet_match.dev_match_val = device_address
        # end if
        if endpoint is not None:
            packet_match.ep_match_type = BG_USB2_MATCH_TYPE_EQUAL
            packet_match.ep_match_val = endpoint
        # end if

        # The data_match structure is initialized to zero so only the fields that we want enabled need to be set.
        data_match = BeagleUsb2DataMatch()
        data_match.data_match_type = BG_USB2_MATCH_TYPE_EQUAL
        data_match.data_match_pid = BG_USB2_DATA_MATCH_DATA0 | BG_USB2_DATA_MATCH_DATA1
        if data is not None and data_valid is not None:
            assert len(data) == len(data_valid)
            data_match.data = array('B', data)
            data_match.data_valid = array('B', data_valid)
        # end if

        # Enable digital output pin 4
        bg_usb2_digital_out_config(self.beagle,
                                   BG_USB2_DIGITAL_OUT_ENABLE_PIN4,
                                   BG_USB2_DIGITAL_OUT_PIN4_ACTIVE_HIGH)

        # Configure digital output pin 4 match pattern
        bg_usb2_digital_out_match(self.beagle,
                                  BG_USB2_DIGITAL_OUT_MATCH_PIN4,
                                  packet_match, data_match)
        self.print_to_output("Configuring digital output pin 4")
    # end def setup_digital_output


    def print_to_output(self, string):
        """
        Wrapper to save the logs in a file or sent them to the console depending on global constants configuration

        :param string: The given string to be printed
        :type string: ``str``
        """
        if SAVE_ON_FILE and self.log_file is not None:
            self.log_file.write(f"{string}\n")
        # end if
        if ENABLE_STDOUT:
            stdout.write(f"{string}\n")
            stdout.flush()
        # end if
    # end def print_to_output
# end class Beagle480

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
