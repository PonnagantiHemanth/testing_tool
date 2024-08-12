#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.fpgatransport_test
:brief: Tests for the FPGA Transport
:author: Alexandre Lafaye <alafaye@logitech.com>
:date: 2022/10/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class FPGATransportTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos FPGA Transport class
    """

    def test_hwcfg(self):
        """
        Validate ``FPGATransport.hwcfg`` property.
        """
        fpga_hwcfg = self.kosmos.dt.fpga_transport.hwcfg
        self.printd(fpga_hwcfg)
    # end def test_hwcfg

    def test_fpga_revision(self):
        """
        Validate ``FPGATransport.fpga_revision`` property.
        """
        fpga_revision = self.kosmos.dt.fpga_transport.fpga_revision
        self.printd(fpga_revision)
    # end def test_fpga_revision
# end class FPGATransportTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
