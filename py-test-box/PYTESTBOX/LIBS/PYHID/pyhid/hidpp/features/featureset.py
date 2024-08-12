#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.featureset

@brief  HID++ 2.0 FeatureSet command interface definition

@author christophe.roquebert

@date   2018/12/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class FeatureSet(HidppMessage):
    """
    FeatureSet implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x0001
    MAX_FUNCTION_INDEX = 1

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  feature Index
        """
        super(FeatureSet, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
# end class FeatureSet


class FeatureSetModel(FeatureModel):
    """
    FeatureSet feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_COUNT = 0
        GET_FEATURE_ID = 1
    # end class

    @staticmethod
    def _get_data_model():
        """
        FeatureSet feature data model
        """
        return {
            "feature_base": FeatureSet,
            "versions": {
                FeatureSetV0.VERSION: {
                    "main_cls": FeatureSetV0,
                    "api": {
                        "functions": {
                            0: {"request": GetCount, "response": GetCountResponse},
                            1: {"request": GetFeatureID, "response": GetFeatureIDResponse},
                        }
                    },
                },
                FeatureSetV1.VERSION: {
                    "main_cls": FeatureSetV1,
                    "api": {
                        "functions": {
                            0: {"request": GetCount, "response": GetCountResponse},
                            1: {"request": GetFeatureID, "response": GetFeatureIDv1Response},
                        }
                    },
                },
                FeatureSetV2.VERSION: {
                    "main_cls": FeatureSetV2,
                    "api": {
                        "functions": {
                            0: {"request": GetCount, "response": GetCountResponse},
                            1: {"request": GetFeatureID, "response": GetFeatureIDv2Response},
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class FeatureSetModel


class FeatureSetFactory(FeatureFactory):
    """
    FeatureSet factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        FeatureSet object creation from version number

        :param version: FeatureSet feature version
        :type version: ``int``
        :return: FeatureSet object
        :rtype: ``FeatureSetInterface``
        """
        return FeatureSetModel.get_main_cls(version)()
    # end def create
# end class FeatureSetFactory


class FeatureSetInterface(FeatureInterface, ABC):
    """
    Interface to configurable device properties

    Defines required interfaces for configurable device properties classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_count_cls = None
        self.get_feature_id_cls = None

        self.get_count_response_cls = None
        self.get_feature_id_response_cls = None
    # end def __init__
# end class FeatureSetInterface


class FeatureSetV0(FeatureSetInterface):
    """
    FeatureSet
    This feature allows the host to enumerate all the features present on a device.

    [0] getCount() ? count
    [1] getFeatureID(featureIndex) ? featureID, featureType
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`FeatureSetInterface.__init__`
        """
        super().__init__()
        self.get_count_cls = FeatureSetModel.get_request_cls(self.VERSION, FeatureSetModel.INDEX.GET_COUNT)
        self.get_count_response_cls = FeatureSetModel.get_response_cls(self.VERSION, FeatureSetModel.INDEX.GET_COUNT)

        self.get_feature_id_cls = FeatureSetModel.get_request_cls(self.VERSION, FeatureSetModel.INDEX.GET_FEATURE_ID)
        self.get_feature_id_response_cls = FeatureSetModel.get_response_cls(self.VERSION,
            FeatureSetModel.INDEX.GET_FEATURE_ID)
    # end def init

    def get_max_function_index(self):
        return FeatureSetModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class FeatureSetV0


class FeatureSetV1(FeatureSetV0):
    """
    [1] getFeatureID(featureIndex) ? featureID, featureType, featureVersion
    with featureType
    obsl  |hidden |  eng  | --- | --- |  ---  |  ---  |  ---
    """
    VERSION = 1
# end class FeatureSetV1


class FeatureSetV2(FeatureSetV1):
    """
    [1] getFeatureID(featureIndex) ? featureID, featureType, featureVersion
    with featureType
    obsl  |hidden |  eng  | manuf_deact | compl_deact |  ---  |  ---  |  ---
    """
    VERSION = 2
# end class FeatureSetV2


class GetCount(FeatureSet):
    """
    FeatureSet GetCount implementation class
    
    Returns the number of features contained in the set, 
    not including the root feature.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(FeatureSet.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(FeatureSet.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = FeatureSet.FIELDS + (
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       default_value=FeatureSet.DEFAULT.PADDING),
              )

    def __init__(self, deviceIndex,
                       featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(GetCount, self).__init__(deviceIndex, featureId)

        self.functionIndex = GetCountResponse.FUNCTION_INDEX
    # end def __init__
# end class GetCount

    
class GetCountResponse(FeatureSet):
    """
    FeatureSet GetCount response implementation class
    
    Response returning the number of features in the set, 
    not including the root feature.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Count                  || 8            ||
    || Padding                || 120          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCount,)
    VERSION = (0, 1, 2,)
    FUNCTION_INDEX = 0

    class FID(FeatureSet.FID):
        """
        Field Identifiers
        """
        COUNT = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(FeatureSet.LEN):
        """
        Field Lengths
        """
        COUNT = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = FeatureSet.FIELDS + (
              BitField(FID.FEATURE_INDEX,
                       LEN.FEATURE_INDEX,
                       0x00,
                       0x00,
                       title='Count',
                       name='count',
                       checks=(CheckHexList(LEN.FEATURE_INDEX // 8),
                               CheckByte(),),
                       conversions={HexList: Numeral},),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8),
                               CheckByte(),),
                       default_value=FeatureSet.DEFAULT.PADDING),
              )

    def __init__(self,
                 deviceIndex,
                 featureId,
                 count):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  count                  [in] (int)  returned Count
        """
        super(GetCountResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.count = count
    # end def __init__
# end class GetCountResponse


class GetFeatureID(FeatureSet):
    """
    FeatureSet GetFeatureID implementation class

    Returns a feature index returns its ID.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || FeatureIndexToGet      || 8            ||
    || Padding                || 16           ||
    """
    GET_FEATURE_ID_FUNCTION_INDEX = 1

    class FID(FeatureSet.FID):
        """
        Field Identifiers
        """
        FEATURE_INDEX = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(FeatureSet.LEN):
        """
        Field Lengths
        """
        FEATURE_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = FeatureSet.FIELDS + (
              BitField(FID.FEATURE_INDEX,
                       LEN.FEATURE_INDEX,
                       0x00,
                       0x00,
                       title='Feature Index To Get',
                       name='feature_index_to_get'),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       default_value=FeatureSet.DEFAULT.PADDING),
              )

    def __init__(self,
                 deviceIndex,
                 featureId,
                 feature_index_to_get):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  feature_index_to_get   [in] (int)  The one based feature index in the feature table.
        """
        super(GetFeatureID, self).__init__(deviceIndex, featureId)

        self.feature_index_to_get = feature_index_to_get
        self.functionIndex = GetFeatureIDResponse.FUNCTION_INDEX
    # end def __init__
