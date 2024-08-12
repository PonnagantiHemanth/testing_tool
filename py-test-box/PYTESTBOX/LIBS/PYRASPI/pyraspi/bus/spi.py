#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: pyraspi.bus.spi
:brief: Manages the SPI connections between RaspberryPi and FPGA
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/03/19
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from queue import Empty
from queue import Queue
from threading import Thread
from time import time

from pyraspi.bus.spidev.spi import SPIDevice
from pyraspi.services.kosmos.module.error import KosmosFatalErrorException
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
# Available SPI buses for this project, on a RaspberryPi 4B
BUS = {
    'SPI0': 0,
    'SPI4': 4,
    'SPI5': 5,
    'SPI6': 6,
    # Second SPI bus on a Raspberry Pi 5 Model B
    'SPI10': 10,
}

# Maximum timeout user can set, in seconds
SPI_RX_TIMEOUT_MAX = 1


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class SpiTransactionError(KosmosFatalErrorException, Exception):
    """
    SPI transaction error base class.
    """
    pass
# end class SpiTransactionError


class SpiTransactionTimeoutError(SpiTransactionError, TimeoutError):
    """
    Exception emitted if SPI packet reply was not received after a given timeout.
    """
    pass
# end class SpiTransactionTimeoutError


class SpiTransactionCrcError(SpiTransactionError):
    """
    Exception emitted if SPI packet reply has invalid Frame CRC.
    """
    pass
# end class SpiTransactionCrcError


class SpiTransactionSequenceError(SpiTransactionError):
    """
    Exception emitted if SPI packet reply has invalid Frame Sequence ID.
    """
    pass
# end class SpiTransactionSequenceError


