#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.important.feature_0103.interface
:brief: VLP 1.0 ``VLPFeatureSet`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
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
class VLPFeatureSetInterfaceTestCase(VLPFeatureSetTestCase):
    """
    Validate ``VLPFeatureSet`` interface test cases
    """

    @features("Feature0103")
    @level("Interface")
    def test_get_count(self):
        """
        Validate ``GetCount`` normal processing

        [0] getCount() -> count
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCount request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPFeatureSetTestUtils.HIDppHelper.get_count(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCountResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPFeatureSetTestUtils.GetCountResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_0103_index)),
            }
        )
        checker.check_fields(self, response, self.feature_0103.get_count_response_cls, check_map)

        self.testCaseChecked("INT_0103_0001", _AUTHOR)
    # end def test_get_count

    @features("Feature0103")
    @level("Interface")
    def test_get_feature_id(self):
        """
        Validate ``GetFeatureID`` normal processing

        [1] getFeatureID(featureIdx) -> featureIdx, featureId, featureVersion, featureMaxMemory
        """
        feature_idx = self.feature_0103_index
        feature_id = HexList("0103")
        feature_max_memory = self.config.F_FeatureMaxMemory
        feature_version = self.config_manager.get_feature_version(self.config)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetFeatureID request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(test_case=self, feature_idx=feature_idx)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetFeatureIDResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPFeatureSetTestUtils.GetFeatureIDResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_0103_index)),
                "feature_idx": (checker.check_feature_idx, feature_idx),
                "feature_id": (checker.check_feature_id, feature_id),
                "feature_version": (checker.check_feature_version, feature_version),
                "feature_type": (checker.check_feature_type, self.FEATURE_TYPE_NOT_HIDDEN),
                "feature_max_memory": (checker.check_feature_max_memory, feature_max_memory)
            }
        )
        checker.check_fields(self, response, self.feature_0103.get_feature_id_response_cls, check_map)

        self.testCaseChecked("INT_0103_0002", _AUTHOR)
    # end def test_get_feature_id

    @features("Feature0103")
    @level("Interface")
    def test_get_all_feature_ids(self):
        """
        Validate ``GetAllFeatureIDs`` normal processing

        [2] getAllFeatureIDs() -> featureRecordsCount, featureRecordsSize, featureIdx, featureId,
        featureType, featureVersion, featureMaxMemory
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAllFeatureIDs request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPFeatureSetTestUtils.HIDppHelper.get_all_feature_ids(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAllFeatureIDsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPFeatureSetTestUtils.GetAllFeatureIDsResponseChecker
        check_map = \
            {
                "device_index": (checker.check_device_index, HexList(self.device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_0103_index)),
            }
        checker.check_fields(self, response, self.feature_0103.get_all_feature_ids_response_cls, check_map)
        self.check_feature_records(response)
        self.testCaseChecked("INT_0103_0003", _AUTHOR)
    # end def test_get_all_feature_ids
# end class FeatureSetInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
