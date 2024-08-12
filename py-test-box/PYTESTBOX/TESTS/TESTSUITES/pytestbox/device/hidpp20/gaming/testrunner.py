#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.hid.gaming.testrunner
:brief:  HID gaming Devices testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date:   2019/02/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8030.testrunner import DeviceHidpp20Feature8030TestSuite
from pytestbox.device.hidpp20.gaming.feature_8040.testrunner import DeviceHidpp20Feature8040TestSuite
from pytestbox.device.hidpp20.gaming.feature_8051.testrunner import DeviceHidpp20Feature8051TestSuite
from pytestbox.device.hidpp20.gaming.feature_8060.testrunner import DeviceHidpp20Feature8060TestSuite
from pytestbox.device.hidpp20.gaming.feature_8061.testrunner import DeviceHidpp20Feature8061TestSuite
from pytestbox.device.hidpp20.gaming.feature_8071.testrunner import DeviceHidpp20Feature8071TestSuite
from pytestbox.device.hidpp20.gaming.feature_8081.testrunner import DeviceHidpp20Feature8081TestSuite
from pytestbox.device.hidpp20.gaming.feature_8090.testrunner import DeviceHidpp20Feature8090TestSuite
from pytestbox.device.hidpp20.gaming.feature_80a4.testrunner import DeviceHidpp20Feature80A4TestSuite
from pytestbox.device.hidpp20.gaming.feature_80d0.testrunner import DeviceHidpp20Feature80D0TestSuite
from pytestbox.device.hidpp20.gaming.feature_8100.testrunner import DeviceHidpp20Feature8100TestSuite
from pytestbox.device.hidpp20.gaming.feature_8101.testrunner import DeviceHidpp20Feature8101TestSuite
from pytestbox.device.hidpp20.gaming.feature_8134.testrunner import DeviceHidpp20Feature8134TestSuite
from pytestbox.device.hidpp20.gaming.feature_8135.testrunner import DeviceHidpp20Feature8135TestSuite


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GamingHidTestSuite(PyHarnessSuite):
    """
    Test runner class for HID common tests
    """
    def runTests(self, result, context):
        # See: ``PyHarnessSuite.runTests``
        self.runTest(result, context, DeviceHidpp20Feature8030TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8040TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8051TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8060TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8061TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8071TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8081TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8090TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature80A4TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature80D0TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8100TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8101TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8134TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature8135TestSuite)
    # end def runTests
# end class GamingHidTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
