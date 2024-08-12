#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures
    :brief: HID++ 1.0 Manage Deactivatable Features registers definition
    :author: Christophe Roquebert
    :date: 2020/11/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel, GetRegisterRequest, GetRegister
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ManageDeactivatableFeaturesInfoAndDisableModel(BaseRegisterModel):
    """
    Register Manage Deactivatable Features Info and Disable model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": ManageDeactivatableFeaturesDisableFeaturesRequest,
                "response": ManageDeactivatableFeaturesDisableFeaturesResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": ManageDeactivatableFeaturesGetInfoRequest,
                "response": ManageDeactivatableFeaturesGetInfoResponse
            },
        }
    # end def _get_data_model
# end class ManageDeactivatableFeaturesInfoAndDisableModel


class ManageDeactivatableFeaturesDisableFeaturesRequest(SetRegister):
    """
    Write Manage Deactivatable Features 'Disable Features' request
    """
    class FID(SetRegister.FID):
        """
        Fields Identifiers
        """
        DISABLE_BIT_MAP = SetRegister.FID.ADDRESS - 1
        PADDING = DISABLE_BIT_MAP - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Fields Lengths in bits
        """
        DISABLE_BIT_MAP = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.DISABLE_BIT_MAP,
                 LEN.DISABLE_BIT_MAP,
                 title='DisableBitMap',
                 name='disable_bit_map',
                 checks=(CheckHexList(LEN.DISABLE_BIT_MAP // 8), CheckByte(),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SetRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, disable_all_bit=False, disable_gothard=False, disable_compliance=False,
                 disable_manufacturing=False):
        """
        Constructor

        Disable BitMap
            A bit set to 1 specifies that the corresponding features shall be disabled.
            A bit set to 0 specifies that it shall remain unmodified

        :param disable_all_bit: When this bit is set, the 7 least significant bits are ignored and
                                all supported features are disabled.
        :type disable_all_bit: ``int`` or ``bool``
        :param disable_gothard: The Gothard manufacturing protocol is disabled.
        :type disable_gothard: ``int`` or ``bool``
        :param disable_compliance: All compliance HID++ deactivatable features are disabled.
        :type disable_compliance: ``int`` or ``bool``
        :param disable_manufacturing: All manufacturing HID++ deactivatable features are disabled.
        :type disable_manufacturing: ``int`` or ``bool``
        """
        super().__init__(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
            address=Hidpp1Data.Hidpp1RegisterAddress.MANAGE_DEACTIVATABLE_FEATURES_GET_INFO_AND_DISABLE_FEATURES)

        self.disable_bit_map = ManageDeactivatableFeaturesAuth.BitMap(
            all_bit=disable_all_bit, gothard=disable_gothard, compliance=disable_compliance,
            manufacturing=disable_manufacturing)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param cls: Target class
        :type cls: ``type``
        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``ManageDeactivatableFeaturesDisableFeaturesRequest``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.disable_bit_map = ManageDeactivatableFeaturesAuth.BitMap.fromHexList(
            inner_field_container_mixin.disable_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class ManageDeactivatableFeaturesDisableFeaturesRequest


class ManageDeactivatableFeaturesDisableFeaturesResponse(SetRegisterResponse):
    """
    Write Manage Deactivatable Features 'Disable Features' response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
            address=Hidpp1Data.Hidpp1RegisterAddress.MANAGE_DEACTIVATABLE_FEATURES_GET_INFO_AND_DISABLE_FEATURES)
    # end def __init__
# end class ManageDeactivatableFeaturesDisableFeaturesResponse


class ManageDeactivatableFeaturesGetInfoRequest(GetRegisterRequest):
    """
    Read Manage Deactivatable Features 'Get Info' request
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
            address=Hidpp1Data.Hidpp1RegisterAddress.MANAGE_DEACTIVATABLE_FEATURES_GET_INFO_AND_DISABLE_FEATURES)
    # end def __init__
# end class ManageDeactivatableFeaturesGetInfoRequest


class ManageDeactivatableFeaturesGetInfoResponse(GetRegister):
    """
    Read Manage Deactivatable Features 'Get Info' response
    """
    class FID(SetRegister.FID):
        """
        Fields Identifiers
        """
        SUPPORT_BIT_MAP = GetRegister.FID.ADDRESS - 1
        PERSIST_BIT_MAP = SUPPORT_BIT_MAP - 1
        STATE_BIT_MAP = PERSIST_BIT_MAP - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Fields Lengths in bits
        """
        SUPPORT_BIT_MAP = 0x08
        PERSIST_BIT_MAP = 0x08
        STATE_BIT_MAP = 0x08
    # end class LEN

    FIELDS = GetRegister.FIELDS + (
        BitField(fid=FID.SUPPORT_BIT_MAP,
                 length=LEN.SUPPORT_BIT_MAP,
                 title='SupportBitMap',
                 name='support_bit_map',
                 checks=(CheckHexList(LEN.SUPPORT_BIT_MAP // 8), CheckByte(),), ),
        BitField(fid=FID.PERSIST_BIT_MAP,
                 length=LEN.PERSIST_BIT_MAP,
                 title='PersistBitMap',
                 name='persist_bit_map',
                 checks=(CheckHexList(LEN.PERSIST_BIT_MAP // 8), CheckByte(),), ),
        BitField(fid=FID.STATE_BIT_MAP,
                 length=LEN.STATE_BIT_MAP,
                 title='StateBitMap',
                 name='state_bit_map',
                 checks=(CheckHexList(LEN.STATE_BIT_MAP // 8), CheckByte(),), ),
    )

    def __init__(self, support_all_bit=False, support_gothard=False,
                 support_compliance=False, support_manufacturing=False, persistent_all_bit_activation=False,
                 persistent_gothard_activation=False, persistent_compliance_activation=False,
                 persistent_manufacturing_activation=False, state_all_bit_activation=False,
                 state_gothard_activation=False, state_compliance_activation=False,
                 state_manufacturing_activation=False):
        """
        Constructor

        Support BitMap
            A bit set to 1 specifies that the corresponding feature is supported.
            A bit set to 0 specifies that a deactivation mechanism for the corresponding feature is not provided

        Persist BitMap
            A bit set to 1 specifies that the activation of the corresponding feature is persistent.
            A bit set to 0 specifies that it is volatile.

        State BitMap
            A bit set to 1 specifies that corresponding feature is activated.
            A bit set to 0 specifies that it is not activated.

        :param support_all_bit: The most significant bit shall always be zero.
        :type support_all_bit: ``int`` or ``bool``
        :param support_gothard: The Gothard manufacturing protocol.
        :type support_gothard: ``int`` or ``bool``
        :param support_compliance: All compliance HID++ deactivatable features.
        :type support_compliance: ``int`` or ``bool``
        :param support_manufacturing: All manufacturing HID++ deactivatable features.
        :type support_manufacturing: ``int`` or ``bool``
        :param persistent_all_bit_activation: The most significant bit shall always be zero.
        :type persistent_all_bit_activation: ``int`` or ``bool``
        :param persistent_gothard_activation: Activation of Gothard features is persistent.
        :type persistent_gothard_activation: ``int`` or ``bool``
        :param persistent_compliance_activation: Activation of all compliance HID++ features is persistent.
        :type persistent_compliance_activation: ``int`` or ``bool``
        :param persistent_manufacturing_activation: Activation of all manufacturing HID++ features is persistent.
        :type persistent_manufacturing_activation: ``int`` or ``bool``
        :param state_all_bit_activation: The most significant bit shall always be zero.
        :type state_all_bit_activation: ``int`` or ``bool``
        :param state_gothard_activation: Activation of Gothard features is persistent.
        :type state_gothard_activation: ``int`` or ``bool``
        :param state_compliance_activation: Activation of all compliance HID++ features is persistent.
        :type state_compliance_activation: ``int`` or ``bool``
        :param state_manufacturing_activation: Activation of all manufacturing HID++ features is persistent.
        :type state_manufacturing_activation: ``int`` or ``bool``
        """
        super().__init__(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
            address=Hidpp1Data.Hidpp1RegisterAddress.MANAGE_DEACTIVATABLE_FEATURES_GET_INFO_AND_DISABLE_FEATURES)

        self.support_bit_map = ManageDeactivatableFeaturesAuth.BitMap(
            all_bit=support_all_bit, gothard=support_gothard, compliance=support_compliance,
            manufacturing=support_manufacturing)
        self.persist_bit_map = ManageDeactivatableFeaturesAuth.BitMap(
            all_bit=persistent_all_bit_activation, gothard=persistent_gothard_activation,
            compliance=persistent_compliance_activation, manufacturing=persistent_manufacturing_activation)
        self.state_bit_map = ManageDeactivatableFeaturesAuth.BitMap(
            all_bit=state_all_bit_activation, gothard=state_gothard_activation,
            compliance=state_compliance_activation, manufacturing=state_manufacturing_activation)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``ManageDeactivatableFeaturesGetInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.support_bit_map = ManageDeactivatableFeaturesAuth.BitMap.fromHexList(
            inner_field_container_mixin.support_bit_map)
        inner_field_container_mixin.persist_bit_map = ManageDeactivatableFeaturesAuth.BitMap.fromHexList(
            inner_field_container_mixin.persist_bit_map)
        inner_field_container_mixin.state_bit_map = ManageDeactivatableFeaturesAuth.BitMap.fromHexList(
            inner_field_container_mixin.state_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class ManageDeactivatableFeaturesGetInfoResponse


class ManageDeactivatableFeaturesEnableModel(BaseRegisterModel):
    """
    Register Manage Deactivatable Features Enable model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": ManageDeactivatableFeaturesEnableFeaturesRequest,
                "response": ManageDeactivatableFeaturesEnableFeaturesResponse
            },
        }
    # end def _get_data_model
