#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.important.feature_0103.business
:brief: VLP 1.0 ``VLPFeatureSet`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/05/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import random

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.vlp.base.vlpfeaturesetutils import VLPFeatureSetTestUtils
from pytestbox.device.vlp.important.feature_0103.vlpfeatureset import VLPFeatureSetTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class VLPFeatureSetBusinessTestCase(VLPFeatureSetTestCase):
    """
    Validate ``VLPFeatureSet`` business test cases
    """

    @features("Feature0103")
    @level("Business")
    def test_get_feature_id_coherence(self):
        """
        Validate Get Feature ID response parameters do not change from one call to another
        """
        sample_size = min(self.DEFAULT_LOOP_COUNT, self.config.F_FeatureCount)
        feature_indexes = random.choices(range(self.config.F_FeatureCount + 1), k=sample_size)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over a sample size = {sample_size} of feature index values in random order"
                           )
        # --------------------------------------------------------------------------------------------------------------
        for feature_idx in feature_indexes:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureID request with current feature index = {feature_idx}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(self, HexList(feature_idx))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Check GetFeatureIDResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            self.check_feature_record(response)
            old_feature_version = response.feature_version
            old_feature_max_memory = response.feature_max_memory

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetCount request")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_count(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCountResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPFeatureSetTestUtils.GetCountResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_0103.get_count_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureID request with current feature index = {feature_idx}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(self, HexList(feature_idx))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureIDResponse for the current index value exactly matches the"
                                      "first GetFeatureIDResponse")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(old_feature_version, response.feature_version,
                             "Feature version in GetFeatureIDResponse is not as expected")
            self.assertEqual(old_feature_max_memory, response.feature_max_memory,
                             "Feature max memory in GetFeatureIDResponse is not as expected")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_0103_0001", _AUTHOR)
    # end def test_get_feature_id_coherence
# end class VLPFeatureSetBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
