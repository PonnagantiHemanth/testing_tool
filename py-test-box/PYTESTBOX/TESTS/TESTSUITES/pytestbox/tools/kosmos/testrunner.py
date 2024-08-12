#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.tools.kosmos.testrunner
:brief: Kosmos testrunner implementation
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/07/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.tools.kosmos.kbdgtech import KosmosDualKbdTestCase
from pytestbox.tools.kosmos.kbdgtech import KosmosKbdGtechGalvanicTestCase
from pytestbox.tools.kosmos.kbdmatrix import KosmosKbdMatrixTestCase
from pytestbox.tools.kosmos.kbdgtech import KosmosKbdGtechAnalogTestCase
from pytestbox.tools.kosmos.kbdgtech import KosmosKbdGtechLegacyTestCase
from pytestbox.tools.kosmos.optemu import KosmosOptEmuTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class KosmosTestSuite(PyHarnessSuite):
    """
    Test runner class for Kosmos Test Suite.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, KosmosOptEmuTestCase)
        self.runTest(result, context, KosmosKbdMatrixTestCase)
        self.runTest(result, context, KosmosKbdGtechLegacyTestCase)
        self.runTest(result, context, KosmosKbdGtechAnalogTestCase)
        self.runTest(result, context, KosmosKbdGtechGalvanicTestCase)
        self.runTest(result, context, KosmosDualKbdTestCase)
    # end def runTests
# end class KosmosTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
