# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.important.feature_0102.functionality
:brief: VLP IRoot Functionality test cases
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/09/19
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.vlp.features.important.vlproot import GetPingData
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.configurationmanager import ConfigurationManager
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
class VLPRootFunctionalityTestCase(VLPRootTestCase):
    """
    Validates VLP Root functionality testcases.
    """
    @features('Feature0102')
    @level('Functionality')
    def test_ping_data(self):
        """
        Validate Ping Data Functionality.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over most significant pingData within its valid range")
        # --------------------------------------------------------------------------------------------------------------
        for test_ping_data in compute_sup_values(GetPingData.DEFAULT.PING_DATA):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetPingData request")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPRootTestUtils.HIDppHelper.get_ping_data(
                test_case=self,
                ping_data=test_ping_data,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPingDataResponse fields")
            # --------------------------------------------------------------------------------------------------------------
            checker = VLPRootTestUtils.GetPingDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_0102_index)),
                "ping_data": (checker.check_ping_data, test_ping_data)
            })
            checker.check_fields(self, response, self.feature_0102.get_ping_data_response_cls, check_map)
        # end for
        self.testCaseChecked("FUN_0102_0001", _AUTHOR)

    # end def test_ping_data

    @features('Feature0102')
    @level('Time-consuming')
    def test_all_feature_id(self):
        """
        Validate Get Feature Index with all possible Feature ID value
        """
        # ---------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over feature index range')
        # ---------------------------------------------------------------
        feature_id_list = []
        # Important range
        feature_id_test_list = list(range(1, 0xF0))
        feature_id_test_list.extend(list(range(0x0100, 0x0110))) # VLP Important range
        # Common range
        feature_id_test_list.extend(list(range(0x1000, 0x1010)))
        feature_id_test_list.extend(list(range(0x1300, 0x1310)))
        feature_id_test_list.extend(list(range(0x1500, 0x1510)))
        feature_id_test_list.extend(list(range(0x1600, 0x1610)))
        feature_id_test_list.extend(list(range(0x1700, 0x1710)))
        feature_id_test_list.extend(list(range(0x1800, 0x18F0)))
        feature_id_test_list.extend(list(range(0x1980, 0x1990)))
        feature_id_test_list.extend(list(range(0x19A0, 0x19FF))) # VLP common features
        feature_id_test_list.extend(list(range(0x1A10, 0x1A30)))
        feature_id_test_list.extend(list(range(0x1B00, 0x1C00)))
        feature_id_test_list.extend(list(range(0x1D40, 0x1F30)))
        # Mouse range
        feature_id_test_list.extend(list(range(0x2000, 0x2010)))
        feature_id_test_list.extend(list(range(0x2110, 0x2160)))
        feature_id_test_list.extend(list(range(0x2200, 0x2260)))
        feature_id_test_list.extend(list(range(0x2300, 0x2400)))
        # Keyboard range
        feature_id_test_list.extend(list(range(0x40A0, 0x4230)))
        feature_id_test_list.extend(list(range(0x4520, 0x4610)))
        # Touchpad range
        feature_id_test_list.extend(list(range(0x6100, 0x6120)))
        feature_id_test_list.extend(list(range(0x6500, 0x6510)))
        # Gaming range
        feature_id_test_list.extend(list(range(0x8000, 0x8140)))
        feature_id_test_list.extend(list(range(0x8300, 0x8400)))
        # Peripheral range
        feature_id_test_list.extend(list(range(0x9000, 0x9010)))
        feature_id_test_list.extend(list(range(0x9200, 0x92F0)))
        feature_id_test_list.extend(list(range(0x9300, 0x9330)))
        # Prototypes range
        feature_id_test_list.extend(list(range(0xF000, 0xF0D0)))

        for feature_id in feature_id_test_list:
            # ---------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Root.GetFeature with featureId in all known ranges')
            # ---------------------------------------------------------------------------------
            get_feature_response = VLPRootTestUtils.HIDppHelper.get_feature_index(
                test_case=self,
                feature_id=feature_id,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)

            feature_index = int(get_feature_response.feature_idx)
            if feature_index != 0:
                # -----------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate VLPRoot.GetFeature.featIndex is unique')
                # -----------------------------------------------------------------------
                self.assertFalse(get_feature_response.feature_idx in feature_id_list,
                                 msg=(f"The index in the feature table shall be unique (\n"
                                      f"{get_feature_response.feature_idx} already in {str(feature_id_list)})."))
                feature_id_list.append(int(get_feature_response.feature_idx))
                # This print should stay in the console because it has been considered useful
                print('feature index=0x%s version=%d on position %d' % (
                    str(Numeral(feature_id, 2)),
                    int(Numeral(get_feature_response.feature_version)),
                    int(get_feature_response.feature_idx)))
            else:
                # ----------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check VLPRoot.GetFeature.featVer is 0 if feature not found')
                # ----------------------------------------------------------------------------------
                # The value 0 indicates the feature was not found
                self.assertEqual(expected=0,
                                 obtained=int(Numeral(get_feature_response.feature_version)),
                                 msg="The feature_version shall be 0 if feature not supported.")
            # end if
        # end for
        self.assertEqual(
            expected=int(Numeral(self.config_manager.get_feature(ConfigurationManager.ID.VLP_FEATURE_COUNT))),
            obtained=len(feature_id_list),
            msg=f'Found {len(feature_id_list)} features, expected '
                f'{int(Numeral(self.config_manager.get_feature(ConfigurationManager.ID.VLP_FEATURE_COUNT)))}')

        self.testCaseChecked("FUN_0102_0002")
    # end def test_all_feature_id
# end class VLPRootFunctionalityTestCase