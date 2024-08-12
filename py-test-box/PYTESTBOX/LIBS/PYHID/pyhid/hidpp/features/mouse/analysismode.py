#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.mouse.analysismode
:brief: HID++ 2.0 ``AnalysisMode`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:author: Christophe Roquebert <croquebert@logitech.com>
:date   2023/22/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum
from enum import unique

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
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalysisMode(HidppMessage):
    """
    This feature allows to get analysis data that is used for generic analytics.
    """
    FEATURE_ID = 0x2250
    MAX_FUNCTION_INDEX_V0 = 2
    MAX_FUNCTION_INDEX_V1 = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__

    @unique
    class MODE(IntEnum):
        """
        The Analysis modes
        """
        OFF = 0
        ON = 1
    # end class MODE

    class Capabilities(BitFieldContainerMixin):
        """
        Define ``Capabilities`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        reserved                      7
        overflow                      1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            OVERFLOW = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            OVERFLOW = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.OVERFLOW, length=LEN.OVERFLOW,
                     title="Overflow", name="overflow",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.OVERFLOW) - 1),)),
        )
    # end class Capabilities

    class MaxClampedValues(object):
        """
        Define positive and negative maximum clamped value for motion registers
        """
        NEGATIVE_CLAMPED_VALUE = 0x80000000
        POSITIVE_CLAMPED_VALUE = 0x7FFFFFFF
    # end class MaxClampedValues
# end class AnalysisMode


# noinspection DuplicatedCode
class AnalysisModeModel(FeatureModel):
    """
    Define ``AnalysisMode`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_ANALYSIS_MODE = 0
        SET_ANALYSIS_MODE = 1
        GET_ANALYSIS_DATA = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``AnalysisMode`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_ANALYSIS_MODE: {
                    "request": GetAnalysisModeV0,
                    "response": GetAnalysisModeV0Response
                },
                cls.INDEX.SET_ANALYSIS_MODE: {
                    "request": SetAnalysisModeV0,
                    "response": SetAnalysisModeV0Response
                },
                cls.INDEX.GET_ANALYSIS_DATA: {
                    "request": GetAnalysisDataV0,
                    "response": GetAnalysisDataV0Response
                }
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_ANALYSIS_MODE: {
                    "request": GetAnalysisModeV1,
                    "response": GetAnalysisModeV1Response
                },
                cls.INDEX.SET_ANALYSIS_MODE: {
                    "request": SetAnalysisModeV1,
                    "response": SetAnalysisModeV1Response
                },
                cls.INDEX.GET_ANALYSIS_DATA: {
                    "request": GetAnalysisDataV1,
                    "response": GetAnalysisDataV1Response
                }
            }
        }

        return {
            "feature_base": AnalysisMode,
            "versions": {
                AnalysisModeV0.VERSION: {
                    "main_cls": AnalysisModeV0,
                    "api": function_map_v0
                },
                AnalysisModeV1.VERSION: {
                    "main_cls": AnalysisModeV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class AnalysisModeModel


class AnalysisModeFactory(FeatureFactory):
    """
    Get ``AnalysisMode`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``AnalysisMode`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``AnalysisModeInterface``
        """
        return AnalysisModeModel.get_main_cls(version)()
    # end def create
# end class AnalysisModeFactory


class AnalysisModeInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``AnalysisMode``
    """

    def __init__(self):
        # Requests
        self.get_analysis_mode_cls = None
        self.set_analysis_mode_cls = None
        self.get_analysis_data_cls = None

        # Responses
        self.get_analysis_mode_response_cls = None
        self.set_analysis_mode_response_cls = None
        self.get_analysis_data_response_cls = None
    # end def __init__
# end class AnalysisModeInterface


class AnalysisModeV0(AnalysisModeInterface):
    """
    Define ``AnalysisModeV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getAnalysisMode() -> mode

    [1] setAnalysisMode(mode) -> mode

    [2] getAnalysisData() -> data
    """
    VERSION = 0

    def __init__(self):
        # See ``AnalysisMode.__init__``
        super().__init__()
        index = AnalysisModeModel.INDEX

        # Requests
        self.get_analysis_mode_cls = AnalysisModeModel.get_request_cls(
            self.VERSION, index.GET_ANALYSIS_MODE)
        self.set_analysis_mode_cls = AnalysisModeModel.get_request_cls(
            self.VERSION, index.SET_ANALYSIS_MODE)
        self.get_analysis_data_cls = AnalysisModeModel.get_request_cls(
            self.VERSION, index.GET_ANALYSIS_DATA)

        # Responses
        self.get_analysis_mode_response_cls = AnalysisModeModel.get_response_cls(
            self.VERSION, index.GET_ANALYSIS_MODE)
        self.set_analysis_mode_response_cls = AnalysisModeModel.get_response_cls(
            self.VERSION, index.SET_ANALYSIS_MODE)
        self.get_analysis_data_response_cls = AnalysisModeModel.get_response_cls(
            self.VERSION, index.GET_ANALYSIS_DATA)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``AnalysisModeInterface.get_max_function_index``
        return AnalysisModeModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class AnalysisModeV0


