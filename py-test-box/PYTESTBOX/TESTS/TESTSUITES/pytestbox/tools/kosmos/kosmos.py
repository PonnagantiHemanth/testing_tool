#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.tools.kosmos.kosmos
:brief: Kosmos Validation
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/07/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KosmosTestCase(BaseTestCase):
    """
    Kosmos Validation
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_clean_default_memory_cache = False
        super().setUp()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_clean_default_memory_cache:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean default memory cache")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator._init_default_memory_cache()
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class KosmosTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
