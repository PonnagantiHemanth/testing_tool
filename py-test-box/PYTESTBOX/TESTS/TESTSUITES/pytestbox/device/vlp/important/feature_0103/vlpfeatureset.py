#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.important.feature_0103.vlpfeatureset
:brief: Validate VLP 1.0 ``VLPFeatureSet`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.vlp.features.important.vlpfeatureset import GetAllFeatureIDsResponse
from pyhid.vlp.features.important.vlpfeatureset import GetAllFeatureIDsResponsePayloadMixin
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int, Numeral
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.vlp.base.vlpfeaturesetutils import VLPFeatureSetTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class VLPFeatureSetTestCase(DeviceBaseTestCase):
    """
    Validate ``VLPFeatureSet`` TestCases in Application mode
    """
    FEATURE_TYPE_HIDDEN = True
    FEATURE_TYPE_NOT_HIDDEN = False
    DEFAULT_LOOP_COUNT = 5

    VLP_FEATURES_SUBSYSTEM_NAME = {
        0x0102: "IMPORTANT.ROOT",
        0x0103: "IMPORTANT.FEATURE_SET",
        0x19A1: "COMMON.CONTEXTUAL_DISPLAY",
    }

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0103 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0103_index, self.feature_0103, self.device_index, _ = \
            VLPFeatureSetTestUtils.HIDppHelper.get_vlp_parameters(test_case=self)

        self.config = self.f.PRODUCT.FEATURES.VLP.IMPORTANT.FEATURE_SET
    # end def setUp

    def check_feature_records(self, response):
        """
        Check the feature records information

        :param response: The get all feature ids response
        :type response: ``GetAllFeatureIDsResponse``

        Assert feature records information that raises an error
        """
        visited_feature_ids = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Parse feature records payload from GetAllFeatureIDsResponse")
        # --------------------------------------------------------------------------------------------------------------
        feature_records_payload = GetAllFeatureIDsResponsePayloadMixin.fromHexList(HexList(response.vlp_payload))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check feature count and feature record size in GetAllFeatureIDsResponse")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(HexList(self.config.F_FeatureCount), feature_records_payload.feature_records_count,
                         f"Feature count in GetAllFeatureIDsResponse is not as expected")
        self.assertEqual(HexList(self.config.F_FeatureRecordSize), feature_records_payload.feature_records_size,
                         f"Feature record size in GetAllFeatureIDsResponse is not as expected")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Check each feature record in GetAllFeatureIDsResponse")
        # --------------------------------------------------------------------------------------------------------------
        for feature_idx in range(1, to_int(feature_records_payload.feature_records_count) + 1):
            feature_id = getattr(feature_records_payload, f"feature_id_{feature_idx}")
            # Check feature id is not duplicated
            self.assertTrue(feature_id not in visited_feature_ids, f"Feature id 0x{feature_id} is duplicated in "
                                                                   f"GetAllFeatureIDsResponse fields")
            visited_feature_ids.append(feature_id)

            feature_config = eval(f"self.f.PRODUCT.FEATURES.VLP.{self.VLP_FEATURES_SUBSYSTEM_NAME[to_int(feature_id)]}")

            # Check feature version
            feature_version = self.config_manager.get_feature_version(feature_config)
            self.assertEqual(Numeral(feature_version),
                             Numeral(getattr(feature_records_payload, f"feature_version_{feature_idx}")),
                             msg=f"Feature version for {feature_id} in GetAllFeatureIDsResponse is not as expected")

            # Check feature max memory
            self.assertEqual(Numeral(feature_config.F_FeatureMaxMemory),
                             Numeral(getattr(feature_records_payload, f"feature_max_memory_{feature_idx}")),
                             msg=f"Feature max memory for {feature_id} in GetAllFeatureIDsResponse is not as expected")
        # end for
    # end def check_feature_records

    def check_feature_record(self, response):
        """
        Check the get feature id response parameters

        :param response: The get feature id response
        :type response: ``GetFeatureIDResponse``

        Assert get feature id response parameters that raises an error
        """
        feature_id = response.feature_id
        feature_config = eval(f"self.f.PRODUCT.FEATURES.VLP.{self.VLP_FEATURES_SUBSYSTEM_NAME[to_int(feature_id)]}")

        # check feature version
        feature_version = self.config_manager.get_feature_version(feature_config)
        self.assertEqual(Numeral(feature_version), Numeral(response.feature_version),
                         msg=f"Feature version for {feature_id} in GetAllFeatureIDsResponse is not as expected")

        # check feature max memory
        self.assertEqual(Numeral(feature_config.F_FeatureMaxMemory),
                         Numeral(response.feature_max_memory),
                         msg=f"Feature max memory for {feature_id} in GetAllFeatureIDsResponse is not as expected")
    # end def check_feature_record
# end class VLPFeatureSetTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
