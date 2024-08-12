#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.mousebuttonspy
:brief: HID++ 2.0 ``MouseButtonSpy`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MouseButtonSpy(HidppMessage):
    """
    Manage button remapping
    """
    FEATURE_ID = 0x8110
    MAX_FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class MouseButtonSpy


class MouseButtonSpyModel(FeatureModel):
    """
    ``MouseButtonSpy`` feature model
    """
    class INDEX(object):
        """
        Function/Event index
        """
        # Function index
        GET_NB_OF_BUTTONS = 0
        START_SPY = 1
        STOP_SPY = 2
        GET_REMAPPING = 3
        SET_REMAPPING = 4

        # Event index
        BUTTON = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        ``MouseButtonSpy`` feature data model
        """
        return {
            "feature_base": MouseButtonSpy,
            "versions": {
                MouseButtonSpyV0.VERSION: {
                    "main_cls": MouseButtonSpyV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_NB_OF_BUTTONS: {
                                "request": GetNbOfButtons,
                                "response": GetNbOfButtonsResponse
                            },
                            cls.INDEX.START_SPY: {
                                "request": StartSpy,
                                "response": StartSpyResponse
                            },
                            cls.INDEX.STOP_SPY: {
                                "request": StopSpy,
                                "response": StopSpyResponse
                            },
                            cls.INDEX.GET_REMAPPING: {
                                "request": GetRemapping,
                                "response": GetRemappingResponse
                            },
                            cls.INDEX.SET_REMAPPING: {
                                "request": SetRemapping,
                                "response": SetRemappingResponse
                            }
                        },
                        "events": {
                            cls.INDEX.BUTTON: {
                                "report": ButtonEvent
                            }
                        }
                    }
                }
            }
        }
    # end def _get_data_model
# end class MouseButtonSpyModel


class MouseButtonSpyFactory(FeatureFactory):
    """
    Factory which creates a ``MouseButtonSpy`` object from a given version
    """
    @staticmethod
    def create(version):
        """
        ``MouseButtonSpy`` object creation from version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``MouseButtonSpyInterface``
        """
        return MouseButtonSpyModel.get_main_cls(version)()
    # end def create
# end class MouseButtonSpyFactory


class MouseButtonSpyInterface(FeatureInterface, ABC):
    """
    Defines required interfaces for ``MouseButtonSpy`` classes
    """
    def __init__(self):
        # Requests
        self.get_nb_of_buttons_cls = None
        self.start_spy_cls = None
        self.stop_spy_cls = None
        self.get_remapping_cls = None
        self.set_remapping_cls = None

        # Responses
        self.get_nb_of_buttons_response_cls = None
        self.start_spy_response_cls = None
        self.stop_spy_response_cls = None
        self.get_remapping_response_cls = None
        self.set_remapping_response_cls = None

        # Events
        self.button_event_cls = None
    # end def __init__
# end class MouseButtonSpyInterface


class MouseButtonSpyV0(MouseButtonSpyInterface):
    """
    ``MouseButtonSpyV0``

    This feature provides model and unit specific information for version 0

    [0] getNbOfButtons() -> nbButtons

    [1] startSpy() -> None

    [2] stopSpy() -> None

    [3] getRemapping() -> button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12, button13, button14, button15, button16

    [4] setRemapping(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12, button13, button14, button15, button16) -> None

    [Event 0] buttonEvent -> button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12, button13, button14, button15, button16
    """
    VERSION = 0

    def __init__(self):
        # See ``MouseButtonSpy.__init__``
        super().__init__()
        index = MouseButtonSpyModel.INDEX

        # Requests
        self.get_nb_of_buttons_cls = MouseButtonSpyModel.get_request_cls(
            self.VERSION, index.GET_NB_OF_BUTTONS)
        self.start_spy_cls = MouseButtonSpyModel.get_request_cls(
            self.VERSION, index.START_SPY)
        self.stop_spy_cls = MouseButtonSpyModel.get_request_cls(
            self.VERSION, index.STOP_SPY)
        self.get_remapping_cls = MouseButtonSpyModel.get_request_cls(
            self.VERSION, index.GET_REMAPPING)
        self.set_remapping_cls = MouseButtonSpyModel.get_request_cls(
            self.VERSION, index.SET_REMAPPING)

        # Responses
        self.get_nb_of_buttons_response_cls = MouseButtonSpyModel.get_response_cls(
            self.VERSION, index.GET_NB_OF_BUTTONS)
        self.start_spy_response_cls = MouseButtonSpyModel.get_response_cls(
            self.VERSION, index.START_SPY)
        self.stop_spy_response_cls = MouseButtonSpyModel.get_response_cls(
            self.VERSION, index.STOP_SPY)
        self.get_remapping_response_cls = MouseButtonSpyModel.get_response_cls(
            self.VERSION, index.GET_REMAPPING)
        self.set_remapping_response_cls = MouseButtonSpyModel.get_response_cls(
            self.VERSION, index.SET_REMAPPING)

        # Events
        self.button_event_cls = MouseButtonSpyModel.get_report_cls(
            self.VERSION, index.BUTTON)
    # end def __init__

    def get_max_function_index(self):
        # See ``MouseButtonSpyInterface.get_max_function_index``
        return MouseButtonSpyModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class MouseButtonSpyV0


class ShortEmptyPacketDataFormat(MouseButtonSpy):
    """
    This class is to be used as a base class for several messages in this feature
        - GetNbOfButtons
        - StartSpy
        - StopSpy
        - GetRemapping

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """
    class FID(MouseButtonSpy.FID):
        """
        Field Identifiers
        """
        PADDING = MouseButtonSpy.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MouseButtonSpy.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = MouseButtonSpy.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseButtonSpy.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(MouseButtonSpy):
    """
    This class is to be used as a base class for several messages in this feature
        - StartSpyResponse
        - StopSpyResponse
        - SetRemappingResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """
    class FID(MouseButtonSpy.FID):
        """
        Field Identifiers
        """
        PADDING = MouseButtonSpy.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MouseButtonSpy.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = MouseButtonSpy.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseButtonSpy.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class ButtonFormat(MouseButtonSpy):
    """
    This class is to be used as a base class for several messages in this feature.
        - GetRemappingResponse
        - SetRemapping

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Button1                       8
    Button2                       8
    Button3                       8
    Button4                       8
    Button5                       8
    Button6                       8
    Button7                       8
    Button8                       8
    Button9                       8
    Button10                      8
    Button11                      8
    Button12                      8
    Button13                      8
    Button14                      8
    Button15                      8
    Button16                      8
    ============================  ==========
    """
    class FID(MouseButtonSpy.FID):
        """
        Field Identifiers
        """
        BUTTON_1 = MouseButtonSpy.FID.SOFTWARE_ID - 1
        BUTTON_2 = BUTTON_1 - 1
        BUTTON_3 = BUTTON_2 - 1
        BUTTON_4 = BUTTON_3 - 1
        BUTTON_5 = BUTTON_4 - 1
        BUTTON_6 = BUTTON_5 - 1
        BUTTON_7 = BUTTON_6 - 1
        BUTTON_8 = BUTTON_7 - 1
        BUTTON_9 = BUTTON_8 - 1
        BUTTON_10 = BUTTON_9 - 1
        BUTTON_11 = BUTTON_10 - 1
        BUTTON_12 = BUTTON_11 - 1
        BUTTON_13 = BUTTON_12 - 1
        BUTTON_14 = BUTTON_13 - 1
        BUTTON_15 = BUTTON_14 - 1
        BUTTON_16 = BUTTON_15 - 1
    # end class FID

    class LEN(MouseButtonSpy.LEN):
        """
        Field Lengths
        """
        BUTTON_1 = 0x8
        BUTTON_2 = 0x8
        BUTTON_3 = 0x8
        BUTTON_4 = 0x8
        BUTTON_5 = 0x8
        BUTTON_6 = 0x8
        BUTTON_7 = 0x8
        BUTTON_8 = 0x8
        BUTTON_9 = 0x8
        BUTTON_10 = 0x8
        BUTTON_11 = 0x8
        BUTTON_12 = 0x8
        BUTTON_13 = 0x8
        BUTTON_14 = 0x8
        BUTTON_15 = 0x8
        BUTTON_16 = 0x8
    # end class LEN

    FIELDS = MouseButtonSpy.FIELDS + (
        BitField(fid=FID.BUTTON_1, length=LEN.BUTTON_1,
                 title="Button1", name="button_1",
                 checks=(CheckHexList(LEN.BUTTON_1 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_2, length=LEN.BUTTON_2,
                 title="Button2", name="button_2",
                 checks=(CheckHexList(LEN.BUTTON_2 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_3, length=LEN.BUTTON_3,
                 title="Button3", name="button_3",
                 checks=(CheckHexList(LEN.BUTTON_3 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_4, length=LEN.BUTTON_4,
                 title="Button4", name="button_4",
                 checks=(CheckHexList(LEN.BUTTON_4 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_5, length=LEN.BUTTON_5,
                 title="Button5", name="button_5",
                 checks=(CheckHexList(LEN.BUTTON_5 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_6, length=LEN.BUTTON_6,
                 title="Button6", name="button_6",
                 checks=(CheckHexList(LEN.BUTTON_6 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_7, length=LEN.BUTTON_7,
                 title="Button7", name="button_7",
                 checks=(CheckHexList(LEN.BUTTON_7 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_8, length=LEN.BUTTON_8,
                 title="Button8", name="button_8",
                 checks=(CheckHexList(LEN.BUTTON_8 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_9, length=LEN.BUTTON_9,
                 title="Button9", name="button_9",
                 checks=(CheckHexList(LEN.BUTTON_9 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_10, length=LEN.BUTTON_10,
                 title="Button10", name="button_10",
                 checks=(CheckHexList(LEN.BUTTON_10 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_11, length=LEN.BUTTON_11,
                 title="Button11", name="button_11",
                 checks=(CheckHexList(LEN.BUTTON_11 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_12, length=LEN.BUTTON_12,
                 title="Button12", name="button_12",
                 checks=(CheckHexList(LEN.BUTTON_12 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_13, length=LEN.BUTTON_13,
                 title="Button13", name="button_13",
                 checks=(CheckHexList(LEN.BUTTON_13 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_14, length=LEN.BUTTON_14,
                 title="Button14", name="button_14",
                 checks=(CheckHexList(LEN.BUTTON_14 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_15, length=LEN.BUTTON_15,
                 title="Button15", name="button_15",
                 checks=(CheckHexList(LEN.BUTTON_15 // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_16, length=LEN.BUTTON_16,
                 title="Button16", name="button_16",
                 checks=(CheckHexList(LEN.BUTTON_16 // 8), CheckByte(),)),
    )
# end class ButtonFormat


class GetNbOfButtons(ShortEmptyPacketDataFormat):
    """
    ``GetNbOfButtons`` implementation class for version 0
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetNbOfButtonsResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetNbOfButtons


class GetNbOfButtonsResponse(MouseButtonSpy):
    """
    ``GetNbOfButtonsResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbButtons                     8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetNbOfButtons,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(MouseButtonSpy.FID):
        """
        Field Identifiers
        """
        NB_BUTTONS = MouseButtonSpy.FID.SOFTWARE_ID - 1
        PADDING = NB_BUTTONS - 1
    # end class FID

    class LEN(MouseButtonSpy.LEN):
        """
        Field Lengths
        """
        NB_BUTTONS = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = MouseButtonSpy.FIELDS + (
        BitField(fid=FID.NB_BUTTONS, length=LEN.NB_BUTTONS,
                 title="NbButtons", name="nb_buttons",
                 checks=(CheckHexList(LEN.NB_BUTTONS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseButtonSpy.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, nb_buttons, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param nb_buttons: Number of physical buttons of the device
        :type nb_buttons: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.nb_buttons = nb_buttons
    # end def __init__
# end class GetNbOfButtonsResponse


class StartSpy(ShortEmptyPacketDataFormat):
    """
    ``StartSpy`` implementation class for version 0
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=StartSpyResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class StartSpy


class StartSpyResponse(LongEmptyPacketDataFormat):
    """
    ``StartSpyResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartSpy,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class StartSpyResponse


class StopSpy(ShortEmptyPacketDataFormat):
    """
    ``StopSpy`` implementation class for version 0
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=StopSpyResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class StopSpy


class StopSpyResponse(LongEmptyPacketDataFormat):
    """
    ``StopSpyResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StopSpy,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class StopSpyResponse


class GetRemapping(ShortEmptyPacketDataFormat):
    """
    ``GetRemapping`` implementation class for version 0
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetRemappingResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetRemapping


class GetRemappingResponse(ButtonFormat):
    """
    ``GetRemappingResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRemapping,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index,
                 button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10, button_11, button_12, button_13, button_14, button_15, button_16,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param button_1: Button 1
        :type button_1: ``int`` or ``HexList``
        :param button_2: Button 2
        :type button_2: ``int`` or ``HexList``
        :param button_3: Button 3
        :type button_3: ``int`` or ``HexList``
        :param button_4: Button 4
        :type button_4: ``int`` or ``HexList``
        :param button_5: Button 5
        :type button_5: ``int`` or ``HexList``
        :param button_6: Button 6
        :type button_6: ``int`` or ``HexList``
        :param button_7: Button 7
        :type button_7: ``int`` or ``HexList``
        :param button_8: Button 8
        :type button_8: ``int`` or ``HexList``
        :param button_9: Button 9
        :type button_9: ``int`` or ``HexList``
        :param button_10: Button 10
        :type button_10: ``int`` or ``HexList``
        :param button_11: Button 11
        :type button_11: ``int`` or ``HexList``
        :param button_12: Button 12
        :type button_12: ``int`` or ``HexList``
        :param button_13: Button 13
        :type button_13: ``int`` or ``HexList``
        :param button_14: Button 14
        :type button_14: ``int`` or ``HexList``
        :param button_15: Button 15
        :type button_15: ``int`` or ``HexList``
        :param button_16: Button 16
        :type button_16: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.button_1 = button_1
        self.button_2 = button_2
        self.button_3 = button_3
        self.button_4 = button_4
        self.button_5 = button_5
        self.button_6 = button_6
        self.button_7 = button_7
        self.button_8 = button_8
        self.button_9 = button_9
        self.button_10 = button_10
        self.button_11 = button_11
        self.button_12 = button_12
        self.button_13 = button_13
        self.button_14 = button_14
        self.button_15 = button_15
        self.button_16 = button_16
    # end def __init__
# end class GetRemappingResponse


class SetRemapping(ButtonFormat):
    """
    ``SetRemapping`` implementation class for version 0
    """
    def __init__(self, device_index, feature_index,
                 button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10, button_11, button_12, button_13, button_14, button_15, button_16,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param button_1: Button 1
        :type button_1: ``int`` or ``HexList``
        :param button_2: Button 2
        :type button_2: ``int`` or ``HexList``
        :param button_3: Button 3
        :type button_3: ``int`` or ``HexList``
        :param button_4: Button 4
        :type button_4: ``int`` or ``HexList``
        :param button_5: Button 5
        :type button_5: ``int`` or ``HexList``
        :param button_6: Button 6
        :type button_6: ``int`` or ``HexList``
        :param button_7: Button 7
        :type button_7: ``int`` or ``HexList``
        :param button_8: Button 8
        :type button_8: ``int`` or ``HexList``
        :param button_9: Button 9
        :type button_9: ``int`` or ``HexList``
        :param button_10: Button 10
        :type button_10: ``int`` or ``HexList``
        :param button_11: Button 11
        :type button_11: ``int`` or ``HexList``
        :param button_12: Button 12
        :type button_12: ``int`` or ``HexList``
        :param button_13: Button 13
        :type button_13: ``int`` or ``HexList``
        :param button_14: Button 14
        :type button_14: ``int`` or ``HexList``
        :param button_15: Button 15
        :type button_15: ``int`` or ``HexList``
        :param button_16: Button 16
        :type button_16: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetRemappingResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.button_1 = button_1
        self.button_2 = button_2
        self.button_3 = button_3
        self.button_4 = button_4
        self.button_5 = button_5
        self.button_6 = button_6
        self.button_7 = button_7
        self.button_8 = button_8
        self.button_9 = button_9
        self.button_10 = button_10
        self.button_11 = button_11
        self.button_12 = button_12
        self.button_13 = button_13
        self.button_14 = button_14
        self.button_15 = button_15
        self.button_16 = button_16
    # end def __init__
# end class SetRemapping


class SetRemappingResponse(LongEmptyPacketDataFormat):
    """
    ``SetRemappingResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRemapping,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetRemappingResponse


class ButtonEvent(MouseButtonSpy):
    """
    ``ButtonEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Button1                       1
    Button2                       1
    Button3                       1
    Button4                       1
    Button5                       1
    Button6                       1
    Button7                       1
    Button8                       1
    Button9                       1
    Button10                      1
    Button11                      1
    Button12                      1
    Button13                      1
    Button14                      1
    Button15                      1
    Button16                      1
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(MouseButtonSpy.FID):
        """
        Field Identifiers
        """
        BUTTON_1 = MouseButtonSpy.FID.SOFTWARE_ID - 1
        BUTTON_2 = BUTTON_1 - 1
        BUTTON_3 = BUTTON_2 - 1
        BUTTON_4 = BUTTON_3 - 1
        BUTTON_5 = BUTTON_4 - 1
        BUTTON_6 = BUTTON_5 - 1
        BUTTON_7 = BUTTON_6 - 1
        BUTTON_8 = BUTTON_7 - 1
        BUTTON_9 = BUTTON_8 - 1
        BUTTON_10 = BUTTON_9 - 1
        BUTTON_11 = BUTTON_10 - 1
        BUTTON_12 = BUTTON_11 - 1
        BUTTON_13 = BUTTON_12 - 1
        BUTTON_14 = BUTTON_13 - 1
        BUTTON_15 = BUTTON_14 - 1
        BUTTON_16 = BUTTON_15 - 1
        PADDING = BUTTON_16 - 1
    # end class FID

    class LEN(MouseButtonSpy.LEN):
        """
        Field Lengths
        """
        BUTTON_1 = 0x1
        BUTTON_2 = 0x1
        BUTTON_3 = 0x1
        BUTTON_4 = 0x1
        BUTTON_5 = 0x1
        BUTTON_6 = 0x1
        BUTTON_7 = 0x1
        BUTTON_8 = 0x1
        BUTTON_9 = 0x1
        BUTTON_10 = 0x1
        BUTTON_11 = 0x1
        BUTTON_12 = 0x1
        BUTTON_13 = 0x1
        BUTTON_14 = 0x1
        BUTTON_15 = 0x1
        BUTTON_16 = 0x1
        PADDING = 0x70
    # end class LEN

    FIELDS = MouseButtonSpy.FIELDS + (
        BitField(fid=FID.BUTTON_1, length=LEN.BUTTON_1,
                 title="Button1", name="button_1",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_1) - 1),)),
        BitField(fid=FID.BUTTON_2, length=LEN.BUTTON_2,
                 title="Button2", name="button_2",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_2) - 1),)),
        BitField(fid=FID.BUTTON_3, length=LEN.BUTTON_3,
                 title="Button3", name="button_3",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_3) - 1),)),
        BitField(fid=FID.BUTTON_4, length=LEN.BUTTON_4,
                 title="Button4", name="button_4",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_4) - 1),)),
        BitField(fid=FID.BUTTON_5, length=LEN.BUTTON_5,
                 title="Button5", name="button_5",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_5) - 1),)),
        BitField(fid=FID.BUTTON_6, length=LEN.BUTTON_6,
                 title="Button6", name="button_6",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_6) - 1),)),
        BitField(fid=FID.BUTTON_7, length=LEN.BUTTON_7,
                 title="Button7", name="button_7",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_7) - 1),)),
        BitField(fid=FID.BUTTON_8, length=LEN.BUTTON_8,
                 title="Button8", name="button_8",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_8) - 1),)),
        BitField(fid=FID.BUTTON_9, length=LEN.BUTTON_9,
                 title="Button9", name="button_9",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_9) - 1),)),
        BitField(fid=FID.BUTTON_10, length=LEN.BUTTON_10,
                 title="Button10", name="button_10",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_10) - 1),)),
        BitField(fid=FID.BUTTON_11, length=LEN.BUTTON_11,
                 title="Button11", name="button_11",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_11) - 1),)),
        BitField(fid=FID.BUTTON_12, length=LEN.BUTTON_12,
                 title="Button12", name="button_12",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_12) - 1),)),
        BitField(fid=FID.BUTTON_13, length=LEN.BUTTON_13,
                 title="Button13", name="button_13",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_13) - 1),)),
        BitField(fid=FID.BUTTON_14, length=LEN.BUTTON_14,
                 title="Button14", name="button_14",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_14) - 1),)),
        BitField(fid=FID.BUTTON_15, length=LEN.BUTTON_15,
                 title="Button15", name="button_15",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_15) - 1),)),
        BitField(fid=FID.BUTTON_16, length=LEN.BUTTON_16,
                 title="Button16", name="button_16",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.BUTTON_16) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseButtonSpy.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index,
                 button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10,
                 button_11, button_12, button_13, button_14, button_15, button_16, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param button_1: Button 1
        :type button_1: ``bool`` or ``HexList``
        :param button_2: Button 2
        :type button_2: ``bool`` or ``HexList``
        :param button_3: Button 3
        :type button_3: ``bool`` or ``HexList``
        :param button_4: Button 4
        :type button_4: ``bool`` or ``HexList``
        :param button_5: Button 5
        :type button_5: ``bool`` or ``HexList``
        :param button_6: Button 6
        :type button_6: ``bool`` or ``HexList``
        :param button_7: Button 7
        :type button_7: ``bool`` or ``HexList``
        :param button_8: Button 8
        :type button_8: ``bool`` or ``HexList``
        :param button_9: Button 9
        :type button_9: ``bool`` or ``HexList``
        :param button_10: Button 10
        :type button_10: ``bool`` or ``HexList``
        :param button_11: Button 11
        :type button_11: ``bool`` or ``HexList``
        :param button_12: Button 12
        :type button_12: ``bool`` or ``HexList``
        :param button_13: Button 13
        :type button_13: ``bool`` or ``HexList``
        :param button_14: Button 14
        :type button_14: ``bool`` or ``HexList``
        :param button_15: Button 15
        :type button_15: ``bool`` or ``HexList``
        :param button_16: Button 16
        :type button_16: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.button_1 = button_1
        self.button_2 = button_2
        self.button_3 = button_3
        self.button_4 = button_4
        self.button_5 = button_5
        self.button_6 = button_6
        self.button_7 = button_7
        self.button_8 = button_8
        self.button_9 = button_9
        self.button_10 = button_10
        self.button_11 = button_11
        self.button_12 = button_12
        self.button_13 = button_13
        self.button_14 = button_14
        self.button_15 = button_15
        self.button_16 = button_16
    # end def __init__
# end class ButtonEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
