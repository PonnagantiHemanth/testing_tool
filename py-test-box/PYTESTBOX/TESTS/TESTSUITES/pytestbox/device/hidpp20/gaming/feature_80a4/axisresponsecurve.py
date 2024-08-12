#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80a4.axisresponsecurve
:brief: Validate HID++ 2.0 ``AxisResponseCurve`` feature
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/03/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.axisresponsecurveutils import AxisResponseCurveTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AxisResponseCurveTestCase(DeviceBaseTestCase):
    """
    Validate ``AxisResponseCurve`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # axis_index values => 0:accelerator, 1:brake, 2:clutch
        self.axis_value = ("00", "01", "02")
        self.axis_points_value_1 = HexList('0000 0000 0000 0000 0000 0010')
        self.axis_points_value_2 = HexList('0000 0000 0000 0010 FFFF FFFF')
        self.axis_points_value_3 = HexList('0000 0010 0003 0030 FFFF FFFF')
        self.input_value = HexList('7FFF')
        self.axis_64_points_ordered = [HexList('0000 0002 0001 0003 0002 0004'),
                                       HexList('0003 0006 0004 0008 0005 0009'),
                                       HexList('0007 000E 0008 0010 0009 0012'),
                                       HexList('0010 0020 0011 0022 0012 0024'),
                                       HexList('0013 0026 0014 0028 0015 0030'),
                                       HexList('0020 0040 0024 0048 0025 0050'),
                                       HexList('0030 0060 0031 0062 0033 0066'),
                                       HexList('0034 0068 0040 0080 0048 0090'),
                                       HexList('0049 0092 0067 00CE 0080 0100'),
                                       HexList('0089 0118 0090 0120 0091 0122'),
                                       HexList('0092 0124 00CE 019C 0100 0200'),
                                       HexList('019C 0338 0200 0400 0240 0480'),
                                       HexList('0241 0482 0338 0670 0400 0800'),
                                       HexList('0401 0802 0402 0804 0403 0806'),
                                       HexList('0480 0900 0481 0902 0670 0CE0'),
                                       HexList('0800 1000 0900 1200 0901 1202'),
                                       HexList('0CE0 19C0 1000 2000 1200 2400'),
                                       HexList('1201 2402 19C0 3380 2000 4000'),
                                       HexList('2400 4800 2401 4802 3380 6700'),
                                       HexList('4000 8000 4800 9000 4801 9002'),
                                       HexList('4900 9200 4901 9002 6700 CE00'),
                                       HexList('FFFF FFFF')]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x80A4 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_80a4_index, self.feature_80a4, _, _ = AxisResponseCurveTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.AXIS_RESPONSE_CURVE
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        finally:
            super().tearDown()
        # end try
    # end def tearDown
# end class AxisResponseCurveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
