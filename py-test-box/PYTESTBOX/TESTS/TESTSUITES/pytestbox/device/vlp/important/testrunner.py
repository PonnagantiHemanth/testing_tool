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
from pytestbox.device.vlp.important.feature_0102.testrunner import DeviceVlpFeature0102TestSuite
from pytestbox.device.vlp.important.feature_0103.testrunner import DeviceVlpFeature0103TestSuite


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceImportantVlpTestSuite(PyHarnessSuite):
    """
    Test runner class for VLP important tests
    """
    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        # VLP Root Test Case
        self.runTest(result, context, DeviceVlpFeature0102TestSuite)
        self.runTest(result, context, DeviceVlpFeature0103TestSuite)
    # end def runTests
# end class DeviceVlpTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
