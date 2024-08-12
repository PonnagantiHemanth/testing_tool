#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.important.feature_0103.functionality
:brief: VLP 1.0 ``VLPFeatureSet`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/05/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import random

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.vlp.features.important.vlpfeatureset import GetAllFeatureIDsResponsePayloadMixin
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
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
class VLPFeatureSetFunctionalityTestCase(VLPFeatureSetTestCase):
    """
    Validate ``VLPFeatureSet`` functionality test cases
    """

    @features("Feature0103")
    @level("Functionality")
    def test_get_feature_id_for_all_feature_index(self):
        """
        Validate sending Get Feature ID request with all feature index values in order from range 0 to max feature
        index gives expected feature record response
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available feature index in range 0 to max feature index")
        # --------------------------------------------------------------------------------------------------------------
        for feature_idx in range(self.config.F_FeatureCount + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureID request with current feature index = {feature_idx}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(self, HexList(feature_idx))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureIDResponse fields values matches the expected feature record"
                                      f"for the current feature index = {feature_idx}")
            # ----------------------------------------------------------------------------------------------------------
            self.check_feature_record(response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_0103_0001", _AUTHOR)
    # end def test_get_feature_id_for_all_feature_index

    @features("Feature0103")
    @level("Functionality")
    def test_get_feature_id_for_all_feature_index_in_random(self):
        """
        Validate sending Get Feature ID request with all feature index values from 0 to max feature index in a random
        order gives expected feature record response
        """
        feature_index_list = list(range(self.config.F_FeatureCount + 1))
        random.shuffle(feature_index_list)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available feature index in range 0 to max feature index in a"
                                 "random order")
        # --------------------------------------------------------------------------------------------------------------
        for feature_idx in feature_index_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureID request with current feature index = {feature_idx}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(self, HexList(feature_idx))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureIDResponse fields values matches the expected feature record"
                                      "for the current random index")
            # ----------------------------------------------------------------------------------------------------------
            self.check_feature_record(response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_0103_0002", _AUTHOR)
    # end def test_get_feature_id_for_all_feature_index_in_random

    @features("Feature0103")
    @level("Functionality")
    def test_total_feature_memory(self):
        """
        Check Total Feature memory does not exceed availableTotalMemory
        """
        total_feature_memory = 0
        total_available_memory = self.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT.F_TotalMemory
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available feature index")
        # --------------------------------------------------------------------------------------------------------------
        for feature_id in range(self.config.F_FeatureCount + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Get Feature ID request with the selected feature index")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(self, HexList(feature_id))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureIDResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            self.check_feature_record(response)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Sum the current feature memory to totalFeatureMemory")
            # ----------------------------------------------------------------------------------------------------------
            total_feature_memory += to_int(Numeral(response.feature_max_memory))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Total Feature memory does not exceed availableTotalMemory")
        # --------------------------------------------------------------------------------------------------------------
        self.assertLessEqual(total_feature_memory, total_available_memory,
                             msg="Total Feature memory exceeds availableTotalMemory")

        self.testCaseChecked("FUN_0103_0003", _AUTHOR)
    # end def test_total_feature_memory

    @features("Feature0103")
    @level("Functionality")
    def test_feature_count(self):
        """
        Check feature count value from Get Count and Get All Feature Ids requests are equal
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCount request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPFeatureSetTestUtils.HIDppHelper.get_count(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCountResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPFeatureSetTestUtils.GetCountResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_0103.get_count_response_cls, check_map)
        feature_count_1 = response.count

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAllFeatureIds request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPFeatureSetTestUtils.HIDppHelper.get_all_feature_ids(self)
        feature_records = GetAllFeatureIDsResponsePayloadMixin.fromHexList(HexList(response.vlp_payload))
        feature_count_2 = feature_records.feature_records_count

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAllFeatureIdsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        self.check_feature_records(response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the value of feature count from GetCountResponse and"
                                  "GetAllFeatureIdsResponse are same")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(feature_count_1, feature_count_2, msg="Feature count value from Get Count and Get All Feature"
                                                               "Ids requests are not equal")

        self.testCaseChecked("FUN_0103_0004", _AUTHOR)
    # end def test_feature_count
# end class VLPFeatureSetFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
