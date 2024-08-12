#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: autotests.base.features
:brief:  EXAMPLES features
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/11/13
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.systems import AbstractSubSystem

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ExamplesSubSystem( AbstractSubSystem ):
    """
    [EXAMPLES] section
    """

    def __init__(self):
        AbstractSubSystem.__init__(self, 'EXAMPLES')
        ##@name Main features
        ##@{
        self.F_Enabled  = False ##< Enable/disable the section
        ##@}

    # end def __init__
# end class ExamplesSubSystem

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
