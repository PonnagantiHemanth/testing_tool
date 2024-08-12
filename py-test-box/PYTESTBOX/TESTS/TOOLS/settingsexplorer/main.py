#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: settingsexplorer.main
:brief: Settings Explorer
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/12/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import os.path as op
import sys
from argparse import ArgumentParser

FILE_PATH = op.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("TESTS")]
TOOLS_DIR = op.join(WS_DIR, "TESTS", "TOOLS")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
# end if

from settingsexplorer.controller import ConfigurationController
from settingsexplorer.model import ConfigurationModel
from settingsexplorer.view import ConfigurationView

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Settings filename")
    parser.add_argument("-d", "--directory", help="Root directory")
    args = parser.parse_args()

    config_model = ConfigurationModel()
    config_view = ConfigurationView()
    config_controller = ConfigurationController(
        model=config_model, view=config_view, filename=args.file, root_path=args.directory)
    config_controller.start()
# end if
