#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1eb0.functionality
:brief: HID++ 2.0 ``TdeAccessToNvm`` functionality test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/07/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.error import ErrorCodes
from pytestbox.device.hidpp20.common.feature_1eb0.tdeaccesstonvm import TdeAccessToNvmTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TdeAccessToNvmFunctionalityTestCase(TdeAccessToNvmTestCase):
    """
    Validate ``TdeAccessToNvm`` functionality test cases
    """
    @features("Feature1EB0")
    @level("Functionality")
    def test_write_data_to_all_buffer(self):
        """
        Validates writing data to all buffer
        """

        params = self.get_parameters(number_of_bytes=self.tde_buffer_size,
                                     write_dict=self.get_write_parameters(),
                                     read_dict=self.get_read_parameters())

        self.process_api(params)

        self.testCaseChecked("FUN_1EB0_0001", _AUTHOR)
    # end def test_write_data_to_all_buffer

    @features("Feature1EB0")
    @level("Functionality")
    def test_all_bits_are_writable(self):
        """
        Test all bits are writable

        TDE memory length is 64 bytes (Vary based on device).
        TDE data length is 14 bytes (Vary based on device).
        Write data from 0 to 13, 14 to 27, 28 to 41, 42 to 55 with data size 14.
        Write data from 56 to 63 with data size 8.
        """

        (q, r) = divmod(self.tde_max_size, self.tde_buffer_size)

        for i in range(q):
            starting_position = self.starting_position
            if starting_position is None:
                # data from 0 to 13, 14 to 27, 28 to 41, 42 to 55 with data size 14
                starting_position = (i * self.tde_buffer_size)
            # end if
            params = self.get_parameters(
                    starting_position=starting_position,
                    number_of_bytes=self.tde_buffer_size,
                    read_dict=self.get_read_parameters(),
                    write_dict=self.get_write_parameters())
            self.process_api(params)
        # end for

        if r > 0:
            starting_position = self.starting_position
            if starting_position is None:
                # data from 56 to 63 with data size 8
                starting_position = (q * self.tde_buffer_size)
            # end if
            params = self.get_parameters(
                    starting_position=starting_position,
                    number_of_bytes=r,
                    read_dict=self.get_read_parameters(),
                    write_dict=self.get_write_parameters())
            self.process_api(params)
        # end if

        self.testCaseChecked("FUN_1EB0_0002", _AUTHOR)

    # end def test_all_bits_are_writable

    @features("Feature1EB0")
    @level("Functionality")
    def test_tde_clear_data_normal_processing(self):
        """
        Validates TdeClearData normal processing
        """
        params = self.get_parameters(write_dict=self.get_write_parameters(),
                                     read_dict=self.get_read_parameters(err_code=ErrorCodes.HW_ERROR))
        params["clear_api"] = True
        self.process_api(params)

        self.testCaseChecked("FUN_1EB0_0003", _AUTHOR)
    # end def test_tde_clear_data_normal_processing

    @features("Feature1EB0")
    @features("Feature1802")
    @level("Functionality")
    def test_tde_data_available_after_reset_by_feature_1802(self):
        """
        Validates TDE data available after reset
        """
        params = self.get_parameters(read_dict=self.get_read_parameters(),
                                     write_dict=self.get_write_parameters())
        params["device_reset_by_feature_1802"] = True
        self.process_api(params)

        self.testCaseChecked("FUN_1EB0_0004", _AUTHOR)
    # end def test_tde_data_available_after_reset_by_feature_1802

    @features("Feature1EB0")
    @level("Functionality")
    @services("PowerSupply")
    def test_tde_data_available_after_reset_by_power_emulator(self):
        """
        Validates TDE data available after reset
        """
        params = self.get_parameters(read_dict=self.get_read_parameters(),
                                     write_dict=self.get_write_parameters())
        params["device_reset_by_power_emulator"] = True
        self.process_api(params)

        self.testCaseChecked("FUN_1EB0_0005", _AUTHOR)
    # end def test_tde_data_available_after_reset_by_power_emulator
# end class TdeAccessToNvmFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
