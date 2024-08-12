#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.managedeactivatablefeaturesauth
    :brief: HID++ 2.0 Manage deactivatable features (based on authentication mechanism) command interface definition
    :author: Martin Cryonnet
    :date: 2020/11/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.docutils import DocUtils
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ManageDeactivatableFeaturesAuth(HidppMessage):
    """
    ManageDeactivatableFeaturesAuth implementation class

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
    FEATURE_ID = 0x1E02
    MAX_FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__

    class BitMap(BitFieldContainerMixin):
        """
            Generic BitMap format for Manage Deactivatable Features (based on authentication mechanism) feature

           Format:

           ============================  ==========
           Name                          Bit count
           ============================  ==========
           AllBit                        1
           Reserved                      4
           Gothard                       1
           ComplHidpp                    1
           ManufHidpp                    1
           ============================  ==========
        """
        class FID:
            """
            Field identifiers
            """
            ALL_BIT = 0x0FF
            RESERVED = ALL_BIT - 1
            GOTHARD = RESERVED - 1
            COMPLIANCE = GOTHARD - 1
            MANUFACTURING = COMPLIANCE - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            ALL_BIT = 1
            RESERVED = 4
            GOTHARD = 1
            COMPLIANCE = 1
            MANUFACTURING = 1
        # end class LEN

        class DEFAULT:
            """
            Field default values
            """
            ALL_BIT = 0
            RESERVED = 0x00
            GOTHARD = 0
            COMPLIANCE = 0
            MANUFACTURING = 0
        # end class DEFAULT

        FIELDS = (
            BitField(FID.ALL_BIT,
                     LEN.ALL_BIT,
                     title='AllBit',
                     name='all_bit',
                     optional=True,
                     default_value=DEFAULT.ALL_BIT,
                     checks=(CheckInt(0, pow(2, LEN.ALL_BIT) - 1),)),
            BitField(FID.RESERVED,
                     LEN.RESERVED,
                     title='Reserved',
                     name='reserved',
                     default_value=DEFAULT.RESERVED,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
            BitField(FID.GOTHARD,
                     LEN.GOTHARD,
                     title='Gothard',
                     name='gothard',
                     aliases=('gotthard',),
                     default_value=DEFAULT.GOTHARD,
                     checks=(CheckInt(0, pow(2, LEN.GOTHARD) - 1),)),
            BitField(FID.COMPLIANCE,
                     LEN.COMPLIANCE,
                     title='Compliance',
                     name='compliance',
                     aliases=('compl_hidpp',),
                     default_value=DEFAULT.COMPLIANCE,
                     checks=(CheckInt(0, pow(2, LEN.COMPLIANCE) - 1),)),
            BitField(FID.MANUFACTURING,
                     LEN.MANUFACTURING,
                     title='Manufacturing',
                     name='manufacturing',
                     aliases=('manuf_hidpp',),
                     default_value=DEFAULT.MANUFACTURING,
                     checks=(CheckInt(0, pow(2, LEN.MANUFACTURING) - 1),)),
        )
    # end class BitMap
# end class ManageDeactivatableFeaturesAuth


class ManageDeactivatableFeaturesAuthModel(FeatureModel):
    """
    ManageDeactivatableFeaturesAuth feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_INFO = 0
        DISABLE_FEATURES = 1
        ENABLE_FEATURES = 2
        GET_REACTIVATION_INFO = 3
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Manage Deactivatable Features (based on authentication mechanism) feature data model
        """
        return {
            "feature_base": ManageDeactivatableFeaturesAuth,
            "versions": {
                ManageDeactivatableFeaturesAuthV0.VERSION: {
                    "main_cls": ManageDeactivatableFeaturesAuthV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_INFO: {"request": GetInfo, "response": GetInfoResponse},
                            cls.INDEX.DISABLE_FEATURES: {"request": DisableFeatures,
                                                         "response": DisableFeaturesResponse},
                            cls.INDEX.ENABLE_FEATURES: {"request": EnableFeatures, "response": EnableFeaturesResponse},
                            cls.INDEX.GET_REACTIVATION_INFO: {"request": GetReactInfo, "response": GetReactInfoResponse}
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class ManageDeactivatableFeaturesAuthModel


class ManageDeactivatableFeaturesAuthFactory(FeatureFactory):
    """
    Manage Deactivatable Features (based on authentication mechanism) factory to create a feature object from a given
    version
    """
    @staticmethod
    def create(version):
        """
        Manage Deactivatable Features (based on authentication mechanism) object creation from version number

        :param version: Manage Deactivatable Features feature version
        :type version: ``int``
        :return: Manage Deactivatable Features (based on authentication mechanism) object
        :rtype: ``ManageDeactivatableFeaturesAuthInterface``
        """
        return ManageDeactivatableFeaturesAuthModel.get_main_cls(version)()
    # end def create
# end class ManageDeactivatableFeaturesAuthFactory


class ManageDeactivatableFeaturesAuthInterface(FeatureInterface, ABC):
    """
    Interface to Manage Deactivatable Features (based on authentication mechanism)

    Defines required interfaces for Manage Deactivatable Features classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_info_cls = None
        self.get_info_response_cls = None

        self.disable_features_cls = None
        self.disable_features_response_cls = None

        self.enable_features_cls = None
        self.enable_features_response_cls = None

        self.get_reactivation_info_cls = None
        self.get_reactivation_info_response_cls = None
    # end def __init__
