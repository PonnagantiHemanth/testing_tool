#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.layout.layout
:brief: Hid Keyboard layout test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/07/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.keyboard.keycode.keycode import KeyCodeTestCase
from pytestbox.device.base.layoututils import LayoutTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LayoutTestCase(KeyCodeTestCase):
    """
    Validate Keyboard International Layout requirement
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        self.post_requisite_reload_nvs = True
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
        # end with

        with self.manage_post_requisite():
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Switch back to the default Keyboard layout")
            # ------------------------------------------------------------------------------------------------------
            LayoutTestUtils.select_layout(test_case=self)
        # end with

        super().tearDown()
    # end def tearDown
# end class LayoutTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
