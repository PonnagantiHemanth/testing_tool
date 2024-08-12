#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.setup.setup
:brief: Initialisation of a CI setup
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/01/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join
from sys import stdout
from time import sleep

# noinspection PyUnresolvedReferences
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pysetup import PROJECT_PATH
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytransport.usb.usbconstants import LogitechReceiverProductId
from pytransport.usb.usbconstants import ProductId

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import CutOffControl
from pyhid.hidpp.features.common.batterylevelscalibration import CutOffControlResponse
from pyhid.hidpp.features.common.batterylevelscalibration import GetBattCalibrationInfo
from pyhid.hidpp.features.common.batterylevelscalibration import GetBattCalibrationInfoResponse
from pyhid.hidpp.features.common.batterylevelscalibration import MeasureBattery
from pyhid.hidpp.features.common.batterylevelscalibration import MeasureBatteryResponse
from pyhid.hidpp.features.common.batterylevelscalibration import ReadCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import ReadCalibrationResponse
from pyhid.hidpp.features.common.batterylevelscalibration import SetBatterySourceInfo
from pyhid.hidpp.features.common.batterylevelscalibration import SetBatterySourceInfoResponse
from pyhid.hidpp.features.common.batterylevelscalibration import StoreCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import StoreCalibrationResponse
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesFactory
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesFactory
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthFactory
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pylibrary.mcu.kbdmasktablechunk import KbdMaskTableChunk
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52MemoryManager
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurabledevicepropertiesutils import ConfigurableDevicePropertiesTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.opticalswitchesutils import OpticalSwitchesTestUtils
from pytestbox.device.base.tdeaccesstonvmutils import TdeAccessToNvmTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.equaddeviceconnectionutils import EQuadDeviceConnectionUtils
from pytestbox.shared.base.memoryutils import SharedMemoryTestUtils
from pyusb.libusbdriver import ChannelIdentifier
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SetupTestCase(ReceiverBaseTestCase):
    """
    CI node setup TestCases
    """
    UICR_AES_KEY_ADDRESS_BASE = 0x100010A0
    UICR_AES_KEY_SIZE = 0x10

    WAIT_ADC_STABLE_TIME = 6
    ADC_AVERAGE_COUNT = 10

    # Defined in application/led_rgb.c in the firmware code base
    DEFAULT_CALIBRATION_MAX = 0x55
    # Defined in application/led_rgb.h in the firmware code base
    RGB_LO_RED_ID_IN_CALIBRATION_FACT = 0x01
    RGB_LO_GREEN_ID_IN_CALIBRATION_FACT = 0x03
    RGB_LO_BLUE_ID_IN_CALIBRATION_FACT = 0x05

    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_cutoff = False

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn on first receiver only, turn all others off')
        # --------------------------------------------------------------------------------------------------------------
        if len(LibusbDriver.discover_usb_hub()) > 0:
            self.initial_ports_status = self.device.get_usb_ports_status()
            first_receiver = ChannelUtils.get_port_index(test_case=self)
            receivers_ports = []
            for pid in list(LogitechReceiverProductId) + [ProductId.LOGITECH_GOTTHARD_RECEIVER]:
                receivers_ports += ReceiverTestUtils.get_receiver_port_indexes(self, pid, skip=[first_receiver])
            # end for
            ports_status = {}
            for port_index, port_status in self.initial_ports_status.items():
                ports_status[port_index] = False if port_index in receivers_ports else port_status
            # end for
            assert ports_status[first_receiver] is True
            self.device.set_usb_ports_status(ports_status)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable HID notification')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(test_case=self)
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_cutoff and self.power_supply_emulator is not None:
                # Enable Manufacturing Features
                DeviceTestUtils.HIDppHelper.activate_features(
                    self, manufacturing=True, device_index=self.pairing_slot)
                # Post-requisite#1: Enable cutoff
                self._enable_cutoff()
            # end if

            if self.power_supply_emulator is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Turn off DUT')
                # ------------------------------------------------------------------------------------------------------
                self.power_supply_emulator.turn_off()
                self.power_supply_emulator.recharge(enable=False)
            # end if

            if self.power_slider_emulator is not None:
                # Turn the power slider off
                self.power_slider_emulator.power_off()
            # end if

            if self.initial_ports_status:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Turn back all ports to initial state')
                # ------------------------------------------------------------------------------------------------------
                self.device.set_usb_ports_status(self.initial_ports_status)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super().tearDown()
    # end def tearDown

    @features('BLEDevicePairing')
    @level('CiScript')
    @services('Debugger')
    def test_node_setup(self):
        """
        Pair the receiver with the connected device.

        Set up a CI node:
            * Update BLE context application (if power supply emulator is available)
            * Flash receiver (if receiver debugger is available)
            * Flash the device
            * Pair the receiver with the connected device.
            * Perform battery calibration (if a power supply emulator is available)
            * Configure properties
            * Disable Gotthard
            * Read and store NVS for both device and receiver
        """
        # Update BLE context hardware to match wanted one
        self.update_ble_context_hardware()

        # Initialize Bluetooth address test parameter
        self.bluetooth_address = HexList("00" * 6)
        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        # Set up the connection key ids
        self.button_stimuli_emulator.setup_connected_key_ids()

        # Program the receiver firmware
        self._flash_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Program device firmware')
        # --------------------------------------------------------------------------------------------------------------
        device_firmware_hex_file = join(TESTS_PATH, "DFU_FILES", self.f.SHARED.DEVICES.F_DeviceHexFile)
        self.device_debugger.erase_and_flash_firmware(device_firmware_hex_file)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Clean all receiver pairing slot')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            class_type=SetPerformDeviceConnectionResponse)
        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            class_type=Hidpp1ErrorCodes)
        DevicePairingTestUtils.unpair_all(self, first_slot=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        # Empty pairing status message queue
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=PairingStatus)
        try:
            bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        except AssertionError:  # Queue still empty after 2 seconds
            stdout.write(f"Error during the discovery process. Press the button to enter pairing mode")
            bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=True)
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        self.pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address)
        self.assertEqual(obtained=self.pairing_slot, expected=1,
                         msg='Receiver pairing slot 1 should be used')
        self.current_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
            port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.pairing_slot))
        ChannelUtils.open_channel(test_case=self)
        root_version = self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
        self.current_channel.hid_dispatcher.add_feature_entry(Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Manufacturing Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True, device_index=self.pairing_slot)

        common_config = self.f.PRODUCT.FEATURES.COMMON
        if common_config.BATTERY_LEVELS_CALIBRATION.F_Enabled:
            if common_config.BATTERY_LEVELS_CALIBRATION.F_Version_1 and \
                    len(common_config.UNIFIED_BATTERY.F_CapabilitiesFlags) > UnifiedBattery.Flags.BATTERY_SOURCE_INDEX \
                    and common_config.UNIFIED_BATTERY.F_CapabilitiesFlags[UnifiedBattery.Flags.BATTERY_SOURCE_INDEX]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Set battery source index')
                # ------------------------------------------------------------------------------------------------------
                self._set_battery_source_index(self.pairing_slot)
            # end if

            if self.power_supply_emulator is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Battery calibration')
                # ------------------------------------------------------------------------------------------------------
                self._make_battery_calibration(self.pairing_slot)
            # end if
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Properties configuration')
        # --------------------------------------------------------------------------------------------------------------
        self._configure_properties()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable Gotthard feature')
        # --------------------------------------------------------------------------------------------------------------
        man_deact_feat_params = DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_parameters(
            self, ManageDeactivatableFeaturesAuth.FEATURE_ID, ManageDeactivatableFeaturesAuthFactory)
        manage_deactivatable_feature_index = man_deact_feat_params[0]
        manage_deactivatable_features = man_deact_feat_params[1]
        disable_features_req = manage_deactivatable_features.disable_features_cls(
            self.pairing_slot, manage_deactivatable_feature_index, disable_gothard=True)
        ChannelUtils.send(
            test_case=self, report=disable_features_req, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=manage_deactivatable_features.disable_features_response_cls)

        if common_config.BATTERY_LEVELS_CALIBRATION.F_Enabled and self.power_supply_emulator is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Increase the last voltage value by 100mV to be above the cut-off value')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage + 0.1)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Re-enable cutoff')
            # ------------------------------------------------------------------------------------------------------
            self._enable_cutoff()
        # end if

        # --------------------------------------------------------------------------------------------------------------
        # noinspection DuplicatedCode
        LogHelper.log_post_requisite(
            self, 'Create nvs files for both device and receiver targets (if debuggers are available)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)

        self._create_nvs_files()

        if self.receiver_debugger is not None:
            self.receiver_debugger.reset()
            sleep(5)
        else:
            ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
            ReceiverTestUtils.reset_receiver(self, skip_link_established_verification=True)
        # end if

        if self.device_debugger is not None:
            self.device_debugger.reset()
            sleep(5)
        # end if

        LibusbDriver.generate_usb_config_file()

        self.current_channel = self.backup_dut_channel
        ChannelUtils.open_channel(test_case=self)

        self.testCaseChecked("STP_CI_0001")
    # end def test_node_setup

    @features('NoBLEDevicePairing')
    @features('Unifying')
    @level('CiScript')
    @services('Debugger')
    def test_node_setup_unifying(self):
        """
        Set up a node with a Unifying connection

        Set up a CI node:
            * Update BLE context application (if power supply emulator is available)
            * Flash receiver (if receiver debugger is available)
            * Flash the device
            * Pair the receiver with the connected device.
            * Perform battery calibration (if a power supply emulator is available)
            * Configure properties
            * Disable Gotthard
            * Read and store NVS for both device and receiver
        """
        # Update BLE context hardware to match wanted one
        self.update_ble_context_hardware()

        # Set up the connection key ids
        self.button_stimuli_emulator.setup_connected_key_ids()

        # Program the receiver firmware
        self._flash_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Program device firmware')
        # --------------------------------------------------------------------------------------------------------------
        device_firmware_hex_file = join(TESTS_PATH, "DFU_FILES", self.f.SHARED.DEVICES.F_DeviceHexFile)
        LogHelper.log_info(self, f"Device firmware file: {device_firmware_hex_file}")
        self.device_debugger.erase_and_flash_firmware(device_firmware_hex_file)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Reset device after programming firmware')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        if self.f.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES.F_Enabled:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Write Keyboard Mask Table to enable full key matrix')
            # ----------------------------------------------------------------------------------------------------------
            kbd_mask_tables = self.config_manager.get_feature(
                feature_id=ConfigurationManager.ID.OPTICAL_SWITCHES_KBD_MASK_TABLE)
            default_key_layout_index = self.f.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES.F_DefaultKeyLayout
            default_mask_table = KbdMaskTableChunk(kbd_mask_tables[default_key_layout_index])
            OpticalSwitchesTestUtils.NvsHelper.add_kbd_mask_table(test_case=self,
                                                                  kbd_mask_table=HexList(default_mask_table),
                                                                  no_reset=True)
        # end if

        if self.f.PRODUCT.FEATURES.COMMON.TDE_ACCESS_TO_NVM.F_Enabled:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Disable power on pairing and enable LED driver')
            # ----------------------------------------------------------------------------------------------------------
            TdeAccessToNvmTestUtils.NvsHelper.write_tde_chunk(
                test_case=self,
                data=HexList([0] * (self.f.PRODUCT.FEATURES.COMMON.TDE_ACCESS_TO_NVM.F_TdeMaxSize - 1) + [0xAA]),
                no_reset=True)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Perform new device connection and pre-pairing')
        # --------------------------------------------------------------------------------------------------------------
        device_channel = EQuadDeviceConnectionUtils.new_device_connection_and_pre_pairing(
            test_case=self, unit_ids=self.f.SHARED.DEVICES.F_UnitIds_1, disconnect=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Manufacturing Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True, device_index=self.pairing_slot)

        common_config = self.f.PRODUCT.FEATURES.COMMON
        if common_config.BATTERY_LEVELS_CALIBRATION.F_Enabled:
            if common_config.BATTERY_LEVELS_CALIBRATION.F_Version_1 and \
                    len(common_config.UNIFIED_BATTERY.F_CapabilitiesFlags) > UnifiedBattery.Flags.BATTERY_SOURCE_INDEX \
                    and common_config.UNIFIED_BATTERY.F_CapabilitiesFlags[UnifiedBattery.Flags.BATTERY_SOURCE_INDEX]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Set battery source index')
                # ------------------------------------------------------------------------------------------------------
                self._set_battery_source_index(device_index=self.pairing_slot)
            # end if

            if self.power_supply_emulator is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Battery calibration')
                # ------------------------------------------------------------------------------------------------------
                self._make_battery_calibration(device_index=self.pairing_slot)
            # end if
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Properties configuration')
        # --------------------------------------------------------------------------------------------------------------
        self._configure_properties()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'configure report rates using x8100')
        self._configure_report_rate()

        man_deact_feat_params = DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_parameters(
            self, ManageDeactivatableFeaturesAuth.FEATURE_ID, ManageDeactivatableFeaturesAuthFactory,
            skip_not_found=True)
        manage_deactivatable_feature_index = man_deact_feat_params[0]
        manage_deactivatable_features = man_deact_feat_params[1]
        if manage_deactivatable_feature_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Disable Gotthard feature')
            # ----------------------------------------------------------------------------------------------------------
            disable_features_req = manage_deactivatable_features.disable_features_cls(
                self.pairing_slot, manage_deactivatable_feature_index, disable_gothard=True)
            ChannelUtils.send(
                test_case=self, report=disable_features_req, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=manage_deactivatable_features.disable_features_response_cls)
        # end if

        if common_config.BATTERY_LEVELS_CALIBRATION.F_Enabled and self.power_supply_emulator is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Increase the last voltage value by 100mV to be above the cut-off value')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage + 0.1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Re-enable cutoff')
            # ----------------------------------------------------------------------------------------------------------
            self._enable_cutoff()
        # end if

        # --------------------------------------------------------------------------------------------------------------
        # noinspection DuplicatedCode
        LogHelper.log_post_requisite(
            self, 'Create nvs files for both device and receiver targets (if debuggers are available)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)

        self._create_nvs_files()

        if self.receiver_debugger is not None:
            self.receiver_debugger.reset()
            sleep(5)
        else:
            ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
            ReceiverTestUtils.reset_receiver(self, skip_link_established_verification=True)
        # end if

        if self.device_debugger is not None:
            self.device_debugger.reset()
            sleep(5)
        # end if

        LibusbDriver.generate_usb_config_file()

        self.current_channel = self.backup_dut_channel
        DeviceManagerUtils.set_channel(test_case=self, new_channel=device_channel)

        self.testCaseChecked("STP_CI_0002")
    # end def test_node_setup_unifying

    def _enable_cutoff(self):
        """
        Post-requisite#1: Enable cutoff
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, 'Enable cutoff')
        # --------------------------------------------------------------------------------------------------------------
        cutoff_control = CutOffControl(device_index=self.pairing_slot,
                                       feature_index=self.battery_calibration_feature_id,
                                       cutoff_change_state_requested=True,
                                       cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_ENABLE)
        ChannelUtils.send(
            test_case=self, report=cutoff_control, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=CutOffControlResponse)
        self.post_requisite_cutoff = False
    # end def _enable_cutoff

    def _create_nvs_files(self):
        """
        Create nvs files for both device and receiver targets if debuggers are available
        """
        if self.receiver_debugger is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Create NVS file for receiver")
            # ----------------------------------------------------------------------------------------------------------
            self._create_nvs_file(
                self.receiver_memory_manager,
                join(TESTS_PATH, "DFU_FILES", 'nvs_uicr_' + self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName))
        # end if

        if self.device_debugger is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Create NVS file for device")
            # ----------------------------------------------------------------------------------------------------------
            self._create_nvs_file(self.device_memory_manager,
                                  join(TESTS_PATH, "DFU_FILES", 'nvs_uicr_' + self.f.SHARED.DEVICES.F_DeviceHexFile))
        # end if
    # end def _create_nvs_files

    def _create_nvs_file(self, memory_manager, nvs_file_name):
        """
        Create nvs file corresponding to a memory manager

        :param memory_manager: Memory manager
        :type memory_manager: ``MemoryManager``
        :param nvs_file_name: NVS filename
        :type nvs_file_name: ``str``
        """
        memory_manager.read_nvs()
        hex_file = memory_manager.nvs_parser.to_hex_file()

        if isinstance(memory_manager, Nrf52MemoryManager):
            uicr_addresses = range(SetupTestCase.UICR_AES_KEY_ADDRESS_BASE,
                                   SetupTestCase.UICR_AES_KEY_ADDRESS_BASE + SetupTestCase.UICR_AES_KEY_SIZE)
            memory_manager.debugger.stop()
            memory_manager.debugger.exclude_flash_cache_range(
                SetupTestCase.UICR_AES_KEY_ADDRESS_BASE,
                SetupTestCase.UICR_AES_KEY_ADDRESS_BASE + SetupTestCase.UICR_AES_KEY_SIZE)
            memory_manager.debugger.reset()
            uicr_data = memory_manager.debugger.readMemory(SetupTestCase.UICR_AES_KEY_ADDRESS_BASE,
                                                           SetupTestCase.UICR_AES_KEY_SIZE)
            hex_uicr_data = dict(zip(uicr_addresses, uicr_data))
            hex_file.fromdict(hex_uicr_data)
        # end if
        hex_file.tofile(nvs_file_name, format='hex')
        SharedMemoryTestUtils.StackHelper.restore_cache_settings(test_case=self, debugger=memory_manager.debugger)
    # end def _create_nvs_file

    @staticmethod
    def _measure_and_average_adc_value(test_case, voltage):
        """
        Measure the voltage to ADC value by HID++ Feature x1861 then return the average ADC value

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param voltage: The output voltage to DUT
        :type voltage: ``float``

        :return: The average ADC value
        :rtype: ``int``
        """
        sum_adc = 0
        for _ in range(SetupTestCase.ADC_AVERAGE_COUNT):
            test_case.power_supply_emulator.set_voltage(voltage)
            sleep(SetupTestCase.WAIT_ADC_STABLE_TIME)
            measure_battery = MeasureBattery(device_index=test_case.pairing_slot,
                                             feature_index=test_case.battery_calibration_feature_id)
            measure_battery_response = test_case.send_report_wait_response(
                report=measure_battery,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=MeasureBatteryResponse)
            sum_adc += int(Numeral(measure_battery_response.measure))
        # end for
        return round(sum_adc / SetupTestCase.ADC_AVERAGE_COUNT)
    # end def _measure_and_average_adc_value

    def _set_battery_source_index(self, device_index):
        if self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_BatterySourceIndex == 0:
            raise ValueError("Unable to set battery source to 0, please ensure the setting is correct.")
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature(0x1861)')
        # --------------------------------------------------------------------------------------------------------------
        self.battery_calibration_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=BatteryLevelsCalibration.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetBatterySourceInfo request')
        # --------------------------------------------------------------------------------------------------------------
        set_battery_source_info = SetBatterySourceInfo(
            device_index=device_index,
            feature_index=self.battery_calibration_feature_id,
            battery_source_index=self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_BatterySourceIndex)
        set_battery_source_info_response = ChannelUtils.send(
            test_case=self, report=set_battery_source_info, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=SetBatterySourceInfoResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetBatterySourceInfoResponse.battery_source_index')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=set_battery_source_info.battery_source_index,
                         obtained=set_battery_source_info_response.battery_source_index,
                         msg='The battery source index parameter differs from the one expected')
    # end def _set_battery_source_index

    def _make_battery_calibration(self, device_index):
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature(0x1861)')
        # --------------------------------------------------------------------------------------------------------------
        self.battery_calibration_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=BatteryLevelsCalibration.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable cutoff')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_cutoff = True

        cutoff_control = CutOffControl(device_index=device_index,
                                       feature_index=self.battery_calibration_feature_id,
                                       cutoff_change_state_requested=True,
                                       cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE)
        ChannelUtils.send(
            test_case=self, report=cutoff_control, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=CutOffControlResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetBattCalibrationInfo')
        # --------------------------------------------------------------------------------------------------------------
        get_batt_calibration_info = GetBattCalibrationInfo(device_index=device_index,
                                                           feature_index=self.battery_calibration_feature_id)
        get_batt_calibration_info_response = ChannelUtils.send(
            test_case=self, report=get_batt_calibration_info, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=GetBattCalibrationInfoResponse)

        precision_to_10_mv = PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1
        calibration_points_list = [
            round(to_int(get_batt_calibration_info_response.calibration_point_0) / 1000, precision_to_10_mv),
            round(to_int(get_batt_calibration_info_response.calibration_point_1) / 1000, precision_to_10_mv),
            round(to_int(get_batt_calibration_info_response.calibration_point_2) / 1000, precision_to_10_mv),
            round(to_int(get_batt_calibration_info_response.calibration_point_3) / 1000, precision_to_10_mv),
            round(to_int(get_batt_calibration_info_response.calibration_point_4) / 1000, precision_to_10_mv),
            round(to_int(get_batt_calibration_info_response.calibration_point_5) / 1000, precision_to_10_mv),
            round(to_int(get_batt_calibration_info_response.calibration_point_6) / 1000, precision_to_10_mv)]

        calibration_points_list_to_store = [0] * 7

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery voltage values from full to cut-off voltage')
        # --------------------------------------------------------------------------------------------------------------
        """
        nRF52832 Power Reset
        A step increase in supply voltage of 300 mV or more, with rise time of 300 ms or less, within the valid
        supply range, may result in a system reset.

        So the testing voltage values cannot be [cut-off, full]. Shall reverse it to [full, cut-off] to avoid
        trigger MCU power reset mechanism.

        Reference: nRF52832 datasheet "nRF52832_PS_v1.0", page 80 for more details.
        """
        calibration_points_reverse_sorted_list = calibration_points_list.copy()
        calibration_points_reverse_sorted_list.sort(reverse=True)
        for i in range(to_int(get_batt_calibration_info_response.calibration_points_nb)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send MeasureBattery by tuning the voltage to the requested '
                                     f'calibration point {calibration_points_list[i]}V')
            # ----------------------------------------------------------------------------------------------------------
            index = calibration_points_list.index(calibration_points_reverse_sorted_list[i])
            calibration_points_list_to_store[index] = \
                self._measure_and_average_adc_value(self, calibration_points_reverse_sorted_list[i])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send StoreCalibration with the value gotten from MeasureBattery')
        # --------------------------------------------------------------------------------------------------------------
        store_calibration = StoreCalibration(
            device_index=device_index,
            feature_index=self.battery_calibration_feature_id,
            calibration_points_nb=get_batt_calibration_info_response.calibration_points_nb,
            calibration_point_0=calibration_points_list_to_store[0],
            calibration_point_1=calibration_points_list_to_store[1],
            calibration_point_2=calibration_points_list_to_store[2],
            calibration_point_3=calibration_points_list_to_store[3],
            calibration_point_4=calibration_points_list_to_store[4],
            calibration_point_5=calibration_points_list_to_store[5],
            calibration_point_6=calibration_points_list_to_store[6])
        ChannelUtils.send(
            test_case=self, report=store_calibration, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=StoreCalibrationResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send ReadCalibration')
        # --------------------------------------------------------------------------------------------------------------
        read_calibration = ReadCalibration(device_index=device_index,
                                           feature_index=self.battery_calibration_feature_id)
        read_calibration_response = ChannelUtils.send(
            test_case=self, report=read_calibration, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=ReadCalibrationResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate ReadCalibration.measuresNB')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=get_batt_calibration_info_response.calibration_points_nb,
                         obtained=read_calibration_response.calibration_points_nb,
                         msg='The measuresNB parameter differs from the one expected')
    # end def _make_battery_calibration

    def _configure_properties(self):
        """
        Write required configurable properties using either 0x1807 or 0x1806 feature
        """
        try:
            feature_1807_index, _, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
                test_case=self, feature_id=ConfigurableProperties.FEATURE_ID, factory=ConfigurablePropertiesFactory,
                skip_not_found=True)
        except KeyError as err:
            stdout.write(f"Error while fetching feature 0x1807: {err}. Skip properties configuration.")
            return
        # end try
        if feature_1807_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Properties initialization using 0x1807")
            # ----------------------------------------------------------------------------------------------------------
            self._configure_properties_1807()
        else:
            feature_1806_index, _, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
                test_case=self, feature_id=ConfigurableDeviceProperties.FEATURE_ID,
                factory=ConfigurableDevicePropertiesFactory, skip_not_found=True)
            if feature_1806_index != Root.FEATURE_NOT_FOUND:
                self._configure_properties_1806()
            # end if
        # end if
    # end def _configure_properties

    def _configure_properties_1807(self):
        """
        Write required configurable properties using 0x1807 feature
        """
        for property_id in (ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0,
                            ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1,
                            ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2,
                            ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE3,
                            ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE4):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Get property {repr(property_id)} info")
            # ----------------------------------------------------------------------------------------------------------
            get_property_info_response = ConfigurablePropertiesTestUtils.HIDppHelper.get_property_info(
                self, property_id)

            if get_property_info_response.flags.supported:
                property_size = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(self, property_id)
                if property_id in [ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0,
                                   ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1,
                                   ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2,
                                   ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE3,
                                   ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE4]:
                    property_value = HexList("00" * property_size)
                    property_value[self.RGB_LO_RED_ID_IN_CALIBRATION_FACT] = self.DEFAULT_CALIBRATION_MAX
                    property_value[self.RGB_LO_GREEN_ID_IN_CALIBRATION_FACT] = self.DEFAULT_CALIBRATION_MAX
                    property_value[self.RGB_LO_BLUE_ID_IN_CALIBRATION_FACT] = self.DEFAULT_CALIBRATION_MAX
                else:
                    property_value = RandHexList(size=property_size)
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Select property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Write property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                # noinspection DuplicatedCode
                ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, property_value)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Re-Select property {repr(property_id)} at offset 0")
                # ------------------------------------------------------------------------------------------------------
                ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Read property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                read_data = ConfigurablePropertiesTestUtils.HIDppHelper.read_data(self,
                                                                                  data_size=len(property_value))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check property {repr(property_id)} data")
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(property_value, read_data, "Read data should match the written data")
            # end if
        # end for
    # end def _configure_properties_1807

    def _configure_properties_1806(self):
        """
        Write required configurable properties using 0x1806 feature
        """
        for property_id in (ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE0,
                            ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE1,
                            ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE2,):
            if str(property_id) in self.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_PROPERTIES.F_SupportedPropertyIds:
                if property_id in (
                        ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE0,
                        ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE1,
                        ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE2, ):
                    size = 14
                    data_calibration = HexList("00" * size)
                    data_calibration[self.RGB_LO_RED_ID_IN_CALIBRATION_FACT] = self.DEFAULT_CALIBRATION_MAX
                    data_calibration[self.RGB_LO_GREEN_ID_IN_CALIBRATION_FACT] = self.DEFAULT_CALIBRATION_MAX
                    data_calibration[self.RGB_LO_BLUE_ID_IN_CALIBRATION_FACT] = self.DEFAULT_CALIBRATION_MAX
                    ConfigurableDevicePropertiesTestUtils.SetDevicePropertiesHelper.HIDppHelper.write(
                        self,
                        property_id=property_id,
                        flag=1,
                        sub_data_index=0x02,
                        property_data=data_calibration)
                else:
                    size = 14
                    data_calibration = RandHexList(size=size)
                    ConfigurableDevicePropertiesTestUtils.SetDevicePropertiesHelper.HIDppHelper.write(
                        self,
                        property_id=property_id,
                        flag=0,
                        sub_data_index=0x00,
                        property_data=data_calibration)
                # end if
            # end if
        # end for
    # end def _configure_properties_1806

    def _configure_report_rate(self):
        """
        Change x8061 report rate using x8100 onboard profile
        if the report rate wireless or wired is configured in the test configuration file.
        """
        modifier = {}

        report_rate_wireless = self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ConfigureReportRateWireless
        if report_rate_wireless is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Set report rate wireless to the index {report_rate_wireless}')
            # ----------------------------------------------------------------------------------------------------------
            modifier['report_rate_wireless'] = report_rate_wireless
        # end if

        report_rate_wired = self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ConfigureReportRateWired
        if report_rate_wired is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Set report rate wired to the index {report_rate_wired}')
            # ----------------------------------------------------------------------------------------------------------
            modifier['report_rate_wired'] = report_rate_wired
        # end if

        if len(modifier) > 0:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Create default profiles and set active profile to the profile 1')
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.Profile.create_default_profiles(test_case=self, modifier=modifier)
            OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
            OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self,
                                                                    profile_id=OnboardProfiles.SectorId.PROFILE_START)
            profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self,
                                                                    profile_id=OnboardProfiles.SectorId.PROFILE_START)
            checker = OnboardProfilesTestUtils.ProfileChecker
            if report_rate_wireless is not None:
                checker.check_report_rate_wireless(test_case=self, response=profile, expected=report_rate_wireless)
            # end if
            if report_rate_wired is not None:
                checker.check_report_rate_wired(test_case=self, response=profile, expected=report_rate_wired)
            # end if
        # end if
    # end def _configure_report_rate

    def _flash_receiver(self):
        """
        Program receiver firmware
        """
        ChannelUtils.close_channel(self)
        if self.companion_debugger and self.receiver_debugger:
            receiver_companion_fw_hex_file = join(
                TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHexFileName)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Program receiver companion firmware')
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Receiver companion firmware file: {receiver_companion_fw_hex_file}")
            self.receiver_companion_debugger.stop()
            self.receiver_debugger.stop()
            self.receiver_companion_debugger.erase_and_flash_firmware(
                firmware_hex_file=receiver_companion_fw_hex_file, no_reset=True)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Program receiver firmware')
            # ----------------------------------------------------------------------------------------------------------
            receiver_firmware_hex_file = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)
            LogHelper.log_info(self, f"Receiver firmware file: {receiver_firmware_hex_file}")
            self.receiver_debugger.erase_and_flash_firmware(receiver_firmware_hex_file, no_reset=True)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Reset receiver')
            # ----------------------------------------------------------------------------------------------------------
            self.receiver_debugger.reset()
            self.receiver_companion_debugger.reset()
        elif self.receiver_debugger is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Program receiver firmware')
            # ----------------------------------------------------------------------------------------------------------
            receiver_firmware_hex_file = join(TESTS_PATH, "DFU_FILES",
                                              self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)
            LogHelper.log_info(self, f"Receiver firmware file: {receiver_firmware_hex_file}")
            self.receiver_debugger.erase_and_flash_firmware(receiver_firmware_hex_file)
        else:
            LogHelper.log_info(self, "Receiver can not be programmed")
        # end if
        sleep(5.0)
        ChannelUtils.open_channel(test_case=self)

        if self.f.PRODUCT.USB_COMMUNICATION.F_SetIdleSupported:
            ChannelUtils.set_idle(test_case=self)
        # end if

        # Empty message queues
        ChannelUtils.empty_queues(test_case=self)

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
    # end def _flash_receiver
# end class SetupTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
