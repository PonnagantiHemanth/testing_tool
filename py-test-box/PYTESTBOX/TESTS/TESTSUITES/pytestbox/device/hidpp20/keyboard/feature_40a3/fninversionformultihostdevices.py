#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_40a3.fninversionformultihostdevices
:brief: Validate HID++ 2.0 ``FnInversionForMultiHostDevices`` feature
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/9/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import IntEnum
from enum import unique

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevices
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FnInversionForMultiHostDevicesTestCase(DeviceBaseTestCase):
    """
    Validate ``FnInversionForMultiHostDevices`` TestCases in Application mode
    """

    @unique
    class ChangeHostType(IntEnum):
        """
        Define the method to change host
        """
        HIDPP_1814 = 0
        EASY_SWITCH = 1
    # end class ChangeHostType

    @unique
    class ReportType(IntEnum):
        """
        F-Row report type
        """
        SHORTCUT_KEY = 0
        F_KEY = 1
    # end class ReportType

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        self.post_requisite_clean_pairing_info_on_receivers = False
        self.post_requisite_enable_all_usb_ports = False
        self.post_requisite_new_equad_connection = False
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x40A3 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_40a3_index, self.feature_40a3, _, _ = FnInversionForMultiHostDevicesTestUtils.HIDppHelper. \
            get_parameters(self)

        # Verify only a version is configured
        if self.f.PRODUCT.F_IsGaming:
            assert self.f.PRODUCT.DEVICE.FN_LOCK.F_GAMING_UX_V1_0 is True
        else:
            assert sum([self.f.PRODUCT.DEVICE.FN_LOCK.F_PWS_UX_V1_0, self.f.PRODUCT.DEVICE.FN_LOCK.F_PWS_UX_V1_1,
                        self.f.PRODUCT.DEVICE.FN_LOCK.F_PWS_UX_V1_2, self.f.PRODUCT.DEVICE.FN_LOCK.F_PWS_UX_V1_3]) == 1
        # end if

        self.config = self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES

        self.nb_host = self.f.PRODUCT.DEVICE.F_NbHosts if self.f.PRODUCT.DEVICE.F_NbHosts > 0 else 1
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_enable_all_usb_ports:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Turn on all the receivers usb ports to restore the initial state')
                # ------------------------------------------------------------------------------------------------------
                self.device.enable_all_usb_ports()
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_channel != self.backup_dut_channel:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Back to the initial channel")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.close_channel(test_case=self)
                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_clean_pairing_info_on_receivers:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean pairing info on receivers except the first slot in the first "
                                                   "receiver")
                # ------------------------------------------------------------------------------------------------------
                # Clean all pairing info on receivers except the first slot of the first receiver
                for host_idx in range(self.nb_host):
                    ReceiverTestUtils.switch_to_receiver(self, self.host_number_to_port_index(host_idx))
                    DevicePairingTestUtils.unpair_all(self, first_slot=2 if host_idx == 0 else 1)
                # end for
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_new_equad_connection:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Redo the equad pairing with the default values")
                # ------------------------------------------------------------------------------------------------------
                # noinspection PyUnresolvedReferences
                # unit_id should be read in test pre-requisite if this post-requisite is required
                EQuadDeviceConnectionUtils.new_device_connection_and_pre_pairing(
                    test_case=self, unit_ids=[self.unit_id], disconnect=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Get device name in pairing info')
                # ------------------------------------------------------------------------------------------------------
                device_name_req = GetEQuadDeviceNameRequest(
                    NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN +
                    ChannelUtils.get_device_index(self) - 1)
                device_name_resp = ChannelUtils.send(
                    test_case=self,
                    channel=self.current_channel.receiver_channel,
                    report=device_name_req,
                    response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                    response_class_type=GetEQuadDeviceNameResponse
                )
                equad_device_name = device_name_resp.name_string.toString()
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'New connection with device {equad_device_name}')
                # ------------------------------------------------------------------------------------------------------
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def check_fn_inversion_state(self, host_index, fn_inversion_state):
        """
        Check the fn inversion state of the given host index

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param host_index: Host index
        :type host_index: ``int``
        :param fn_inversion_state: fnInversionState (0 = Fn Inversion Off, 1 = Fn Inversion On)
        :type fn_inversion_state: ``FnInversionForMultiHostDevices.FnInversionState``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check fnInversionState == {fn_inversion_state} for Host index 0x{host_index} by "
                                  "getGlobalFnInversion")
        # --------------------------------------------------------------------------------------------------------------
        response = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.get_global_fn_inversion(self, host_index)
        checker = FnInversionForMultiHostDevicesTestUtils.GetGlobalFnInversionResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['host_index'] = (checker.check_host_index, host_index)
        check_map['fn_inversion_state'] = (checker.check_fn_inversion_state, fn_inversion_state)
        checker.check_fields(self, response, self.feature_40a3.get_global_fn_inversion_response_cls, check_map)
    # end def check_fn_inversion_state

    def set_fn_inversion_state(self, host_index, fn_inversion_state):
        """
        Set the fn inversion state of specific host index

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param host_index: Host index
        :type host_index: ``int``
        :param fn_inversion_state: fnInversionState (0 = Fn Inversion Off, 1 = Fn Inversion On)
        :type fn_inversion_state: ``FnInversionForMultiHostDevices.FnInversionState``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set fnInversionState == {fn_inversion_state} for Host index 0x{host_index} by "
                                 "setGlobalFnInversion")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(self, host_index,
                                                                                    fn_inversion_state)
    # end def set_fn_inversion_state

    def set_fn_inversion_state_for_all_host(self, fn_inversion_state):
        """
        Set the fn inversion state to ON or OFF for all hosts

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param fn_inversion_state: fnInversionState (0 = Fn Inversion Off, 1 = Fn Inversion On)
        :type fn_inversion_state: ``FnInversionForMultiHostDevices.FnInversionState``
        """
        assert fn_inversion_state in FnInversionForMultiHostDevices.FnInversionState

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set FnInversion to '{repr(fn_inversion_state)}' for all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(self.nb_host):
            FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(self, host_index,
                                                                                        fn_inversion_state)
        # end for
    # end def set_fn_inversion_state_for_all_host

    def check_f_lock_change_event(self, fn_inversion_state):
        """
        Check fn inversion state in fLockChange event

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param fn_inversion_state: fnInversionState (0 = Fn Inversion Off, 1 = Fn Inversion On)
        :type fn_inversion_state: ``FnInversionForMultiHostDevices.FnInversionState``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get fLockChange event")
        # --------------------------------------------------------------------------------------------------------------
        event = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.f_lock_change_event(self, check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check fnInversionState in fLockChange event")
        # --------------------------------------------------------------------------------------------------------------
        checker = FnInversionForMultiHostDevicesTestUtils.FLockChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, FnInversionForMultiHostDevices.HostIndex.HOST1),
            "fn_inversion_state": (checker.check_fn_inversion_state, fn_inversion_state),
        })
        checker.check_fields(self, event, self.feature_40a3.f_lock_change_event_cls, check_map)
    # end def check_f_lock_change_event

    def keystroke_f_row_and_check_report(self, press_fn, expected_report_type, os_variant=None):
        """
        Generate a keystroke on an F-Row key possibly combined with the FN key then check the HID report(s) received

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param press_fn: Press Fn key or not
        :type press_fn: ``bool``
        :param expected_report_type: The expected report type
        :type expected_report_type: ``FnInversionForMultiHostDevicesTestCase.ReportType``
        :param os_variant: OS used to build the expected report - OPTIONAL
        :type os_variant: ``str``
        """
        assert expected_report_type in FnInversionForMultiHostDevicesTestCase.ReportType
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Expected report type is {str(expected_report_type)}')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported F-Keys")
        # --------------------------------------------------------------------------------------------------------------
        exclude_double_press_key = KEY_ID.PLAY_PAUSE if self.f.PRODUCT.FEATURES.KEYBOARD.F_PlayPauseDoublePress \
            else None
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        for key_id in range(KEY_ID.KEYBOARD_F1, KEY_ID.KEYBOARD_F24):
            if key_id not in fn_keys or fn_keys[KEY_ID(key_id)] in [KEY_ID.HOST_1, KEY_ID.HOST_2, KEY_ID.HOST_3,
                                                                    exclude_double_press_key]:
                # Skip not supported keys on the DUT and host-switch buttons
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(KEY_ID(key_id))}')
            # ----------------------------------------------------------------------------------------------------------
            if press_fn:
                self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                                 delay=ButtonStimuliInterface.DEFAULT_DURATION)
                self.button_stimuli_emulator.keystroke(key_id=fn_keys[KEY_ID(key_id)])
                self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                                   delay=ButtonStimuliInterface.DEFAULT_DURATION)
            else:
                self.button_stimuli_emulator.keystroke(key_id=fn_keys[KEY_ID(key_id)])
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported F-Keys")
        # --------------------------------------------------------------------------------------------------------------
        for key_id in [x for x in KEY_ID if KEY_ID.KEYBOARD_F1 <= x <= KEY_ID.KEYBOARD_F24]:
            if key_id not in fn_keys or fn_keys[key_id] in [KEY_ID.HOST_1, KEY_ID.HOST_2, KEY_ID.HOST_3,
                                                            exclude_double_press_key]:
                # Skip not supported keys on the DUT and host-switch buttons
                continue
            # end if

            report_type = fn_keys[key_id] if \
                expected_report_type == FnInversionForMultiHostDevicesTestCase.ReportType.SHORTCUT_KEY else \
                KEY_ID(key_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check that the HID report corresponds to the key: '
                                      f'{str(KEY_ID(key_id))}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(report_type, MAKE),
                                                          variant=os_variant)
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(report_type, BREAK),
                                                          variant=os_variant)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end keystroke_f_row_and_check_report

    def keystroke_f_row_and_check_report_gaming(self):
        """
        Generate a keystroke on an F-Row key then check the HID report(s) received for gaming

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported F-Keys")
        # --------------------------------------------------------------------------------------------------------------
        for key_id in range(KEY_ID.KEYBOARD_F1, KEY_ID.KEYBOARD_F24):
            if key_id not in self.button_stimuli_emulator._keyboard_layout.KEYS:
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(KEY_ID(key_id))}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported F-Keys")
        # --------------------------------------------------------------------------------------------------------------
        for key_id in range(KEY_ID.KEYBOARD_F1, KEY_ID.KEYBOARD_F24):
            if key_id not in self.button_stimuli_emulator._keyboard_layout.KEYS:
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check that the HID report corresponds to the key: {str(KEY_ID(key_id))}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(KEY_ID(key_id), MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(KEY_ID(key_id), BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end keystroke_f_row_and_check_report_gaming

    def switch_to_another_host(self, target_host_idx, change_host_type=ChangeHostType.HIDPP_1814):
        """
        Switch to the given host by either the 0x1814 HID++ request or keystroke on easy switch buttons

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param target_host_idx: The target host index which starts from 0
        :type target_host_idx: ``int``
        :param change_host_type: The type of how to change device host - OPTIONAL
        :type change_host_type: ``FnInversionForMultiHostDevicesTestCase.ChangeHostType``
        """
        assert change_host_type in FnInversionForMultiHostDevicesTestCase.ChangeHostType
        LogHelper.log_info(self, f'Change host by {str(change_host_type)}')

        if change_host_type == FnInversionForMultiHostDevicesTestCase.ChangeHostType.HIDPP_1814:
            ChangeHostTestUtils.HIDppHelper.set_current_host(
                self, device_index=ChannelUtils.get_device_index(test_case=self),
                host_index=target_host_idx)
        elif change_host_type == FnInversionForMultiHostDevicesTestCase.ChangeHostType.EASY_SWITCH:
            self.button_stimuli_emulator.change_host(HOST.ALL[target_host_idx])
        # end if

        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=self.host_number_to_port_index(target_host_idx),
                                             device_index=1))
    # end def switch_to_another_host
# end class FnInversionForMultiHostDevicesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
