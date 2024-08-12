# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.important.feature_0102.business
:brief: VLP IRoot Business test cases
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/09/19
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import importlib

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.vlp.features.important.vlproot import VLPRoot
from pylibrary.tools.numeral import Numeral
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.vlprootutils import VLPRootTestUtils
from pytestbox.device.vlp.important.feature_0102.vlproot import VLPRootTestCase


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VLPRootBusinessTestCase(VLPRootTestCase):
    """
    Validates VLP Root business testcases.
    """

    @features("Feature0102")
    @level("Business")
    def test_all_feature_id_version(self):
        """
        Validate if all VLP feature versions defined in ini settings file are equal to the values returned by the DUT
        in application mode

        [0] getFeatureIndex(featureId) -> featureId, featureIndex, featureVersion, featureMaxMemory
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Retrieve all enabled VLP1.0 features version from ini config")
        # --------------------------------------------------------------------------------------------------------------
        raw_vlp_feature_list = self._retrieve_vlp_features_info()
        vlp_feature_list = self._revise_vlp_feature_info(raw_vlp_feature_list)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all enabled VLP features from ini config")
        # --------------------------------------------------------------------------------------------------------------
        for vlp_feature in vlp_feature_list:
            vlp_feature_module = getattr(importlib.import_module(vlp_feature.class_import_path), vlp_feature.class_name)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getFeatureIndex request with selected'
                                     f'featureId 0x{vlp_feature_module.FEATURE_ID:04x}')
            # ----------------------------------------------------------------------------------------------------------
            get_vlp_feature_response = VLPRootTestUtils.HIDppHelper.get_feature_index(
                test_case=self,
                feature_id=vlp_feature_module.FEATURE_ID,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)
            if vlp_feature_module.FEATURE_ID != VLPRoot.FEATURE_ID:
                self.assertNotEquals(unexpected=0,
                                     obtained=int(Numeral(get_vlp_feature_response.feature_idx)),
                                     msg=f"The feature index is 0 for feature 0x{vlp_feature_module.FEATURE_ID:04x}")
            # end if

            self.assertEqual(expected=vlp_feature.version,
                             obtained=int(Numeral(get_vlp_feature_response.feature_version)),
                             msg=f"The feature 0x{vlp_feature_module.FEATURE_ID:04x} version parameter does not match the "
                                 f"expected one!\nExpected: {vlp_feature.version}\nObtained: "
                                 f"{int(Numeral(get_vlp_feature_response.feature_version))}")

        self.testCaseChecked("BUS_0102_0001", _AUTHOR)
    # end def test_all_feature_id_version
# end class VLPRootInterfaceTestCase