# end class GetFeatureID


class GetFeatureIDResponse(FeatureSet):
    """
    FeatureSet GetFeatureID response implementation class

    Response returning a feature ID given its index.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || FeatureID              || 16           ||
    || Obsolete               || 1            ||
    || SW hidden              || 1            ||
    || engineering hidden     || 1            ||
    || Reserved               || 5            ||
    || Padding                || 104          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFeatureID,)
    VERSION = (0, )
    FUNCTION_INDEX = 1

    class FID(FeatureSet.FID):
        """
        Field Identifiers
        """
        FEATURE_ID = 0xFA
        OBSOLETE = 0xF9
        SW_HIDDEN = 0xF8
        ENGINEERING_HIDDEN = 0xF7
        RESERVED = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(FeatureSet.LEN):
        """
        Field Lengths
        """
        FEATURE_ID = 0x10
        OBSOLETE = 0x1
        SW_HIDDEN = 0x1
        ENGINEERING_HIDDEN = 0x1
        RESERVED = 0x5
        PADDING = 0x68
    # end class LEN

    class DEFAULT(FeatureSet.DEFAULT):
        """
        Fields Default values
        """
        RESERVED = 0x00
    # end class DEFAULT

    FIELDS = FeatureSet.FIELDS + (
              BitField(FID.FEATURE_ID,
                       LEN.FEATURE_ID,
                       0x00,
                       0x00,
                       title='FeatureID',
                       name='feature_id',
                       checks=(CheckHexList(LEN.FEATURE_ID // 8),
                               CheckByte(),),),
              BitField(FID.OBSOLETE,
                       LEN.OBSOLETE,
                       0x00,
                       0x00,
                       title='Obsolete',
                       name='obsolete',
                       checks=(CheckInt(0, pow(2, LEN.OBSOLETE) - 1),)),
              BitField(FID.SW_HIDDEN,
                       LEN.SW_HIDDEN,
                       0x00,
                       0x00,
                       title='SW hidden',
                       name='sw_hidden',
                       checks=(CheckInt(0, pow(2, LEN.SW_HIDDEN) - 1),)),
              BitField(FID.ENGINEERING_HIDDEN,
                       LEN.ENGINEERING_HIDDEN,
                       0x00,
                       0x00,
                       title='Engineering hidden',
                       name='engineering_hidden',
                       checks=(CheckInt(0, pow(2, LEN.ENGINEERING_HIDDEN) - 1),)),
              BitField(FID.RESERVED,
                       LEN.RESERVED,
                       0x00,
                       0x00,
                       title='Reserved',
                       name='reserved',
                       checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                       default_value=DEFAULT.RESERVED),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8),
                               CheckByte(),),
                       default_value=FeatureSet.DEFAULT.PADDING),
              )

    def __init__(self,
                 deviceIndex,
                 featureId,
                 feature_id,
                 obsolete,
                 sw_hidden,
                 engineering_hidden):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  feature_id             [in] (int)  The ID of the feature
        @param  obsolete               [in] (int)  1: obsolete feature
                                                   0: active feature
        @param  sw_hidden              [in] (int)  1: SW hidden feature
                                                   0: SW supported  feature
        @param  engineering_hidden     [in] (int)  1: engineering hidden feature
                                                   0: regular feature

        """
        super(GetFeatureIDResponse, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
        self.feature_id = feature_id
        self.obsolete = obsolete
        self.sw_hidden = sw_hidden
        self.engineering_hidden = engineering_hidden
    # end def __init__
# end class GetFeatureIDResponse


class GetFeatureIDv1Response(GetFeatureIDResponse):
    """
    FeatureSet GetFeatureID version 1 response implementation class

    Response returning a feature ID and its version given its index .

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || FeatureID              || 16           ||
    || Obsolete               || 1            ||
    || SW hidden              || 1            ||
    || engineering hidden     || 1            ||
    || Reserved               || 5            ||
    || Feature Version        || 8            ||
    || Padding                || 96           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFeatureID, )
    VERSION = (1, )

    class FID(GetFeatureIDResponse.FID):
        """
        Field Identifiers
        """
        FEATURE_VERSION = 0xF5
        PADDING = 0xF4
    # end class FID

    class LEN(GetFeatureIDResponse.LEN):
        """
        Field Lengths
        """
        FEATURE_VERSION = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = FeatureSet.FIELDS + (
              BitField(FID.FEATURE_ID,
                       LEN.FEATURE_ID,
                       0x00,
                       0x00,
                       title='FeatureID',
                       name='feature_id',
                       checks=(CheckHexList(LEN.FEATURE_ID // 8),
                               CheckByte(),),),
              BitField(FID.OBSOLETE,
                       LEN.OBSOLETE,
                       0x00,
                       0x00,
                       title='Obsolete',
                       name='obsolete',
                       checks=(CheckInt(0, pow(2, LEN.OBSOLETE) - 1),)),
              BitField(FID.SW_HIDDEN,
                       LEN.SW_HIDDEN,
                       0x00,
                       0x00,
                       title='SW hidden',
                       name='sw_hidden',
                       checks=(CheckInt(0, pow(2, LEN.SW_HIDDEN) - 1),)),
              BitField(FID.ENGINEERING_HIDDEN,
                       LEN.ENGINEERING_HIDDEN,
                       0x00,
                       0x00,
                       title='Engineering hidden',
                       name='engineering_hidden',
                       checks=(CheckInt(0, pow(2, LEN.ENGINEERING_HIDDEN) - 1),)),
              BitField(FID.RESERVED,
                       LEN.RESERVED,
                       0x00,
                       0x00,
                       title='Reserved',
                       name='reserved',
                       checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                       default_value=GetFeatureIDResponse.DEFAULT.RESERVED),
              BitField(FID.FEATURE_VERSION,
                       LEN.FEATURE_VERSION,
                       0x00,
                       0x00,
                       title='Feature Version',
                       name='feature_version',
                       checks=(CheckHexList(LEN.FEATURE_VERSION // 8),
                               CheckByte(),),),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8),
                               CheckByte(),),
                       default_value=FeatureSet.DEFAULT.PADDING),
              )

    def __init__(self,
                 deviceIndex,
                 featureId,
                 feature_id,
                 obsolete,
                 sw_hidden,
                 engineering_hidden,
                 feature_version):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        @param  feature_id             [in] (int)  The ID of the feature
        @param  obsolete               [in] (int)  1: obsolete feature
                                                   0: active feature
        @param  sw_hidden              [in] (int)  1: SW hidden feature
                                                   0: SW supported  feature
        @param  engineering_hidden     [in] (int)  1: engineering hidden feature
                                                   0: regular feature
        @param  feature_version        [in] (int)  The feature version
        """
        super(GetFeatureIDv1Response, self).__init__(deviceIndex,
                                                   featureId,
                                                   feature_id,
                                                   obsolete,
                                                   sw_hidden,
                                                   engineering_hidden
                                                   )
        self.feature_version = feature_version
    # end def __init__
# end class GetFeatureIDv1Response


class GetFeatureIDv2Response(GetFeatureIDResponse):
    """
    FeatureSet GetFeatureID version 2 response implementation class

    Response returning a feature ID and its version given its index .

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || FeatureID              || 16           ||
    || Obsolete               || 1            ||
    || SW hidden              || 1            ||
    || engineering hidden     || 1            ||
    || manuf_deact            || 1            ||
    || compl_deact            || 1            ||
    || Reserved               || 3            ||
    || Feature Version        || 8            ||
    || Padding                || 96           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFeatureID, )
    VERSION = (2, )

    class FID(GetFeatureIDResponse.FID):
        """
        Field Identifiers
        """
        MANUF_DEACT = 0xF6
        COMPL_DEACT = 0xF5
        RESERVED = 0xF4
        FEATURE_VERSION = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(GetFeatureIDResponse.LEN):
        """
        Field Lengths
        """
        MANUF_DEACT = 0x01
        COMPL_DEACT = 0x01
        RESERVED = 0x03
        FEATURE_VERSION = 0x08
        PADDING = 0x60
    # end class LEN

    FIELDS = FeatureSet.FIELDS + (
        BitField(FID.FEATURE_ID,
                 LEN.FEATURE_ID,
                 title='FeatureID',
                 name='feature_id',
                 checks=(CheckHexList(LEN.FEATURE_ID // 8),
                         CheckByte(),),),
        BitField(FID.OBSOLETE,
                 LEN.OBSOLETE,
                 title='Obsolete',
                 name='obsolete',
                 aliases=('obsl',),
                 checks=(CheckInt(0, pow(2, LEN.OBSOLETE) - 1),)),
        BitField(FID.SW_HIDDEN,
                 LEN.SW_HIDDEN,
                 title='Hidden',
                 name='hidden',
                 aliases=('sw_hidden',),
                 checks=(CheckInt(0, pow(2, LEN.SW_HIDDEN) - 1),)),
        BitField(FID.ENGINEERING_HIDDEN,
                 LEN.ENGINEERING_HIDDEN,
                 title='Engineering',
                 name='engineering',
                 aliases=('engineering_hidden', 'eng',),
                 checks=(CheckInt(0, pow(2, LEN.ENGINEERING_HIDDEN) - 1),)),
        BitField(FID.MANUF_DEACT,
                 LEN.MANUF_DEACT,
                 title='ManufacturingDeactivatable',
                 name='manuf_deact',
                 aliases=('manufacturing_deactivatable',),
                 checks=(CheckInt(0, pow(2, LEN.MANUF_DEACT) - 1),)),
        BitField(FID.COMPL_DEACT,
                 LEN.COMPL_DEACT,
                 title='ComplianceDeactivatable',
                 name='compl_deact',
                 aliases=('compliance_deactivatable',),
                 checks=(CheckInt(0, pow(2, LEN.COMPL_DEACT) - 1),)),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=GetFeatureIDResponse.DEFAULT.RESERVED),
        BitField(FID.FEATURE_VERSION,
                 LEN.FEATURE_VERSION,
                 title='Feature Version',
                 name='feature_version',
                 checks=(CheckHexList(LEN.FEATURE_VERSION // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=FeatureSet.DEFAULT.PADDING),
        )

    def __init__(self, deviceIndex, featureId, feature_id, feature_version, obsolete=False, hidden=False,
                 engineering=False, manuf_deact=False, compl_deact=False):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param featureId: desired feature Id
        :type featureId: ``int``
        :param feature_id: The ID of the feature
        :type feature_id: ``int``
        :param feature_version: The returned feature version
        :type feature_version: ``int``
        :param obsolete: An obsolete feature is a feature that has been replaced by a newer one.
        :type obsolete: ``bool``
        :param hidden: A SW hidden feature is a feature that should not be known/managed/used by end user
                        configuration SW.
        :type hidden: ``bool``
        :param engineering: A hidden feature that has been disabled for user software.
        :type engineering: ``bool``
        :param manuf_deact: A manufacturing feature that can be deactivated.
        :type manuf_deact: ``bool``
        :param compl_deact: A compliance feature that can be deactivated.
        :type compl_deact: ``bool``
        """
        super().__init__(deviceIndex, featureId, feature_id, obsolete, hidden, engineering)

        # parameters initialization
        self.manuf_deact = manuf_deact
        self.compl_deact = compl_deact
        self.feature_version = feature_version
    # end def __init__
# end class GetFeatureIDv1Response

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
