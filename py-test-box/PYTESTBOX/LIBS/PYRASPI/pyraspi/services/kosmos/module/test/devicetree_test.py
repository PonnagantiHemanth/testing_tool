#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.devicetree_test
:brief: Kosmos DeviceTree Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/02/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase

from pyraspi.services.kosmos.module.devicetree import to_identifier


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceTreeModuleTestCase(TestCase):
    """
    Kosmos DeviceTree Module Test Class
    """

    def test_to_identifier(self):
        """
        Validate the static method `to_identifier()`
        """
        # Expect no changes
        self.assertEqual('ABC', to_identifier('ABC'))
        self.assertEqual('abc', to_identifier('abc'))
        self.assertEqual('abcDEF', to_identifier('abcDEF'))
        self.assertEqual('abc_DEF', to_identifier('abc_DEF'))
        self.assertEqual('abc_DEF123', to_identifier('abc_DEF123'))
        self.assertEqual('abc_DEF_123', to_identifier('abc_DEF_123'))

        # Expect changes
        self.assertEqual('abc_DEF', to_identifier('abc DEF'))
        self.assertEqual('abc_DEF', to_identifier('abc$DEF'))
        self.assertEqual('_abc_DEF_123_', to_identifier('<abc DEF-123>'))
        self.assertEqual('_123abcDEF', to_identifier('123abcDEF'))
        self.assertEqual('_', to_identifier('%'))
    # end def test_to_identifier
# end class DeviceTreeModuleTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
