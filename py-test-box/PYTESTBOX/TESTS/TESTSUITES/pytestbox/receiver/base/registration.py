#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.base.registration
    :brief: Receiver feature registration module
    :author: Christophe Roquebert
    :date: 2020/02/19
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.selector import features
from pytestbox.base.registration import check_feature

# ------------------------------------------------------------------------------
# Features implementation
# ------------------------------------------------------------------------------

# Receiver Features
# -----------------
# Enumeration
function = lambda context: (check_feature(context, 'RECEIVER/ENUMERATION', 'F_Enabled'))
features.registerFeature('RcvEnumeration', function, featureHelp='Help for Receiver Enumeration')
function = lambda context: (check_feature(context, 'RECEIVER/ENUMERATION', 'F_BLE'))
features.registerFeature('RcvBLEEnumeration', function, featureHelp='Help for Receiver BLE Enumeration')
function = lambda context: (check_feature(context, 'RECEIVER/ENUMERATION', 'F_DeviceEnumeration'))
features.registerFeature('RcvBLEDeviceEnumeration', function, featureHelp='Help for Receiver BLE Device Enumeration')
function = lambda context: (check_feature(context, 'RECEIVER/ENUMERATION', 'F_UFY'))
features.registerFeature('RcvUFYEnumeration', function, featureHelp='Help for Receiver UFY Enumeration')
function = lambda context: (check_feature(context, 'RECEIVER/ENUMERATION', 'F_ReadSerialNumber'))
features.registerFeature('RcvReadSerialNumber', function, featureHelp='Help for Receiver Enumeration')
# 0xB4 Get RSSI
function = lambda context: (check_feature(context, 'RECEIVER', 'F_GetRssi'))
features.registerFeature('RcvGetRssi', function, featureHelp='Help for Get Rssi feature')
# TDE
function = lambda context: (check_feature(context, 'RECEIVER/TDE', 'F_Enabled'))
features.registerFeature('RcvBLEProTDE', function, featureHelp='Help for Receiver BLE Pro TDE')
function = lambda context: (check_feature(context, 'RECEIVER/TDE', 'F_Prepairing'))
features.registerFeature('RcvBLEProPrepairing', function, featureHelp='Help for Receiver BLE Pro Prepairing')
function = lambda context: (check_feature(context, 'RECEIVER/TDE', 'F_IRK'))
features.registerFeature('RcvBLEProIRK', function, featureHelp='Help for Receiver BLE Pro IRK')
function = lambda context: (check_feature(context, 'RECEIVER/TDE', 'F_CSRK'))
features.registerFeature('RcvBLEProCSRK', function, featureHelp='Help for Receiver BLE Pro CSRK')
function = lambda context: (check_feature(context, 'RECEIVER/TDE', 'F_IrkOptional'))
features.registerFeature('RcvBLEProIrkOptional', function, featureHelp='Help for Receiver BLE Pro IRK Keys optional '
                                                                       'in pre-pairing sequence')
# 0xF0
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU_CONTROL', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU_CONTROL', 'F_F0ReadCapabilities'))
features.registerFeature('DfuControlReadCapabilities', function, featureHelp='Help for DFU Control tests on receiver ' +
                                                                             'with register read capabilities')
# USB Boost
function = lambda context: (check_feature(context, 'RECEIVER', 'F_USBBoost'))
features.registerFeature('RcvUSBBoost', function, featureHelp='Help for USB Boost feature')

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
