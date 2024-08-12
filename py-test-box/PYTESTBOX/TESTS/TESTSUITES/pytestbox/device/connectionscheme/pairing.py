#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.device.connectionscheme.pairing
    :brief: Validates device pairing feature
    :author: Christophe Roquebert
    :date: 2020/03/09
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.shared.connectionscheme.pairing import SharedPairingTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingTestCase(SharedPairingTestCase, DeviceBaseTestCase):
    """
    Device Pairing TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        super().tearDown()
    # end def tearDown
# end class PairingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
