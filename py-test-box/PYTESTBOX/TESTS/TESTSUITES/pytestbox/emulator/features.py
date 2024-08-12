#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.emulator.features
:brief: pytestbox Emulator SubSystem implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/07/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.systems import AbstractSubSystem


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class EmulatorSubSystem(AbstractSubSystem):
    """
    EMULATOR SubSystem
    """

    def __init__(self):
        AbstractSubSystem.__init__(self, "EMULATOR")

        # ------------
        # Emulator feature
        # ------------
        self.F_Enabled = False
    # end def __init__
# end class EmulatorSubSystem

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
