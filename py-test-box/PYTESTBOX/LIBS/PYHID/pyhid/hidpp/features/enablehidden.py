#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.enablehidden

@brief  HID++ 2.0 Enable Hidden command interface definition

@author christophe.roquebert

@date   2019/03/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------

class EnableHidden(HidppMessage):
    """
    Enable Hidden Features implementation class
    """

    FEATURE_ID = 0x1E00
    MAX_FUNCTION_INDEX = 1

    # Enable Byte values
    DISABLED = 0
    ENABLED = 1

    def __init__(self, device_index, feature_index):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        """
        super(EnableHidden, self).__init__()

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class EnableHidden


class EnableHiddenModel(FeatureModel):
    """
    EnableHidden feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_ENABLE_HIDDEN_FEATURES = 0
        SET_ENABLE_HIDDEN_FEATURES = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        EnableHidden feature data model
        """
        return {
            "feature_base": EnableHidden,
            "versions": {
                EnableHiddenV0.VERSION: {
                    "main_cls": EnableHiddenV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_ENABLE_HIDDEN_FEATURES: {
                                "request": GetEnableHiddenFeatures,
                                "response": GetEnableHiddenFeaturesResponse
                            },
                            cls.INDEX.SET_ENABLE_HIDDEN_FEATURES: {
                                "request": SetEnableHiddenFeatures,
                                "response": SetEnableHiddenFeaturesResponse
                            }
                        }
                    }
                }
            }
        }
# end class EnableHiddenModel


class EnableHiddenFactory(FeatureFactory):
    """
    Get ``EnableHidden`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``EnableHidden`` object from given version number

        :param version: EnableHidden feature version
        :type version: ``int``

        :return: EnableHidden object
        :rtype: ``EnableHiddenInterface``
        """
        return EnableHiddenModel.get_main_cls(version)()
    # end def create
# end class EnableHiddenFactory


class EnableHiddenInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``EnableHidden``
    """
    def __init__(self):
        self.get_enable_hidden_features_cls = None
        self.set_enable_hidden_features_cls = None

        self.get_enable_hidden_features_response_cls = None
        self.set_enable_hidden_features_response_cls = None
    # end def __init__
# end class EnableHiddenInterface


class EnableHiddenV0(EnableHiddenInterface):
    """
    Define ``EnableHiddenV0`` feature
    """
    VERSION = 0

    def __init__(self):
        # See ``EnableHiddenInterface.__init__``
        super().__init__()

        self.get_enable_hidden_features_cls = EnableHiddenModel.get_request_cls(
            self.VERSION, EnableHiddenModel.INDEX.GET_ENABLE_HIDDEN_FEATURES)
        self.set_enable_hidden_features_cls = EnableHiddenModel.get_request_cls(
            self.VERSION, EnableHiddenModel.INDEX.SET_ENABLE_HIDDEN_FEATURES)

        self.get_enable_hidden_features_response_cls = EnableHiddenModel.get_response_cls(
            self.VERSION, EnableHiddenModel.INDEX.GET_ENABLE_HIDDEN_FEATURES)
        self.set_enable_hidden_features_response_cls = EnableHiddenModel.get_response_cls(
            self.VERSION, EnableHiddenModel.INDEX.SET_ENABLE_HIDDEN_FEATURES)
    # end def __init__

    def get_max_function_index(self):
        # See  ``EnableHiddenInterface.get_max_function_index``
        return EnableHiddenModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class EnableHiddenV0


class GetEnableHiddenFeatures(EnableHidden):
    """
    EnableHidden GetEnableHiddenFeatures implementation class

    Request the status of the engineering features accessibility.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(EnableHidden.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(EnableHidden.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = EnableHidden.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=EnableHidden.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        """
        super(GetEnableHiddenFeatures, self).__init__(device_index, feature_index)

        self.functionIndex = GetEnableHiddenFeaturesResponse.FUNCTION_INDEX
    # end def __init__

# end class GetEnableHiddenFeatures


class GetEnableHiddenFeaturesResponse(EnableHidden):
    """
    EnableHidden GetEnableHiddenFeatures response implementation class

    Returns the status of the engineering features accessibility.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    EnableByte                    8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetEnableHiddenFeatures,)
    FUNCTION_INDEX = 0
    VERSION = (0, )

    class FID(EnableHidden.FID):
        """
        Field Identifiers
        """
        ENABLE_BYTE = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(EnableHidden.LEN):
        """
        Field Lengths
        """
        ENABLE_BYTE = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = EnableHidden.FIELDS + (
        BitField(FID.ENABLE_BYTE,
                 LEN.ENABLE_BYTE,
                 0x00,
                 0x00,
                 title='EnableByte',
                 name='enableByte',
                 checks=(CheckHexList(LEN.ENABLE_BYTE // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=EnableHidden.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, enable_byte):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param enable_byte: Engineering Feature Access Byte
        :type enable_byte: ``int``
        """
        super(GetEnableHiddenFeaturesResponse, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.enableByte = enable_byte
    # end def __init__
# end class GetEnableHiddenFeaturesResponse


class SetEnableHiddenFeatures(EnableHidden):
    """
    EnableHidden SetEnableHiddenFeatures implementation class

    Allows enabling/disabling the device's engineering features.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    EnableByte                    8
    Padding                       16
    ============================  ==========
    """
    MSG_TYPE = TYPE.REQUEST
    FUNCTION_INDEX = 1

    class FID(EnableHidden.FID):
        """
        Field Identifiers
        """
        ENABLE_BYTE = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(EnableHidden.LEN):
        """
        Field Lengths
        """
        ENABLE_BYTE = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = EnableHidden.FIELDS + (
        BitField(FID.ENABLE_BYTE,
                 LEN.ENABLE_BYTE,
                 0x00,
                 0x00,
                 title='EnableByte',
                 name='enableByte',
                 checks=(CheckHexList(LEN.ENABLE_BYTE // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=EnableHidden.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, enable_byte):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param enable_byte: Engineering Feature Access Byte
        :type enable_byte: ``int``
        """
        super(SetEnableHiddenFeatures, self).__init__(device_index, feature_index)

        self.functionIndex = SetEnableHiddenFeaturesResponse.FUNCTION_INDEX
        self.enableByte = enable_byte
    # end def __init__
# end class SetEnableHiddenFeatures


class SetEnableHiddenFeaturesResponse(EnableHidden):
    """
    EnableHidden SetEnableHiddenFeatures response implementation class

    Acknowledges the device's engineering features access.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetEnableHiddenFeatures,)
    FUNCTION_INDEX = 1
    VERSION = (0, )

    class FID(EnableHidden.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(EnableHidden.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = EnableHidden.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=EnableHidden.DEFAULT.PADDING),
    )

    def __init__(self,
                 device_index,
                 feature_index):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        """
        super(SetEnableHiddenFeaturesResponse, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetEnableHiddenFeaturesResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
