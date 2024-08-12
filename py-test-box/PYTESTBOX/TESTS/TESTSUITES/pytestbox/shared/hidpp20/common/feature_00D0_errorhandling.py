#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hidpp20.common.feature_00D0_errorhandling
:brief: Shared HID++ 2.0 Common feature 0x00D0
:author: Stanislas Cottard
:date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from os.path import join
from random import randint

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd1or2
from pyhid.hidpp.features.common.dfu import DfuCmdDataXData
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.features.common.dfu import Restart
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_wrong_range
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
class SharedDfuTestCaseErrorHandling(CommonDfuTestCase):
    """
    Validates DFU ErrorHandling TestCases
    """
    DFU_APP = 'application'
    DFU_IMAGE = 'images'

    def _wrong_sequence_number(self, dfu=DFU_APP):
        """
        Sending a wrong sequence number in dfuCmdDatax shall raise an error 'Bad sequence number'
        """
        f = self.getFeatures()
        dfu_file = f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName if dfu == self.DFU_APP else \
            f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesDfuFileName
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", dfu_file),
            device_index=ChannelUtils.get_device_index(test_case=self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())
        timeout = 60 if (dfu_file_parser.dfu_start_command.magic_str.ascii_converter() ==
                         self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesMagicString) else 30

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over wrong dfuCmdDatax in [dfuCmdData0, dfuCmdData2, dfuCmdData3]')
        # ---------------------------------------------------------------------------
        # dfuCmdData1 cannot be used for this test because it will be considered as a repetition of the command 1 packet
        for i in [0, 3]:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of dfu file')
            # ---------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(test_case=self,
                                                    report=dfu_file_parser.dfu_start_command,
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=0,
                                     timeout=timeout)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuCmdData1: next 16 bytes of dfu file is command 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(test_case=self,
                                                    report=dfu_file_parser.command_1[0][0],
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=1,
                                     timeout=timeout)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 3: Send dfuCmdData{i} instead of dfuCmdData2: next 16 bytes of '
                           'Regular_application.dfu file is program data packet 1')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_1[0][1][0].functionIndex = i
            dfu_status_response = ChannelUtils.send(test_case=self,
                                                    report=dfu_file_parser.command_1[0][1][0],
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Wait for dfuStatus with status = 0x17 (Bad sequence number)')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.BAD_SEQUENCE_NUMBER,
                                     timeout=timeout)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
    # end def _wrong_sequence_number

    @features('Feature00D0')
    @features('Feature00D0FlashWriteVerify')
    @level('ErrorHandling')
    @services('Debugger')
    def test_RepeatCommand1DataFlashWriteVerifyError(self):
        """
        @tc_synopsis    Sending a DFU duplicating the command 1 + the first 16 bytes data block request shall raise
                        the error 'Program/check data write failure'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is command 1'
                       'changing size to one packet (16 bytes)')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[0][0].size = 16
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send dfuCmdData2 : Send program data packet filled with 0x00')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[0][1][0].data = HexList([0]*16)
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][1][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = '
                       f'{sequence_number}')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Send dfuCmdData3 : Send again command 1 with same address and size as the first '
                       'one')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[0][0].functionIndex = 3
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Send dfuCmdData0 : Send program data packet filled with 0xFF')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[0][1][0].functionIndex = 0
        dfu_file_parser.command_1[0][1][0].data = HexList([0xFF]*16)
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][1][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 5: Wait for dfuStatus with status = 0x1F (Program/check data write failure)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PROGRAM_CHECK_DATA_WRITE_FAILURE)

        self.testCaseChecked("ROT_00D0_0001")
    # end def test_RepeatCommand1DataFlashWriteVerifyError

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuStartWrongFunctionId(self):
        """
        @tc_synopsis    Invalid Function index shall raise an error INVALID_FUNCTION_ID (7)

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        f = self.getFeatures()

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over functionIndex invalid range (typical wrong values)')
        # ---------------------------------------------------------------------------
        for invalid_function_index in compute_wrong_range([x for x in range(Dfu.MAX_FUNCTION_INDEX+1)], max_value=0xF):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuStart with fwEntity = 0xFF and functionIndex = ' +
                           str(invalid_function_index))
            # ---------------------------------------------------------------------------
            dfu_start = dfu_start_class(device_index=self.deviceIndex,
                                        feature_index=self.bootloader_dfu_feature_id,
                                        fw_entity=0xFF,
                                        encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                        magic_str=self.format_magic_string_hex_list(
                                            f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                                        flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                        secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
            dfu_start.functionIndex = invalid_function_index
            dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                                 response_queue=self.hidDispatcher.error_message_queue,
                                                                 response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidFunctionId (0x07) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=int(Numeral(dfu_status_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0003")
    # end def test_DfuStartWrongFunctionId

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuStartOnNotUpgradableError(self):
        """
        @tc_synopsis    Known DfuStart firmware Entity parameter (i.e. in range [0..n-1]) but not upgradable shall
                        raise an error 'Unsupported firmware entity'

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#4: Send Root.GetFeature(0x0003)')
        self.logTitle2('Test Step 1: Use feature 0x0003 to create a list valid fwEntity value but that are NOT '
                       'upgradable in the device')
        # ---------------------------------------------------------------------------
        upgradable_entities = DeviceInformationTestUtils.get_upgradable_entities(
            test_case=self, device_index=ChannelUtils.get_device_index(test_case=self))

        fw_entity_to_do = [not elt for elt in upgradable_entities]

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over list valid fwEntity value but that are NOT upgradable in the device')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        for entity_index in range(f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount):
            if not fw_entity_to_do[entity_index]:
                continue
            # end if

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuStart with fwEntity = {entity_index}')
            # ---------------------------------------------------------------------------
            dfu_start = dfu_start_class(device_index=self.deviceIndex,
                                        feature_index=self.bootloader_dfu_feature_id,
                                        fw_entity=entity_index,
                                        encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                        magic_str=self.format_magic_string_hex_list(
                                            f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                                        flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                        secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
            dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x12 (Unsupported firmware entity)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.UNSUPPORTED_FIRMWARE_ENTITY if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0010")
    # end def test_DfuStartOnNotUpgradableError

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuStartInvalidFwEntityError(self):
        """
        @tc_synopsis    Invalid DfuStart firmware Entity parameter shall raise an error 'Unsupported firmware entity'

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over fwEntity invalid value')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        for entity_index in compute_wrong_range(list(range(f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount)),
                                                max_value=0xFE):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send dfuStart with fwEntity = {entity_index}')
            # ---------------------------------------------------------------------------
            dfu_start = dfu_start_class(device_index=self.deviceIndex,
                                        feature_index=self.bootloader_dfu_feature_id,
                                        fw_entity=entity_index,
                                        encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                        magic_str=self.format_magic_string_hex_list(
                                            f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                                        flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                        secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
            dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x12 (Unsupported firmware entity)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.UNSUPPORTED_FIRMWARE_ENTITY if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0011")
    # end def test_DfuStartInvalidFwEntityError

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuStartEncrypt0Error(self):
        """
        @tc_synopsis    Invalid DfuStart encrypt parameter 0 shall raise an error 'Unsupported encryption mode'

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#4: Send Root.GetFeature(0x0003)')
        self.logTitle2('Test Step 1: Use feature 0x0003 to get first fwEntity upgradable')
        # ---------------------------------------------------------------------------
        upgradable_entities = DeviceInformationTestUtils.get_upgradable_entities(
            test_case=self, device_index=ChannelUtils.get_device_index(test_case=self))

        fw_entity_to_use = upgradable_entities.index(True)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Send dfuStart with fwEntity = {fw_entity_to_use} and encrypt = 0')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        dfu_start = dfu_start_class(
                               device_index=self.deviceIndex,
                               feature_index=self.bootloader_dfu_feature_id,
                               fw_entity=fw_entity_to_use,
                               encrypt=0,
                               magic_str=self.format_magic_string_hex_list(f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                               flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                               secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
        dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = Unsupported encryption mode)')
        # ---------------------------------------------------------------------------
        expected_status = DfuStatusResponse.StatusValue.UNSUPPORTED_ENCRYPTION_MODE if \
            self.f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else \
            DfuStatusResponse.StatusValue.GENERIC_ERROR
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)

        self.testCaseChecked("ROT_00D0_0012")
    # end def test_DfuStartEncrypt0Error

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuStartInvalidEncryptError(self):
        """
        @tc_synopsis    Reserved DfuStart encrypt parameter [2..0xFF] shall raise an error 'Unsupported encryption mode'

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#4: Send Root.GetFeature(0x0003)')
        self.logTitle2('Test Step 1: Use feature 0x0003 to get first fwEntity upgradable')
        # ---------------------------------------------------------------------------
        upgradable_entities = DeviceInformationTestUtils.get_upgradable_entities(
            test_case=self, device_index=ChannelUtils.get_device_index(test_case=self))

        fw_entity_to_use = upgradable_entities.index(True)

        assert fw_entity_to_use is not None, "No upgradable entity"

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over encrypt invalid value (0 excluded)')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        for encrypt in compute_wrong_range([0, 1], max_value=0xFF):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuStart with fwEntity = {fw_entity_to_use} and encrypt = {encrypt}')
            # ---------------------------------------------------------------------------
            dfu_start = dfu_start_class(device_index=self.deviceIndex,
                                        feature_index=self.bootloader_dfu_feature_id,
                                        fw_entity=fw_entity_to_use,
                                        encrypt=encrypt,
                                        magic_str=self.format_magic_string_hex_list(
                                            f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                                        flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                        secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
            dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x13 (Unsupported encryption mode)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.UNSUPPORTED_ENCRYPTION_MODE if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0013")
    # end def test_DfuStartInvalidEncryptError

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuStartInvalidMagicStrError(self):
        """
        @tc_synopsis    Invalid DfuStart magic String parameter shall raise an error 'Bad magic string'

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#4: Send Root.GetFeature(0x0003)')
        self.logTitle2('Test Step 1: Use feature 0x0003 to get first fwEntity upgradable')
        # ---------------------------------------------------------------------------
        upgradable_entities = DeviceInformationTestUtils.get_upgradable_entities(
            test_case=self, device_index=ChannelUtils.get_device_index(test_case=self))

        fw_entity_to_use = upgradable_entities.index(True)

        assert fw_entity_to_use is not None, "No upgradable entity"

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over magicString invalid value')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        for magic_str in compute_wrong_range(HexList([ord(i) for i in f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString])):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuStart with fwEntity = {fw_entity_to_use} and '
                           f'magicString = {magic_str}')
            # ---------------------------------------------------------------------------
            dfu_start = dfu_start_class(device_index=self.deviceIndex,
                                        feature_index=self.bootloader_dfu_feature_id,
                                        fw_entity=fw_entity_to_use,
                                        encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                        magic_str=self.format_magic_string_hex_list(magic_str),
                                        flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                        secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
            dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x14 (Bad magic string)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.BAD_MAGIC_STRING if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0014")
    # end def test_DfuStartInvalidMagicStrError

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuStartInvalidMagicStrLastByteNullError(self):
        """
        @tc_synopsis    Changing the last byte of the magic String parameter by a null terminated string shall also
                        raise an error 'Bad magic string'

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#4: Send Root.GetFeature(0x0003)')
        self.logTitle2('Test Step 1: Use feature 0x0003 to get first fwEntity upgradable')
        # ---------------------------------------------------------------------------
        upgradable_entities = DeviceInformationTestUtils.get_upgradable_entities(
            test_case=self, device_index=ChannelUtils.get_device_index(test_case=self))

        fw_entity_to_use = upgradable_entities.index(True)

        assert fw_entity_to_use is not None, "No upgradable entity"

        f = self.getFeatures()
        magic_str = self.format_magic_string_hex_list(f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString)
        magic_str[len(f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString) - 1] = 0

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Send dfuStart with fwEntity = {fw_entity_to_use} and '
                       f'magicString = {magic_str}')
        # ---------------------------------------------------------------------------
        dfu_start = dfu_start_class(device_index=self.deviceIndex,
                                    feature_index=self.bootloader_dfu_feature_id,
                                    fw_entity=fw_entity_to_use,
                                    encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                    magic_str=magic_str,
                                    flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                    secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
        dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x14 (Bad magic string)')
        # ---------------------------------------------------------------------------
        expected_status = DfuStatusResponse.StatusValue.BAD_MAGIC_STRING if \
            f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)

        self.testCaseChecked("ROT_00D0_0015")
    # end def test_DfuStartInvalidMagicStrLastByteNullError

    @features('Feature00D0')
    @features('Feature00D0MagicStrMaxSize', 9)
    @level('ErrorHandling')
    def test_DfuStartInvalidMagicStrFirstNullToRandomError(self):
        """
        @tc_synopsis    Changing the first null terminated byte padding the magic String parameter by a random byte
                        shall also raise an error 'Bad magic string'


        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#4: Send Root.GetFeature(0x0003)')
        self.logTitle2('Test Step 1: Use feature 0x0003 to get first fwEntity upgradable')
        # ---------------------------------------------------------------------------
        upgradable_entities = DeviceInformationTestUtils.get_upgradable_entities(
            test_case=self, device_index=ChannelUtils.get_device_index(test_case=self))

        fw_entity_to_use = upgradable_entities.index(True)

        assert fw_entity_to_use is not None, "No upgradable entity"

        f = self.getFeatures()
        magic_str = self.format_magic_string_hex_list(f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString)
        magic_str[len(f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString)] = randint(1, 255)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Send dfuStart with fwEntity = {fw_entity_to_use} and '
                       f'magicString = {magic_str}')
        # ---------------------------------------------------------------------------
        dfu_start = dfu_start_class(device_index=self.deviceIndex,
                                    feature_index=self.bootloader_dfu_feature_id,
                                    fw_entity=fw_entity_to_use,
                                    encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                    magic_str=magic_str,
                                    flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                    secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
        dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x14 (Bad magic string)')
        # ---------------------------------------------------------------------------
        expected_status = DfuStatusResponse.StatusValue.BAD_MAGIC_STRING if \
            f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)

        self.testCaseChecked("ROT_00D0_0016")
    # end def test_DfuStartInvalidMagicStrFirstNullToRandomError

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_WrongCheckDataError(self):
        """
        @tc_synopsis    Changing any bit of the check data (i.e. signature) shall trigger an error
                        'Firmware check failure' during command 3 processing (last 16 bytes block of the dfu).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change check data in Regular_application.dfu file to make '
                       'Wrong_check_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        bit_to_change = randint(0, 15 * 8 if int(Numeral(dfu_file_parser.command_2[0][0].size)) % 16 == 0 else ((int(
            Numeral(dfu_file_parser.command_2[0][0].size)) % 16) - 1) * 8)
        packet_to_change = HexList(dfu_file_parser.command_2[0][1][-1])
        packet_to_change[4 + bit_to_change // 8] ^= 1 << (bit_to_change % 8)
        dfu_file_parser.command_2[0][1][-1] = DfuCmdDataXData.fromHexList(packet_to_change)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Wrong_check_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is '
                           'command 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list)}, packet number should start at 1')
            # ---------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'program data packet {i+1}')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ---------------------------------------------------------------------------
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                           'command 2')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of check data packets to be sent = '
                           f'{len(check_data_list)}, packet number should start at 1')
            # ---------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'check data packet {i+1}')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 5: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ---------------------------------------------------------------------------
        # end for

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of Wrong_check_application.dfu file is command 3')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x22 (Firmware check failure)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE)

        self.testCaseChecked("ROT_00D0_0017")
        self.testCaseChecked("ROT_00D0_0041")
    # end def test_WrongCheckDataError

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command1AddressTooLowError(self):
        """
        @tc_synopsis    Sending a DFU targeting an address lower than the lowest authorized address shall raise the
                        error 'Address/size combination out of range'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuCmdData1 with command 1.address < lowest authorized address')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[0][0].address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1A (Address/size combination out of range)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ADDRESS_SIZE_COMBINATION_OUT_OF_RANGE)

        self.testCaseChecked("ROT_00D0_0018")
    # end def test_Command1AddressTooLowError

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command1AddressTooHighError(self):
        """
        @tc_synopsis    Sending a DFU targeting an address higher than the highest authorized address shall raise the
                        error 'Address/size combination out of range'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuCmdData1 with command 1.address > highest authorized address')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[0][0].address = f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress + \
            f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram - int(Numeral(dfu_file_parser.command_1[0][0].size)) - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationValidityFlagSize
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1A (Address/size combination out of range)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ADDRESS_SIZE_COMBINATION_OUT_OF_RANGE)

        self.testCaseChecked("ROT_00D0_0019")
    # end def test_Command1AddressTooHighError

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_RestartOnNotUpgradableError(self):
        """
        @tc_synopsis    Calling the Restart function with a known fwEntity parameter (i.e. in range [0..n-1]
                        but not upgradable) shall return a INVALID_ARGUMENT (2) error code

        [5] restart(fwEntity) -> pktNb, status, param
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#4: Send Root.GetFeature(0x0003)')
        self.logTitle2('Test Step 1: Use feature 0x0003 to create a list valid fwEntity value but '
                       'that are NOT upgradable in the device')
        # ---------------------------------------------------------------------------
        upgradable_entities = DeviceInformationTestUtils.get_upgradable_entities(
            test_case=self, device_index=ChannelUtils.get_device_index(test_case=self))

        fw_entity_to_do = [not elt for elt in upgradable_entities]

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over list valid fwEntity value but that are NOT upgradable in the device')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        for entity_index in range(f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount):
            if not fw_entity_to_do[entity_index]:
                continue
            # end if

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuStart with fwEntity = {entity_index}')
            # ---------------------------------------------------------------------------
            restart = Restart(device_index=self.deviceIndex,
                              feature_index=self.bootloader_dfu_feature_id,
                              fw_entity=entity_index)
            restart_response = self.send_report_wait_response(report=restart,
                                                              response_queue=self.hidDispatcher.error_message_queue,
                                                              response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidArgument (0x02) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=int(Numeral(restart_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0020")
    # end def test_RestartOnNotUpgradableError

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_RestartInvalidFwEntityError(self):
        """
        @tc_synopsis    Invalid Restart firmware Entity parameter shall return a INVALID_ARGUMENT (2) error code

        [5] restart(fwEntity) -> pktNb, status, param
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over list valid fwEntity value but that are NOT upgradable in the device')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        for entity_index in compute_wrong_range(list(range(f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount)),
                                                max_value=0xFE):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send dfuStart with fwEntity = {entity_index}')
            # ---------------------------------------------------------------------------
            restart = Restart(device_index=self.deviceIndex,
                              feature_index=self.bootloader_dfu_feature_id,
                              fw_entity=entity_index)
            restart_response = self.send_report_wait_response(report=restart,
                                                              response_queue=self.hidDispatcher.error_message_queue,
                                                              response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidArgument (0x02) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=int(Numeral(restart_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0021")
    # end def test_RestartInvalidFwEntityError

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_RestartWhenDfuNotFinishedError(self):
        """
        @tc_synopsis    Calling the Restart function while a DFU is in progress before command 1, 2 and 3 shall
                        return a BUSY (8) error code.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Send restart with fwEntity = '
                       f'{int(Numeral(dfu_file_parser.dfu_start_command.fw_entity))}')
        # ---------------------------------------------------------------------------
        restart = Restart(device_index=self.deviceIndex,
                          feature_index=self.bootloader_dfu_feature_id,
                          fw_entity=dfu_file_parser.dfu_start_command.fw_entity)
        restart_response = self.send_report_wait_response(report=restart,
                                                          response_queue=self.hidDispatcher.error_message_queue,
                                                          response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Received ErrorCode BUSY (0x08) error code')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.BUSY,
                         obtained=int(Numeral(restart_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is '
                           'command 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list)}, packet number should start at 1')
            # ---------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'program data packet {i+1}')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ---------------------------------------------------------------------------
        # end for

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 5: Send restart with fwEntity = '
                       f'{int(Numeral(dfu_file_parser.dfu_start_command.fw_entity))}')
        # ---------------------------------------------------------------------------
        restart = Restart(device_index=self.deviceIndex,
                          feature_index=self.bootloader_dfu_feature_id,
                          fw_entity=dfu_file_parser.dfu_start_command.fw_entity)
        restart_response = self.send_report_wait_response(report=restart,
                                                          response_queue=self.hidDispatcher.error_message_queue,
                                                          response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 5: Received ErrorCode BUSY (0x08) error code')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.BUSY,
                         obtained=int(Numeral(restart_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 6: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                           'command 2')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 6: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of check data packets to be sent = '
                           f'{len(check_data_list)}, packet number should start at 1')
            # ---------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 7: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'check data packet {i+1}')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 7: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ---------------------------------------------------------------------------
        # end for

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 8: Send restart with fwEntity = '
                       f'{int(Numeral(dfu_file_parser.dfu_start_command.fw_entity))}')
        # ---------------------------------------------------------------------------
        restart = Restart(device_index=self.deviceIndex,
                          feature_index=self.bootloader_dfu_feature_id,
                          fw_entity=dfu_file_parser.dfu_start_command.fw_entity)
        restart_response = self.send_report_wait_response(report=restart,
                                                          response_queue=self.hidDispatcher.error_message_queue,
                                                          response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 8: Received ErrorCode BUSY (0x08) error code')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.BUSY,
                         obtained=int(Numeral(restart_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 9: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is command 3')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 9: Wait for dfuStatus with status = 0x02 (DFU success)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_check=10)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=11, log_check=11)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("ROT_00D0_0022")
        self.testCaseChecked("ROT_00D0_0023")
        self.testCaseChecked("ROT_00D0_0024")
    # end def test_RestartWhenDfuNotFinishedError

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuCmdDataXCommand1BeforeDfuStart(self):
        """
        @tc_synopsis    Calling dfuCmdDataX command 1 before 'DfuStart' shall raise the error 'DFU not started'

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over dfuCmdDataX classes')
        # ---------------------------------------------------------------------------
        for i in range(4):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuCmdDataX with command 1 parameters from Regular_application.dfu file')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_1[0][0].functionIndex = i
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x16 (DFU not started)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.DFU_NOT_STARTED if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0025")
    # end def test_DfuCmdDataXCommand1BeforeDfuStart

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuCmdDataXCommand2BeforeDfuStart(self):
        """
        @tc_synopsis    Calling dfuCmdDataX command 2 before 'DfuStart' shall raise the error 'DFU not started'

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over dfuCmdDataX classes')
        # ---------------------------------------------------------------------------
        for i in range(4):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuCmdDataX with command 2 parameters from Regular_application.dfu file')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_2[0][0].functionIndex = i
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_2[0][0],
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x16 (DFU not started)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.DFU_NOT_STARTED if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0026")
    # end def test_DfuCmdDataXCommand2BeforeDfuStart

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuCmdDataXCommand3BeforeDfuStart(self):
        """
        @tc_synopsis    Calling dfuCmdDataX command 3 before 'DfuStart' shall raise the error 'DFU not started'

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over dfuCmdDataX classes')
        # ---------------------------------------------------------------------------
        for i in range(4):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuCmdDataX with command 3 parameters from Regular_application.dfu file')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_3.functionIndex = i
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x16 (DFU not started)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.DFU_NOT_STARTED if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0027")
    # end def test_DfuCmdDataXCommand3BeforeDfuStart

    @features('Feature00D0')
    @level('ErrorHandling')
    def test_DfuCmdDataXDataBeforeDfuStart(self):
        """
        @tc_synopsis    Calling dfuCmdDataX data before 'DfuStart' shall raise the error 'DFU not started'

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over dfuCmdDataX classes')
        # ---------------------------------------------------------------------------
        for i in range(4):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuCmdDataX with the first program data packet from '
                           'Regular_application.dfu file')
            # ---------------------------------------------------------------------------
            first_program_data_packet = dfu_file_parser.command_1[0][1][0]
            first_program_data_packet.functionIndex = i
            dfu_status_response = self.send_report_wait_response(report=first_program_data_packet,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x16 (DFU not started)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.DFU_NOT_STARTED if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0028")
    # end def test_DfuCmdDataXDataBeforeDfuStart

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command1WrongSequenceNumberError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with a wrong (greater or lower) sequence number (i.e. function index)
                        for command 1 shall raise the error 'Bad sequence number'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over wrong dfuCmdDatax in [dfuCmdData0, dfuCmdData2, dfuCmdData3]')
        # ---------------------------------------------------------------------------
        for i in [0, 2, 3]:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=0)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuCmdData{i} instead of dfuCmdData1: next 16 bytes of '
                           'Regular_application.dfu file is command 1')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_1[0][0].functionIndex = i
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x17 (Bad sequence number)')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.BAD_SEQUENCE_NUMBER)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0029")
    # end def test_Command1WrongSequenceNumberError

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command2WrongSequenceNumberError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with a wrong (greater or lower) sequence number (i.e. function index)
                        for command 2 shall raise the error 'Bad sequence number'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over wrong dfuCmdDatax in [dfuCmdData0, dfuCmdData2, dfuCmdData3]')
        # ---------------------------------------------------------------------------
        for i in [0, 2, 3]:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=0)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuCmdData{i} instead of dfuCmdData1: next 16 bytes of '
                           'Regular_application.dfu file is command 2')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_2[0][0].functionIndex = i
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_2[0][0],
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x17 (Bad sequence number)')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.BAD_SEQUENCE_NUMBER)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0030")
    # end def test_Command2WrongSequenceNumberError

    @features('Feature00D0')
    @features('Feature00D0VerifyCmd3DoneAfterCmd1And2')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command3WrongSequenceNumberError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with a wrong (greater or lower) sequence number (i.e. function index)
                        for command 3 shall raise the error 'Bad sequence number'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over wrong dfuCmdDatax in the list of non expected command 3 sequence number')
        # ---------------------------------------------------------------------------
        # We cannot test the third because it would be as a repetition of the previous packet
        for _ in range(2):
            sequence_number = 0
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            for (cmd_1, program_data_list) in dfu_file_parser.command_1:
                # ---------------------------------------------------------------------------
                self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is '
                               'command 1')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=cmd_1,
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1

                # ---------------------------------------------------------------------------
                self.logTitle2('Test Loop over the number of program data packets to be sent = '
                               f'{len(program_data_list)}, packet number should start at 1')
                # ---------------------------------------------------------------------------
                for i in range(len(program_data_list)):
                    # ---------------------------------------------------------------------------
                    self.logTitle2(f'Test Step 3: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                                   f'program data packet {i+1}')
                    # ---------------------------------------------------------------------------
                    dfu_status_response = self.send_report_wait_response(
                        report=program_data_list[i],
                        response_queue=self.hidDispatcher.common_message_queue,
                        response_class_type=DfuStatusResponse)

                    # ---------------------------------------------------------------------------
                    self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and '
                                   f'pktNb = {sequence_number}')
                    # ---------------------------------------------------------------------------
                    self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                             status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                             packet_number=sequence_number)

                    sequence_number += 1
                # end for
                # ---------------------------------------------------------------------------
                self.logTitle2('End Test Loop')
                # ---------------------------------------------------------------------------
            # end for

            for (cmd_2, check_data_list) in dfu_file_parser.command_2:
                # ---------------------------------------------------------------------------
                self.logTitle2('Test Step 4: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               'command 2')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=cmd_2,
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1

                # ---------------------------------------------------------------------------
                self.logTitle2('Test Loop over the number of check data packets to be sent = '
                               f'{len(check_data_list)}, packet number should start at 1')
                # ---------------------------------------------------------------------------
                for i in range(len(check_data_list)):
                    # ---------------------------------------------------------------------------
                    self.logTitle2(f'Test Step 5: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                                   f'check data packet {i+1}')
                    # ---------------------------------------------------------------------------
                    dfu_status_response = self.send_report_wait_response(
                        report=check_data_list[i],
                        response_queue=self.hidDispatcher.common_message_queue,
                        response_class_type=DfuStatusResponse)

                    # ---------------------------------------------------------------------------
                    self.logTitle2(f'Test Check 5: Wait for dfuStatus with status = 0x01 (Packet success) and '
                                   f'pktNb = {sequence_number}')
                    # ---------------------------------------------------------------------------
                    self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                             status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                             packet_number=sequence_number)

                    sequence_number += 1
                # end for
                # ---------------------------------------------------------------------------
                self.logTitle2('End Test Loop')
                # ---------------------------------------------------------------------------
            # end for

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 6: Send '
                           f'dfuCmdData{(dfu_file_parser.command_3.functionIndex + 1) % 4} instead of '
                           f'dfuCmdData{dfu_file_parser.command_3.functionIndex} : next 16 bytes of '
                           'Regular_application.dfu file is command 3')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_3.functionIndex = (dfu_file_parser.command_3.functionIndex + 1) % 4
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x17 (Bad sequence number)')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.BAD_SEQUENCE_NUMBER)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0031")
    # end def test_Command3WrongSequenceNumberError

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_DataWrongSequenceNumberError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with a wrong (greater or lower) sequence number (i.e. function index)
                        for data  shall raise the error 'Bad sequence number'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [2] dfuCmdData1(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        self._wrong_sequence_number()

        self.testCaseChecked("ROT_00D0_0032#1")
    # end def test_DataWrongSequenceNumberError

    @features('Feature00D0')
    @features('ImageDFU')
    @level('ErrorHandling')
    @services('Debugger')
    def test_DataWrongSequenceNumberError_images(self):
        """
        see ``test_DataWrongSequenceNumberError`` but with an image DFU file
        """
        self._wrong_sequence_number(dfu=self.DFU_IMAGE)

        self.testCaseChecked("ROT_00D0_0032#2")
    # end def test_DataWrongSequenceNumberError

    @features('Feature00D0')
    @features('Feature00D0MinProgramQuantum', 2)
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command1UnalignedAddressError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with an address in command 1 not multiple of the program quantum shall
                        raise the error 'Unaligned address'.

        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change program data address in command 1 in Regular_application.dfu file to make '
                       'Wrong_program_address_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # Since the program quantum is minimum 2, adding 1 will always be unaligned
        dfu_file_parser.command_1[0][0].address = int(Numeral(dfu_file_parser.command_1[0][0].address)) + 1
        # To avoid error of address to high, the size is reduced
        dfu_file_parser.command_1[0][0].size = int(Numeral(dfu_file_parser.command_1[0][0].size)) - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Wrong_program_address_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send dfuCmdData1: next 16 bytes of Wrong_program_address_application.dfu file '
                       'is command 1')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1B (Unaligned address)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.UNALIGNED_ADDRESS)

        self.testCaseChecked("ROT_00D0_0033")
    # end def test_Command1UnalignedAddressError

    @features('Feature00D0')
    @features('Feature00D0MinCheckQuantum', 2)
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command2UnalignedAddressError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with an address in command 2 not multiple of the check quantum shall
                        raise the error 'Unaligned address'.

        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change check data address in command 2 in Regular_application.dfu file to make '
                       'Wrong_check_address_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # Since the program quantum is minimum 2, adding 1 will always be unaligned
        dfu_file_parser.command_2[0][0].address = int(Numeral(dfu_file_parser.command_2[0][0].address)) + 1
        # To avoid error of address/size to high, the size is reduced
        dfu_file_parser.command_2[0][0].size = int(Numeral(dfu_file_parser.command_2[0][0].size)) - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Wrong_check_address_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send dfuCmdData1: get16 bytes of Wrong_check_address_application.dfu file that '
                       'are command 2')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_2[0][0].functionIndex = 1
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_2[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1B (Unaligned address)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.UNALIGNED_ADDRESS)

        self.testCaseChecked("ROT_00D0_0034")
    # end def test_Command2UnalignedAddressError

    @features('Feature00D0')
    @features('Feature00D0MinProgramQuantum', 2)
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command1UnalignedSizeError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with a size in command 1 not multiple of the program quantum shall
                        raise the error 'Bad size'.

        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change program data size in command 1 in Regular_application.dfu file to make '
                       'Wrong_program_size_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # Since the program quantum is minimum 2, reducing by 1 will always be unaligned
        dfu_file_parser.command_1[0][0].size = int(Numeral(dfu_file_parser.command_1[0][0].size)) - 1

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Wrong_program_size_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send dfuCmdData1: next 16 bytes of Wrong_program_size_application.dfu file '
                       'is command 1')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1C (Bad size)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.BAD_SIZE)

        self.testCaseChecked("ROT_00D0_0035")
    # end def test_Command1UnalignedSizeError

    @features('Feature00D0')
    @features('Feature00D0MinCheckQuantum', 2)
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command2UnalignedSizeError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with a size in command 2 not multiple of the check quantum shall
                        raise the error 'Bad size'.

        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change check data size in command 2 in Regular_application.dfu file to make '
                       'Wrong_check_size_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # Since the check quantum is minimum 2, reducing by 1 will always be unaligned
        dfu_file_parser.command_2[0][0].size = int(Numeral(dfu_file_parser.command_2[0][0].size)) - 1

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Wrong_check_size_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send dfuCmdData1: get16 bytes of Wrong_check_size_application.dfu file that '
                       'are command 2')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_2[0][0].functionIndex = 1
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_2[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1B (Unaligned address)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.BAD_SIZE)

        self.testCaseChecked("ROT_00D0_0036")
    # end def test_Command1UnalignedSizeError

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command1ZeroSizeError(self):
        """
        @tc_synopsis    When an empty command 1 is received, the boot-loader may either accept it (and do nothing) or
                        return a bad size error (implementation-specific).

        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change program data size = 0 in command 1 in Regular_application.dfu file to make '
                       'Wrong_program_size_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.command_1[0][0].size = 0

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Wrong_program_size_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send dfuCmdData1: next 16 bytes of Wrong_program_size_application.dfu file '
                       'is command 1')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) or 0x1D '
                       '(Missing program data)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS +
                                 DfuStatusResponse.StatusValue.MISSING_PROGRAM_DATA)

        self.testCaseChecked("ROT_00D0_0037")
    # end def test_Command1ZeroSizeError

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command2ZeroSizeError(self):
        """
        @tc_synopsis    When an empty command 2 is received, the boot-loader may either accept it (and do nothing) or
                        return a bad size error (implementation-specific).

        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change check data size = 0 in command 2 in Regular_application.dfu file to make '
                       'Wrong_check_size_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.command_2[0][0].size = 0

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Wrong_check_size_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send dfuCmdData1: get 16 bytes of Wrong_check_size_application.dfu file that are '
                       'command 2')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_2[0][0].functionIndex = 1
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_2[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) or 0x1D '
                       '(Missing program data)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS +
                                 DfuStatusResponse.StatusValue.MISSING_PROGRAM_DATA)

        self.testCaseChecked("ROT_00D0_0038")
    # end def test_Command2ZeroSizeError

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command3BeforeCommand1Error(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' command 3 while the data to program haven't been send thru command 1 may
                        raise the error 'Missing program data' or 'Firmware check failure' if directly proceeding to
                        the verification (implementation-specific).

        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Put command 3 before command 1 in Regular_application.dfu file to make '
                       'Cmd3_first_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.command_3.functionIndex = 1

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Cmd3_first_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send dfuCmdData1: next 16 bytes of Cmd3_first_application.dfu file is command 3')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1D (Missing program data) or 0x22 '
                       '(Firmware check failure)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE +
                                 DfuStatusResponse.StatusValue.MISSING_PROGRAM_DATA)

        self.testCaseChecked("ROT_00D0_0039")
    # end def test_Command3BeforeCommand1Error

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_Command3BeforeCommand2Error(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' command 3 while we don't provide the mandatory check data thru command 2
                        may raise the error 'Missing check data' or 'Firmware check failure' if directly proceeding to
                        the verification (implementation-specific).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Put command 3 before command 2 in Regular_application.dfu file to make '
                       'Cmd3_second_application.dfu')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of Cmd3_second_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is '
                           'command 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list)}, packet number should start at 1')
            # ---------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 3: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'program data packet {i+1}')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ---------------------------------------------------------------------------
        # end for

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Send dfuCmdData1: next 16 bytes of Cmd3_second_application.dfu file is command 3')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1D (Missing program data) or 0x22 '
                       '(Firmware check failure)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE +
                                 DfuStatusResponse.StatusValue.MISSING_PROGRAM_DATA)

        self.testCaseChecked("ROT_00D0_0040")
    # end def test_Command3BeforeCommand1Error

    @features('Feature00D0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_WrongCommandError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with cmd parameter greater than 3 shall raise the error
                        'Unsupported command'.

        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over invalid cmd parameter')
        # ---------------------------------------------------------------------------
        for invalid_cmd in compute_wrong_range(value=[1, 2, 3], max_value=0xFF):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Wrong_program_size_application.dfu file')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=0)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuCmdData1 with cmd = {invalid_cmd}')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_1[0][0].cmd = invalid_cmd
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x18 (Unsupported command)')
            # ---------------------------------------------------------------------------
            expected_status = DfuStatusResponse.StatusValue.UNSUPPORTED_COMMAND if \
                f.PRODUCT.FEATURES.COMMON.DFU.F_ErrorLevel > 1 else DfuStatusResponse.StatusValue.GENERIC_ERROR
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response, status=expected_status)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0042")
    # end def test_WrongCommandError

    @features('Feature00D0')
    @features('NoFeature00D0FlashWriteVerify')
    @level('Time-consuming')
    @services('Debugger')
    def test_RepeatCommand1DataNoFlashWriteVerifyError(self):
        """
        @tc_synopsis    Sending a DFU duplicating the first command 1 and first data packet, then doing the full DFU
                        will generate an error 0xA2 (Firmware check failure) for command 3.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData2(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        repeated_command_1 = DfuCmdDataXCmd1or2.fromHexList(HexList(dfu_file_parser.command_1[0][0]))
        repeated_command_1.size = 16
        repeated_program_data = DfuCmdDataXData.fromHexList(HexList(dfu_file_parser.command_1[0][1][0]))
        byte_changed = False
        for j in range(16):
            if dfu_file_parser.command_1[0][1][0].data[j] != 0:
                dfu_file_parser.command_1[0][1][0].data[j] = 0
                byte_changed = True

        self.assertTrue(expr=byte_changed,
                        msg="Could not change a byte that would create a problem")

        dfu_file_parser.command_1.insert(0, (repeated_command_1, [repeated_program_data]))

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is command 1 '
                       'changing the size to 1 packet (16 bytes)')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = '
                       f'{sequence_number}')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for program_data in dfu_file_parser.command_1[0][1]:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is program '
                           f'data packet 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=program_data,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = '
                           f'{sequence_number}')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1
        # end for

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Send dfuCmdData1 : Send again command 1 with the regular size')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[1][0].functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[1][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = '
                       f'{sequence_number}')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Send again program data packet 1 one byte to 0x00')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[1][1][0].functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[1][1][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 5: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = '
                       f'{sequence_number}')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        # It start at -1 to remove the first packet already sent
        number_program_data_packets_to_send = -1
        for(_, program_data_list) in dfu_file_parser.command_1[1:]:
            number_program_data_packets_to_send += len(program_data_list)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over the number of program data packets to be sent = '
                       f'{number_program_data_packets_to_send}, packet number should start at 2')
        # ---------------------------------------------------------------------------
        for i in range(1, len(dfu_file_parser.command_1)):
            if i > 1:
                self.logTrace(msg="New command 1, packet number will restart at 1")
                dfu_file_parser.command_1[i][0].functionIndex = sequence_number % 4
                dfu_status_response = self.send_report_wait_response(
                    report=dfu_file_parser.command_1[i][0],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end if

            for j in range(len(dfu_file_parser.command_1[i][1])):
                if i == 1 and j == 0:
                    continue
                # end if

                # ---------------------------------------------------------------------------
                self.logTitle2('Test Step 6: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'program data packet {j+1}')
                # ---------------------------------------------------------------------------
                dfu_file_parser.command_1[i][1][j].functionIndex = sequence_number % 4
                dfu_status_response = self.send_report_wait_response(
                    report=dfu_file_parser.command_1[i][1][j],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = '
                               f'{sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                           'command 2')
            # ---------------------------------------------------------------------------
            cmd_2.functionIndex = sequence_number % 4
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 7: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of check data packets to be sent = '
                           f'{len(check_data_list)}, packet number should start at 1')
            # ---------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 8: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'check data packet {i+1}')
                # ---------------------------------------------------------------------------
                check_data_list[i].functionIndex = sequence_number % 4
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 8: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ---------------------------------------------------------------------------
        # end for

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 9: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is command 3')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 9: Wait for dfuStatus with status = 0xA2 (Firmware check failure)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE)

        self.testCaseChecked("ROT_00D0_0043")
    # end def test_RepeatCommand1DataNoFlashWriteVerifyError

    @features('Feature00D0')
    @features('NoFeature00D0VerifyCmd3DoneAfterCmd1And2')
    @level('ErrorHandling')
    @services('Debugger')
    def test_Command3NoVerifyWrongSequenceNumberError(self):
        """
        @tc_synopsis    Calling 'dfuCmdDatax' with a wrong (greater or lower) sequence number (i.e. function index)
                        for command 3 shall raise the error 'Bad sequence number'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over wrong dfuCmdDatax in [dfuCmdData0, dfuCmdData2, dfuCmdData3]')
        # ---------------------------------------------------------------------------
        for i in [0, 2, 3]:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=0)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuCmdData{i} instead of dfuCmdData1: next 16 bytes of '
                           'Regular_application.dfu file is command 3')
            # ---------------------------------------------------------------------------
            dfu_file_parser.command_3.functionIndex = i
            dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x17 (Bad sequence number)')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.BAD_SEQUENCE_NUMBER)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0044")
    # end def test_Command3NoVerifyWrongSequenceNumberError

    @features('Feature00D0SoftDevice')
    @level('ErrorHandling')
    @services('Debugger')
    def test_SoftDeviceAddressTooLowError(self):
        """
        @tc_synopsis    Sending a SoftDEvice DFU targeting an address lower than the lowest authorized address shall
                        raise the error 'Address/size combination out of range'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuCmdData1 with command 1.address < lowest authorized address')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[0][0].address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestSoftDeviceAddress - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1A (Address/size combination out of range)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ADDRESS_SIZE_COMBINATION_OUT_OF_RANGE)

        self.testCaseChecked("ROT_00D0_0049")
    # end def test_SoftDeviceAddressTooLowError

    @features('Feature00D0SoftDevice')
    @level('ErrorHandling')
    @services('Debugger')
    def test_SoftDeviceAddressTooHighError(self):
        """
        @tc_synopsis    Sending a SoftDevice DFU targeting an address higher than the highest authorized address shall
                        raise the error 'Address/size combination out of range'.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuCmdData1 with command 1.address > highest authorized address')
        # ---------------------------------------------------------------------------
        dfu_file_parser.command_1[0][0].address = (f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress + \
            f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram - int(Numeral(dfu_file_parser.command_1[0][0].size)))
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_1[0][0],
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for dfuStatus with status = 0x1A (Address/size combination out of range)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ADDRESS_SIZE_COMBINATION_OUT_OF_RANGE)

        self.testCaseChecked("ROT_00D0_0050")
    # end def test_SoftDeviceAddressTooHighError

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('ErrorHandling')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_mcu_address_too_low(self):
        """
        Sending a SoftDEvice DFU targeting an address lower than the lowest authorized address shall raise the error
        'Address/size combination out of range'.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Parse DFU file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(ChannelUtils.get_device_index(self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of DFU file")
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(self,
                                                dfu_file_parser.dfu_start_command,
                                                HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0")
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuCmdData1 with command 1.address < lowest authorized address")
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_1[0][0].address = (
            self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress -
            self.f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
        )

        dfu_status_response = ChannelUtils.send(self,
                                                dfu_file_parser.command_1[0][0],
                                                HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DFU Status is Address/Size combination out of range")
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ADDRESS_SIZE_COMBINATION_OUT_OF_RANGE)

        self.testCaseChecked("ERR_00D0_0066")
    # end def test_companion_mcu_address_too_low

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('ErrorHandling')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_mcu_address_too_high(self):
        """
        Sending a SoftDEvice DFU targeting an address higher than the highest authorized address shall raise the error
        'Address/size combination out of range'.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Parse DFU file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(ChannelUtils.get_device_index(self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of DFU file")
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(self,
                                                dfu_file_parser.dfu_start_command,
                                                HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0")
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuCmdData1 with command 1.address < lowest authorized address")
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_1[0][0].address = (
                self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress +
                self.f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram -
                int(Numeral(dfu_file_parser.command_1[0][0].size))
        )

        dfu_status_response = ChannelUtils.send(self,
                                                dfu_file_parser.command_1[0][0],
                                                HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DFU Status is Address/Size combination out of range")
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ADDRESS_SIZE_COMBINATION_OUT_OF_RANGE)

        self.testCaseChecked("ERR_00D0_0067")
    # end def test_companion_mcu_address_too_high
# end class SharedDfuTestCaseErrorHandling

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
