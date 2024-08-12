#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.important.feature_0103.robustness
:brief: VLP 1.0 ``VLPFeatureSet`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/05/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSet
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_inf_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.vlp.base.vlpfeaturesetutils import VLPFeatureSetTestUtils
from pytestbox.device.vlp.important.feature_0103.vlpfeatureset import VLPFeatureSetTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class VLPFeatureSetRobustnessTestCase(VLPFeatureSetTestCase):
    """
    Validate ``VLPFeatureSet`` robustness test cases
    """

    @features("Feature0103")
    @level("Robustness")
    def test_get_count_software_id(self):
        """
        Validate ``GetCount`` software id field is ignored by the firmware

        [0] getCount() -> count

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(VLPFeatureSet.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCount request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_count(test_case=self, software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCountResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPFeatureSetTestUtils.GetCountResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_0103.get_count_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0103_0001#1", _AUTHOR)
    # end def test_get_count_software_id

    @features("Feature0103")
    @level("Robustness")
    def test_get_feature_id_software_id(self):
        """
        Validate ``GetFeatureID`` software id field is ignored by the firmware

        [1] getFeatureID(featureIdx) -> featureIdx, featureId, featureType, featureVersion, featureMaxMemory

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.FeatureIdx.0xPP.0xPP

        SwID boundary values [0..F]
        """
        feature_idx = self.feature_0103_index
        feature_id = HexList("0103")
        feature_max_memory = self.config.F_FeatureMaxMemory
        feature_version = self.config_manager.get_feature_version(self.config)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(VLPFeatureSet.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureID request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(test_case=self, feature_idx=feature_idx,
                                                                         software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureIDResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPFeatureSetTestUtils.GetFeatureIDResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "feature_idx": (checker.check_feature_idx, feature_idx),
                    "feature_id": (checker.check_feature_id, feature_id),
                    "feature_version": (checker.check_feature_version, feature_version),
                    "feature_type": (checker.check_feature_type, self.FEATURE_TYPE_NOT_HIDDEN),
                    "feature_max_memory": (checker.check_feature_max_memory, feature_max_memory)
                }
            )
            checker.check_fields(self, response, self.feature_0103.get_feature_id_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0103_0001#2", _AUTHOR)
    # end def test_get_feature_id_software_id

    @features("Feature0103")
    @level("Robustness")
    def test_get_all_feature_ids_software_id(self):
        """
        Validate ``GetAllFeatureIDs`` software id field is ignored by the firmware

        [2] getAllFeatureIDs() -> featureRecordsCount, featureRecordsSize, featureIdx, featureId,
        featureType, featureVersion, featureMaxMemory

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(VLPFeatureSet.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAllFeatureIDs request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPFeatureSetTestUtils.HIDppHelper.get_all_feature_ids(test_case=self, software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAllFeatureIDsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            self.check_feature_records(response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0103_0001#3", _AUTHOR)
    # end def test_get_all_feature_ids_software_id
# end class VLPFeatureSetRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
