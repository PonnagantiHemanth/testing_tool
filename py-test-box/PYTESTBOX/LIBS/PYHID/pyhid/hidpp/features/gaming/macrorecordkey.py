#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.gaming.macrorecordkey
:brief: HID++ 2.0 ``MacroRecordkey`` command interface definition
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
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
class MacroRecordkey(HidppMessage):
    """
    Device supports a single MR button for host-mode macro recording.
    """
    FEATURE_ID = 0x8030
    MAX_FUNCTION_INDEX_V0 = 0

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
# end class MacroRecordkey


class MacroRecordkeyModel(FeatureModel):
    """
    Define ``MacroRecordkey`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        SET_LED = 0

        # Event index
        BUTTON_REPORT = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``MacroRecordkey`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.SET_LED: {
                    "request": SetLED,
                    "response": SetLEDResponse
                }
            },
            "events": {
                cls.INDEX.BUTTON_REPORT: {"report": ButtonReportEvent}
            }
        }

        return {
            "feature_base": MacroRecordkey,
            "versions": {
                MacroRecordkeyV0.VERSION: {
                    "main_cls": MacroRecordkeyV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class MacroRecordkeyModel


class MacroRecordkeyFactory(FeatureFactory):
    """
    Get ``MacroRecordkey`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``MacroRecordkey`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``MacroRecordkeyInterface``
        """
        return MacroRecordkeyModel.get_main_cls(version)()
    # end def create
# end class MacroRecordkeyFactory


class MacroRecordkeyInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``MacroRecordkey``
    """

    def __init__(self):
        # Requests
        self.set_led_cls = None

        # Responses
        self.set_led_response_cls = None

        # Events
        self.button_report_event_cls = None
    # end def __init__
# end class MacroRecordkeyInterface


class MacroRecordkeyV0(MacroRecordkeyInterface):
    """
    Define ``MacroRecordkeyV0`` feature

    This feature provides model and unit specific information for version 0

    [0] setLED(enabled) -> None

    [Event 0] ButtonReportEvent -> mrButtonStatus
    """
    VERSION = 0

    def __init__(self):
        # See ``MacroRecordkey.__init__``
        super().__init__()
        index = MacroRecordkeyModel.INDEX

        # Requests
        self.set_led_cls = MacroRecordkeyModel.get_request_cls(
            self.VERSION, index.SET_LED)

        # Responses
        self.set_led_response_cls = MacroRecordkeyModel.get_response_cls(
            self.VERSION, index.SET_LED)

        # Events
        self.button_report_event_cls = MacroRecordkeyModel.get_report_cls(
            self.VERSION, index.BUTTON_REPORT)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``MacroRecordkeyInterface.get_max_function_index``
        return MacroRecordkeyModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class MacroRecordkeyV0


class LongEmptyPacketDataFormat(MacroRecordkey):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetLEDResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(MacroRecordkey.FID):
        # See ``MacroRecordkey.FID``
        PADDING = MacroRecordkey.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MacroRecordkey.LEN):
        # See ``MacroRecordkey.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = MacroRecordkey.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MacroRecordkey.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class SetLED(MacroRecordkey):
    """
    Define ``SetLED`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    enabled                       8
    Padding                       16
    ============================  ==========
    """

    class FID(MacroRecordkey.FID):
        # See ``MacroRecordkey.FID``
        ENABLED = MacroRecordkey.FID.SOFTWARE_ID - 1
        PADDING = ENABLED - 1
    # end class FID

    class LEN(MacroRecordkey.LEN):
        # See ``MacroRecordkey.LEN``
        ENABLED = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = MacroRecordkey.FIELDS + (
        BitField(fid=FID.ENABLED, length=LEN.ENABLED,
                 title="Enabled", name="enabled",
                 checks=(CheckHexList(LEN.ENABLED // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MacroRecordkey.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, enabled, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param enabled: enabled
        :type enabled: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetLEDResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.enabled = HexList(Numeral(enabled, self.LEN.ENABLED // 8))
    # end def __init__
# end class SetLED


class SetLEDResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetLEDResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetLED,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

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
# end class SetLEDResponse


class ButtonReportEvent(MacroRecordkey):
    """
    Define ``ButtonReportEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    MR button status              8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(MacroRecordkey.FID):
        # See ``MacroRecordkey.FID``
        MR_BUTTON_STATUS = MacroRecordkey.FID.SOFTWARE_ID - 1
        PADDING = MR_BUTTON_STATUS - 1
    # end class FID

    class LEN(MacroRecordkey.LEN):
        # See ``MacroRecordkey.LEN``
        MR_BUTTON_STATUS = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = MacroRecordkey.FIELDS + (
        BitField(fid=FID.MR_BUTTON_STATUS, length=LEN.MR_BUTTON_STATUS,
                 title="MrButtonStatus", name="mr_button_status",
                 checks=(CheckHexList(LEN.MR_BUTTON_STATUS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MacroRecordkey.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mr_button_status, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param mr_button_status: MR button status
        :type mr_button_status: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mr_button_status = HexList(Numeral(mr_button_status, self.LEN.MR_BUTTON_STATUS // 8))
    # end def __init__
# end class ButtonReportEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
