#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.test.displaypasskeykey_test
    :brief: HID++ 1.0 HID++ 1.0 display passkey key notification tests
    :author: Christophe Roquebert
    :date: 2020/03/17
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.test.registerbasetest import RegisterBaseTestCase
from pyhid.hidpp.hidpp1.notifications.displaypasskeykey import DisplayPassKeyKey


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DisplayPassKeyKeyTestCase(RegisterBaseTestCase):
    """
    Display PassKey Key notification testing class
    """

    def test_display_passkey_key_notification(self):
        """
        Tests Display PassKey Key class instantiation
        """
        # Test Class notification minimum values
        my_class = DisplayPassKeyKey(device_index=0, key_code=0, bluetooth_address=0)
        self._long_function_class_checker(my_class)

        # Test Class maximum value
        my_class = DisplayPassKeyKey(device_index=0xFF, key_code=0xFF, bluetooth_address=0xFF)
        self._long_function_class_checker(my_class)

    # end def test_display_passkey_key_notification
# end class DisplayPassKeyKeyTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
