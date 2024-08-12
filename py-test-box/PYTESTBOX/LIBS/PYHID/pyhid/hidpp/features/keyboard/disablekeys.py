#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.keyboard.disablekeys
    :brief: HID++ 2.0 Disable Keys command interface definition
    :author: YY Liu
    :date: 2021/12/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckHexList, CheckByte
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableKeys(HidppMessage):
    """
    DisableKeys implementation class
    
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Params                        24
    ============================  ==========
    """
    FEATURE_ID = 0x4521
    MAX_FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class DisableKeys


class DisableKeysModel(FeatureModel):
    """
    DisableKeys feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_CAPABILITIES = 0
        GET_DISABLED_KEYS = 1
        SET_DISABLED_KEYS = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        DisableKeys feature data model
        """
        return {
            "feature_base": DisableKeys,
            "versions": {
                DisableKeysV0.VERSION: {
                    "main_cls": DisableKeysV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {
                                "request": GetCapabilities,
                                "response": GetCapabilitiesResponse
                            },
                            cls.INDEX.GET_DISABLED_KEYS: {
                                "request": GetDisabledKeys,
                                "response": GetDisabledKeysResponse
                            },
                            cls.INDEX.SET_DISABLED_KEYS: {
                                "request": SetDisabledKeys,
                                "response": SetDisabledKeysResponse
                            },
                        }
                    }
                }
            }
        }
    # end def _get_data_model
# end class DisableKeysModel


class DisableKeysFactory(FeatureFactory):
    """
    DisableKeys feature factory creates an object from a given version
    """

    @staticmethod
    def create(version):
        """
        DisableKeys object creation from version number

        :param version: DisableKeys feature version
        :type version: ``int``

        :return: DisableKeys object
        :rtype: ``DisableKeysInterface``
        """
        return DisableKeysModel.get_main_cls(version)()
    # end def create
# end class DisableKeysFactory


class DisableKeysInterface(FeatureInterface, ABC):
    """
    Interface to DisableKeys feature
    Defines required interfaces for DisableKeys classes
    """
    def __init__(self):
        self.get_capabilities_cls = None
        self.get_capabilities_response_cls = None

        self.get_disabled_keys_cls = None
        self.get_disabled_keys_response_cls = None

        self.set_disabled_keys_cls = None
        self.set_disabled_keys_response_cls = None
    # end def __init__
# end class DisableKeysInterface


class DisableKeysV0(DisableKeysInterface):
    """
    DisableKeys
    [0] GetCapabilities() => disableableKeys
    [1] GetDisabledKeys() => disabledKeys
    [2] SetDisableKeys(keysToDisable) => disabledKeys
    """
    VERSION = 0

    def __init__(self):
        super().__init__()
        self.get_capabilities_cls = DisableKeysModel.get_request_cls(
            self.VERSION, DisableKeysModel.INDEX.GET_CAPABILITIES)
        self.get_capabilities_response_cls = DisableKeysModel.get_response_cls(
            self.VERSION, DisableKeysModel.INDEX.GET_CAPABILITIES)
        self.get_disabled_keys_cls = DisableKeysModel.get_request_cls(
            self.VERSION, DisableKeysModel.INDEX.GET_DISABLED_KEYS)
        self.get_disabled_keys_response_cls = DisableKeysModel.get_response_cls(
            self.VERSION, DisableKeysModel.INDEX.GET_DISABLED_KEYS)
        self.set_disabled_keys_cls = DisableKeysModel.get_request_cls(
            self.VERSION, DisableKeysModel.INDEX.SET_DISABLED_KEYS)
        self.set_disabled_keys_response_cls = DisableKeysModel.get_response_cls(
            self.VERSION, DisableKeysModel.INDEX.SET_DISABLED_KEYS)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any: ``DisableKeysInterface.get_max_function_index``
        """
        return DisableKeysModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class DisableKeysV0


class EmptyPacketFormat(DisableKeys):
    """
    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    Padding                         24
    ==============================  ==========
    """

    class FID(DisableKeys.FID):
        # See ``DisableKeys.FID``
        PADDING = DisableKeys.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DisableKeys.LEN):
        # See ``DisableKeys.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = DisableKeys.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title="Padding",
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableKeys.DEFAULT.PADDING),
    )
# end class EmptyPacketFormat


class DisabledKeysPacketFormat(DisableKeys):
    """
    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    DisabledKeys                    8
    Padding                         16
    ==============================  ==========
    """

    class FID(DisableKeys.FID):
        # See ``DisableKeys.FID``
        DISABLED_KEYS = DisableKeys.FID.SOFTWARE_ID - 1
        PADDING = DISABLED_KEYS - 1
    # end class FID

    class LEN(DisableKeys.LEN):
        # See ``DisableKeys.LEN``
        DISABLED_KEYS = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = DisableKeys.FIELDS + (
        BitField(fid=FID.DISABLED_KEYS,
                 length=LEN.DISABLED_KEYS,
                 title="DisabledKeys",
                 name="disabled_keys",
                 checks=(CheckHexList(LEN.DISABLED_KEYS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 title="Padding",
                 name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableKeys.DEFAULT.PADDING),
    )
# end class DisabledKeysPacketFormat


class GetCapabilities(EmptyPacketFormat):
    """
    GetCapabilities implementation class for version 0

    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    ReportID                        8
    DeviceIndex                     8
    FeatureIndex                    8
    FunctionID                      4
    SoftwareID                      4
    Padding                         24
    ==============================  ==========
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetCapabilitiesResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetCapabilities


