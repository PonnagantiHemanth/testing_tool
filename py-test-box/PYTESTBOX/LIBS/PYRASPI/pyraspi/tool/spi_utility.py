#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
"""
:package: pyraspi.tool.spi_utility
:brief:   Utility for SPI control.
:author:  Lila Viollette <lviollette@logitech.com>, Fred Chen <fchen7@logitech.com>
:date:    2021/02/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

# Add PYRASPI folder to PYTHONPATH
import sys
import os.path as op
FILE_PATH = op.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("LIBS")]
PYRASPI_DIR = op.join(WS_DIR, "LIBS", "PYRASPI")
if PYRASPI_DIR not in sys.path:
    sys.path.insert(0, PYRASPI_DIR)
# end if

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from pyraspi.bus.spidev.spi import SPIDEV
from pyraspi.bus.spidev.spi import SPIDevice

from threading import Thread
from time import perf_counter


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SpiUtility(object):
    """
    Raspberry Pi SPI port test utility.

    Requirements:
    1. Enabled SPI in /boot/config.txt, https://elinux.org/RPi_SPI#Loopback_test
    2. Installed Python py-spidev library, https://github.com/doceme/py-spidev
    """
    VERSION = '0.1.0.0'

    def __init__(self):
        self._parser = None

        self.spi_threads = []

        self.args = self.parse_args()
        self.command_handler()
    # end def __init__

    def get_parser(self):
        """
        Parses script's arguments.

        :return: ArgumentParser instance
        :rtype: ``ArgumentParser``
        """
        if self._parser is None:
            parser = ArgumentParser(description='Raspberry Pi SPI control utility, based on py-spidev library.',
                                    formatter_class=RawDescriptionHelpFormatter,
                                    allow_abbrev=True)
            parser.add_argument('--version', action='version', version=self.VERSION)
            parser.add_argument('-m', '--mode', dest='spi_mode', type=int, choices=[0, 1, 2, 3],
                                default=0, const=0, nargs='?',
                                help='''SPI clock mode (polarity & phase): 
                                    Mode 0 CPOL:0/CPHA:0, 
                                    Mode 1 CPOL:0/CPHA:1, 
                                    Mode 2 CPOL:1/CPHA:0, 
                                    Mode 3 CPOL:1/CPHA:1.''')
            parser.add_argument('-t', '--throughput', dest='cmd_throughput', type=int, nargs=4, action='append',
                                help="Measure SPI loopback throughput. "
                                     "This command can be repeated for each bus to test in parallel.",
                                metavar=('bus', 'speed', 'block_size', 'count'))
            parser.epilog = """
Argument details:
  'bus' is the SPI bus number X, when device is registered as /dev/spiX.Y.
  'speed' is the SPI bus clock frequency in MHz.
  'block_size' is the number of byte of each message.
  'count' is the number of time the measurement take place.
