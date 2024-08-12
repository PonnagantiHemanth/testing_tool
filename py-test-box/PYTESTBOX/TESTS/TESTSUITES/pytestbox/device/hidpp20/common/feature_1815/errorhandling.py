#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1815.errorhandling
:brief: HID++ 2.0 Hosts Info Error Handling test suite
:author: Christophe Roquebert
:date: 2021/03/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.hostsinfo import HostsInfoModel
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.hostsinfoutils import HostsInfoTestUtils
from pytestbox.device.hidpp20.common.feature_1815.hostsinfo import HostsInfoTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HostsInfoErrorHandlingTestCase(HostsInfoTestCase):
    """
    Validates Hosts Info Error Handling TestCases
    """

    @features('Feature1815')
    @level('ErrorHandling')
    def test_function_index_out_of_range(self):
        """
        Check an invalid Function index raises an error INVALID_FUNCTION_ID (7)

        """
        for function_index in compute_wrong_range(value=list(range(self.feature_1815.get_max_function_index() + 1)),
                                                max_value=0xF):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send request with function index out of range')
            # ----------------------------------------------------------------------------
            request = self.feature_1815.get_feature_info_cls(self.deviceIndex, self.feature_1815_index)
            request.functionIndex = function_index

            err_resp = self.send_report_wait_response(
                report=request,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_FUNCTION_ID (7) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=request.featureIndex,
                function_index=request.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID])
        # end for

        self.testCaseChecked("ROT_1815_0000")
    # end def test_function_index_out_of_range

    @features('Feature1815')
    @level('ErrorHandling')
    def test_get_host_info_wrong_host_index(self):
        """
        Check getHostInfo returns InvalidArgument if an invalid host index is given.
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getFeatureInfo request to retrieve num_hosts value')
        # ----------------------------------------------------------------------------
        get_feature_info_resp = HostsInfoTestUtils.HIDppHelper.get_feature_info(self)

        for wrong_host_index in compute_wrong_range(value=list(range(int(Numeral(get_feature_info_resp.num_hosts)))),
                                                  max_value=0xFE):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostInfo request with host index out of range')
            # ----------------------------------------------------------------------------
            get_host_info_req = self.feature_1815.get_host_info_cls(
                self.deviceIndex, self.feature_1815_index, host_index=wrong_host_index)

            err_resp = self.send_report_wait_response(
                report=get_host_info_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=int(Numeral(get_host_info_req.featureIndex)),
                function_index=get_host_info_req.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for

        self.testCaseChecked("ROT_1815_0001")
    # end def test_get_host_info_wrong_host_index

    @features('Feature1815')
    @level('ErrorHandling')
    def test_get_host_descriptor_wrong_host_index(self):
        """
        Check getHostDescriptor returns InvalidArgument if an invalid host index is given.
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getFeatureInfo request to retrieve num_hosts value')
        # ----------------------------------------------------------------------------
        get_feature_info_resp = HostsInfoTestUtils.HIDppHelper.get_feature_info(self)

        for wrong_host_index in compute_wrong_range(value=list(range(int(Numeral(get_feature_info_resp.num_hosts)))),
                                                  max_value=0xFE):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostDescriptor request with host index out of range')
            # ----------------------------------------------------------------------------
            get_host_descriptor_req = self.feature_1815.get_host_descriptor_cls(
                self.deviceIndex, self.feature_1815_index, host_index=wrong_host_index)

            err_resp = self.send_report_wait_response(
                report=get_host_descriptor_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=int(Numeral(get_host_descriptor_req.featureIndex)),
                function_index=get_host_descriptor_req.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for

        self.testCaseChecked("ROT_1815_0002")
    # end def test_get_host_descriptor_wrong_host_index

    @features('Feature1815v2+')
    @level('ErrorHandling')
    def test_get_host_descriptor_wrong_page_index(self):
        """
        Check getHostDescriptor returns InvalidArgument if an invalid page index is given.
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostInfo request to retrieve num_pages value')
        # ----------------------------------------------------------------------------
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0)

        for wrong_page_index in compute_wrong_range(value=list(range(int(Numeral(get_host_info_resp.num_pages))))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostDescriptor request with page index out of range')
            # ----------------------------------------------------------------------------
            get_host_descriptor_req = self.feature_1815.get_host_descriptor_cls(
                self.deviceIndex, self.feature_1815_index, host_index=0, page_index=wrong_page_index)

            err_resp = self.send_report_wait_response(
                report=get_host_descriptor_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=int(Numeral(get_host_descriptor_req.featureIndex)),
                function_index=get_host_descriptor_req.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for

        self.testCaseChecked("ROT_1815_0003")
    # end def test_get_host_descriptor_wrong_page_index

    @features('Feature1815')
    @level('ErrorHandling')
    def test_get_host_friendly_name_wrong_host_index(self):
        """
        Check getHostFriendlyName returns InvalidArgument if an invalid host index is given.
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getFeatureInfo request to retrieve num_hosts value')
        # ----------------------------------------------------------------------------
        get_feature_info_resp = HostsInfoTestUtils.HIDppHelper.get_feature_info(self)

        for wrong_host_index in compute_wrong_range(value=list(range(int(Numeral(get_feature_info_resp.num_hosts)))),
                                                  max_value=0xFE):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostFriendlyName request with host index out of range')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_req = self.feature_1815.get_host_friendly_name_cls(
                self.deviceIndex, self.feature_1815_index, host_index=wrong_host_index, byte_index=0)

            err_resp = self.send_report_wait_response(
                report=get_host_friendly_name_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=int(Numeral(get_host_friendly_name_req.featureIndex)),
                function_index=get_host_friendly_name_req.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for

        self.testCaseChecked("ROT_1815_0004")
    # end def test_get_host_friendly_name_wrong_host_index

    @features('Feature1815')
    @level('ErrorHandling')
    def test_set_host_friendly_name_wrong_host_index(self):
        """
        Check setHostFriendlyName returns InvalidArgument if an invalid host index is given.
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getFeatureInfo request to retrieve num_hosts value')
        # ----------------------------------------------------------------------------
        get_feature_info_resp = HostsInfoTestUtils.HIDppHelper.get_feature_info(self)

        for wrong_host_index in compute_wrong_range(value=list(range(int(Numeral(get_feature_info_resp.num_hosts)))),
                                                  max_value=0xFE):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setHostFriendlyName request with host index out of range')
            # ----------------------------------------------------------------------------
            set_host_friendly_name_req = self.feature_1815.set_host_friendly_name_cls(
                self.deviceIndex, self.feature_1815_index, host_index=wrong_host_index, byte_index=0,
                name_chunk='bad host index')

            err_resp = self.send_report_wait_response(
                report=set_host_friendly_name_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=int(Numeral(set_host_friendly_name_req.featureIndex)),
                function_index=set_host_friendly_name_req.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for

        self.testCaseChecked("ROT_1815_0005")
    # end def test_set_host_friendly_name_wrong_host_index

    @features('Feature1815')
    @level('ErrorHandling')
    def test_get_host_os_version_wrong_host_index(self):
        """
        Check GetHostOsVersion returns InvalidArgument is an invalid host index is given.
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getFeatureInfo request to retrieve num_hosts value')
        # ----------------------------------------------------------------------------
        get_feature_info_resp = HostsInfoTestUtils.HIDppHelper.get_feature_info(self)

        for wrong_host_index in compute_wrong_range(value=list(range(int(Numeral(get_feature_info_resp.num_hosts)))),
                                                  max_value=0xFE):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetHostOsVersion request with host index out of range')
            # ----------------------------------------------------------------------------
            get_host_os_version_req = self.feature_1815.get_host_os_version_cls(
                self.deviceIndex, self.feature_1815_index, host_index=wrong_host_index)

            err_resp = self.send_report_wait_response(
                report=get_host_os_version_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=int(Numeral(get_host_os_version_req.featureIndex)),
                function_index=get_host_os_version_req.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for

        self.testCaseChecked("ROT_1815_0006")
    # end def test_get_host_os_version_wrong_host_index

    @features('Feature1815')
    @level('ErrorHandling')
    def test_set_host_os_version_wrong_host_index(self):
        """
        Check SetHostOsVersion returns InvalidArgument is an invalid host index is given.
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getFeatureInfo request to retrieve num_hosts value')
        # ----------------------------------------------------------------------------
        get_feature_info_resp = HostsInfoTestUtils.HIDppHelper.get_feature_info(self)

        for wrong_host_index in compute_wrong_range(value=list(range(int(Numeral(get_feature_info_resp.num_hosts)))),
                                                  max_value=0xFE):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetHostOsVersion request with host index out of range')
            # ----------------------------------------------------------------------------
            set_host_os_version_req = self.feature_1815.set_host_os_version_cls(
                self.deviceIndex, self.feature_1815_index, host_index=wrong_host_index, os_type=0, os_version=0,
                os_revision=0, os_build=0)

            err_resp = self.send_report_wait_response(
                report=set_host_os_version_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=int(Numeral(set_host_os_version_req.featureIndex)),
                function_index=set_host_os_version_req.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for

        self.testCaseChecked("ROT_1815_0007")
    # end def test_set_host_os_version_wrong_host_index

    @features('Feature1815v2+')
    @level('ErrorHandling')
    def test_move_host(self):
        """
        Check moveHost() command is not supported and raises an HIDPP_ERR_NOT_ALLOWED (5) error

        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send deprecated moveHost request')
        # ----------------------------------------------------------------------------
        request = self.feature_1815.get_feature_info_cls(self.deviceIndex, self.feature_1815_index)
        request.functionIndex = HostsInfoModel.INDEX.MOVE_HOST

        err_resp = self.send_report_wait_response(
            report=request,
            response_queue=self.hidDispatcher.error_message_queue,
            response_class_type=Hidpp2ErrorCodes)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HIDPP_ERR_NOT_ALLOWED (5) Error Code returned by the device')
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
            test_case=self,
            error_message=err_resp,
            feature_index=request.featureIndex,
            function_index=request.functionIndex,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ROT_1815_0008")
    # end def test_move_host

    @features('Feature1815v2+')
    @level('ErrorHandling')
    def test_delete_host(self):
        """
        Check deleteHost() command is not supported and raises an HIDPP_ERR_NOT_ALLOWED (5) error

        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send deprecated deleteHost request')
        # ----------------------------------------------------------------------------
        request = self.feature_1815.get_feature_info_cls(self.deviceIndex, self.feature_1815_index)
        request.functionIndex = HostsInfoModel.INDEX.DELETE_HOST

        err_resp = self.send_report_wait_response(
            report=request,
            response_queue=self.hidDispatcher.error_message_queue,
            response_class_type=Hidpp2ErrorCodes)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HIDPP_ERR_NOT_ALLOWED (5) Error Code returned by the device')
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
            test_case=self,
            error_message=err_resp,
            feature_index=request.featureIndex,
            function_index=request.functionIndex,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ROT_1815_0008")
    # end def test_delete_host
# end class HostsInfoErrorHandlingTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
