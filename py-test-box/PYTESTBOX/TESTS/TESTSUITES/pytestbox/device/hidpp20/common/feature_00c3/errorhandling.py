#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00c3.errorhandling
:brief: HID++ 2.0  Device Secure DFU control error handling test suite
:author: Stanislas Cottard <scottard@logitech.com>, Kevin Dayet <kdayet@logitech.com>
:date: 2020/09/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.numeral import to_int
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_00c3.securedfucontrol import DeviceSecureDfuControlTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceSecureDfuControlErrorHandlingTestCase(DeviceSecureDfuControlTestCase):
    """
    Validate Secure DFU Control error handling testcases for the device (feature 0x00C3).
    """

    @features('SecureDfuControlAllActionTypes')
    @level('ErrorHandling')
    @services('Debugger')
    def test_set_dfu_control_wrong_magic_key(self):
        """
        setDfuControl processing shall enforce the magic key value - Every bit flipped combination shall be verify
        """
        self.generic_set_dfu_control_wrong_magic_key()

        self.testCaseChecked("ERR_00C3_0001")
    # end def test_set_dfu_control_wrong_magic_key

    @features('SecureDfuControlAllActionTypes')
    @level('ErrorHandling')
    @services('Debugger')
    def test_get_dfu_control_wrong_function_index(self):
        """
        Invalid Function index shall raise an error. Tests function index error range [2..0xF]
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over function index invalid range ([2..0xF])')
        # ---------------------------------------------------------------------------
        for wrong_function_index in range(2, 0x10):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Test Step 1: Send DFU getDfuControl with functionIndex='
                                     f'{wrong_function_index}')
            # ---------------------------------------------------------------------------
            get_dfu_control = self.feature_under_test.get_dfu_control_cls(device_index=self.deviceIndex,
                                                                          feature_index=self.feature_id)
            get_dfu_control.functionIndex = wrong_function_index
            get_dfu_control_response = self.send_report_wait_response(
                report=get_dfu_control,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_FUNCTION_ID (0x07) Error Code returned by '
                                      'the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=to_int(get_dfu_control_response.errorCode),
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ERR_00C3_0002")
    # end def test_get_dfu_control_wrong_function_index
# end class DeviceSecureDfuControlErrorHandlingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
