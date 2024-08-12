#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.daemon
:brief: Kosmos Daemon Class
        cf Kosmos RPi Daemon Specs in
        https://docs.google.com/document/d/15xh6XPZHOIvJJCx44n7HuSDXESJWvU2QD7VV5bG3law/view
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/09/21
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from kosmos_daemon.kosmosmodules import KosmosModule
from kosmos_daemon.public.hardware import Hardware
from kosmos_daemon.public.hardware import Modules
from kosmos_daemon.utils.utils import HW_KOSMOSV2
from kosmos_daemon.utils.utils import HW_RPI
from os import getloadavg
from pkg_resources import require

from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pyraspi.services.kosmos.gitversion import VersionTag
from pyraspi.services.kosmos.version import KosmosVersion

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()

# Configure Daemon traces verbosity
#  - None: disable all traces (Default)
#  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
#  - TraceLevel.INFO: Info level will be used for minimal information
#  - TraceLevel.DEBUG: Debug level will be for maximum information
FORCE_AT_CREATION_ALL_DAEMON_TRACE_LEVEL = TraceLevel.INFO
FORCE_AT_CREATION_ALL_DAEMON_TRACE_FILE_NAME = None

SETUP_TYPE_STR = {
    HW_KOSMOSV2: 'Kosmos HW detected',
    HW_RPI: 'Standard test setup (no Kosmos HW)',
}

