#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.test.registerbasetest
    :brief: HID++ 1.0 base for registers tests
    :author: Christophe Roquebert
    :date: 2020/03/19
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidppmessage import HidppMessage
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class RegisterBaseTestCase(TestCase):
    """
    Set/Get Register testing class
    """
    def _top_level_class_checker(self, a_class, msg=None):
        """
        Checks some generic attributes from top-level class
        """
        # SUB_ID Constant presence
        self.assertTrue(hasattr(a_class, 'SUB_ID'), msg)
    # end def _top_level_class_checker

    def _function_class_checker(self, a_class, payload_size, msg=None):
        """
        Checks some generic attributes from top-level class
        """
        # top-level attribute presence
        self._top_level_class_checker(a_class, msg)
        # sub_id attribute presence
        self.assertTrue(hasattr(a_class, 'sub_id'), msg)
        # Check payload size
        buffer = HexList(a_class)
        self.assertEqual(payload_size, len(buffer), msg)
    # end def _function_class_checker

    def _attributes_checker(self, a_class, name_size_tuples, msg=None):
        """
        Checks attributes presence and length
        """
        # Other attributes verification
        for name, size in name_size_tuples:
            self.assertTrue(hasattr(a_class, name), msg)
            self.assertEqual(a_class.get_field_from_name(name).length, size, f"""{a_class.name} parameter {name} has \
            an expected size of {a_class.get_field_from_name(name).length} while receiving {size}""")
        # end for
    # end def _attributes_checker

    def _short_function_class_checker(self, a_class, msg=None):
        """
        Checks some generic attributes from top-level class
        """
        # short payload class verification
        self._function_class_checker(a_class, HidppMessage.SHORT_MSG_SIZE, msg)
    # end def _short_function_class_checker

    def _long_function_class_checker(self, a_class, msg=None):
        """
        Checks some generic attributes from top-level class
        """
        # long payload class verification
        self._function_class_checker(a_class, HidppMessage.LONG_MSG_SIZE, msg)
    # end def _long_function_class_checker
# end class RegisterBaseTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
