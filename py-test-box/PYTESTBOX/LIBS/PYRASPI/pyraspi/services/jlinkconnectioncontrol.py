#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.jlinkconnectioncontrol
:brief: Jlink connection control class
:author: Fred Chen <fchen7@logitech.com>
:date: 2020/01/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from contextlib import contextmanager
from enum import IntEnum
from enum import auto
from subprocess import PIPE
from subprocess import Popen
from sys import platform
from sys import stdout
from time import sleep

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pytransport.usb.usbhub.smartusbhub import SmartUsbHub
from pytransport.usb.usbhub.usbhubconstants import UsbHubAction

if platform == "linux":
    import RPi.GPIO as GPIO
# end if


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
__version__ = "0.0.0-auto.0"

GENERIC_SUBPROCESS_TIMEOUT = 10
PIN_SWITCHING_TIME = .05
DEBUGGER_SWITCHING_TIME = 15


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class JlinkConnectionControl:
    """
    Control Jlink connection to the DUT
    """

    class State(IntEnum):
        """
        J-Link Connection State
        """
        DISCONNECTED = 0
        CONNECTED = auto()
    # end class State

    @property
    def state(self):
        """
        Get the current Jlink connected/disconnected state

        :return: connected/disconnected state
        :rtype: ``JlinkConnectionControl.State``
        """
        raise NotImplementedAbstractMethodError()
    # end def state

    def connect(self):
        """
        Connect the Jlink to the DUT
        """
        raise NotImplementedAbstractMethodError()
    # end def connect

    def disconnect(self):
        """
        Disconnect the Jlink from the DUT
        """
        raise NotImplementedAbstractMethodError()
    # end def disconnect

    @contextmanager
    def disconnected(self):
        """
        Disconnect the Jlink from the DUT (if necessary) while executing.
        """
        if self.state == JlinkConnectionControl.State.DISCONNECTED:
            yield
        else:
            self.disconnect()
            try:
                yield
            finally:
                self.connect()
            # end try
        # end if
    # end def disconnected

    @contextmanager
    def connected(self):
        """
        Connect the Jlink to the DUT (if necessary) while executing.
        """
        if self.state == JlinkConnectionControl.State.CONNECTED:
            yield
        else:
            self.connect()
            try:
                yield
            finally:
                self.disconnect()
            # end try
        # end if
    # end def connected
# end class JlinkConnectionControl