# end class ManageDeactivatableFeaturesEnableModel


class ManageDeactivatableFeaturesEnableFeaturesRequest(SetRegister):
    """
    Write Manage Deactivatable Features 'Enable Features' request
    """
    class FID(SetRegister.FID):
        """
        Fields Identifiers
        """
        ENABLE_BIT_MAP = SetRegister.FID.ADDRESS - 1
        PADDING = ENABLE_BIT_MAP - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Fields Lengths in bits
        """
        ENABLE_BIT_MAP = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.ENABLE_BIT_MAP,
                 LEN.ENABLE_BIT_MAP,
                 title='EnableBitMap',
                 name='enable_bit_map',
                 checks=(CheckHexList(LEN.ENABLE_BIT_MAP // 8), CheckByte(),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SetRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, enable_all_bit=False, enable_gothard=False, enable_compliance=False,
                 enable_manufacturing=False):
        """
        Constructor

        Enable BitMap
            A bit set to 1 specifies that the corresponding features shall be enabled.
            A bit set to 0 specifies that it shall remain unmodified

        :param enable_all_bit: When this bit is set, the 7 least significant bits are ignored and
                                all supported features are enabled.
        :type enable_all_bit: ``int`` or ``bool``
        :param enable_gothard: The Gothard manufacturing protocol is enabled.
        :type enable_gothard: ``int`` or ``bool``
        :param enable_compliance: All compliance HID++ deactivatable features are enabled.
        :type enable_compliance: ``int`` or ``bool``
        :param enable_manufacturing: All manufacturing HID++ deactivatable features are enabled.
        :type enable_manufacturing: ``int`` or ``bool``
        """
        super().__init__(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
            address=Hidpp1Data.Hidpp1RegisterAddress.MANAGE_DEACTIVATABLE_FEATURES_ENABLE_FEATURES)

        self.enable_bit_map = ManageDeactivatableFeaturesAuth.BitMap(
            all_bit=enable_all_bit, gothard=enable_gothard, compliance=enable_compliance,
            manufacturing=enable_manufacturing)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param cls: Target class
        :type cls: ``type``
        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``ManageDeactivatableFeaturesEnableFeaturesRequest``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.enable_bit_map = ManageDeactivatableFeaturesAuth.BitMap.fromHexList(
            inner_field_container_mixin.enable_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class ManageDeactivatableFeaturesEnableFeaturesRequest


class ManageDeactivatableFeaturesEnableFeaturesResponse(SetRegisterResponse):
    """
    Write Manage Deactivatable Features 'Enable Features' response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
            address=Hidpp1Data.Hidpp1RegisterAddress.MANAGE_DEACTIVATABLE_FEATURES_ENABLE_FEATURES)
    # end def __init__
# end class ManageDeactivatableFeaturesEnableFeaturesResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