"""
            self._parser = parser
        # end if

        return self._parser
    # end def get_parser

    parser = property(get_parser)

    def parse_args(self):
        """
        Parses the program arguments.

        :return: list of parsed arguments
        :rtype: ``Namespace``
        """
        parser = self.get_parser()
        return parser.parse_args()
    # end def parse_args

    def command_handler(self):
        """
        Runs the commands listed in program arguments.
        Note: Expand this script functionality by adding a command to be dispatched here.
        """
        if self.args.cmd_throughput:
            self.check_throughput()
        # end if
    # end def command_handler

    def check_throughput(self):
        """
        Measures SPI loopback throughput and checks data integrity.
        Sequence of action:
        1) Get SPI ports configuration.
        2) Create a thread for each SPI port.
        3) Start thread and wait for test completion.
        4) Check RX data against TX data (loopback mode).
        5) Print results.

        :raise ``AssertionError``: Invalid port length
        """
        # Instantiate a thread for each SPI port to test
        for port in self.args.cmd_throughput:
            assert len(port) == 4       # Expect 4 arguments per SPI port:
            bus = port[0]               # 1) SPI peripheral identifier
            speed = port[1] * 1000000   # 2) Clock frequency in Hz (converted from MHz)
            block_size = port[2]        # 3) Number of byte per block
            count = port[3]             # 4) Number of time the measurement take place

            mode = self.args.spi_mode   # Clock polarity & phase, common to all SPI ports

            # Create a thread to run the test
            thread = self.TestRunner(bus, mode, speed, block_size, count)
            self.spi_threads.append(thread)
        # end for

        # Start tests
        for thread in self.spi_threads:
            thread.start()
        # end for

        # Wait for tests to finish
        for thread in self.spi_threads:
            thread.join()
        # end for

        # Verify received data integrity (loopback mode)
        for thread in self.spi_threads:
            thread.check_data_integrity()
        # end for

        # Print results
        for thread in self.spi_threads:
            self.print_results(thread.bus, thread.total_bytes, thread.time_consumed, thread.error_count)
        # end for
    # end def check_throughput

    @staticmethod
    def print_results(bus, total_bytes, time_consumed, error_count):
        """
        Prints test results.

        :param bus: SPI bus identifier
        :type bus: ``int``
        :param total_bytes: RX bytes count
        :type total_bytes: ``int``
        :param time_consumed: Time spent running the test
        :type time_consumed: ``float``
        :param error_count: Number of errors detected during the test
        :type error_count: ``int``
        """
        throughput = total_bytes // time_consumed if time_consumed else 0
        print(f'Device: {SPIDEV}{bus}.0\n'
              f'Time: {round(time_consumed * 1000, 3)} ms\n'
              f'Total: {total_bytes} Bytes\n'
              f'Error: {error_count}\n'
              f'Throughput: {throughput // 1024} KiB/s\n'
              f'            {throughput // 1000} Byte/ms\n')
    # end def print_results

    class TestRunner(Thread):
        """
        Runs SPI test in a thread.
        Sequence of action:
        1) Init thread to configure SPI port:
            'TestRunner(bus, mode, speed, block_size, count)'
        2) Start test:
            'thread.start()'
        3) Wait for test to finish, all collect results:
            'thread.join()'
        4) SPI port will be automatically closed when thread is terminated.
        """
        def __init__(self, bus, mode, speed, block_size, count):
            """
            :param bus: SPI bus identifier
            :type bus: ``int``
            :param mode: SPI bus mode (clock polarity & phase)
            :type mode: ``int``
            :param speed: SPI bus speed in [Hz]
            :type speed: ``int``
            :param block_size: Size in byte of the block of data to be sent as part of the test
            :type block_size: ``int``
            :param count: Number of time the block of data will be sent as part of the test
            :type count: ``int``
            """
            # Initialize Thread and set its name
            Thread.__init__(self, name=f"{self.__class__.__name__}_SPI{bus}")

            # Initialize SPI parameters
            self.bus = bus                  # SPI peripheral identifier
            self.block_size = block_size    # Number of byte per block
            self.count = count              # Number of time the measurement take place
            self.spi = self.init_spi_port(bus, mode, speed)  # Open and configure SPI port

            # Test data: initialize TX buffer (1D array, constant)
            self.tx_data = bytes((x & 0xFF) for x in range(0, block_size))

            # Initialize RX buffer (2D array: each RX array will be appended)
            self.rx_data = []

            # Initialize time and byte counters
            self.t0 = 0
            self.t1 = 0
            self.time_consumed = 0
            self.total_bytes = 0
            self.error_count = 0
        # end def __init__

        @staticmethod
        def init_spi_port(bus, mode, speed):
            """
            Configures SPI port.

            :param bus: SPI bus identifier
            :type bus: ``int``
            :param mode: SPI bus mode (clock polarity & phase)
            :type mode: ``int``
            :param speed: SPI bus speed in [Hz]
            :type speed: ``int``

            :return: SPIDevice object
            :rtype: ``SPIDevice``
            """
            # Open and configure SPI device
            spi = SPIDevice(bus=bus, chip_select=0)
            spi.open()
            spi.clock_mode = mode  # Clock polarity & phase
            spi.speed_hz = speed  # Clock frequency in Hz
            return spi
        # end def init_spi_port

        def run(self):
            """
            Starts the test and measures the time it takes.
            This thread method is called via 'thread.start()'
            """
            # Start timing measurement
            self.t0 = perf_counter()

            # Perform loopback throughput measurements
            self.spi_loopback()

            # Stop timing measurement
            self.t1 = perf_counter()
            self.time_consumed = self.t1 - self.t0
        # end def run

        def spi_loopback(self):
            """
            Tests SPI in loopback mode.
            The data block to be sent is pre-filled with a defined content.
            The same data block is sent over the line multiple time.
            Each received data block is stored for later verification.
            """
            # Transfer the block 'repeat' times over
            for _ in range(self.count):
                # Execute SPI transfer
                rx_data = self.spi.transaction(self.tx_data)

                # Save RX buffer for later verification
                self.rx_data.append(rx_data)

                # Increment to byte counter (RX and TX lines carry the same amount of data per definition)
                self.total_bytes += len(rx_data)
            # end for
        # end def spi_loopback

        def check_data_integrity(self):
            """
            Verifies received data integrity.
            Loopback mode: The received data should match the data that was sent.

            :raise ``AssertionError``: Invalid block size
            """
            assert len(self.rx_data) == self.count
            for block in self.rx_data:
                assert len(block) == self.block_size
                for i in range(0, self.block_size):
                    if block[i] != self.tx_data[i]:
                        self.error_count += 1
                    # end if
                # end for
            # end for
        # end def check_data_integrity
    # end class TestRunner
# end class SpiUtility


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
    Entry point of the SPI test script
    """
    SpiUtility()
# end if


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
