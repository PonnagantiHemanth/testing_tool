#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1815.testrunner
:brief: Device HID++ 2.0 Common feature 0x1815 testrunner implementation
:author: Christophe Roquebert
:date: 2021/03/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1815.business import HostsInfoBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1815.errorhandling import HostsInfoErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1815.functionality import HostsInfoFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1815.functionality import HostsInfoFunctionalityMultiReceiverTestCase
from pytestbox.device.hidpp20.common.feature_1815.interface import HostsInfoInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1815.robustness import HostsInfoRobustnessTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature1815TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x1815 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, HostsInfoBusinessTestCase)
        self.runTest(result, context, HostsInfoErrorHandlingTestCase)
        self.runTest(result, context, HostsInfoFunctionalityTestCase)
        self.runTest(result, context, HostsInfoFunctionalityMultiReceiverTestCase)
        self.runTest(result, context, HostsInfoInterfaceTestCase)
        self.runTest(result, context, HostsInfoRobustnessTestCase)

    # end def runTests
# end class DeviceHidpp20Feature1815TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
