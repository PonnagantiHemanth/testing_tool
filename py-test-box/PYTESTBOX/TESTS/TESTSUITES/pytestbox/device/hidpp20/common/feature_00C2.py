#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.hid.common.feature_00C2
    :brief: Validates HID common feature 0x00C2
    :author: Stanislas Cottard
    :date: 2019/06/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import unittest

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.core import TYPE_SUCCESS
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.dfucontrol import DfuControl
from pyhid.hidpp.features.common.dfucontrol import GetDfuStatus
from pyhid.hidpp.features.common.dfucontrol import GetDfuStatusResponse
from pyhid.hidpp.features.common.dfucontrol import StartDfu
from pyhid.hidpp.features.common.dfucontrol import StartDfuResponse
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import choices
from pylibrary.tools.util import compute_inverted_bit_range
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.transportcontext import TransportContextException


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ApplicationDfuControlTestCase(BaseTestCase):
    """
    Validates DFU Control TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(ApplicationDfuControlTestCase, self).setUp()

        if self.current_channel.protocol in LogitechProtocol.gaming_protocols() and \
                self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
            # Switch to USB channel if the DUT is a gaming device, otherwise do nothing
            ProtocolManagerUtils.switch_to_usb_channel(self)
        # end if
        
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x00C2)')
        # ---------------------------------------------------------------------------
        self.featureId = self.updateFeatureMapping(feature_id=DfuControl.FEATURE_ID)
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.status != TYPE_SUCCESS:
                # ---------------------------------------------------------------------------
                self.logTitle2('Post-requisite#1: In case of test failure, the Device shall be forced in Main '
                               'Application mode')
                # ---------------------------------------------------------------------------
                DfuTestUtils.force_target_on_application(test_case=self)
            # end if

            if self.backup_dut_channel.protocol in LogitechProtocol.gaming_protocols() and \
                    self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
                # Leave from USB channel if the DUT is a gaming device, otherwise do nothing
                ProtocolManagerUtils.exit_usb_channel(self)
            # end if
        except AttributeError:
            # AttributeError: 'ApplicationDfuControlTestCase' object has no attribute 'deviceIndex'
            pass
        except:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super(ApplicationDfuControlTestCase, self).tearDown()
    # end def tearDown
    
    @features('DfuControl')
    @level('Interface')
    def test_GetDfuStatusAPI(self):
        """
        @tc_synopsis    Validates DFU Control.getDfuStatus API (Feature 0x00C2)

        [0] getDfuStatus() -> 0, 0, notAvail
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check reserved_enterDfu = 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.reserved_enter_dfu,
                         msg='The reserved_enter_dfu parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check enterDfu = 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.enter_dfu,
                         msg='The reserved_enter_dfu parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Check dfuControlParam= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList(0),
                         obtained=get_dfu_status_response.dfu_control_param,
                         msg='The dfu_control_param parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Check reserved_notAvail= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.reserved_not_avail,
                         msg='The reserved_not_avail parameter differs from the one expected')
        
        self.testCaseChecked("FNT_00C2_0001")
    # end def test_GetDfuStatusAPI

    @features('DfuControl')
    @features('Feature00D0')
    @level('Interface')
    @unittest.skip("Needs more information on the relevance of this test")
    def test_StartDfuAPI(self):
        """
        @tc_synopsis    Validates DFU Control.startDfu API (Feature 0x00C2)

        [1] startDfu(enterDfu, dfuControlParam, dfuMagicKey)
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send DFU Control.startDfu with enterDfu = 1 and the correct magicKey')
        # ---------------------------------------------------------------------------
        start_dfu = StartDfu(device_index=self.deviceIndex,
                             feature_index=self.featureId,
                             enter_dfu=1,
                             dfu_control_param=0,
                             dfu_magic_key=StartDfu.DEFAULT.DFU_MAGIC_KEY)
        try:
            self.send_report_to_device(report=start_dfu, timeout=.6)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        """
        According to StartDfu specification: "This command may not return a response. If it does, the response is 
        empty (all bytes set to zero)." So we check that if there is a message it is a StartDfuResponse 
        (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;h=3bb246b0246f3318de4f1faaef1b0d65616647db;f=doc/hidpp20/x00c2_dfu_control.ad)
        """
        self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.common_message_queue,
            class_type=StartDfuResponse,
            timeout=0.4,
            allow_no_message=True)

        if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
            DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self,
                                                                              ble_service_changed_required=False)
        # end if

        # ---------------------------------------------------------------------------
        self.logTitle2('Test step 3: Send Root.GetFeature(0x0003)')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check the device is in Bootloader mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                        msg="Device not in bootloader")

        # This function does step 4, 5 and check 3
        DfuTestUtils.send_dfu_restart_function(test_case=self,
                                               ble_service_changed_required=False,
                                               log_step=4,
                                               log_check=3)

        self.testCaseChecked("FNT_00C2_0002")
    # end def test_StartDfuAPI

    @features('DfuControlDfuAvailable')
    @features('Feature00D0')
    @level('Business')
    def test_StartDfuWithDfuAvailable(self):
        """
        @tc_synopsis    Validates DFU Control Business case when DFU mode is available
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check notAvail= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.not_avail,
                         msg='The not_avail parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send DFU Control.startDfu with enterDfu = 1 and the correct magicKey')
        # ---------------------------------------------------------------------------
        start_dfu = StartDfu(device_index=self.deviceIndex,
                             feature_index=self.featureId,
                             enter_dfu=1,
                             dfu_control_param=0,
                             dfu_magic_key=StartDfu.DEFAULT.DFU_MAGIC_KEY)
        try:
            self.send_report_to_device(report=start_dfu, timeout=.6)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        """
        According to StartDfu specification: "This command may not return a response. If it does, the response is 
        empty (all bytes set to zero)." So we check that if there is a message it is a StartDfuResponse
        (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;h=3bb246b0246f3318de4f1faaef1b0d65616647db;f=doc/hidpp20/x00c2_dfu_control.ad)
        """
        self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.common_message_queue,
            class_type=StartDfuResponse,
            timeout=0.4,
            allow_no_message=True)

        if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
            DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self,
                                                                              ble_service_changed_required=False)
        # end if

        # ---------------------------------------------------------------------------
        self.logTitle2('Test step 3: Send Root.GetFeature(0x0003)')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check the device is in Bootloader mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                        msg="Device not in bootloader")

        # This function does step 4, 5 and check 3
        DfuTestUtils.send_dfu_restart_function(test_case=self,
                                               ble_service_changed_required=False,
                                               log_step=4,
                                               log_check=3)

        self.testCaseChecked("FNT_00C2_0003")
    # end def test_StartDfuWithDfuAvailable

    @features('DfuControlDfuNotAvailable')
    @level('Business')
    def test_StartDfuWithDfuNotAvailable(self):
        """
        @tc_synopsis    Validates DFU Control Business case when DFU mode is NOT available
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check notAvail= 1')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=get_dfu_status_response.not_avail,
                         msg='The not_avail parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send DFU Control.startDfu with enterDfu = 1 and the correct magicKey')
        # ---------------------------------------------------------------------------
        start_dfu = StartDfu(device_index=self.deviceIndex,
                             feature_index=self.featureId,
                             enter_dfu=1,
                             dfu_control_param=0,
                             dfu_magic_key=StartDfu.DEFAULT.DFU_MAGIC_KEY)
        start_dfu_response = self.send_report_wait_response(report=start_dfu,
                                                            response_queue=self.hidDispatcher.error_message_queue,
                                                            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check HIDPP_ERR_NOT_ALLOWED (5) Error Code returned by the device')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=start_dfu_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("FNT_00C2_0004")
    # end def test_StartDfuWithDfuNotAvailable

    @features('DfuControlDfuAvailable')
    @level('Functionality')
    def test_StartDfuNoOperationWithDfuAvailable(self):
        """
        @tc_synopsis    Validates the StartDfu no operation mode
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check notAvail= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.not_avail,
                         msg='The not_avail parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send DFU Control.startDfu with enterDfu = 0 and the correct magicKey')
        # ---------------------------------------------------------------------------
        start_dfu = StartDfu(device_index=self.deviceIndex,
                             feature_index=self.featureId,
                             enter_dfu=0,
                             dfu_control_param=0,
                             dfu_magic_key=StartDfu.DEFAULT.DFU_MAGIC_KEY)
        try:
            self.send_report_to_device(report=start_dfu, timeout=.6)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        """
        According to StartDfu specification: "This command may not return a response. If it does, the response is 
        empty (all bytes set to zero)." So we check that if there is a message it is a StartDfuResponse
        (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;h=3bb246b0246f3318de4f1faaef1b0d65616647db;f=doc/hidpp20/x00c2_dfu_control.ad)
        """
        self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.common_message_queue,
            class_type=StartDfuResponse,
            timeout=0.4,
            allow_no_message=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test step 3: Send Root.GetFeature(0x0003)')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check the device is in Main Application mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                        msg="Device not in Main Application")

        self.testCaseChecked("FNT_00C2_0005")
    # end def test_StartDfuNoOperationWithDfuAvailable

    @features('DfuControlDfuAvailable')
    @features('Feature00D0')
    @level('Functionality')
    def test_StartDfuIgnoreReservedEnterDfuWithDfuAvailable(self):
        """
        @tc_synopsis    Validates StartDfu processing ignores bits which are reserved for futur use in the first
                        enterDfu byte.
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check notAvail= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.not_avail,
                         msg='The not_avail parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over reserved_enterDfu in range[1..0x7F]')
        # ---------------------------------------------------------------------------
        for reserved_enter_dfu in compute_wrong_range([0], max_value=0x7F):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send DFU Control.startDfu with enterDfu = 1 and the correct magicKey')
            # ---------------------------------------------------------------------------
            start_dfu = StartDfu(device_index=self.deviceIndex,
                                 feature_index=self.featureId,
                                 enter_dfu=1,
                                 dfu_control_param=0,
                                 dfu_magic_key=StartDfu.DEFAULT.DFU_MAGIC_KEY)
            start_dfu.reserved_enter_dfu = reserved_enter_dfu
            try:
                self.send_report_to_device(report=start_dfu, timeout=.6)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try

            """
            According to StartDfu specification: "This command may not return a response. If it does, the response is 
            empty (all bytes set to zero)." So we check that if there is a message it is a StartDfuResponse
            (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;h=3bb246b0246f3318de4f1faaef1b0d65616647db;f=doc/hidpp20/x00c2_dfu_control.ad)
            """
            self.get_first_message_type_in_queue(
                queue=self.hidDispatcher.common_message_queue,
                class_type=StartDfuResponse,
                timeout=0.4,
                allow_no_message=True)

            if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
                DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self,
                                                                                  ble_service_changed_required=False)
            # end if

            # ---------------------------------------------------------------------------
            self.logTitle2('Test step 3: Send Root.GetFeature(0x0003)')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Check the device is in Bootloader mode')
            # ---------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                            msg="Device not in bootloader")

            # This function does step 4, 5 and check 3
            DfuTestUtils.send_dfu_restart_function(test_case=self,
                                                   ble_service_changed_required=False,
                                                   log_step=4,
                                                   log_check=3)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_00C2_0006")
    # end def test_StartDfuIgnoreReservedEnterDfuWithDfuAvailable

    @features('DfuControlDfuAvailable')
    @features('Feature00D0')
    @level('Functionality')
    def test_StartDfuIgnoreReservedWithDfuAvailable(self):
        """
        @tc_synopsis    Validates StartDfu processing ignores bytes which are reserved for future use.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check notAvail= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.not_avail,
                         msg='The not_avail parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over reserved bytes in range[1..0xFFFF]')
        # ---------------------------------------------------------------------------
        for reserved in compute_wrong_range([0], max_value=0xFFFF):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send DFU Control.startDfu with enterDfu = 1 and the correct magicKey')
            # ---------------------------------------------------------------------------
            start_dfu = StartDfu(device_index=self.deviceIndex,
                                 feature_index=self.featureId,
                                 enter_dfu=1,
                                 dfu_control_param=0,
                                 dfu_magic_key=StartDfu.DEFAULT.DFU_MAGIC_KEY)
            start_dfu.reserved = reserved
            try:
                self.send_report_to_device(report=start_dfu, timeout=.6)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try

            """
            According to StartDfu specification: "This command may not return a response. If it does, the response is 
            empty (all bytes set to zero)." So we check that if there is a message it is a StartDfuResponse
            (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;h=3bb246b0246f3318de4f1faaef1b0d65616647db;f=doc/hidpp20/x00c2_dfu_control.ad)
            """
            self.get_first_message_type_in_queue(
                queue=self.hidDispatcher.common_message_queue,
                class_type=StartDfuResponse,
                timeout=0.4,
                allow_no_message=True)

            if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
                DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self,
                                                                                  ble_service_changed_required=False)
            # end if

            # ---------------------------------------------------------------------------
            self.logTitle2('Test step 3: Send Root.GetFeature(0x0003)')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Check the device is in Bootloader mode')
            # ---------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                            msg="Device not in bootloader")

            # This function does step 4, 5 and check 3
            DfuTestUtils.send_dfu_restart_function(test_case=self,
                                                   ble_service_changed_required=False,
                                                   log_step=4,
                                                   log_check=3)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_00C2_0007")
    # end def test_StartDfuIgnoreReservedWithDfuAvailable

    @features('DfuControlDfuAvailable')
    @features('Feature00D0')
    @level('Functionality')
    def test_StartDfuDfuControlParam(self):
        """
        @tc_synopsis    Validates DFU Control.dfuControlParam processing if needed by the bootloader
                        (implementation seems to be project specific - TBC)
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check notAvail= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.not_avail,
                         msg='The not_avail parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send DFU Control.startDfu with enterDfu = 1 and the correct magicKey')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        start_dfu = StartDfu(device_index=self.deviceIndex,
                             feature_index=self.featureId,
                             enter_dfu=1,
                             dfu_control_param=f.PRODUCT.FEATURES.COMMON.DFU_CONTROL.F_DfuControlParam,
                             dfu_magic_key=StartDfu.DEFAULT.DFU_MAGIC_KEY)
        try:
            self.send_report_to_device(report=start_dfu, timeout=.6)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        """
        According to StartDfu specification: "This command may not return a response. If it does, the response is 
        empty (all bytes set to zero)." So we check that if there is a message it is a StartDfuResponse
        (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;h=3bb246b0246f3318de4f1faaef1b0d65616647db;f=doc/hidpp20/x00c2_dfu_control.ad)
        """
        self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.common_message_queue,
            class_type=StartDfuResponse,
            timeout=0.4,
            allow_no_message=True)

        if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
            DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self,
                                                                              ble_service_changed_required=False)
        # end if

        # ---------------------------------------------------------------------------
        self.logTitle2('Test step 3: Send Root.GetFeature(0x0003)')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check the device is in Bootloader mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                        msg="Device not in bootloader")
        # TODO check if parameters are processed

        # This function does step 4, 5 and check 3
        DfuTestUtils.send_dfu_restart_function(test_case=self,
                                               ble_service_changed_required=False,
                                               log_step=4,
                                               log_check=3)

        self.testCaseChecked("FNT_00C2_0008")
    # end def test_StartDfuDfuControlParam

    @features('DfuControl')
    @level('Functionality')
    def test_GetDfuStatusSoftwareId(self):
        """
        @tc_synopsis    Validates GetDfuStatus softwareId validity range

          SwID n boundary values 0 to F
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over softwareId  in its validity range')
        # ---------------------------------------------------------------------------
        for software_id in range(0x10):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
            # ---------------------------------------------------------------------------
            get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                          feature_index=self.featureId)
            get_dfu_status.softwareId = software_id
            get_dfu_status_response = self.send_report_wait_response(
                report=get_dfu_status,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetDfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check getDfuStatus response')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=get_dfu_status_response.reserved_enter_dfu,
                             msg='The reserved_enter_dfu parameter differs from the one expected')
            self.assertEqual(expected=0,
                             obtained=get_dfu_status_response.enter_dfu,
                             msg='The reserved_enter_dfu parameter differs from the one expected')
            self.assertEqual(expected=HexList(0),
                             obtained=get_dfu_status_response.dfu_control_param,
                             msg='The dfu_control_param parameter differs from the one expected')
            self.assertEqual(expected=0,
                             obtained=get_dfu_status_response.reserved_not_avail,
                             msg='The reserved_not_avail parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_00C2_0009")
    # end def test_GetDfuStatusSoftwareId

    @features('DfuControlDfuAvailable')
    @level('ErrorHandling')
    def test_StartDfuWithDfuAvailableWrongMagicKey(self):
        """
        @tc_synopsis    Validates StartDfu processing enforces the 3 bytes long magic key value
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Control.GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check notAvail= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.not_avail,
                         msg='The not_avail parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over magicKey value bit flipped combination')
        # ---------------------------------------------------------------------------
        for wrong_magic_key in compute_inverted_bit_range(HexList(Numeral(StartDfu.DEFAULT.DFU_MAGIC_KEY))):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send DFU Control.startDfu with several incorrect magicKey values plus ' +
                           'enterDfu = 1')
            # ---------------------------------------------------------------------------
            start_dfu = StartDfu(device_index=self.deviceIndex,
                                 feature_index=self.featureId,
                                 enter_dfu=1,
                                 dfu_control_param=0,
                                 dfu_magic_key=wrong_magic_key)
            start_dfu_response = self.send_report_wait_response(report=start_dfu,
                                                                response_queue=self.hidDispatcher.error_message_queue,
                                                                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=start_dfu_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')

            # ---------------------------------------------------------------------------
            self.logTitle2('Test step 3: Send Root.GetFeature(0x0003)')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Check the device is in Main Application mode')
            # ---------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
                            msg="Device not in Main Application")
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00C2_0001")
    # end def test_StartDfuWithDfuAvailableWrongMagicKey

    @features('DfuControl')
    @level('ErrorHandling')
    def test_GetDfuStatusWrongFunctionId(self):
        """
        @tc_synopsis    Validates DFU Control robustness processing (Feature 0x1E00)

        Tests function index error range [2..0xF]
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over function index invalid range ([2..0xF])')
        # ---------------------------------------------------------------------------
        for wrong_function_index in range(2, 0x10):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send DFU Control with a wrong function index value')
            # ---------------------------------------------------------------------------
            get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                          feature_index=self.featureId)
            get_dfu_status.functionIndex = wrong_function_index
            get_dfu_status_response = self.send_report_wait_response(
                report=get_dfu_status,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Check HIDPP_ERR_INVALID_FUNCTION_ID (7) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_dfu_status_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00C2_0002")
    # end def test_GetDfuStatusSoftwareId

    @features('DfuControl')
    @level('Robustness')
    def test_PaddingGetDfuStatus(self):
        """
        Validates   Validates GetDfuStatus padding bytes are ignored

        Request: 0x10.DeviceIndex.0x00.0x1F.0xPP.0xPP.0xPP
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over GetDfuStatus padding range')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(GetDfuStatus.DEFAULT.PADDING,
                                                             GetDfuStatus.LEN.PADDING // 8))):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send GetDfuStatus with several value for padding')
            # ---------------------------------------------------------------------------
            get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                          feature_index=self.featureId)
            get_dfu_status.padding = padding_byte
            get_dfu_status_response = self.send_report_wait_response(
                report=get_dfu_status,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetDfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate GetDfuStatus response')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=get_dfu_status_response.reserved_enter_dfu,
                             msg='The reserved_enter_dfu parameter differs from the one expected')
            self.assertEqual(expected=0,
                             obtained=get_dfu_status_response.enter_dfu,
                             msg='The reserved_enter_dfu parameter differs from the one expected')
            self.assertEqual(expected=HexList(0),
                             obtained=get_dfu_status_response.dfu_control_param,
                             msg='The dfu_control_param parameter differs from the one expected')
            self.assertEqual(expected=0,
                             obtained=get_dfu_status_response.reserved_not_avail,
                             msg='The reserved_not_avail parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00C2_0003")
    # end def test_PaddingGetDfuStatus

    @features('DfuControlDfuAvailable')
    @features('Feature00D0')
    @level('Robustness')
    def test_PaddingStartDfu(self):
        """
        Validates   Validates GetDfuStatus padding bytes are ignored

        Request: 0x10.DeviceIndex.0x00.0x1F.0xPP.0xPP.0xPP
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetDfuStatus')
        # ---------------------------------------------------------------------------
        get_dfu_status = GetDfuStatus(device_index=self.deviceIndex,
                                      feature_index=self.featureId)
        get_dfu_status_response = self.send_report_wait_response(report=get_dfu_status,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=GetDfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check notAvail= 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_dfu_status_response.not_avail,
                         msg='The not_avail parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over StartDfu padding range')
        # ---------------------------------------------------------------------------
        # The length of the range was way to big for the test so we decided to reduce it to 5 values
        for padding_byte in choices(compute_sup_values(HexList(Numeral(StartDfu.DEFAULT.PADDING,
                                                                     StartDfu.LEN.PADDING // 8))), elem_nb=5):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send DFU Control.startDfu with enterDfu = 1 and the correct magicKey')
            # ---------------------------------------------------------------------------
            start_dfu = StartDfu(device_index=self.deviceIndex,
                                 feature_index=self.featureId,
                                 enter_dfu=1,
                                 dfu_control_param=0,
                                 dfu_magic_key=StartDfu.DEFAULT.DFU_MAGIC_KEY)
            start_dfu.padding = padding_byte
            try:
                self.send_report_to_device(report=start_dfu, timeout=.6)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try

            """
            According to StartDfu specification: "This command may not return a response. If it does, the response is 
            empty (all bytes set to zero)." So we check that if there is a message it is a StartDfuResponse
            (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;h=3bb246b0246f3318de4f1faaef1b0d65616647db;f=doc/hidpp20/x00c2_dfu_control.ad)
            """
            self.get_first_message_type_in_queue(
                queue=self.hidDispatcher.common_message_queue,
                class_type=StartDfuResponse,
                timeout=0.4,
                allow_no_message=True)

            if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
                DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self,
                                                                                  ble_service_changed_required=False)
            # end if

            # ---------------------------------------------------------------------------
            self.logTitle2('Test step 3: Send Root.GetFeature(0x0003)')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Check the device is in Bootloader mode')
            # ---------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                            msg="Device not in bootloader")

            # This function does step 4, 5 and check 3
            DfuTestUtils.send_dfu_restart_function(test_case=self,
                                                   ble_service_changed_required=False,
                                                   log_step=4,
                                                   log_check=3)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_00C2_0004")
    # end def test_PaddingStartDfu
# end class ApplicationDfuControlTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
