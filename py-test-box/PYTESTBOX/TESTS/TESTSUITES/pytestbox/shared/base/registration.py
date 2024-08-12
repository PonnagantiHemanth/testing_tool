#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.shared.base.registration
    :brief: Shared feature registration module
    :author: Christophe Roquebert
    :date: 2020/03/17
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.selector import features
from pytestbox.base.registration import check_feature

# ------------------------------------------------------------------------------
# Features implementation
# ------------------------------------------------------------------------------

# Shared Features
# -----------------
# Pairing
function = lambda context: (check_feature(context, 'SHARED/DISCOVERY', 'F_Enabled'))
features.registerFeature('BLEDeviceDiscovery', function, featureHelp='Help for BLE Device Discovery')
function = lambda context: (check_feature(context, 'SHARED/PAIRING', 'F_BLEDevicePairing'))
features.registerFeature('BLEDevicePairing', function, featureHelp='Help for BLE Device Pairing')
function = lambda context: (check_feature(context, 'SHARED/PAIRING', 'F_PasskeyAuthenticationMethod'))
features.registerFeature('PasskeyAuthenticationMethod', function, featureHelp='Help for Passkey Authentication Method')
function = lambda context: (check_feature(context, 'SHARED/PAIRING', 'F_Passkey2ButtonsAuthenticationMethod'))
features.registerFeature('Passkey2ButtonsAuthenticationMethod', function, featureHelp='Help for Passkey 2Buttons '
                                                                                      'Authentication Method')
function = lambda context: (check_feature(context, 'SHARED/PAIRING', 'F_Passkey2ButtonsAuthenticationMethod') and
                            not check_feature(context, 'PRODUCT', 'F_IsPlatform') and
                            not check_feature(context, 'SHARED/DEVICES', 'F_IsPlatform'))
features.registerFeature('PasskeyLowEntropy', function, featureHelp='Help for Entropy smaller than 20')
# BLE PRO improvements
function = lambda context: (check_feature(context, 'SHARED/PAIRING', 'F_BLEProOsDetection'))
features.registerFeature('BLEProOsDetection', function, featureHelp='Help for BLE Pro Receiver Detection')
# BLE PRO Attributes
function = lambda context: (check_feature(context, 'SHARED/PAIRING', 'F_BLELatencyRemoval'))
features.registerFeature('BLELatencyRemoval', function, featureHelp='Help for BLE Latency Removal')

function = lambda context: (check_feature(context, 'SHARED/DEVICES', 'F_NumberOfDevices') > 0)
features.registerFeature('RcvWithDevice', function, featureHelp='Help for Shared Devices Enabled')

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
