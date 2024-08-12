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
from pytestbox.device.vlp.common.feature_19a1.testrunner import DeviceVlpFeature19A1TestSuite


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceCommonVlpTestSuite(PyHarnessSuite):
    """
    Test runner class for VLP Common tests
    """
    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        # 0x19A1 Contextual Display Test Case
        self.runTest(result, context, DeviceVlpFeature19A1TestSuite)
    # end def runTests
# end class DeviceCommonVlpTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
