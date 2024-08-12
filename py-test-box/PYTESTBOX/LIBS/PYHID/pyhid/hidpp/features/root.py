#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.root

@brief  HID++ 2.0 Root command interface definition

@author christophe.roquebert

@date   2018/12/12
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
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class Root(HidppMessage):
    """
    Root implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x0000
    MAX_FUNCTION_INDEX = 1
    # IRoot feature index hard coded at 0
    FEATURE_INDEX = 0x00

    FEATURE_NOT_FOUND = 0x00

    def __init__(self, device_index):
        """
        Constructor

        @param  device_index           [in] (int)  Device Index
        """
        super(Root, self).__init__()

        self.deviceIndex = device_index
        self.featureIndex = self.FEATURE_INDEX
    # end def __init__
# end class Root


class RootModel(FeatureModel):
    """
    Root feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_FEATURE = 0
        GET_PROTOCOL_VERSION = 1
    # end class INDEX

    @staticmethod
    def _get_data_model():
        """
        Root feature data model
        """
        return {
            "feature_base": Root,
            "versions": {
                RootV0.VERSION: {
                    "main_cls": RootV0,
                    "api": {
                        "functions": {
                            0: {"request": RootGetFeature, "response": RootGetFeatureResponse},
                            1: {"request": RootGetProtocolVersion, "response": RootGetProtocolVersionResponse},
                        }
                    },
                },
                RootV1.VERSION: {
                    "main_cls": RootV1,
                    "api": {
                        "functions": {
                            0: {"request": RootGetFeature, "response": RootGetFeaturev1Response},
                            1: {"request": RootGetProtocolVersion, "response": RootGetProtocolVersionResponse},
                        }
                    },
                },
                RootV2.VERSION: {
                    "main_cls": RootV2,
                    "api": {
                        "functions": {
                            0: {"request": RootGetFeature, "response": RootGetFeaturev2Response},
                            1: {"request": RootGetProtocolVersion, "response": RootGetProtocolVersionResponse},
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class RootModel


class RootFactory(FeatureFactory):
    """
    Root factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        Root object creation from version number

        :param version: Root feature version
        :type version: ``int``
        :return: Root object
        :rtype: ``RootInterface``
        """
        return RootModel.get_main_cls(version)()
    # end def create
# end class RootFactory


class RootInterface(FeatureInterface, ABC):
    """
    Interface to configurable device properties

    Defines required interfaces for configurable device properties classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_feature_cls = None
        self.get_protocol_version_cls = None

        self.get_feature_response_cls = None
        self.get_protocol_version_response_cls = None
    # end def __init__
# end class RootInterface


class RootV0(RootInterface):
    """
    Root
    The root feature allows obtaining information from all other features in the
    device (enumeration) and helps in determining the host software compatibility.

    [0] getFeature(featId) ? featIndex, featType
    [1] getProtocolVersion(0, 0, pingData) ? protocolNum, targetSw, pingData
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`RootInterface.__init__`
        """
        super().__init__()
        self.get_feature_cls = RootModel.get_request_cls(self.VERSION, RootModel.INDEX.GET_FEATURE)
        self.get_feature_response_cls = RootModel.get_response_cls(self.VERSION, RootModel.INDEX.GET_FEATURE)

        self.get_protocol_version_cls = RootModel.get_request_cls(self.VERSION, RootModel.INDEX.GET_PROTOCOL_VERSION)
        self.get_protocol_version_response_cls = RootModel.get_response_cls(self.VERSION,
                                                                            RootModel.INDEX.GET_PROTOCOL_VERSION)
    # end def __init__

    def get_max_function_index(self):
        return RootModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class RootV0


class RootV1(RootV0):
    """
    [0] getFeature(featId) ? featIndex, featType, featVer
    with featType
    obsl  |hidden |  eng  | --- | --- |  ---  |  ---  |  ---
    """
    VERSION = 1
# end class RootV1


class RootV2(RootV1):
    """
    [0] getFeature(featId) ? featIndex, featType, featVer
    with featType
    obsl  |hidden |  eng  | manuf_deact | compl_deact |  ---  |  ---  |  ---
    """
    VERSION = 2
# end class RootV2


class RootGetFeature(Root):
    """
    Root GetFeature implementation class

    Given a desired FeatureID, returns its index in the feature table

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || FeatureID              || 16           ||
    || Padding                || 8            ||
    """
    # Test Constants
    NOT_OBSOLETE = 0
    OBSOLETE = 1
    NOT_HIDDEN = 0
    HIDDEN = 1
    NOT_ENGINEERING_ONLY = 0
    ENGINEERING_ONLY = 1
    # ----

    class FID(Root.FID):
        """
        Field Identifiers
        """
        FEATURE_ID = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(Root.LEN):
        """
        Field Lengths
        """
        FEATURE_ID = 0x10
        PADDING = 0x08
    # end class LEN

    FIELDS = Root.FIELDS + (
        BitField(FID.FEATURE_ID,
                 LEN.FEATURE_ID,
                 title='Feature Id',
                 name='featureId',
                 checks=(CheckHexList(LEN.FEATURE_ID // 8),
                         CheckInt(max_value=0xFFFF),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=Root.DEFAULT.PADDING),
        )

    def __init__(self,
                 deviceIndex,
                 featureId):
        """
        Constructor

        @param  deviceIndex           [in] (int)  Device Index
        @param  featureId             [in] (int)  desired feature Id
        """
        super(RootGetFeature, self).__init__(deviceIndex)

        self.functionIndex = RootGetFeatureResponse.FUNCTION_INDEX
        self.featureId = featureId
    # end def __init__
# end class RootGetFeature


class RootGetFeatureResponseMixin(Root):
    """
    Common part of Root GetFeature version 0 AND 1 class

    Do not instanciate this class directly
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RootGetFeature, )
    FUNCTION_INDEX = 0

    class FID(Root.FID):
        """
        Field Identifiers
        """
        FEATURE_INDEX = 0xFA
        OBSOLETE = 0xF9
        HIDDEN = 0xF8
        ENGINEERING = 0xF7
        RESERVED = 0xF6
    # end class FID

    class LEN(Root.LEN):
        """
        Field Lengths
        """
        FEATURE_INDEX = 0x08
        OBSOLETE = 0x01
        HIDDEN = 0x01
        ENGINEERING = 0x01
        RESERVED = 0x05
    # end class LEN

    class DEFAULT(object):
        """
        Fields Default values
        """
        RESERVED = 0x00
    # end class DEFAULT

    FIELDS = Root.FIELDS + (
              BitField(FID.FEATURE_INDEX,
                       LEN.FEATURE_INDEX,
                       0x00,
                       0x00,
                       title='Feature Index',
                       name='featIndex',
                       checks=(CheckHexList(LEN.FEATURE_INDEX // 8),
                               CheckByte(),),
                       conversions={HexList: Numeral},),
              BitField(FID.OBSOLETE,
                       LEN.OBSOLETE,
                       0x00,
                       0x00,
                       title='Obsolete',
                       name='obsl',
                       checks=(CheckInt(0, pow(2, LEN.OBSOLETE) - 1),)),
              BitField(FID.HIDDEN,
                       LEN.HIDDEN,
                       0x00,
                       0x00,
                       title='Hidden',
                       name='hidden',
                       checks=(CheckInt(0, pow(2, LEN.HIDDEN) - 1),)),
              BitField(FID.ENGINEERING,
                       LEN.ENGINEERING,
                       0x00,
                       0x00,
                       title='Engineering',
                       name='eng',
                       checks=(CheckInt(0, pow(2, LEN.ENGINEERING) - 1),)),
              BitField(FID.RESERVED,
                       LEN.RESERVED,
                       0x00,
                       0x00,
                       title='Reserved',
                       name='reserved',
                       checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                       default_value=DEFAULT.RESERVED),
              )

    def __init__(self,
                 device_index,
                 feature_index):
        """
        Constructor

        @param  device_index           [in] (int)  Device Index
        @param  feature_index          [in] (int)  returned feature Index
        """
        super(RootGetFeatureResponseMixin, self).__init__(device_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.featIndex = feature_index
    # end def __init__
# end class RootGetFeatureResponseMixin


class RootGetFeatureResponse(RootGetFeatureResponseMixin):
    """
    Root GetFeature response implementation class

    Response returning the index in the feature table

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || featIndex              || 8            ||
    || obsl                   || 1            ||
    || hidden                 || 1            ||
    || eng                    || 1            ||
    || Reserved               || 5            ||
    || Padding                || 112          ||
    """
    VERSION = (0, )

    class FID(RootGetFeatureResponseMixin.FID):
        """
        Field Identifiers
        """
        PADDING = 0xF5
    # end class FID

    class LEN(RootGetFeatureResponseMixin.LEN):
        """
        Field Lengths
        """
        PADDING = 0x70
    # end class LEN

    FIELDS = RootGetFeatureResponseMixin.FIELDS + (
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       default_value=Root.DEFAULT.PADDING),
              )
# end class RootGetFeatureResponse


class RootGetFeaturev1Response(RootGetFeatureResponseMixin):
    """
    Root GetFeature response implementation class

    Response returning the index in the feature table

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || featIndex              || 8            ||
    || obsl                   || 1            ||
    || hidden                 || 1            ||
    || eng                    || 1            ||
    || Reserved               || 5            ||
    || FeatVer                || 8            ||
    || Padding                || 104          ||
    """
    VERSION = (1,)

    class FID(RootGetFeatureResponseMixin.FID):
        """
        Field Identifiers
        """
        FEATURE_VERSION = 0xF5
        PADDING = 0xF4

    # end class FID

    class LEN(RootGetFeatureResponseMixin.LEN):
        """
        Field Lengths
        """
        FEATURE_VERSION = 0x08
        PADDING = 0x68

    # end class LEN

    FIELDS = RootGetFeatureResponseMixin.FIELDS + (
                BitField(FID.FEATURE_VERSION,
                         LEN.FEATURE_VERSION,
                         0x00,
                         0x00,
                         title='Feature Version',
                         name='featVer',
                         checks=(CheckHexList(LEN.FEATURE_VERSION // 8),
                                 CheckByte(),)),
                BitField(FID.PADDING,
                         LEN.PADDING,
                         0x00,
                         0x00,
                         title='Padding',
                         name='padding',
                         default_value=Root.DEFAULT.PADDING),
    )

    def __init__(self,
                 device_index,
                 feature_index,
                 feature_version):
        """
        Constructor

        @param  device_index           [in] (int)  Device Index
        @param  feature_version        [in] (int)  returned feature version
        """
        super(RootGetFeaturev1Response, self).__init__(device_index, feature_index)

        self.featVer = feature_version
    # end def __init__
# end class RootGetFeaturev1Response


class RootGetFeaturev2Response(RootGetFeatureResponseMixin):
    """
    Root GetFeature version 2 response implementation class

    Response returning the index in the feature table

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || featureIndex           || 8            ||
    || obsl                   || 1            ||
    || hidden                 || 1            ||
    || eng                    || 1            ||
    || manuf_deact            || 1            ||
    || compl_deact            || 1            ||
    || Reserved               || 3            ||
    || featureVersion         || 8            ||
    || Padding                || 104          ||
    """
    VERSION = (2,)

    class FID(RootGetFeatureResponseMixin.FID):
        """
        Field Identifiers
        """
        MANUF_DEACT = 0xF6
        COMPL_DEACT = 0xF5
        RESERVED = 0xF4
        FEATURE_VERSION = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(RootGetFeatureResponseMixin.LEN):
        """
        Field Lengths
        """
        MANUF_DEACT = 0x01
        COMPL_DEACT = 0x01
        RESERVED = 0x03
        FEATURE_VERSION = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = Root.FIELDS + (
        BitField(FID.FEATURE_INDEX,
                 LEN.FEATURE_INDEX,
                 title='Feature Index',
                 name='featIndex',
                 aliases=('featureIndex',),
                 checks=(CheckHexList(LEN.FEATURE_INDEX // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral},),
        BitField(FID.OBSOLETE,
                 LEN.OBSOLETE,
                 title='Obsolete',
                 name='obsl',
                 aliases=('obsolete',),
                 checks=(CheckInt(0, pow(2, LEN.OBSOLETE) - 1),)),
        BitField(FID.HIDDEN,
                 LEN.HIDDEN,
                 title='Hidden',
                 name='hidden',
                 checks=(CheckInt(0, pow(2, LEN.HIDDEN) - 1),)),
        BitField(FID.ENGINEERING,
                 LEN.ENGINEERING,
                 title='Engineering',
                 name='eng',
                 aliases=('engineering',),
                 checks=(CheckInt(0, pow(2, LEN.ENGINEERING) - 1),)),
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
                 default_value=RootGetFeatureResponseMixin.DEFAULT.RESERVED),
        BitField(FID.FEATURE_VERSION,
                 LEN.FEATURE_VERSION,
                 title='Feature Version',
                 name='featVer',
                 aliases=('featureVersion',),
                 checks=(CheckHexList(LEN.FEATURE_VERSION // 8),
                         CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=Root.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, feature_version, obsolete=False, hidden=False, engineering=False,
                 manuf_deact=False, compl_deact=False):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: The returned feature index
        :type feature_index: ``int``
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
        :param feature_version: The returned feature version
        :type feature_version: ``int``
        """
        super().__init__(device_index, feature_index)

        # parameters initialization
        self.obsolete = obsolete
        self.hidden = hidden
        self.engineering = engineering
        self.manuf_deact = manuf_deact
        self.compl_deact = compl_deact
        self.featVer = feature_version
    # end def __init__
# end class RootGetFeaturev2Response


class RootGetProtocolVersion(Root):
    """
    Root GetFeature implementation class

    Given a desired FeatureID, returns its index in the feature table

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Zero                   || 16           ||
    || PingData               || 8            ||
    """

    class FID(Root.FID):
        """
        Field Identifiers
        """
        ZERO = 0xFA
        PING_DATA = 0xF9
    # end class FID

    class LEN(Root.LEN):
        """
        Field Lengths
        """
        ZERO = 0x10
        PING_DATA = 0x08
    # end class LEN

    class DEFAULT(Root.DEFAULT):
        """
        Fields Default values
        """
        ZERO = 0x00
    # end class DEFAULT

    FIELDS = Root.FIELDS + (
              BitField(FID.ZERO,
                       LEN.ZERO,
                       0x00,
                       0x00,
                       title='Zero',
                       name='zero',
                       default_value=DEFAULT.ZERO),
              BitField(FID.PING_DATA,
                       LEN.PING_DATA,
                       0x00,
                       0x00,
                       title='Ping Data',
                       name='pingData',
                       checks=(CheckHexList(LEN.PING_DATA // 8),
                               CheckByte(),)),
              )

    def __init__(self,
                 deviceIndex,
                 pingData):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  pingData               [in] (int)   Ping Data
        """
        super(RootGetProtocolVersion, self).__init__(deviceIndex)

        self.functionIndex = RootGetProtocolVersionResponse.FUNCTION_INDEX
        self.pingData = pingData
    # end def __init__
# end class RootGetProtocolVersion


class RootGetProtocolVersionResponse(Root):
    """
    Root GetFeature Response implementation class

    Returns protocol number, target SW, and echoes ping data.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || protocolNum            || 8            ||
    || targetSW               || 8            ||
    || PingData               || 8            ||
    || Padding                || 104          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RootGetProtocolVersion,)
    FUNCTION_INDEX = 1
    VERSION = (0, 1, 2,)

    class FID(Root.FID):
        """
        Field Identifiers
        """
        PROTOCOL_NUMBER = 0xFA
        TARGET_SOFTWARE = 0xF9
        PING_DATA = 0xF8
        PADDING = 0xF7
    # end class FID

    class LEN(Root.LEN):
        """
        Field Lengths
        """
        PROTOCOL_NUMBER = 0x08
        TARGET_SOFTWARE = 0x08
        PING_DATA = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = Root.FIELDS + (
              BitField(FID.PROTOCOL_NUMBER,
                       LEN.PROTOCOL_NUMBER,
                       0x00,
                       0x00,
                       title='Protocol Number',
                       name='protocolNum',
                       checks=(CheckHexList(LEN.PROTOCOL_NUMBER // 8),
                               CheckByte(),)),
              BitField(FID.TARGET_SOFTWARE,
                       LEN.TARGET_SOFTWARE,
                       0x00,
                       0x00,
                       title='Target Software',
                       name='targetSw',
                       checks=(CheckHexList(LEN.TARGET_SOFTWARE // 8),
                               CheckByte(),)),
              BitField(FID.PING_DATA,
                       LEN.PING_DATA,
                       0x00,
                       0x00,
                       title='Ping Data',
                       name='pingData',
                       checks=(CheckHexList(LEN.PING_DATA // 8),
                               CheckByte(),)),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       0x00,
                       0x00,
                       title='Padding',
                       name='padding',
                       default_value=Root.DEFAULT.PADDING),
              )

    def __init__(self,
                 device_index,
                 protocol_number,
                 target_software,
                 ping_data):
        """
        Constructor

        @param  device_index           [in] (int)  Device Index
        @param  protocol_number        [in] (int)  Protocol Number
        @param  target_software        [in] (int)  Target Software
        @param  ping_data              [in] (int)  PingData
        """
        super(RootGetProtocolVersionResponse, self).__init__(device_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.protocolNum = protocol_number
        self.targetSw = target_software
        self.pingData = ping_data
    # end def __init__
# end class RootGetProtocolVersionResponse


class FeatureIniConfigInfo(object):
    """
    Define the feature information required by the check_all_features_version test (in 0x0000 test suite)
    """
    def __init__(self, category=None, name=None, version=None, class_name=None, class_import_path=None):
        """
        :param category: feature category - OPTIONAL
        :type category: ``str``
        :param name: feature name - OPTIONAL
        :type name: ``str``
        :param version: feature version - OPTIONAL
        :type version: ``str | int``
        :param class_name: feature class name - OPTIONAL
        :type class_name: ``str``
        :param class_import_path: feature import path for feature class - OPTIONAL
        :type class_import_path: ``str``
        """
        self.category = category
        self.name = name
        self.version = version
        self.class_name = class_name
        self.class_import_path = class_import_path
    # end def __init__

    def __str__(self):
        return f"(category: {self.category}, name: {self.name}, version: {self.version}," \
               f" class_name: {self.class_name}, class_import_path: {self.class_import_path})"
    # end def __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__

    def get_class_name(self):
        """
        Find the right feature class name given the feature name
        """
        # Some special class name handling
        if self.name == "RGB_EFFECTS":
            self.class_name = "RGBEffects"
        elif self.name == "SPECIAL_KEYS_MSE_BUTTONS":
            self.class_name = "SpecialKeysMSEButtons"
        elif self.name == "EQUAD_DJ_DEBUG_INFO":
            self.class_name = "EquadDJDebugInfo"
        elif self.name == "I2C_DIRECT_ACCESS":
            self.class_name = "I2CDirectAccess"
        elif self.name == "LED_TEST":
            self.class_name = "LEDTest"
        elif self.name == "MLX_90393_MULTI_SENSOR":
            self.class_name = "MLX90393MultiSensor"
        elif self.name == "MLX903XX":
            self.class_name = "MLX903xx"
        elif self.name == "PMW3816_AND_PMW3826":
            self.class_name = "PMW3816andPMW3826"
        elif self.name == "RF_TEST":
            self.class_name = "RFTest"
        elif self.name == "SPI_DIRECT_ACCESS":
            self.class_name = "SPIDirectAccess"
        elif self.name == "TOUCHPAD_RAW_XY":
            self.class_name = "TouchpadRawXY"
        elif self.name == "DISABLE_CONTROLS_BY_CIDX":
            self.class_name = "DisableControlsByCIDX"
        else:
            self.class_name = ''.join(word.capitalize() for word in self.name.split('_'))
        # end if
    # end def get_class_name

    def get_class_import_path(self):
        """
        Get the right feature class import path given the feature category and name
        """
        # For legacy path feature handling, ref: PTB/LIBS/PYHID/pyhid/hidpp/features/
        legacy_path_features = ['BatteryUnifiedLevelStatus',
                                'ConfigChange',
                                'DeviceReset',
                                'EnableHidden',
                                'FeatureInfo',
                                'FeatureSet',
                                'HiResWheel',
                                'PerKeyLighting',
                                'Root',
                                'VerticalScrolling']
        if self.class_name in legacy_path_features:
            category_path = ''
        else:
            category_path = self.category.lower() + '.'
        # end if

        self.class_import_path = f"pyhid.hidpp.features.{category_path}{self.class_name.replace('_', '').lower()}"
    # end def get_class_import_path
# end class FeatureIniConfigInfo

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
