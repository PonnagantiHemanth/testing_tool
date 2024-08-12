#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyharness.debuggers
:brief: Debugger package
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/10/26
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
DEBUGGERS_MAPPING = {
    "FakeDebugger":                 "pyharness.debuggers.jlinkdebugger.FakeDebugger",
    # NRF52 family
    "GravitonJlinkDebugger":        "pyharness.debuggers.jlinkdebugger.GravitonJlinkDebugger",
    "Graviton4Zones64KJlinkDebugger":"pyharness.debuggers.jlinkdebugger.Graviton4Zones64KJlinkDebugger",
    "QuarkJlinkDebugger":           "pyharness.debuggers.jlinkdebugger.QuarkJlinkDebugger",
    "QuarkMultiZoneJlinkDebugger":  "pyharness.debuggers.jlinkdebugger.QuarkMultiZoneJlinkDebugger",
    "Quark256JlinkDebugger":        "pyharness.debuggers.jlinkdebugger.Quark256JlinkDebugger",
    "GluonJlinkDebugger":           "pyharness.debuggers.jlinkdebugger.GluonJlinkDebugger",
    "DeviceMesonJlinkDebugger":     "pyharness.debuggers.jlinkdebugger.DeviceMesonJlinkDebugger",
    "Hadron3Zones24KJlinkDebugger": "pyharness.debuggers.jlinkdebugger.Hadron3Zones24KJlinkDebugger",
    "Hadron4Zones40KJlinkDebugger": "pyharness.debuggers.jlinkdebugger.Hadron4Zones40KJlinkDebugger",
    "Hadron5Zones64KJlinkDebugger": "pyharness.debuggers.jlinkdebugger.Hadron5Zones64KJlinkDebugger",
    "Hadron4Zones64KJlinkDebugger": "pyharness.debuggers.jlinkdebugger.Hadron4Zones64KJlinkDebugger",
    "Hadron4Zones104KJlinkDebugger": "pyharness.debuggers.jlinkdebugger.Hadron4Zones104KJlinkDebugger",
    "Hadron1Zone8KJlinkDebugger":   "pyharness.debuggers.jlinkdebugger.Hadron1Zone8KJlinkDebugger",
    "Hadron1Zone24KJlinkDebugger":   "pyharness.debuggers.jlinkdebugger.Hadron1Zone24KJlinkDebugger",
    "ReceiverMesonJlinkDebugger":   "pyharness.debuggers.jlinkdebugger.ReceiverMesonJlinkDebugger",
    "MezzyOnGravitonJlinkDebugger": "pyharness.debuggers.jlinkdebugger.MezzyOnGravitonJlinkDebugger",
    # NRF Probe lib
    "Nrf54H20ProbeDebugger":        "pyharness.debuggers.nrfprobedebugger.Nrf54H20ProbeDebugger",
    # STM32 family
    "STM32F723IEJLinkDebugger":     "pyharness.debuggers.jlinkdebugger.STM32F723IEJLinkDebugger",
    "STM32F072CBJlinkDebugger":     "pyharness.debuggers.jlinkdebugger.STM32F072CBJlinkDebugger",
    "STM32H7B0IBJLinkDebugger":     "pyharness.debuggers.jlinkdebugger.STM32H7B0IBJLinkDebugger",
    "STM32L052JLinkDebugger":       "pyharness.debuggers.jlinkdebugger.STM32L052JLinkDebugger",
    "STM32C071Debugger":            "pyharness.debuggers.stlinkdebugger.STM32C071Debugger",
    "LexendJLinkDebugger":          "pyharness.debuggers.jlinkdebugger.LexendJLinkDebugger",
    # Telink family
    "TLSR8208CDebugger":            "pyharness.debuggers.telinkdebugger.TLSR8208CDebugger",
}

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
