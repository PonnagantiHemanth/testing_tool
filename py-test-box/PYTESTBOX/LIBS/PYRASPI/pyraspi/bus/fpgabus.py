#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: pyraspi.bus.fpgabus
:brief: Abstracts the connection layers between RaspberryPi and FPGA
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/03/19
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import Enum
from threading import enumerate as threading_enumerate
from typing import Dict

from pyraspi.bus.spidev.linux_spi_spidev import SPI_MODE_3
from pyraspi.raspi import is_kosmos_setup
from pyraspi.raspi import Raspi
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame

if Raspi.is_host_raspberry_pi():
    from pyraspi.bus.spi import BUS
    from pyraspi.bus.spi import SPI
# end if


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
class Link(Enum):
    """
    Enum for naming the two SPI links between RPi and FPGA.
    """
    CONTROL = 0
    DATA = 1
# end class Link


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class FpgaBus(object):
    """
    FPGA bus interface: Abstracts the connection layers between RaspberryPi and FPGA.

    Note: An exception will be raised if the SPI buses are already instantiated.
          That means only one ``FpgaBus`` object can exist at any given time.
          The FPGA interface relies on two SPI buses between the RPi and the FPGA.
    """
    _bus: Dict[Link, SPI]

    def __init__(self):
        self._bus = {}

        self._bus[Link.CONTROL] = self._get_thread_instance(BUS['SPI0'])

        if is_kosmos_setup() and Raspi.is_raspberry_pi_5():
            self._bus[Link.DATA] = self._get_thread_instance(BUS['SPI10'])
        elif is_kosmos_setup():
            self._bus[Link.DATA] = self._get_thread_instance(BUS['SPI4'])
        else:  # Kosmos v1
            self._bus[Link.DATA] = self._get_thread_instance(BUS['SPI6'])
        # end if
    # end def __init__

    @staticmethod
    def _get_thread_instance(spi_bus):
        """
        Return a SPI daemon thread: Look for an existing daemon thread, or create and start one.

        :param spi_bus: SPI bus number, used to identify the SPI thread instance
        :type spi_bus: ``int``

        :return: Return a SPI daemon thread
        :rtype: ``SPI``

        :raise ``AssertionError``: if any of the following condition is met:
                                    - the SPI bus cannot be opened exclusively, when creating a new SPI thread
                                    - a SPI thread already exist but is not alive.
        """
        thread = None

        # Look for existing SPI daemon thread
        active_threads = threading_enumerate()
        for active_thread in active_threads:
            if isinstance(active_thread, SPI) and active_thread.spi_bus == spi_bus:
                thread = active_thread
                assert thread.is_alive(), f'Found SPI thread {thread}, but it is not alive as expected.'
                break
            # end if
        # end for

        if thread is None:
            # Create and start SPI daemon thread
            thread = SPI(bus=spi_bus, mode=SPI_MODE_3, speed=1000000)
            thread.daemon = True
            thread.start()
        # end if
        return thread
    # end def _get_thread_instance

    def send_datagram(self, datagram, link):
        """
        Send a datagram to FPGA and gets reply.

        OSI Layer 4: TRANSPORT (split datagram into packets)

        :param datagram: data to be sent.
        :type datagram: ``MessageFrame`` or ``list[MessageFrame]``
        :param link: SPI bus to be used for the transaction
        :type link: ``Link``

        :return: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :rtype: ``list[tuple[MessageFrame, MessageFrame]]``
        """
        # Split datagram into packets. In this case, a datagram is a packet.
        packet = datagram

        # Convert input to list
        if not isinstance(packet, list):
            packet = [packet]
        # end if

        # Send packet on selected SPI bus.
        return self.send_packet(packet, link)
    # end def send_datagram

    def send_packet(self, packet, link):
        """
        Send packets via the relevant SPI link.

        OSI Layer 3: NETWORK (route packets via relevant SPI interface)

        :param packet: data to be sent.
        :type packet: ``list[MessageFrame]``
        :param link: SPI bus to be used for the transaction
        :type link: ``Link``

        :return: list of TX ``MessageFrame`` coupled with their respective RX ``MessageFrame``
        :rtype: ``list[tuple[MessageFrame, MessageFrame]]``

        :raise ``TypeError``: if packet type is unexpected
        :raise ``IndexError``: if SPI link is not valid
        """
        # Ensure packet is composed of MessageFrames
        if not isinstance(packet, list) or not all(isinstance(p, MessageFrame) for p in packet):
            raise TypeError(packet)
        # end if

        if link not in Link:
            raise IndexError(f"Unknown SPI link: {link}")
        # end if

        # Send packet on selected SPI bus.
        txrx_packet = self._bus[link].send(packet)

        return txrx_packet
    # end def send_packet
# end class FpgaBus

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