class SPI(Thread):
    """
    SPI bus interface: Handles the full-duplex SPI transactions.

    Note: ``SPIInitError`` will be raised if the SPI bus is already open
    """

    # Dummy frame (all zero)
    _dummy_frame = MessageFrame()

    class StopSignal(object):
        """
        Arbitrary 'Stop' signal to be sent in TX queue to interrupt the SPI thread's ``self.run()`` function.
        """
        pass
    # end class StopSignal

    def __init__(self, bus, mode, speed):
        """
        :param bus: SPI bus identifier
        :type bus: ``int``
        :param mode: SPI bus mode (clock polarity & phase). Refer to ``pyraspi.bus.spidev.spi.SPIDevice.clock_mode()``.
        :type mode: ``int``
        :param speed: SPI bus speed in [Hz]
        :type speed: ``int``
        """
        # Initialize Thread and set its name
        Thread.__init__(self, name=f"{self.__class__.__name__}_SPI{bus}")

        self.spi_bus = bus
        self.spi_mode = mode
        self.spi_speed_hz = speed
        self.spi = SPIDevice(bus=bus, chip_select=0)

        self.rx_queue = Queue()
        self.tx_queue = Queue()

        self.tx_seq_counter = 1

        self.rx_timeout = 0.1  # in second

        self._open()
    # end def __init__

    def __del__(self):
        """
        Close the SPI interface.
        """
        self._close()
    # end def __del__

    def _open(self):
        """
        Open SPI device and sets clock speed & mode.

        :raise ``AssertionError``: if the SPI bus mode or speed was not set correctly
        """
        self.spi.open()
        self.spi.clock_mode = self.spi_mode    # Clock polarity & phase
        self.spi.speed_hz = self.spi_speed_hz  # Clock frequency in Hz

        assert self.spi_mode == self.spi.clock_mode, f'Expected SPI mode {self.spi_mode}, got {self.spi.clock_mode}'
        assert self.spi_speed_hz == self.spi.speed_hz, (f'Expected SPI frequency {self.spi_speed_hz} Hz, '
                                                        f'got {self.spi.speed_hz}')
    # end def _open

    def _close(self):
        """
        Close SPI device.
        """
        if getattr(self, 'spi', None) is not None and self.spi.fd is not None:
            self.spi.close()
        # end if
    # end def _close

    def send(self, packet):
        """
        Send a packet and get reply.
        A packet is composed of zero or more ``MessageFrame``.

        OSI Layer 2: DATA LINK (split packet into frames; send/receive frames).

        Note: ``SpiTransactionTimeoutError`` will be raised if reply is not received within a defined time.

        :param packet: TX Message(s)
        :type packet: ``list[MessageFrame]``

        :return: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :rtype: ``list[tuple[MessageFrame, MessageFrame]]``

        :raise ``AssertionError``: if the SPI bus is not opened
        :raise ``TypeError``: if packet type is unexpected
        """
        assert self.spi.fd

        # Ensure packet is composed of MessageFrames
        if not isinstance(packet, list) or not all(isinstance(p, MessageFrame) for p in packet):
            raise TypeError(packet)
        # end if

        # Set Sequence ID and compute CRC
        for frame in packet:
            frame.frame.seq_id = self.tx_seq_counter
            frame.compute_store_crc()

            # Increment and wrap Sequence ID
            self.tx_seq_counter += 1
            if self.tx_seq_counter > 0xFF:
                # skips sequence ID 0, to distinguish from null-frame
                self.tx_seq_counter = 1
            # end if
        # end for

        # Send packet
        self.tx_queue.put(packet)

        # Wait for reply (or timeout)
        txrx_frames = self.rx_queue.get()

        # Sanity check
        assert txrx_frames is not self.StopSignal, f'StopSignal received in place of data.'

        # If reply is an error, raise it from here
        if isinstance(txrx_frames, Exception):
            raise txrx_frames
        # end if

        return txrx_frames
    # end def send

    def stop(self):
        """
        Request stop of current thread.
        This solution is the simplest and most effective.
        https://stackoverflow.com/a/5987293/1641819
        """
        try:
            # Empty TX queue
            while self.tx_queue.get_nowait():
                pass
            # end while
        except Empty:
            pass
        finally:
            # Send Stop signal
            self.tx_queue.put(self.StopSignal)
        # end try
    # end def stop

    def run(self):
        """
        Thread function: Send & receive SPI packets in an infinite loop.
        A packet is composed of zero or more ``MessageFrames``.

        TX packets are fetched from ``self.tx_queue`` (blocking operation).
        (TX, RX) packets are pushed to ``self.rx_queue`` (non-blocking operation).

        This function returns when ``self.stop()`` is called, then the thread terminates.
        """
        try:
            while True:
                # Get TX packet from TX queue
                tx_packet = self.tx_queue.get()

                # Check for stop signal
                if tx_packet is self.StopSignal:
                    break
                # end if

                # Perform SPI transaction (with timeout)
                try:
                    txrx_packet = self._run_pipelined_spi_transaction(tx_packet, self.rx_timeout)
                except SpiTransactionError as error:
                    # Push Error to RX queue
                    self.rx_queue.put(error)
                else:
                    # Push (TX, RX) packet to RX queue
                    self.rx_queue.put(txrx_packet)
                # end try
            # end while
        finally:
            # Close SPI resources before exiting thread
            self._close()
        # end try
    # end def run

    def _run_pipelined_spi_transaction(self, packet, timeout):
        """
        Send and receive a packet over SPI, using full-duplex, pipelined strategy.
        A packet is composed of zero or more ``MessageFrames``.

        Note: this method will return:
         - RX & TX messages, in normal cases
         - ``SpiTransactionTimeoutError``: if no reply is received within a defined time
         - ``SpiTransactionSequenceError``: if received unmatched sequence id number
         - ``SpiTransactionSequenceError``: if received frame with invalid CRC

        :param packet: list of zero or more TX ``MessageFrame``
        :type packet: ``list[MessageFrame]``

        :param timeout: maximum duration to wait for a reply, in seconds
        :type timeout: ``float``

        :return: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``, or errors
        :rtype: ``list[tuple[MessageFrame, MessageFrame]] or SpiTransactionSequenceError or SpiTransactionTimeoutError``

        :raise ``TypeError``: if packet type is unexpected.
        :raise ``ValueError``: if timeout value is out of bounds [0 to ``SPI_RX_TIMEOUT_MAX``]
        :raise ``SpiTransactionError``: if system time is not monotonically increasing.
        :raise ``AssertionError``: Reply message length is invalid
        """
        # Ensure packet is composed of MessageFrames
        if not isinstance(packet, list) or not all(isinstance(p, MessageFrame) for p in packet):
            raise TypeError(packet)
        # end if

        # Check timeout bounds, in seconds
        if not (0 <= timeout <= SPI_RX_TIMEOUT_MAX):
            raise ValueError(timeout)
        # end if

        # Transaction loop
        tx_index = 0
        rx_index = 0
        time_start = time()
        frame_count = len(packet)
        rx_frames = list()
        # For error logging
        rx_dummy_frames_num = 0
        tx_dummy_frames_num = 0
        while tx_index < frame_count or rx_index < frame_count:
            # Select TX frame
            if tx_index < frame_count:
                tx_frame = packet[tx_index]
                tx_index += 1
            else:
                # no more TX frame to send, use dummy frame instead (all null)
                tx_frame = SPI._dummy_frame
                tx_dummy_frames_num += 1
            # end if

            # Perform RX/TX SPI transaction
            rx_buffer = self._transaction(tx_frame.raw.byte)
            rx_frame = MessageFrame(buffer=rx_buffer)

            # Check RX frame validity
            if sum(rx_frame.raw.dword) == 0:
                # Received dummy RX frame (all null)
                rx_dummy_frames_num += 1

                # Debug to ensure that system timestamp are valid
                monotonic_time = time() > time_start
                if not monotonic_time:
                    raise SpiTransactionError("System time is not monotonic!\n"
                                              "Now is after the beginning of the transaction")
                # end if
            elif rx_frame.frame.seq_id != packet[rx_index].frame.seq_id:
                # Received wrong sequence id number
                return SpiTransactionSequenceError(
                    f'[SPI{self.spi_bus}]: Received unmatched sequence id number: \n'
                    f'TX: {packet[rx_index].str_raw_memory()}\n'
                    f'RX: {rx_frame.str_raw_memory()}')
            elif not rx_frame.is_crc_valid():
                # Received frame with invalid CRC
                return SpiTransactionSequenceError(
                    f'[SPI{self.spi_bus}]: Received frame with invalid CRC.\n'
                    f'Received {rx_frame.frame.crc:#04x}, '
                    f'Expected {rx_frame.compute_crc():#04x}.\n'
                    f'RX: {rx_frame.str_raw_memory()}\n')
            else:
                # Received valid RX frame, save it
                rx_frames.append(rx_frame)
                rx_index += 1
                time_start = time()
            # end if

            if time() > time_start + timeout:
                # Timeout
                return SpiTransactionTimeoutError(
                    f'[SPI{self.spi_bus}]: Timeout after ({(time()-time_start):.4f} s) '
                    'while waiting for reply of message:\n'
                    f'  TX: {packet[rx_index].str_raw_memory()}\n'
                    f'  RX: {rx_frame.str_raw_memory()}\n'
                    f'  RX Dummy frame num: {rx_dummy_frames_num}\n'
                    f'  TX Dummy frame num: {tx_dummy_frames_num}\n')
            # end if
        # end while

        # save results
        assert len(packet) == len(rx_frames)
        return list(zip(packet, rx_frames))
    # end def _run_pipelined_spi_transaction

    def _transaction(self, data):
        """
        SPI transaction: Send one frame, while receiving another one.
        (SPI is full-duplex)

        :param data: Bytes to send via the SPI device.
        :type data: ``bytes``
        :return: returned bytes from SPI device
        :rtype: ``bytes``

        :raise ``AssertionError``: SPI file descriptor is null (not open)
        """
        assert self.spi.fd

        rx_frame = self.spi.transaction(data)
        return rx_frame
    # end def _transaction
# end class SPI


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
