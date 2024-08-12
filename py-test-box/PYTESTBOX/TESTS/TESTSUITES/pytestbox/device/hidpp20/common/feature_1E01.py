#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1E01
:brief: Validate HID++ 2.0 Manage deactivatable features
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/10/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.common.managedeactivatablefeatures import ManageDeactivatableFeatures
from pyhid.hidpp.features.common.managedeactivatablefeatures import ManageDeactivatableFeaturesFactory
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.managedeactivatablefeaturesutils import ManageDeactivatableFeaturesTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ManageDeactivatableFeaturesTestCase(DeviceBaseTestCase):
    """
    Validates Manage deactivatable features TestCases in Application mode
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.force_tde_counter_in_tear_down = False

        super().setUp()

        # Force TDE counters to max values
        DeviceBaseTestUtils.NvsHelper.force_tde_counters(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Get feature 0x1E01 index')
        # ---------------------------------------------------------------------------
        self.feature_1e01_index = self.updateFeatureMapping(feature_id=ManageDeactivatableFeatures.FEATURE_ID)
        self.feature_1e01 = ManageDeactivatableFeaturesFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES))

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Enable Hidden Features')
        # ---------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Setup End')
        # ---------------------------------------------------------------------------
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            # ---------------------------------------------------------------------------
            self.logTitle2('Start Tear Down')
            # ---------------------------------------------------------------------------
            if self.force_tde_counter_in_tear_down:
                DeviceBaseTestUtils.NvsHelper.force_tde_counters(self)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try
        super().tearDown()
    # end def tearDown

    def _test_set_counter(self, manuf_hidpp=None, compl_hidpp=None, gothard=None, exp_manuf_hidpp=None,
                          exp_compl_hidpp=None, exp_gothard=None, check_nvs=True, check_get=True):
        """
        Validate setCounter

        :param manuf_hidpp: Manufacturing counter value
        :type manuf_hidpp: ``int``
        """
        log_step = 1
        log_check = 1
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Step {log_step}: Send SetCounters request ')
        # ----------------------------------------------------------------------------
        log_step += 1
        set_counters_resp = ManageDeactivatableFeaturesTestUtils.HIDppHelper.set_counters(
            self,
            self.deviceIndex,
            self.feature_1e01,
            self.feature_1e01_index,
            manuf_hidpp_counter=manuf_hidpp if manuf_hidpp is not None else None,
            compl_hidpp_counter=compl_hidpp if compl_hidpp is not None else None,
            gothard_counter=gothard if gothard is not None else None
        )

        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Check {log_check}: Check response fields')
        # ----------------------------------------------------------------------------
        log_check += 1
        ManageDeactivatableFeaturesTestUtils.MessageChecker.check_fields(
            self, set_counters_resp, self.feature_1e01.set_counters_response_cls, {})

        expected_manuf = exp_manuf_hidpp if exp_manuf_hidpp is not None else None
        expected_compl = exp_compl_hidpp if exp_compl_hidpp is not None else None
        expected_gothard = exp_gothard if exp_gothard is not None else None
        if check_nvs:
            # ----------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Check NVS fields')
            # ----------------------------------------------------------------------------
            log_check += 1
            ManageDeactivatableFeaturesTestUtils.NvsHelper.check_counters(
                self,
                expected_manuf_counter=expected_manuf,
                expected_compl_counter=expected_compl,
                expected_gothard_counter=expected_gothard
            )

        if check_get:
            # ----------------------------------------------------------------------------
            self.logTitle2(f'Test Step {log_step}: Send GetCounters request')
            # ----------------------------------------------------------------------------
            log_step += 1
            get_counters_req = self.feature_1e01.get_counters_cls(self.deviceIndex, self.feature_1e01_index)
            get_counters_resp = self.send_report_wait_response(
                report=get_counters_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1e01.get_counters_response_cls)

            # ----------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Check response fields')
            # ----------------------------------------------------------------------------
            log_check += 1
            ManageDeactivatableFeaturesTestUtils.GetCountersResponseChecker.check_counters(
                self,
                get_counters_resp,
                self.feature_1e01.get_counters_response_cls,
                expected_manuf_counter=expected_manuf,
                expected_compl_counter=expected_compl,
                expected_gothard_counter=expected_gothard
            )
    # end def _test_set_counter

    def _test_set_counter_range(self, values_range, expected_manuf_hidpp_range=None, expected_compl_hidpp_range=None,
                                expected_gothard_range=None):
        """
        Validate setCounter range

        :param values_range: Values to test
        :type values_range: ``list``
        :param expected_manuf_hidpp_range: Expected values for manufacturing counter
        :type expected_manuf_hidpp_range: ``list``
        :param expected_compl_hidpp_range: Expected values for compliance counter
        :type expected_compl_hidpp_range: ``list``
        :param expected_gothard_range: Expected values for Gothard counter
        :type expected_gothard_range: ``list``
        """
        for idx, counter_value in enumerate(values_range):
            self._test_set_counter(
                manuf_hidpp=counter_value if expected_manuf_hidpp_range is not None else None,
                compl_hidpp=counter_value if expected_compl_hidpp_range is not None else None,
                gothard=counter_value if expected_gothard_range is not None else None,
                exp_manuf_hidpp=expected_manuf_hidpp_range[idx] if expected_manuf_hidpp_range is not None else None,
                exp_compl_hidpp=expected_compl_hidpp_range[idx] if expected_compl_hidpp_range is not None else None,
                exp_gothard=expected_gothard_range[idx] if expected_gothard_range is not None else None
            )
        # end for
    # end def _test_set_counter_range
# end class ManageDeactivatableFeaturesTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
