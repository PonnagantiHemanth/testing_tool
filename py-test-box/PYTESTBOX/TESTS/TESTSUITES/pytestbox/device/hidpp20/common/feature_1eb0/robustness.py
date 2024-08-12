#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1eb0.robustness
:brief: HID++ 2.0 ``TdeAccessToNvm`` robustness test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/07/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvm
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.tdeaccesstonvmutils import TdeAccessToNvmTestUtils
from pytestbox.device.hidpp20.common.feature_1eb0.tdeaccesstonvm import TdeAccessToNvmTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TdeAccessToNvmRobustnessTestCase(TdeAccessToNvmTestCase):
    """
    Validate ``TdeAccessToNvm`` robustness test cases
    """

    @features("Feature1EB0")
    @level("Robustness")
    def test_padding(self):
        """
        Validates writing data to few buffer with remaining padding
        """
        number_of_bytes = 0x05
        payload = RandHexList(TdeAccessToNvm.MAX_PACKET_SIZE)
        params = self.get_parameters(number_of_bytes=number_of_bytes,
                                     write_dict=self.get_write_parameters(payload=payload),
                                     read_dict=self.get_read_parameters())

        self.process_api(params)

        self.testCaseChecked("ROB_1EB0_0001", _AUTHOR)
    # end def test_padding

    @features("Feature1EB0")
    @level("Robustness")
    def test_nvs_chunk_content_verification(self):
        """
        Verify TDE NVS chunk content
        """
        payload = RandHexList(TdeAccessToNvm.MAX_PACKET_SIZE)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send TdeWriteData (sp = 0) (nb = 0x0E) (payload = {payload})")
        # --------------------------------------------------------------------------------------------------------------
        TdeAccessToNvmTestUtils.HIDppHelper.tde_write_data(
            test_case=self,
            starting_position=HexList(self.starting_position),
            number_of_bytes_to_read_or_write=HexList(self.tde_buffer_size),
            data_byte_0=HexList(payload[0]),
            data_byte_1=HexList(payload[1]),
            data_byte_2=HexList(payload[2]),
            data_byte_3=HexList(payload[3]),
            data_byte_4=HexList(payload[4]),
            data_byte_5=HexList(payload[5]),
            data_byte_6=HexList(payload[6]),
            data_byte_7=HexList(payload[7]),
            data_byte_8=HexList(payload[8]),
            data_byte_9=HexList(payload[9]),
            data_byte_10=HexList(payload[10]),
            data_byte_11=HexList(payload[11]),
            data_byte_12=HexList(payload[12]),
            data_byte_13=HexList(payload[13])
        )
        TdeAccessToNvmTestUtils.NvsHelper.validate_tde_chunk(self)

        self.testCaseChecked("ROB_1EB0_0002", _AUTHOR)
    # end def test_nvs_chunk_content_verification
# end class TdeAccessToNvmRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
