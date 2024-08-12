#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: edge_case_reraise_raise
:brief: Sample file with a reraised raised exception, that does not look at the exception
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/07/09
"""
from subprocess import CalledProcessError


def test_method():
    """
    Sample code with an empty raise

    :raise ``Exception``: reraised exception
    """
    try:
        pass
    except Exception:
        raise
    # end try
# end def test_method
