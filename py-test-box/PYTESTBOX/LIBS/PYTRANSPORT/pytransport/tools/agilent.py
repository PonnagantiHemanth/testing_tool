#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.tools.agilent
:brief: Agilent Power Supply Control Class.
        System Setup Reference: https://spaces.logitech.com/display/ptb/Agilent
:author: Fred Chen <fchen7@logitech.com>
:date: 2019/6/27
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import serial
import serial.tools.list_ports
from threading import RLock

from pylibrary.tools.threadutils import synchronized


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
AGILENT_VID = 0x0957
AGILENT_LOCK = RLock()


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Agilent(object):
    """
    Agilent Power Supply Control Class
    """

    _instance = None

    @staticmethod
    @synchronized(AGILENT_LOCK)
    def get_instance():
        """
        Static method to get this class singleton instance of Agilent Power Supply controller

        :return: The singleton instance of Agilent Power Supply controller
        :rtype: ``Agilent`` or ``None``
        """
        if Agilent._instance is None:
            port = None

            for p in serial.tools.list_ports.comports():
                if p.vid == AGILENT_VID:
                    port = p.device
                    break
                # end if
            # end for

            if port is None:
                return None
            # end if

            Agilent(port)
        # end if

        return Agilent._instance
    # end def get_instance

    def __init__(self, port):
        """
        :param port: Serial port to use
        :type port: ``str``
        """
        assert Agilent._instance is None, 'Allowed one Agilent instance only!'
        # noinspection PyBroadException
        try:
            self.serial = serial.Serial(
                port, 9600, rtscts=0, parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
            Agilent._instance = self
        except Exception:
            Agilent._instance = None
        # end try
    # end def __init__

    def __del__(self):
        """
        Destructor
        """
        if Agilent._instance is not None:
            self.serial.close()
        # end if
    # end def __del__

    def read_id(self):
        """
        Read the model name

        :return: The model name
        :rtype: ``bytes`` or ``None``
        """
        self.serial.write(b'*idn?\r\n')
        idn = self.serial.readline().rstrip(b'\r\n')
        if idn == b'':
            return None
        else:
            return idn
        # end if
    # end def read_id

    def read_version(self):
        """
        Read the version number

        :return: The version number
        :rtype: ``bytes`` or ``None``
        """
        self.serial.write(b'syst:vers?\r\n')
        version = self.serial.readline().rstrip(b'\r\n')
        if version == b'':
            return None
        else:
            return version
        # end if
    # end def read_version

    def clear_status(self):
        """
        Clear abnormal status
        """
        self.serial.write(b'*CLS\r\n')
    # end def clear_status

    def get_max_current(self):
        """
        Get the max current support

        :return: The max current, None means fail to get it
        :rtype: ``float`` or ``None``
        """
        self.serial.write(b'SENS:CURR:RANGE?\r\n')
        max_curr = self.serial.readline().rstrip(b'\r\n')
        if max_curr == b'':
            return None
        else:
            return float(max_curr)
        # end if
    # end def get_max_current

    @synchronized(AGILENT_LOCK)
    def output_voltage(self, on_off):
        """
        On/Off output voltage

        :param on_off: 'on' or 'off'
        :type on_off: ``str``
        """
        assert on_off == 'on' or on_off == 'off', 'the possible value of on_off are \'on\' or \'off\' string!'
        self.serial.write(Agilent._create_payload('outp', on_off))
    # end def output_voltage

    @synchronized(AGILENT_LOCK)
    def set_voltage(self, volt):
        """
        Set voltage

        :param volt: Voltage value in Volt
        :type volt: ``float``

        :return: New output voltage value in Volt, None means fail to get it
        :rtype: ``float``
        """
        self.serial.write(Agilent._create_payload('volt', volt))
        return self.read_voltage()
    # end def set_voltage

    def read_voltage(self):
        """
        Read voltage

        :return: Output voltage value in Volt, None means fail to get it
        :rtype: ``float`` or ``None``
        """
        self.serial.write(b'volt?\r\n')
        v = self.serial.readline()
        if v == b'':
            return None
        else:
            return float(v)
        # end if
    # end def read_voltage

    def set_current(self, curr):
        """
        Set current

        :param curr: Current value in amper
        :type curr: ``float``

        :return: New output current value in amper, None means fail to get it
        :rtype: ``float`` or ``None``
        """
        self.serial.write(Agilent._create_payload('curr', curr))
        return self.read_current()
    # end def set_current

    def read_current(self):
        """
        Read current value

        :return: Output current value in amper, None means fail to get it
        :rtype: ``float`` or ``None``
        """
        self.serial.write(b'meas:curr?\r\n')
        a = self.serial.readline()
        if a == b'':
            return None
        else:
            return float(a)
        # end if
    # end def read_current

    @staticmethod
    def _create_payload(cmd, data):
        """
        Create payload by parameters

        :param cmd: Command name
        :type cmd: ``str``
        :param data: Parameters for the command
        :type data: ``str`` or ``float``

        :return: Command payload
        :rtype: ``bytearray``
        """
        cmd = '{0} {1}\r\n'.format(cmd, data)
        payload = bytearray()
        payload.extend(map(ord, cmd))
        return payload
    # end def _create_payload

    @staticmethod
    def discover_agilent():
        """
        Has a quick availability check for Agilent Power Supply.

        :return: Flag indicating if Agilent is present
        :rtype: ``bool``
        """
        agilent = Agilent.get_instance()
        if agilent is None:
            return False
        else:
            if agilent.read_id() is None:
                return False
            else:
                return True
            # end if
        # end if
    # end def discover_agilent
# end class Agilent

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
