#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: ciscripts.permissions_clean_up
:brief: Clean up the permissions for all the files in py-test-box to be non sudo and have the launcher of the
        execution as the owner of each file and folder.
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/12/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import getpass
import os
from os import getgid
from os import getuid
from os import path
from os import stat
from pathlib import Path
from subprocess import Popen
from sys import executable
from sys import stdout

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
# Mask corresponding to sudo permissions on a file
SUDO_MASK = 0b0000110000000000

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    if not (stat(executable).st_mode & SUDO_MASK):
        stdout.write(f"Python exec {executable} is not root, workaround should not be executed, skipping step")
        exit()
    # end if

    py_test_box_path = str(Path(__file__).parent.resolve()).split("/")
    py_test_box_path = "/".join(py_test_box_path[:py_test_box_path.index("PYTESTBOX")])

    stdout.write(f"Give right ownership and permission to {py_test_box_path}:\n")
    stdout.write(f"\tchown -R {getuid()}:{getgid()} {py_test_box_path}\n")
    process = Popen(["chown", "-R", f"{getuid()}:{getgid()}", py_test_box_path])
    process.communicate()
    stdout.write(f"\tchmod -R -s {py_test_box_path}\n")
    process = Popen(["chmod", "-R", "-s", py_test_box_path])
    process.communicate()

    power_supply_json_path = f"/home/{getpass.getuser()}/framework"
    if path.exists(power_supply_json_path):
        stdout.write(f"Give right ownership and permission to {power_supply_json_path} (power supply json file):\n")
        stdout.write(f"\tchown -R {getuid()}:{getgid()} {power_supply_json_path}\n")
        process = Popen(["chown", "-R", f"{getuid()}:{getgid()}", power_supply_json_path])
        process.communicate()
        stdout.write(f"\tchmod -R -s {power_supply_json_path}\n")
        process = Popen(["chmod", "-R", "-s", power_supply_json_path])
        process.communicate()
    # end if
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
