#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.base.bootloadertest
:brief: common bootloader processing module for device and receiver targets
    A description of the BaseTestCase hierarchy could be found here
    https://drive.google.com/drive/folders/1YiT7CYc_1UIFwVzOwVkcoIa8hH5oTkwi
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/03/26
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from abc import ABC
from os.path import join
from time import sleep

from intelhex import IntelHex
from pylink import JLinkException

from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyharness.core import TYPE_SUCCESS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.tools.util import NotImplementedAbstractMethodError
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pyusb.libusbdriver import LibusbDriver


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class CommonBootloaderTestCase(CommonBaseTestCase, ABC):
    """
    Device and receiver common Bootloader processing test case class.
    """
    MAX_TRY = 3

    # The naming of methodName is inherited from PyHarnessCase
    # noinspection PyPep8Naming
    def __init__(self, methodName='runTest'):
        """
        :param methodName: Name of the method to launch
        :type methodName: ``str``
        """
        self.post_requisite_restart_in_main_application = False
        self.post_requisite_program_mcu_initial_state = False
        self.post_requisite_erase_and_flash = False
        self.post_requisite_reset_receiver = False
        self.post_requisite_restore_companion = False
        self.bootloader_dfu_feature_id = 0

        super().__init__(methodName=methodName)
    # end def __init__

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        if self.debugger is not None:
            # -----------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Backup initial NVS')
            # -----------------------------------------------------------------
            self.memory_manager.read_nvs(backup=True)
            if self.debugger.CONNECT_UNDER_RESET:
                # Reopen Channel to avoid the issue of the device not being able to connect after a reset
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
                # end if
            # end if
        # end if

        self.dut_jump_on_bootloader()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if (not isinstance(self, DeviceBaseTestCase) or self.PROTOCOL_TO_CHANGE_TO is None) and \
                    self.current_channel != self.backup_dut_channel and not self.f.PRODUCT.F_IsGaming:
                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_restore_companion:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Restore the companion firmware")
                # ------------------------------------------------------------------------------------------------------
                if self.current_channel.protocol == LogitechProtocol.USB and self.current_channel.is_open:
                    ChannelUtils.close_channel(test_case=self)
                # end if

                self.companion_debugger.stop()
                self.debugger.stop()
                self.companion_debugger.erase_and_flash_firmware(
                    firmware_hex_file=join(
                        TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHexFileName),
                    no_reset=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Reset (both MCUs)")
                # ------------------------------------------------------------------------------------------------------
                self.debugger.reset()
                self.companion_debugger.reset()

                if self.f.PRODUCT.USB_COMMUNICATION.F_SetIdleSupported:
                    ChannelUtils.set_idle(test_case=self)
                # end if

                self.post_requisite_restart_in_main_application = True
            # end if
        # end with

        with self.manage_post_requisite():
            try_count = 0
            while try_count < self.MAX_TRY:
                try:
                    if self.post_requisite_program_mcu_initial_state:
                        assert self.debugger is not None, \
                            "Cannot program MCU to initial state if the debugger is not present"
                        assert self.memory_manager.backup_nvs_parser is not None, \
                            "Cannot program MCU to initial state if the backup NVS is not present"
                            
                        if self.current_channel.protocol == LogitechProtocol.USB and self.current_channel.is_open:
                            ChannelUtils.close_channel(test_case=self)
                        # end if

                        if self.companion_debugger:
                            self.companion_debugger.stop()
                        # end if

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_post_requisite(test_case=self, text="Program the MCU back to its initial state")
                        # ----------------------------------------------------------------------------------------------
                        # noinspection PyUnresolvedReferences
                        fw_hex = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)
                        nvs_file = self.memory_manager.backup_nvs_parser.to_hex_file()
                        self.debugger.reload_file(firmware_hex_file=fw_hex, nvs_hex_file=nvs_file, no_reset=True)

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_post_requisite(test_case=self, text="Force target on application")
                        # ----------------------------------------------------------------------------------------------
                        # If the protocol is BLE, it is important not to reset the device after setting the
                        # application bit so that a force service changed can be requested. This would then trigger
                        # the reset and avoid an intermediate reset.
                        is_ble = self.config_manager.current_protocol in [LogitechProtocol.BLE_PRO,
                                                                          LogitechProtocol.BLE]
                        if self.companion_debugger is None:
                            self.debugger.set_application_bit(no_reset=is_ble)

                            if is_ble:
                                # --------------------------------------------------------------------------------------
                                LogHelper.log_post_requisite(test_case=self,
                                                             text="In BLE, force service change to be sure to have "
                                                                  "the right state of the receiver")
                                # --------------------------------------------------------------------------------------
                                CommonBaseTestUtils.NvsHelper.force_service_changed(test_case=self)
                            # end if
                        else:
                            self.debugger.reset()
                            self.companion_debugger.reset()
                            DfuTestUtils.force_target_on_application(test_case=self, check_required=True)
                        # end if

                        # This distinction is only to be done here because this part will happen for all protocols
                        # except Unifying.
                        # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it
                        #  would be interesting to investigate a better solution
                        if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
                            # ------------------------------------------------------------------------------------------
                            LogHelper.log_post_requisite(test_case=self, text="Verify disconnection-reconnection")
                            # ------------------------------------------------------------------------------------------
                            CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                                test_case=self, ble_service_changed_required=is_ble)
                        # end if

                        self.post_requisite_restart_in_main_application = False
                        self.post_requisite_program_mcu_initial_state = False
                    elif self.post_requisite_restart_in_main_application or self.status != TYPE_SUCCESS:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_post_requisite(test_case=self, text="Restart in Main Application mode")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.open_channel(test_case=self)
                        DfuTestUtils.force_target_on_application(test_case=self)
                        self.post_requisite_restart_in_main_application = False
                    # end if

                    ChannelUtils.empty_queue(test_case=self,
                                             queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)

                    break
                except Exception as e:
                    try_count += 1

                    self.log_traceback_as_warning(
                        supplementary_message=f"Exception in tearDown with retry counter = {try_count}:")

                    if try_count >= self.MAX_TRY:
                        raise RuntimeError("Max tries") from e
                    # end if

                    if self.debugger is not None:
                        if self.memory_manager.backup_nvs_parser is None:
                            # Stop trying if not possible to reload the NVS
                            raise RuntimeError("Not possible to reload NVS") from e
                        # end if
                        if isinstance(self.current_channel, (UsbReceiverChannel, ThroughReceiverChannel)) and \
                                len(LibusbDriver.discover_usb_hub()) > 0:
                            ChannelUtils.close_channel(test_case=self, close_associated_channel=True)

                            # ------------------------------------------------------------------------------------------
                            LogHelper.log_post_requisite(test_case=self, text="Reset the receiver")
                            # ------------------------------------------------------------------------------------------
                            # Use a try finally to be sure to enable the receiver at the end
                            with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=self.receiver_debugger), \
                                 CommonBaseTestUtils.EmulatorHelper.debugger_closed(
                                     debugger=self.receiver_companion_debugger):
                                try:
                                    LibusbDriver.disable_usb_port(port_index=ChannelUtils.get_port_index(self))
                                finally:
                                    LibusbDriver.enable_usb_port(port_index=ChannelUtils.get_port_index(self))
                                # end try
                            # end with

                            ChannelUtils.open_channel(test_case=self, open_associated_channel=True)
                        # end if
                        self.post_requisite_program_mcu_initial_state = True
                    # end if
                # end try
            # end while
        # end with

        with self.manage_post_requisite():
            if not self.post_requisite_erase_and_flash and not DfuTestUtils.is_main_app(self):
                self.post_requisite_erase_and_flash = True
            # end if
            if self.post_requisite_erase_and_flash:
                try_count = 0
                while try_count < self.MAX_TRY:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case=self, msg=f"Erase and flash full firmware (retry = {try_count})")
                    # --------------------------------------------------------------------------------------------------
                    try:
                        fw_hex = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)
                        fw_hex = IntelHex(fw_hex)
                        if self.f.PRODUCT.FEATURES.COMMON.DFU.F_BootHexFileName:
                            btldr_hex = join(
                                TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_BootHexFileName)
                            btldr_hex = IntelHex(btldr_hex)
                            fw_hex.merge(btldr_hex, 'replace')
                        # end if
                        if self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesHexFileName:
                            img_hex = join(
                                TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesHexFileName)
                            img_hex = IntelHex(img_hex)
                            fw_hex.merge(img_hex, 'replace')
                        # end if
                        nvs_file = self.memory_manager.backup_nvs_parser.to_hex_file()
                        nvs_file = IntelHex(nvs_file)
                        fw_hex.merge(nvs_file, 'replace')
                        if self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY is not None:
                            initial_aes_local_key = self.memory_manager.debugger.readMemory(
                                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY,
                                self.memory_manager.SIZE.NVS_ENCRYPTION_KEY)
                            aes_key_addresses = range(
                                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY,
                                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY +
                                self.memory_manager.SIZE.NVS_ENCRYPTION_KEY)
                            aes_key_intel_hex = IntelHex(dict(zip(aes_key_addresses, initial_aes_local_key)))
                            fw_hex.merge(aes_key_intel_hex, overlap='replace')
                        # end if
                        self.debugger.erase_and_flash_firmware(firmware_hex_file=fw_hex)
                        self.reset()
                        break
                    except JLinkException as e:
                        # Reconnect the debugger and retry
                        self.debugger.close()
                        sleep(0.7)
                        self.debugger.open()
                        try_count += 1
                        if try_count >= self.MAX_TRY:
                            raise RuntimeError("Max tries") from e
                        # end if
                    # end try
                # end while
            # end if
        # end with

        with self.manage_post_requisite():
            if self.backup_dut_channel.protocol in LogitechProtocol.gaming_protocols() and \
                    self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
                # Leave from USB channel if the DUT is a gaming device, otherwise do nothing
                ProtocolManagerUtils.exit_usb_channel(self)
                ChannelUtils.clean_messages(
                    test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                    class_type=WirelessDeviceStatusBroadcastEvent)
                self.cleanup_battery_event_from_queue()
                self.post_requisite_reset_receiver = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reset_receiver:
                if self.receiver_debugger is not None:
                    ChannelUtils.close_channel(test_case=self, channel=self.current_channel.receiver_channel)
                    self.receiver_debugger.reset()
                # end if
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def perform_dfu(self, dfu_file_path, bootloader_dfu_feature_id, log_step=0, log_check=0, restart_all=False,
                    encrypt_algorithm=None):
        """
        Perform a DFU, if log_step and log_check are <=0, there is no log message.

        :param dfu_file_path: The path of the DFU file to use
        :type dfu_file_path: ``str``
        :param bootloader_dfu_feature_id: The DFU feature index in bootloader
        :type bootloader_dfu_feature_id: ``int``
        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``
        :param restart_all: Restart all entities at the end (if True) or only the entity updated (if False)
        :type restart_all: ``bool``
        :param encrypt_algorithm: The encryption algorithm to use in Dfu.EncryptionMode, if ``None`` no encryption
                                  will be done
        :type encrypt_algorithm: ``int``

        :return: The new log_step and log_check
        :rtype: ``tuple``
        """
        raise NotImplementedAbstractMethodError()
    # end def perform_dfu

    def dut_jump_on_bootloader(self, *args, **kwargs):
        """
        Request the device to jump on the bootloader (if it is not already in bootloader mode).

        :param args: The action type required - OPTIONAL
        :type args: ``int`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def dut_jump_on_bootloader

    def check_application_mode(self, log_step=0, log_check=0):
        """
        Check the DUT is in application mode.

        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def check_application_mode
