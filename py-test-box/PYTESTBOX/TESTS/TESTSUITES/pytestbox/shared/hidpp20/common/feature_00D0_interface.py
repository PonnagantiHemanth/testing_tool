#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.hidpp20.common.feature_00D0_interface
    :brief: Shared HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from os.path import join


from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationFactory
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.tools.numeral import Numeral
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.dfuprocessing import CommonDfuTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedDfuTestCaseInterface(CommonDfuTestCase):
    """
    Validate DFU Interface TestCases
    """

    @features('Feature00D0')
    @level('Interface')
    def test_DfuStartDfuStatusAPI(self):
        """
        Validate dfuStart and dfuStatus functions interface

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param
        """
        dfu_start_class = self.get_dfu_start_class()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuStart with fwEntity = 0xFF')
        # ---------------------------------------------------------------------------
        dfu_start = dfu_start_class(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.bootloader_dfu_feature_id,
            fw_entity=0xFF, encrypt=int(self.f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
            magic_str=self.format_magic_string_hex_list(self.f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
            flag=int(self.f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
            secur_lvl=int(self.f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))

        dfu_status_response = ChannelUtils.send(
                test_case=self,
                report=dfu_start,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        self.testCaseChecked("FUN_00D0_0001")
        self.testCaseChecked("FUN_00D0_0004")
    # end def test_DfuStartDfuStatusAPI

    @features('Feature00D0')
    @level('Interface')
    def test_RestartAPI(self):
        """
        Validate restart function interface

        [5] restart(fwEntity) -> pktNb, status, param
        """

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=1,
            log_check=1)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=2, log_check=2)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_restart_in_main_application = False

        self.testCaseChecked("FUN_00D0_0002")
    # end def test_RestartAPI

    @features('Feature00D0')
    @level('Interface')
    @services('Debugger')
    def test_DfuCmdDataXAPI(self):
        """
        Validate dfuCmdData0, dfuCmdData1, dfuCmdData2, dfuCmdData3 functions interface

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=ChannelUtils.get_device_index(test_case=self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
                test_case=self,
                report=dfu_file_parser.dfu_start_command,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        sequence_number = 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send dfuCmdData{sequence_number % 4} : next 16 bytes of '
                                     'Regular_application.dfu file is command 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=self,
                report=cmd_1,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            for i in range(len(program_data_list)):
                # ---------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send dfuCmdData{sequence_number % 4} : next 16 bytes of '
                                         f'Regular_application.dfu file is program data packet {i+1}')
                # ---------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self,
                    report=program_data_list[i],
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and '
                                          f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1

                if sequence_number > 4:
                    break
                # end if
            # end for
            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ---------------------------------------------------------------------------

            if sequence_number > 4:
                break
            # end if
        # end for

        self.testCaseChecked("FUN_00D0_0003")
    # end def test_DfuCmdDataXAPI

    @features('Feature00D0')
    @level('Interface')
    @services('Debugger')
    @bugtracker('Companion_WrongEntityType')
    def test_device_information_while_app_dfu_ongoing(self):
        """
        Check 0x0003 GetFWInfo parameters while an application dfu installation is on-going
        (App entity is not valid)
        """
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=ChannelUtils.get_device_index(test_case=self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self,
            report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature(0x0003)')
        LogHelper.log_step(self, 'Send DeviceInformation.GetFwInfo')
        # ---------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)

        for entity_index in range(self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount):
            get_fw_info_response = DeviceInformationTestUtils.HIDppHelper.get_fw_info(
                test_case=self, entity_index=entity_index, device_index=ChannelUtils.get_device_index(test_case=self))

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetFwInfo response and check parameters are zeroed')
            # ----------------------------------------------------------------------------
            if int(Numeral(get_fw_info_response.fw_type)) == DeviceInformation.EntityTypeV1.MAIN_APP:
                DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                    self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls,
                    DeviceInformationTestUtils.GetFwInfoResponseChecker.get_check_erased_entity(self, entity_index))
            else:
                DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                    self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls,
                    DeviceInformationTestUtils.GetFwInfoResponseChecker.get_check_map_for_entity(self, entity_index))
            # end if
        # end for

        self.testCaseChecked("FUN_00D0_0048")
    # end def test_device_information_while_app_dfu_ongoing

    @features('Feature00D0SoftDevice')
    @features('NoFeature00D0DfuInPlace')
    @level('Interface')
    @services('Debugger')
    def test_device_information_while_sd_dfu_ongoing(self):
        """
        Check 0x0003 GetFWInfo parameters while a soft device dfu installation is on-going
        (App entity is not valid)
        """
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=ChannelUtils.get_device_index(test_case=self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuStart : 16 first bytes of Regular_softdevice.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self,
            report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature(0x0003)')
        LogHelper.log_step(self, 'Send DeviceInformation.GetFwInfo')
        # ---------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)

        for entity_index in range(self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount):
            get_fw_info_response = DeviceInformationTestUtils.HIDppHelper.get_fw_info(
                test_case=self, entity_index=entity_index, device_index=ChannelUtils.get_device_index(test_case=self))

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetFwInfo response and check parameters are zeroed')
            # ----------------------------------------------------------------------------
            if int(Numeral(get_fw_info_response.fw_type)) == DeviceInformation.EntityTypeV1.MAIN_APP:
                DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                    self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls,
                    DeviceInformationTestUtils.GetFwInfoResponseChecker.get_check_erased_entity(self, entity_index))
            else:
                DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                    self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls,
                    DeviceInformationTestUtils.GetFwInfoResponseChecker.get_check_map_for_entity(self, entity_index))
            # end if
        # end for

        self.testCaseChecked("FUN_00D0_0049")
    # end def test_device_information_while_sd_dfu_ongoing

    @features('Feature00D0SoftDevice')
    @features('Feature00D0DfuInPlace')
    @level('Interface')
    @services('Debugger')
    @bugtracker('Mezzy_DfuInPlace_WrongEntityType')
    def test_device_information_while_sd_dfu_in_place_ongoing(self):
        """
        Check 0x0003 GetFWInfo parameters while a soft device 'dfu in place' installation is on-going
        (SD & App entities are not valid)
        """
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=ChannelUtils.get_device_index(test_case=self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuStart : 16 first bytes of Regular_softdevice.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self,
            report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature(0x0003)')
        LogHelper.log_step(self, 'Send DeviceInformation.GetFwInfo')
        # ---------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)

        for entity_index in range(self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount):
            get_fw_info_response = DeviceInformationTestUtils.HIDppHelper.get_fw_info(
                test_case=self, entity_index=entity_index, device_index=ChannelUtils.get_device_index(test_case=self))

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetFwInfo response and check parameters are zeroed')
            # ----------------------------------------------------------------------------
            if (int(Numeral(get_fw_info_response.fw_type)) == DeviceInformation.EntityTypeV1.MAIN_APP) or (
                    int(Numeral(get_fw_info_response.fw_type)) == DeviceInformation.EntityTypeV1.SOFTDEVICE):
                DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                    self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls,
                    DeviceInformationTestUtils.GetFwInfoResponseChecker.get_check_erased_entity(self, entity_index))
            else:
                DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                    self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls,
                    DeviceInformationTestUtils.GetFwInfoResponseChecker.get_check_map_for_entity(self, entity_index))
            # end if
        # end for

        self.testCaseChecked("FUN_00D0_0050")
    # end def test_device_information_while_sd_dfu_in_place_ongoing
# end class SharedDfuTestCaseInterface

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
