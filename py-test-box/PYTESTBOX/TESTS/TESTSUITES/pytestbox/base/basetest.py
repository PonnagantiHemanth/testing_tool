#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.base.basetest
:brief: pytestbox Base test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2014/11/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
# Configure the logging as early as possible, to catch log messages generated
# by the code generation.
# Next import force the initialization of the global logger
# noinspection PyUnresolvedReferences
import sys
import warnings
from contextlib import contextmanager
from os.path import exists
from os.path import join
from queue import Empty
from sys import stdout
from time import sleep
from time import time

from pychannel.blechannel import BleChannel
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.channelinterfaceclasses import LogitechReportType
from pychannel.throughreceiverchannel import ThroughBleProReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyharness.context import ContextLoader
from pyharness.core import TYPE_ERROR
from pyharness.core import TestException
from pyharness.debugger import DebuggerTestCase
from pyharness.debugger import DebuggerTestCaseMixin
from pyharness.device import DeviceTestCase
from pyharness.extensions import WarningLevel
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.hidmouse import HidMouse
from pyhid.hiddata import HidData
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hiddispatcher import HidMessageQueue
from pyhid.hidpp.features.batteryunifiedlevelstatus import BatteryLevelStatusBroadcastEvent
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryFactory
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidpp1.notifications.deviceconnection import BLEProReceiverInformation
from pyhid.hidpp.hidpp1.notifications.deviceconnection import BluetoothOrQuadReceiverInformation
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.deviceconnection import EQuadReceiverInformation
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import ReceiverFwInfo
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.vlp.features.important.vlproot import VLPRoot
from pylibrary.mcu.memorymanagerfactory import MemoryManagerFactory
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import StoppableThread
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.bus.spi import SpiTransactionError
from pyraspi.services.kosmos.ambientlightsensoremulator import AmbientLightSensorEmulator
from pyraspi.services.kosmos.dualkeymatrixemulator import KosmosDualKeyMatrixEmulator
from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulator
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.kosmosi2cspy import KosmosLedSpyOverI2c
from pyraspi.services.kosmos.module.error import KosmosFatalError
from pyraspi.services.kosmos.motionemulator import KosmosMotionEmulator
from pyraspi.services.kosmos.powerslideremulator import KosmosPowerSliderEmulator
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RESET_DONE
from pyraspi.services.kosmos.proximitysensoremulator import ProximitySensorEmulator
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.emulatorsmanager import EmulatorsManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
# Next line force the initialization of the global device features & services decorator
# noinspection PyUnresolvedReferences
from pytestbox.base.registration import features
from pytestbox.base.serial_logger import print_serial_debug
# Next line force the initialization of the global bugtracker decorator
# noinspection PyUnresolvedReferences
from pytestbox.bugtracking.bugtracker import set_expected_failure
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils
# Next line force the initialization of the global device features & services decorator
# noinspection PyUnresolvedReferences
from pytestbox.receiver.base.registration import features
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pytestbox.shared.base.registration import features
from pyusb.libusbdriver import ChannelIdentifier
from pyusb.libusbdriver import LibusbDriver

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
# TODO Those are for statistics, they are to be removed after some time but for now should stay. That is why it was put
#  them in a different verbosity constant. If we want to keep them in the future, LogHelper.log_info would be a
#  good solution. For now we want them to appear on the console
PRINT_TEST_TIMINGS = False
# Temporarily set to True to evaluate impact on all targets (Hadron DEV board, Bazooka2, ...)
PRINT_MOTION_EMULATOR_SETUP_TIMING = True
MOTION_EMULATOR_SETUP_THRESHOLD = .02  # print when timing is above 20ms


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CommonBaseTestCase(DebuggerTestCase, DeviceTestCase):
    """
    Common TestCase class for both receiver and device targets.
    """
    _PREDICATE_CACHE = dict()
    MAX_RESET_TRY = 4

    # The naming of methodName is inherited from PyHarnessCase
    # noinspection PyPep8Naming
    def __init__(self, methodName='runTest'):
        """
        :param methodName: Name of the method to launch - OPTIONAL
        :type methodName: ``str``
        """
        DeviceTestCase.__init__(self, methodName=methodName)

        # Device Under Test (DUT) handle
        self.led_timeline = None
        self.device = None
        self.original_device_index = None
        # Emulator device
        self.emulator_device = None
        # Emulator handle for power supply
        self.power_supply_emulator = None
        # Emulator handle for main wheel
        self.main_wheel_emulator = None
        # J-Link IO switch control
        self.jlink_connection_control = None
        # Ratchet spy
        self.ratchet_spy = None
        # LED spy
        self.led_spy = None

        self.elf_symbol_file_path = ''

        # ------------------- Debuggers -------------------
        # The read only properties debugger and memory_manager can be used when the debugger for the DUT is to be
        # used (regardless of if it is a device or a receiver)
        # Debugger & Memory Manager linked to a device in the ecosystem
        self.device_debugger = None
        self.device_memory_manager = None
        # Debugger & Memory Manager linked to a receiver in the ecosystem
        self.receiver_debugger = None
        self.receiver_memory_manager = None
        # Debugger & Memory Manager linked to a receiver companion MCU in the ecosystem
        self.receiver_companion_debugger = None
        self.receiver_companion_memory_manager = None
        # Debugger & Memory Manager linked to a device companion MCU in the ecosystem
        self.device_companion_debugger = None
        self.device_companion_memory_manager = None

        self.last_ble_address = None
        self.post_requisite_reload_nvs = False

        self.device_ids = None
        self.backup_dut_channel = None
        self.backup_through_receiver_channel = None
        self.current_channel = None
        self._start_time = None
        self._serial_thread = None

        # Call static function to force class constant initialization (ex. MAX_USB_PORT_COUNT)
        LibusbDriver.discover_usb_hub()

        # This attribute controls the maximum length of diffs output by assert methods that report diffs on failure.
        # cf https://docs.python.org/3/library/unittest.html#unittest.TestCase.maxDiff
        # self.maxDiff = 1024

        # Kosmos-related post requisite
        self._kosmos_post_requisite_done = False
    # end def __init__

    def setUp(self):
        """
        Initialise the test.
        """
        self.warning_occurred = False

        # Inherited setup
        super().setUp()

        self.f = self.getFeatures()

        # Device setup
        DeviceTestCase.setUp(self)

        # Configuration Manager
        self.config_manager = ConfigurationManager(self.f)

        # Power supply emulation setup including optional calibration
        self.initialize_emulators()

        # Reset LogHelper counters.
        LogHelper.reset()
        # Reset ``KeyExpectedActions`` variables
        KeyMatrixTestUtils.KeyExpectedActions.reset()

        # Configure HID report types and HID Guidelines version
        HidData.configure(version=self.f.PRODUCT.HID_REPORT.F_HidGuidelinesVersion,
                          is_gaming=self.f.PRODUCT.F_IsGaming,
                          mouse_report_type=self.f.PRODUCT.HID_REPORT.F_HidMouseType,
                          keyboard_report_type=self.f.PRODUCT.HID_REPORT.F_HidKeyboardType,
                          options=self.f.PRODUCT.HID_REPORT.F_HidOptions)

        if self.power_supply_emulator is not None and self.power_supply_emulator.is_off():
            # Turn on the device battery with the default voltage value
            self.power_supply_emulator.turn_on()
        # end if

        if self.game_mode_emulator is not None:
            # disable the game mode
            self.game_mode_emulator.set_mode()
        # end if

        if self.power_slider_emulator is not None:
            # Turn the power slider on
            self.power_slider_emulator.power_on()
            # add 50ms delay to let the DUT boot
            sleep(.05)
        # end if

        if self.f.LOGGING.F_SerialLoggingEnabled and self.f.LOGGING.F_SerialSource is not None:

            if exists(self.f.LOGGING.F_SerialSource):
                self._serial_thread = StoppableThread(print_serial_debug,
                                                      source=self.f.LOGGING.F_SerialSource,
                                                      logger=self.getLogger())
                self._serial_thread.start()
            else:
                stdout.write(f"{self.f.LOGGING.F_SerialSource} does not exist")
            # end if
        # end if

        # Kosmos-related post requisite
        self._kosmos_post_requisite_done = False
    # end def setUp

    def tearDown(self):
        """
        Destroy the test.
        """

        with self.manage_post_requisite():
            if self._serial_thread is not None:
                self._serial_thread.stop()
            # end if
        # end with

        with self.manage_kosmos_post_requisite():
            if self.button_stimuli_emulator is not None:
                self.button_stimuli_emulator.release_all()
                if self.current_channel is not None and self.current_channel.is_open:
                    # Empty hid_message_queue
                    ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end if
            # end if
        # end with

        with self.manage_kosmos_post_requisite():
            if self.motion_emulator is not None:
                # Reset local Python cache and FPGA module cache
                self.motion_emulator.reset()
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_channel is not None and self.current_channel.is_open:
                if self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_Enabled:
                    feature_1004 = UnifiedBatteryFactory.create(
                        self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY))
                    low_warning_classes = (WirelessDeviceStatusBroadcastEvent, feature_1004.battery_status_event_cls)
                else:
                    low_warning_classes = (WirelessDeviceStatusBroadcastEvent,)
                # end if
                # Check queues are empty
                for queue in self.current_channel.hid_dispatcher.queue_list:
                    if queue.name != HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT:
                        while not ChannelUtils.warn_queue_not_empty(
                                test_case=self, queue_name=queue.name, low_warning_classes=low_warning_classes):
                            pass
                        # end while
                    else:
                        # Exclude connection event queue from global queue monitoring
                        ChannelUtils.empty_queue(test_case=self, queue_name=queue.name)
                    # end if
                # end for
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_channel is not None:
                self.current_channel.hid_dispatcher.clear_feature_entries()
                ChannelUtils.close_channel(test_case=self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.device is not None:
                for channel in self.device.get_all_cached_channels_in_list():
                    channel.hid_dispatcher.clear_feature_entries()

                    if channel.hid_dispatcher.receiver_event_queue.is_message_type_accepted(DeviceConnection):
                        # The device connection notification should not be in the receiver event queue but in some
                        # instance can be added in the middle of a test. This is a protection to avoid having it in
                        # the next test
                        channel.hid_dispatcher.receiver_event_queue.update_accepted_messages(
                            Hidpp1Model.get_available_events_classes())
                    # end if

                    if channel.is_open:
                        ChannelUtils.close_channel(test_case=self, channel=channel)
                    # end if
                # end for

                if isinstance(self.backup_dut_channel, ThroughReceiverChannel):
                    # Add the backup channel back to the cache (add_channel_to_cache() does nothing if the channel is
                    # already in the cache)
                    DeviceManagerUtils.add_channel_to_cache(test_case=self, channel=self.backup_dut_channel)
                # end if

                self.device.remove_all_channel_through_gotthard_from_cache()
            # end if
        # end with

        DebuggerTestCaseMixin.tearDown(self)
        DeviceTestCase.tearDown(self)
    # end def tearDown

    def debuggers_setup(self):
        """
        Set up the debuggers for the test.

        Debuggers are sorted in serial number descending order in debugger.ini file. So, the targets in the settings
        file should be sorted following this order.
        If this requirement cannot be met, then the debugger.ini file can be edited manually.

        :raise ``AssertionError``: If the number of debuggers does not match what was discovered by ``LibusbDriver``
        """
        debugger_targets = list(self.f.RUNTIME.DEBUGGERS.F_Targets)
        if "" in debugger_targets:
            debugger_targets.remove("")
        # end if
        assert len(debugger_targets) == LibusbDriver.discover_debug_probe(), \
               "Number of debuggers should match number of targets"

        for index, target in enumerate(debugger_targets):
            debugger_name = target.lower().replace(' ', '_') + "_debugger"
            memory_manager_name = target.lower().replace(' ', '_') + "_memory_manager"
            setattr(self, debugger_name, self.get_dbg(index_or_predicate=index, keep_for_test_duration=True))
            setattr(self, memory_manager_name, MemoryManagerFactory.create(
                debugger=getattr(self, debugger_name), target=target, config_mgr=self.config_manager))
        # end for
    # end def debuggers_setup

    def kosmos_tear_down(self):
        """
        Kosmos-related tearDown

        :raise ``AssertionError``: If the sequencer status after reset does not match ``SEQUENCER_STATE_RESET_DONE``
        """
        if self.kosmos is None or self.kosmos.is_fake():
            return
        # end if

        self._force_reset_microblaze = False

        # Check if Kosmos Fatal Errors were raised during the previous test run
        if KosmosFatalError.has_exception():
            exceptions_names = ', '.join(f'<{exception.__class__.__name__}>'
                                         for exception in KosmosFatalError.get_exception())
            self.log_warning(f'{exceptions_names} was raised during the test case method '
                             f'<{self.__module__}.{self.__class__.__name__}.{self._testMethodName}>.\n'
                             '==> As a consequence, the Microblaze core will be soft-reset before '
                             'continuing the test suite.', force_console_print=True)
            self._force_reset_microblaze = True
        # end if

        # Assess if Global Error Flag was raised during the test
        if self.kosmos.fpga.is_global_error_flag_raised():
            self.log_warning(
                'The Global Error Flag was raised during the execution of the test method '
                f'<{self.__module__}.{self.__class__.__name__}.{self._testMethodName}>.', force_console_print=True)
            self.kosmos.fpga.reset_global_error_flag()
            self._force_reset_microblaze = True
        # end if

        # Assess remote modules status only if the microblaze is not a reset state
        if not self._force_reset_microblaze:
            status = self.kosmos.sequencer.status()
            error_list = self.kosmos.sequencer.is_sequencer_state_clean(status)
            if error_list:
                self.log_warning('Issue detected in test case teardown.\n' + '\n'.join(error_list),
                                 force_console_print=True)
                self._force_reset_microblaze = True
            # end if
        # end if

        if self._force_reset_microblaze:
            try:
                # Soft-reset the Microblaze
                hw_rev = self.kosmos.dt.fpga.soft_reset_microblaze()
                self.log_warning(f"Fpga version: {hw_rev}")

                status_after_reset = self.kosmos.sequencer.status()
                self.log_warning(
                    f"Sequencer status after reset: {status_after_reset}",
                    force_console_print=True if status_after_reset.state != SEQUENCER_STATE_RESET_DONE else False)
                assert status_after_reset.state == SEQUENCER_STATE_RESET_DONE
                self._force_reset_microblaze = False
            except (SpiTransactionError, AssertionError):
                self.log_warning("Exception in Kosmos tearDown, wait 30s before retry soft reset microblaze")
                sleep(30)
                # Soft-reset the Microblaze
                hw_rev = self.kosmos.dt.fpga.soft_reset_microblaze()
                self.log_warning(f"Fpga version: {hw_rev}")

                status_after_reset = self.kosmos.sequencer.status()
                self.log_warning(
                    f"Sequencer status after second reset: {status_after_reset}",
                    force_console_print=True if status_after_reset.state != SEQUENCER_STATE_RESET_DONE else False)
                self._force_reset_microblaze = False
            # end try

            # Reset flags
            self._force_reset_microblaze = False
            KosmosFatalError.clear_exception()

            # Re-initialize kosmos pods configuration after the soft reset
            self.kosmos.pods_configuration.init_pods(device_tree=self.kosmos.dt)
            if (self.button_stimuli_emulator is not None and
                    isinstance(self.button_stimuli_emulator, KosmosKeyMatrixEmulator)):
                # Send back default memory cache to kosmos fpga
                self.button_stimuli_emulator.send_default_memory_cache_to_fpga()
                self.button_stimuli_emulator.release_all()
            # end if
        # end if

        # Clear local Kosmos Module buffers
        self.kosmos.dt.sequencer.clear_buffer()
    # end def kosmos_tear_down

    def _log_channel_identifiers_to_get_current_channel(self):
        """
        Log the channel identifiers when trying to find the current channel
        """
        if self.device_ids is None:
            return
        # end if

        to_log = "Try finding current channel using those channel identifiers:"
        for channel_identifier in self.device_ids:
            to_log += f"\n\t- {channel_identifier}"
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, to_log)
        # --------------------------------------------------------------------------------------------------------------
    # end def _log_channel_identifiers_to_get_current_channel

    @property
    def debugger(self):
        """
        Get the debugger (if it exists) of the DUT (device or receiver).

        READ ONLY PROPERTY

        :return: The debugger of the DUT
        :rtype: ``JLinkDebugger`` or ``None``
        """
        return None
    # end def property getter debugger

    @property
    def memory_manager(self):
        """
        Get the memory manager (if it exists) of the DUT (device or receiver).

        READ ONLY PROPERTY

        NB: Compatible with NRF52 memory manager structure only.

        :return: The memory manager of the DUT
        :rtype: ``MemoryManager`` or ``None``
        """
        return None
    # end def property getter memory_manager

    @property
    def companion_debugger(self):
        """
        Get debugger (if it exists) of the companion MCU of the DUT (device or receiver).

        READ ONLY PROPERTY

        :return: The debugger of the companion MCU of the DUT
        :rtype: ``JLinkDebugger`` or ``None``
        """
        return None
    # end def property getter companion_debugger

    @property
    def kosmos(self):
        """
        Get the Kosmos instance.

        READ ONLY PROPERTY

        :return: Kosmos instance
        :rtype: ``Kosmos``
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        return emulators_manager.kosmos
    # end def property getter kosmos

    @property
    def button_stimuli_emulator(self):
        """
        Get the button stimuli emulator instance.

        READ ONLY PROPERTY

        :return: Button stimuli emulator instance
        :rtype: ``KosmosKeyMatrixEmulator or BasicButtonEmulator or KeyboardEmulator or KosmosDualKeyMatrixEmulator``
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        return emulators_manager.button_stimuli_emulator
    # end def property getter button_stimuli_emulator

    @property
    def power_slider_emulator(self):
        """
        Get the power slider emulator instance.

        READ ONLY PROPERTY

        :return: Power slider emulator instance
        :rtype: ``KosmosPowerSliderEmulator``
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        return emulators_manager.power_slider_emulator
    # end def property getter power_slider_emulator

    @property
    def ambient_light_sensor_emulator(self):
        """
        Get the ambient light sensor emulator instance.

        READ ONLY PROPERTY

        :return: Ambient light sensor emulator instance
        :rtype: ``AmbientLightSensorEmulator``
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        return emulators_manager.ambient_light_sensor_emulator
    # end def property getter ambient_light_sensor_emulator

    @property
    def proximity_sensor_emulator(self):
        """
        Get the proximity sensor emulator instance.

        READ ONLY PROPERTY

        :return: Proximity sensor emulator instance
        :rtype: ``ProximitySensorEmulator``
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        return emulators_manager.proximity_sensor_emulator
    # end def property getter proximity_sensor_emulator

    @property
    def led_spy_over_i2c(self):
        """
        Get the LED over I2C spy instance

        :return: LED over I2C spy instance
        :rtype: ``KosmosLedSpyOverI2c``
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        return emulators_manager.led_spy_over_i2c
    # end def property getter led_spy_over_i2c

    @property
    def motion_emulator(self):
        """
        Get the motion emulator instance

        :return: Motion emulator instance
        :rtype: ``KosmosMotionEmulator``
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        motion_emulator: KosmosMotionEmulator = emulators_manager.motion_emulator
        return motion_emulator
    # end def property getter motion_emulator

    @property
    def game_mode_emulator(self):
        """
        Get the game mode emulator instance.

        READ ONLY PROPERTY

        :return: Game mode emulator instance
        :rtype: ``GameModeEmulator``
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        return emulators_manager.game_mode_emulator
    # end def property getter game_mode_emulator

    def hasFeature(self, feature_name):
        """
        Tell whether a feature is present or not.

        :param feature_name: Name of the feature to test
        :type feature_name: ``str``

        :return: ``True`` is feature is present, ``False`` otherwise
        :rtype: ``bool``
        """
        return features._decoratorToFeatures[feature_name](context=self.getContext())
    # end def hasFeature

    def wake_up_device_with_user_action(self):
        """
        Perform a user action to wake up the device and wait for ``WirelessDeviceStatusBroadcastEvent`` to be received.
        """
        # Perform a user action to wake the device up
        self.button_stimuli_emulator.user_action()

        if isinstance(self.current_channel, ThroughReceiverChannel):
            # Wait for 0x1D4B to be sent
            ChannelUtils.get_only(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=WirelessDeviceStatusBroadcastEvent,
                check_first_message=False,
                allow_no_message=True)
            # Empty connection event queue
            ChannelUtils.clean_messages(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=(DeviceConnection, DeviceDisconnection))
        # end if
    # end def wake_up_device_with_user_action

    def testCaseChecked(self, criterion, author=None, comment=None):
        """
        Check a criterion as validated.

        :param criterion: The criterion to validate
        :type criterion: ``str``
        :param author: The author of the validation - OPTIONAL
        :type author: ``str`` or ``None``
        :param comment: An optional comment on the validation - OPTIONAL
        :type comment: ``str`` or ``None``
        """
        DeviceTestCase.testCaseChecked(self, criterion, author=author, comment=comment)
    # end def testCaseChecked

    @staticmethod
    def get_device_info_bit_field_structure_in_device_connection(device_connection):
        """
        Get device information class from protocol type bit.

        :param device_connection: The notification from the receiver
        :type device_connection: ``DeviceConnection``

        :return: The class to use to get the Device Info format in DeviceConnection
        :rtype: ``BluetoothOrQuadReceiverInformation`` or ``EQuadReceiverInformation``
        """
        protocol_type = int(Numeral(device_connection.protocol_type))
        if protocol_type == DeviceConnection.ProtocolTypes.BLUETOOTH:
            return BluetoothOrQuadReceiverInformation
        elif protocol_type in [DeviceConnection.ProtocolTypes.QUAD_OR_EQUAD,
                               DeviceConnection.ProtocolTypes.EQUAD_STEP_4_DJ,
                               DeviceConnection.ProtocolTypes.EQUAD_STEP_4_LITE,
                               DeviceConnection.ProtocolTypes.EQUAD_STEP_4_GAMING,
                               DeviceConnection.ProtocolTypes.EQUAD_STEP_4_GAMEPADS,
                               DeviceConnection.ProtocolTypes.DVC_DEF_PROTOCOL_GOTHARD,
                               DeviceConnection.ProtocolTypes.DVC_DEF_PROTOCOL_GAMING,
                               DeviceConnection.ProtocolTypes.DVC_DEF_PROTOCOL_GAMING_V2,
                               DeviceConnection.ProtocolTypes.DVC_DEF_PROTOCOL_GAMING_LS2_LLPM,
                               DeviceConnection.ProtocolTypes.DVC_DEF_PROTOCOL_GAMING_LS2_CA,
                               DeviceConnection.ProtocolTypes.DVC_DEF_PROTOCOL_GAMING_LS2_CA_2]:
            return EQuadReceiverInformation
        elif protocol_type in [DeviceConnection.ProtocolTypes.BLE_PRO, DeviceConnection.ProtocolTypes.UNKNOWN]:
            # Following the merge of this commit on the 'mpr01_gravity codeline',
            # we have to add 'Unknown' in the list of possible returned protocol type value:
            #  lble_hidpp, fix ghost slot issue
            #
            # This change addresses the problem where a device is not reported
            # to the host due to incomplete bonding information.
            # With this change, the receiver will continue reporting the presence
            # of such a device by
            # - using a 0x41 device connection notification with an unknown
            #   protocol value (0x00) upon receiving a fake device arrival
            #   command
            #
            # Change-Id: I2d299abe63bece6d32af7e96ca572bf869b56297
            return BLEProReceiverInformation
        # end if

        return None
    # end def get_device_info_bit_field_structure_in_device_connection

    def reset_ble_context_hardware(self):
        """
        Reset the hardware for the BLE context. The debugger is a shared resource with the device (as opposed to
        receiver). Therefore, it is important to disconnect the jlink from the device.

        # TODO: this method should be moved in the device manager when developed
        """
        if self.device_debugger is not None and self.jlink_connection_control is not None and \
                EmulatorsManager.is_jlink_io_switch_present(features=self.f) and LibusbDriver.BLE_CONTEXT is not None:
            with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=self.device_debugger):
                with self.jlink_connection_control.disconnected():
                    LibusbDriver.reset_ble_context_hardware(debugger=self.device_debugger)
                # end with
            # end with
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"BLE context reset: {type(LibusbDriver.BLE_CONTEXT)}")
            # ----------------------------------------------------------------------------------------------------------
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"BLE context was not reset, current: {type(LibusbDriver.BLE_CONTEXT)}")
            # ----------------------------------------------------------------------------------------------------------
        # end if
    # end def reset_ble_context_hardware

    def update_ble_context_hardware(self, force=False):
        """
        Update the hardware for the BLE context. The debugger is a shared resource with the device (as opposed to
        receiver). Therefore, it is important to disconnect the jlink from the device.

        # TODO: this method should be moved in the device manager when developed

        :param force: Flag indicating to force the update, even if the hardware is already up-to-date - OPTIONAL
        :type force: ``bool``
        """
        ble_context_class_id = self.f.PRODUCT.PROTOCOLS.BLE.F_BleContextClassId

        if ble_context_class_id is not None and self.jlink_connection_control is not None and \
                self.device_debugger is not None and EmulatorsManager.is_jlink_io_switch_present(features=self.f):
            LibusbDriver.update_ble_context_hardware(
                ble_context_class_id=ble_context_class_id, debugger=self.device_debugger,
                jlink_connection_control=self.jlink_connection_control, force=force)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"BLE context updated: {type(LibusbDriver.BLE_CONTEXT)}")
            # ----------------------------------------------------------------------------------------------------------
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"BLE context was not updated, current: {type(LibusbDriver.BLE_CONTEXT)}")
            # ----------------------------------------------------------------------------------------------------------
        # end if
    # end def update_ble_context_hardware

    def getOutputDir(self):
        """
        Get current output directory. Points to files in LOCAL.

        :return: Absolute path
        :rtype: ``str``
        """

        config = self.getContext().getConfig()

        root_path = config.get(ContextLoader.SECTION_CONFIG,
                               ContextLoader.OPTION_ROOTPATHS)[0].replace('\\\\?\\', '')
        product = config.get(ContextLoader.SECTION_PRODUCT,
                             ContextLoader.OPTION_VALUE)
        version = config.get(ContextLoader.SECTION_VARIANT,
                             ContextLoader.OPTION_VALUE).replace('/', '\\')  # Subvariant -> subfolder
        target = config.get(ContextLoader.SECTION_TARGET,
                            ContextLoader.OPTION_VALUE)
        path_elts = [root_path, "LOCAL", product, version, target, ]

        return join(*path_elts)
    # end def getOutputDir

    def get_dut_nvs_parser(self):
        """
        Get the DUT NVS parser from memory (if debugger available).

        NB: Compatible with NRF52 NVS structure only.

        :return: The wanted NVS parser or ``None`` if the associated debugger is not present
        :rtype: ``NvsParser`` or ``None``
        """
        if self.memory_manager is not None:
            self.memory_manager.read_nvs()
            return self.memory_manager.nvs_parser
        # end if

        return None
    # end def get_dut_nvs_parser

    def initialize_emulators(self):
        """
        Initialize Emulator classes depending on the detection of external hardware tools.
        """
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        if self.kosmos is None:
            emulators_manager.init_kosmos()
        # end if
        if self.power_supply_emulator is None:
            emulators_manager.init_power_supply()
            self.power_supply_emulator = emulators_manager.power_supply_emulator
        # end if
        if self.power_slider_emulator is None:
            emulators_manager.init_power_slider_emulator()
        # end if
        if self.button_stimuli_emulator is None:
            emulators_manager.init_button_emulator(self.config_manager.current_device_type)
        # end if
        if self.ambient_light_sensor_emulator is None:
            emulators_manager.init_ambient_light_sensor_emulator()
        # end if
        if self.proximity_sensor_emulator is None:
            emulators_manager.init_proximity_sensor_emulator()
        # end if
        if self.led_spy is None:
            emulators_manager.init_led_monitoring_service()
            self.led_spy = emulators_manager.led_spy
        # end if
        if self.led_spy_over_i2c is None:
            emulators_manager.init_led_spy_over_i2c_monitoring_service()
        # end if
        if self.motion_emulator is None:
            emulators_manager.init_motion_emulator()
        # end if
        if self.jlink_connection_control is None:
            emulators_manager.init_jlink_io_switch()
            self.jlink_connection_control = emulators_manager.jlink_connection_control
        # end if
        if self.game_mode_emulator is None:
            emulators_manager.init_game_mode_emulator()
        # end if
    # end def initialize_emulators

    @staticmethod
    def host_number_to_port_index(host_index):
        """
        Get the port index of a host index according to what was decided upon when creating a node: the first
        port is host 0, and each other host is on a next port. Since the port indexes start at 1, it means that the
        port index is the host index + 1.

        :param host_index: The host index to use
        :type host_index: ``int``

        :return: The port index for the host
        :rtype: ``int``
        """
        return host_index + 1
    # end def host_number_to_port_index

    @staticmethod
    def port_index_to_host_number(port_index):
        """
        Get the host index for a port index according to what was decided upon when creating a node: the first
        port is host 0, and each other host is on a next port. Since the port indexes start at 1, it means that the
        host index is the port index - 1.

        :param port_index: The port index to use
        :type port_index: ``int``

        :return: The host index for the port
        :rtype: ``int``
        """
        return port_index - 1
    # end def port_index_to_host_number

    def is_hardware_reset_possible(self):
        """
        Verify if a hardware reset is possible.

        :return: Flag indicating if a hardware reset is possible
        :rtype: ``bool``
        """
        return self.power_slider_emulator is not None or self.power_supply_emulator is not None or \
            self.debugger is not None
    # end def is_hardware_reset_possible

    def hardware_reset(self, *args, **kwargs):
        """
        DEPRECATED

        Perform a hardware reset. This will NOT handle anything else (channel, connection events, ...) than the reset.

        :param args: Potential child argument - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential child keyword argument - OPTIONAL
        :type kwargs: ``object``
        """
        raise NotImplementedAbstractMethodError()
    # end def hardware_reset

    def reset(self, *args, **kwargs):
        """
        Reset DUT connection.

        :param args: Potential child argument - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential child keyword argument - OPTIONAL
        :type kwargs: ``object``
        """
        raise NotImplementedAbstractMethodError()
    # end def reset

    # ------------------------------------------------------------- #
    #      Deprecated methods kept for backward compatability       #
    # ------------------------------------------------------------- #
    @property
    def hidDispatcher(self):
        """
        DEPRECATED

        Property getter of ``hidDispatcher``.

        :return: ``hidDispatcher`` value
        :rtype: ``HIDDispatcher``
        """
        warnings.warn(
            'This function is deprecated, you should avoid using directly the dispatcher and use the wrapper methods',
            DeprecationWarning)

        if self.current_channel is None:
            return None
        # end if

        return self.current_channel.hid_dispatcher
    # end def property getter hidDispatcher

    @property
    def deviceIndex(self):
        """
        DEPRECATED

        Property getter of ``deviceIndex``.

        :return: ``deviceIndex`` value
        :rtype: ``int``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.get_device_index instead', DeprecationWarning)

        return ChannelUtils.get_device_index(test_case=self)
    # end def property getter deviceIndex

    def enable_hidpp_reporting(self, enable=True):
        """
        DEPRECATED

        Enable the HID++ reporting flag of the receiver.

        :param enable: Flag enabling the HID++ reporting - OPTIONAL
        :type enable: ``bool``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.set_hidpp_reporting instead', DeprecationWarning)

        ChannelUtils.set_hidpp_reporting(
            test_case=self, channel=self.current_channel, enable=enable, force_send_unknown_channel_type=True)
    # end def enable_hidpp_reporting

    def _set_current_channel_to_expected_one(self, device_index=None, port_index=None):
        """
        DEPRECATED

        Change the current channel to the expected one.

        :param device_index: The index of the device to use. If ``None``, the instance device index will be
                             used - OPTIONAL
        :type device_index: ``int`` or ``None``
        :param port_index: Port Index. If ``None``, the instance port index will be used - OPTIONAL
        :type port_index: ``int`` or ``None``
        """
        warnings.warn(
            'This function is deprecated and should not be used at all', DeprecationWarning)

        current_port_index = ChannelUtils.get_port_index(test_case=self)
        current_device_index = ChannelUtils.get_device_index(test_case=self)
        port_index = port_index if port_index is not None else current_port_index
        device_index = device_index if device_index is not None else current_device_index

        wanted_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                port_index=port_index,
                device_index=device_index if device_index != Hidpp1Data.DeviceIndex.TRANSCEIVER else None))

        if wanted_channel is not None and wanted_channel != self.current_channel:
            self.log_traceback_as_warning(
                supplementary_message="The wanted channel is not the current one, change current "
                                      "channel before using this method",
                force_console_print=False)

            ChannelUtils.open_channel(test_case=self, channel=wanted_channel)

            if self.current_channel.protocol == wanted_channel.protocol:
                self.current_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
                    other_dispatcher=wanted_channel.hid_dispatcher)
            elif self.backup_dut_channel.protocol == wanted_channel.protocol:
                self.backup_dut_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
                    other_dispatcher=wanted_channel.hid_dispatcher)
            # end if

            self.current_channel = wanted_channel
        # end if
    # end def _set_current_channel_to_expected_one

    def _set_current_channel_to_expected_one_from_report(self, report):
        """
        DEPRECATED

        Change the current channel to the expected one from a report.

        :param report: The report to use
        :type report: ``BitFieldContainerMixin``
        """
        warnings.warn(
            'This function is deprecated and should not be used at all', DeprecationWarning)

        wanted_device_index = to_int(report.device_index)
        if isinstance(report, (Hidpp1Message, HidppMessage)) and \
                wanted_device_index != ChannelUtils.get_device_index(test_case=self):
            wanted_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                    port_index=ChannelUtils.get_port_index(test_case=self),
                    device_index=wanted_device_index if wanted_device_index != Hidpp1Data.DeviceIndex.TRANSCEIVER
                    else None))

            if wanted_channel is not None and wanted_channel != self.current_channel:
                self.log_traceback_as_warning(
                    supplementary_message="The wanted channel is not the current one, change current "
                                          "channel before using this method",
                    force_console_print=False)

                ChannelUtils.open_channel(test_case=self, channel=wanted_channel)

                if self.current_channel.protocol == wanted_channel.protocol:
                    self.current_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
                        other_dispatcher=wanted_channel.hid_dispatcher)
                elif self.backup_dut_channel.protocol == wanted_channel.protocol:
                    self.backup_dut_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
                        other_dispatcher=wanted_channel.hid_dispatcher)
                # end if

                self.current_channel = wanted_channel
            # end if
        # end if
    # end def _set_current_channel_to_expected_one_from_report

    def updateFeatureMapping(self, feature_id, device_index=None, port_index=None, skip_not_found=False):
        """
        DEPRECATED

        Retrieve feature ID to feature index mapping from DUT and update the internal ``HidDispatcher``.

        :param feature_id: The feature ID to add to the feature mapping
        :type feature_id: ``int``
        :param device_index: The index of the device to use. If ``None``, the instance device index will be
                             used - OPTIONAL
        :type device_index: ``int`` or ``None``
        :param port_index: Port Index. If ``None``, the instance port index will be used - OPTIONAL
        :type port_index: ``int`` or ``None``
        :param skip_not_found: Flag indicating that the method shall raise an error when the feature ID is
                               not found if ``False`` and return 0 if ``True`` - OPTIONAL
        :type skip_not_found: ``bool``

        :return: The feature Index returned by the device
        :rtype: ``int``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.update_feature_mapping instead', DeprecationWarning)

        # Since this is a deprecated method called in a deprecated method, it is acceptable
        # noqa is used as there is no noinspection for it
        self._set_current_channel_to_expected_one(device_index=device_index, port_index=port_index)  # noqa

        return ChannelUtils.update_feature_mapping(test_case=self, feature_id=feature_id, skip_not_found=skip_not_found)
    # end def updateFeatureMapping

    def empty_queue(self, queue):
        """
        DEPRECATED

        Empty all device queues.

        :param queue: Queue to empty
        :type queue: ``HidMessageQueue``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.empty_queue instead', DeprecationWarning)

        if self.current_channel is None or not self.current_channel.is_open:
            return
        # end if

        ChannelUtils.empty_queue(test_case=self, queue_name=queue.name, channel=self.current_channel)
    # end def empty_queue

    def empty_queues(self):
        """
        DEPRECATED

        Empty all device queues.
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.empty_queues instead', DeprecationWarning)

        if self.current_channel is None or not self.current_channel.is_open:
            return
        # end if

        ChannelUtils.empty_queues(test_case=self, channel=self.current_channel)
    # end def empty_queues

    def send_report_to_device(self, report, timeout=0):
        """
        DEPRECATED

        Send a report to the device. This is a blocking method. If ``timeout`` is ``0`` it blocks infinitely while
        message is not sent.

        :param report: The report to send
        :type report: ``TimestampedBitFieldContainerMixin``
        :param timeout: Timeout to send the report - OPTIONAL
        :type timeout: ``int`` or ``float``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.send_only instead', DeprecationWarning)

        # Since this is a deprecated method called in a deprecated method, it is acceptable
        # noqa is used as there is no noinspection for it
        self._set_current_channel_to_expected_one_from_report(report=report)  # noqa

        ChannelUtils.send_only(test_case=self, report=report, timeout=timeout)
    # end def send_report_to_device

    def getMessage(self, queue, class_type=None, timeout=2, check_first_message=True, skip_error_message=False):
        """
        DEPRECATED

        Get message from queue and optionally check if its type is as expected.

        :param queue: The queue in which the message is expected
        :type queue: ``HidMessageQueue``
        :param class_type: The type(s) of expected message. If ``None``, the type is not checked - OPTIONAL
        :type class_type: ``type`` or ``tuple[type]`` or ``None``
        :param timeout: Time to wait for message before raising exception [seconds] - OPTIONAL
        :type timeout: ``float``
        :param check_first_message: Flag indicating if the order should be kept for checking the expected
                                    type - OPTIONAL
        :type check_first_message: ``bool``
        :param skip_error_message: Flag indicating if the automatic error catching mechanism should be skipped or
                                   not. This will be always True if the queue is hid_message_queue (HID++ error message
                                   are not important to HID messages) - OPTIONAL
        :type skip_error_message: ``bool``

        :return: The message retrieved from the queue
        :rtype: ``BitFieldContainerMixin`` or ``class_type``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.get_only instead', DeprecationWarning)

        channel_to_use = self.current_channel
        if isinstance(channel_to_use, ThroughReceiverChannel) and "Receiver" in queue.name:
            channel_to_use = channel_to_use.receiver_channel
        # end if

        return ChannelUtils.get_only(
            test_case=self,
            channel=channel_to_use,
            queue_name=queue.name,
            class_type=class_type,
            timeout=timeout,
            check_first_message=check_first_message,
            skip_error_message=skip_error_message)
    # end def getMessage

    def get_first_message_type_in_queue(
            self, queue, class_type, timeout=2, allow_no_message=False, skip_error_message=False):
        """
        DEPRECATED

        Get the first message from a Queue that matches the given type.

        :param queue: The queue in which the message is expected
        :type queue: ``HidMessageQueue``
        :param class_type: The type of messages to be retrieved from the queue, cannot be ``None``
        :type class_type: ``type`` or ``tuple[type]``
        :param timeout: Time to wait for message before raising exception [seconds] - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param allow_no_message: Flag to enable (default) / disable exception when the requested message in not
                                 received - OPTIONAL
        :type allow_no_message: ``bool``
        :param skip_error_message: Flag indicating if the automatic error catching mechanism should be skipped or
                                   not. This will be always True if the queue is hid_message_queue (JID++ error message
                                   are not important to HID messages) - OPTIONAL
        :type skip_error_message: ``bool``

        :return: message
        :rtype: ``class_type``

        :raise ``AssertionError``: If ``class_type`` is ``None``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.get_only with check_first_message=False '
            'instead',
            DeprecationWarning)

        assert class_type is not None, "class_type cannot be None"

        channel_to_use = self.current_channel
        if isinstance(channel_to_use, ThroughReceiverChannel) and "Receiver" in queue.name:
            channel_to_use = channel_to_use.receiver_channel
        # end if

        return ChannelUtils.get_only(
            test_case=self,
            channel=channel_to_use,
            queue_name=queue.name,
            class_type=class_type,
            timeout=timeout,
            check_first_message=False,
            allow_no_message=allow_no_message,
            skip_error_message=skip_error_message)
    # end def get_first_message_type_in_queue

    def clean_message_type_in_queue(self, queue, class_type):
        """
        DEPRECATED

        Get Message from Queue and optionally check if its type is as expected

        :param queue: The queue in which the message is expected
        :type queue: ``HidMessageQueue``
        :param class_type: The type of messages to remove from the queue, cannot be ``None``
        :type class_type: ``type`` or ``tuple[type]``

        :return: List of removed messages
        :rtype: ``list[BitFieldContainerMixin]``

        :raise ``AssertionError``: If ``class_type`` is ``None``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.clean_messages instead',
            DeprecationWarning)

        assert class_type is not None, "class_type cannot be None"

        channel_to_use = self.current_channel
        if isinstance(channel_to_use, ThroughReceiverChannel) and "Receiver" in queue.name:
            channel_to_use = channel_to_use.receiver_channel
        # end if

        if channel_to_use is None or not channel_to_use.is_open:
            return
        # end if

        return ChannelUtils.clean_messages(
            test_case=self, channel=channel_to_use, queue_name=queue.name, class_type=class_type)
    # end def clean_message_type_in_queue

    def check_queue_empty(self, queue, during=0, class_type=None):
        """
        DEPRECATED

        Check that a queue is empty for the duration of ``timeout``.

        :param queue: The queue in which the message is expected
        :type queue: ``HidMessageQueue``
        :param during: Duration to check that the queue stays empty in second - OPTIONAL
        :type during: ``int`` or ``float``
        :param class_type: The type of messages to be retrieved from the queue, cannot be ``None`` - OPTIONAL
        :type class_type: ``type`` or ``tuple[type]`` or ``None``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.check_queue_empty instead',
            DeprecationWarning)

        channel_to_use = self.current_channel
        if isinstance(channel_to_use, ThroughReceiverChannel) and "Receiver" in queue.name:
            channel_to_use = channel_to_use.receiver_channel
        # end if

        if channel_to_use is None or not channel_to_use.is_open:
            return
        # end if

        ChannelUtils.check_queue_empty(
            test_case=self, channel=channel_to_use, queue_name=queue.name, timeout=during, class_type=class_type)
    # end def check_queue_empty

    def is_current_hid_dispatcher_queue_empty(self, queue):
        """
        DEPRECATED

        Return a flag indicating if the current HID dispatcher queue given is empty or not. This method has been
        created only to be able to get the right dispatcher when used for receiver queues when the current device is
        through a receiver. It is done for backward compatibility and should not be used in the future.

        :param queue: Queue to check
        :type queue: ``HidMessageQueue``

        :return: Flag indicating if the queue is empty or not
        :rtype: ``bool``

        :raise ``AssertionError``: If ``queue`` is ``None``
        """
        warnings.warn('This function is deprecated, Should not be used at all', DeprecationWarning)

        channel_to_use = self.current_channel
        if isinstance(channel_to_use, ThroughReceiverChannel) and "Receiver" in queue.name:
            channel_to_use = channel_to_use.receiver_channel
            queue = channel_to_use.hid_dispatcher.get_queue_by_name(name=queue.name)
            assert queue is not None, f"Could not find receiver queue: {queue.name}"
        # end if

        if channel_to_use is None or not channel_to_use.is_open:
            return True
        # end if

        for report_type in (LogitechReportType.HIDPP, LogitechReportType.MOUSE, LogitechReportType.KEYBOARD):
            channel_to_use.process_all_report_type_in_dispatcher(report_type=report_type)
        # end for

        return queue.event_empty.is_set()
    # end def is_current_hid_dispatcher_queue_empty

    def send_report_wait_response(
            self, report, response_queue, timeout=.6, response_class_type=None, skip_error_message=False):
        """
        DEPRECATED

        Get Message from Queue and optionally check if its type is as expected.
        This function is used because of the instability of libusb.

        :param report: The report to send
        :type report: ``BitFieldContainerMixin``
        :param response_queue: The queue in which the message is expected
        :type response_queue: ``HidMessageQueue``
        :param timeout: If ``timeout`` <= 0, the sending process is non-blocking. Otherwise, the sending process waits
                        for the report to be sent or for the timeout to be reached DEPRECATED - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param response_class_type: The type of expected message. If ``None``, the type is not checked - OPTIONAL
        :type response_class_type: ``type`` or ``tuple[type]`` or ``None``
        :param skip_error_message: Flag indicating if the automatic error catching mechanism should be skipped or
                                   not. This will be always True if the queue is hid_message_queue (JID++ error message
                                   are not important to HID messages) - OPTIONAL
        :type skip_error_message: ``bool``

        :return: The message get from the queue
        :rtype: ``BitFieldContainerMixin`` or ``response_class_type``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.send instead',
            DeprecationWarning)

        # Since this is a deprecated method called in a deprecated method, it is acceptable
        # noqa is used as there is no noinspection for it
        self._set_current_channel_to_expected_one_from_report(report=report)  # noqa

        channel_to_use = self.current_channel
        if isinstance(channel_to_use, ThroughReceiverChannel) and isinstance(report, Hidpp1Message):
            channel_to_use = channel_to_use.receiver_channel
        # end if

        return ChannelUtils.send(
            test_case=self,
            channel=channel_to_use,
            report=report,
            response_queue_name=response_queue.name,
            send_timeout=timeout,
            response_class_type=response_class_type,
            skip_error_message=skip_error_message)
    # end def send_report_wait_response

    def get_device_descriptors(self):
        """
        DEPRECATED

        Retrieve interface descriptors from the DUT.
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.get_descriptors instead', DeprecationWarning)
        ChannelUtils.get_descriptors(test_case=self)
    # end def get_device_descriptors

    def warn_if_not_empty(self, message_queue):
        """
        DEPRECATED

        Check if there is any message in a queue. It will add a warning if the queue is not empty.

        :param message_queue: The queue to be checked
        :type message_queue: ``HidMessageQueue``

        :return: ``True`` if the queue is empty, ``False`` otherwise
        :rtype: ``bool``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.warn_queue_not_empty instead',
            DeprecationWarning)

        channel_to_use = self.current_channel
        if isinstance(channel_to_use, ThroughReceiverChannel) and "Receiver" in message_queue.name:
            channel_to_use = channel_to_use.receiver_channel
        # end if

        if channel_to_use is None or not channel_to_use.is_open:
            return True
        # end if

        return ChannelUtils.warn_queue_not_empty(
            test_case=self, queue_name=message_queue.name, channel=channel_to_use)
    # end def warn_if_not_empty

    def get_feature_version_from_dut_to_int(self, feature_index, device_index=None, port_index=None):
        """
        DEPRECATED

        Get version of a feature from the device under test using its feature id.

        :param feature_index: Feature index
        :type feature_index: ``int``
        :param device_index: Device index DEPRECATED - OPTIONAL
        :type device_index: ``int``
        :param port_index: Port index DEPRECATED - OPTIONAL
        :type port_index: ``int``

        :return: Feature version
        :rtype: ``int``
        """
        warnings.warn(
            'This function is deprecated, use ChannelUtils.get_feature_version instead',
            DeprecationWarning)

        # Since this is a deprecated method called in a deprecated method, it is acceptable
        # noqa is used as there is no noinspection for it
        self._set_current_channel_to_expected_one(device_index=device_index, port_index=port_index)  # noqa

        return ChannelUtils.get_feature_version(test_case=self, feature_index=feature_index)
    # end def get_feature_version_from_dut_to_int

    def channel_disable(self, usb_port_index):
        """
        DEPRECATED

        Disable a USB port.

        :param usb_port_index: USB port to disable
        :type usb_port_index: ``int``
        """
        warnings.warn(
            'This function is deprecated, it should not be used at all, it will be replaced with the device manager',
            DeprecationWarning)

        if usb_port_index == ChannelUtils.get_port_index(test_case=self):
            # Stop Task executor
            ChannelUtils.close_channel(test_case=self)
        # end if
        self.device.disable_usb_port(usb_port_index)
    # end def channel_disable

    # TODO : different functions for different needs should be implemented:
    #  - port_disable
    #  - port_enable
    #  - channel_disable
    #  - channel_enable
    def channel_enable(self, usb_port_index, wait_time=2.0):
        """
        DEPRECATED

        Enable a USB port.

        :param usb_port_index: USB port to enable
        :type usb_port_index: ``int``
        :param wait_time: Time to let for the device to recover after its internal reset - OPTIONAL
        :type wait_time: ``float``
        """
        warnings.warn(
            'This function is deprecated, it should not be used at all, it will be replaced with the device manager',
            DeprecationWarning)

        if isinstance(self.current_channel, ThroughReceiverChannel) and \
                ChannelUtils.get_port_index(test_case=self) == usb_port_index:
            device_index = self.current_channel.device_index
        else:
            device_index = None
        # end if

        self.device.enable_usb_port(usb_port_index)
        # Stop Task executor
        ChannelUtils.close_channel(test_case=self)
        # Let some time for the device to recover after its internal reset
        sleep(wait_time)
        # Start on the connected device
        # Since this is a deprecated method called in a deprecated method, it is acceptable
        # noqa is used as there is no noinspection for it
        self.channel_switch(device_uid=ChannelIdentifier(port_index=usb_port_index, device_index=device_index))  # noqa
    # end def channel_enable

    def channel_switch(self, task_enabler=BitStruct(Numeral(LinkEnablerInfo.ALL_MASK)), device_uid=None):
        """
        DEPRECATED

        Switch communication channel (To be used after a 0x1814 HID++ Change Host request).

        :param task_enabler: List of polling task to be executed - OPTIONAL
        :type task_enabler: ``BitStruct``
        :param device_uid: The device unique identifier of the device to switch to - OPTIONAL
        :type device_uid: ``ChannelIdentifier`` or ``None``

        :return: ``True`` if connection on the usb port index succeeded, ``False`` otherwise
        :rtype: ``bool``
        """
        warnings.warn(
            'This function is deprecated, it should not be used at all, it will be replaced with the device manager',
            DeprecationWarning)

        device_ids = [device_uid] if device_uid is not None else self.device_ids

        new_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=device_ids, check_connected=True)

        if new_channel is None:
            return False
        # end if

        if self.current_channel.is_open:
            ChannelUtils.close_channel(test_case=self)
        # end if
        DeviceManagerUtils.set_channel(test_case=self, new_channel=new_channel, open_channel=False)
        ChannelUtils.open_channel(test_case=self, link_enabler=task_enabler)

        f = self.getFeatures()
        if f.PRODUCT.USB_COMMUNICATION.F_SetIdleSupported:
            ChannelUtils.set_idle(test_case=self)
        # end if

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        return True
    # end def channel_switch

    @contextmanager
    def manage_post_requisite(self):
        """
        Manage post requisite and catch exception if any.

        Note: For Kosmos-related post requisite actions, use `manage_kosmos_post_requisite()` instead.
        """
        # noinspection PyBroadException
        try:
            yield
        except Exception as e:
            self.log_traceback_as_warning(
                supplementary_message=f"Exception during a post-requisite execution in tearDown: {e}")
        # end try
    # end def manage_post_requisite

    @contextmanager
    def manage_kosmos_post_requisite(self):
        """
        Manage Kosmos-related post requisite and catch exception if any.
        Ensure Kosmos setup is in a ready state before triggering the post requisite action.

        Note: For post requisite actions not related to Kosmos, use `manage_post_requisite()` instead.
        """
        # noinspection PyBroadException
        try:
            with self.manage_post_requisite():
                if not self._kosmos_post_requisite_done:
                    self.kosmos_tear_down()
                    self._kosmos_post_requisite_done = True
                # end if
            # end with
            yield
        except Exception:
            self.log_traceback_as_warning(
                supplementary_message="Exception during a Kosmos post-requisite execution in tearDown:")
        # end try
    # end def manage_kosmos_post_requisite

    def cleanup_battery_event_from_queue(self):
        """
        Remove all Battery related notifications from the event message queue
        """
        # Empty event message queue from BatteryLevelStatusBroadcastEvent notifications sent by the device
        if self.f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_Enabled:
            ChannelUtils.clean_messages(
                test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
                class_type=BatteryLevelStatusBroadcastEvent)
        elif self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_Enabled:
            # Empty event message queue from BatteryStatusEvent notifications sent by the device
            feature_1004 = UnifiedBatteryFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY))
            ChannelUtils.clean_messages(
                test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
                class_type=feature_1004.battery_status_event_cls)
        # end if
    # end def cleanup_battery_event_from_queue
# end class CommonBaseTestCase


class DeviceBaseTestCase(CommonBaseTestCase):
    """
    TestCase class for tests targeting devices (Mouse, Keyboard, ... products).
    """
    # Protocol to change to in setUp method after finding the current channel. This permit to create specific test
    # cases for specific protocol. If not None, it should be a LogitechProtocol
    PROTOCOL_TO_CHANGE_TO = None

    # The naming of methodName is inherited from PyHarnessCase
    # noinspection PyPep8Naming
    def __init__(self, methodName='runTest'):
        # See ``CommonBaseTestCase.__init__``

        # To use when PROTOCOL_TO_CHANGE_TO is not None
        self.nvs_before_protocol_change = None
        self.backup_dut_protocol_channel = None
        self.ble_context_device_used = None

        self._setup_hardware_reset_done = False

        super().__init__(methodName=methodName)
    # end def __init__

    @property
    def debugger(self):
        # See ``CommonBaseTestCase.debugger``
        return self.device_debugger
    # end def property getter debugger

    @property
    def memory_manager(self):
        # See ``CommonBaseTestCase.memory_manager``
        return self.device_memory_manager
    # end def property getter memory_manager

    def setUp(self):
        """
        Create the test context, device and debugger initialization.

        :raise ``ValueError``: If the Root feature was not found
        """
        if PRINT_TEST_TIMINGS:
            start_time = time()
        # end if

        # Call inherited setup
        super().setUp()
        self.config_manager.current_target = ConfigurationManager.TARGET.DEVICE
        self._setup_hardware_reset_done = False

        if self.button_stimuli_emulator is not None and self.button_stimuli_emulator.connected_key_ids is None:
            self.button_stimuli_emulator.setup_connected_key_ids()
        # end if

        # Debugger connection setup
        self.debuggers_setup()

        if (self.device_debugger is not None) or (self.receiver_debugger is not None):
            if self.id().split('.')[2] == 'connectionscheme':
                # Cleanup all pairing slots except the first one
                CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)
                self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                    test_case=self, memory_manager=self.device_memory_manager)
                sleep(.1)
            else:
                # Let some time for the receivers to be ready after the debugger reset
                sleep(1.2)
            # end if
        else:
            # Useful for test setups lacking a debugger.
            sleep(1)
        # end if

        root_version = self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
        vlp_root_version = self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT)
        if root_version is None:
            raise ValueError('Unknown Root feature version!')
        # end if

        # Reset Kosmos Dual Keymatrix Emulator before each test
        if isinstance(self.button_stimuli_emulator, KosmosDualKeyMatrixEmulator):
            self.button_stimuli_emulator.setup_defaults()
        # end if

        # wake up the device
        if self.button_stimuli_emulator is not None and not ProtocolManagerUtils.is_corded_device_only(test_case=self):
            self.button_stimuli_emulator.user_action()
        # end if

        if self.f.PRODUCT.F_Enabled:
            self.create_device_handle()

            self._change_protocol_setup()
        # end if

        # TODO unplugging any charging mechanism
        # Must disable recharge before doing any tests
        if self.power_supply_emulator is not None:
            self.power_supply_emulator.recharge(enable=False)
        # end if

        # Start test threaded executor
        if self.device is not None:
            self.current_channel.hid_dispatcher.add_feature_entry(Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)
            if isinstance(self.current_channel, ThroughReceiverChannel):
                self.current_channel.receiver_channel.hid_dispatcher.add_feature_entry(
                    Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)
                if self.current_channel.protocol > LogitechProtocol.UNKNOWN:
                    self._reload_feature_cache()
                # end if
            # end if

            if vlp_root_version is not None:
                self.current_channel.hid_dispatcher.add_vlp_feature_entry(
                    VLPRoot.FEATURE_INDEX, VLPRoot.FEATURE_ID, vlp_root_version)
            # end if

            ChannelUtils.open_channel(test_case=self)
            # Prevent the DUT to send empty HID reports which could make the ChannelUtils.empty_queues call an
            # infinite loop
            if self.f.PRODUCT.USB_COMMUNICATION.F_SetIdleSupported and \
                    isinstance(self.current_channel, (UsbChannel, ThroughReceiverChannel)):
                ChannelUtils.set_idle(test_case=self)
            # end if

            # Descriptor
            ChannelUtils.get_descriptors(test_case=self)

            if not self._setup_hardware_reset_done:
                self.reset(hardware_reset=True,
                           verify_wireless_device_status_broadcast_event=(
                                   self.current_channel.protocol > LogitechProtocol.UNKNOWN and
                                   WirelessDeviceStatus.FEATURE_ID in LibusbDriver.FEATURE_CACHE),
                           cleanup_battery_event=False)
            # end if

            # Empty message queues
            ChannelUtils.empty_queues(test_case=self)

            if isinstance(self.current_channel, ThroughReceiverChannel):
                ChannelUtils.set_hidpp_reporting(test_case=self)
            # end if

            if self.current_channel.protocol > LogitechProtocol.UNKNOWN and \
                    WirelessDeviceStatus.FEATURE_ID not in LibusbDriver.FEATURE_CACHE:
                self._build_feature_cache()

                self._print_receiver_info()
            # end if

            self.original_device_index = ChannelUtils.get_device_index(test_case=self)

            if self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_Enabled:
                # Because the fn inversion state be stored in NVS by 0x40A3. Shall confirm the fn inversion state is
                # in default setting before executing test script.
                FnInversionForMultiHostDevicesTestUtils.restore_fn_inversion_to_default_for_all_hosts(self)
            # end if
        else:
            self.original_device_index = None
        # end if

        if PRINT_TEST_TIMINGS:
            # Noqa is used to avoid the error marking due to start_time being set in an if
            sys.stdout.write(f"Basetest setup took {time() - start_time}s\n")  # noqa

            self._start_time = time()
        # end if
    # end def setUp

    def _build_feature_cache(self):
        """
        Create a cache with the feature index, id and version for the 0x1D4B Wireless device status
        and 0x1004 Unified battery features
        """
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=WirelessDeviceStatus.FEATURE_ID)
        wds_index = self.current_channel.hid_dispatcher.get_feature_index(feature_id=WirelessDeviceStatus.FEATURE_ID)
        wds_id, wds_version = self.current_channel.hid_dispatcher.get_feature_entry_by_index(feature_index=wds_index)
        LibusbDriver.FEATURE_CACHE[WirelessDeviceStatus.FEATURE_ID] = (wds_index, wds_id, wds_version)
        battery_feature_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=UnifiedBattery.FEATURE_ID, skip_not_found=True)
        if battery_feature_index != Root.FEATURE_NOT_FOUND:
            batt_index = self.current_channel.hid_dispatcher.get_feature_index(feature_id=UnifiedBattery.FEATURE_ID)
            batt_id, batt_version = self.current_channel.hid_dispatcher.get_feature_entry_by_index(
                feature_index=batt_index)
            LibusbDriver.FEATURE_CACHE[UnifiedBattery.FEATURE_ID] = (batt_index, batt_id, batt_version)
        # end if
    # end def _build_feature_cache

    def _print_receiver_info(self):
        """
        Log on console the receiver revision and build id
        """
        if isinstance(self.current_channel, ThroughBleProReceiverChannel):
            # Read BLE Pro receiver FW information
            fw_info = EnumerationTestUtils.get_receiver_fw_version(
                self, entity_idx=self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(str(HexList(
                    ReceiverFwInfo.EntityType.MAIN_APP))))
            sys.stdout.write(f"\tBLE Pro Receiver FW build = 0x{fw_info.fw_build}, FW revision ="
                             f" 0x{fw_info.fw_revision}\n")
        # end if
    # end def _print_receiver_info

    def _reload_feature_cache(self):
        """
        Reload the feature cache in the current hid dispatcher feature mapping
        """
        if WirelessDeviceStatus.FEATURE_ID in LibusbDriver.FEATURE_CACHE:
            wds = LibusbDriver.FEATURE_CACHE[WirelessDeviceStatus.FEATURE_ID]
            self.current_channel.hid_dispatcher.add_feature_entry(wds[0], wds[1], wds[2])
        # end if
        if UnifiedBattery.FEATURE_ID in LibusbDriver.FEATURE_CACHE:
            batt = LibusbDriver.FEATURE_CACHE[UnifiedBattery.FEATURE_ID]
            self.current_channel.hid_dispatcher.add_feature_entry(batt[0], batt[1], batt[2])
        # end if
    # end def _reload_feature_cache

    def _change_protocol_setup(self):
        """
        Change during setup to the communication protocol given by ``PROTOCOL_TO_CHANGE_TO`` if set to any
        ``LogitechProtocol`` value. If ``PROTOCOL_TO_CHANGE_TO`` is ``None``, this method will just return.
        """
        if self.PROTOCOL_TO_CHANGE_TO is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(test_case=self, text=f'Select {repr(self.PROTOCOL_TO_CHANGE_TO)} channel')
            # ----------------------------------------------------------------------------------------------------------
            ProtocolManagerUtils.select_channel_by_protocol(test_case=self, protocol=self.PROTOCOL_TO_CHANGE_TO)
        # end if
    # end def _change_protocol_setup

    def tearDown(self):
        """
        Destroy the test.
        """
        if self._start_time is not None and PRINT_TEST_TIMINGS:
            sys.stdout.write(f"Test took {time() - self._start_time}s\n")
        # end if

        if PRINT_TEST_TIMINGS:
            start_time = time()
        # end if

        with self.manage_post_requisite():
            self._change_protocol_tear_down()
        # end with

        with self.manage_kosmos_post_requisite():
            if self.power_slider_emulator is not None:
                # Turn the power slider off
                self.power_slider_emulator.power_off()
            # end if

            # Turn off DUT
            if self.power_supply_emulator is not None:
                self.power_supply_emulator.turn_off()
                self.power_supply_emulator.recharge(enable=False)
            # end if
        # end with

        super().tearDown()

        if PRINT_TEST_TIMINGS:
            # Noqa is used to avoid the error marking due to start_time being set in an if
            sys.stdout.write(f"Basetest teardown took {time() - start_time}s\n")  # noqa
        # end if
    # end def tearDown

    def _change_protocol_tear_down(self):
        """
        Change during tear down to the communication protocol given by ``PROTOCOL_TO_CHANGE_TO`` if set to any
        ``LogitechProtocol`` value. If ``PROTOCOL_TO_CHANGE_TO`` is ``None``, this method will just return.

        :raise ``AssertionError``: If ``PROTOCOL_TO_CHANGE_TO`` is not ``None`` and not a ``LogitechProtocol``
        """
        if self.PROTOCOL_TO_CHANGE_TO in [None, LogitechProtocol.BLE_PRO]:
            return
        # end if

        assert isinstance(self.PROTOCOL_TO_CHANGE_TO, LogitechProtocol), \
            f"The protocol shall be of type LogitechProtocol, {self.PROTOCOL_TO_CHANGE_TO} is not"

        if self.PROTOCOL_TO_CHANGE_TO == LogitechProtocol.BLE:
            with self.manage_post_requisite():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload NVS from before switching to BLE")
                # ------------------------------------------------------------------------------------------------------
                self.device_memory_manager.backup_nvs_parser = self.nvs_before_protocol_change
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end with

            with self.manage_post_requisite():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Exit BLE channel")
                # ------------------------------------------------------------------------------------------------------
                ProtocolManagerUtils.exit_ble_channel(self)
            # end with
        elif self.PROTOCOL_TO_CHANGE_TO == LogitechProtocol.USB:
            with self.manage_post_requisite():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Unplug the USB cable to exit the USB protocol")
                # ------------------------------------------------------------------------------------------------------
                ProtocolManagerUtils.exit_usb_channel(test_case=self)
            # end with
        elif self.PROTOCOL_TO_CHANGE_TO == LogitechProtocol.LS2_CA_CRC24_FOR_CRUSH:
            with self.manage_post_requisite():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload NVS from before switching to Crush")
                # ------------------------------------------------------------------------------------------------------
                self.device_memory_manager.backup_nvs_parser = self.nvs_before_protocol_change
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end with

            with self.manage_post_requisite():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Exit crush channel")
                # ------------------------------------------------------------------------------------------------------
                ProtocolManagerUtils.exit_crush_channel(test_case=self)
            # end with
        else:
            raise NotImplementedError(
                f"The protocol {self.PROTOCOL_TO_CHANGE_TO} is not yet implemented to be used in change_protocol_setup")
        # end if
    # end def _change_protocol_tear_down

    @staticmethod
    def create_device_predicate(device_uid_list):
        """
        Create predicate with function parameters for USB Device.

        :param device_uid_list: List of the device unique identifier
        :type device_uid_list: ``list[ChannelIdentifier]``

        :return: The predicate created
        :rtype: ``callable type``
        """
        # create a hashable key
        key = str('_'.join(str(device_uid_list)))

        if key not in BaseTestCase._PREDICATE_CACHE:
            def device_predicate_true(device):
                """
                Predicate that returns ``True`` if matching USB device UID test, ``False`` otherwise.

                :param device: USB Device instance
                :type device: ``LibusbDriver``

                :return: ``True`` is the LibusbDriver configure function was called successfully
                :rtype: ``bool``
                """
                return device.IS_CONFIGURED
            # end def device_predicate_true
            BaseTestCase._PREDICATE_CACHE[key] = device_predicate_true
        # end if
        return BaseTestCase._PREDICATE_CACHE[key]
    # end def create_device_predicate

    def create_device_handle(self):
        """
        Create device handle by calling getDevice with a predicate.

        :raise ``TestException``: If no device with the expected predicate is found or if it could not be allocated
        :raise ``AssertionError``: If the device manager was not found
        :raise ``RuntimeError``: If no hardware reset is possible
        """
        f = self.getFeatures()

        if f.PRODUCT.F_DeviceID == '':
            vendor_id_list = [None]
        else:
            vendor_id_list = f.PRODUCT.F_DeviceID.split(' ')
        # end if

        if f.PRODUCT.F_ProductID == '':
            product_id_list = [None]
        else:
            product_id_list = f.PRODUCT.F_ProductID.split(' ')
        # end if

        transport_id_list = f.PRODUCT.F_TransportID

        default_protocol = f.PRODUCT.PROTOCOLS.F_DefaultProtocol
        if default_protocol is not None:
            self.assertTrue(expr=default_protocol in LogitechProtocol,
                            msg=f"Unknown protocol {default_protocol}, it should be from the enum LogitechProtocol")

            default_protocol = LogitechProtocol(default_protocol)
        # end if

        self.device_ids = []

        for vendor_id in vendor_id_list:
            for product_id in product_id_list:
                for transport_id in transport_id_list:
                    # TODO Add unit ID maybe ?
                    self.device_ids.append(ChannelIdentifier(transport_id=transport_id,
                                                             vendor_id=vendor_id,
                                                             product_id=product_id,
                                                             protocol=default_protocol))
                # end for
            # end for
        # end for

        device_predicate = self.create_device_predicate(self.device_ids)

        # Get device handle
        try:
            self.device = self.getDevice(device_predicate, keepForTestduration=True)
        except TestException:
            if not ProtocolManagerUtils.is_corded_device_only(test_case=self):
                # Reset the device to re-establish the wireless connection with the receiver
                if self.power_supply_emulator is not None:
                    self.power_supply_emulator.restart_device()
                # end if
                # wake up the device
                if self.button_stimuli_emulator is not None:
                    self.button_stimuli_emulator.user_action()
                # end if
            # end if
            try:
                # Try once more to acquire the device
                self.device = self.getDevice(device_predicate, keepForTestduration=True)
            except TestException:
                raise TestException(TYPE_ERROR, """No Device available.
                    This is is usually due to one of the following:
                    1. The Config.ini file may be incorrect (check the TARGET section)
                    2. The Libusb.ini file may be incorrect (wrong bus/port combination)
                    3. The Dongle VendorId / ProductId is different than the predefined one
                    4. Zadig drivers not installed (check windows device manager)
                    5. The Device do not enumerate (check code execution)""")
            # end try
        # end try

        self.assertNotNone(obtained=self.device, msg="Device manager not found")
        self.assertTrue(expr=self.device.is_allocated(), msg="Device manager not allocated")

        DeviceManagerUtils.refresh_channel_cache(test_case=self)
        DeviceManagerUtils.log_all_channels_in_cache(test_case=self)

        self._log_channel_identifiers_to_get_current_channel()

        current_channels = DeviceManagerUtils.get_channels(test_case=self, channel_id=self.device_ids)
        self.assertNotEqual(unexpected=0, obtained=len(current_channels), msg='Current channel not found')

        if len(current_channels) > 1:
            self.log_warning(
                message=f"Found more than one channel matching the wanted configuration: {current_channels}\n"
                        f"The first one will be used",
                warning_level=WarningLevel.ROBUSTNESS)
        # end if

        first_channel_found = current_channels[0]

        if default_protocol is None:
            default_protocol = current_channels[0].protocol
        # end if

        self.assertTrue(expr=default_protocol > LogitechProtocol.UNKNOWN or default_protocol == LogitechProtocol.USB,
                        msg=f"Unsupported default protocol: {default_protocol}")
        if default_protocol > LogitechProtocol.UNKNOWN:
            wanted_channel = None
            for channel in current_channels:
                # The first port of the hub or the device outside hub is targeted
                if ChannelUtils.get_port_index(test_case=self, channel=channel) in [0, 1]:
                    wanted_channel = channel
                    break
                # end if
            # end for
        else:
            wanted_channel = first_channel_found
        # end if

        self.assertNotNone(obtained=wanted_channel,
                           msg=f"Could not find wanted channel with default protocol: {default_protocol}")

        retry_count = 0

        while retry_count < self.MAX_RESET_TRY:
            # noinspection PyBroadException
            try:
                if isinstance(wanted_channel, UsbChannel) and ChannelUtils.get_port_index(
                        test_case=self, channel=wanted_channel) == LibusbDriver.CHARGING_PORT_NUMBER:
                    self.device.enable_usb_port(LibusbDriver.CHARGING_PORT_NUMBER)
                elif isinstance(wanted_channel, ThroughReceiverChannel):
                    # The receiver channel has to be opened to avoid missing connection packets between checking the
                    # connection status and the wait for connection, if this part fails, it will be closed in the
                    # tear down
                    ChannelUtils.open_channel(test_case=self, channel=wanted_channel.receiver_channel)
                # end if

                # Get the cache connection state that should have been refreshed earlier in this method
                if not wanted_channel.is_device_connected(force_refresh_cache=False):
                    # If it is not connected in the cache, make sure that the cache is up-to-date as it could have
                    # been connected between the refresh and now
                    if wanted_channel.is_device_connected(force_refresh_cache=True):
                        # If this part is reached, it means it worked well and the retry loop can be stopped
                        break
                    # end if
                else:
                    # If this part is reached, it means it worked well and the retry loop can be stopped
                    break
                # end if

                # If the device is disconnected for sure, wait for the connection
                ChannelUtils.wait_for_channel_device_to_be_connected(
                    test_case=self, channel=wanted_channel, open_channel=False)
            except Exception as e:
                retry_count += 1
                if retry_count >= self.MAX_RESET_TRY:
                    # This permit to normally never need the end criteria of the retry loop but as a
                    # precaution it is still kept
                    raise TestException(TYPE_ERROR, f"No connection found after {retry_count - 1} resets") from e
                # end if

                self.log_traceback_as_warning(warning_level=WarningLevel.ROBUSTNESS,
                                              supplementary_message=f"No connection found after {retry_count} try(ies)")
                if self.is_hardware_reset_possible():
                    # Reset the device and try to reconnect
                    DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)
                    self._setup_hardware_reset_done = True
                else:
                    raise RuntimeError("No hardware reset possible") from e
                # end if

                continue
            # end try

            # If this part is reached, it means it worked well and the retry loop can be stopped
            break
        # end while

        if retry_count > 0:
            self.log_warning(message=f"Reset needed to find a connected channel: {retry_count} times",
                             warning_level=WarningLevel.ROBUSTNESS)
        # end if

        self.current_channel = wanted_channel
        # Configure current protocol in ConfigurationManager
        self.config_manager.current_protocol = self.current_channel.protocol

        self.backup_dut_channel = self.current_channel
        sys.stdout.write(f"\n\tBackup DUT channel: {self.backup_dut_channel}\n")

        ChannelUtils.open_channel(test_case=self)
    # end def create_device_handle

    def reset(self, task_bitmap=LinkEnablerInfo.ALL_MASK, hardware_reset=False, starting_voltage=None,
              recover_time_needed=True, verify_wireless_device_status_broadcast_event=True,
              verify_connection_reset=True, cleanup_battery_event=True, delay=0.0, *args, **kwargs):
        """
        Reset device connection.

        :param task_bitmap: Bitfield of active tasks - OPTIONAL
        :type task_bitmap: ``int``
        :param hardware_reset: Perform a hardware reset - OPTIONAL
        :type hardware_reset: ``bool``
        :param starting_voltage: Value of the hardware reset voltage - OPTIONAL
        :type starting_voltage: ``float`` or ``None``
        :param recover_time_needed: Does the device need some time to recover after its internal reset - OPTIONAL
        :type recover_time_needed: ``bool``
        :param verify_wireless_device_status_broadcast_event: For wireless devices, verify if after a hardware reset a
                                                              ``WirelessDeviceStatusBroadcastEvent`` is
                                                              received - OPTIONAL
        :type verify_wireless_device_status_broadcast_event: ``bool``
        :param verify_connection_reset: Flag indicating to verify that the connection reset even when
                                        ``hardware_reset`` is ``False`` - OPTIONAL
        :type verify_connection_reset: ``bool``
        :param cleanup_battery_event: Cleanup event message queue from Battery notifications - OPTIONAL
        :type cleanup_battery_event: ``bool``
        :param delay: Delay to wait for the device to reset in seconds - OPTIONAL
        :type delay: ``float``
        :param args: Potential argument of ``CommonBaseTestCase`` other child classes - OPTIONAL
        :type args: ``tuple``
        :param kwargs: Potential keyword argument of ``CommonBaseTestCase`` other child classes - OPTIONAL
        :type kwargs: ``dict``
        """
        reset_try_count = 0
        while reset_try_count < self.MAX_RESET_TRY:
            if self.current_channel.is_open:
                if hardware_reset:
                    # Empty message queue before power reset
                    ChannelUtils.empty_queues(test_case=self)
                # end if
                ChannelUtils.close_channel(test_case=self, close_associated_channel=False)
            # end if

            if isinstance(self.current_channel, ThroughReceiverChannel):
                self.current_channel.receiver_channel.enable_hidpp_reporting(enable=True)
            # end if

            if hardware_reset:
                if self.is_hardware_reset_possible():
                    if isinstance(self.current_channel, BleChannel) and self.current_channel.is_device_connected():
                        ChannelUtils.disconnect_ble_channel(test_case=self)
                    # end if

                    # Hardware reset
                    DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self, starting_voltage=starting_voltage,
                                                                   delay=delay)

                    if verify_connection_reset:
                        try:
                            CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                                test_case=self,
                                ble_service_changed_required=False,
                                link_enabler=BitStruct(Numeral(task_bitmap)),
                                wireless_broadcast_event_required=False)
                        except (AssertionError, Empty) as exception:
                            reset_try_count += 1
                            if reset_try_count < self.MAX_RESET_TRY:
                                continue
                            else:
                                exception_message = (f"Reset retry fails more than {self.MAX_RESET_TRY} times: "
                                                     f"{exception}")
                                raise TestException(TYPE_ERROR,
                                                    exception_message).with_traceback(sys.exc_info()[2]) from None
                                # end if
                            # end if
                        # end try
                    # end if
                else:
                    self.log_warning("Hardware reset needed but no Power Supply emulator available")
                # end if
            elif verify_connection_reset:
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=self,
                    ble_service_changed_required=False,
                    link_enabler=BitStruct(Numeral(task_bitmap)),
                    wireless_broadcast_event_required=False)
            # end if

            if not self.current_channel.is_open:
                ChannelUtils.open_channel(test_case=self, link_enabler=BitStruct(Numeral(task_bitmap)))
            # end if

            f = self.getFeatures()
            if f.PRODUCT.USB_COMMUNICATION.F_SetIdleSupported and \
                    isinstance(self.current_channel, (UsbChannel, ThroughReceiverChannel)):
                ChannelUtils.set_idle(test_case=self)
            # end if

            if hardware_reset or verify_connection_reset:
                if self.current_channel.protocol > LogitechProtocol.UNKNOWN:
                    if verify_wireless_device_status_broadcast_event:
                        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
                            test_case=self)

                        # Empty hid_message_queue from HidMouse and HidKeyboard notifications sent by the receiver
                        ChannelUtils.clean_messages(
                            test_case=self,
                            queue_name=HIDDispatcher.QueueName.HID,
                            class_type=(HidMouse, HidKeyboard))
                    elif recover_time_needed:
                        # Let some time for the device to recover after its internal reset
                        sleep(.5)
                    # end if
                # end if

                if cleanup_battery_event:
                    self.cleanup_battery_event_from_queue()
                # end if
            # end if

            break
        # end while

        if isinstance(self.current_channel, UsbReceiverChannel):
            self.current_channel.enable_hidpp_reporting(enable=True)
        # end if

        if reset_try_count > 0:
            self.log_warning(message=f"Retry reset needed: {reset_try_count} times",
                             warning_level=WarningLevel.ROBUSTNESS)
        # end if
    # end def reset

    def hardware_reset(self, starting_voltage=None):
        """
        DEPRECATED

        Perform a device hardware reset.
        This will NOT handle anything else (channel, connection events, ...) than the reset.

        :param starting_voltage: Value of the hardware reset voltage - OPTIONAL
        :type starting_voltage: ``float`` or ``None``
        """
        warnings.warn(
            'This function is deprecated, use DeviceBaseTestUtils.ResetHelper.hardware_reset instead',
            DeprecationWarning)

        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self, starting_voltage=starting_voltage)
    # end def hardware_reset

    def set_receiver_wireless_notification_and_wait_notification(self):
        """
        Set the Wireless Notification flag of the receiver (if on receiver) to the desired state.

        :raise ``TestException``: If no device is connected
        """
        if not isinstance(self.current_channel, ThroughReceiverChannel):
            return
        # end if

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        if not self.current_channel.is_device_connected(force_refresh_cache=True):
            raise TestException(TYPE_ERROR, "Device not connected")
        # end if
    # end def set_receiver_wireless_notification_and_wait_notification

    def channel_enable(self, usb_port_index, wait_time=2.0, wait_device_notification=True):
        """
        DEPRECATED

        Enable a USB port.

        :param usb_port_index: USB port to enable
        :type usb_port_index: ``int``
        :param wait_time: Time to let for the device to recover after its internal reset - OPTIONAL
        :type wait_time: ``float``
        :param wait_device_notification: Flag indicating if a Device Connection notification from device should be
                                         expected - OPTIONAL
        :type wait_device_notification: ``bool``
        """
        warnings.warn('This function is deprecated, Should not be used at all', DeprecationWarning)

        # Since this is a deprecated method called in a deprecated method, it is acceptable
        # noqa is used as there is no noinspection for it
        super().channel_enable(usb_port_index=usb_port_index, wait_time=wait_time)  # noqa

        # TODO : remove wait_device_notification parameter and
        #  set_receiver_wireless_notification_and_wait_notification call : it should be done out of this function
        if wait_device_notification:
            self.set_receiver_wireless_notification_and_wait_notification()
        # end if
    # end def channel_enable

    def is_device_corded_or_platform(self):
        """
        Check if the current device is a platform or a corded device.

        :return: Is the current device used a platform or a corded device
        :rtype: ``bool``
        """
        f = self.getFeatures()
        return self.current_channel.protocol == LogitechProtocol.USB or f.PRODUCT.F_IsPlatform
    # end def is_device_corded_or_platform

    def turn_off_corded_device_or_platform(self):
        """
        Turn off the current device only if it is a platform or a corded device.

        :raise ``AssertionError``: If the current device is not a platform nor a corded device.
        """
        assert self.is_device_corded_or_platform(), "Not a corded device nor a platform"

        ChannelUtils.close_channel(test_case=self)
        self.device.turn_off_usb_charging_cable()
        self.device_debugger.close()
    # end def turn_off_corded_device_or_platform

    def turn_on_corded_device_or_platform(self):
        """
        Turn on the current device only if it is a platform or a corded device.

        :raise ``AssertionError``: If the current device is not a platform nor a corded device.
        """
        assert self.is_device_corded_or_platform(), "Not a corded device nor a platform"

        self.device.turn_on_usb_charging_cable()
        sleep(1)
        self.device_debugger.open()
    # end def turn_on_corded_device_or_platform
# end class DeviceBaseTestCase


BaseTestCase = DeviceBaseTestCase


class ReceiverBaseTestCase(CommonBaseTestCase):
    """
    TestCase class for tests targeting receivers (USB dongle products).
    """

    @property
    def debugger(self):
        # See ``CommonBaseTestCase.debugger``
        return self.receiver_debugger
    # end def property getter debugger

    @property
    def memory_manager(self):
        # See ``CommonBaseTestCase.memory_manager``
        return self.receiver_memory_manager
    # end def property getter memory_manager

    @property
    def companion_debugger(self):
        # See ``CommonBaseTestCase.companion_debugger``
        return self.receiver_companion_debugger
    # end def property getter companion_debugger

    def setUp(self):
        """
        Creates the test context of selected plug-in.

        :raise ``ValueError``: If no known root version is given
        """

        # Inherited setup
        super().setUp()
        self.config_manager.current_target = ConfigurationManager.TARGET.RECEIVER

        # Debugger connection setup
        self.debuggers_setup()

        if (self.device_debugger is not None) or (self.receiver_debugger is not None):
            if self.id().split('.')[2] == 'connectionscheme':
                # Cleanup all pairing slots except the first one
                CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)
                self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                    self, self.device_memory_manager)
                sleep(.1)
            else:
                # Let some time for the receivers to be ready after the debugger reset
                sleep(1.2)
            # end if
        # end if

        root_version = self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
        if root_version is None:
            raise ValueError('Unknown Root feature version!')
        # end if

        if self.f.RECEIVER.F_Enabled:
            self.create_device_handle()
        # end if

        # Start test threaded executor
        if self.device is not None:
            self.current_channel.hid_dispatcher.add_feature_entry(Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)

            # Restart Task executor
            ChannelUtils.open_channel(test_case=self)

            if self.f.PRODUCT.USB_COMMUNICATION.F_SetIdleSupported:
                ChannelUtils.set_idle(test_case=self)
            # end if

            # Empty message queues
            ChannelUtils.empty_queues(test_case=self)

            ChannelUtils.set_hidpp_reporting(test_case=self)
        # end if
    # end def setUp

    @staticmethod
    def create_receiver_predicate(device_uid_list):
        """
        Create predicate with function parameters for USB Device.

        :param device_uid_list: List of the device unique identifier
        :type device_uid_list: ``list[ChannelIdentifier]``

        :return: The predicate created
        :rtype: ``callable type``
        """
        # create a hashable key
        key = str('_'.join(str(device_uid_list)))

        if key not in BaseTestCase._PREDICATE_CACHE:
            def receiver_predicate_true(device):
                """
                Predicate that returns ``True`` if matching USB device UID test, ``False`` otherwise

                :param device: USB Device instance
                :type device: ``LibusbDriver``

                :return: ``True`` is the LibusbDriver configure function was called successfully
                :rtype: ``bool``
                """
                return device.IS_CONFIGURED
            # end def receiver_predicate_true
            BaseTestCase._PREDICATE_CACHE[key] = receiver_predicate_true
        # end if
        return BaseTestCase._PREDICATE_CACHE[key]
    # end def create_receiver_predicate

    def create_device_handle(self):
        """
        Create receiver handle.

        :raise ``TestException``: If no device with the expected predicate is found or if it could not be allocated
        :raise ``AssertionError``: If the device manager was not found
        """
        f = self.getFeatures()

        if f.PRODUCT.F_DeviceID == '':
            vendor_id_list = [None]
        else:
            vendor_id_list = f.PRODUCT.F_DeviceID.split(' ')
        # end if

        if f.PRODUCT.F_ProductID == '':
            product_id_list = [None]
        else:
            product_id_list = f.PRODUCT.F_ProductID.split(' ')
        # end if

        transport_id_list = f.PRODUCT.F_TransportID

        # A non hub port or the first port of a hub are always targeted
        port_index_list = [LibusbDriver.NON_HUB_USB_PORT_INDEX, 1]

        self.device_ids = []

        for vendor_id in vendor_id_list:
            for product_id in product_id_list:
                for transport_id in transport_id_list:
                    for port_index in port_index_list:
                        # TODO Add unit ID maybe ?
                        self.device_ids.append(ChannelIdentifier(transport_id=transport_id,
                                                                 protocol=LogitechProtocol.USB,
                                                                 vendor_id=vendor_id,
                                                                 product_id=product_id,
                                                                 port_index=port_index))
                    # end for
                # end for
            # end for
        # end for

        target_predicate = self.create_receiver_predicate(self.device_ids)

        # Get device handle
        try:
            self.device = self.getDevice(target_predicate, keepForTestduration=True)
        except TestException:
            raise TestException(TYPE_ERROR, """No Receiver available.
            This is is usually due to one of the following:
            1. The Config.ini file may be incorrect (check the TARGET section)
            2. The Libusb.ini file may be incorrect (wrong bus/port combination)
            3. The Receiver VendorId / ProductId is different than the predefined one
            4. The Receiver do not enumerate (check code execution)""")
        # end try

        self.assertNotEqual(None, self.device, 'Device manager not found')
        self.assertTrue(self.device.is_allocated(), 'Device manager not allocated')

        DeviceManagerUtils.refresh_channel_cache(test_case=self)
        DeviceManagerUtils.log_all_channels_in_cache(test_case=self)

        self._log_channel_identifiers_to_get_current_channel()

        current_channel = DeviceManagerUtils.get_channel(
            test_case=self, channel_id=self.device_ids, check_connected=True)
        self.assertNotEqual(None, current_channel, 'Current channel not found')
        self.assertIsInstance(obj=current_channel, cls=UsbChannel, msg="Current channel is not on USB")

        self.current_channel = current_channel
        # Configure current protocol in ConfigurationManager
        self.config_manager.current_protocol = self.current_channel.protocol
        self.backup_dut_channel = self.current_channel
        sys.stdout.write(f"\n\tBackup DUT channel: {self.backup_dut_channel}\n")

        secondary_channels = DeviceManagerUtils.get_channels(
            test_case=self,
            channel_id=ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self)))
        for channel in secondary_channels:
            if isinstance(channel, ThroughReceiverChannel):
                self.backup_through_receiver_channel = channel
                break
            # end if
        # end for
        sys.stdout.write(f"\tBackup through receiver channel: {self.backup_through_receiver_channel}\n")
    # end def create_device_handle

    MAX_RESET_TRY = 3

    def reset(self, hardware_reset=False, recover_time_needed=False, verify_connection_reset=True, *args, **kwargs):
        """
        Reset Receiver connection

        :param hardware_reset: Perform a hardware reset - OPTIONAL
        :type hardware_reset: ``bool``
        :param recover_time_needed: Does the device need some time to recover after its internal reset - OPTIONAL
        :type recover_time_needed: ``bool``
        :param verify_connection_reset: Flag indicating to verify that the connection reset even when
                                        ``hardware_reset`` is ``False`` - OPTIONAL
        :type verify_connection_reset: ``bool``
        :param args: Potential argument of ``CommonBaseTestCase`` other child classes - OPTIONAL
        :type args: ``tuple``
        :param kwargs: Potential keyword argument of ``CommonBaseTestCase`` other child classes - OPTIONAL
        :type kwargs: ``dict``

        :raise ``Exception``: if the reset procedure could not be completed after 3 tries
        """
        reset_try_count = 0
        while reset_try_count < self.MAX_RESET_TRY:
            # noinspection PyBroadException
            try:
                # Stop Task executor
                ChannelUtils.close_channel(test_case=self)

                if hardware_reset:
                    ReceiverBaseTestUtils.ResetHelper.hardware_reset(self)

                    CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
                elif verify_connection_reset:
                    CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
                # end if

                if not self.current_channel.is_open:
                    ChannelUtils.open_channel(test_case=self)
                # end if

                f = self.getFeatures()
                if f.PRODUCT.USB_COMMUNICATION.F_SetIdleSupported:
                    ChannelUtils.set_idle(test_case=self)
                # end if
                break
            except Exception:
                reset_try_count += 1

                if reset_try_count >= self.MAX_RESET_TRY:
                    raise
                # end if
            # end try
        # end while

        if self.config_manager.current_mode == ConfigurationManager.MODE.APPLICATION:
            ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
        # end if

        if reset_try_count > 0:
            self.log_warning(message=f"Retry reset needed: {reset_try_count} times",
                             warning_level=WarningLevel.ROBUSTNESS)
        # end if
    # end def reset

    def hardware_reset(self):
        """
        DEPRECATED

        Perform a receiver hardware reset.
        This will NOT handle anything else (channel, connection events, ...) than the reset.
        """
        warnings.warn(
            'This function is deprecated, use ReceiverBaseTestUtils.ResetHelper.hardware_reset instead',
            DeprecationWarning)

        ReceiverBaseTestUtils.ResetHelper.hardware_reset(self)
    # end def hardware_reset
# end class ReceiverBaseTestCase

# ----------------------------------------------------------------------------------------------------------------------
# End of file
# ----------------------------------------------------------------------------------------------------------------------
