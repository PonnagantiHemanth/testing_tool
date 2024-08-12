#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b10.functionality
:brief: HID++ 2.0 ``ControlList`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.controllist import GetControlListResponse
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pylibrary.tools.numeral import to_int
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.layoututils import LayoutTestUtils
from pytestbox.device.hidpp20.common.feature_1b10.controllist import ControlListTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ControlListFunctionalityTestCase(ControlListTestCase):
    """
    Validate ``ControlList`` functionality test cases
    """

    @features("Feature1B10")
    @level("Functionality")
    def test_no_duplicated_cid_in_control_list(self):
        """
        Verify there is no duplicated key in the control list
        """
        cid_list = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over offset in range(0, {self.config.F_Count}, 8)")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range(0, self.config.F_Count, GetControlListResponse.NUM_OF_CID_PER_PACKET):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send getControlList request with offset={offset} to collect the partial cid list")
            # ----------------------------------------------------------------------------------------------------------
            response = ControlListTestUtils.HIDppHelper.get_control_list(
                test_case=self,
                offset=offset)
            cid_list += [to_int(getattr(response, f'cid_{index}'))
                         for index in range(GetControlListResponse.NUM_OF_CID_PER_PACKET)]
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check there is no any duplicated cid in the {cid_list}")
        # --------------------------------------------------------------------------------------------------------------
        duplicated_cid = [cid for cid in set(cid_list) if cid_list.count(cid) > 1 and cid != 0]
        self.assertEqual(expected=0,
                         obtained=len(duplicated_cid),
                         msg=f"There are some duplicated CIDs found in the CID list: {duplicated_cid}")

        self.testCaseChecked("FUN_1B10_0001", _AUTHOR)
    # end def test_no_duplicated_cid_in_control_list

    @features("Feature1B10")
    @level("Functionality")
    def test_cid_list_defined_all_physical_keys(self):
        """
        Verify all physical controls are defined in the CID list
        """
        # In firmware, there are only 3 different layouts defined in the code: ISO_104, ISO_105 and ISO_109.
        # We can cover all other countries layouts by switching to the following layouts.
        layouts = [KeyboardInternationalLayouts.LAYOUT.US, KeyboardInternationalLayouts.LAYOUT.UK,
                   KeyboardInternationalLayouts.LAYOUT.JAPANESE]
        self.post_requisite_reload_us_layout = True
        cid_list_from_device = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over layout in {layouts!s}")
        # --------------------------------------------------------------------------------------------------------------
        for layout in layouts:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Configure the Keyboard International Layout to {layout!s}")
            # ----------------------------------------------------------------------------------------------------------
            LayoutTestUtils.select_layout(self, layout=layout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get whole CID list from the device")
            # ----------------------------------------------------------------------------------------------------------
            cid_list_from_device += ControlListTestUtils.get_cid_list_from_device(test_case=self, force_refresh=True)
        # for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Concatenate CID list from key matrix of all physical layouts")
        # --------------------------------------------------------------------------------------------------------------
        cid_list_from_dut_layouts = set(ControlListTestUtils.get_cid_list_from_dut_layouts(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there is no difference between "
                                  f"the cid list returned by the device: {cid_list_from_device}, "
                                  f"and the one defined in the test settings: {set(cid_list_from_dut_layouts)}")
        # --------------------------------------------------------------------------------------------------------------
        difference = set(cid_list_from_dut_layouts).difference(cid_list_from_device)
        for cid_not_found_in_device in difference.copy():
            # The cid_list_from_dut_layouts are gotten from KEY_ID, and there are some control IDs are linking to the
            # same KEY_ID. So this procedure is going to remove the CID which is linking to a KEY_ID that already
            # represents another CID.
            if cid_not_found_in_device in ControlListTestUtils.get_cids_sharing_key_id():
                if len(set(ControlListTestUtils.get_cids_sharing_key_id_with_cid(
                        cid_not_found_in_device)).intersection(cid_list_from_device)) > 0:
                    difference.remove(cid_not_found_in_device)
                # end if
            # end if
        # end for
        self.assertEqual(expected=0,
                         obtained=len(difference),
                         msg=f"Some physical controls differ from the expected list: {difference}")

        self.testCaseChecked("FUN_1B10_0002", _AUTHOR)
    # end def test_cid_list_defined_all_physical_keys
# end class ControlListFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