class AnalysisModeV1(AnalysisModeV0):
    """
    Define ``AnalysisModeV1`` feature

    This feature provides model and unit specific information for version 1
    """
    VERSION = 1

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``AnalysisModeInterface.get_max_function_index``
        return AnalysisModeModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class AnalysisModeV1


class ShortEmptyPacketDataFormat(AnalysisMode):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetAnalysisData
        - GetAnalysisMode

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(AnalysisMode.FID):
        # See ``AnalysisMode.FID``
        PADDING = AnalysisMode.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(AnalysisMode.LEN):
        # See ``AnalysisMode.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = AnalysisMode.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AnalysisMode.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class AnalysisModePacket(AnalysisMode):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetAnalysisModeResponseV0
        - SetAnalysisModeResponseV0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    mode                          8
    Padding                       120
    ============================  ==========
    """

    class FID(AnalysisMode.FID):
        # See ``AnalysisMode.FID``
        MODE = AnalysisMode.FID.SOFTWARE_ID - 1
        PADDING = MODE - 1
    # end class FID

    class LEN(AnalysisMode.LEN):
        # See ``AnalysisMode.LEN``
        MODE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = AnalysisMode.FIELDS + (
        BitField(fid=FID.MODE, length=LEN.MODE,
                 title="Mode", name="mode",
                 checks=(CheckHexList(LEN.MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AnalysisMode.DEFAULT.PADDING),
    )
# end class AnalysisModePacket


class GetAnalysisModeV0(ShortEmptyPacketDataFormat):
    """
    Define ``GetAnalysisModeV0`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetAnalysisModeV0Response.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetAnalysisModeV0


class GetAnalysisModeV1(GetAnalysisModeV0):
    """
    Define ``GetAnalysisModeV1`` implementation class
    """
    # See ``GetAnalysisModeV0``
# end class GetAnalysisModeV1


class SetAnalysisModeV0(AnalysisMode):
    """
    Define ``SetAnalysisModeV0`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    mode                          8
    Padding                       16
    ============================  ==========
    """

    class FID(AnalysisMode.FID):
        # See ``AnalysisMode.FID``
        MODE = AnalysisMode.FID.SOFTWARE_ID - 1
        PADDING = MODE - 1
    # end class FID

    class LEN(AnalysisMode.LEN):
        # See ``AnalysisMode.LEN``
        MODE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = AnalysisMode.FIELDS + (
        BitField(fid=FID.MODE, length=LEN.MODE,
                 title="Mode", name="mode",
                 checks=(CheckHexList(LEN.MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AnalysisMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param mode: The mode is used to start or stop the analysis mode
        :type mode: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetAnalysisModeV0Response.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.mode = HexList(Numeral(mode, self.LEN.MODE // 8))
    # end def __init__
# end class SetAnalysisModeV0


class SetAnalysisModeV1(SetAnalysisModeV0):
    """
    Define ``SetAnalysisModeV0`` implementation class
    """
    # See ``SetAnalysisModeV0``
# end class SetAnalysisModeV1


class GetAnalysisDataV0(ShortEmptyPacketDataFormat):
    """
    Define ``GetAnalysisDataV0`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetAnalysisDataV0Response.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetAnalysisDataV0


class GetAnalysisDataV1(GetAnalysisDataV0):
    """
    Define ``GetAnalysisDataV1`` implementation class
    """
    # See ``GetAnalysisDataV0``
# end class GetAnalysisDataV1


class GetAnalysisModeV0Response(AnalysisModePacket):
    """
    Define ``GetAnalysisModeV0Response`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAnalysisModeV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param mode: The Current analysis mode
        :type mode: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mode = HexList(Numeral(mode, self.LEN.MODE // 8))
    # end def __init__
# end class GetAnalysisModeV0Response


class GetAnalysisModeV1Response(AnalysisMode):
    """
    Define ``GetAnalysisModeV1Response`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Mode                          8
    Capabilities                  8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAnalysisModeV1,)
    VERSION = (1,)
    FUNCTION_INDEX = 0

    class FID(AnalysisMode.FID):
        # See ``AnalysisMode.FID``
        MODE = AnalysisMode.FID.SOFTWARE_ID - 1
        CAPABILITIES = MODE - 1
        PADDING = CAPABILITIES - 1
    # end class FID

    class LEN(AnalysisMode.LEN):
        # See ``AnalysisMode.LEN``
        MODE = 0x8
        CAPABILITIES = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = AnalysisMode.FIELDS + (
        BitField(fid=FID.MODE, length=LEN.MODE,
                 title="Mode", name="mode",
                 checks=(CheckHexList(LEN.MODE // 8), CheckByte(),)),
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckHexList(LEN.CAPABILITIES // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AnalysisMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mode, overflow, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param mode: The Current analysis mode
        :type mode: ``int`` or ``HexList``
        :param overflow: overflow bit = 0 - Analytics data will wrap around it's maximum/minimum value
            (modular arithmetic), overflow bit = 1 - Analytics data will be saturated (clamped) at it's maximum/minimum
            value. Depends on data format
        :type overflow: ``bool`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mode = HexList(Numeral(mode, self.LEN.MODE // 8))
        self.capabilities = self.Capabilities(overflow=overflow)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetAnalysisModeResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.capabilities = cls.Capabilities.fromHexList(
            inner_field_container_mixin.capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetAnalysisModeV1Response


class SetAnalysisModeV0Response(AnalysisModePacket):
    """
    Define ``SetAnalysisModeV0Response`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetAnalysisModeV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param mode: Echo of request parameters
        :type mode: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mode = HexList(Numeral(mode, self.LEN.MODE // 8))
    # end def __init__
# end class SetAnalysisModeV0Response


class SetAnalysisModeV1Response(SetAnalysisModeV0Response):
    """
    Define ``SetAnalysisModeV1Response`` implementation class
    """
    # See ``SetAnalysisModeV0Response``
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetAnalysisModeV1,)
    VERSION = (1,)
    FUNCTION_INDEX = 1
# end class SetAnalysisModeV1Response


class GetAnalysisDataV0Response(AnalysisMode):
    """
    Define ``GetAnalysisDataV0Response`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    data                          128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAnalysisDataV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(AnalysisMode.FID):
        # See ``AnalysisMode.FID``
        DATA = AnalysisMode.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(AnalysisMode.LEN):
        # See ``AnalysisMode.LEN``
        DATA = 0x80
    # end class LEN

    class DefaultValue(object):
        """
        Define the default values
        """
        DATA = 0x00
    # end class DefaultValue

    FIELDS = AnalysisMode.FIELDS + (
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="Data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
    )

    def __init__(self, device_index, feature_index, data, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param data: Data to be analyzed returned in a product-dependent format
        :type data: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        data_copy = HexList(data.copy())
        data_copy.addPadding(self.LEN.DATA // 8)
        self.data = data_copy
    # end def __init__
# end class GetAnalysisDataV0Response


class GetAnalysisDataV1Response(GetAnalysisDataV0Response):
    """
    Define ``GetAnalysisDataV1Response`` implementation class
    """
    # See ``GetAnalysisDataV0Response``
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAnalysisDataV1,)
    VERSION = (1,)
    FUNCTION_INDEX = 2
# end class GetAnalysisDataV1Response


class AccumulationPacket(BitFieldContainerMixin):
    """
    Data with positive and negative accumulations of the X and Y displacements

    Valid on the Lombock and Herzog mouse project
    """

    class FID(object):
        """
        Field Identifiers
        """
        ACCU_POSITIVE_X = 0xFF
        ACCU_NEGATIVE_X = 0xFE
        ACCU_POSITIVE_Y = 0xFD
        ACCU_NEGATIVE_Y = 0xFC
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        ACCU_POSITIVE_X = 0x20
        ACCU_NEGATIVE_X = 0x20
        ACCU_POSITIVE_Y = 0x20
        ACCU_NEGATIVE_Y = 0x20
    # end class LEN

    class DEFAULT(object):
        """
        Fields Default values
        """
        CLEARED = 0x00000000
    # end class DEFAULT

    FIELDS = (BitField(FID.ACCU_POSITIVE_X,
                       LEN.ACCU_POSITIVE_X,
                       0x00,
                       0x00,
                       title='AccuPositiveX',
                       name='accuPositiveX',
                       default_value=DEFAULT.CLEARED,
                       checks=(CheckHexList(LEN.ACCU_POSITIVE_X // 8),
                               CheckInt(),),
                       conversions={HexList: Numeral},),
              BitField(FID.ACCU_NEGATIVE_X,
                       LEN.ACCU_NEGATIVE_X,
                       0x00,
                       0x00,
                       title='AccuNegativeX',
                       name='accuNegativeX',
                       default_value=DEFAULT.CLEARED,
                       checks=(CheckHexList(LEN.ACCU_NEGATIVE_X // 8),
                               CheckInt(),),
                       conversions={HexList: Numeral}, ),
              BitField(FID.ACCU_POSITIVE_Y,
                       LEN.ACCU_POSITIVE_Y,
                       0x00,
                       0x00,
                       title='AccuPositiveY',
                       name='accuPositiveY',
                       default_value=DEFAULT.CLEARED,
                       checks=(CheckHexList(LEN.ACCU_POSITIVE_Y // 8),
                               CheckInt(),),
                       conversions={HexList: Numeral}, ),
              BitField(FID.ACCU_NEGATIVE_Y,
                       LEN.ACCU_NEGATIVE_Y,
                       0x00,
                       0x00,
                       title='AccuNegativeY',
                       name='accuNegativeY',
                       default_value=DEFAULT.CLEARED,
                       checks=(CheckHexList(LEN.ACCU_NEGATIVE_Y // 8),
                               CheckInt(),),
                       conversions={HexList: Numeral}, ),
              )
# end class AccumulationPacket

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
