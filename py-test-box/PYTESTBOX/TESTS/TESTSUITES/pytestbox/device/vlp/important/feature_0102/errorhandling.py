# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.important.feature_0102.errorhandling
:brief: VLP IRoot Error Handling test cases
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/09/19
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import VlpErrorCodes
from pyhid.vlp.features.important.vlproot import VLPRoot
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.vlprootutils import VLPRootTestUtils
from pytestbox.device.vlp.important.feature_0102.vlproot import VLPRootTestCase


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_END = "End Test Loop"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VLPRootErrorHandlingTestCase(VLPRootTestCase):
    """
    Validates VLP Root error handling testcases.
    """
    @features("Feature0102")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        feature_id = VLPRoot.FEATURE_ID
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over wrong function index (several interesting values)")
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(
                value=list(range(self.feature_0102.get_max_function_index() + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            VLPRootTestUtils.HIDppHelper.get_feature_index_and_check_error(
                test_case=self,
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_id=feature_id,
                function_index=function_index,
                error_codes=[VlpErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_0102_0001", _AUTHOR)
    # end def test_wrong_function_index
# end class VLPRootErrorHandlingTestCase