class GetCapabilitiesResponse(DisableKeys):
    """
    GetCapabilitiesResponse implementation class for version 0

    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    ReportID                        8
    DeviceIndex                     8
    FeatureIndex                    8
    FunctionID                      4
    SoftwareID                      4
    DisableableKeys                 8
    Padding                         16
    ==============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities, )
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(DisableKeys.FID):
        # See ``DisableKeys.FID``
        DISABLEABLE_KEYS = DisableKeys.FID.SOFTWARE_ID - 1
        PADDING = DISABLEABLE_KEYS - 1
    # end class FID

    class LEN(DisableKeys.LEN):
        # See ``DisableKeys.LEN``
        DISABLEABLE_KEYS = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = DisableKeys.FIELDS + (
        BitField(fid=FID.DISABLEABLE_KEYS,
                 length=LEN.DISABLEABLE_KEYS,
                 title="DisableableKeys",
                 name="disableable_keys",
                 checks=(CheckHexList(LEN.DISABLEABLE_KEYS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 title="Padding",
                 name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, disableable_keys, **kwargs):
        """
        :param device_index: device index
        :type device_index: ``int``
        :param feature_index: feature index
        :type feature_index: ``int``
        :param disableable_keys: keys which the SW allows the user to disable
        :type disableable_keys: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         disableable_keys=disableable_keys,
                         functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetCapabilitiesResponse


class GetDisabledKeys(EmptyPacketFormat):
    """
    GetDisabledKeys implementation for version 0

    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    ReportID                        8
    DeviceIndex                     8
    FeatureIndex                    8
    FunctionID                      4
    SoftwareID                      4
    Padding                         24
    ==============================  ==========
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetDisabledKeysResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetDisabledKeys


class GetDisabledKeysResponse(DisabledKeysPacketFormat):
    """
    GetDisabledKeysResponse implementation for version 0

    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    ReportID                        8
    DeviceIndex                     8
    FeatureIndex                    8
    FunctionID                      4
    SoftwareID                      4
    DisabledKeys                    8
    Padding                         16
    ==============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDisabledKeys, )
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, disabled_keys, **kwargs):
        """
        :param device_index: device index
        :type device_index: ``int``
        :param feature_index: feature index
        :type feature_index: ``int``
        :param disabled_keys: keys which the SW has disabled
        :type disabled_keys: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         disableable_keys=disabled_keys,
                         functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetDisabledKeysResponse


class SetDisabledKeys(DisableKeys):
    """
    SetDisabledKeys implementation for version 0

    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    ReportID                        8
    DeviceIndex                     8
    FeatureIndex                    8
    FunctionID                      4
    SoftwareID                      4
    KeysToDisable                   8
    Padding                         16
    ==============================  ==========
    """

    class FID(DisableKeys.FID):
        # See ``DisableKeys.FID``
        KEYS_TO_DISABLE = DisableKeys.FID.SOFTWARE_ID - 1
        PADDING = KEYS_TO_DISABLE - 1
    # end class FID

    class LEN(DisableKeys.FID):
        # See ``DisableKeys.LEN``
        KEYS_TO_DISABLE = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = DisableKeys.FIELDS + (
        BitField(fid=FID.KEYS_TO_DISABLE,
                 length=LEN.KEYS_TO_DISABLE,
                 title="KeysToDisable",
                 name="keys_to_disable",
                 checks=(CheckHexList(LEN.KEYS_TO_DISABLE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 title="Padding",
                 name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableKeys.DEFAULT.PADDING)
    )

    def __init__(self, device_index, feature_index, keys_to_disable, **kwargs):
        """
        :param device_index: device index
        :type device_index: ``int``
        :param feature_index: feature index
        :type feature_index: ``int``
        :param keys_to_disable: keys which the user selects to disable
        :type keys_to_disable: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index,
                         feature_index,
                         keys_to_disable=keys_to_disable,
                         functionIndex=SetDisabledKeysResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class SetDisabledKeys


class SetDisabledKeysResponse(DisabledKeysPacketFormat):
    """
    SetDisabledKeysResponse implementation for version 0

    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    ReportID                        8
    DeviceIndex                     8
    FeatureIndex                    8
    FunctionID                      4
    SoftwareID                      4
    DisabledKeys                    8
    Padding                         16
    ==============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDisabledKeys,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __int__(self, device_index, feature_index, disabled_keys, **kwargs):
        """
        :param device_index: device index
        :type device_index: ``int``
        :param feature_index: feature index
        :type feature_index: ``int``
        :param disabled_keys: keys which the SW has disabled
        :type disabled_keys: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         disabled_keys=disabled_keys,
                         functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class SetDisabledKeysResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
