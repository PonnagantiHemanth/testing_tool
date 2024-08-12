#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp20.common.feature_00D0_business
:brief: Validates Receiver HID++ 2.0 Common feature 0x00D0
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.mcu.nrf52.blenvschunks import ReceiverBleBondInfoIdV0
from pylibrary.tools.numeral import to_int
from pylibrary.tools.nvsparser import MODE
from pytestbox.base.dfuprocessing import ReceiverDfuTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.hidpp20.common.feature_00D0_business import SharedDfuTestCaseBusiness


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestCaseBusiness(SharedDfuTestCaseBusiness, ReceiverDfuTestCase):
    """
    Validate DFU Business TestCases
    """

    @features('Feature00D0')
    @features('BLEProProtocol')
    @level('Business')
    @services('Debugger')
    def test_no_re_enumeration_after_a_DFU_without_services_change(self):
        """
        Validate the receiver does NOT force device services re-enumeration after any DFU if the services structure
        was unchanged.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the NVS and keep the initial bond info chunk history')
        # --------------------------------------------------------------------------------------------------------------
        bond_info_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_BLE_BOND_INFO_ID_0')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Complete the DFU of the receiver application')
        # --------------------------------------------------------------------------------------------------------------
        self.generic_complete_dfu_business()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify the bond info chunks are unchanged')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        new_bond_info_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(
            chunk_id='NVS_BLE_BOND_INFO_ID_0', mode=MODE.RECEIVER)
        self.assertEqual(expected=len(bond_info_chunk_history),
                         obtained=len(new_bond_info_chunk_history),
                         msg='The number of DFU chunk in history is not the expected one')

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is not set')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.DISABLED,
                         obtained=to_int(new_bond_info_chunk_history[-1].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        self.testCaseChecked("FNT_00D0_0062")
    # end def test_no_re_enumeration_after_a_DFU_without_services_change

# end class DfuTestCaseBusiness

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