# First Kosmos Daemon version to expose a public API
EXPECTED_DAEMON_VERSION = VersionTag(major=0, minor=2, patch=5)


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Daemon:
    """
    Define some methods to interact with the Kosmos Daemon Public API.
    """
    _is_host_kosmos = None

    def __init__(self, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        """
        :param trace_level: Trace level of the hub - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the hub - OPTIONAL
        :type trace_file_name: ``str``

        :raise ``ValueError``: Kosmos daemon version is not up-to-date
        """
        if FORCE_AT_CREATION_ALL_DAEMON_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_DAEMON_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_DAEMON_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_DAEMON_TRACE_FILE_NAME
        # end if

        TRACE_LOGGER.subscribe(subscription_owner=self,
                               trace_level=trace_level,
                               trace_file_name=trace_file_name,
                               trace_name=f'Kosmos Daemon')

        version = require("kosmos_daemon")[0].version
        self.daemon_version = VersionTag(major=int(version.split('.')[0]), minor=int(version.split('.')[1]),
                                         patch=int(version.split('.')[2]))

        if KosmosVersion.test_tag_versions(expected=EXPECTED_DAEMON_VERSION, actual=self.daemon_version):
            # Create a handle on the Kosmos Daemon public interface
            self.kosmos_hardware = Hardware()
        else:
            raise ValueError('\tKosmos daemon version is not up-to-date. You shall consider updating your SD card.\n'
                             f'\tExpected: {EXPECTED_DAEMON_VERSION}\n\tActual: {version}')
        # end if
        self.motherboard = None
        self.pods_module = None
        self.power_emulator_left = None
        self.power_emulator_right = None
    # end def __init__

    @staticmethod
    def is_host_kosmos():
        """
        Retrieve the CI setup type and check if it's a Kosmos deployment.

        :return: ``True`` if the host is a RaspberryPi configured for KOSMOS project
        :rtype: ``bool``

        :raise ``ValueError``: The daemon was not able to find a suitable setup type
        """
        # Returned cached value if present
        if Daemon._is_host_kosmos is not None:
            return Daemon._is_host_kosmos
        # end if

        kosmos_hardware = Hardware()
        setup_type = kosmos_hardware.setup_type
        if kosmos_hardware.setup_type not in [HW_KOSMOSV2, HW_RPI]:
            raise ValueError(f'The daemon was not able to find a suitable setup type ({setup_type} found)')
        # end if
        Daemon._is_host_kosmos = (kosmos_hardware.setup_type == HW_KOSMOSV2)
        return Daemon._is_host_kosmos
    # end def is_host_kosmos

    def log_kosmos_setup_info(self):
        """
        Log information related to a Kosmos system.
        """
        if self.kosmos_hardware is not None:
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f'\tTest setup type: {SETUP_TYPE_STR[self.kosmos_hardware.setup_type]}',
                                   trace_level=TraceLevel.INFO)
            if hasattr(self.kosmos_hardware, 'rpi_model'):
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f'\tRaspberry Pi {self.kosmos_hardware.rpi_model} Model B '
                                               f'Rev {self.kosmos_hardware.rpi_revision}',
                                       trace_level=TraceLevel.INFO)
            # end if
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f"\tAverage CPU Load (last 5 min): {getloadavg()[1]:.2f}",
                                   trace_level=TraceLevel.INFO)
            try:
                # Keep the local import while a new PI OS image with this package was not published
                from gpiozero import CPUTemperature
                cpu = CPUTemperature()
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f'\tCPU Temperature: {cpu.temperature}°C', trace_level=TraceLevel.INFO)
            except ImportError as e:
                # module doesn't exist, deal with it.
                pass
            # end try
            self.motherboard = Modules(KosmosModule.MOTHERBOARD)
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f'\tMOTHERBOARD hardware rev{self.motherboard.hardware_revision} ; '
                                           f'KOSMOS{self.motherboard.inventory_id} ; '
                                           f'UUID={hex(self.motherboard.module_uuid)}',
                                   trace_level=TraceLevel.INFO)
            has_pods = self.kosmos_hardware.has_pods
            if has_pods:
                self.pods_module = Modules(KosmosModule.PODS)
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f'\tPODS hardware rev{self.pods_module.hardware_revision} ; '
                                               f'inventory id={self.pods_module.inventory_id} ; '
                                               f'UUID={hex(self.pods_module.module_uuid)}',
                                       trace_level=TraceLevel.INFO)
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f'\tGDB hardware rev{str(self.pods_module.gdb_version)[:1]}.'
                                               f'{str(self.pods_module.gdb_version)[1:]} ; '
                                               f'inventory id={self.pods_module.gdb_inventory_id}',
                                       trace_level=TraceLevel.INFO)
            else:
                TRACE_LOGGER.log_trace(subscription_owner=self, message=f'\tNo PODS detected',
                                       trace_level=TraceLevel.INFO)
            # end if
            has_power_emulator_left = self.kosmos_hardware.has_power_emulator_left
            has_power_emulator_right = self.kosmos_hardware.has_power_emulator_right
            if has_power_emulator_left:
                self.power_emulator_left = Modules(KosmosModule.POWER_EMULATOR_LEFT)
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message='\tPOWER BOARD (Left side) hardware revision ='
                                               f' {self.power_emulator_left.hardware_revision} ; '
                                               f'inventory id={self.power_emulator_left.inventory_id} ; '
                                               f'UUID=0x{self.power_emulator_left.module_uuid}',
                                       trace_level=TraceLevel.INFO)
            # end if
            if has_power_emulator_right:
                self.power_emulator_right = Modules(KosmosModule.POWER_EMULATOR_RIGHT)
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message='\tPOWER BOARD (Right side) hardware revision ='
                                               f' {self.power_emulator_right.hardware_revision} ; '
                                               f'inventory id={self.power_emulator_right.inventory_id} ; '
                                               f'UUID=0x{self.power_emulator_right.module_uuid}',
                                       trace_level=TraceLevel.INFO)
            # end if
            if not has_power_emulator_left and not has_power_emulator_right:
                TRACE_LOGGER.log_trace(subscription_owner=self, message=f'\tNo POWER BOARD detected',
                                       trace_level=TraceLevel.INFO)
            # end if
            if self.kosmos_hardware.vl805_fw_version != 'not available':
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f'\tUSB driver vl805 version: 0x{self.kosmos_hardware.vl805_fw_version}',
                                       trace_level=TraceLevel.INFO)
            # end if
        # end if
    # end def log_kosmos_setup_info

    def log_standard_setup_info(self):
        """
        Log information related to a standard deployment based on a PI and a power supply board.
        """
        if self.kosmos_hardware is not None:
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f'\tTest setup type: {SETUP_TYPE_STR[self.kosmos_hardware.setup_type]}',
                                   trace_level=TraceLevel.INFO)
            if self.kosmos_hardware.has_power_supply_v3:
                TRACE_LOGGER.log_trace(subscription_owner=self, message=f'\tPOWER SUPPLY detected',
                                       trace_level=TraceLevel.INFO)
            # end if
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f'\tUSB driver vl805 version: 0x{self.kosmos_hardware.vl805_fw_version}',
                                   trace_level=TraceLevel.INFO)
        # end if
    # end def log_standard_setup_info

    def get_motherboard_inventory_id(self):
        """
        Retrieve the motherboard inventory ID of a Kosmos deployment.

        :return: Motherboard inventory ID if the host is a RaspberryPi configured for KOSMOS project otherwise``None``
        :rtype: ``int`` or ``None``
        """
        inventory_id = None
        if self.kosmos_hardware is not None:
            self.motherboard = Modules(KosmosModule.MOTHERBOARD)
            inventory_id = self.motherboard.inventory_id
        # end if
        return inventory_id
    # end def get_motherboard_inventory_id
# end class Daemon

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
