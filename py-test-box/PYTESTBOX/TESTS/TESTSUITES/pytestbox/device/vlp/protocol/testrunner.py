#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.protocol.testrunner
:brief: Device VLP protocol testrunner implementation
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2023/07/10
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.vlp.protocol.business import VlpProtocolBusinessTestCase
from pytestbox.device.vlp.protocol.errorhandling import VlpProtocolErrorHandlingTestCase
from pytestbox.device.vlp.protocol.functionality import VlpProtocolFunctionalityTestCase
from pytestbox.device.vlp.protocol.robustness import VlpProtocolRobustnessTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceVlpProtocolTestSuite(PyHarnessSuite):
    """
    Test runner class for VLP tests
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        # VLP Protocol Test Suite
        self.runTest(result, context, VlpProtocolBusinessTestCase)
        self.runTest(result, context, VlpProtocolFunctionalityTestCase)
        self.runTest(result, context, VlpProtocolRobustnessTestCase)
        self.runTest(result, context, VlpProtocolErrorHandlingTestCase)
    # end def runTests
# end class DeviceVlpProtocolTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
