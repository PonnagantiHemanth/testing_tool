#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.test.pairingstatus_test
    :brief: HID++ 1.0 HID++ 1.0 pairing status notification tests
    :author: Christophe Roquebert
    :date: 2020/04/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.test.registerbasetest import RegisterBaseTestCase
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PairingStatusTestCase(RegisterBaseTestCase):
    """
    Pairing Status testing class
    """

    def test_pairing_status_notification(self):
        """
        Tests Pairing Status class instantiation
        """
        # Test Class notification minimum values
        my_class = PairingStatus(device_index=0,
                                 device_pairing_status=0,
                                 error_type=0,
                                 bluetooth_address=HexList("00"*(PairingStatus.LEN.BLUETOOTH_ADDRESS//8)),
                                 pairing_slot=0x00)
        self._long_function_class_checker(my_class)

        # Test Class maximum value
        my_class = PairingStatus(device_index=0xFF,
                                 device_pairing_status=0xFF,
                                 error_type=0xFF,
                                 bluetooth_address=HexList("FF"*(PairingStatus.LEN.BLUETOOTH_ADDRESS//8)),
                                 pairing_slot=0xFF)
        self._long_function_class_checker(my_class)
    # end def test_pairing_status_notification

    def test_pairing_status(self):
        """
        Tests Pairing Status constants
        """
        # Test PAIRING_START constant
        my_class = PairingStatus(device_index=0, device_pairing_status=PairingStatus.STATUS.PAIRING_START)
        self._long_function_class_checker(my_class)

        # Test PAIRING_CANCEL constant
        my_class = PairingStatus(device_index=0, device_pairing_status=PairingStatus.STATUS.PAIRING_CANCEL)
        self._long_function_class_checker(my_class)

        # Test PAIRING_STOP constant
        my_class = PairingStatus(device_index=0, device_pairing_status=PairingStatus.STATUS.PAIRING_STOP)
        self._long_function_class_checker(my_class)
    # end def test_pairing_status

    def test_error_types(self):
        """
        Tests Error Types constants
        """
        # Test NO_ERROR constant
        my_class = PairingStatus(device_index=0, error_type=PairingStatus.ERROR_TYPE.NO_ERROR)
        self._long_function_class_checker(my_class)

        # Test TIMEOUT constant
        my_class = PairingStatus(device_index=0, error_type=PairingStatus.ERROR_TYPE.TIMEOUT)
        self._long_function_class_checker(my_class)

        # Test FAILED constant
        my_class = PairingStatus(device_index=0, error_type=PairingStatus.ERROR_TYPE.FAILED)
        self._long_function_class_checker(my_class)

        # Test RESERVED constant
        for my_error in PairingStatus.ERROR_TYPE.RESERVED:
            my_class = PairingStatus(device_index=0, error_type=my_error)
            self._long_function_class_checker(my_class)
        # end for
    # end def test_pairing_status
# end class PairingStatusTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
