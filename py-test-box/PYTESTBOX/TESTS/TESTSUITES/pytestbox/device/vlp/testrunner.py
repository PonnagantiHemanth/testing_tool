#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.testrunner
:brief: Device VLP features testrunner implementation
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2023/07/10
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.vlp.common.testrunner import DeviceCommonVlpTestSuite
from pytestbox.device.vlp.important.testrunner import DeviceImportantVlpTestSuite
from pytestbox.device.vlp.protocol.testrunner import DeviceVlpProtocolTestSuite


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceVlpTestSuite(PyHarnessSuite):
    """
    Test runner class for VLP tests
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        # VLP Protocol Test Case
        self.runTest(result, context, DeviceVlpProtocolTestSuite)

        # VLP Important Test Case
        self.runTest(result, context, DeviceImportantVlpTestSuite)

        # VLP Common Test Case
        self.runTest(result, context, DeviceCommonVlpTestSuite)
    # end def runTests
# end class DeviceVlpTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
