#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.tools.tempfile
:brief: Overload tempfile
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2023/03/03
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import tempfile as o_tempfile
from os import getgid
from os import getuid
from subprocess import Popen


def mkdtemp(suffix=None, prefix=None, dir=None):
    """
    Overload mkdtemp from tempfile to set permissions recursively on created directory.

    See ``tempfile.mkdtemp``
    """
    temp_dir = o_tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
    p_chown = Popen(["chown", "-R", f"{getuid()}:{getgid()}", temp_dir])
    p_chown.communicate()
    p_chmod = Popen(["chmod", "-R", "-s", temp_dir])
    p_chmod.communicate()
    return temp_dir
# end def mkdtemp

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
