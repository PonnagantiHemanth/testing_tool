#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.gaming.gaminggkeys
:brief: HID++ 2.0 ``GamingGKeys`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2023/11/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
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
class GamingGKeys(HidppMessage):
    """
    Define Gaming G Keys implementation
    """
    FEATURE_ID = 0x8010
    MAX_FUNCTION_INDEX_V0 = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class GamingGKeys


# noinspection DuplicatedCode
class GamingGKeysModel(FeatureModel):
    """
    Define ``GamingGKeys`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GETCOUNT = 0
        GETPHYSICALLAYOUT = 1
        ENABLESOFTWARECONTROL = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``GamingGKeys`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GETCOUNT: {
                    "request": GetCount,
                    "response": GetCountResponse
                },
                cls.INDEX.GETPHYSICALLAYOUT: {
                    "request": GetPhysicalLayout,
                    "response": GetPhysicalLayoutResponse
                },
                cls.INDEX.ENABLESOFTWARECONTROL: {
                    "request": EnableSoftwareControl,
                    "response": EnableSoftwareControlResponse
                }
            }
        }

        return {
            "feature_base": GamingGKeys,
            "versions": {
                GamingGKeysV0.VERSION: {
                    "main_cls": GamingGKeysV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class GamingGKeysModel


class GamingGKeysFactory(FeatureFactory):
    """
    Get ``GamingGKeys`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``GamingGKeys`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``GamingGKeysInterface``
        """
        return GamingGKeysModel.get_main_cls(version)()
    # end def create
# end class GamingGKeysFactory


class GamingGKeysInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``GamingGKeys``
    """

    def __init__(self):
        # Requests
        self.get_count_cls = None
        self.get_physical_layout_cls = None
        self.enable_software_control_cls = None

        # Responses
        self.get_count_response_cls = None
        self.get_physical_layout_response_cls = None
        self.enable_software_control_response_cls = None
    # end def __init__
# end class GamingGKeysInterface


class GamingGKeysV0(GamingGKeysInterface):
    """
    Define ``GamingGKeysV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCount() -> nbbuttons

    [1] getPhysicalLayout() -> gkeylayout

    [2] enableSoftwareControl(enable) -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``GamingGKeys.__init__``
        super().__init__()
        index = GamingGKeysModel.INDEX

        # Requests
        self.get_count_cls = GamingGKeysModel.get_request_cls(
            self.VERSION, index.GETCOUNT)
        self.get_physical_layout_cls = GamingGKeysModel.get_request_cls(
            self.VERSION, index.GETPHYSICALLAYOUT)
        self.enable_software_control_cls = GamingGKeysModel.get_request_cls(
            self.VERSION, index.ENABLESOFTWARECONTROL)

        # Responses
        self.get_count_response_cls = GamingGKeysModel.get_response_cls(
            self.VERSION, index.GETCOUNT)
        self.get_physical_layout_response_cls = GamingGKeysModel.get_response_cls(
            self.VERSION, index.GETPHYSICALLAYOUT)
        self.enable_software_control_response_cls = GamingGKeysModel.get_response_cls(
            self.VERSION, index.ENABLESOFTWARECONTROL)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``GamingGKeysInterface.get_max_function_index``
        return GamingGKeysModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class GamingGKeysV0


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(GamingGKeys):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCount
        - GetPhysicalLayout

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(GamingGKeys.FID):
        # See ``GamingGKeys.FID``
        PADDING = GamingGKeys.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(GamingGKeys.LEN):
        # See ``GamingGKeys.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = GamingGKeys.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=GamingGKeys.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(GamingGKeys):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - EnableSoftwareControlResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(GamingGKeys.FID):
        # See ``GamingGKeys.FID``
        PADDING = GamingGKeys.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(GamingGKeys.LEN):
        # See ``GamingGKeys.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = GamingGKeys.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=GamingGKeys.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class GetCount(ShortEmptyPacketDataFormat):
    """
    Define ``GetCount`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetCountResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCount


class GetPhysicalLayout(ShortEmptyPacketDataFormat):
    """
    Define ``GetPhysicalLayout`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetPhysicalLayoutResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetPhysicalLayout


class EnableSoftwareControl(GamingGKeys):
    """
    Define ``EnableSoftwareControl`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    enable                        8
    Padding                       16
    ============================  ==========
    """

    class FID(GamingGKeys.FID):
        # See ``GamingGKeys.FID``
        ENABLE = GamingGKeys.FID.SOFTWARE_ID - 1
        PADDING = ENABLE - 1
    # end class FID

    class LEN(GamingGKeys.LEN):
        # See ``GamingGKeys.LEN``
        ENABLE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = GamingGKeys.FIELDS + (
        BitField(fid=FID.ENABLE, length=LEN.ENABLE,
                 title="Enable", name="enable",
                 checks=(CheckHexList(LEN.ENABLE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=GamingGKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, enable, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param enable: enable
        :type enable: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=EnableSoftwareControlResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.enable = HexList(Numeral(enable, self.LEN.ENABLE // 8))
    # end def __init__
# end class EnableSoftwareControl


class GetCountResponse(GamingGKeys):
    """
    Define ``GetCountResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    nbButtons                     8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCount,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(GamingGKeys.FID):
        # See ``GamingGKeys.FID``
        NBBUTTONS = GamingGKeys.FID.SOFTWARE_ID - 1
        PADDING = NBBUTTONS - 1
    # end class FID

    class LEN(GamingGKeys.LEN):
        # See ``GamingGKeys.LEN``
        NBBUTTONS = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = GamingGKeys.FIELDS + (
        BitField(fid=FID.NBBUTTONS, length=LEN.NBBUTTONS,
                 title="Nbbuttons", name="nbbuttons",
                 checks=(CheckHexList(LEN.NBBUTTONS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=GamingGKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, nbbuttons, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param nbbuttons: nbButtons
        :type nbbuttons: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.nbbuttons = HexList(Numeral(nbbuttons, self.LEN.NBBUTTONS // 8))
    # end def __init__
# end class GetCountResponse


class GetPhysicalLayoutResponse(GamingGKeys):
    """
    Define ``GetPhysicalLayoutResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    gkeyLayout                    8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPhysicalLayout,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(GamingGKeys.FID):
        # See ``GamingGKeys.FID``
        GKEYLAYOUT = GamingGKeys.FID.SOFTWARE_ID - 1
        PADDING = GKEYLAYOUT - 1
    # end class FID

    class LEN(GamingGKeys.LEN):
        # See ``GamingGKeys.LEN``
        GKEYLAYOUT = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = GamingGKeys.FIELDS + (
        BitField(fid=FID.GKEYLAYOUT, length=LEN.GKEYLAYOUT,
                 title="Gkeylayout", name="gkeylayout",
                 checks=(CheckHexList(LEN.GKEYLAYOUT // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=GamingGKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, gkeylayout, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param gkeylayout: gkeyLayout
        :type gkeylayout: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.gkeylayout = HexList(Numeral(gkeylayout, self.LEN.GKEYLAYOUT // 8))
    # end def __init__
# end class GetPhysicalLayoutResponse


class EnableSoftwareControlResponse(LongEmptyPacketDataFormat):
    """
    Define ``EnableSoftwareControlResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (EnableSoftwareControl,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class EnableSoftwareControlResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
