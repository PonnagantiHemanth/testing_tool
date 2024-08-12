#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.performdeviceconnection
    :brief: HID++ 1.0 Perform Device Connection and Disconnection registers definition
    :author: Christophe Roquebert
    :date: 2020/03/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegisterResponse
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PerformDeviceConnectionModel(BaseRegisterModel):
    """
    Register Perform Device Connection model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get register model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                "request": SetPerformDeviceConnectionRequest,
                "response": SetPerformDeviceConnectionResponse
            },
        }
    # end def _get_data_model
# end class PerformDeviceConnectionModel


class SetPerformDeviceConnectionRequest(SetLongRegister):
    """
    Sending this command will force the device to connect using the requested authentication method.
    """
    class ConnectState:
        """
        Connect Devices p0 Values
        """
        RESERVED_0 = 0
        PAIRING = 1
        CANCEL_PAIRING = 2
        UNPAIRING = 3
        # 4..255 = Reserved
        RESERVED = 4
    # end class ConnectState

    class FID(SetLongRegister.FID):
        """
        Field Identifiers
        """
        CONNECT_DEVICES = SetLongRegister.FID.ADDRESS - 1
        PAIRING_SLOT_TO_BE_UNPAIRED = CONNECT_DEVICES - 1
        BLUETOOTH_ADDRESS = PAIRING_SLOT_TO_BE_UNPAIRED - 1
        RESERVED_AUTH_METHOD = BLUETOOTH_ADDRESS - 1
        EMU_2BUTTONS_AUTH_METHOD = RESERVED_AUTH_METHOD - 1
        PASSKEY_AUTH_METHOD = EMU_2BUTTONS_AUTH_METHOD - 1
        AUTH_ENTROPY = PASSKEY_AUTH_METHOD - 1
        PADDING = AUTH_ENTROPY - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        """
        Field Lengths in bits
        """
        CONNECT_DEVICES = 0x08
        PAIRING_SLOT_TO_BE_UNPAIRED = 0x08
        BLUETOOTH_ADDRESS = 0x30
        # Requested Authentication method
        RESERVED_AUTH_METHOD = 0x06
        EMU_2BUTTONS_AUTH_METHOD = 0x01
        PASSKEY_AUTH_METHOD = 0x01
        AUTH_ENTROPY = 0x08
        PADDING = 0x30
    # end class LEN

    class DEFAULT(SetLongRegister.DEFAULT):
        """
        Fields Default values
        """
        RESERVED = 0x00
        ENTROPY_LENGTH_MIN = 0x0A
        TWO_BUTTONS_EMULATION_ENTROPY_LENGTH_MIN = 0x0A
        PASSKEY_ENTROPY_LENGTH_MIN = 0x14
        ENTROPY_LENGTH_MAX = 0x14
    # end class DEFAULT

    class MASK():
        """
        Requested Authentication bit field masks
        """
        RESERVED_AUTH_METHOD = 0xFC
        EMU_2BUTTONS_AUTH_METHOD = 0x02
        PASSKEY_AUTH_METHOD = 0x01
        BOTH_AUTH_METHOD = EMU_2BUTTONS_AUTH_METHOD | PASSKEY_AUTH_METHOD
    # end class MASK

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.CONNECT_DEVICES,
                 LEN.CONNECT_DEVICES,
                 title='ConnectDevices',
                 name='connect_devices',
                 checks=(CheckHexList(LEN.CONNECT_DEVICES // 8),
                         CheckByte(),),
                 default_value=0),
        BitField(FID.PAIRING_SLOT_TO_BE_UNPAIRED,
                 LEN.PAIRING_SLOT_TO_BE_UNPAIRED,
                 title='PairingSlotToBeUnpaired',
                 name='pairing_slot_to_be_unpaired',
                 checks=(CheckHexList(LEN.PAIRING_SLOT_TO_BE_UNPAIRED // 8),
                         CheckByte(),),
                 default_value=0),
        BitField(FID.BLUETOOTH_ADDRESS,
                 LEN.BLUETOOTH_ADDRESS,
                 title='BluetoothAddress',
                 name='bluetooth_address',
                 checks=(CheckHexList(LEN.BLUETOOTH_ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BLUETOOTH_ADDRESS) - 1),), ),
        BitField(FID.RESERVED_AUTH_METHOD,
                 LEN.RESERVED_AUTH_METHOD,
                 title='ReservedAuthMethod',
                 name='reserved_auth_method',
                 checks=(CheckHexList(LEN.RESERVED_AUTH_METHOD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED_AUTH_METHOD) - 1),),
                 default_value=DEFAULT.RESERVED),
        BitField(FID.EMU_2BUTTONS_AUTH_METHOD,
                 LEN.EMU_2BUTTONS_AUTH_METHOD,
                 title='Emu2ButtonsAuthMethod',
                 name='emu_2buttons_auth_method',
                 checks=(CheckHexList(LEN.EMU_2BUTTONS_AUTH_METHOD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EMU_2BUTTONS_AUTH_METHOD) - 1),),
                 default_value=0),
        BitField(FID.PASSKEY_AUTH_METHOD,
                 LEN.PASSKEY_AUTH_METHOD,
                 title='PassKeyAuthMethod',
                 name='passkey_auth_method',
                 checks=(CheckHexList(LEN.PASSKEY_AUTH_METHOD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PASSKEY_AUTH_METHOD) - 1),),
                 default_value=0),
        BitField(FID.AUTH_ENTROPY,
                 LEN.AUTH_ENTROPY,
                 title='AuthEntropy',
                 name='auth_entropy',
                 checks=(CheckHexList(LEN.AUTH_ENTROPY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.AUTH_ENTROPY) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DEFAULT.PADDING),
    )

    def __init__(self, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                 connect_devices=0, pairing_slot_to_be_unpaired=0, bluetooth_address=0, passkey_auth_method=0,
                 emu_2buttons_auth_method=0, auth_entropy=DEFAULT.ENTROPY_LENGTH_MAX):
        """
        Constructor
        """
        super().__init__(device_index,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_CONNECTION_DISCONNECTION)
        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG

        self.connect_devices = connect_devices
        self.pairing_slot_to_be_unpaired = pairing_slot_to_be_unpaired
        self.bluetooth_address = bluetooth_address
        self.passkey_auth_method = passkey_auth_method
        self.emu_2buttons_auth_method = emu_2buttons_auth_method
        self.auth_entropy = auth_entropy
    # end def __init__
# end class SetPerformDeviceConnectionRequest


class SetPerformDeviceConnectionResponse(SetLongRegisterResponse):
    """
    Perform device connection and disconnection

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || Address                || 8            ||
    || Padding                || 24           ||
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_CONNECTION_DISCONNECTION)
# end class SetPerformDeviceConnectionResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
