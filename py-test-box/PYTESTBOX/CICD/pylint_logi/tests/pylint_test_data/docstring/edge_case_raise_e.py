#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: edge_case_raise_e
:brief: Sample file with a reraised raised exception,
    taken from pyraspi.services.kosmos.gitversion.LocalGitVersion._run_command:
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/07/09
"""
from subprocess import CalledProcessError


def _run_command():
    """
    Sample code taken from ``pyraspi.services.kosmos.gitversion.LocalGitVersion._run_command`` method.

    :raise ``FileNotFoundError``: File not found
    :raise ``CalledProcessError``: When the command fails
    """
    try:
        pass
    except CalledProcessError as e:
        if e.returncode == 128:
            msg = e.output.strip().decode()
            raise FileNotFoundError(msg) from e
        # end if
        raise e
    # end try
# end def _run_command
