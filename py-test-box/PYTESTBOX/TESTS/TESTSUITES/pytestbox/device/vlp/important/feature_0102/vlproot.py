#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pytestbox.device.hidpp20.common.feature_0011.propertyaccess
:brief: Validate HID++ 2.0 ``PropertyAccess`` feature
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/20
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.systems import AbstractSubSystem
from pyhid.vlp.features.important.vlproot import VLPFeatureIniConfigInfo
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.vlprootutils import VLPRootTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class VLPRootTestCase(DeviceBaseTestCase):
    """
    Validate ``VLPRootTestCase`` TestCases in Application mode
    """

    def setUp(self):
        """
                Handle test prerequisites.
                """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0102 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0102_index, self.feature_0102, _, _ = VLPRootTestUtils.HIDppHelper.get_vlp_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT
    # end def setUp

    def _retrieve_vlp_features_info(self):
        """
        Retrieve all VLP 1.0 information [feature_category, feature_name, feature_version] to a list

        :return: raw hidpp features list
        :rtype: ``list[FeatureIniConfigInfo]``
        """
        raw_feature_info_list = []
        for f_category in self.f.PRODUCT.FEATURES.VLP:
            if isinstance(getattr(self.f.PRODUCT.FEATURES.VLP, f_category), AbstractSubSystem) is False:
                continue
            # end if
            for f_name in getattr(self.f.PRODUCT.FEATURES.VLP, f_category):
                # Version is 0 by default if the feature is enabled, otherwise version is None
                if isinstance(eval(f'self.f.PRODUCT.FEATURES.VLP.{f_category}.{f_name}'), AbstractSubSystem) is False:
                    continue
                elif eval(f'self.f.PRODUCT.FEATURES.VLP.{f_category}.{f_name}.F_Enabled'):
                    f_version = self.config_manager.get_feature_version(
                        eval(f'self.f.PRODUCT.FEATURES.VLP.{f_category}.{f_name}'))
                    f_version = f_version if f_version else 0
                else:
                    f_version = None
                # end if
                raw_feature_info_list.append(VLPFeatureIniConfigInfo(category=f_category, name=f_name, version=f_version))
            # end for
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "raw_feature_info_list:")
        # --------------------------------------------------------------------------------------------------------------
        for raw_feature_info in raw_feature_info_list:
            LogHelper.log_info(self, f"{raw_feature_info}")
        # end for

        return raw_feature_info_list
    # end def _retrieve_vlp_features_info

    def _revise_vlp_feature_info(self, raw_feature_info_list):
        """
        Revise raw_feature_info_list which includes
        - Filter disabled features
        - Initialize class name and class import path

        :param raw_feature_info_list: raw hidpp features list
        :type raw_feature_info_list: ``list[FeatureIniConfigInfo]``

        :return: revised vlp features list
        :rtype: ``list[FeatureIniConfigInfo]``
        """
        revised_vlp_feature_info_list = []
        for raw_vlp_feature_info in raw_feature_info_list:
            if raw_vlp_feature_info.version is not None:
                raw_vlp_feature_info.get_class_name()
                raw_vlp_feature_info.get_class_import_path()
                revised_vlp_feature_info_list.append(raw_vlp_feature_info)
            # end if
        # end for

        LogHelper.log_info(self, "revised_vlp_feature_info_list:")
        for vlp_feature_info in revised_vlp_feature_info_list:
            LogHelper.log_info(self, f"{vlp_feature_info}")
        # end for

        return revised_vlp_feature_info_list
    # end def _revise_vlp_feature_info
# end class VLPRootTestCase