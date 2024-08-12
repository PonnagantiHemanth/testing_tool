#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hidpp20.common.feature_00D0_business
:brief: Shared HID++ 2.0 Common feature 0x00D0
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2020/03/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from os.path import join
from time import perf_counter_ns
from time import sleep

from pychannel.blechannel import BleChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.securedfucontrol import GetDfuControlResponseV0
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pylibrary.emulator.ledid import LED_ID
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.bootloadertest import CommonBootloaderTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.dfuprocessing import CommonDfuTestCase
from pytestbox.base.ledspyhelper import LedSpyHelper
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class GenericDfuTestCaseBusiness(CommonDfuTestCase, ABC):
    """
    Generic class for the validation of DFU Business TestCases
    """
    FIVE_SECONDS = 5
    DFU_APP = 'application'
    DFU_IMAGE = 'images'

    def generic_complete_dfu_business(self, encrypt_algorithm=None, dfu=DFU_APP):
        """
        Validate the DFU business case targeting the application entity. This is a generic method used by subclasses.

        :param encrypt_algorithm: The encryption algorithm to use in Dfu.EncryptionMode, if ``None`` no encryption
                                  will be done - OPTIONAL
        :type encrypt_algorithm: ``int``
        :param dfu: APP or Image DFU to perform, default is App DFU - OPTIONAL
        :type dfu: ``str``
        """
        f = self.getFeatures()
        dfu_file_name = f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName \
            if dfu == self.DFU_APP else f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesDfuFileName

        self.perform_dfu(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", dfu_file_name),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1,
            log_check=1,
            encrypt_algorithm=encrypt_algorithm)
    # end def generic_complete_dfu_business

    def generic_change_action_type_by_dfu(self):
        """
        Check if action type to enter in bootloader can be changed by DFU. This is a generic method used by subclasses.

        JIRA: https://jira.logitech.io/browse/NRF52-121
        """
        f = self.getFeatures()
        action_type = int(f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_ReloadActionTypes[0])
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Perform DFU with application action type = {action_type}')
        # ---------------------------------------------------------------------------
        dfu_file = join(TESTS_PATH,
                        "DFU_FILES",
                        f"{f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName[:-4]}_action_type_app_{action_type}.dfu")
        LogHelper.log_info(self, f'DFU file: {dfu_file}')
        self.perform_dfu(dfu_file_path=dfu_file, bootloader_dfu_feature_id=self.bootloader_dfu_feature_id)
        self.post_requisite_program_mcu_initial_state = True

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # ---------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check enableDfu=0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check dfu_control_action_type={action_type}')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=action_type,
                         obtained=to_int(get_dfu_control_response.dfu_control_action_type),
                         msg='The enable_dfu parameter differs from the expected one')

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self,
                                            action_type=get_dfu_control_response.dfu_control_action_type)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform new action type to enter DFU')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self, action_type=action_type)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target is in Bootloader mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
            msg="Target not in bootloader")

        action_type = int(f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType)
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Perform DFU with default application action type (i.e. {action_type})')
        # ---------------------------------------------------------------------------
        dfu_file = join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)
        LogHelper.log_info(self, f'DFU file: {dfu_file}')
        self.perform_dfu(dfu_file_path=dfu_file, bootloader_dfu_feature_id=self.bootloader_dfu_feature_id)
        self.post_requisite_program_mcu_initial_state = True

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # ---------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check enableDfu=0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check dfu_control_action_type={action_type}')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=action_type,
                         obtained=to_int(get_dfu_control_response.dfu_control_action_type),
                         msg='The enable_dfu parameter differs from the expected one')

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self,
                                            action_type=get_dfu_control_response.dfu_control_action_type)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform default action type to enter DFU')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self, action_type=action_type)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target is in Bootloader mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
            msg="Target not in bootloader")
    # end def generic_change_action_type_by_dfu

    def generic_soft_device_dfu_business(self):
        """
        Validate the DFU business case targeting the softdevice entity. This is a generic method used by subclasses.
        """
        f = self.getFeatures()

        # Soft device DFU processing
        self.bootloader_dfu_processing(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1, log_check=1, restart_all=False, is_ble_service_changed_required=False)

        self.reset(hardware_reset=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 10: Send Root.GetFeature(0x0003)')
        self.logTitle2('Test Check 10: Device shall be in Bootloader mode')
        # ---------------------------------------------------------------------------
        DeviceInformationTestUtils.check_active_entity_type(
            test_case=self,
            device_index=ChannelUtils.get_device_index(test_case=self),
            entity_type=DeviceInformation.EntityTypeV1.BOOTLOADER)

        self.perform_dfu(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=11,
            log_check=11)
    # end def generic_soft_device_dfu_business

    def generic_companion_dfu_business(self):
        """
        Validate the DFU business case targeting the companion entity. This is a generic method used by subclasses.
        """
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform DFU for the companion application entity')
        # --------------------------------------------------------------------------------------------------------------
        self.bootloader_dfu_processing(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1,
            log_check=1)
    # end def generic_companion_dfu_business

    def generic_check_led_behaviour_on_dfu(self):
        """
        Check the Battery and Connectivity LEDs behaviour during DFU for PWS devices
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start Battery and Connectivity LEDs Monitoring")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.start_monitoring(
            self, [LED_ID.DEVICE_STATUS_GREEN_LED, LED_ID.DEVICE_STATUS_RED_LED, LED_ID.CONNECTIVITY_STATUS_LED_1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Do Dfu on DUT")
        # --------------------------------------------------------------------------------------------------------------
        start_time = perf_counter_ns()
        self.generic_complete_dfu_business()
        dfu_time_duration_ms = round((perf_counter_ns() - start_time) / 1_000_000)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Wait for 5 seconds to record Battery and Connectivity LED behaviour after Dfu")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop the LEDs Monitoring")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.stop_monitoring(
            self, [LED_ID.DEVICE_STATUS_GREEN_LED, LED_ID.DEVICE_STATUS_RED_LED, LED_ID.CONNECTIVITY_STATUS_LED_1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check Battery Green LED and Battery Red LED was in slow blinking state with "
                                 "time period = 500 ms")
        # --------------------------------------------------------------------------------------------------------------
        for led in [LED_ID.DEVICE_STATUS_GREEN_LED, LED_ID.DEVICE_STATUS_RED_LED]:
            LedSpyHelper.check_effect_duration(
                self, led, SchemeType.SLOW_BLINKING, minimum_duration=dfu_time_duration_ms,
                position=LedSpyHelper.POSITION.FIRST, reset=True)
        # end for

        if self.config_manager.current_protocol == LogitechProtocol.BLE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Check Connectivity Status LED is in slow blinking state while device reconnects"
                                     " back to the host")
            # ----------------------------------------------------------------------------------------------------------
            LedSpyHelper.check_effect_duration(
                self, LED_ID.CONNECTIVITY_STATUS_LED_1, SchemeType.SLOW_BLINKING,
                maximum_duration=LedSpyHelper.TWO_SECONDS, reset=True)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Check Connectivity Status LED 1 is in steady on state for 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(
            self, LED_ID.CONNECTIVITY_STATUS_LED_1, SchemeType.STEADY, exact_duration=LedSpyHelper.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check Battery Green LED is in Steady ON state for exactly 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(
            self, LED_ID.DEVICE_STATUS_GREEN_LED, SchemeType.STEADY, exact_duration=LedSpyHelper.FIVE_SECONDS,
            reset=True, position=LedSpyHelper.POSITION.FROM_LAST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check Battery Red LED is in OFF state for at least 5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        LedSpyHelper.check_effect_duration(
            self, LED_ID.DEVICE_STATUS_RED_LED, SchemeType.OFF, minimum_duration=LedSpyHelper.FIVE_SECONDS, reset=True,
            position=LedSpyHelper.POSITION.FROM_LAST)
    # end def generic_check_led_behaviour_on_dfu
# end class GenericDfuTestCaseBusiness


class SharedDfuTestCaseBusiness(GenericDfuTestCaseBusiness, ABC):
    """
    Validate DFU Business TestCases
    """

    @features('Feature00D0')
    @level('Business')
    @services('Debugger')
    def test_complete_dfu_business(self):
        """
        Validate the DFU business case targeting the application entity.
        """
        self.generic_complete_dfu_business()

        self.testCaseChecked("FNT_00D0_0005#1")
    # end def test_complete_dfu_business

    @features('Feature00D0')
    @features('ImageDFU')
    @level('Business')
    @services('Debugger')
    def test_complete_image_dfu_business(self):
        """
        Validate the DFU business case targeting the application entity.
        """
        self.generic_complete_dfu_business(dfu=self.DFU_IMAGE)

        self.testCaseChecked("FNT_00D0_0005#2")
    # end def test_complete_image_dfu_business

    @features('SecureDfuControlAnyReloadActionType')
    @features('SecureDfuControlChangeActionTypeByDFU')
    @features('Feature00D0')
    @level('Business')
    @services('Debugger')
    def test_change_action_type_by_dfu(self):
        """
        Check action type to enter in bootloader can be changed by DFU.

        JIRA: https://jira.logitech.io/browse/NRF52-121
        """
        self.generic_change_action_type_by_dfu()

        self.testCaseChecked("BUS_00D0_0009")
    # end def test_change_action_type_by_dfu

    @features('Feature00D0SoftDevice')
    @level('Business', 'SmokeTests')
    @services('Debugger')
    def test_soft_device_dfu_business(self):
        """
        Validate the DFU business case targeting the softdevice entity.
        """
        self.generic_soft_device_dfu_business()

        self.testCaseChecked("FNT_00D0_0015")
    # end def test_soft_device_dfu_business

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_CBC)
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_complete_dfu_business_aes_cbc(self):
        """
        Validate the DFU business case targeting the application entity with program data encrypted with AES algorithm
        in cipher-block chaining (CBC).
        """
        self.generic_complete_dfu_business(encrypt_algorithm=Dfu.EncryptionMode.AES_CBC)

        self.testCaseChecked("FNT_00D0_0033")
    # end def test_complete_dfu_business_aes_cbc

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_CFB)
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_complete_dfu_business_aes_cfb(self):
        """
        Validate the DFU business case targeting the application entity with program data encrypted with AES algorithm
        in cipher feedback (CFB).
        """
        self.generic_complete_dfu_business(encrypt_algorithm=Dfu.EncryptionMode.AES_CFB)

        self.testCaseChecked("FNT_00D0_0034")
    # end def test_complete_dfu_business_aes_cfb

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_OFB)
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_complete_dfu_business_aes_ofb(self):
        """
        Validate the DFU business case targeting the application entity with program data encrypted with AES algorithm
        in output feedback (OFB).
        """
        self.generic_complete_dfu_business(encrypt_algorithm=Dfu.EncryptionMode.AES_OFB)

        self.testCaseChecked("FNT_00D0_0035")
    # end def test_complete_dfu_business_aes_ofb

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Business')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_dfu_business(self):
        """
        Validate the DFU business case targeting the companion application entity.
        """
        self.generic_companion_dfu_business()

        self.testCaseChecked("BUS_00D0_0010")
    # end def test_companion_dfu_business
# end class SharedDfuTestCaseBusiness


class GenericDfuOnTagTestCaseBusiness(CommonDfuTestCase, ABC):
    """
    Generic class for the validation DFU Business TestCases
    """
    TAG1 = 0
    TAG2 = 1
    TAG3 = 2

    def setUp(self):
        """
        Handle test prerequisites.
        """
        # The call to CommonBootloaderTestCase.setUp() is bypassed. This is because even if we need all the method of
        # CommonDfuTestCase and CommonBootloaderTestCase, this test case should not jump on bootloader as a prerequisite
        super(CommonBootloaderTestCase, self).setUp()

        self.dfu_config = self.f.PRODUCT.FEATURES.COMMON.DFU

        self.post_requisite_program_mcu_initial_state = True

        # -----------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Backup initial NVS')
        # -----------------------------------------------------------------
        self.memory_manager.read_nvs(backup=True)
        if self.device_memory_manager is not None:
            # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
            self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                test_case=self, memory_manager=self.device_memory_manager)
        # end if

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        if self.current_channel != self.backup_dut_channel:
            # If channel not on
            DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        # end if

        try_count = 0
        while try_count < self.MAX_TRY:
            # noinspection PyBroadException
            try:
                if self.post_requisite_program_mcu_initial_state:
                    # --------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, 'Program the MCU back to its initial state')
                    # --------------------------------------------------------------------
                    fw_hex = join(TESTS_PATH, "DFU_FILES", self.dfu_config.F_HexFileName)
                    nvs_file = self.memory_manager.backup_nvs_parser.to_hex_file()
                    self.debugger.reload_file(firmware_hex_file=fw_hex, nvs_hex_file=nvs_file, no_reset=True)

                    # ----------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(test_case=self, text="Force target on application")
                    # ----------------------------------------------------------------------------------------------
                    # If the protocol is BLE, it is important not to reset the device after setting the
                    # application bit so that a force service changed can be requested. This would then trigger
                    # the reset and avoid an intermediate reset.
                    is_ble = self.config_manager.current_protocol in [LogitechProtocol.BLE_PRO, LogitechProtocol.BLE]
                    self.debugger.set_application_bit(no_reset=is_ble)

                    if is_ble:
                        # ------------------------------------------------------------------------------------------
                        LogHelper.log_post_requisite(
                            test_case=self,
                            text="In BLE, force service change to be sure to have the right state of the receiver")
                        # ------------------------------------------------------------------------------------------
                        # In BLE, a service changed is forced to be sure to have the right state of the receiver
                        DfuTestUtils.NvsHelper.force_service_changed(test_case=self)
                    # end if

                    # This distinction is only to be done here because this part will happen for all protocols
                    # except Unifying.
                    # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it
                    #  would be interesting to investigate a better solution
                    if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
                        # Expected sequence: ble_service_changed_required=False
                        # because the first disconnection is on slot 2 !
                        # - Disconnection from pairing slot 2
                        # - Connection to pairing slot 1
                        # - Disconnection from pairing slot 1 due to force service changed
                        # - Reconnection to pairing slot 1
                        DfuTestUtils.verify_communication_disconnection_then_reconnection(
                            test_case=self, ble_service_changed_required=is_ble)
                    # end if

                    self.post_requisite_program_mcu_initial_state = False
                # end if
                break
            except Exception:
                try_count += 1
                self.log_traceback_as_warning(supplementary_message=f"Exception in tearDown with retry counter = "
                                                                    f"{try_count}:")
            # end try
        # end while
        # The call to CommonBootloaderTestCase.tearDown() is bypassed because CommonBootloaderTestCase.setUp() was too.
        # Moreover, it is very similar to the tearDown() of this method and have actions that should not be done twice.
        super(CommonBootloaderTestCase, self).tearDown()
    # end def tearDown

    def _dfu_over_tag(self, tag_index):
        """
        Execute a DFU compatibility test with a previous version (i.e. TAG).

        :param tag_index: Index of the compatible tag in the configuration list
        :type tag_index: ``int``
        """
        hex_file_name = self.dfu_config.F_HexFileName[:-4] + "_" + self.dfu_config.F_CompatibleTags[tag_index] + ".hex"
        action_type = getattr(GetDfuControlResponseV0.ACTION,
                              self.dfu_config.F_CompatibleTagsDfuControlActionType[tag_index].upper()[len('ACTION_'):],
                              self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType)

        if self.current_channel.protocol == LogitechProtocol.USB and self.current_channel.is_open:
            ChannelUtils.close_channel(test_case=self)
        # end if

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Flash {hex_file_name} file')
        # ---------------------------------------------------------------------------
        self.post_requisite_program_mcu_initial_state = True
        # Call 'reload_file' method to keep the AES key untouched
        self.debugger.reload_file(firmware_hex_file=join(TESTS_PATH, "DFU_FILES", hex_file_name),
                                  nvs_hex_file=join(TESTS_PATH, "DFU_FILES", hex_file_name))

        self._reconnect_device()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch in bootloader mode')
        # ---------------------------------------------------------------------------
        self.dut_jump_on_bootloader(action_type)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Soft device DFU processing')
        # ---------------------------------------------------------------------------
        self.bootloader_dfu_processing(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", self.dfu_config.F_SoftDeviceDfuFileName),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id, restart_all=False,
            is_ble_service_changed_required=False)

        self.reset(hardware_reset=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the DUT is still in bootloader mode')
        # ---------------------------------------------------------------------------
        DeviceInformationTestUtils.check_active_entity_type(
            test_case=self,
            device_index=ChannelUtils.get_device_index(test_case=self),
            entity_type=DeviceInformation.EntityTypeV1.BOOTLOADER)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Application DFU processing')
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x02 (DFU success)')
        # ---------------------------------------------------------------------------
        self.perform_dfu(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", self.dfu_config.F_ApplicationDfuFileName),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id)
        self.post_requisite_program_mcu_initial_state = True
    # end def _dfu_over_tag

    def _reconnect_device(self):
        """
        Reconnect the device after flashing the firmware (NVS included).
        """
        if self.current_channel.protocol > LogitechProtocol.UNKNOWN:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Clean all receiver pairing slot')
            # ---------------------------------------------------------------------------
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                        class_type=SetPerformDeviceConnectionResponse)
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                        class_type=Hidpp1ErrorCodes)
            DevicePairingTestUtils.unpair_all(self)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start the discovery sequence')
            # ---------------------------------------------------------------------------
            bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Restart the pairing sequence')
            # ---------------------------------------------------------------------------
            pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address)
            DeviceManagerUtils.set_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(
                    port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot))
            root_version = self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
            self.current_channel.hid_dispatcher.add_feature_entry(Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=WirelessDeviceStatus.FEATURE_ID)
        elif self.current_channel.protocol == LogitechProtocol.BLE:
            if hasattr(self, "ble_context_device_used"):
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.ble_context_device_used)
            # end if

            self.memory_manager.read_nvs()

            # -----------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Enter pairing mode on current slot')
            # -----------------------------------------------------------------
            self.button_stimuli_emulator.enter_pairing_mode()

            # -----------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Scan for BLE device')
            # -----------------------------------------------------------------
            self.ble_context_device_used = BleProtocolTestUtils.scan_for_current_device(
                test_case=self, scan_timeout=1, send_scan_request=True)
            # Delete device bond if it already exists
            BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.ble_context_device_used)

            # -----------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Connect and bond to the BLE device')
            # -----------------------------------------------------------------
            BleProtocolTestUtils.connect_and_bond_device(
                test_case=self, ble_context_device=self.ble_context_device_used)

            current_channel = BleChannel(ble_context=BleProtocolTestUtils.get_ble_context(test_case=self),
                                         ble_context_device=self.ble_context_device_used)

            DeviceManagerUtils.set_channel(test_case=self, new_channel=current_channel)
        elif self.current_channel.protocol == LogitechProtocol.USB:
            ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)
        else:
            raise RuntimeError(f"Unknown channel protocol: {self.current_channel.protocol}")
        # end if
    # end def _reconnect_device
# end class GenericDfuOnTagTestCaseBusiness


class SharedDfuOnTagTestCaseBusiness(GenericDfuOnTagTestCaseBusiness, ABC):
    """
    Validate DFU Business TestCases
    """

    @features('Feature00D0')
    @features('Feature00D0Tags', GenericDfuOnTagTestCaseBusiness.TAG1)
    @features('Bluetooth')
    @level('Business')
    @services('Debugger')
    def test_dfu_over_first_tag(self):
        """
        Validate the DFU compatibility with a previous version (i.e. first given TAG).
        """
        self._dfu_over_tag(self.TAG1)

        self.testCaseChecked("BUS_00D0_0006")
    # end def test_dfu_over_first_tag

    @features('Feature00D0')
    @features('Feature00D0Tags', GenericDfuOnTagTestCaseBusiness.TAG2)
    @features('Bluetooth')
    @level('Business')
    @services('Debugger')
    def test_dfu_over_second_tag(self):
        """
        Validate the DFU compatibility with a previous version (i.e. second given TAG).
        """
        self._dfu_over_tag(self.TAG2)

        self.testCaseChecked("BUS_00D0_0007")
    # end def test_dfu_over_second_tag

    @features('Feature00D0')
    @features('Feature00D0Tags', GenericDfuOnTagTestCaseBusiness.TAG3)
    @features('Bluetooth')
    @level('Business')
    @services('Debugger')
    def test_dfu_over_third_tag(self):
        """
        Validate the DFU compatibility with a previous version (i.e. third given TAG).
        """
        self._dfu_over_tag(self.TAG3)

        self.testCaseChecked("BUS_00D0_0008")
    # end def test_dfu_over_third_tag
# end class SharedDfuOnTagTestCaseBusiness

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
