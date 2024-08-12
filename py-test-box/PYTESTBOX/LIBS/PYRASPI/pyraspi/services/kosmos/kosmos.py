#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.kosmos
:brief: Kosmos implementation Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/02/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from itertools import count
from sys import stdout
from typing import Dict
from typing import List
from typing import Iterable

from pylibrary.emulator.emulatorinterfaces import KosmosInterface
from pyraspi.bus.spi import SpiTransactionError
from pyraspi.bus.spi import SpiTransactionTimeoutError
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.config.podsconfiguration import GET_PODS_CONFIGURATION_BY_KOSMOS_ID
from pyraspi.services.kosmos.config.podsconfiguration import PodsConfiguration
from pyraspi.services.kosmos.fpgatransport import FPGATransport
from pyraspi.services.kosmos.module.adda import AddaModule
from pyraspi.services.kosmos.module.bas import BasModule
from pyraspi.services.kosmos.module.cmods6 import Cmods6Manager
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.devicetree import DeviceTree
from pyraspi.services.kosmos.module.fpga import FpgaModule
from pyraspi.services.kosmos.module.i2cspy import I2cSpyExtendedModule
from pyraspi.services.kosmos.module.kbdgtech import KbdGtechModule
from pyraspi.services.kosmos.module.kbdmatrix import KbdMatrixModule
from pyraspi.services.kosmos.module.ledspy import LedSpyModule
from pyraspi.services.kosmos.module.module import ProducerModuleBaseClass
from pyraspi.services.kosmos.module.optemu_sensors import E7788Module
from pyraspi.services.kosmos.module.optemu_sensors import E7790Module
from pyraspi.services.kosmos.module.optemu_sensors import E7792Module
from pyraspi.services.kosmos.module.optemu_sensors import Paw3266Module
from pyraspi.services.kosmos.module.optemu_sensors import Pmw3816Module
from pyraspi.services.kosmos.module.pes import PesModule
from pyraspi.services.kosmos.module.pescpu import PesCpuModule
from pyraspi.services.kosmos.module.pestimer import PesTimersModule
from pyraspi.services.kosmos.module.pio import PioModule
from pyraspi.services.kosmos.module.sequencer import SequencerModule
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_DYN_BASE
from pyraspi.services.kosmos.version import KosmosVersion

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
FPGA_TARGET_CLOCK_FREQ = 100 * 10**6  # 100 MHz - ideal FPGA / Microblaze clock frequency
FPGA_CURRENT_CLOCK_FREQ = 50 * 10**6  # 50 MHz - Workaround: clock was reduced to achieve FPGA timing constraints.
FPGA_CLOCK_SCALING_FACTOR = FPGA_CURRENT_CLOCK_FREQ / FPGA_TARGET_CLOCK_FREQ
FPGA_CLOCK_PERIOD_NS = 10**9 / FPGA_CURRENT_CLOCK_FREQ


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Kosmos(KosmosInterface):
    """
    Kosmos Test Box discovery, configuration and usage.
    """
    dt: DeviceTree
    version: KosmosVersion
    pods_configuration: PodsConfiguration

    # Private attributes
    _instance: 'Kosmos' = None
    _timeout_error: bool = False
    _capabilities: Dict[DeviceName or DeviceFamilyName, int] = None

    @staticmethod
    def get_instance():
        """
        Get ``Kosmos`` singleton instance.
        Shall not instantiate ``Kosmos`` class by any other way.

        :return: Kosmos instance
        :rtype: ``Kosmos``
        """
        if Kosmos._instance is None:
            Kosmos()
        # end if
        return Kosmos._instance
    # end def get_instance

    def __init__(self):
        """
        :raise ``AssertionError``: multiple source of error:
         - If the Kosmos class was already instantiated (should be used as a singleton)
         - If this class is instantiated without a valid hardware
         - Failure to communicate with Microblaze Core over SPI
        """
        assert Kosmos._instance is None, 'A single Kosmos instance is allowed!'
        assert Daemon.is_host_kosmos(), 'This class can only be instantiated on a RaspberryPi ' \
                                        'prepared for Kosmos project'

        # Set singleton instance reference
        Kosmos._instance = self

        # Open connection to Kosmos Hardware
        fpga_transport = FPGATransport()

        # Init Daemon
        daemon = Daemon()

        # Fetch Kosmos software, firmware and hardware versions
        try:
            self.version = KosmosVersion(fpga_transport=fpga_transport)
        except SpiTransactionError as err:
            raise AssertionError('Fail to communicate with Microblaze Core over SPI.') from err
        # end try

        # Check versions compatibility
        self.version.check()

        # Fetch Kosmos Hardware Configuration
        hwcfg = fpga_transport.hwcfg

        # Initialize Kosmos Device Tree
        msg_id = count(start=MSG_ID_DYN_BASE)
        self.dt = DeviceTree(
            fpga_transport=fpga_transport,

            # --- Core FPGA Modules ---
            fpga=FpgaModule(),
            sequencer=SequencerModule(),
            pes=PesModule(fpga_clock_period_ns=FPGA_CLOCK_PERIOD_NS),
            pes_cpu=PesCpuModule(),
            timers=PesTimersModule(),
            pio=PioModule(),
            adda=AddaModule(),
            cmods6=Cmods6Manager(),

            # --- Optional FPGA Modules ---
            kbd_matrix=KbdMatrixModule(msg_id=next(msg_id)) if hwcfg.kbd_matrix else [],
            kbd_gtech=KbdGtechModule(msg_id=next(msg_id)) if hwcfg.kbd_gtech else [],
            bas=BasModule(msg_id=next(msg_id)) if hwcfg.bas else [],
            led_spy=LedSpyModule(msg_id=next(msg_id)) if hwcfg.led_spy else [],
            i2c_spy=[I2cSpyExtendedModule(fpga_clock_freq_hz=FPGA_CURRENT_CLOCK_FREQ,
                                          instance_id=i, msg_id=next(msg_id))
                     for i in range(hwcfg.i2c_spy)][0] if hwcfg.i2c_spy else [],
            i2c_per=[],         #TODO Not Yet Implemented: refer to hwcfg.i2c_per
            spi_em7770=[],      #TODO Not Yet Implemented: refer to hwcfg.spi_em7770
            spi_e7788=[E7788Module(instance_id=i, msg_id=next(msg_id))
                       for i in range(hwcfg.spi_e7788)][0] if hwcfg.spi_e7788 else [],
            spi_e7790=[E7790Module(instance_id=i, msg_id=next(msg_id))
                       for i in range(hwcfg.spi_e7790)][0] if hwcfg.spi_e7790 else [],
            spi_e7792=[E7792Module(instance_id=i, msg_id=next(msg_id))
                       for i in range(hwcfg.spi_e7792)][0] if hwcfg.spi_e7792 else [],
            spi_paw3266=[Paw3266Module(instance_id=i, msg_id=next(msg_id))
                         for i in range(hwcfg.spi_paw3266)][0] if hwcfg.spi_paw3266 else [],
            spi_pmw3816=[Pmw3816Module(instance_id=i, msg_id=next(msg_id))
                         for i in range(hwcfg.spi_pmw3816)][0] if hwcfg.spi_pmw3816 else [],
            spi_mlx90393=[],    #TODO Not Yet Implemented: refer to hwcfg.spi_mlx90393
        )

        # Compute the list of capabilities supported by the current Kosmos setup.
        self._capabilities = {dev: (len(self.dt[dev.value]) if isinstance(self.dt[dev.value], Iterable)
                                    else int(self.dt[dev.value] is not None))
                              for dev in DeviceName if dev.value in self.dt}

        # Pods channels and voltages initialization
        self.pods_configuration = GET_PODS_CONFIGURATION_BY_KOSMOS_ID[daemon.get_motherboard_inventory_id()]
        self.pods_configuration.init_pods(device_tree=self.dt)
    # end def __init__

    def __getattr__(self, name):
        """
        Retrieve the Kosmos Module instance from the Device Tree.
        This is meant to give a shorthand notation to the developer.

        Note: this will raise an ``AttributeError`` if Module name was not found in Kosmos DeviceTree

        For example, in order to call PES module, instead of writing
            `self.dt.pes` or `[...].kosmos.dt.pes`,
        simply type
            `self.pes`    or `[...].kosmos.pes`,
        as if it was a direct member of the `Kosmos` instance.

        :param name: Module name in the Kosmos DeviceTree
        :type name: ``str``

        :return: Kosmos Module instance
        :rtype: ``DeviceTreeModuleBaseClass``
        """
        return getattr(self.dt, name) if name != 'dt' else None
    # end def __getattr__

    @staticmethod
    def is_connected():
        """
        Flag to tell if an actual board is connected on the CI node

        :return: true if an emulator board is connected, false otherwise
        :rtype: ``bool``
        """
        if not Daemon.is_host_kosmos():
            return False
        # end if
        kosmos = Kosmos.get_instance()
        if kosmos is None:
            return False
        # end if
        if Kosmos._timeout_error:
            return False
        # end if
        try:
            kosmos.dt.fpga.status()
        except SpiTransactionTimeoutError:
            stdout.write(f"Kosmos connection status = timeout error\n")
            Kosmos._timeout_error = True
            return False
        # end try
        return True
    # end def is_connected

    @staticmethod
    def discover_emulator(emulation_type, emulator_min_count=1):
        """
        Check if Kosmos system is available, then check its capabilities.

        The `emulation_type` shall be one from `DeviceName` or from `DeviceFamilyName`. In the latter case, at least
        one `DeviceName` from the family should be present in the Kosmos `DeviceTree` to satisfy the condition.

        If more than one device instance is required, set `emulator_min_count` parameter.

        :param emulation_type: Required Kosmos device type
        :type emulation_type: ``DeviceName or DeviceFamilyName``
        :param emulator_min_count: Minimum count of emulator required; defaults to one - OPTIONAL
        :type emulator_min_count: ``int``

        :return: ``True`` if a Kosmos system is found and has the required capability, ``False`` otherwise
        :rtype: ``bool``
        """
        if not Kosmos.is_connected():
            return False
        # end if
        return Kosmos.has_capability(emulation_type, emulator_min_count)
        # end if
    # end def discover_emulator

    @staticmethod
    def has_capability(emulation_type, emulator_min_count=1):
        """
        Check if a given capability is supported by the current Kosmos setup.

        :param emulation_type: Type of emulation required
        :type emulation_type: ``DeviceName or DeviceFamilyName``
        :param emulator_min_count: Minimum count of emulator required; defaults to one - OPTIONAL
        :type emulator_min_count: ``int``

        :return: true if the current Kosmos setup has the required capability, false otherwise
        :rtype: ``bool``

        :raise ``ValueError``: Invalid `emulator_min_count` value
        :raise ``TypeError``: Invalid `emulation_type` type
        """
        if not isinstance(emulator_min_count, int) or emulator_min_count < 1:
            raise ValueError(emulator_min_count)
        # end if
        kosmos = Kosmos.get_instance()
        if kosmos is None:
            return False
        # end if
        supported_emulation = kosmos.get_capabilities()
        if isinstance(emulation_type, DeviceName):
            return supported_emulation[emulation_type] >= emulator_min_count
        elif isinstance(emulation_type, DeviceFamilyName):
            return any(supported_emulation[dev] >= emulator_min_count for dev in emulation_type)
        else:
            raise TypeError(emulation_type)
        # end if
    # end def has_capability

    @staticmethod
    def get_capabilities():
        """
        Get list of capabilities supported by the current Kosmos setup.

        :return: The list of capabilities supported by the current Kosmos setup
        :rtype: ``Dict[DeviceName or DeviceFamilyName, int]``
        """
        kosmos = Kosmos.get_instance()
        return kosmos._capabilities
    # end def get_capabilities

    @staticmethod
    def is_fake():
        # See ``KosmosInterface.is_fake``
        return False
    # end def is_fake

    def get_status(self):
        # See ``KosmosInterface.get_status``
        return self.dt.fpga.status()
    # end def get_status

    def clear(self, force=False):
        # See ``KosmosInterface.clear``

        # Clear remote FIFO & buffers of Modules producing data (TIMERS, LED_SPY, I2C_SPY ...)
        for module in self.dt.flatmap.values():
            if isinstance(module, (PesTimersModule, ProducerModuleBaseClass)):
                module.reset_module()
            # end if
        # end for

        # Clear remote FIFO & buffers of Modules consuming instructions (PES, KBD, BAS, PES_CPU ...)
        if force:
            self.dt.sequencer.reset_module()
        else:
            self.dt.sequencer.reset_sequence()
        # end if

        # Clear local buffers of Modules consuming instructions (PES, KBD, BAS, PES_CPU ...)
        self.dt.sequencer.clear_buffer()
    # end def clear
# end class Kosmos
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
