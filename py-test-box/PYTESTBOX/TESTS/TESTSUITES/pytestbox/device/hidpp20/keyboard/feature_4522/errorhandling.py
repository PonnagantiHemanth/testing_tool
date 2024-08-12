#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4522.errorhandling
:brief: HID++ 2.0 DisableKeysByUsage errorhandling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/10/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsage
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysbyusageutils import DisableKeysByUsageTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4522.disablekeysbyusage import DisableKeysByUsageBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysByUsageErrorHandlingTestCase(DisableKeysByUsageBaseTestCase):
    """
    x4522 - Disable keys by usage error handling test case
    """
    @features('Feature4522')
    @level('ErrorHandling')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_A, ))
    def test_invalid_function_index(self):
        """
        Invalid Function index shall raise an error InvalidFunctionId (0x07)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over functionIndex invalid range (typical wrong values)')
        # ---------------------------------------------------------------------------
        for invalid_function_index in compute_wrong_range(
                list(range(DisableKeysByUsage.MAX_FUNCTION_INDEX+1)), max_value=0xF):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DisableKeys with functionIndex = ')
            # ---------------------------------------------------------------------------
            response = DisableKeysByUsageTestUtils.disable_key_with_function_id(test_case=self,
                                                                                function_id=invalid_function_index,
                                                                                key_id=KEY_ID.KEYBOARD_A)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidFunctionId(7) returned by the device')
            # ---------------------------------------------------------------------------
            DisableKeysByUsageTestUtils.check_error_invalid_function_id(test_case=self,
                                                                        response=response)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked('ERR_4522_0001')
    # end def test_invalid_function_index
# end class DisableKeysByUsageErrorHandlingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
