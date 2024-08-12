#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.securedfucontrol
:brief: Shared test case for the validation of HID++2 common feature 0x00C3 and HID++1 register 0xF5
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2020/10/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join
from time import sleep
from time import time

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.core import TYPE_SUCCESS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.securedfucontrol import GetDfuControlResponseV0
from pyhid.hidpp.features.common.securedfucontrol import GetDfuControlResponseV1
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlFactory
from pyhid.hidpp.features.common.securedfucontrol import SetDfuControlV0
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.notifications.dfutimeout import DfuTimeout
from pyhid.hidpp.hidpp1.registers.securedfucontrol import GetDfuControlRequest
from pyhid.hidpp.hidpp1.registers.securedfucontrol import SetDfuControlRequest
from pylibrary.mcu.securitychunks import DfuCtrlChunk
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import choices
from pylibrary.tools.util import compute_inverted_bit_range
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_END_TEST_LOOP = 'End Test Loop'


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CommonSecureDfuControlTestCase(CommonBaseTestCase):
    """
    Validates Secure DFU Control TestCases
    """
    ACCEPTED_ERROR_TIMEOUT = .5  # In seconds
    TIMEOUT_TOLERANCE = 5 / 100
    MINUS_TIMEOUT_TOLERANCE = 1 - TIMEOUT_TOLERANCE
    PLUS_TIMEOUT_TOLERANCE = 1 + TIMEOUT_TOLERANCE

    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_program_mcu_initial_state = False
        self.post_requisite_force_reload_nvs = False
        self.feature_id = 0
        self.feature_under_test = None

        super().setUp()

        if self.current_channel.protocol in LogitechProtocol.gaming_protocols() and \
                self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
            # Switch to USB channel if the DUT is a gaming device, otherwise do nothing
            ProtocolManagerUtils.switch_to_usb_channel(self)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_program_mcu_initial_state:
                if self.current_channel.protocol == LogitechProtocol.USB and self.current_channel.is_open:
                    ChannelUtils.close_channel(test_case=self)
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_prerequisite(self, 'Program the MCU back to its initial state')
                # ------------------------------------------------------------------------------------------------------
                self.debugger.reload_file(firmware_hex_file=join(TESTS_PATH, "DFU_FILES",
                                                                 self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName),
                                          no_reset=True)
                self.debugger.set_application_bit(no_reset=True)
                if self.config_manager.current_protocol == LogitechProtocol.BLE_PRO:
                    # In BLE, a service changed is forced to be sure to have the right state of the receiver
                    DfuTestUtils.NvsHelper.force_service_changed(test_case=self, nvs_backup_reload=True)
                    DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
                else:
                    DfuControlTestUtils.load_nvs(test_case=self, backup=True)
                # end if

                self.post_requisite_program_mcu_initial_state = False
                self.post_requisite_force_reload_nvs = False
            elif self.post_requisite_force_reload_nvs or self.status != TYPE_SUCCESS:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reload NVS to its initial state')
                # ------------------------------------------------------------------------------------------------------
                DfuControlTestUtils.load_nvs(test_case=self, backup=True)

                if self.status != TYPE_SUCCESS:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, 'In case of test failure, the target shall be '
                                                       'forced back in Main Application mode')
                    # --------------------------------------------------------------------------------------------------
                    DfuTestUtils.force_target_on_application(test_case=self)
                # end if
            # end if
        except AttributeError:
            # AttributeError: 'ApplicationDfuControlTestCase' object has no attribute 'deviceIndex'
            pass
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
            # noinspection PyBroadException
            try:
                DfuTestUtils.force_target_on_application(test_case=self)
            except Exception:
                self.log_traceback_as_warning(supplementary_message="Could not event jump on application")
            # end try
        # end try

        # noinspection PyBroadException
        try:
            if self.backup_dut_channel.protocol in LogitechProtocol.gaming_protocols() and \
                    self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
                # Leave from USB channel if the DUT is a gaming device, otherwise do nothing
                ProtocolManagerUtils.exit_usb_channel(self)
                ChannelUtils.clean_messages(
                    test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                    class_type=WirelessDeviceStatusBroadcastEvent)
                if isinstance(self, DeviceBaseTestCase):
                    self.cleanup_battery_event_from_queue()
                # end if
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super().tearDown()
    # end def tearDown

    def _perform_business_case(self, dfu_control_param=None, add_user_action=False):
        """
        Perform a business case, it will be used in the business test but also in some other tests with fewer steps
        and checks

        :param dfu_control_param: The value of dfu_control_param. If None, it will be by default 0 and more
                                  steps/checks will be done
        :type dfu_control_param: ``int``
        :param add_user_action: Add a user action to perform when entering DFU mode
        :type add_user_action: ``bool``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        if dfu_control_param is None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
            # ----------------------------------------------------------------------------------------------------------
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send DFU setDfuControl with enableDfu=1 and dfuControlParam={dfu_control_param}')
            # ----------------------------------------------------------------------------------------------------------
        # end if
        DfuControlTestUtils.set_dfu_control(test_case=self,
                                            dfu_control_param=dfu_control_param,
                                            action_type=get_dfu_control_response.dfu_control_action_type)

        if to_int(get_dfu_control_response.dfu_control_action_type) != GetDfuControlResponseV0.ACTION.NO_ACTION:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU getDfuControl')
            # ----------------------------------------------------------------------------------------------------------
            get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=1,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')
        # end if

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            action_data = get_dfu_control_response.dfu_control_action_data
        else:
            action_data = None
        # end if

        if not add_user_action:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.perform_action_to_enter_dfu_mode(
                test_case=self,
                action_type=get_dfu_control_response.dfu_control_action_type,
                action_data=action_data)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the target reset with the requested user actions plus '
                                     'another one simultaneously')
            # ----------------------------------------------------------------------------------------------------------

            DfuControlTestUtils.perform_action_to_enter_dfu_mode(
                test_case=self,
                action_type=get_dfu_control_response.dfu_control_action_type,
                action_data=action_data,
                add_user_actions=1)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target is in Bootloader mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                        msg="Target not in bootloader")

        feature_00d0_id = None
        if dfu_control_param is None and not add_user_action:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the 0xD0 feature is supported by the target')
            # ----------------------------------------------------------------------------------------------------------
            feature_00d0_id = ChannelUtils.update_feature_mapping(self, feature_id=Dfu.FEATURE_ID)
            self.assertNotEqual(unexpected=0, obtained=feature_00d0_id, msg="No feature 0x00D0 present on the target")

            if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the Connectivity LED is slow blinking')
                # ------------------------------------------------------------------------------------------------------
                # TODO
                self.logTrace(msg="Check not done because the hardware needed to do the measurement is not present")
            # end if
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
        # --------------------------------------------------------------------------------------------------------------
        DfuTestUtils.send_dfu_restart_function(test_case=self, bootloader_dfu_feature_id=feature_00d0_id)

        if dfu_control_param is None and not add_user_action:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the target is in Main Application mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                            msg="Target not in application")

            if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the Connectivity LED goes off immediately')
                # ------------------------------------------------------------------------------------------------------
                # TODO
                self.logTrace(msg="Check not done because the hardware needed to do the measurement is not present")
            # end if
        # end if
    # end def _perform_business_case

    def generic_get_dfu_control_no_dfu_chunk_api(self):
        """
        getDfuControl API validation when no DFU chunk in NVS
        """
        if self.config_manager.current_target in [ConfigurationManager.TARGET.DEVICE,
                                                  ConfigurationManager.TARGET.RECEIVER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Invalidate all 'NVS_DFU_ID' chunks in NVS")
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        self.memory_manager.invalidate_chunks(chunk_names=['NVS_DFU_ID'])
        DfuControlTestUtils.load_nvs(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check reserved_enableDfu = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.reserved_enable_dfu),
                         msg='The reserved_enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check dfuControlParam matches product configuration')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlParam),
                             obtained=to_int(get_dfu_control_response.dfu_control_param),
                             msg='The dfu_control_param parameter differs from the expected one')
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check reserved value r1 = 0')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.reserved),
                             msg='The reserved r1 parameter differs from the expected one')
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check dfuControlTimeout matches product configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlTimeout),
                         obtained=to_int(get_dfu_control_response.dfu_control_timeout),
                         msg='The dfu_control_timeout parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check dfuControlActionType matches product configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType),
                         obtained=to_int(get_dfu_control_response.dfu_control_action_type),
                         msg='The dfu_control_action_type parameter differs from the expected one')

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check dfuControlActionData matches product configuration')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionData),
                             obtained=to_int(get_dfu_control_response.dfu_control_action_data),
                             msg='The dfu_control_action_data parameter differs from the expected one')
        # end if
    # end def generic_get_dfu_control_no_dfu_chunk_api

    def generic_get_dfu_control_dfu_enabled_in_nvs_api(self):
        """
        getDfuControl API validation when DFU enabled in NVS
        """
        self.post_requisite_force_reload_nvs = True
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'add a \'NVS_DFU_ID\' chunk with enable=1 and param=0xFF')
            # ----------------------------------------------------------------------------------------------------------
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'add a \'NVS_DFU_ID\' chunk with enable=1 and param=0xFF')
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        chunk = DfuCtrlChunk(enable=1, param=0xFF)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
        DfuControlTestUtils.load_nvs(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check reserved_enableDfu = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.reserved_enable_dfu),
                         msg='The reserved_enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check dfuControlParam matches product configuration')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlParam),
                             obtained=to_int(get_dfu_control_response.dfu_control_param),
                             msg='The dfu_control_param parameter differs from the expected one')
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check reserved value r1 = 0')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.reserved),
                             msg='The reserved r1 parameter differs from the expected one')
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check dfuControlTimeout matches product configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlTimeout),
                         obtained=to_int(get_dfu_control_response.dfu_control_timeout),
                         msg='The dfu_control_timeout parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check dfuControlActionType matches product configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType),
                         obtained=to_int(get_dfu_control_response.dfu_control_action_type),
                         msg='The dfu_control_action_type parameter differs from the expected one')

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check dfuControlActionData matches product configuration')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionData),
                             obtained=to_int(get_dfu_control_response.dfu_control_action_data),
                             msg='The dfu_control_action_data parameter differs from the expected one')
        # end if
    # end def generic_get_dfu_control_dfu_enabled_in_nvs_api

    def generic_get_dfu_control_dfu_disabled_in_nvs_api(self):
        """
        getDfuControl API validation when DFU disabled in NVS
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check reserved_enableDfu = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.reserved_enable_dfu),
                         msg='The reserved_enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check dfuControlParam matches product configuration')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlParam),
                             obtained=to_int(get_dfu_control_response.dfu_control_param),
                             msg='The dfu_control_param parameter differs from the expected one')
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check reserved value r1 = 0')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.reserved),
                             msg='The reserved r1 parameter differs from the expected one')
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check dfuControlTimeout matches product configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlTimeout),
                         obtained=to_int(get_dfu_control_response.dfu_control_timeout),
                         msg='The dfu_control_timeout parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check dfuControlActionType matches product configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType),
                         obtained=to_int(get_dfu_control_response.dfu_control_action_type),
                         msg='The dfu_control_action_type parameter differs from the expected one')

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check dfuControlActionData matches product configuration')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionData),
                             obtained=to_int(get_dfu_control_response.dfu_control_action_data),
                             msg='The dfu_control_action_data parameter differs from the expected one')
        # end if
    # end def generic_get_dfu_control_dfu_disabled_in_nvs_api

    def generic_set_dfu_control_enable_dfu_api(self):
        """
        setDfuControl API validation with DFU enable when no DFU chunk in NVS
        """
        self.post_requisite_force_reload_nvs = True

        if self.config_manager.current_target in [ConfigurationManager.TARGET.DEVICE,
                                                  ConfigurationManager.TARGET.RECEIVER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Invalidate all 'NVS_DFU_ID' chunks in NVS")
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        self.memory_manager.invalidate_chunks(chunk_names=['NVS_DFU_ID'])
        DfuControlTestUtils.load_nvs(test_case=self)

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1, dfuControlParam=0xFF')
            # ----------------------------------------------------------------------------------------------------------
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        set_dfu_control_response = DfuControlTestUtils.set_dfu_control(test_case=self,
                                                                       enable_dfu=1,
                                                                       dfu_control_param=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate all bytes in the response set to zero')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(set_dfu_control_response.padding),
                         msg='The padding parameter differs from the expected one')

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Dump the NVS and check enable byte is 1 and param is 0xFF')
            # ----------------------------------------------------------------------------------------------------------
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Dump the NVS and check enable byte is 1 and param is 0')
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        self.memory_manager.read_nvs()
        dfu_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_DFU_ID')
        self.assertEqual(expected=1,
                         obtained=to_int(dfu_chunk.enable),
                         msg='The enable parameter differs from the expected one')
        self.assertEqual(expected=0xFF if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE
                         else 0,
                         obtained=to_int(dfu_chunk.param),
                         msg='The param parameter differs from the expected one')
    # end def generic_set_dfu_control_enable_dfu_api

    def generic_set_dfu_control_disable_dfu_api(self):
        """
        setDfuControl API validation with DFU disable when no DFU chunk in NVS
        """
        if self.config_manager.current_target in [ConfigurationManager.TARGET.DEVICE,
                                                  ConfigurationManager.TARGET.RECEIVER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Invalidate all 'NVS_DFU_ID' chunks in NVS")
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        self.memory_manager.invalidate_chunks(chunk_names=['NVS_DFU_ID'])
        DfuControlTestUtils.load_nvs(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=0, dfuControlParam=0')
        # --------------------------------------------------------------------------------------------------------------
        set_dfu_control_response = DfuControlTestUtils.set_dfu_control(test_case=self,
                                                                       enable_dfu=0,
                                                                       dfu_control_param=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate all bytes in the response set to zero')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(set_dfu_control_response.padding),
                         msg='The padding parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and check enable byte is 0 and param is 0')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        dfu_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_DFU_ID')
        self.assertEqual(expected=0,
                         obtained=to_int(dfu_chunk.enable),
                         msg='The enable parameter differs from the expected one')
        self.assertEqual(expected=0,
                         obtained=to_int(dfu_chunk.param),
                         msg='The enable parameter differs from the expected one')
    # end def generic_set_dfu_control_disable_dfu_api

    def generic_dfu_control_business(self):
        """
        DFU Control business case when enable DFU mode is requested. Check target is in bootloader mode after a reset
        is performed with the requested user actions. Check 0xD0 feature is advertised in bootloader mode.
        If the target is a device, it checks DFU status LED starts blinking when entering bootloader mode and stops
        immediately when it leaves this mode.
        """
        self._perform_business_case()
    # end def generic_dfu_control_business

    def generic_perform_action_when_dfu_disabled(self):
        """
        DFU Control use case when enable DFU mode is NOT requested. Check target stays in application mode after a
        reset is performed with the requested user actions.
        """
        if (self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType
                not in [GetDfuControlResponseV1.ACTION.ON_SCREEN_CONFIRMATION]):
            if self.config_manager.current_target in [ConfigurationManager.TARGET.DEVICE,
                                                      ConfigurationManager.TARGET.RECEIVER]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_prerequisite(self, "Add a 'NVS_DFU_ID' chunk with enable=1")
                # ------------------------------------------------------------------------------------------------------
            else:
                raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
            # end if
            chunk = DfuCtrlChunk(enable=1, param=0)
            self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
            DfuControlTestUtils.load_nvs(test_case=self)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self, dfu_enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target stays in application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                        msg="Target not in application")

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the Connectivity LED stays off')
            # ----------------------------------------------------------------------------------------------------------
            # TODO
            self.logTrace(msg="Check not done because the hardware needed to do the measurement is not present")
        # end if
    # end def generic_perform_action_when_dfu_disabled

    def generic_perform_action_when_dfu_enabled_then_disabled(self):
        """
        Cancel a previous enable DFU request. Check target stays in application mode after a reset is performed with
        the requested user actions.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self, dfu_enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target stays in application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                        msg="Target not in application")

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the Connectivity LED stays off')
            # ----------------------------------------------------------------------------------------------------------
            # TODO
            self.logTrace(msg="Check not done because the hardware needed to do the measurement is not present")
        # end if
    # end def generic_perform_action_when_dfu_enabled_then_disabled

    def generic_perform_action_when_just_before_timeout(self):
        """
        DFU Control Timeout: Enable DFU mode is requested and reset is performed just before the end of the DFU control
        timeout. Check target is in bootloader mode after a reset is performed with the requested user actions.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # A delay is needed because the wait is done after sending getDfuControl which can add some time.
        # It is set before sending getDfuControl because it can take some time to get the response (especially
        # if a packet is missed, one measurement showed a delay of 6s...)
        delay_start = time()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for the duration of the timeout minus 5% tolerance')
        # --------------------------------------------------------------------------------------------------------------
        time_to_close_channel = 0
        if self.config_manager.current_protocol == LogitechProtocol.USB and self.current_channel.is_open:
            # In USB, channel has to be closed. This takes some time and has to be anticipated. Experience shows that
            # it takes a bit more than 1.5 seconds most of the time.
            time_to_close_channel = 1.5
        # end if
        # It is mandatory to check that the delay wanted has not already been exceeded before arriving here
        delay_time = time() - delay_start + time_to_close_channel
        self.assertGreater(a=self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout),
                           b=delay_time,
                           msg="The delay to wait has been exceeded before we arrive here")
        sleep(self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout) - delay_time)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target stays in bootloader mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                        msg="Target not in bootloader")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
        # --------------------------------------------------------------------------------------------------------------
        DfuTestUtils.send_dfu_restart_function(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target is in Main Application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                        msg="Target not in application")
    # end def generic_perform_action_when_just_before_timeout

    def generic_perform_action_when_just_after_timeout(self):
        """
        DFU Control Timeout: Enable DFU mode is requested and reset is performed just after the DFU control
        timeout. Check target stays in application mode after the reset is performed with the requested user actions.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # A delay is needed because the wait is done after sending getDfuControl which can add some time.
        # It is set before sending getDfuControl because it can take some time to get the response (especially
        # if a packet is missed, one measurement showed a delay of 6s...)
        delay_start = time()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for the duration of the timeout minus 5% tolerance')
        # --------------------------------------------------------------------------------------------------------------
        # It is mandatory to check that the timeout has not already been exceeded before arriving here.
        delay_time = time() - delay_start
        self.assertGreater(a=self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout),
                           b=delay_time,
                           msg="The timeout to wait has been exceeded before we arrive here")
        sleep(self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout) - delay_time)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the dfuTimeoutEvent notification')
        # --------------------------------------------------------------------------------------------------------------
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            dfu_control_interface = SecureDfuControlFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL))
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=dfu_control_interface.dfu_timeout_event_cls, check_first_message=False)
            self.assertGreater(a=self.PLUS_TIMEOUT_TOLERANCE * (to_int(get_dfu_control_response.dfu_control_timeout)),
                               b=time() - delay_start,
                               msg="dfuTimeoutEvent took too long to be received, the timout is not the right value")
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=DfuTimeout, check_first_message=False)
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self, dfu_enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target stays in Main Application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                        msg="Target not in application")
        self.cleanup_battery_event_from_queue()

        if (self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType
                not in [GetDfuControlResponseV1.ACTION.ON_SCREEN_CONFIRMATION]):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Dump the NVS and check enable byte is 0')
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.read_nvs()
            dfu_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_DFU_ID')
            self.assertEqual(expected=0,
                             obtained=to_int(dfu_chunk.enable),
                             msg='The enable parameter differs from the expected one')
        # end if
    # end def generic_perform_action_when_just_after_timeout

    def generic_perform_action_when_just_before_timeout_after_restarting_it(self):
        """
        DFU Control Timeout restart: Send multiple enable DFU mode requests and validate the DFU control timeout
        restarts each time from zero. Check target is in bootloader mode after the reset performed with the requested
        user actions.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # A delay is needed because the wait is done after sending getDfuControl which can add some time.
        # It is set before sending getDfuControl because it can take some time to get the response (especially
        # if a packet is missed, one measurement showed a delay of 6s...)
        delay_start = time()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for half the timeout')
        # --------------------------------------------------------------------------------------------------------------
        # It is mandatory to check that the timeout (minus 1s) has not already been exceeded before arriving here.
        # Since the test is about restarting the timeout it is ok to check the timeout value is not reached and not
        # just the wanted delay in this Test Step.
        delay_time = time() - delay_start
        self.assertGreater(a=to_int(get_dfu_control_response.dfu_control_timeout) - 1,
                           b=delay_time,
                           msg="The timeout to wait has been exceeded before we arrive here")

        if delay_time <= to_int(get_dfu_control_response.dfu_control_timeout)//2:
            sleep(to_int(get_dfu_control_response.dfu_control_timeout)//2 - delay_time)
        else:
            self.log_warning(message="Waited more than half the timout but less than the timout itself (minus 1)")
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Resend DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # A delay is needed because the wait is done after sending getDfuControl which can add some time.
        # It is set before sending getDfuControl because it can take some time to get the response (especially
        # if a packet is missed, one measurement showed a delay of 6s...)
        delay_start = time()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for the duration of the timeout minus 1 second')
        # --------------------------------------------------------------------------------------------------------------
        time_to_close_channel = 0
        if self.config_manager.current_protocol == LogitechProtocol.USB and self.current_channel.is_open:
            # In USB, channel has to be closed. This takes some time and has to be anticipated. Experience shows that
            # it takes a bit more than 1.5 seconds most of the time.
            time_to_close_channel = 1.5
        # end if
        # It is mandatory to check that the delay wanted has not already been exceeded before arriving here
        delay_time = time() - delay_start + time_to_close_channel
        self.assertGreater(a=self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout),
                           b=delay_time,
                           msg="The delay to wait has been exceeded before we arrive here")
        sleep(self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout) - delay_time)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target stays in bootloader mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                        msg="Target not in bootloader")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
        # --------------------------------------------------------------------------------------------------------------
        DfuTestUtils.send_dfu_restart_function(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target is in Main Application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                        msg="Target not in application")
    # end def generic_perform_action_when_just_before_timeout_after_restarting_it

    def generic_perform_action_when_just_after_timeout_after_restarting_it(self):
        """
        DFU Control Timeout restart: Send multiple enable Dfu mode requests and validate the timeout notification is
        returned after the correct delay following the last request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # A delay is needed because the wait is done after sending getDfuControl which can add some time.
        # It is set before sending getDfuControl because it can take some time to get the response (especially
        # if a packet is missed, one measurement showed a delay of 6s...)
        delay_start = time()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for half the timeout')
        # --------------------------------------------------------------------------------------------------------------
        # It is mandatory to check that the timeout (minus 1s) has not already been exceeded before arriving here.
        # Since the test is about restarting the timeout it is ok to check the timeout value is not reached and not
        # just the wanted delay in this Test Step.
        delay_time = time() - delay_start
        self.assertGreater(a=to_int(get_dfu_control_response.dfu_control_timeout) - 1,
                           b=delay_time,
                           msg="The timeout to wait has been exceeded before we arrive here")

        if delay_time <= to_int(get_dfu_control_response.dfu_control_timeout)//2:
            sleep(to_int(get_dfu_control_response.dfu_control_timeout)//2 - delay_time)
        else:
            self.log_warning(message="Waited more than half the timout but less than the timout itself (minus 1)")
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Resend DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # A delay is needed because the wait is done after sending getDfuControl which can add some time.
        # It is set before sending getDfuControl because it can take some time to get the response (especially
        # if a packet is missed, one measurement showed a delay of 6s...)
        delay_start = time()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for the duration of the timeout minus 5% tolerance')
        # --------------------------------------------------------------------------------------------------------------
        # It is mandatory to check that the timeout has not already been exceeded before arriving here.
        delay_time = time() - delay_start
        self.assertGreater(a=self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout),
                           b=delay_time,
                           msg="The timeout to wait has been exceeded before we arrive here")
        sleep(self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout) - delay_time)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the dfuTimeoutEvent notification')
        # --------------------------------------------------------------------------------------------------------------
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            dfu_control_interface = SecureDfuControlFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL))
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=dfu_control_interface.dfu_timeout_event_cls, check_first_message=False)
            self.assertGreater(a=self.PLUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout),
                               b=time() - delay_start,
                               msg="dfuTimeoutEvent took too long to be received, the timout is not the right value")
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=DfuTimeout, check_first_message=False)
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self, dfu_enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target stays in Main Application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                        msg="Target not in application")
        self.cleanup_battery_event_from_queue()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and check enable byte is 0')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        dfu_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_DFU_ID')
        self.assertEqual(expected=0,
                         obtained=to_int(dfu_chunk.enable),
                         msg='The enable parameter differs from the expected one')
    # end def generic_perform_action_when_just_after_timeout_after_restarting_it

    def generic_get_dfu_control_do_not_influence_timeout(self):
        """
        DFU Control Timeout: Send multiple getDfuControl requests and validate the DFU control timeout does NOT
        restart each time from zero. Check device stays in application mode after the reset performed with the
        requested user actions.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # A delay is needed because the wait is done after sending getDfuControl which can add some time.
        # It is set before sending getDfuControl because it can take some time to get the response (especially
        # if a packet is missed, one measurement showed a delay of 6s...)
        delay_start = time()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for the getDfuControl response and check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for half the timeout')
        # --------------------------------------------------------------------------------------------------------------
        # It is mandatory to check that the timeout (minus 1s) has not already been exceeded before arriving here.
        # Since the test is about restarting the timeout it is ok to check the timeout value is not reached and not
        # just the wanted delay in this Test Step.
        delay_time = time() - delay_start
        self.assertGreater(a=to_int(get_dfu_control_response.dfu_control_timeout) - 1,
                           b=delay_time,
                           msg="The timeout to wait has been exceeded before we arrive here")

        if delay_time <= to_int(get_dfu_control_response.dfu_control_timeout)//2:
            sleep(to_int(get_dfu_control_response.dfu_control_timeout)//2 - delay_time)
        else:
            self.log_warning(message="Waited more than half the timout but less than the timout itself (minus 1)")
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Resend DFU getDfuControl request')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do nothing for the second half of the timeout minus 5% tolerance')
        # --------------------------------------------------------------------------------------------------------------
        # It is mandatory to check that the timeout has not already been exceeded before arriving here.
        delay_time = time() - delay_start
        self.assertGreater(a=self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout),
                           b=delay_time,
                           msg="The timeout to wait has been exceeded before we arrive here")
        sleep(self.MINUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout) - delay_time)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the dfuTimeoutEvent notification')
        # --------------------------------------------------------------------------------------------------------------
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            dfu_control_interface = SecureDfuControlFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL))
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=dfu_control_interface.dfu_timeout_event_cls, check_first_message=False)
            self.assertGreater(a=self.PLUS_TIMEOUT_TOLERANCE * to_int(get_dfu_control_response.dfu_control_timeout),
                               b=time() - delay_start,
                               msg="dfuTimeoutEvent took too long to be received, the timout is not the right value")
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=DfuTimeout, check_first_message=False)
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
    # end def generic_get_dfu_control_do_not_influence_timeout

    def generic_soft_reset_do_not_jump_on_bootloader(self):
        """
        DFU Control reset type. Check target stays in application mode after a Soft reset is performed with the
        requested user actions. Check the DFU enable NVS state is not modified by a soft reset.
        """
        self.post_requisite_force_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a target soft reset with all the requested user actions')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self, force_soft_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target stays in Main Application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                        msg="Target not in application")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and check enable byte is 1')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        dfu_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_DFU_ID')
        self.assertEqual(expected=1,
                         obtained=to_int(dfu_chunk.enable),
                         msg='The enable parameter differs from the expected one')
    # end def generic_soft_reset_do_not_jump_on_bootloader

    def generic_nvs_chunk_dfu_disabled_to_enabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not match the
        request:
        - setDfuControl with DFU enabled when DFU disabled in NVS
        """
        self.post_requisite_force_reload_nvs = True

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'add a \'NVS_DFU_ID\' chunk with enable=0')
            # ----------------------------------------------------------------------------------------------------------
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'add a \'NVS_DFU_ID\' chunk with enable=0')
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        chunk = DfuCtrlChunk(enable=0, param=0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
        DfuControlTestUtils.load_nvs(test_case=self)
        dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify a new chunk has been added with enable=1')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        new_dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')
        self.assertEqual(expected=len(dfu_chunk_history) + 1,
                         obtained=len(new_dfu_chunk_history),
                         msg='The number of DFU chunk in history is not the expected one')
        self.assertEqual(expected=1,
                         obtained=to_int(new_dfu_chunk_history[-1].chunk_data[0]),
                         msg='The enable parameter differs from the expected one')
    # end def generic_nvs_chunk_dfu_disabled_to_enabled

    def generic_nvs_chunk_dfu_enabled_to_disabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not match the
        request:
        - setDfuControl with DFU disabled when DFU enabled in NVS
        """
        if self.config_manager.current_target in [ConfigurationManager.TARGET.DEVICE,
                                                  ConfigurationManager.TARGET.RECEIVER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Add a 'NVS_DFU_ID' chunk with enable=1")
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        chunk = DfuCtrlChunk(enable=1, param=0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
        DfuControlTestUtils.load_nvs(test_case=self)
        dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify a new chunk has been added with enable=0')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        new_dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')
        self.assertEqual(expected=len(dfu_chunk_history) + 1,
                         obtained=len(new_dfu_chunk_history),
                         msg='The number of DFU chunk in history is not the expected one')
        self.assertEqual(expected=0,
                         obtained=to_int(new_dfu_chunk_history[-1].chunk_data[0]),
                         msg='The enable parameter differs from the expected one')
    # end def generic_nvs_chunk_dfu_enabled_to_disabled

    def generic_nvs_chunk_dfu_enabled_to_enable(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not match the
        request:
        - setDfuControl with DFU enabled when DFU already enabled in NVS
        """
        self.post_requisite_force_reload_nvs = True

        if self.config_manager.current_target in [ConfigurationManager.TARGET.DEVICE,
                                                  ConfigurationManager.TARGET.RECEIVER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Add a 'NVS_DFU_ID' chunk with enable=1")
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        chunk = DfuCtrlChunk(enable=1, param=0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
        DfuControlTestUtils.load_nvs(test_case=self)
        dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify a new chunk has been added with enable=0')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        new_dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')
        self.assertEqual(expected=len(dfu_chunk_history),
                         obtained=len(new_dfu_chunk_history),
                         msg='The number of DFU chunk in history is not the expected one')
    # end def generic_nvs_chunk_dfu_enabled_to_enable

    def generic_nvs_chunk_dfu_disabled_to_disabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not match the
        request:
        - setDfuControl with DFU disabled when DFU already disabled in NVS
        """
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'add a \'NVS_DFU_ID\' chunk with enable=0')
            # ----------------------------------------------------------------------------------------------------------
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'add a \'NVS_DFU_ID\' chunk with enable=0')
            # ----------------------------------------------------------------------------------------------------------
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if
        chunk = DfuCtrlChunk(enable=0, param=0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
        DfuControlTestUtils.load_nvs(test_case=self)
        dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=0')
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify a new chunk has been added with enable=0')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        new_dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')
        self.assertEqual(expected=len(dfu_chunk_history),
                         obtained=len(new_dfu_chunk_history),
                         msg='The number of DFU chunk in history is not the expected one')
    # end def generic_nvs_chunk_dfu_disabled_to_disabled

    def generic_get_dfu_control_enable_in_nvs_superior_to_1(self):
        """
        getDfuControl when enable byte value greater than 1 in NVS but with enable bit to 1 should return enable = 1
        and all reserved bit to 0
        """
        self.post_requisite_force_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test loop over some NVS chunk enable values other than 0 and 1')
        # --------------------------------------------------------------------------------------------------------------
        for enable in compute_wrong_range(value=[0x00, 0x01], max_value=0xFF, min_value=0x02):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'add a \'NVS_DFU_ID\' chunk with enable={enable}')
            # ----------------------------------------------------------------------------------------------------------
            chunk = DfuCtrlChunk(enable=enable, param=0)
            self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
            DfuControlTestUtils.load_nvs(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU getDfuControl')
            # ----------------------------------------------------------------------------------------------------------
            get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1 and '
                                      'reserved_enable=0')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=1,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.reserved_enable_dfu),
                             msg='The reserved_enable_dfu parameter differs from the expected one')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_get_dfu_control_enable_in_nvs_superior_to_1

    def generic_entering_dfu_enable_in_nvs_superior_to_1(self):
        """
        getDfuControl when enable byte value greater than 1 in NVS but with enable bit to 1. Check target is in
        bootloader mode after the reset performed with the requested user actions
        """
        self.post_requisite_force_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test loop over some NVS chunk enable values superior to 1')
        # --------------------------------------------------------------------------------------------------------------
        for enable in compute_wrong_range(value=[0x00, 0x01], max_value=0xFF, min_value=0x02):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'add a \'NVS_DFU_ID\' chunk with enable={enable}')
            # ----------------------------------------------------------------------------------------------------------
            chunk = DfuCtrlChunk(enable=enable, param=0)
            self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
            DfuControlTestUtils.load_nvs(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the target is in Bootloader mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                            msg="Target not in bootloader")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
            # ----------------------------------------------------------------------------------------------------------
            DfuTestUtils.send_dfu_restart_function(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the target is in Main Application mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                            msg="Target not in application")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(_END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_entering_dfu_enable_in_nvs_superior_to_1

    def generic_entering_dfu_param_in_nvs_superior_to_0(self):
        """
        Send getDfuControl when the param value is greater than 0 in NVS.
        Check target is in bootloader mode after the reset performed with the requested user actions
        """
        self.post_requisite_force_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test loop over some NVS chunk param values other than 0')
        # --------------------------------------------------------------------------------------------------------------
        for param in compute_wrong_range(value=0x00, max_value=0xFF, min_value=0x01):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'add a \'NVS_DFU_ID\' chunk with enable=1 and param={param}')
            # ----------------------------------------------------------------------------------------------------------
            chunk = DfuCtrlChunk(enable=1, param=param)
            self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
            DfuControlTestUtils.load_nvs(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the target is in Bootloader mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                            msg="Target not in bootloader")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
            # ----------------------------------------------------------------------------------------------------------
            DfuTestUtils.send_dfu_restart_function(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the target is in Main Application mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                            msg="Target not in application")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(_END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_entering_dfu_param_in_nvs_superior_to_0

    def generic_set_dfu_control_reserved_enable_ignored(self):
        """
        setDfuControl processing shall ignore bits which are reserved for future use in the first enableDfu byte
        """
        self.post_requisite_force_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test loop over some reserved_enable_dfu values other than 0')
        # --------------------------------------------------------------------------------------------------------------
        for reserved_enable_dfu in compute_wrong_range(value=0x00, max_value=0x7F, min_value=0x01):
            if (self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType
                    not in [GetDfuControlResponseV1.ACTION.ON_SCREEN_CONFIRMATION]):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Add a "NVS_DFU_ID" chunk with enable=0')
                # ------------------------------------------------------------------------------------------------------
                chunk = DfuCtrlChunk(enable=0, param=0)
                self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
                DfuControlTestUtils.load_nvs(test_case=self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send DFU setDfuControl with enableDfu=1 and '
                                     f'reserved_enable_dfu={reserved_enable_dfu}')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1, reserved_enable_dfu=reserved_enable_dfu)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU getDfuControl')
            # ------------------------------------------------------------------------------------------------------
            get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1 and '
                                      'reserved_enable_dfu=0')
            # ------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=1,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.reserved_enable_dfu),
                             msg='The reserved_enable_dfu parameter differs from the expected one')

            if (self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType
                    not in [GetDfuControlResponseV1.ACTION.ON_SCREEN_CONFIRMATION]):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Dump the NVS and verify the chunk has enable=1')
                # ------------------------------------------------------------------------------------------------------
                self.memory_manager.read_nvs()
                new_dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')
                self.assertEqual(expected=1,
                                 obtained=to_int(new_dfu_chunk_history[-1].chunk_data[0]),
                                 msg='The enable parameter differs from the expected one')
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_set_dfu_control_reserved_enable_ignored

    def generic_set_dfu_control_reserved_ignored(self):
        """
        setDfuControl processing shall ignore bytes which are reserved for future use
        """
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            dfu_control_interface = SecureDfuControlFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL))
            set_dfu_control_class = dfu_control_interface.set_dfu_control_cls
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            set_dfu_control_class = SetDfuControlRequest
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test loop over some reserved values other than 0')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_force_reload_nvs = True
        for reserved in compute_wrong_range(value=0, max_value=pow(2, set_dfu_control_class.LEN.RESERVED) - 1,
                                            min_value=0x01):
            if (self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType
                    not in [GetDfuControlResponseV1.ACTION.ON_SCREEN_CONFIRMATION]):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Add a "NVS_DFU_ID" chunk with enable=0')
                # ------------------------------------------------------------------------------------------------------
                chunk = DfuCtrlChunk(enable=0, param=0)
                self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
                DfuControlTestUtils.load_nvs(test_case=self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send DFU setDfuControl with enableDfu=1 and reserved={reserved}')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1, reserved=reserved)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU getDfuControl')
            # ----------------------------------------------------------------------------------------------------------
            get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=1,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')

            if (self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType
                    not in [GetDfuControlResponseV1.ACTION.ON_SCREEN_CONFIRMATION]):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Dump the NVS and verify the chunk has enable=1')
                # ------------------------------------------------------------------------------------------------------
                self.memory_manager.read_nvs()
                new_dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')
                self.assertEqual(expected=1,
                                 obtained=to_int(new_dfu_chunk_history[-1].chunk_data[0]),
                                 msg='The enable parameter differs from the expected one')
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_set_dfu_control_reserved_ignored

    def generic_set_dfu_control_wrong_magic_key(self):
        """
        setDfuControl processing shall enforce the magic key value - Every bit flipped combination shall be verified
        """
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            correct_magic_key = SetDfuControlV0.DEFAULT.DFU_MAGIC_KEY
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            correct_magic_key = SetDfuControlRequest.DEFAULT.DFU_MAGIC_KEY
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'add a \'NVS_DFU_ID\' chunk with enable=0')
        # --------------------------------------------------------------------------------------------------------------
        chunk = DfuCtrlChunk(enable=0, param=0)
        self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
        DfuControlTestUtils.load_nvs(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over magic_key value bit flipped combination')
        # --------------------------------------------------------------------------------------------------------------
        for wrong_magic_key in compute_inverted_bit_range(HexList(Numeral(correct_magic_key))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Send DFU setDfuControl with enableDfu=1 and dfu_magic_key={wrong_magic_key}')
            # ----------------------------------------------------------------------------------------------------------
            set_dfu_control_response = DfuControlTestUtils.set_dfu_control(test_case=self,
                                                                           enable_dfu=1,
                                                                           dfu_magic_key=wrong_magic_key)

            if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, 'Check HIDPP_ERR_INVALID_ARGUMENT (0x02) Error Code returned by the target')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                                 obtained=to_int(set_dfu_control_response.errorCode),
                                 msg='The errorCode parameter differs from the one expected')
            elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, 'Check ERR_INVALID_PARAM_VALUE (0x0B) Error Code returned by the receiver')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                                 obtained=to_int(set_dfu_control_response.error_code),
                                 msg='The error_code parameter differs from the one expected')
            else:
                raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU getDfuControl')
            # ----------------------------------------------------------------------------------------------------------
            get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=0')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Dump the NVS and verify the chunk has enable=0')
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.read_nvs()
            new_dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')
            self.assertEqual(expected=0,
                             obtained=to_int(new_dfu_chunk_history[-1].chunk_data[0]),
                             msg='The enable parameter differs from the expected one')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_set_dfu_control_wrong_magic_key

    def generic_get_dfu_control_padding_ignored(self):
        """
        Validates getDfuControl padding bytes are ignored
        """
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            dfu_control_interface = SecureDfuControlFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL))
            get_dfu_control_class = dfu_control_interface.get_dfu_control_cls
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            get_dfu_control_class = GetDfuControlRequest
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over getDfuControl padding range')
        # --------------------------------------------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(get_dfu_control_class.DEFAULT.PADDING,
                                                               get_dfu_control_class.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getDfuControl with padding={padding_byte}')
            # ----------------------------------------------------------------------------------------------------------
            get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self, padding=padding_byte)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetDfuStatus response')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.reserved_enable_dfu),
                             msg='The reserved_enable_dfu parameter differs from the expected one')
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')
            if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
                self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlParam),
                                 obtained=to_int(get_dfu_control_response.dfu_control_param),
                                 msg='The dfu_control_param parameter differs from the expected one')
            elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
                self.assertEqual(expected=0,
                                 obtained=to_int(get_dfu_control_response.reserved),
                                 msg='The reserved r1 parameter differs from the expected one')
            else:
                raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
            # end if
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlTimeout),
                             obtained=to_int(get_dfu_control_response.dfu_control_timeout),
                             msg='The dfu_control_timeout parameter differs from the expected one')
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType),
                             obtained=to_int(get_dfu_control_response.dfu_control_action_type),
                             msg='The dfu_control_action_type parameter differs from the expected one')
            if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
                self.assertEqual(
                            expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionData),
                            obtained=to_int(get_dfu_control_response.dfu_control_action_data),
                            msg='The dfu_control_action_data parameter differs from the expected one')
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_get_dfu_control_padding_ignored

    def generic_set_dfu_control_padding_ignored(self):
        """
        Validates setDfuControl padding bytes are ignored
        """
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            dfu_control_interface = SecureDfuControlFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL))
            set_dfu_control_class = dfu_control_interface.set_dfu_control_cls
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            set_dfu_control_class = SetDfuControlRequest
        else:
            raise ValueError(f'Unknown target configuration: {self.config_manager.current_target}')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check enable_dfu=0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over setDfuControl padding range')
        # --------------------------------------------------------------------------------------------------------------
        for padding in choices(compute_sup_values(HexList(Numeral(
                set_dfu_control_class.DEFAULT.PADDING, set_dfu_control_class.LEN.PADDING // 8))), 10):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send DFU setDfuControl with padding = {padding}, enable_dfu=1 '
                                     f'and the correct magicKey')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the target reset with the requested user actions simultaneously')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.perform_action_to_enter_dfu_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the target is in Bootloader mode')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                            msg="Target not in bootloader")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
            # ----------------------------------------------------------------------------------------------------------
            DfuTestUtils.send_dfu_restart_function(test_case=self)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(_END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
    # end def generic_set_dfu_control_padding_ignored

    def generic_set_get_dfu_control(self):
        """
        Set DFU control to enabled then check state using get DFU control

        :return: the response to Get DFU control providing the dfu Control Action Type & Data
        :rtype: ``GetDfuControlResponseV0``
        """
        self.post_requisite_force_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enable_dfu=1 and the correct magicKey')
        # --------------------------------------------------------------------------------------------------------------
        set_dfu_control = self.feature_under_test.set_dfu_control_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id, enable_dfu=1)

        ChannelUtils.send(
            test_case=self,
            report=set_dfu_control,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_under_test.set_dfu_control_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # --------------------------------------------------------------------------------------------------------------
        get_dfu_control = self.feature_under_test.get_dfu_control_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id)
        get_dfu_control_response = ChannelUtils.send(
            test_case=self,
            report=get_dfu_control,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_under_test.get_dfu_control_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')
        return get_dfu_control_response
    # end def generic_set_get_dfu_control
# end class CommonSecureDfuControlTestCase


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