# end class ManageDeactivatableFeaturesAuthInterface


class ManageDeactivatableFeaturesAuthV0(ManageDeactivatableFeaturesAuthInterface):
    """
    ManageDeactivatableFeatures
    This feature allows to manage deactivatable features, that is:

    - The set of all HID++ features tagged as "manufacturing deactivatable"
    (in the feature-type bit-field readable via Features 0x0000 and 0x0001).
    - The set of all HID++ features tagged as "compliance deactivatable"
    (in the feature-type bit-field readable via Features 0x0000 and 0x0001).
    - Other deactivatable product features, such as manufaturing communication
    protocols (currently only Gothard is supported).

    [0] getInfo() -> supportBitMap, persitBitMap
    [1] disableFeatures(disableBitMap)
    [2] enableFeatures(enableBitMap)
    [3] getReactInfo() -> authFeature
    """
    VERSION = 0

    @DocUtils.copy_doc(ManageDeactivatableFeaturesAuthInterface.__init__)
    def __init__(self):
        """
        See `ManageDeactivatableFeaturesAuthInterface.__init__`
        """
        super().__init__()
        self.get_info_cls = ManageDeactivatableFeaturesAuthModel.get_request_cls(
            self.VERSION, ManageDeactivatableFeaturesAuthModel.INDEX.GET_INFO)
        self.get_info_response_cls = ManageDeactivatableFeaturesAuthModel.get_response_cls(
            self.VERSION, ManageDeactivatableFeaturesAuthModel.INDEX.GET_INFO)

        self.disable_features_cls = ManageDeactivatableFeaturesAuthModel.get_request_cls(
            self.VERSION, ManageDeactivatableFeaturesAuthModel.INDEX.DISABLE_FEATURES)
        self.disable_features_response_cls = ManageDeactivatableFeaturesAuthModel.get_response_cls(
            self.VERSION, ManageDeactivatableFeaturesAuthModel.INDEX.DISABLE_FEATURES)

        self.enable_features_cls = ManageDeactivatableFeaturesAuthModel.get_request_cls(
            self.VERSION, ManageDeactivatableFeaturesAuthModel.INDEX.ENABLE_FEATURES)
        self.enable_features_response_cls = ManageDeactivatableFeaturesAuthModel.get_response_cls(
            self.VERSION, ManageDeactivatableFeaturesAuthModel.INDEX.ENABLE_FEATURES)

        self.get_reactivation_info_cls = ManageDeactivatableFeaturesAuthModel.get_request_cls(
            self.VERSION, ManageDeactivatableFeaturesAuthModel.INDEX.GET_REACTIVATION_INFO)
        self.get_reactivation_info_response_cls = ManageDeactivatableFeaturesAuthModel.get_response_cls(
            self.VERSION, ManageDeactivatableFeaturesAuthModel.INDEX.GET_REACTIVATION_INFO)
    # end def __init__

    def get_max_function_index(self):
        """
        Get max function index
        """
        return ManageDeactivatableFeaturesAuthModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ManageDeactivatableFeaturesAuthV0


