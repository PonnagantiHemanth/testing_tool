#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1806.business
:brief: HID++ 2.0 ConfigurableDeviceProperties business test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/04/28
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.configurabledevicepropertiesutils import ConfigurableDevicePropertiesTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_1806.configurabledeviceproperties import \
    ConfigurableDevicePropertiesTestCase
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"
LogHelper = CommonBaseTestUtils.LogHelper


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ConfigurableDevicePropertiesBusinessTestCase(ConfigurableDevicePropertiesTestCase):
    """
    Validates ConfigurableDeviceProperties business test cases
    """
    @features("Feature1806")
    @level("Business")
    def test_get_device_name_max_count(self):
        """
        Validates GetDeviceNameMaxCount value
        """
        self.post_requisite_reload_nvs = True

        response = Utils.GetDeviceNameMaxCountHelper.HIDppHelper.read(self)
        Utils.GetDeviceNameMaxCountHelper.MessageChecker.check_fields(
                self, response, self.feature_1806.get_device_name_max_count_response_cls)
        device_name_max_count = int(Numeral(response.device_name_max_count))

        full_name = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 2)[0:device_name_max_count]
        # 15 bytes of data & 1 byte of index
        size = 0xF
        (q, r) = divmod(device_name_max_count, size)
        for i in range(q):
            index = i * size
            name_chunk = full_name[index:(index+size)]
            Utils.SetDeviceNameHelper.HIDppHelper.write(self, char_index=index, device_name=name_chunk)
        # end for

        if r > 0:
            index = q * size
            name_chunk = full_name[index:(index + r)]
            Utils.SetDeviceNameHelper.HIDppHelper.write(self, char_index=index, device_name=name_chunk)
        # end if

        Utils.SetDeviceNameCommitHelper.HIDppHelper.write(self, length=device_name_max_count)

        received_name = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
                self, device_name_max_count=device_name_max_count)

        # -----------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate device_name (set x1806 == get x0005) for "
                                  f"device_name_max_count:{device_name_max_count}")
        # -----------------------------------------------------------------------------
        self.assertEqual(expected=full_name,
                         obtained=received_name,
                         msg="The expected device_name is different from obtained")

        self.testCaseChecked("BUS_1806_0001", _AUTHOR)
    # end def test_get_device_name_max_count

    @features("Feature1806")
    @features("Feature0003v4+")
    @level('Business', 'SmokeTests')
    def test_set_device_extend_model_id(self):
        """
        Validates SetDeviceExtendModelID value
        """
        self.post_requisite_reload_nvs = True
        input_value = 1
        Utils.SetDeviceExtendModelIDHelper.HIDppHelper.write(self, extended_model_id=input_value)

        # -----------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDeviceInfo request")
        # -----------------------------------------------------------------------------
        output_value = DeviceInformationTestUtils.HIDppHelper.get_extended_model_id(self)

        # -----------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate device_extend_model_id (set x1806 == get x0003)")
        # -----------------------------------------------------------------------------------
        self.assertEqual(expected=HexList(input_value),
                         obtained=output_value,
                         msg="The expected extended model_id is different from obtained")
        self.testCaseChecked("BUS_1806_0002", _AUTHOR)
    # end def test_set_device_extend_model_id

    @features("Feature1806")
    @features("Feature0005")
    @level("Business")
    def test_set_device_name(self):
        """
        Validates SetDeviceName value
        """
        self.post_requisite_reload_nvs = True

        name_chunk = "Testing"
        Utils.SetDeviceNameHelper.HIDppHelper.write(self, char_index=0, device_name=name_chunk)

        output_value = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
                self, device_name_max_count=len(name_chunk))

        # --------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate device_name before commit (set x1806 != get x0003)")
        # --------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=name_chunk,
                            obtained=output_value,
                            msg="The unexpected device_name is same as obtained")

        Utils.SetDeviceNameCommitHelper.HIDppHelper.write(self, length=len(name_chunk))
        output_value = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
                self, device_name_max_count=len(name_chunk))

        # -------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate device_name after commit (set x1806 == get x0003)")
        # -------------------------------------------------------------------------------------
        self.assertEqual(expected=name_chunk,
                         obtained=output_value,
                         msg="The expected device_name is different from obtained")
        self.testCaseChecked("BUS_1806_0003", _AUTHOR)
    # end def test_set_device_name

    @features("Feature1806")
    @level("Business")
    def test_set_and_get_device_properties(self):
        """
        Validates SetDeviceProperties and GetDeviceProperties
        """
        Utils.HIDppHelper.validate_supported_property_ids(self, read_by_other_feature=True)
        self.testCaseChecked("BUS_1806_0004", _AUTHOR)
# end class ConfigurableDevicePropertiesBusinessTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
