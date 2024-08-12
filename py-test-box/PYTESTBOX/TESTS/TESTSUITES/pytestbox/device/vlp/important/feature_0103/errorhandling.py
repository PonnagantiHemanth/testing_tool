#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.important.feature_0103.errorhandling
:brief: VLP 1.0 ``VLPFeatureSet`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/05/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.vlp.base.vlpfeaturesetutils import VLPFeatureSetTestUtils
from pytestbox.device.vlp.important.feature_0103.vlpfeatureset import VLPFeatureSetTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class VLPFeatureSetErrorHandlingTestCase(VLPFeatureSetTestCase):
    """
    Validate ``VLPFeatureSet`` errorhandling test cases
    """

    @features("Feature0103")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_0103.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCount request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            VLPFeatureSetTestUtils.HIDppHelper.get_count_and_check_error(
                test_case=self, error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID], function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_0103_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature0103")
    @level("ErrorHandling")
    def test_get_feature_id_invalid_index(self):
        """
        Validate Invalid argument error is raised when sending Get Feature ID with invalid feature index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting invalid feature index values in range max"
                                 "feature index + 1 to 0xFF")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_feature_idx in compute_wrong_range(value=list(range(0, self.config.F_FeatureCount + 1)),
                                                       max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetFeatureID request with invalid feature index and check INVALID error "
                                     "returned as response")
            # ----------------------------------------------------------------------------------------------------------
            VLPFeatureSetTestUtils.HIDppHelper.get_feature_id_and_check_error(
                test_case=self, error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                feature_idx=HexList(invalid_feature_idx))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_103_0002", _AUTHOR)
    # end def test_get_feature_id_invalid_index
# end class VLPFeatureSetErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
