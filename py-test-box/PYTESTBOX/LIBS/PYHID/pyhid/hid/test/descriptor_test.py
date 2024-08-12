#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.test.descriptor_test
:brief: descriptor test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/31
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from time import perf_counter_ns

from pyharness.core import TestCase
from pyhid.hid.descriptor import ReportDescriptor


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DescriptorTestCase(TestCase):
    """
    Descriptor testing class
    """

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        super().setUp()
        self.timestamp = perf_counter_ns()
    # end def setUp

    def descriptor_class_checker(self, instance, my_class, timestamp=None):
        """
        Check some generic attributes of a class inheriting from ``ReportDescriptor``
        """
        self.assertNotNone(instance, f'Could not instantiate the {my_class.__name__} class')
        self.assertTrue(isinstance(instance, my_class), f'Wrong class name {instance.name} vs {my_class.__name__}')
        # BITFIELD_LENGTH attribute presence
        self.assertEqual(instance.BITFIELD_LENGTH, len(instance))
        # Inheriting from ``TimestampedBitFieldContainerMixin``
        if timestamp is not None:
            self.assertEqual(instance.timestamp, timestamp)
        else:
            self.assertNotNone(instance.timestamp, 'Timestamp has not been initialized')
        # end if
    # end def descriptor_class_checker

    def test_interface_descriptor_instantiation(self):
        """
        Test ``ReportDescriptor`` class instantiation
        """
        descriptor = ReportDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, ReportDescriptor, self.timestamp)
    # end def test_interface_descriptor_instantiation

# end class DescriptorTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
