#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.usb.usbhub.smartusbhub
:brief: Smart USB HUB classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import re
import subprocess
from importlib import util
from os import path
from platform import machine
from sys import modules
from time import time

from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pyraspi.raspi import Raspi
from pytransport.usb.usbhub.usbhubconstants import UsbHubAction

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()

# Configure Smart USB Hub traces verbosity
#  - None: disable all traces (Default)
#  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
#  - TraceLevel.INFO: Info level will be used for minimal information at the end of a method
#  - TraceLevel.DEBUG: Debug level will be for maximum information
FORCE_AT_CREATION_ALL_USB_HUB_TRACE_LEVEL = None
FORCE_AT_CREATION_ALL_USB_HUB_TRACE_FILE_NAME = None

SD_CARD_VERSION_MODULE_NAME = 'version'
SD_CARD_VERSION_FILE = "/home/pi/version.py"


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SmartUsbHub:
    """
    This is the definition of the common implementation of a smart USB hub.
    """

    def __init__(self, hub_id, port_count, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        """
        :param hub_id: The hub identifier, can be found using ``get_smart_usb_hub_location``
        :type hub_id: ``str``
        :param port_count: The number of port on the hub
        :type port_count: ``int``
        :param trace_level: Trace level of the hub - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the hub - OPTIONAL
        :type trace_file_name: ``str``
        """
        if FORCE_AT_CREATION_ALL_USB_HUB_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_USB_HUB_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_USB_HUB_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_USB_HUB_TRACE_FILE_NAME
        # end if

        TRACE_LOGGER.subscribe(subscription_owner=self,
                               trace_level=trace_level,
                               trace_file_name=trace_file_name,
                               trace_name=f'SmartUsbHub {hub_id}')

        self.port_count = port_count
        self.hub_id = hub_id
    # end def __init__

    @staticmethod
    def get_sd_card_version():
        """
        Retrieve the current sd card version
        Importing style is working for python 3.5+ as per:
        https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly

        :return: List containing the date fields + version as follow: [year,month,day,version]
        :rtype: ``list[str]``
        """
        # Method 1, the new version.py is available and VERSION constant is also there
        spec = util.spec_from_file_location(SD_CARD_VERSION_MODULE_NAME, SD_CARD_VERSION_FILE)
        try:
            version = util.module_from_spec(spec)
            modules[SD_CARD_VERSION_MODULE_NAME] = version
            spec.loader.exec_module(version)
            return version.SD_CARD_VERSION.split('.')
        except AttributeError:
            # Method 2, old version.py file, have to parse the docstring to find the version
            with open(SD_CARD_VERSION_FILE, 'r', encoding='utf-8') as sd_card_version_file:
                for line in sd_card_version_file.readlines():
                    # Remove \n
                    words = line[:-1].split(' ')
                    if '@version' in words:
                        return words[1].split('.')
                    # end if
                # end for
            # end with
        # end try
    # end def get_sd_card_version

    @staticmethod
    def get_smart_usb_hub_location():
        """
        Retrieve plugged smart USB hubs identifiers.

        :return: List of the found USB hubs identifier
        :rtype: ``list[str]``
        """
        process = subprocess.run(["/usr/local/bin/uhubctl"], capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"UHUBCTL subprocess failed: {process.stderr}"
        hub_id_list = []
        if Raspi.is_raspberry_pi_5():
            # Current status for hub 3-2 [1a40:0201 USB 2.0 Hub [MTT], USB 2.00, 7 ports, ppps]
            hub_id_extractor = re.compile(r'Current status for hub ([0-9-]{3,5}) [(\s\S)*]')
        else:
            # Current status for hub 1-1.1 [1a40:0201 USB 2.0 Hub [MTT], USB 2.00, 7 ports, ppps]
            hub_id_extractor = re.compile(r'Current status for hub ([0-9-.]{5,7}) [(\s\S)*]')
        # end if
        for line in process.stdout.split('\n'):
            hub_id_matching = hub_id_extractor.search(line)
            if hub_id_matching:
                # save entry in hub identifier list
                hub_id_list.append(hub_id_matching.group(1))
                break
            # end if
        # end for
        return hub_id_list
    # end def get_smart_usb_hub_location

    def get_usb_ports_status(self, port_index):
        """
        Get the usb port enable/disable status on the hub.

        :param port_index: Port index on the hub, between 1 and the maximum number of port (0 is not valid)
        :type port_index: ``int``

        :return: The Usb HUB action which has been completed
        :rtype: ``UsbHubAction``

        :raise ``AssertionError``: If the port number is out of range or if the targeted port has not been found or if
                                   the child process does not terminate with an exit status of 0
        """
        assert 0 < port_index <= self.port_count, f"Port index ({port_index}) out of range [1 .. {self.port_count}]"

        TRACE_LOGGER.log_trace(subscription_owner=self,
                               message=f"Starting get_usb_ports_status for port {port_index}...",
                               trace_level=TraceLevel.DEBUG)

        start_time = time()
        completed_process = subprocess.run(["/usr/local/bin/uhubctl", "-l", f'{self.hub_id}', "-p", f'{port_index}'],
                                           capture_output=True, universal_newlines=True)
        assert completed_process.returncode == 0, f"UHUBCTL subprocess failed: {completed_process.stderr}"

        stdout_print = "\t" + "\n\t".join([line for line in completed_process.stdout.splitlines()])
        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Run stdout:\n{stdout_print}", trace_level=TraceLevel.DEBUG)

        for line in completed_process.stdout.splitlines():
            line = line.lstrip()
            s = line.split(': ')
            if len(s) > 1 and s[0].startswith('Port') and int(s[0].split(' ')[1]) == port_index:
                status = UsbHubAction.OFF if s[1].split(' ')[1] == 'off' else UsbHubAction.ON

                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f"get_usb_ports_status for port {port_index}, "
                                               f"status = {status.value}, duration = {time()-start_time}s",
                                       trace_level=TraceLevel.INFO)
                return status
            # end if
        # end for

        assert False, f"Did not find the port {port_index}"
    # end def get_usb_ports_status

    def set_usb_ports_status(self, port_index, status):
        """
        Enable/disable the usb port on the hub.

        :param port_index: Port index on the hub
        :type port_index: ``int``
        :param status: Status of the port
        :type status: ``UsbHubAction``

        :raise ``AssertionError``: If the port number is out of range or if the targeted port has not been found or if
                                   the child process does not terminate with an exit status of 0
        """
        assert 0 < port_index <= self.port_count, f"Port index ({port_index}) out of range [1 .. {self.port_count}]"
        assert isinstance(status, UsbHubAction), f"status type {type(status)} is invalid should be UsbHubAction"

        TRACE_LOGGER.log_trace(subscription_owner=self,
                               message=f"Starting set_usb_ports_status for port {port_index} to {status.value}...",
                               trace_level=TraceLevel.DEBUG)

        start_time = time()
        command_string = ["/usr/local/bin/uhubctl", "-a", status.value, "-l", f'{self.hub_id}', "-p", f'{port_index}']

        if machine() == 'armv7l' and status == UsbHubAction.OFF:
            # Workaround necessary for linux older than 6.0, see:
            # https://github.com/mvp/uhubctl/blob/master/README.md#power-comes-back-on-after-few-seconds-on-linux
            command_string.append("-r")
            command_string.append("100")

            file_path = f"/sys/bus/usb/devices/{self.hub_id}.{port_index}/authorized"

            if path.exists(file_path):
                completed_process = subprocess.run(
                    ["echo", "0", ">", "tee", file_path], capture_output=True, universal_newlines=True)
                assert completed_process.returncode == 0, \
                    f"UHUBCTL first OFF workaround subprocess failed: {completed_process.stderr}"
            # end if
        # end if

        completed_process = subprocess.run(command_string, capture_output=True, universal_newlines=True)
        assert completed_process.returncode == 0, f"UHUBCTL subprocess failed: {completed_process.stderr}"

        directory_path = f"/sys/bus/usb/devices/{self.hub_id}.{port_index}/"
        if machine() == 'armv7l' and status == UsbHubAction.OFF and path.exists(directory_path):
            completed_process = subprocess.run(
                ["sudo", "udevadm", "trigger", "--action=remove", directory_path], capture_output=True, universal_newlines=True)
            assert completed_process.returncode == 0, \
                f"UHUBCTL second OFF workaround subprocess failed: {completed_process.stderr}"
        # end if

        stdout_print = "\t" + "\n\t".join([line for line in completed_process.stdout.splitlines()])
        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Run stdout:\n{stdout_print}", trace_level=TraceLevel.DEBUG)

        TRACE_LOGGER.log_trace(subscription_owner=self,
                               message=f"set_usb_ports_status for port {port_index}, "
                                       f"status = {status.value}, duration = {time()-start_time}s",
                               trace_level=TraceLevel.INFO)
    # end def set_usb_ports_status
# end class SmartUsbHub

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