class GetInfo(ManageDeactivatableFeaturesAuth):
    """
        ManageDeactivatableFeatures GetInfo implementation class for version 0

        This function allows to get information on deactivatable features.

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
    class FID(ManageDeactivatableFeaturesAuth.FID):
        """
        Field identifiers
        """
        PADDING = ManageDeactivatableFeaturesAuth.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ManageDeactivatableFeaturesAuth.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = ManageDeactivatableFeaturesAuth.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=ManageDeactivatableFeaturesAuth.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetInfoResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetInfo


class GetInfoResponse(ManageDeactivatableFeaturesAuth):
    """
        ManageDeactivatableFeatures GetInfoResponse implementation class for version 0

        This function allows to get information on deactivatable features.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        SupportBitMap                 8
            AllBit                      1
            Reserved                    4
            Gothard                     1
            ComplHidpp                  1
            ManufHidpp                  1
        PersistBitMap                 8
            AllBit                      1
            Reserved                    4
            Gothard                     1
            ComplHidpp                  1
            ManufHidpp                  1
        StateBitMap                   8
            AllBit                      1
            Reserved                    4
            Gothard                     1
            ComplHidpp                  1
            ManufHidpp                  1
        Padding                       112
        ============================  ==========
    """
    REQUEST_LIST = (GetInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0
    MSG_TYPE = TYPE.RESPONSE

    class FID(ManageDeactivatableFeaturesAuth.FID):
        """
        Field identifiers
        """
        SUPPORT_BIT_MAP = ManageDeactivatableFeaturesAuth.FID.SOFTWARE_ID - 1
        PERSIST_BIT_MAP = SUPPORT_BIT_MAP - 1
        STATE_BIT_MAP = PERSIST_BIT_MAP - 1
        PADDING = STATE_BIT_MAP - 1
    # end class FID

    class LEN(ManageDeactivatableFeaturesAuth.LEN):
        """
        Field lengths in bits
        """
        SUPPORT_BIT_MAP = 0x08
        PERSIST_BIT_MAP = 0x08
        STATE_BIT_MAP = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = ManageDeactivatableFeaturesAuth.FIELDS + (
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
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=ManageDeactivatableFeaturesAuth.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, support_all_bit=False, support_gothard=False,
                 support_compliance=False, support_manufacturing=False, persistent_all_bit_activation=False,
                 persistent_gothard_activation=False, persistent_compliance_activation=False,
                 persistent_manufacturing_activation=False, state_all_bit_activation=False,
                 state_gothard_activation=False, state_compliance_activation=False,
                 state_manufacturing_activation=False, **kwargs):
        """
        Constructor

        supportBitMap
            A bit set to 1 specifies that the corresponding feature is supported. A bit set to 0 specifies that a
            deactivation mechanism for the corresponding feature is not provided. The latter may be always active or
            inexistent. The most significant bit shall always be zero.

        persistBitMap
            A bit set to 1 specifies that the activation of the corresponding feature is persistent. A bit set to 0
            specifies that it is volatile. The bits corresponding to unsupported features, as well as the most
            significant bit, shall always be zero.

        stateBitMap
            A bit set to 1 specifies that the corresponding feature is currently active. A bit set to 0 specifies
            that it is inactive. The bits corresponding to unsupported features, as well as the most significant bit,
            shall always be zero.

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
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
        :param state_gothard_activation: Activation state of Gothard features is persistent.
        :type state_gothard_activation: ``int`` or ``bool``
        :param state_compliance_activation: Activation state of all compliance HID++ features is persistent.
        :type state_compliance_activation: ``int`` or ``bool``
        :param state_manufacturing_activation: Activation state of all manufacturing HID++ features is persistent.
        :type state_manufacturing_activation: ``int`` or ``bool``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         reportId=self.DEFAULT.REPORT_ID_LONG, functionIndex=self.FUNCTION_INDEX, **kwargs)
        self.support_bit_map = self.BitMap(all_bit=support_all_bit,
                                           gothard=support_gothard,
                                           compliance=support_compliance,
                                           manufacturing=support_manufacturing)
        self.persist_bit_map = self.BitMap(all_bit=persistent_all_bit_activation,
                                           gothard=persistent_gothard_activation,
                                           compliance=persistent_compliance_activation,
                                           manufacturing=persistent_manufacturing_activation)
        self.state_bit_map = self.BitMap(all_bit=state_all_bit_activation,
                                         gothard=state_gothard_activation,
                                         compliance=state_compliance_activation,
                                         manufacturing=state_manufacturing_activation)
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
        :rtype: ``GetInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.support_bit_map = cls.BitMap.fromHexList(
            inner_field_container_mixin.support_bit_map)
        inner_field_container_mixin.persist_bit_map = cls.BitMap.fromHexList(
            inner_field_container_mixin.persist_bit_map)
        inner_field_container_mixin.state_bit_map = cls.BitMap.fromHexList(
            inner_field_container_mixin.state_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetInfoResponse


class DisableFeatures(ManageDeactivatableFeaturesAuth):
    """
        ManageDeactivatableFeatures DisableFeatures implementation class for version 0

        This function allows to disable deactivatable features.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        DisableBitMap                 8
            AllBit                      1
            Reserved                    4
            Gothard                     1
            ComplHidpp                  1
            ManufHidpp                  1
        Padding                       120
        ============================  ==========
    """
    class FID(ManageDeactivatableFeaturesAuth.FID):
        """
        Field identifiers
        """
        DISABLE_BIT_MAP = ManageDeactivatableFeaturesAuth.FID.SOFTWARE_ID - 1
        PADDING = DISABLE_BIT_MAP - 1
    # end class FID

    class LEN(ManageDeactivatableFeaturesAuth.LEN):
        """
        Field lengths in bits
        """
        DISABLE_BIT_MAP = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = ManageDeactivatableFeaturesAuth.FIELDS + (
        BitField(fid=FID.DISABLE_BIT_MAP,
                 length=LEN.DISABLE_BIT_MAP,
                 title='DisableBitMap',
                 name='disable_bit_map',
                 checks=(CheckHexList(LEN.DISABLE_BIT_MAP // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=ManageDeactivatableFeaturesAuth.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, disable_all_bit=False, disable_gothard=False,
                 disable_compliance=False, disable_manufacturing=False, **kwargs):
        """
        Constructor

        disableBitMap
            A bit set to 1 specifies that the corresponding features shall be disabled. A bit set to 0 specifies that
            it shall remain unmodified. The most significant bit has a special meaning.

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param disable_all_bit: When this bit is set, the 7 least significant bits are ignored and all supported
                                features are disabled.
        :type disable_all_bit: ``int`` or ``bool``
        :param disable_gothard: The Gothard manufacturing protocol features shall be disabled.
        :type disable_gothard: ``int`` or ``bool``
        :param disable_compliance: All compliance HID++ deactivatable features shall be disabled.
        :type disable_compliance: ``int`` or ``bool``
        :param disable_manufacturing: All manufacturing HID++ deactivatable features shall be disabled.
        :type disable_manufacturing: ``int`` or ``bool``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, reportId=self.DEFAULT.REPORT_ID_LONG,
                         functionIndex=DisableFeaturesResponse.FUNCTION_INDEX, **kwargs)
        self.disable_bit_map = self.BitMap(all_bit=disable_all_bit,
                                           gothard=disable_gothard,
                                           compliance=disable_compliance,
                                           manufacturing=disable_manufacturing)
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
        :rtype: ``DisableFeatures``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.disable_bit_map = cls.BitMap.fromHexList(
            inner_field_container_mixin.disable_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class DisableFeatures


class DisableFeaturesResponse(ManageDeactivatableFeaturesAuth):
    """
        ManageDeactivatableFeatures DisableFeaturesResponse implementation class for version 0

        This function allows to disable deactivatable features.

        Format:

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
    REQUEST_LIST = (DisableFeatures,)
    VERSION = (0,)
    FUNCTION_INDEX = 1
    MSG_TYPE = TYPE.RESPONSE

    class FID(ManageDeactivatableFeaturesAuth.FID):
        """
        Field identifiers
        """
        PADDING = ManageDeactivatableFeaturesAuth.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ManageDeactivatableFeaturesAuth.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = ManageDeactivatableFeaturesAuth.FIELDS + (
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=ManageDeactivatableFeaturesAuth.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         reportId=self.DEFAULT.REPORT_ID_LONG, functionIndex=self.FUNCTION_INDEX, **kwargs)
    # end def __init__
# end class DisableFeaturesResponse


class EnableFeatures(ManageDeactivatableFeaturesAuth):
    """
        ManageDeactivatableFeatures EnableFeatures implementation class for version 0

        This function allows to enable deactivatable features.

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        EnableBitMap                  8
            AllBit                      1
            Reserved                    4
            Gothard                     1
            ComplHidpp                  1
            ManufHidpp                  1
        Padding                       120
        ============================  ==========
    """
    class FID(ManageDeactivatableFeaturesAuth.FID):
        """
        Field identifiers
        """
        ENABLE_BIT_MAP = ManageDeactivatableFeaturesAuth.FID.SOFTWARE_ID - 1
        PADDING = ENABLE_BIT_MAP - 1
    # end class FID

    class LEN(ManageDeactivatableFeaturesAuth.LEN):
        """
        Field lengths in bits
        """
        ENABLE_BIT_MAP = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = ManageDeactivatableFeaturesAuth.FIELDS + (
        BitField(fid=FID.ENABLE_BIT_MAP,
                 length=LEN.ENABLE_BIT_MAP,
                 title='EnableBitMap',
                 name='enable_bit_map',
                 checks=(CheckHexList(LEN.ENABLE_BIT_MAP // 8), CheckByte(),), ),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=ManageDeactivatableFeaturesAuth.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, enable_all_bit=False, enable_gothard=False,
                 enable_compliance=False, enable_manufacturing=False, **kwargs):
        """
        Constructor

        enableBitMap
            A bit set to 1 specifies that the corresponding features shall be enabled. A bit set to 0 specifies that
            it shall remain unmodified. The most significant bit has a special meaning. It is allowed to enable a
            feature only if the corresponding account has been authenticated (see function getReactInfo).

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param enable_all_bit: When this bit is set, the 7 least significant bits are ignored and all supported
                                features are enabled.
        :type enable_all_bit: ``int`` or ``bool``
        :param enable_gothard: The Gothard manufacturing protocol shall be enabled.
        :type enable_gothard: ``int`` or ``bool``
        :param enable_compliance: All compliance HID++ deactivatable features shall be enabled.
        :type enable_compliance: ``int`` or ``bool``
        :param enable_manufacturing: All manufacturing HID++ deactivatable features shall be enabled.
        :type enable_manufacturing: ``int`` or ``bool``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, reportId=self.DEFAULT.REPORT_ID_LONG,
                         functionIndex=EnableFeaturesResponse.FUNCTION_INDEX, **kwargs)
        self.enable_bit_map = self.BitMap(all_bit=enable_all_bit,
                                          gothard=enable_gothard,
                                          compliance=enable_compliance,
                                          manufacturing=enable_manufacturing)
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
        :rtype: ``EnableFeatures``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.enable_bit_map = cls.BitMap.fromHexList(
            inner_field_container_mixin.enable_bit_map)
        return inner_field_container_mixin
    # end def fromHexList
# end class EnableFeatures


class EnableFeaturesResponse(ManageDeactivatableFeaturesAuth):
    """
        ManageDeactivatableFeatures EnableFeaturesResponse implementation class for version 0

        This function allows to enable deactivatable features.

        Format:

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
    REQUEST_LIST = (EnableFeatures,)
    VERSION = (0,)
    FUNCTION_INDEX = 2
    MSG_TYPE = TYPE.RESPONSE

    class FID(ManageDeactivatableFeaturesAuth.FID):
        """
        Field identifiers
        """
        PADDING = ManageDeactivatableFeaturesAuth.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ManageDeactivatableFeaturesAuth.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = ManageDeactivatableFeaturesAuth.FIELDS + (
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 default_value=ManageDeactivatableFeaturesAuth.DEFAULT.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         reportId=self.DEFAULT.REPORT_ID_LONG, functionIndex=self.FUNCTION_INDEX, **kwargs)
    # end def __init__
# end class EnableFeaturesResponse


class GetReactInfo(ManageDeactivatableFeaturesAuth):
    """
        ManageDeactivatableFeatures GetReactInfo implementation class for version 0

        This function provides the information whether re-activation is possible and which feature shall be used for
        this purpose.

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
    class FID(ManageDeactivatableFeaturesAuth.FID):
        """
        Field identifiers
        """
        PADDING = ManageDeactivatableFeaturesAuth.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ManageDeactivatableFeaturesAuth.LEN):
        """
        Field lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = ManageDeactivatableFeaturesAuth.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=ManageDeactivatableFeaturesAuth.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetReactInfoResponse.FUNCTION_INDEX, **kwargs)
    # end def __init__
# end class GetReactInfo


class GetReactInfoResponse(ManageDeactivatableFeaturesAuth):
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
    FUNCTION_INDEX = 3
    MSG_TYPE = TYPE.RESPONSE

    class FID(ManageDeactivatableFeaturesAuth.FID):
        """
        Field identifiers
        """
        AUTH_FEATURE = ManageDeactivatableFeaturesAuth.FID.SOFTWARE_ID - 1
        PADDING = AUTH_FEATURE - 1
    # end class FID

    class LEN(ManageDeactivatableFeaturesAuth.LEN):
        """
        Field lengths in bits
        """
        AUTH_FEATURE = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = ManageDeactivatableFeaturesAuth.FIELDS + (
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
            default_value=ManageDeactivatableFeaturesAuth.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, auth_feature=0x0000, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param auth_feature: When set to zero, feature (re-)activation is not supported. Otherwise, this field is the
                             identifier of the HID++ feature used for authentication.
        :type auth_feature: ``int`` or ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         reportId=self.DEFAULT.REPORT_ID_LONG, functionIndex=self.FUNCTION_INDEX,
                         auth_feature=auth_feature, **kwargs)
    # end def __init__
# end class GetReactInfoResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
