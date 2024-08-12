#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.base.features
:brief: pytestbox Receiver SubSystem implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/02/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.systems import AbstractSubSystem
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverSubSystem(AbstractSubSystem):
    """
    RECEIVER SubSystem
    """

    def __init__(self):
        AbstractSubSystem.__init__(self, "RECEIVER")

        # ------------
        # Main feature
        # ------------
        self.F_Enabled = False

        # Support of Get RSSI register
        self.F_GetRssi = False

        # Support of USB Boost feature (TB renamed from smoothing algo)
        self.F_USBBoost = False

        # Paired device enumeration SubSystem
        self.ENUMERATION = self.EnumerationSubSystem()

        # TDE
        self.TDE = self.TDESubSystem()
    # end def __init__

    class EnumerationSubSystem(AbstractSubSystem):
        """
        Paired device enumeration Enabler/Disabler SubSystem
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "ENUMERATION")

            # Paired device enumeration feature
            self.F_Enabled = False

            # BLE Enumeration feature
            self.F_BLE = False
            # Support of new Device enumeration mechanism defined in this following flowchart as
            # "Enumeration (= Discovery + Activation)"
            # https://lucid.app/lucidchart/4ec2b55b-188c-4473-b6ec-2cb9ed9513ee/edit?shared=true&page=TuoIO9Dc9RQc#
            self.F_DeviceEnumeration = False

            # UFY Enumeration feature
            self.F_UFY = False

            # USB serial number
            self.F_ReadSerialNumber = False

            # FW Version
            self.F_Fw_Name = 0x00
            self.F_Fw_Version = 0x00
            self.F_Fw_Build_Number = 0x0000
            self.F_Bluetooth_PID = 0x0000
            self.F_Ble_Protocol_Version = 0x00
            # test comment
            self.F_Number_Of_Pairing_Slots = 0x00
            self.F_Name_Length = 0
            self.F_Name_String = ''

            # Unique Identifier
            # To retrieve the value from your Meson DEV board, you shall use JLinkExe application
            # The following exemple has been run on the raspberry PI4 7 CI node
            # /opt/SEGGER/JLink/JLinkExe
            # J-Link>mem 0x10000060, 8
            # 10000060 = 63 05 47 F2 29 5F 28 8D  !! Be careful with the endianness !!
            # => UniqueIdentifierList = '8D285F29F2470563'
            self.F_UniqueIdentifierList = ('0'*16, )
        # end def __init__
    # end class EnumerationSubSystem

    class TDESubSystem(AbstractSubSystem):
        """
        TDE SubSystem
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "TDE")
            self.F_Enabled = False
            self.F_Prepairing = False
            self.F_Non_Volatile_Memory_Access_Size = 0
            self.F_IRK = False
            self.F_CSRK = False
            # Mandatory Key in receiver pre-pairing sequence
            # IrkOptional = False if setting IRK Keys is mandatory in receiver prepairing sequence (Default)
            # IrkOptional = True if setting IRK Keys is not mandatory in receiver prepairing sequence
            self.F_IrkOptional = False
        # end def __init__
    # end class TDESubSystem
# end class ReceiverSubSystem

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
