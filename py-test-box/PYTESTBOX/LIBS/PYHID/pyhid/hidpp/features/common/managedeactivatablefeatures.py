#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.managedeactivatablefeatures
    :brief: HID++ 2.0 Manage deactivatable features command interface definition
    :author: Christophe Roquebert
    :date: 2020/06/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ManageDeactivatableFeatures(HidppMessage):
    """
    ManageDeactivatableFeatures implementation class

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
    FEATURE_ID = 0x1E01
    MAX_FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class ManageDeactivatableFeatures


class ManageDeactivatableFeaturesModel(FeatureModel):
    """
    ManageDeactivatableFeatures feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_COUNTERS = 0
        SET_COUNTERS = 1
        GET_REACT_INFO = 2
    # end class

    @classmethod
    def _get_data_model(cls):
        """
        Manage Deactivatable Features feature data model
        """
        return {
            "feature_base": ManageDeactivatableFeatures,
            "versions": {
                ManageDeactivatableFeaturesV0.VERSION: {
                    "main_cls": ManageDeactivatableFeaturesV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COUNTERS: {"request": GetCounters, "response": GetCountersResponse},
                            cls.INDEX.SET_COUNTERS: {"request": SetCounters, "response": SetCountersResponse},
                            cls.INDEX.GET_REACT_INFO: {"request": GetReactInfo, "response": GetReactInfoResponse}
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class ManageDeactivatableFeaturesModel


class ManageDeactivatableFeaturesFactory(FeatureFactory):
    """
    Manage Deactivatable Features factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        Manage Deactivatable Features object creation from version number

        :param version: Manage Deactivatable Features feature version
        :type version: ``int``
        :return: Manage Deactivatable Features object
        :rtype: ``ManageDeactivatableFeaturesInterface``
        """
        return ManageDeactivatableFeaturesModel.get_main_cls(version)()
    # end def create
# end class ManageDeactivatableFeaturesFactory


class ManageDeactivatableFeaturesInterface(FeatureInterface, ABC):
    """
    Interface to Manage Deactivatable Features

    Defines required interfaces for Manage Deactivatable Features classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_counters_cls = None
        self.get_counters_response_cls = None

        self.set_counters_cls = None
        self.set_counters_response_cls = None

        self.get_react_info_cls = None
        self.get_react_info_response_cls = None
    # end def __init__
# end class ManageDeactivatableFeaturesInterface


class ManageDeactivatableFeaturesV0(ManageDeactivatableFeaturesInterface):
    """
    ManageDeactivatableFeatures
    This feature allows to manage deactivatable features, that is:

    - The set of all HID++ features tagged as "manufacturing deactivatable"
    (in the feature-type bit-field readable via Features 0x0000 and 0x0001).
    - The set of all HID++ features tagged as "compliance deactivatable"
    (in the feature-type bit-field readable via Features 0x0000 and 0x0001).
    - Other deactivatable product features, such as manufaturing communication
    protocols (currently only Gothard is supported).

    [0] getCounters() -> supportBitMap, manufHidppCounter, complHidppCounter, gothardCounter
    [1] setCounters(setBitMap, manufHidppCounter, complHidppCounter, gothardCounter)
    [2] getReactInfo() -> authFeature
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`ManageDeactivatableFeaturesInterface.__init__`
        """
        super().__init__()
        self.get_counters_cls = ManageDeactivatableFeaturesModel.get_request_cls(
            self.VERSION, ManageDeactivatableFeaturesModel.INDEX.GET_COUNTERS)
        self.get_counters_response_cls = ManageDeactivatableFeaturesModel.get_response_cls(
            self.VERSION, ManageDeactivatableFeaturesModel.INDEX.GET_COUNTERS)

        self.set_counters_cls = ManageDeactivatableFeaturesModel.get_request_cls(
            self.VERSION, ManageDeactivatableFeaturesModel.INDEX.SET_COUNTERS)
        self.set_counters_response_cls = ManageDeactivatableFeaturesModel.get_response_cls(
            self.VERSION, ManageDeactivatableFeaturesModel.INDEX.SET_COUNTERS)

        self.get_react_info_cls = ManageDeactivatableFeaturesModel.get_request_cls(
            self.VERSION, ManageDeactivatableFeaturesModel.INDEX.GET_REACT_INFO)
        self.get_react_info_response_cls = ManageDeactivatableFeaturesModel.get_response_cls(
            self.VERSION, ManageDeactivatableFeaturesModel.INDEX.GET_REACT_INFO)
    # end def __init__

    def get_max_function_index(self):
        """
        Get max function index
        """
        return ManageDeactivatableFeaturesModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ManageDeactivatableFeaturesV0


class GetCounters(ManageDeactivatableFeatures):
    """
    ManageDeactivatableFeatures GetCounters implementation class for version 0

    This function allows to read the connection counters.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       24
    ============================  ==========
    """

    class FID(ManageDeactivatableFeatures.FID):
        """
        Field identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(ManageDeactivatableFeatures.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = ManageDeactivatableFeatures.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=ManageDeactivatableFeatures.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetCountersResponse.FUNCTION_INDEX
    # end def __init__
# end class GetCounters


class ManageDeactivatableFeaturesMixin(ManageDeactivatableFeatures):
    """
        ManageDeactivatableFeatures Get/SetCounters mixin implementation class for version 0

       Format:

       ============================  ==========
       Name                          Bit count
       ============================  ==========
       ReportID                      8
       DeviceIndex                   8
       FeatureIndex                  8
       FunctionID                    4
       SoftwareID                    4
       AllBit                        1
       SupportBitMapReserved         4
       Gothard                       1
       ComplHidpp                    1
       ManufHidpp                    1
       ManufHidppCounter             8
       ComplHidppCounter             8
       GothardCounter                8
       Padding                       96
       ============================  ==========
    """

    class FID(ManageDeactivatableFeatures.FID):
        """
        Field Identifiers
        """
        ALL_BIT = 0xFA
        SUPPORT_BITMAP_RESERVED = 0xF9
        GOTHARD = 0xF8
        COMPL_HIDPP = 0xF7
        MANUF_HIDPP = 0xF6
        MANUF_HIDPP_COUNTER = 0xF5
        COMPL_HIDPP_COUNTER = 0xF4
        GOTHARD_COUNTER = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(ManageDeactivatableFeatures.LEN):
        """
        Fields Lengths
        """
        ALL_BIT = 0x01
        SUPPORT_BITMAP_RESERVED = 0x04
        GOTHARD = 0x01
        COMPL_HIDPP = 0x01
        MANUF_HIDPP = 0x01
        MANUF_HIDPP_COUNTER = 0x08
        COMPL_HIDPP_COUNTER = 0x08
        GOTHARD_COUNTER = 0x08
        PADDING = 0x60
    # end class LEN

    class DEFAULT(ManageDeactivatableFeatures.DEFAULT):
        """
        Fields default values
        """
        ALL_BIT = 0
        SUPPORT_BITMAP_RESERVED = 0x00
    # end class DEFAULT

    FIELDS = ManageDeactivatableFeatures.FIELDS + (
        BitField(FID.ALL_BIT,
                 LEN.ALL_BIT,
                 title='AllBit',
                 name='all_bit',
                 default_value=DEFAULT.ALL_BIT,
                 checks=(CheckInt(max_value=(1 << LEN.ALL_BIT) - 1),)),
        BitField(FID.SUPPORT_BITMAP_RESERVED,
                 LEN.SUPPORT_BITMAP_RESERVED,
                 title='SupportBitMapReserved',
                 name='support_bitmap_reserved',
                 default_value=DEFAULT.SUPPORT_BITMAP_RESERVED,
                 checks=(CheckInt(max_value=(1 << LEN.SUPPORT_BITMAP_RESERVED) - 1),)),
        BitField(FID.GOTHARD,
                 LEN.GOTHARD,
                 title='Gothard',
                 name='gothard',
                 checks=(CheckInt(max_value=(1 << LEN.GOTHARD) - 1),)),
        BitField(FID.COMPL_HIDPP,
                 LEN.COMPL_HIDPP,
                 title='ComplHidpp',
                 name='compl_hidpp',
                 checks=(CheckInt(max_value=(1 << LEN.COMPL_HIDPP) - 1),)),
        BitField(FID.MANUF_HIDPP,
                 LEN.MANUF_HIDPP,
                 title='ManufHidpp',
                 name='manuf_hidpp',
                 checks=(CheckInt(max_value=(1 << LEN.MANUF_HIDPP) - 1),)),
        BitField(FID.MANUF_HIDPP_COUNTER,
                 LEN.MANUF_HIDPP_COUNTER,
                 title='ManufHidppCounter',
                 name='manuf_hidpp_counter',
                 checks=(CheckHexList(LEN.MANUF_HIDPP_COUNTER // 8), CheckByte(), ),),
        BitField(FID.COMPL_HIDPP_COUNTER,
                 LEN.COMPL_HIDPP_COUNTER,
                 title='ComplHidppCounter',
                 name='compl_hidpp_counter',
                 checks=(CheckHexList(LEN.COMPL_HIDPP_COUNTER // 8), CheckByte(), ),),
        BitField(FID.GOTHARD_COUNTER,
                 LEN.GOTHARD_COUNTER,
                 title='GothardCounter',
                 name='gothard_counter',
                 checks=(CheckHexList(LEN.GOTHARD_COUNTER // 8), CheckByte(), ),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(length=LEN.PADDING // 8), CheckByte(),),
                 default_value=ManageDeactivatableFeatures.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, all_bit=False, gothard=False, compl_hidpp=False, manuf_hidpp=False,
                 manuf_hidpp_counter=0xFF, compl_hidpp_counter=0xFF, gothard_counter=0xFF, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param all_bit: Ignore other bits and set all supported counters
        :type all_bit: ``bool``
        :param gothard: Flag for Gothard deactivation
        :rtype: ``bool``
        :param compl_hidpp: Flag for all compliance HID++ deactivatable features
        :rtype: ``bool``
        :param manuf_hidpp: Flag for all manufacturing HID++ deactivatable features
        :rtype: ``bool``
        :param manuf_hidpp_counter: Connection counter for manufacturing HID++ deactivatable features
        :rtype: ``int``
        :param compl_hidpp_counter: Connection counter for compliance HID++ deactivatable features
        :rtype: ``int``
        :param gothard_counter: Connection counter for Gothard manufacturing protocol
        :rtype: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        # Parameters initialization
        self.all_bit = all_bit
        self.gothard = gothard
        self.compl_hidpp = compl_hidpp
        self.manuf_hidpp = manuf_hidpp
        self.manuf_hidpp_counter = manuf_hidpp_counter
        self.compl_hidpp_counter = compl_hidpp_counter
        self.gothard_counter = gothard_counter
    # end def __init__
# end class ManageDeactivatableFeaturesMixin


class GetCountersResponse(ManageDeactivatableFeaturesMixin):
    """
        ManageDeactivatableFeatures GetCounters response implementation class for version 0

        This function allows to read the connection counters.
    """
    REQUEST_LIST = (GetCounters,)
    VERSION = (0,)
    FUNCTION_INDEX = 0
    MSG_TYPE = TYPE.RESPONSE

    def __init__(self, device_index, feature_index, all_bit=False, gothard=False, compl_hidpp=False, manuf_hidpp=False,
                 manuf_hidpp_counter=0xFF, compl_hidpp_counter=0xFF, gothard_counter=0xFF, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, all_bit, gothard, compl_hidpp, manuf_hidpp,
                         manuf_hidpp_counter, compl_hidpp_counter, gothard_counter, **kwargs)
        self.reportId = self.DEFAULT.REPORT_ID_LONG
        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class GetCountersResponse


class SetCounters(ManageDeactivatableFeaturesMixin):
    """
       ManageDeactivatableFeatures SetCounters implementation class for version 0

        This function allows to write the connection counters.
    """
    def __init__(self, device_index, feature_index, all_bit=False, gothard=False, compl_hidpp=False,
                 manuf_hidpp=False, manuf_hidpp_counter=0xFF, compl_hidpp_counter=0xFF, gothard_counter=0xFF, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, all_bit, gothard, compl_hidpp, manuf_hidpp,
                         manuf_hidpp_counter, compl_hidpp_counter, gothard_counter, **kwargs)

        self.functionIndex = SetCountersResponse.FUNCTION_INDEX
        self.reportId = self.DEFAULT.REPORT_ID_LONG
    # end def __init__
# end class SetCounters


class SetCountersResponse(ManageDeactivatableFeatures):
    """
        ManageDeactivatableFeatures SetCounters response implementation class for version 0

        This function allows to write the connection counters.Format:

       ============================  ==========
       Name                          Bit count
       ============================  ==========
       ReportID                      8
       DeviceIndex                   8
       FeatureIndex                  8
       FunctionID                    4
       SoftwareID                    4
       Padding                       128
       ============================  ==========
    """

    REQUEST_LIST = (SetCounters,)
    VERSION = (0,)
    FUNCTION_INDEX = 1
    MSG_TYPE = TYPE.RESPONSE

    class FID(ManageDeactivatableFeatures.FID):
        """
        Field identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(ManageDeactivatableFeatures.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = ManageDeactivatableFeatures.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=ManageDeactivatableFeatures.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.reportId = self.DEFAULT.REPORT_ID_LONG
        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetCountersResponse


class GetReactInfo(ManageDeactivatableFeatures):
    """
    ManageDeactivatableFeatures GetReactInfo implementation class for version 0

    This function provides the information whether re-activation is possible and which feature shall be used for this
    purpose.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       24
    ============================  ==========
    """
    class FID(ManageDeactivatableFeatures.FID):
        """
        Field identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(ManageDeactivatableFeatures.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = ManageDeactivatableFeatures.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=ManageDeactivatableFeatures.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        self.functionIndex = GetReactInfoResponse.FUNCTION_INDEX
    # end def __init__
# end class GetReactInfo


class GetReactInfoResponse(ManageDeactivatableFeatures):
    """
    ManageDeactivatableFeatures GetReactInfo response implementation class for version 0

    This function provides the information whether re-activation is possible and which feature shall be used for this
    purpose.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    authFeature                   16
    Reserved                      112
    ============================  ==========
    """
    REQUEST_LIST = (GetReactInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 2
    MSG_TYPE = TYPE.RESPONSE

    class FID(ManageDeactivatableFeatures.FID):
        """
        Field identifiers
        """
        AUTH_FEATURE = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(ManageDeactivatableFeatures.LEN):
        """
        Field lengths in bits
        """
        AUTH_FEATURE = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = ManageDeactivatableFeatures.FIELDS + (
        BitField(
            fid=FID.AUTH_FEATURE,
            length=LEN.AUTH_FEATURE,
            title='AuthFeature',
            name='auth_feature',
            checks=(CheckHexList(LEN.AUTH_FEATURE // 8), CheckInt(0, pow(2, LEN.AUTH_FEATURE) - 1)),
        ),
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=ManageDeactivatableFeatures.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, auth_feature=0x0000, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.reportId = self.DEFAULT.REPORT_ID_LONG
        self.functionIndex = self.FUNCTION_INDEX
        self.auth_feature = auth_feature
    # end def __init__
# end class GetReactInfoResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
