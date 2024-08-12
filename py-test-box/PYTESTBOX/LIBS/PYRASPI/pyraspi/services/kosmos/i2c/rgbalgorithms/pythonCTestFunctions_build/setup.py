#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.i2c.rgbalgorithms.pythonCTestFunctions_build.setup
:brief: Setup for Python interface for the pythonCTestFunctions C library function
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/10/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from distutils.core import Extension
from distutils.core import setup


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def main():
    """
    Setup for Python interface for the pythonCTestFunctions C library function
    """
    setup(name="pythonCTestFunctions",
          version="1.0.0",
          description="Python interface for the pythonCTestFunctions C library function",
          author="Kevin Dayet",
          author_email="kdayet@logitech.com",
          ext_modules=[Extension("pythonCTestFunctions", ["test_rgb_algorithms.c"])])
# end def main


if __name__ == "__main__":
    main()
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
