#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.hidpp20.important.testrunner
    :brief: Receiver HID++ 2.0 Important features testrunner implementation
    :author: Christophe Roquebert
    :date: 2018/02/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.hidpp20.important.feature_0000 import IRootTestCase
from pytestbox.receiver.hidpp20.important.feature_0001 import IFeatureSetTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class ReceiverImportantHidpp20TestSuite(PyHarnessSuite):
    """
    Test runner class for HID important tests
    """
    def runTests(self, result, context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        """
        self.runTest(result, context, IRootTestCase)
        self.runTest(result, context, IFeatureSetTestCase)
    # end def runTests
# end class ReceiverImportantHidpp20TestSuite


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
