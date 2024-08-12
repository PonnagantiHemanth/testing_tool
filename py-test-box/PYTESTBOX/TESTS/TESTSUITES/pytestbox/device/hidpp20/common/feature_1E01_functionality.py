#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1E01_functionality
:brief: HID++ 2.0 Manage deactivatable features functional test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/10/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.managedeactivatablefeaturesutils import ManageDeactivatableFeaturesTestUtils
from pytestbox.device.hidpp20.common.feature_1E01 import ManageDeactivatableFeaturesTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ManageDeactivatableFeaturesFunctionalityTestCase(ManageDeactivatableFeaturesTestCase):
    """
    Validates Manage deactivatable features functionality TestCases in Application mode
    """
    @features('Feature1E01')
    @level('Interface')
    def test_get_counters_api(self):
        """
        Validates GetCounters normal processing
        """
        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetCounters request')
        # ----------------------------------------------------------------------------
        get_counters_req = self.feature_1e01.get_counters_cls(self.deviceIndex, self.feature_1e01_index)

        get_counters_resp = self.send_report_wait_response(
            report=get_counters_req,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1e01.get_counters_response_cls)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check GetCounters response fields')
        # ----------------------------------------------------------------------------
        ManageDeactivatableFeaturesTestUtils.GetCountersResponseChecker.check_fields(
            self, get_counters_resp, self.feature_1e01.get_counters_response_cls)

        self.testCaseChecked("FNT_1E01_0001")
    # end def test_get_counters_api

    @features('Feature1E01')
    @level('Interface')
    def test_set_counters_api(self):
        """
        Validates SetCounters normal processing
        """
        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetCounters request default values')
        # ----------------------------------------------------------------------------
        set_counters_req = self.feature_1e01.set_counters_cls(
            self.deviceIndex,
            self.feature_1e01_index,
            gothard=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportGothardCounter,
            compl_hidpp=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportComplianceCounter,
            manuf_hidpp=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportManufacturingCounter,
            manuf_hidpp_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter,
            compl_hidpp_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter,
            gothard_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter
        )

        set_counters_resp = self.send_report_wait_response(
            report=set_counters_req,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1e01.set_counters_response_cls)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check SetCounters response fields')
        # ----------------------------------------------------------------------------
        ManageDeactivatableFeaturesTestUtils.MessageChecker.check_fields(
            self, set_counters_resp, self.feature_1e01.set_counters_response_cls, {})

        self.testCaseChecked("FNT_1E01_0002")
    # end def test_set_counters_api

    @features('Feature1E01')
    @level('Interface')
    def test_get_react_info_api(self):
        """
        Validates getReactInfo normal processing
        """
        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send getReactInfo request')
        # ----------------------------------------------------------------------------
        get_react_info_req = self.feature_1e01.get_react_info_cls(self.deviceIndex, self.feature_1e01_index)

        get_react_info_resp = self.send_report_wait_response(
            report=get_react_info_req,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1e01.get_react_info_response_cls)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check response fields')
        # ----------------------------------------------------------------------------
        ManageDeactivatableFeaturesTestUtils.GetReactInfoResponseChecker.check_fields(
            self, get_react_info_resp, self.feature_1e01.get_react_info_response_cls)

        self.testCaseChecked("FNT_1E01_0003")
    # end def test_get_react_info_api

    @features('Feature1E01')
    @level('Business')
    def test_business_write_read(self):
        """
        Validate Business Case Write/Read business case with a sequence of SetCounter request followed by GetCounter
        request
        """
        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetCounters request default values')
        # ----------------------------------------------------------------------------
        set_counters_req = self.feature_1e01.set_counters_cls(
            self.deviceIndex,
            self.feature_1e01_index,
            gothard=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportGothardCounter,
            compl_hidpp=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportComplianceCounter,
            manuf_hidpp=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportManufacturingCounter,
            manuf_hidpp_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter,
            compl_hidpp_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter,
            gothard_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter
        )

        set_counters_resp = self.send_report_wait_response(
            report=set_counters_req,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1e01.set_counters_response_cls)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check response fields')
        # ----------------------------------------------------------------------------
        ManageDeactivatableFeaturesTestUtils.MessageChecker.check_fields(
            self, set_counters_resp, self.feature_1e01.set_counters_response_cls, {})

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Read NVS')
        # ----------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        conn_counters_chunk_list = self.memory_manager.get_chunks_by_name('NVS_X1E01_CONN_CNTR_ID')

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check NVS fields')
        # ----------------------------------------------------------------------------
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportManufacturingCounter:
            expected_manuf_counter = \
                self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter
        else:
            expected_manuf_counter = 0x00
        # end if

        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportComplianceCounter:
            expected_compl_counter = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter
        else:
            expected_compl_counter = 0x00
        # end if

        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportGothardCounter:
            expected_gothard_counter = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter
        else:
            expected_gothard_counter = 0x00
        # end if

        self.assertEqual(obtained=int(Numeral(conn_counters_chunk_list[-1].disable_manufacturing_registers_counter)),
                         expected=int(Numeral(expected_manuf_counter)),
                         msg="Manufacturing counter value in NVS should be as expected")
        self.assertEqual(obtained=int(Numeral(conn_counters_chunk_list[-1].disable_compliance_registers_counter)),
                         expected=int(Numeral(expected_compl_counter)),
                         msg="Compliance counter value in NVS should be as expected")
        self.assertEqual(obtained=int(Numeral(conn_counters_chunk_list[-1].disable_gothard_counter)),
                         expected=int(Numeral(expected_gothard_counter)),
                         msg="Gothard counter value in NVS should be as expected")

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send GetCounters request')
        # ----------------------------------------------------------------------------
        get_counters_req = self.feature_1e01.get_counters_cls(self.deviceIndex, self.feature_1e01_index)

        get_counters_resp = self.send_report_wait_response(
            report=get_counters_req,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1e01.get_counters_response_cls)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Check response fields')
        # ----------------------------------------------------------------------------
        ManageDeactivatableFeaturesTestUtils.GetCountersResponseChecker.check_counters(
            self,
            get_counters_resp,
            self.feature_1e01.get_counters_response_cls,
            expected_manuf_counter,
            expected_compl_counter,
            expected_gothard_counter
        )

        self.testCaseChecked("FNT_1E01_0004")
    # end def test_business_write_read

    @features('Feature1E01')
    @level('Business')
    def test_tde_business(self):
        """
        Check TDE Business case :
        check 11 <Id> <Idx> 1<Sw> 80 FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00 is accepted
        Note: this (forward-compatible) hexadecimal command will set all supported counters (up to 7
        counters) to their maximum values (which may be different from 255)
        """
        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetCounters TDE request')
        # ----------------------------------------------------------------------------
        set_counters_req = self.feature_1e01.set_counters_cls(
            self.deviceIndex,
            self.feature_1e01_index,
            gothard=False,
            compl_hidpp=False,
            manuf_hidpp=False,
            all_bit=True,
            manuf_hidpp_counter=0xFF,
            compl_hidpp_counter=0xFF,
            gothard_counter=0xFF,
        )
        set_counters_req.padding = HexList("FFFFFFFF0000000000000000")

        set_counters_resp = self.send_report_wait_response(
            report=set_counters_req,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1e01.set_counters_response_cls)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check response fields')
        # ----------------------------------------------------------------------------
        ManageDeactivatableFeaturesTestUtils.MessageChecker.check_fields(
            self, set_counters_resp, self.feature_1e01.set_counters_response_cls, {})

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Read NVS')
        # ----------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        conn_counters_chunk_list = self.memory_manager.get_chunks_by_name('NVS_X1E01_CONN_CNTR_ID')

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check NVS fields')
        # ----------------------------------------------------------------------------
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportManufacturingCounter:
            expected_manuf_counter = \
                self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter
        else:
            expected_manuf_counter = 0x00
        # end if

        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportComplianceCounter:
            expected_compl_counter = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter
        else:
            expected_compl_counter = 0x00
        # end if

        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportGothardCounter:
            expected_gothard_counter = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter
        else:
            expected_gothard_counter = 0x00
        # end if

        self.assertEqual(obtained=int(Numeral(conn_counters_chunk_list[-1].disable_manufacturing_registers_counter)),
                         expected=int(Numeral(expected_manuf_counter)),
                         msg="Manufacturing counter value in NVS should be as expected")
        self.assertEqual(obtained=int(Numeral(conn_counters_chunk_list[-1].disable_compliance_registers_counter)),
                         expected=int(Numeral(expected_compl_counter)),
                         msg="Compliance counter value in NVS should be as expected")
        self.assertEqual(obtained=int(Numeral(conn_counters_chunk_list[-1].disable_gothard_counter)),
                         expected=int(Numeral(expected_gothard_counter)),
                         msg="Gothard counter value in NVS should be as expected")

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send GetCounters request')
        # ----------------------------------------------------------------------------
        get_counters_req = self.feature_1e01.get_counters_cls(self.deviceIndex, self.feature_1e01_index)

        get_counters_resp = self.send_report_wait_response(
            report=get_counters_req,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1e01.get_counters_response_cls)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Check response fields')
        # ----------------------------------------------------------------------------
        ManageDeactivatableFeaturesTestUtils.GetCountersResponseChecker.check_counters(
            self,
            get_counters_resp,
            self.feature_1e01.get_counters_response_cls,
            expected_manuf_counter,
            expected_compl_counter,
            expected_gothard_counter
        )

        self.testCaseChecked("FNT_1E01_0018")
    # end def test_tde_business

    @features('Feature1E01')
    @features('Feature1E01WithManufacturingCounter')
    @level('Interface')
    def test_set_counter_valid_range_manuf_hidpp(self):
        """
        Validate manufHidppCounter valid range
        """
        valid_range = compute_inf_values(
                self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter, is_equal=True)
        if 0 in valid_range:
            valid_range[valid_range.index(0)] = 1
        # end if
        self._test_set_counter_range(values_range=valid_range, expected_manuf_hidpp_range=valid_range)
        self.testCaseChecked("FNT_1E01_0005#1")
    # end def test_set_counter_valid_range_manuf_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithComplianceCounter')
    @level('Interface')
    def test_set_counter_valid_range_compl_hidpp(self):
        """
        Validate complHidppCounter valid range
        """
        valid_range = compute_inf_values(
            self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter, is_equal=True)
        if 0 in valid_range:
            valid_range[valid_range.index(0)] = 1
        # end if
        self._test_set_counter_range(values_range=valid_range, expected_compl_hidpp_range=valid_range)
        self.testCaseChecked("FNT_1E01_0005#2")
    # end def test_set_counter_valid_range_compl_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithGothardCounter')
    @level('Interface')
    def test_set_counter_valid_range_gothard(self):
        """
        Validate gothardCounter valid range
        """
        valid_range = compute_inf_values(
            self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter, is_equal=True)
        if 0 in valid_range:
            valid_range[valid_range.index(0)] = 1
        # end if
        self._test_set_counter_range(values_range=valid_range, expected_gothard_range=valid_range)
        self.testCaseChecked("FNT_1E01_0005#3")
    # end def test_set_counter_valid_range_gothard

    def _test_set_counter_compared_to_memory(self, comparison, manuf_hidpp=False, compl_hidpp=False, gothard=False):
        """
        Check setCounters is working when sending a counter value smaller, equal or greater than the one in memory

        :param comparison: Comparison type
        :type comparison: ``str``
        :param manuf_hidpp: Enable test for manufacturing counter
        :type manuf_hidpp: ``bool``
        :param compl_hidpp: Enable test for compliance counter
        :type compl_hidpp: ``bool``
        :param gothard: Enable test for Gothard counter
        :type gothard: ``bool``
        """
        assert comparison in ['<', '=', '>']

        class DynamicParameters:
            """
            Handle parameters which depend on the comparison type
            """
            def __init__(self, text, new_manuf_hidpp_counter, new_compl_hidpp_counter, new_gothard_counter):
                self.text = text
                self.new_manuf_hidpp_counter = new_manuf_hidpp_counter
                self.new_compl_hidpp_counter = new_compl_hidpp_counter
                self.new_gothard_counter = new_gothard_counter
            # end def __init__
        # end def DynamicParameters

        init_val_manuf_hidpp = \
            self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter // 2
        init_val_compl_hidpp = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter // 2
        init_val_gothard = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter // 2

        smaller_than_comp = DynamicParameters(
            text='smaller than',
            new_manuf_hidpp_counter=init_val_manuf_hidpp - 2 if manuf_hidpp else None,
            new_compl_hidpp_counter=init_val_compl_hidpp - 2 if compl_hidpp else None,
            new_gothard_counter=init_val_gothard - 2 if gothard else None
        )

        equal_to_comp = DynamicParameters(
            text='equal to',
            new_manuf_hidpp_counter=init_val_manuf_hidpp - 1 if manuf_hidpp else None,
            new_compl_hidpp_counter=init_val_compl_hidpp - 1 if compl_hidpp else None,
            new_gothard_counter=init_val_gothard - 1 if gothard else None
        )

        greater_than_comp = DynamicParameters(
            text='greater than',
            new_manuf_hidpp_counter=init_val_manuf_hidpp + 1 if manuf_hidpp else None,
            new_compl_hidpp_counter=init_val_compl_hidpp + 1 if compl_hidpp else None,
            new_gothard_counter=init_val_gothard + 1 if gothard else None
        )

        comp_map = {
            '<': smaller_than_comp,
            '=': equal_to_comp,
            '>': greater_than_comp
        }

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Set initial value in NVS')
        # ----------------------------------------------------------------------------
        ManageDeactivatableFeaturesTestUtils.NvsHelper.set_counters(
            self,
            manuf_hidpp_counter=init_val_manuf_hidpp if manuf_hidpp else None,
            compl_hidpp_counter=init_val_compl_hidpp if compl_hidpp else None,
            gothard_counter=init_val_gothard if gothard else None
        )

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check counters values in NVS')
        # ----------------------------------------------------------------------------
        # Counters should already be decremented by 1 because loading NVS triggers a reset
        ManageDeactivatableFeaturesTestUtils.NvsHelper.check_counters(
            self,
            expected_manuf_counter=init_val_manuf_hidpp - 1 if manuf_hidpp else None,
            expected_compl_counter=init_val_compl_hidpp - 1 if compl_hidpp else None,
            expected_gothard_counter=init_val_gothard - 1 if gothard else None
        )

        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Send setCounters with counter value {comp_map[comparison].text} the one in '
                       f'memory')
        # ----------------------------------------------------------------------------
        # Hidden features need to be re-enable after reset
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Set Counter')
        # ----------------------------------------------------------------------------
        self._test_set_counter(
            manuf_hidpp=comp_map[comparison].new_manuf_hidpp_counter,
            compl_hidpp=comp_map[comparison].new_compl_hidpp_counter,
            gothard=comp_map[comparison].new_gothard_counter,
            exp_manuf_hidpp=comp_map[comparison].new_manuf_hidpp_counter,
            exp_compl_hidpp=comp_map[comparison].new_compl_hidpp_counter,
            exp_gothard=comp_map[comparison].new_gothard_counter
        )
    # end def _test_set_counter_compared_to_memory

    @features('Feature1E01')
    @features('Feature1E01WithManufacturingCounter')
    @level('Functionality')
    def test_set_counter_equal_to_memory_manuf_hidpp(self):
        """
        Check setCounters is working when sending a manufacturing counter value equal to the one in memory.
        Check no chunk is added in NVS.
        """
        self._test_set_counter_compared_to_memory(comparison='=', manuf_hidpp=True)
        self.testCaseChecked("FNT_1E01_0007#1")
    # end def test_set_counter_equal_to_memory_manuf_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithComplianceCounter')
    @level('Functionality')
    def test_set_counter_equal_to_memory_compl_hidpp(self):
        """
        Check setCounters is working when sending a compliance counter value equal to the one in memory.
        Check no chunk is added in NVS.
        """
        self._test_set_counter_compared_to_memory(comparison='=', compl_hidpp=True)
        self.testCaseChecked("FNT_1E01_0007#2")
    # end def test_set_counter_equal_to_memory_compl_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithGothardCounter')
    @level('Functionality')
    def test_set_counter_equal_to_memory_gothard(self):
        """
        Check setCounters is working when sending a Gothard counter value equal to the one in memory.
        Check no chunk is added in NVS.
        """
        self._test_set_counter_compared_to_memory(comparison='=', gothard=True)
        self.testCaseChecked("FNT_1E01_0007#3")
    # end def test_set_counter_equal_to_memory_gothard

    @features('Feature1E01')
    @features('Feature1E01WithManufacturingCounter')
    @level('Functionality')
    def test_set_counter_greater_than_memory_manuf_hidpp(self):
        """
        Check setCounters is working when sending a manufacturing counter value greater than the one in memory
        """
        self._test_set_counter_compared_to_memory(comparison='>', manuf_hidpp=True)
        self.testCaseChecked("FNT_1E01_0008#1")
    # end def test_set_counter_greater_than_memory_manuf_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithComplianceCounter')
    @level('Functionality')
    def test_set_counter_greater_than_memory_compl_hidpp(self):
        """
        Check setCounters is working when sending a compliance counter value greater than the one in memory
        """
        self._test_set_counter_compared_to_memory(comparison='>', compl_hidpp=True)
        self.testCaseChecked("FNT_1E01_0008#2")
    # end def test_set_counter_greater_than_memory_compl_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithGothardCounter')
    @level('Functionality')
    def test_set_counter_greater_than_memory_gothard(self):
        """
        Check setCounters is working when sending a Gothard counter value greater than the one in memory
        """
        self._test_set_counter_compared_to_memory(comparison='>', gothard=True)
        self.testCaseChecked("FNT_1E01_0008#3")
    # end def test_set_counter_greater_than_memory_gothard

    @features('Feature1E01')
    @features('Feature1E01WithManufacturingCounter')
    @level('Functionality')
    def test_set_counter_smaller_than_memory_manuf_hidpp(self):
        """
        Check setCounters is working when sending a manufacturing counter value smaller than the one in memory
        """
        self._test_set_counter_compared_to_memory(comparison='<', manuf_hidpp=True)
        self.testCaseChecked("FNT_1E01_0009#1")
    # end def test_set_counter_smaller_than_memory_manuf_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithComplianceCounter')
    @level('Functionality')
    def test_set_counter_smaller_than_memory_compl_hidpp(self):
        """
        Check setCounters is working when sending a compliance counter value smaller than the one in memory
        """
        self._test_set_counter_compared_to_memory(comparison='<', compl_hidpp=True)
        self.testCaseChecked("FNT_1E01_0009#2")
    # end def test_set_counter_smaller_than_memory_compl_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithGothardCounter')
    @level('Functionality')
    def test_set_counter_smaller_than_memory_gothard(self):
        """
        Check setCounters is working when sending a Gothard counter value smaller than the one in memory
        """
        self._test_set_counter_compared_to_memory(comparison='<', gothard=True)
        self.testCaseChecked("FNT_1E01_0009#3")
    # end def test_set_counter_smaller_than_memory_gothard

    @features('Feature1E01')
    @features('Feature1E01WithManufacturingCounter')
    @level('Functionality')
    def test_set_counter_zero_manuf_hidpp(self):
        """
        Check setCounters is working when sending a manufacturing counter value equal to 0
        """
        self.force_tde_counter_in_tear_down = True
        self._test_set_counter(manuf_hidpp=0, exp_manuf_hidpp=0)
        self.testCaseChecked("FNT_1E01_0011#1")
    # end def test_set_counter_zero_manuf_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithComplianceCounter')
    @level('Functionality')
    def test_set_counter_zero_compl_hidpp(self):
        """
        Check setCounters is working when sending a compliance counter value equal to 0
        """
        self.force_tde_counter_in_tear_down = True
        self._test_set_counter(compl_hidpp=0, exp_compl_hidpp=0)
        self.testCaseChecked("FNT_1E01_0011#2")
    # end def test_set_counter_zero_compl_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithGothardCounter')
    @level('Functionality')
    def test_set_counter_zero_gothard(self):
        """
        Check setCounters is working when sending a compliance counter value equal to 0
        """
        self.force_tde_counter_in_tear_down = True
        self._test_set_counter(gothard=0, exp_gothard=0)
        self.testCaseChecked("FNT_1E01_0011#3")
    # end def test_set_counter_zero_gothard
# end class ManageDeactivatableFeaturesFunctionalityTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