# end class CommonBootloaderTestCase


class DeviceBootloaderTestCase(CommonBootloaderTestCase, DeviceBaseTestCase):
    """
    Device Bootloader test case with
    - bootloader supporting HID++ 2.0 protocol
    - application supporting HID++ 1.0 protocol
    """

    def dut_jump_on_bootloader(self, action_type=None):
        """
        Request the device to jump on the bootloader (if it is not already in bootloader mode).

        :param action_type: The action type required - OPTIONAL
        :type action_type: ``int`` or ``None``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enter into bootloader mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.jump_on_bootloader(test_case=self, action_type=action_type)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x00D0)')
        # ---------------------------------------------------------------------------
        self.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(self, feature_id=Dfu.FEATURE_ID)
    # end def dut_jump_on_bootloader

    def check_application_mode(self, log_step=0, log_check=0):
        # See ``CommonBootloaderTestCase.check_application_mode``
        if log_step > 0:
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step {log_step}: Send Root.GetFeature(0x0003)')
            # ---------------------------------------------------------------------------
        # end if

        if log_check > 0:
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Verify Device is in Main Application mode')
            # ---------------------------------------------------------------------------
        # end if
        DeviceInformationTestUtils.check_active_entity_type_is_main_app(
            test_case=self,
            device_index=ChannelUtils.get_device_index(test_case=self))

        self.config_manager.current_mode = self.config_manager.MODE.APPLICATION
    # end def check_application_mode
# end class DeviceBootloaderTestCase


class ReceiverBootloaderTestCase(CommonBootloaderTestCase, ReceiverBaseTestCase):
    """
    Receiver Bootloader test case with
    - bootloader supporting HID++ 2.0 protocol
    - application supporting HID++ 1.0 protocol
    """
    def dut_jump_on_bootloader(self):
        """
        Request the receiver to jump on the bootloader (if it is not already in bootloader mode).
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enter into bootloader mode')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.jump_on_bootloader(self)

        # ------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x00D0)')
        # ------------------------------------------------------------------------------------------------------
        self.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(self, feature_id=Dfu.FEATURE_ID)
    # end def dut_jump_on_bootloader

    def check_application_mode(self, log_step=0, log_check=0):
        # See ``CommonBootloaderTestCase.check_application_mode``
        if log_step > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Enable HIDPP reporting request')
            # ---------------------------------------------------------------------------
        # end if
        if log_check > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify no Error Response received')
            # ---------------------------------------------------------------------------
        # end if
        ChannelUtils.set_hidpp_reporting(test_case=self)

        self.config_manager.current_mode = self.config_manager.MODE.APPLICATION
    # end def check_application_mode
# end class ReceiverBootloaderTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
