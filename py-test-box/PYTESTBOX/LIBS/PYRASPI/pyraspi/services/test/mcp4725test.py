#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package:    pyraspi.services.mcp4725
:brief:      Tests for Raspi mcp4725 Control Class
:author:     fred.chen
:date:       2019/7/3
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase
from unittest import skipIf
from time import sleep
import sys

if sys.platform == 'linux':
    from pyraspi.services.daemon import Daemon
    from pyraspi.services.mcp4725 import MCP4725
# end if

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


@skipIf(sys.platform != 'linux', 'Support test on Raspi only!')
@skipIf(Daemon.is_host_kosmos(),
        'Support test on Raspberry Pi NOT configured for KOSMOS project (legacy test environment)!')
class MCP4725TestCase(TestCase):
    """
    Test MCP4725 Class
    """

    def test_MCP4725(self):
        """
        Scan all of 12bits steps
        """
        if MCP4725.discover() is False:
            self.skipTest('MCP4725 is not present!')
        else:
            mcp4725 = MCP4725.get_instance()
            mcp4725.raw_value = 0
            sleep(0.1)
            self.assertEqual(mcp4725.raw_value, 0)
            mcp4725.raw_value = 1000
            sleep(0.1)
            self.assertEqual(mcp4725.raw_value, 1000)
            mcp4725.raw_value = 4095
            sleep(0.1)
            self.assertEqual(mcp4725.raw_value, 4095)
        # end if
    # end def test_MCP4725

# end class MCP4725TestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