class PowerSupplyBoardJlinkConnectionControl(JlinkConnectionControl):
    """
    Control Jlink connection to the DUT using a simple GPIO signal on the power supply board V3. The initial ``state``
    is ``JlinkConnectionControl.State.CONNECTED``.

    |

    GPIO level to state:

    * HIGH: connected
    * LOW: disconnected
    """

    def __init__(self, control_pin, verbose=False):
        """
        :param control_pin: Control pin number for board mode GPIO module
        :type control_pin: ``int``
        :param verbose: Enable or disable verbose, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: Invalid platform
        """
        assert platform == "linux", "PowerSupplyBoardJlinkConnectionControl only works for linux environments"
        assert isinstance(control_pin, int), f"Parameter control_pin should be an int, {control_pin} is not"
        assert self.is_control_pin_connected(control_pin=control_pin), \
            "PowerSupplyBoardJlinkConnectionControl needs to have the pin connected to be usable"

        self.verbose = verbose
        self._control_pin = control_pin

        # Initialize the control module and connect the Jlink
        GPIO.setup(self._control_pin, GPIO.OUT, initial=GPIO.HIGH)
        self._state = JlinkConnectionControl.State.CONNECTED

        if self.verbose:
            stdout.write(
                f"JlinkConnectionControl in use: PowerSupplyBoardJlinkConnectionControl on pin {self._control_pin}\n")
        # end if
    # end def __init__

    @property
    def control_pin(self):
        """
        Get the control pin number for board mode GPIO module

        :return: Control pin number for board mode GPIO module
        :rtype: ``int``
        """
        return self._control_pin
    # end def control_pin

    @property
    def state(self):
        # See ``JlinkConnectionControl.state``
        return self._state
    # end def state

    def connect(self):
        # See ``JlinkConnectionControl.connect``
        GPIO.output(self._control_pin, GPIO.HIGH)
        count = 0
        while GPIO.input(self._control_pin) != GPIO.HIGH and count < 10:
            count += 1
            sleep(1e-4)
        # end while
        sleep(PIN_SWITCHING_TIME)
        assert GPIO.input(self._control_pin) == GPIO.HIGH
        self._state = JlinkConnectionControl.State.CONNECTED
        # Add a waiting period to let the debugger switch
        sleep(DEBUGGER_SWITCHING_TIME)
    # end def connect

    def disconnect(self):
        # See ``JlinkConnectionControl.disconnect``
        GPIO.output(self._control_pin, GPIO.LOW)
        count = 0
        while GPIO.input(self._control_pin) != GPIO.LOW and count < 10:
            count += 1
            sleep(1e-4)
        # end while
        sleep(PIN_SWITCHING_TIME)
        assert GPIO.input(self._control_pin) == GPIO.LOW
        self._state = JlinkConnectionControl.State.DISCONNECTED
        # Add a waiting period to let the debugger switch
        sleep(DEBUGGER_SWITCHING_TIME)
    # end def disconnect

    @staticmethod
    def is_control_pin_connected(control_pin):
        """
        Check if the pin is connected. To do that it will put the GPIO module in board mode (and set warnings to
        ``False``).

        :param control_pin: Control pin number for board mode GPIO module
        :type control_pin: ``int``

        :return: Flag indicating if the control pin is connected
        :rtype: ``bool``
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(control_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        return GPIO.input(control_pin) != GPIO.LOW
    # end def is_control_pin_connected
# end class PowerSupplyBoardJlinkConnectionControl


class KosmosJlinkConnectionControl(JlinkConnectionControl):
    """
    Control Jlink connection to the DUT using an I2C GPIO extender. The initial ``state`` is
    ``JlinkConnectionControl.State.CONNECTED``.

    |

    For now, it uses calls of scripts but in the future it should be using kosmos daemon
    """
    KOSMOS_DAEMON_PATH = "/opt/cpg_kosmos_daemon/"
    CONNECT_SCRIPT_COMMAND = ["/usr/local/bin/python", KOSMOS_DAEMON_PATH + "scripts/enable_swd.py"]
    DISCONNECT_SCRIPT_COMMAND = ["/usr/local/bin/python", KOSMOS_DAEMON_PATH + "scripts/disable_swd.py"]

    def __init__(self, verbose=False):
        """
        :param verbose: Enable or disable verbose, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: If this class is instantiated on a platform other than Linux
        """
        assert platform == "linux", "KosmosJlinkConnectionControl only works for linux environments"

        self.verbose = verbose

        # TODO remove state cache and add kosmos daemon call when possible
        self._state = None
        self.connect()

        if self.verbose:
            stdout.write("JlinkConnectionControl in use: KosmosJlinkConnectionControl\n")
        # end if
    # end def __init__

    @property
    def state(self):
        # See ``JlinkConnectionControl.state``
        return self._state
    # end def state

    def connect(self):
        # See ``JlinkConnectionControl.connect``
        process = Popen(self.CONNECT_SCRIPT_COMMAND, stdout=PIPE, stderr=PIPE)
        process.communicate(timeout=GENERIC_SUBPROCESS_TIMEOUT)
        assert process.returncode == 0
        self._state = JlinkConnectionControl.State.CONNECTED
        # Add a waiting period to let the debugger switch
        sleep(DEBUGGER_SWITCHING_TIME)
    # end def connect

    def disconnect(self):
        # See ``JlinkConnectionControl.disconnect``
        process = Popen(self.DISCONNECT_SCRIPT_COMMAND, stdout=PIPE, stderr=PIPE)
        process.communicate(timeout=GENERIC_SUBPROCESS_TIMEOUT)
        assert process.returncode == 0
        self._state = JlinkConnectionControl.State.DISCONNECTED
        # Add a waiting period to let the debugger switch
        sleep(DEBUGGER_SWITCHING_TIME)
    # end def disconnect
# end class KosmosJlinkConnectionControl


class FtdiPoweredDeviceJlinkConnectionControl(JlinkConnectionControl):
    """
    Control Jlink connection for a DUT powered through FTDI, the Jlink control will be done by turning off and on
    the device using the hub to disconnect and connect the FTDI. The initial ``state`` is
    ``JlinkConnectionControl.State.CONNECTED``.
    """
    HUB_STATE_TO_CONNECTION_STATE = {
        UsbHubAction.ON: JlinkConnectionControl.State.CONNECTED,
        UsbHubAction.OFF: JlinkConnectionControl.State.DISCONNECTED,
    }

    def __init__(self, smart_hub, ftdi_hub_port, verbose=False):
        """
        :param smart_hub: Smart hub to use to switch on and off the FTDI port
        :type smart_hub: ``SmartUsbHub``
        :param ftdi_hub_port: Port value on the hub for the FTDI
        :type ftdi_hub_port: ``int``
        :param verbose: Enable or disable verbose, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: If this class is instantiated on a platform other than Linux
        """
        assert platform == "linux", "FtdiPoweredDeviceJlinkConnectionControl only works for linux environments"

        self.verbose = verbose
        self._smart_hub = smart_hub
        self._ftdi_hub_port = ftdi_hub_port

        self._state = FtdiPoweredDeviceJlinkConnectionControl.HUB_STATE_TO_CONNECTION_STATE[
            self._smart_hub.get_usb_ports_status(port_index=self._ftdi_hub_port)]

        if self._state != JlinkConnectionControl.State.CONNECTED:
            self.connect()
        # end if

        if self.verbose:
            stdout.write("JlinkConnectionControl in use: FtdiPoweredDeviceJlinkConnectionControl\n")
        # end if
    # end def __init__

    @property
    def state(self):
        # See ``JlinkConnectionControl.state``
        return self._state
    # end def state

    def connect(self):
        # See ``JlinkConnectionControl.connect``
        self._smart_hub.set_usb_ports_status(port_index=self._ftdi_hub_port, status=UsbHubAction.ON)
        self._state = JlinkConnectionControl.State.CONNECTED
        # Add a waiting period to let the debugger switch
        sleep(DEBUGGER_SWITCHING_TIME)
    # end def connect

    def disconnect(self):
        # See ``JlinkConnectionControl.disconnect``
        self._smart_hub.set_usb_ports_status(port_index=self._ftdi_hub_port, status=UsbHubAction.OFF)
        self._state = JlinkConnectionControl.State.DISCONNECTED
        # Add a waiting period to let the debugger switch
        sleep(DEBUGGER_SWITCHING_TIME)
    # end def disconnect
# end class FtdiPoweredDeviceJlinkConnectionControl


class MockJlinkConnectionControl(JlinkConnectionControl):
    """
    Mock class for JlinkConnectionControl, it is just an internal cached ``state`` changed using the methods
    ``connect`` and ``disconnect``. The initial ``state`` is ``JlinkConnectionControl.State.CONNECTED``.
    """

    def __init__(self, verbose=False):
        """
        :param verbose: Enable or disable verbose, defaults to False - OPTIONAL
        :type verbose: ``bool``
        """
        self.verbose = verbose
        self._state = JlinkConnectionControl.State.CONNECTED

        if self.verbose:
            stdout.write("JlinkConnectionControl in use: MockJlinkConnectionControl\n")
        # end if
    # end def __init__

    @property
    def state(self):
        # See ``JlinkConnectionControl.state``
        return self._state
    # end def state

    def connect(self):
        # See ``JlinkConnectionControl.connect``
        self._state = JlinkConnectionControl.State.CONNECTED
    # end def connect

    def disconnect(self):
        # See ``JlinkConnectionControl.disconnect``
        self._state = JlinkConnectionControl.State.DISCONNECTED
    # end def disconnect
# end class MockJlinkConnectionControl

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
