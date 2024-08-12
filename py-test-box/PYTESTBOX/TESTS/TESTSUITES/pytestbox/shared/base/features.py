#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.features
:brief: pytestbox Shared SubSystem implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/03/17
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.systems import AbstractSubSystem


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedSubSystem(AbstractSubSystem):
    """
    SHARED SubSystem
    """

    def __init__(self):
        AbstractSubSystem.__init__(self, "SHARED")

        # ------------
        # Main feature
        # ------------
        self.F_Enabled = True

        # Discovery SubSystem
        self.DISCOVERY = self.DiscoverySubSystem()

        # Pairing SubSystem
        self.PAIRING = self.PairingSubSystem()

        # Devices SubSystem
        self.DEVICES = self.DevicesSubSystem()
    # end def __init__

    class DiscoverySubSystem(AbstractSubSystem):
        """
        Discovery Enabler/Disabler SubSystem
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "DISCOVERY")

            self.F_Enabled = False
        # end def __init__
    # end class DiscoverySubSystem

    class PairingSubSystem(AbstractSubSystem):
        """
        Pairing Enabler/Disabler SubSystem
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "PAIRING")

            ## BLE Perform device connection
            self.F_BLEDevicePairing = False
            ## BLE Pro Authentication method selected for the test node
            # Passkey
            self.F_PasskeyAuthenticationMethod = False
            # Passkey emulation with 2 buttons
            self.F_Passkey2ButtonsAuthenticationMethod = False

            ## BLE PRO improvements
            # Capability to detect a BLE Pro Receiver
            self.F_BLEProOsDetection = False

            ## BLE Pro Attributes
            # Latency removal feature
            # This feature is used to remove the latency between the connection and the first HID report
            # https://docs.google.com/spreadsheets/d/1PW_wT5PmNeHsGw6s_URL0nYtBOh4q-kclZO6a_w8we4/edit?usp=sharing
            self.F_BLELatencyRemoval = False
        # end def __init__
    # end class PairingSubSystem

    class DevicesSubSystem(AbstractSubSystem):
        """
        Device dependant features
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "DEVICES")

            self.F_NumberOfDevices = 1

            self.F_Type = None
            self.F_Name = None
            self.F_BluetoothPID = None
            self.F_BLEProServiceVersion = None
            self.F_ExtendedModelId = None

            self.F_UnitIds_1 = None
            self.F_UnitIds_2 = None
            self.F_UnitIds_3 = None
            self.F_UnitIds_4 = None
            self.F_UnitIds_5 = None
            self.F_UnitIds_6 = None

            self.F_DeviceHexFile = None
            self.F_DeviceApplicationDfuFileName = None
            self.F_IsPlatform = False

            ## BLE Pro Authentication method supported by the device
            # Passkey
            self.F_PasskeyAuthMethod = None
            # Passkey emulation with 2 buttons
            self.F_Passkey2ButtonsAuthMethod = None
            # Pre Pairing
            self.F_PrePairingAuthMethod = None
            # Authentication entropy
            self.F_AuthEntropy = None

            # Root Feature Version
            self.F_RootFeatureVersion = None
            self.F_VLPRootFeatureVersion = None

        # end def __init__
    # end class DevicesSubSystem
# end class SharedSubSystem

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
