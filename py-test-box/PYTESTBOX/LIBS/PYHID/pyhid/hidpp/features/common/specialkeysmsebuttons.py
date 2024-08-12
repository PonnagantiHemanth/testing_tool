#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.specialkeysmsebuttons
:brief: HID++ 2.0 Special Keys and Mouse Buttons command interface definition
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/05/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
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
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CidInfoPayload(BitFieldContainerMixin):
    """
    Define the format of a CID Info payload
    """
    class FID:
        """
        Field Identifiers
        """
        CTRL_ID = 0xFF
        TASK_ID = CTRL_ID - 1
        FLAGS = TASK_ID - 1
        FKEY_POS = FLAGS - 1
        GROUP = FKEY_POS - 1
        GMASK = GROUP - 1
        ADDITIONAL_FLAGS = GMASK - 1
    # end class FID

    class LEN:
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        TASK_ID = 0x10
        FLAGS = 0x08
        FKEY_POS = 0x08
        GROUP = 0x08
        GMASK = 0x08
        ADDITIONAL_FLAGS = 0x08
    # end class LEN

    FIELDS = (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.TASK_ID,
                 LEN.TASK_ID,
                 title='TaskId',
                 name='task_id',
                 aliases=('tid', 'task'),
                 checks=(CheckHexList(LEN.TASK_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.FLAGS,
                 LEN.FLAGS,
                 title='Flags',
                 name='flags',
                 checks=(CheckHexList(LEN.FLAGS // 8),
                         CheckByte(),), ),
        BitField(FID.FKEY_POS,
                 LEN.FKEY_POS,
                 title='FkeyPos',
                 name='fkey_pos',
                 aliases=('pos',),
                 optional=True,
                 checks=(CheckHexList(LEN.FKEY_POS // 8),
                         CheckByte(),), ),
        BitField(FID.GROUP,
                 LEN.GROUP,
                 title='Group',
                 name='group',
                 optional=True,
                 checks=(CheckHexList(LEN.GROUP // 8),
                         CheckByte(),), ),
        BitField(FID.GMASK,
                 LEN.GMASK,
                 title='Gmask',
                 name='gmask',
                 optional=True,
                 checks=(CheckHexList(LEN.GMASK // 8),
                         CheckByte(),), ),
        BitField(FID.ADDITIONAL_FLAGS,
                 LEN.ADDITIONAL_FLAGS,
                 title='AdditionalFlags',
                 name='additional_flags',
                 optional=True,
                 checks=(CheckHexList(LEN.ADDITIONAL_FLAGS // 8),
                         CheckByte(),), ),
    )

    class Flags(BitFieldContainerMixin):
        """
        This class defines the format of flags field
        """
        class FID:
            """
            Field Identifiers
            """
            VIRTUAL = 0xFF
            PERSIST = VIRTUAL - 1
            DIVERT = PERSIST - 1
            REPROG = DIVERT - 1
            FN_TOG = REPROG - 1
            HOT_KEY = FN_TOG - 1
            FKEY = HOT_KEY - 1
            MOUSE = FKEY - 1
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            VIRTUAL = 0x01
            PERSIST = 0x01
            DIVERT = 0x01
            REPROG = 0x01
            FN_TOG = 0x01
            HOT_KEY = 0x01
            FKEY = 0x01
            MOUSE = 0x01
        # end class LEN

        FIELDS = (
            BitField(FID.VIRTUAL,
                     LEN.VIRTUAL,
                     title='Virtual',
                     name='virtual',
                     checks=(CheckInt(0, pow(2, LEN.VIRTUAL) - 1),)),
            BitField(FID.PERSIST,
                     LEN.PERSIST,
                     title='Persist',
                     name='persist',
                     checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
            BitField(FID.DIVERT,
                     LEN.DIVERT,
                     title='Divert',
                     name='divert',
                     checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
            BitField(FID.REPROG,
                     LEN.REPROG,
                     title='Reprog',
                     name='reprog',
                     checks=(CheckInt(0, pow(2, LEN.REPROG) - 1),)),
            BitField(FID.FN_TOG,
                     LEN.FN_TOG,
                     title='FnTog',
                     name='fn_tog',
                     checks=(CheckInt(0, pow(2, LEN.FN_TOG) - 1),)),
            BitField(FID.HOT_KEY,
                     LEN.HOT_KEY,
                     title='HotKey',
                     name='hot_key',
                     checks=(CheckInt(0, pow(2, LEN.HOT_KEY) - 1),)),
            BitField(FID.FKEY,
                     LEN.FKEY,
                     title='Fkey',
                     name='fkey',
                     checks=(CheckInt(0, pow(2, LEN.FKEY) - 1),)),
            BitField(FID.MOUSE,
                     LEN.MOUSE,
                     title='Mouse',
                     name='mouse',
                     checks=(CheckInt(0, pow(2, LEN.MOUSE) - 1),)),
        )
    # end class Flags

    class AdditionalFlags(BitFieldContainerMixin):
        """
        This class defines the format of additional flags field
        """
        class FID:
            """
            Field Identifiers
            """
            UNUSED = 0xFF
            RAW_WHEEL = UNUSED - 1
            ANALYTICS_KEY_EVENTS = RAW_WHEEL - 1
            FORCE_RAW_XY = ANALYTICS_KEY_EVENTS - 1
            RAW_XY = FORCE_RAW_XY - 1
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            UNUSED = 0x04
            RAW_WHEEL = 0x01
            ANALYTICS_KEY_EVENTS = 0x01
            FORCE_RAW_XY = 0x01
            RAW_XY = 0x01
        # end class LEN

        class DEFAULT:
            """
            Field default values
            """
            UNUSED = 0x00
        # end class DEFAULT

        FIELDS = (
            BitField(FID.UNUSED,
                     LEN.UNUSED,
                     title='Unused',
                     name='unused',
                     default_value=DEFAULT.UNUSED,
                     checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
            BitField(FID.RAW_WHEEL,
                     LEN.RAW_WHEEL,
                     title='RawWheel',
                     name='raw_wheel',
                     checks=(CheckInt(0, pow(2, LEN.RAW_WHEEL) - 1),)),
            BitField(FID.ANALYTICS_KEY_EVENTS,
                     LEN.ANALYTICS_KEY_EVENTS,
                     title='AnalyticsKeyEvents',
                     name='analytics_key_events',
                     checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVENTS) - 1),)),
            BitField(FID.FORCE_RAW_XY,
                     LEN.FORCE_RAW_XY,
                     title='ForceRawXY',
                     name='force_raw_xy',
                     checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
            BitField(FID.RAW_XY,
                     LEN.RAW_XY,
                     title='RawXY',
                     name='raw_xy',
                     checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        )
    # end class AdditionalFlags

    def __init__(self, cid, tid, flags, pos=None, group=None, gmask=None, additional_flags=None):
        """
        Constructor

        :param cid: Control ID
        :type cid: ``int`` or ``HexList``
        :param tid: Task ID
        :type tid: ``int`` or ``HexList``
        :param flags: Flags for this control
        :type flags: ``int`` or ``HexList`` or ``Flags``
        :param pos: The position of the control on the device - OPTIONAL
        :type pos: ``int`` or ``HexList``
        :param group: Which mapping group this control ID belongs to  - OPTIONAL
        :type group: ``int`` or ``HexList``
        :param gmask: This control can be remapped to any control ID contained in the specified groups - OPTIONAL
        :type gmask: ``int`` or ``HexList``
        :param additional_flags: Additional flags for this control - OPTIONAL
        :type additional_flags: ``int`` or ``HexList`` or ``AdditionalFlags``
        """
        super().__init__(cid=cid, tid=tid, flags=flags, pos=pos, group=group, gmask=gmask,
                         additional_flags=additional_flags)
        self.flags = self.Flags.fromHexList(HexList(flags))
        if additional_flags is not None:
            self.additional_flags = self.AdditionalFlags.fromHexList(HexList(additional_flags))
    # end def __init__

    @classmethod
    def from_detailed_fields(cls, cid, task, flag_virtual, flag_persist, flag_divert, flag_reprog, flag_fn_tog,
                             flag_hot_key, flag_f_key, flag_mouse, pos=None, group=None, gmask=None,
                             additional_flags_raw_wheel=None, additional_flags_analytics_key_event=None,
                             additional_flags_force_raw_xy=None, additional_flags_raw_xy=None):
        """
        Constructor from detailed fields, i.e. each flag value given individually

        :param cid: Control Id
        :type cid: ``int`` or ``HexList``
        :param task: Task Id
        :type task: ``int`` or ``HexList``
        :param flag_virtual: Virtual flag
        :type flag_virtual: ``bool`` or ``int`` or ``HexList``
        :param flag_persist: Persist flag
        :type flag_persist: ``bool`` or ``int`` or ``HexList``
        :param flag_divert: Divert flag
        :type flag_divert: ``bool`` or ``int`` or ``HexList``
        :param flag_reprog: Reprog flag
        :type flag_reprog: ``bool`` or ``int`` or ``HexList``
        :param flag_fn_tog: FnTog flag
        :type flag_fn_tog: ``bool`` or ``int`` or ``HexList``
        :param flag_hot_key: HotKey flag
        :type flag_hot_key: ``bool`` or ``int`` or ``HexList``
        :param flag_f_key: FKey flag
        :type flag_f_key: ``bool`` or ``int`` or ``HexList``
        :param flag_mouse: Mouse flag
        :type flag_mouse: ``bool`` or ``int`` or ``HexList``
        :param pos: Pos - OPTIONAL
        :type pos: ``int`` or ``HexList``
        :param group: Group - OPTIONAL
        :type group: ``int`` or ``HexList``
        :param gmask: GMask - OPTIONAL
        :type gmask: ``int`` or ``HexList``
        :param additional_flags_raw_wheel: Raw Wheel flag - OPTIONAL
        :type additional_flags_raw_wheel: ``bool`` or ``int`` or ``HexList``
        :param additional_flags_analytics_key_event: Analytics Key Event flag - OPTIONAL
        :type additional_flags_analytics_key_event: ``bool`` or ``int`` or ``HexList``
        :param additional_flags_force_raw_xy: Force Raw XY flag - OPTIONAL
        :type additional_flags_force_raw_xy: ``bool`` or ``int`` or ``HexList``
        :param additional_flags_raw_xy: Raw XY flag - OPTIONAL
        :type additional_flags_raw_xy: ``bool`` or ``int`` or ``HexList``

        :return: Class instance
        :rtype: ``CidInfoPayload``
        """
        flags = cls.Flags(virtual=flag_virtual, persist=flag_persist, divert=flag_divert, reprog=flag_reprog,
                          fn_tog=flag_fn_tog, hot_key=flag_hot_key, fkey=flag_f_key, mouse=flag_mouse)
        if None not in [additional_flags_raw_wheel, additional_flags_analytics_key_event,
                        additional_flags_force_raw_xy, additional_flags_raw_xy]:
            additional_flags = cls.AdditionalFlags(raw_wheel=additional_flags_raw_wheel,
                                                   analytics_key_events=additional_flags_analytics_key_event,
                                                   force_raw_xy=additional_flags_force_raw_xy,
                                                   raw_xy=additional_flags_raw_xy)
        else:
            additional_flags = None
        # end if
        return cls(cid, task, flags, pos, group, gmask, additional_flags)
    # end def from_detailed_fields

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``CidInfoPayload``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.flags = cls.Flags.fromHexList(inner_field_container_mixin.flags)
        if inner_field_container_mixin.additional_flags is not None:
            inner_field_container_mixin.additional_flags = cls.AdditionalFlags.fromHexList(
                inner_field_container_mixin.additional_flags)
        # end if
        return inner_field_container_mixin
    # end def fromHexList
# end class CidInfoPayload


class SpecialKeysMSEButtons(HidppMessage):
    """
    Define 0x1B04 feature.
    This feature describes nonstandard buttons present on a device and allows them to be diverted to software or mapped
    to different native functions internally within the device.
    """
    FEATURE_ID = 0x1B04
    MAX_FUNCTION_INDEX_V0_TO_V5 = 3
    MAX_FUNCTION_INDEX_V6 = 5

    def __init__(self, device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param report_id: Report id
        :type report_id: ``int``
        """
        super().__init__()

        self.reportId = report_id
        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class SpecialKeysMSEButtons


class SpecialKeysMSEButtonsModel(FeatureModel):
    """
    Define ``SpecialKeysMSEButtons`` feature model
    """
    class INDEX:
        """
        Define Function/Event index
        """
        # Function index
        GET_COUNT = 0
        GET_CID_INFO = 1
        GET_CID_REPORTING = 2
        SET_CID_REPORTING = 3
        GET_CAPABILITIES = 4
        RESET_ALL_CID_REPORT_SETTINGS = 5

        # Events
        DIVERTED_BUTTONS_EVENT = 0
        DIVERTED_RAW_MOUSE_XY_EVENT = 1
        ANALYTICS_KEY_EVENT = 2
        DIVERTED_RAW_WHEEL_EVENT = 4
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``SpecialKeysMSEButtons`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        return {
            "feature_base": SpecialKeysMSEButtons,
            "versions": {
                SpecialKeysMSEButtonsV0.VERSION: {
                    "main_cls": SpecialKeysMSEButtonsV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COUNT: {"request": GetCount, "response": GetCountResponse},
                            cls.INDEX.GET_CID_INFO: {"request": GetCidInfo, "response": GetCidInfoV0Response},
                            cls.INDEX.GET_CID_REPORTING: {"request": GetCidReporting,
                                                          "response": GetCidReportingV0Response},
                            cls.INDEX.SET_CID_REPORTING: {"request": SetCidReportingV0,
                                                          "response": SetCidReportingV0Response},
                        },
                        "events": {
                            cls.INDEX.DIVERTED_BUTTONS_EVENT: {"report": DivertedButtonsEvent},
                        }
                    },
                },
                SpecialKeysMSEButtonsV1.VERSION: {
                    "main_cls": SpecialKeysMSEButtonsV1,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COUNT: {"request": GetCount, "response": GetCountResponse},
                            cls.INDEX.GET_CID_INFO: {"request": GetCidInfo, "response": GetCidInfoV1Response},
                            cls.INDEX.GET_CID_REPORTING: {"request": GetCidReporting,
                                                          "response": GetCidReportingV1Response},
                            cls.INDEX.SET_CID_REPORTING: {"request": SetCidReportingV1,
                                                          "response": SetCidReportingV1Response},
                        },
                        "events": {
                            cls.INDEX.DIVERTED_BUTTONS_EVENT: {"report": DivertedButtonsEvent},
                        }
                    },
                },
                SpecialKeysMSEButtonsV2.VERSION: {
                    "main_cls": SpecialKeysMSEButtonsV2,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COUNT: {"request": GetCount, "response": GetCountResponse},
                            cls.INDEX.GET_CID_INFO: {"request": GetCidInfo, "response": GetCidInfoV2Response},
                            cls.INDEX.GET_CID_REPORTING: {"request": GetCidReporting,
                                                          "response": GetCidReportingV2Response},
                            cls.INDEX.SET_CID_REPORTING: {"request": SetCidReportingV2,
                                                          "response": SetCidReportingV2Response},
                        },
                        "events": {
                            cls.INDEX.DIVERTED_BUTTONS_EVENT: {"report": DivertedButtonsEvent},
                            cls.INDEX.DIVERTED_RAW_MOUSE_XY_EVENT: {"report": DivertedRawMouseXYEventV2toV6}
                        }
                    },
                },
                SpecialKeysMSEButtonsV3.VERSION: {
                    "main_cls": SpecialKeysMSEButtonsV3,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COUNT: {"request": GetCount, "response": GetCountResponse},
                            cls.INDEX.GET_CID_INFO: {"request": GetCidInfo, "response": GetCidInfoV3Response},
                            cls.INDEX.GET_CID_REPORTING: {"request": GetCidReporting,
                                                          "response": GetCidReportingV3Response},
                            cls.INDEX.SET_CID_REPORTING: {"request": SetCidReportingV3,
                                                          "response": SetCidReportingV3Response},
                        },
                        "events": {
                            cls.INDEX.DIVERTED_BUTTONS_EVENT: {"report": DivertedButtonsEvent},
                            cls.INDEX.DIVERTED_RAW_MOUSE_XY_EVENT: {"report": DivertedRawMouseXYEventV2toV6}
                        }
                    },
                },
                SpecialKeysMSEButtonsV4.VERSION: {
                    "main_cls": SpecialKeysMSEButtonsV4,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COUNT: {"request": GetCount, "response": GetCountResponse},
                            cls.INDEX.GET_CID_INFO: {"request": GetCidInfo, "response": GetCidInfoV4Response},
                            cls.INDEX.GET_CID_REPORTING: {"request": GetCidReporting,
                                                          "response": GetCidReportingV4Response},
                            cls.INDEX.SET_CID_REPORTING: {"request": SetCidReportingV4,
                                                          "response": SetCidReportingV4Response},
                        },
                        "events": {
                            cls.INDEX.DIVERTED_BUTTONS_EVENT: {"report": DivertedButtonsEvent},
                            cls.INDEX.DIVERTED_RAW_MOUSE_XY_EVENT: {"report": DivertedRawMouseXYEventV2toV6},
                            cls.INDEX.ANALYTICS_KEY_EVENT: {"report": AnalyticsKeyEventsV4toV6},
                        }
                    },
                },
                SpecialKeysMSEButtonsV5.VERSION: {
                    "main_cls": SpecialKeysMSEButtonsV5,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COUNT: {"request": GetCount, "response": GetCountResponse},
                            cls.INDEX.GET_CID_INFO: {"request": GetCidInfo, "response": GetCidInfoV5toV6Response},
                            cls.INDEX.GET_CID_REPORTING: {"request": GetCidReporting,
                                                          "response": GetCidReportingV5toV6Response},
                            cls.INDEX.SET_CID_REPORTING: {"request": SetCidReportingV5toV6,
                                                          "response": SetCidReportingV5ToV6Response},
                        },
                        "events": {
                            cls.INDEX.DIVERTED_BUTTONS_EVENT: {"report": DivertedButtonsEvent},
                            cls.INDEX.DIVERTED_RAW_MOUSE_XY_EVENT: {"report": DivertedRawMouseXYEventV2toV6},
                            cls.INDEX.ANALYTICS_KEY_EVENT: {"report": AnalyticsKeyEventsV4toV6},
                            cls.INDEX.DIVERTED_RAW_WHEEL_EVENT: {"report": DivertedRawWheelV5toV6},
                        }
                    },
                },
                SpecialKeysMSEButtonsV6.VERSION: {
                    "main_cls": SpecialKeysMSEButtonsV6,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COUNT: {"request": GetCount, "response": GetCountResponse},
                            cls.INDEX.GET_CID_INFO: {"request": GetCidInfo, "response": GetCidInfoV5toV6Response},
                            cls.INDEX.GET_CID_REPORTING: {"request": GetCidReporting,
                                                          "response": GetCidReportingV5toV6Response},
                            cls.INDEX.SET_CID_REPORTING: {"request": SetCidReportingV5toV6,
                                                          "response": SetCidReportingV5ToV6Response},
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilitiesV6,
                                                         "response": GetCapabilitiesV6Response},
                            cls.INDEX.RESET_ALL_CID_REPORT_SETTINGS: {"request": ResetAllCidReportSettingsV6,
                                                                      "response": ResetAllCidReportSettingsV6Response},
                        },
                        "events": {
                            cls.INDEX.DIVERTED_BUTTONS_EVENT: {"report": DivertedButtonsEvent},
                            cls.INDEX.DIVERTED_RAW_MOUSE_XY_EVENT: {"report": DivertedRawMouseXYEventV2toV6},
                            cls.INDEX.ANALYTICS_KEY_EVENT: {"report": AnalyticsKeyEventsV4toV6},
                            cls.INDEX.DIVERTED_RAW_WHEEL_EVENT: {"report": DivertedRawWheelV5toV6},
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class SpecialKeysMSEButtonsModel


class SpecialKeysMSEButtonsFactory(FeatureFactory):
    """
    Get ``SpecialKeysMSEButtons`` object from a given version
    """
    @staticmethod
    def create(version):
        """
        Create ``SpecialKeysMSEButtons`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: SpecialKeysMSEButtons feature object
        :rtype: ``SpecialKeysMSEButtonsInterface``
        """
        return SpecialKeysMSEButtonsModel.get_main_cls(version)()
    # end def create
# end class SpecialKeysMSEButtonsFactory


class SpecialKeysMSEButtonsInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``SpecialKeysMSEButtons``
    """
    def __init__(self):
        # Requests
        self.get_count_cls = None
        self.get_cid_info_cls = None
        self.get_cid_reporting_cls = None
        self.set_cid_reporting_cls = None
        self.get_capabilities_cls = None
        self.reset_all_cid_report_settings_cls = None

        # Responses
        self.get_count_response_cls = None
        self.get_cid_info_response_cls = None
        self.get_cid_reporting_response_cls = None
        self.set_cid_reporting_response_cls = None
        self.get_capabilities_response_cls = None
        self.reset_all_cid_report_settings_response_cls = None

        # Events
        self.diverted_buttons_event_cls = None
        self.diverted_raw_mouse_xy_event_cls = None
        self.analytics_key_event_cls = None
        self.diverted_raw_wheel_event_cls = None
    # end def __init__
# end class SpecialKeysMSEButtonsInterface


class SpecialKeysMSEButtonsV0(SpecialKeysMSEButtonsInterface):
    """
    Define ``SpecialKeysMSEButtonsV0`` feature

    [1] ctrlIDCount -> GetCount()
    [2] ctrlID, taskID, flags -> GetCtrlIDInfo(ctrlIDIndex)
    [3] ctrlID, controlIDReporting -> GetCtrlIDReporting(ctrlID)
    [4] ctrlID, controlIDReporting -> SetCtrlIDReporting(ctrlID, controlIDReporting)
    Event
    [0] ctrlIDIndexPressedList -> ControlIDBroadcastEvent()
    """
    VERSION = 0

    def __init__(self):
        # See ``SpecialKeysMSEButtonsInterface.__init__``
        super().__init__()
        # Requests
        self.get_count_cls = SpecialKeysMSEButtonsModel.get_request_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.GET_COUNT)
        self.get_cid_info_cls = SpecialKeysMSEButtonsModel.get_request_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.GET_CID_INFO)
        self.get_cid_reporting_cls = SpecialKeysMSEButtonsModel.get_request_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.GET_CID_REPORTING)
        self.set_cid_reporting_cls = SpecialKeysMSEButtonsModel.get_request_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.SET_CID_REPORTING)

        # Responses
        self.get_count_response_cls = SpecialKeysMSEButtonsModel.get_response_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.GET_COUNT)
        self.get_cid_info_response_cls = SpecialKeysMSEButtonsModel.get_response_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.GET_CID_INFO)
        self.get_cid_reporting_response_cls = SpecialKeysMSEButtonsModel.get_response_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.GET_CID_REPORTING)
        self.set_cid_reporting_response_cls = SpecialKeysMSEButtonsModel.get_response_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.SET_CID_REPORTING)

        # Events
        self.diverted_buttons_event_cls = SpecialKeysMSEButtonsModel.get_report_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.DIVERTED_BUTTONS_EVENT)
    # end def __init__

    def get_max_function_index(self):
        # See ``SpecialKeysMSEButtonsInterface.get_max_function_index``
        return SpecialKeysMSEButtonsModel.get_base_cls().MAX_FUNCTION_INDEX_V0_TO_V5
    # end def get_max_function_index
# end class SpecialKeysMSEButtonsV0


class SpecialKeysMSEButtonsV1(SpecialKeysMSEButtonsV0):
    """
    Define ``SpecialKeysMSEButtonsV1`` feature

    This feature describes nonstandard buttons present on a device and allows them to be diverted to software or
    mapped to different native functions internally within the device.

    [0] getCount() -> count
    [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask
    [2] getCidReporting(cid) -> cid, divert, persist, remap
    [3] setCidReporting(cid, divert, dvalid, persist, pvalid, remap) -> cid, divert, dvalid, persist, pvalid, remap
    [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
    """
    VERSION = 1
# end class SpecialKeysMSEButtonsV1


class SpecialKeysMSEButtonsV2(SpecialKeysMSEButtonsV1):
    """
    Define ``SpecialKeysMSEButtonsV2`` feature

    This feature describes nonstandard buttons present on a device and allows them to be diverted to software or
    mapped to different native functions internally within the device.

    [0] getCount() -> count
    [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask, additionalflags
    [2] getCidReporting(cid) -> cid, divert, persist, rawXY, remap
    [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap) -> cid, divert, dvalid, persist,
    pvalid, rawXY, rvalid, remap
    [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
    [event1] divertedRawMouseXYEvent -> dx, dy
    """
    VERSION = 2

    def __init__(self):
        # See ``SpecialKeysMSEButtonsInterface.__init__``
        super().__init__()
        # Events
        self.diverted_raw_mouse_xy_event_cls = SpecialKeysMSEButtonsModel.get_report_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.DIVERTED_RAW_MOUSE_XY_EVENT)
    # end def __init__
# end class SpecialKeysMSEButtonsV2


class SpecialKeysMSEButtonsV3(SpecialKeysMSEButtonsV2):
    """
    Define ``SpecialKeysMSEButtonsV3`` feature

    This feature describes nonstandard buttons present on a device and allows them to be diverted to software or
    mapped to different native functions internally within the device.

    [0] getCount() -> count
    [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask, additionalflags
    [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap
    [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap) -> cid,
    divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
    [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
    [event1] divertedRawMouseXYEvent -> dx, dy
    """
    VERSION = 3
# end class SpecialKeysMSEButtonsV3


class SpecialKeysMSEButtonsV4(SpecialKeysMSEButtonsV3):
    """
    Define ``SpecialKeysMSEButtonsV4`` feature

    This feature describes nonstandard buttons present on a device and allows them to be diverted to software or
    mapped to different native functions internally within the device.

    [0] getCount() -> count
    [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask, additionalflags
    [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap, analyticsKeyEvt
    [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, avalid,
    analyticsKeyEvt) -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
    [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
    [event1] divertedRawMouseXYEvent -> dx, dy
    [event2] analyticsKeyEvents -> cid1, event_1, cid2, event_2, cid3, event_3, cid4, event_4, cid5, event_5
    """
    VERSION = 4

    def __init__(self):
        # See ``SpecialKeysMSEButtonsInterface.__init__``
        super().__init__()
        # Events
        self.analytics_key_event_cls = SpecialKeysMSEButtonsModel.get_report_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.ANALYTICS_KEY_EVENT)
    # end def __init__
# end class SpecialKeysMSEButtonsV4


class SpecialKeysMSEButtonsV5(SpecialKeysMSEButtonsV4):
    """
    Define ``SpecialKeysMSEButtonsV5`` feature

    This feature describes nonstandard buttons present on a device and allows them to be diverted to software or
    mapped to different native functions internally within the device.

    [0] getCount() -> count
    [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask, additionalflags
    [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap, analyticsKeyEvt, rawWheel
    [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, avalid,
            analyticsKeyEvt, rawWheel) -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid,
            remap, analyticsKeyEvt, rawWheel

    [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
    [event1] divertedRawMouseXYEvent -> dx, dy
    [event2] analyticsKeyEvents -> cid1, event_1, cid2, event_2, cid3, event_3, cid4, event_4, cid5, event_5
    [event3] Reserved (currently unused)
    [event4] divertedRawWheelEvent -> resolution, periods, deltaV
    """
    VERSION = 5

    def __init__(self):
        # See ``SpecialKeysMSEButtonsInterface.__init__``
        super().__init__()
        # Events
        self.diverted_raw_wheel_event_cls = SpecialKeysMSEButtonsModel.get_report_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.DIVERTED_RAW_WHEEL_EVENT)
    # end def __init__
# end class SpecialKeysMSEButtonsV5


class SpecialKeysMSEButtonsV6(SpecialKeysMSEButtonsV5):
    """
    Define ``SpecialKeysMSEButtonsV6`` feature

    This feature describes nonstandard buttons present on a device and allows them to be diverted to software or
    mapped to different native functions internally within the device.

    [0] getCount() -> count
    [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask, additionalflags
    [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap, analyticsKeyEvt, rawWheel
    [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, avalid,
            analyticsKeyEvt, rawWheel) -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid,
            remap, analyticsKeyEvt, rawWheel
    [4] getCapabilities() -> flags
    [5] resetAllCidReportSettings()

    [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
    [event1] divertedRawMouseXYEvent -> dx, dy
    [event2] analyticsKeyEvents -> cid1, event_1, cid2, event_2, cid3, event_3, cid4, event_4, cid5, event_5
    [event3] Reserved (currently unused)
    [event4] divertedRawWheelEvent -> resolution, periods, deltaV
    """
    VERSION = 6

    def __init__(self):
        # See ``SpecialKeysMSEButtonsInterface.__init__``
        super().__init__()
        # Requests
        self.get_capabilities_cls = SpecialKeysMSEButtonsModel.get_request_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.GET_CAPABILITIES)
        self.reset_all_cid_report_settings_cls = SpecialKeysMSEButtonsModel.get_request_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.RESET_ALL_CID_REPORT_SETTINGS)

        # Responses
        self.get_capabilities_response_cls = SpecialKeysMSEButtonsModel.get_response_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.GET_CAPABILITIES)
        self.reset_all_cid_report_settings_response_cls = SpecialKeysMSEButtonsModel.get_response_cls(
            self.VERSION, SpecialKeysMSEButtonsModel.INDEX.RESET_ALL_CID_REPORT_SETTINGS)
    # end def __init__

    def get_max_function_index(self):
        # See ``SpecialKeysMSEButtonsInterface.get_max_function_index``
        return SpecialKeysMSEButtonsModel.get_base_cls().MAX_FUNCTION_INDEX_V6
    # end def get_max_function_index
# end class SpecialKeysMSEButtonsV6


class GetCount(SpecialKeysMSEButtons):
    """
    Define ``GetCount`` implementation class for all versions

    Request the number of Keys and/or MSE Buttons defined.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = GetCountResponse.FUNCTION_INDEX
    # end def __init__
# end class GetCount


class GetCountResponse(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCount response implementation class

    Returns the number of Keys and/or MSE Buttons defined.

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
    VERSION = (0, 1, 2, 3, 4, 5, 6,)
    FUNCTION_INDEX = 0

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        COUNT = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        COUNT = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.COUNT,
                 LEN.COUNT,
                 title='Count',
                 name='count',
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, count=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param count: The number of Control IDs in the list
        :type count: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.count = count
    # end def __init__
# end class GetCountResponse


class GetCidInfo(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidInfo implementation class

    Request a row from the control ID table. This table information describes capabilities and desired software
    handling for physical controls in the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlIdIndex            || 8            ||
    || Padding                || 16           ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID_INDEX = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID_INDEX,
                 LEN.CTRL_ID_INDEX,
                 title='CtrlIdIndex',
                 name='ctrl_id_index',
                 aliases=('index',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID_INDEX // 8),
                         CheckByte(),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id_index=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id_index:  The zero based row index to retrieve.
        :type ctrl_id_index: ``int``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = GetCidInfoV0Response.FUNCTION_INDEX
        self.ctrl_id_index = ctrl_id_index
    # end def __init__
# end class GetCidInfo


class GetCidInfoV0Response(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidInfo response version 0 implementation class

    Returns a row from the control ID table. This table information describes capabilities and desired software
    handling for physical controls in the device.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || TaskId                 || 16           ||
    || Unused                 || 1            ||
    || Persist                || 1            ||
    || Divert                 || 1            ||
    || Reprog                 || 1            ||
    || FnTog                  || 1            ||
    || HotKey                 || 1            ||
    || Fkey                   || 1            ||
    || Mouse                  || 1            ||
    || FkeyPos                || 8            ||
    || Padding                || 80           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCidInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        TASK_ID = 0xF9
        UNUSED = 0xF8
        PERSIST = 0xF7
        DIVERT = 0xF6
        REPROG = 0xF5
        FN_TOG = 0xF4
        HOT_KEY = 0xF3
        FKEY = 0xF2
        MOUSE = 0xF1
        FKEY_POS = 0xF0
        PADDING = 0xEF
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        TASK_ID = 0x10
        UNUSED = 0x01
        PERSIST = 0x01
        DIVERT = 0x01
        REPROG = 0x01
        FN_TOG = 0x01
        HOT_KEY = 0x01
        FKEY = 0x01
        MOUSE = 0x01
        FKEY_POS = 0x08
        PADDING = 0x50
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.TASK_ID,
                 LEN.TASK_ID,
                 title='TaskId',
                 name='task_id',
                 aliases=('tid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.TASK_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REPROG,
                 LEN.REPROG,
                 title='Reprog',
                 name='reprog',
                 checks=(CheckInt(0, pow(2, LEN.REPROG) - 1),)),
        BitField(FID.FN_TOG,
                 LEN.FN_TOG,
                 title='FnTog',
                 name='fn_tog',
                 checks=(CheckInt(0, pow(2, LEN.FN_TOG) - 1),)),
        BitField(FID.HOT_KEY,
                 LEN.HOT_KEY,
                 title='HotKey',
                 name='hot_key',
                 checks=(CheckInt(0, pow(2, LEN.HOT_KEY) - 1),)),
        BitField(FID.FKEY,
                 LEN.FKEY,
                 title='Fkey',
                 name='fkey',
                 checks=(CheckInt(0, pow(2, LEN.FKEY) - 1),)),
        BitField(FID.MOUSE,
                 LEN.MOUSE,
                 title='Mouse',
                 name='mouse',
                 checks=(CheckInt(0, pow(2, LEN.MOUSE) - 1),)),
        BitField(FID.FKEY_POS,
                 LEN.FKEY_POS,
                 title='FkeyPos',
                 name='fkey_pos',
                 checks=(CheckHexList(LEN.FKEY_POS // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, task_id=0, persist=False, divert=False, reprog=False,
                 fn_tog=False, hot_key=False, fkey=False, mouse=False, fkey_pos=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: Control ID for the physical control.
        :type ctrl_id: ``int``
        :param task_id: Task ID which specifies how the software should handle this physical control.
        :type task_id: ``int``
        :param persist: Flag indicating if this control can be persistently diverted to software by reporting via
                        DivertedButtonsEvent.
        :type persist: ``bool``
        :param divert: Flag indicating if this control can be temporarily diverted to software by reporting via
                       DivertedButtonsEvent.
        :type divert: ``bool``
        :param reprog: Flag indicating if the software should let the user reprogram this control.
        :type reprog: ``bool``
        :param fn_tog:  Flag indicating if this key is affected by the fnToggle setting.
        :type fn_tog: ``bool``
        :param hot_key:  Flag indicating if this control is a nonstandard key which does not reside on a function key.
        :type hot_key: ``bool``
        :param fkey:  Flag indicating if this control resides on a function key.
        :type fkey: ``bool``
        :param mouse:  Flag indicating if this control is a mouse button.
        :type mouse: ``bool``
        :param fkey_pos: For Fkey, position # (1-N) on the Fkey row of keyboard. Value 0 = position not given.
        :type fkey_pos: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.task_id = task_id
        self.unused = 0
        self.persist = persist
        self.divert = divert
        self.reprog = reprog
        self.fn_tog = fn_tog
        self.hot_key = hot_key
        self.fkey = fkey
        self.mouse = mouse
        self.fkey_pos = fkey_pos
    # end def __init__
# end class GetCidInfoV0Response


class _GetCidInfoV1ToV5ResponseMixin(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidInfo response common fields for version 1 to version 4 implementation class

    Common fields Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || TaskId                 || 16           ||
    || Virtual                || 1            ||
    || Persist                || 1            ||
    || Divert                 || 1            ||
    || Reprog                 || 1            ||
    || FnTog                  || 1            ||
    || HotKey                 || 1            ||
    || Fkey                   || 1            ||
    || Mouse                  || 1            ||
    || FkeyPos                || 8            ||
    || Group                  || 8            ||
    || GMask                  || 8            ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCidInfo,)
    FUNCTION_INDEX = 1

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        TASK_ID = 0xF9
        VIRTUAL = 0xF8
        PERSIST = 0xF7
        DIVERT = 0xF6
        REPROG = 0xF5
        FN_TOG = 0xF4
        HOT_KEY = 0xF3
        FKEY = 0xF2
        MOUSE = 0xF1
        FKEY_POS = 0xF0
        GROUP = 0xEF
        GMASK = 0xEE
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        TASK_ID = 0x10
        VIRTUAL = 0x01
        PERSIST = 0x01
        DIVERT = 0x01
        REPROG = 0x01
        FN_TOG = 0x01
        HOT_KEY = 0x01
        FKEY = 0x01
        MOUSE = 0x01
        FKEY_POS = 0x08
        GROUP = 0x08
        GMASK = 0x08
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.TASK_ID,
                 LEN.TASK_ID,
                 title='TaskId',
                 name='task_id',
                 aliases=('tid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.TASK_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.VIRTUAL,
                 LEN.VIRTUAL,
                 title='Virtual',
                 name='virtual',
                 checks=(CheckInt(0, pow(2, LEN.VIRTUAL) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REPROG,
                 LEN.REPROG,
                 title='Reprog',
                 name='reprog',
                 checks=(CheckInt(0, pow(2, LEN.REPROG) - 1),)),
        BitField(FID.FN_TOG,
                 LEN.FN_TOG,
                 title='FnTog',
                 name='fn_tog',
                 checks=(CheckInt(0, pow(2, LEN.FN_TOG) - 1),)),
        BitField(FID.HOT_KEY,
                 LEN.HOT_KEY,
                 title='HotKey',
                 name='hot_key',
                 checks=(CheckInt(0, pow(2, LEN.HOT_KEY) - 1),)),
        BitField(FID.FKEY,
                 LEN.FKEY,
                 title='Fkey',
                 name='fkey',
                 checks=(CheckInt(0, pow(2, LEN.FKEY) - 1),)),
        BitField(FID.MOUSE,
                 LEN.MOUSE,
                 title='Mouse',
                 name='mouse',
                 checks=(CheckInt(0, pow(2, LEN.MOUSE) - 1),)),
        BitField(FID.FKEY_POS,
                 LEN.FKEY_POS,
                 title='FkeyPos',
                 name='fkey_pos',
                 checks=(CheckHexList(LEN.FKEY_POS // 8),
                         CheckByte(),),),
        BitField(FID.GROUP,
                 LEN.GROUP,
                 title='Group',
                 name='group',
                 checks=(CheckHexList(LEN.GROUP // 8),
                         CheckByte(),),),
        BitField(FID.GMASK,
                 LEN.GMASK,
                 title='Gmask',
                 name='gmask',
                 checks=(CheckHexList(LEN.GMASK // 8),
                         CheckByte(),),),
    )

    def __init__(self, device_index, feature_index, ctrl_id, task_id, virtual, persist, divert, reprog, fn_tog,
                 hot_key, fkey, mouse, fkey_pos, group, gmask):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: Control ID for the physical control.
        :type ctrl_id: ``int``
        :param task_id: Task ID which specifies how the software should handle this physical control.
        :type task_id: ``int``
        :param virtual: Flag indicating if this item is not a physical control but is instead a virtual control
                        representing an optional native function on the
        :type virtual: ``bool``
        :param persist: Flag indicating if this control can be persistently diverted to software by reporting via
                        DivertedButtonsEvent.
        :type persist: ``bool``
        :param divert: Flag indicating if this control can be temporarily diverted to software by reporting via
                       DivertedButtonsEvent.
        :type divert: ``bool``
        :param reprog: Flag indicating if the software should let the user reprogram this control.
        :type reprog: ``bool``
        :param fn_tog:  Flag indicating if this key is affected by the fnToggle setting.
        :type fn_tog: ``bool``
        :param hot_key:  Flag indicating if this control is a nonstandard key which does not reside on a function key.
        :type hot_key: ``bool``
        :param fkey:  Flag indicating if this control resides on a function key.
        :type fkey: ``bool``
        :param mouse:  Flag indicating if this control is a mouse button.
        :type mouse: ``bool``
        :param fkey_pos: For Fkey, position # (1-N) on the Fkey row of keyboard. Value 0 = position not given.
        :type fkey_pos: ``int``
        :param group:  Which mapping group this control ID belongs to.
        :type group: ``int``
        :param gmask:  This control can be remapped to any control ID contained in the specified groups
        :type gmask: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.task_id = task_id
        self.virtual = virtual
        self.persist = persist
        self.divert = divert
        self.reprog = reprog
        self.fn_tog = fn_tog
        self.hot_key = hot_key
        self.fkey = fkey
        self.mouse = mouse
        self.fkey_pos = fkey_pos
        self.group = group
        self.gmask = gmask
    # end def __init__
# end class _GetCidInfoV1ToV4ResponseMixin


class GetCidInfoV1Response(_GetCidInfoV1ToV5ResponseMixin):
    """
    SpecialKeysMSEButtons GetCidInfo response version 1 implementation class

    Returns a row from the control ID table. This table information describes capabilities and desired software
    handling for physical controls in the device.

    Format:
    || @b Name                || @b Bit count ||
    || Common fields          || 104          ||
    || Padding                || 64           ||

    For Common fields see the class _GetCidInfoV1ToV4ResponseMixin.
    """
    VERSION = (1,)

    class FID(_GetCidInfoV1ToV5ResponseMixin.FID):
        """
        Field Identifiers
        """
        PADDING = 0xED
    # end class FID

    class LEN(_GetCidInfoV1ToV5ResponseMixin.LEN):
        """
        Field Lengths
        """
        PADDING = 0x40
    # end class LEN

    FIELDS = _GetCidInfoV1ToV5ResponseMixin.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, task_id=0, virtual=False, persist=False, divert=False,
                 reprog=False, fn_tog=False, hot_key=False, fkey=False, mouse=False, fkey_pos=0, group=0, gmask=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: Control ID for the physical control.
        :type ctrl_id: ``int``
        :param task_id: Task ID which specifies how the software should handle this physical control.
        :type task_id: ``int``
        :param virtual: Flag indicating if this item is not a physical control but is instead a virtual control
                        representing an optional native function on the
        :type virtual: ``bool``
        :param persist: Flag indicating if this control can be persistently diverted to software by reporting via
                        DivertedButtonsEvent.
        :type persist: ``bool``
        :param divert: Flag indicating if this control can be temporarily diverted to software by reporting via
                       DivertedButtonsEvent.
        :type divert: ``bool``
        :param reprog: Flag indicating if the software should let the user reprogram this control.
        :type reprog: ``bool``
        :param fn_tog:  Flag indicating if this key is affected by the fnToggle setting.
        :type fn_tog: ``bool``
        :param hot_key:  Flag indicating if this control is a nonstandard key which does not reside on a function key.
        :type hot_key: ``bool``
        :param fkey:  Flag indicating if this control resides on a function key.
        :type fkey: ``bool``
        :param mouse:  Flag indicating if this control is a mouse button.
        :type mouse: ``bool``
        :param fkey_pos: For Fkey, position # (1-N) on the Fkey row of keyboard. Value 0 = position not given.
        :type fkey_pos: ``int``
        :param group:  Which mapping group this control ID belongs to.
        :type group: ``int``
        :param gmask:  This control can be remapped to any control ID contained in the specified groups
        :type gmask: ``int``
        """
        super().__init__(device_index, feature_index, ctrl_id, task_id, virtual, persist, divert, reprog, fn_tog,
                         hot_key, fkey, mouse, fkey_pos, group, gmask)
    # end def __init__
# end class GetCidInfoV1Response


class GetCidInfoV2Response(_GetCidInfoV1ToV5ResponseMixin):
    """
    SpecialKeysMSEButtons GetCidInfo response version 2 implementation class

    Returns a row from the control ID table. This table information describes capabilities and desired software
    handling for physical controls in the device.

    Format:
    || @b Name                || @b Bit count ||
    || Common fields          || 104          ||
    || Unused                 || 7            ||
    || RawXY                  || 1            ||
    || Padding                || 56           ||

    For Common fields see the class _GetCidInfoV1ToV4ResponseMixin.
    """
    VERSION = (2,)

    class FID(_GetCidInfoV1ToV5ResponseMixin.FID):
        """
        Field Identifiers
        """
        UNUSED = 0xED
        RAW_XY = 0xEC
        PADDING = 0xEB
    # end class FID

    class LEN(_GetCidInfoV1ToV5ResponseMixin.LEN):
        """
        Field Lengths
        """
        UNUSED = 0x07
        RAW_XY = 0x01
        PADDING = 0x38
    # end class LEN

    FIELDS = _GetCidInfoV1ToV5ResponseMixin.FIELDS + (
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, task_id=0, virtual=False, persist=False, divert=False,
                 reprog=False, fn_tog=False, hot_key=False, fkey=False, mouse=False, fkey_pos=0, group=0, gmask=0,
                 raw_xy=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: Control ID for the physical control.
        :type ctrl_id: ``int``
        :param task_id: Task ID which specifies how the software should handle this physical control.
        :type task_id: ``int``
        :param virtual: Flag indicating if this item is not a physical control but is instead a virtual control
                        representing an optional native function on the
        :type virtual: ``bool``
        :param persist: Flag indicating if this control can be persistently diverted to software by reporting via
                        DivertedButtonsEvent.
        :type persist: ``bool``
        :param divert: Flag indicating if this control can be temporarily diverted to software by reporting via
                       DivertedButtonsEvent.
        :type divert: ``bool``
        :param reprog: Flag indicating if the software should let the user reprogram this control.
        :type reprog: ``bool``
        :param fn_tog:  Flag indicating if this key is affected by the fnToggle setting.
        :type fn_tog: ``bool``
        :param hot_key:  Flag indicating if this control is a nonstandard key which does not reside on a function key.
        :type hot_key: ``bool``
        :param fkey:  Flag indicating if this control resides on a function key.
        :type fkey: ``bool``
        :param mouse:  Flag indicating if this control is a mouse button.
        :type mouse: ``bool``
        :param fkey_pos: For Fkey, position # (1-N) on the Fkey row of keyboard. Value 0 = position not given.
        :type fkey_pos: ``int``
        :param group:  Which mapping group this control ID belongs to.
        :type group: ``int``
        :param gmask:  This control can be remapped to any control ID contained in the specified groups
        :type gmask: ``int``
        :param raw_xy:  Flag indicating if this control  has capability of being a programmed as a gesture button.
        :type raw_xy: ``bool``
        """
        super().__init__(device_index, feature_index, ctrl_id, task_id, virtual, persist, divert, reprog, fn_tog,
                         hot_key, fkey, mouse, fkey_pos, group, gmask)

        self.unused = 0
        self.raw_xy = raw_xy
    # end def __init__
# end class GetCidInfoV2Response


class GetCidInfoV3Response(_GetCidInfoV1ToV5ResponseMixin):
    """
    SpecialKeysMSEButtons GetCidInfo response version 3 implementation class

    Returns a row from the control ID table. This table information describes capabilities and desired software
    handling for physical controls in the device.

    Format:
    || @b Name                || @b Bit count ||
    || Common fields          || 104          ||
    || Unused                 || 6            ||
    || ForceRawXY             || 1            ||
    || RawXY                  || 1            ||
    || Padding                || 56           ||

    For Common fields see the class _GetCidInfoV1ToV4ResponseMixin.
    """
    VERSION = (3,)

    class FID(_GetCidInfoV1ToV5ResponseMixin.FID):
        """
        Field Identifiers
        """
        UNUSED = 0xED
        FORCE_RAW_XY = 0xEC
        RAW_XY = 0xEB
        PADDING = 0xEA
    # end class FID

    class LEN(_GetCidInfoV1ToV5ResponseMixin.LEN):
        """
        Field Lengths
        """
        UNUSED = 0x06
        FORCE_RAW_XY = 0x01
        RAW_XY = 0x01
        PADDING = 0x38
    # end class LEN

    FIELDS = _GetCidInfoV1ToV5ResponseMixin.FIELDS + (
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, task_id=0, virtual=False, persist=False, divert=False,
                 reprog=False, fn_tog=False, hot_key=False, fkey=False, mouse=False, fkey_pos=0, group=0, gmask=0,
                 force_raw_xy=False, raw_xy=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: Control ID for the physical control.
        :type ctrl_id: ``int``
        :param task_id: Task ID which specifies how the software should handle this physical control.
        :type task_id: ``int``
        :param virtual: Flag indicating if this item is not a physical control but is instead a virtual control
                        representing an optional native function on the
        :type virtual: ``bool``
        :param persist: Flag indicating if this control can be persistently diverted to software by reporting via
                        DivertedButtonsEvent.
        :type persist: ``bool``
        :param divert: Flag indicating if this control can be temporarily diverted to software by reporting via
                       DivertedButtonsEvent.
        :type divert: ``bool``
        :param reprog: Flag indicating if the software should let the user reprogram this control.
        :type reprog: ``bool``
        :param fn_tog:  Flag indicating if this key is affected by the fnToggle setting.
        :type fn_tog: ``bool``
        :param hot_key:  Flag indicating if this control is a nonstandard key which does not reside on a function key.
        :type hot_key: ``bool``
        :param fkey:  Flag indicating if this control resides on a function key.
        :type fkey: ``bool``
        :param mouse:  Flag indicating if this control is a mouse button.
        :type mouse: ``bool``
        :param fkey_pos: For Fkey, position # (1-N) on the Fkey row of keyboard. Value 0 = position not given.
        :type fkey_pos: ``int``
        :param group:  Which mapping group this control ID belongs to.
        :type group: ``int``
        :param gmask:  This control can be remapped to any control ID contained in the specified groups
        :type gmask: ``int``
        :param force_raw_xy:  Flag indicating if this control has capability of being programmed as a gesture button
                              yet the activation of the raw XY function will be initiated by SW without the need of
                              any user action (Enables 1+1=3).
        :type force_raw_xy: ``bool``
        :param raw_xy:  Flag indicating if this control has capability of being a programmed as a gesture button.
        :type raw_xy: ``bool``
        """
        super().__init__(device_index, feature_index, ctrl_id, task_id, virtual, persist, divert, reprog, fn_tog,
                         hot_key, fkey, mouse, fkey_pos, group, gmask)

        self.unused = 0
        self.force_raw_xy = force_raw_xy
        self.raw_xy = raw_xy
    # end def __init__
# end class GetCidInfoV3Response


class GetCidInfoV4Response(_GetCidInfoV1ToV5ResponseMixin):
    """
    SpecialKeysMSEButtons GetCidInfo response version 4 implementation class

    Returns a row from the control ID table. This table information describes capabilities and desired software
    handling for physical controls in the device.

    Format:
    || @b Name                || @b Bit count ||
    || Common fields          || 104          ||
    || Unused                 || 5            ||
    || AnalyticsKeyEvents     || 1            ||
    || ForceRawXY             || 1            ||
    || RawXY                  || 1            ||
    || Padding                || 56           ||
    """
    VERSION = (4,)

    class FID(_GetCidInfoV1ToV5ResponseMixin.FID):
        """
        Field Identifiers
        """
        UNUSED = 0xED
        ANALYTICS_KEY_EVENTS = 0xEC
        FORCE_RAW_XY = 0xEB
        RAW_XY = 0xEA
        PADDING = 0xE9
    # end class FID

    class LEN(_GetCidInfoV1ToV5ResponseMixin.LEN):
        """
        Field Lengths
        """
        UNUSED = 0x05
        ANALYTICS_KEY_EVENTS = 0x01
        FORCE_RAW_XY = 0x01
        RAW_XY = 0x01
        PADDING = 0x38
    # end class LEN

    FIELDS = _GetCidInfoV1ToV5ResponseMixin.FIELDS + (
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.ANALYTICS_KEY_EVENTS,
                 LEN.ANALYTICS_KEY_EVENTS,
                 title='AnalyticsKeyEvents',
                 name='analytics_key_events',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVENTS) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, task_id=0, virtual=False, persist=False, divert=False,
                 reprog=False, fn_tog=False, hot_key=False, fkey=False, mouse=False, fkey_pos=0, group=0, gmask=0,
                 analytics_key_events=False, force_raw_xy=False, raw_xy=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: Control ID for the physical control.
        :type ctrl_id: ``int``
        :param task_id: Task ID which specifies how the software should handle this physical control.
        :type task_id: ``int``
        :param virtual: Flag indicating if this item is not a physical control but is instead a virtual control
                        representing an optional native function on the
        :type virtual: ``bool``
        :param persist: Flag indicating if this control can be persistently diverted to software by reporting via
                        DivertedButtonsEvent.
        :type persist: ``bool``
        :param divert: Flag indicating if this control can be temporarily diverted to software by reporting via
                       DivertedButtonsEvent.
        :type divert: ``bool``
        :param reprog: Flag indicating if the software should let the user reprogram this control.
        :type reprog: ``bool``
        :param fn_tog:  Flag indicating if this key is affected by the fnToggle setting.
        :type fn_tog: ``bool``
        :param hot_key:  Flag indicating if this control is a nonstandard key which does not reside on a function key.
        :type hot_key: ``bool``
        :param fkey:  Flag indicating if this control resides on a function key.
        :type fkey: ``bool``
        :param mouse:  Flag indicating if this control is a mouse button.
        :type mouse: ``bool``
        :param fkey_pos: For Fkey, position # (1-N) on the Fkey row of keyboard. Value 0 = position not given.
        :type fkey_pos: ``int``
        :param group:  Which mapping group this control ID belongs to.
        :type group: ``int``
        :param gmask:  This control can be remapped to any control ID contained in the specified groups
        :type gmask: ``int``
        :param analytics_key_events:  Flag indicating if this controlhas the capability of sending project-dependent
                                      analytics key events to the SW.
        :type analytics_key_events: ``bool``
        :param force_raw_xy:  Flag indicating if this control has capability of being programmed as a gesture button
                              yet the activation of the raw XY function will be initiated by SW without the need of
                              any user action (Enables 1+1=3).
        :type force_raw_xy: ``bool``
        :param raw_xy:  Flag indicating if this control has capability of being a programmed as a gesture button.
        :type raw_xy: ``bool``
        """
        super().__init__(device_index, feature_index, ctrl_id, task_id, virtual, persist, divert, reprog, fn_tog,
                         hot_key, fkey, mouse, fkey_pos, group, gmask)

        self.unused = 0
        self.analytics_key_events = analytics_key_events
        self.force_raw_xy = force_raw_xy
        self.raw_xy = raw_xy
    # end def __init__
# end class GetCidInfoV4Response


class GetCidInfoV5toV6Response(_GetCidInfoV1ToV5ResponseMixin):
    """
    SpecialKeysMSEButtons GetCidInfo response version 5 implementation class

    Returns a row from the control ID table. This table information describes capabilities and desired software
    handling for physical controls in the device.

    Format:
    || @b Name                || @b Bit count ||
    || Common fields          || 104          ||
    || Unused                 || 4            ||
    || RawWheel               || 1            ||
    || AnalyticsKeyEvents     || 1            ||
    || ForceRawXY             || 1            ||
    || RawXY                  || 1            ||
    || Padding                || 56           ||
    """
    VERSION = (5, 6,)

    class FID(_GetCidInfoV1ToV5ResponseMixin.FID):
        """
        Field Identifiers
        """
        UNUSED = 0xED
        RAW_WHEEL = 0xEC
        ANALYTICS_KEY_EVENTS = 0xEB
        FORCE_RAW_XY = 0xEA
        RAW_XY = 0xE9
        PADDING = 0xE8
    # end class FID

    class LEN(_GetCidInfoV1ToV5ResponseMixin.LEN):
        """
        Field Lengths
        """
        UNUSED = 0x04
        RAW_WHEEL = 0x01
        ANALYTICS_KEY_EVENTS = 0x01
        FORCE_RAW_XY = 0x01
        RAW_XY = 0x01
        PADDING = 0x38
    # end class LEN

    FIELDS = _GetCidInfoV1ToV5ResponseMixin.FIELDS + (
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.RAW_WHEEL,
                 LEN.RAW_WHEEL,
                 title='RawWheel',
                 name='raw_wheel',
                 checks=(CheckInt(0, pow(2, LEN.RAW_WHEEL) - 1),)),
        BitField(FID.ANALYTICS_KEY_EVENTS,
                 LEN.ANALYTICS_KEY_EVENTS,
                 title='AnalyticsKeyEvents',
                 name='analytics_key_events',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVENTS) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, task_id=0, virtual=False, persist=False, divert=False,
                 reprog=False, fn_tog=False, hot_key=False, fkey=False, mouse=False, fkey_pos=0, group=0, gmask=0,
                 raw_wheel=False, analytics_key_events=False, force_raw_xy=False, raw_xy=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: Control ID for the physical control.
        :type ctrl_id: ``int``
        :param task_id: Task ID which specifies how the software should handle this physical control.
        :type task_id: ``int``
        :param virtual: Flag indicating if this item is not a physical control but is instead a virtual control
                        representing an optional native function on the
        :type virtual: ``bool``
        :param persist: Flag indicating if this control can be persistently diverted to software by reporting via
                        DivertedButtonsEvent.
        :type persist: ``bool``
        :param divert: Flag indicating if this control can be temporarily diverted to software by reporting via
                       DivertedButtonsEvent.
        :type divert: ``bool``
        :param reprog: Flag indicating if the software should let the user reprogram this control.
        :type reprog: ``bool``
        :param fn_tog:  Flag indicating if this key is affected by the fnToggle setting.
        :type fn_tog: ``bool``
        :param hot_key:  Flag indicating if this control is a nonstandard key which does not reside on a function key.
        :type hot_key: ``bool``
        :param fkey:  Flag indicating if this control resides on a function key.
        :type fkey: ``bool``
        :param mouse:  Flag indicating if this control is a mouse button.
        :type mouse: ``bool``
        :param fkey_pos: For Fkey, position # (1-N) on the Fkey row of keyboard. Value 0 = position not given.
        :type fkey_pos: ``int``
        :param group:  Which mapping group this control ID belongs to.
        :type group: ``int``
        :param gmask:  This control can be remapped to any control ID contained in the specified groups
        :type gmask: ``int``
        :param analytics_key_events:  Flag indicating if this controlhas the capability of sending project-dependent
                                      analytics key events to the SW.
        :type analytics_key_events: ``bool``
        :param force_raw_xy:  Flag indicating if this control has capability of being programmed as a gesture button
                              yet the activation of the raw XY function will be initiated by SW without the need of
                              any user action (Enables 1+1=3).
        :type force_raw_xy: ``bool``
        :param raw_xy:  Flag indicating if this control has capability of being a programmed as a gesture button.
        :type raw_xy: ``bool``
        """
        super().__init__(device_index, feature_index, ctrl_id, task_id, virtual, persist, divert, reprog, fn_tog,
                         hot_key, fkey, mouse, fkey_pos, group, gmask)

        self.unused = 0
        self.raw_wheel = raw_wheel
        self.analytics_key_events = analytics_key_events
        self.force_raw_xy = force_raw_xy
        self.raw_xy = raw_xy
    # end def __init__
# end class GetCidInfoV5toV6Response


class GetCidReporting(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidReporting implementation class

    Request the current reporting method for a control ID. The current reporting method will have been previously
    configured via the function SetCidReporting.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Padding                || 8            ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        PADDING = 0xF8
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        PADDING = 0x08
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = GetCidReportingV0Response.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
    # end def __init__
# end class GetCidReporting


class GetCidReportingV0Response(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidReporting response version 0 implementation class

    Returns the ctrlID and the "Reporting by Control ID only" current and persistent flag state.
    All control IDs with the "Reporting by controlID supported" flag must support this function.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused1                || 5            ||
    || Persist                || 1            ||
    || Unused2                || 1            ||
    || Divert                 || 1            ||
    || Padding                || 104          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCidReporting,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED1 = 0xF9
        PERSIST = 0xF8
        UNUSED2 = 0xF7
        DIVERT = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED1 = 0x05
        PERSIST = 0x01
        UNUSED2 = 0x01
        DIVERT = 0x01
        PADDING = 0x68
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED1,
                 LEN.UNUSED1,
                 title='Unused1',
                 name='unused1',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.UNUSED2,
                 LEN.UNUSED2,
                 title='Unused2',
                 name='unused2',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED2) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, persist=False, divert=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param persist: Flag indicating that the control is being persistently diverted.
        :type persist: ``bool``
        :param divert: Flag indicating that the control is being temporarily diverted.
        :type divert: ``bool``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused1 = 0
        self.persist = persist
        self.unused2 = 0
        self.divert = divert
    # end def __init__
# end class GetCidReportingV0Response


class GetCidReportingV1Response(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidReporting response version 1 implementation class

    Returns  the current reporting method for a control ID. The current reporting method will have been previously
    configured via the function SetCidReportingV1

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused1                || 5            ||
    || Persist                || 1            ||
    || Unused2                || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Padding                || 88           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCidReporting,)
    VERSION = (1,)
    FUNCTION_INDEX = 2

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED1 = 0xF9
        PERSIST = 0xF8
        UNUSED2 = 0xF7
        DIVERT = 0xF6
        REMAP = 0xF5
        PADDING = 0xF4
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED1 = 0x05
        PERSIST = 0x01
        UNUSED2 = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED1,
                 LEN.UNUSED1,
                 title='Unused1',
                 name='unused1',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.UNUSED2,
                 LEN.UNUSED2,
                 title='Unused2',
                 name='unused2',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED2) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, persist=False, divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param persist: Flag indicating that the control is being persistently diverted.
        :type persist: ``bool``
        :param divert: Flag indicating that the control is being temporarily diverted.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused1 = 0
        self.persist = persist
        self.unused2 = 0
        self.divert = divert
        self.remap = remap
    # end def __init__
# end class GetCidReportingV1Response


class GetCidReportingV2Response(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidReporting response version 2 implementation class

    Returns  the current reporting method for a control ID. The current reporting method will have been previously
    configured via the function SetCidReportingV2

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused1                || 3            ||
    || RawXY                  || 1            ||
    || Unused2                || 1            ||
    || Persist                || 1            ||
    || Unused3                || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Padding                || 88           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCidReporting,)
    VERSION = (2,)
    FUNCTION_INDEX = 2

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED1 = 0xF9
        RAW_XY = 0xF8
        UNUSED2 = 0xF7
        PERSIST = 0xF6
        UNUSED3 = 0xF5
        DIVERT = 0xF4
        REMAP = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED1 = 0x03
        RAW_XY = 0x01
        UNUSED2 = 0x01
        PERSIST = 0x01
        UNUSED3 = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED1,
                 LEN.UNUSED1,
                 title='Unused1',
                 name='unused1',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.UNUSED2,
                 LEN.UNUSED2,
                 title='Unused2',
                 name='unused2',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED2) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.UNUSED3,
                 LEN.UNUSED3,
                 title='Unused3',
                 name='unused3',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED3) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, raw_xy=False, persist=False, divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param raw_xy: Flag indicating that the control is being temporarily diverted along with mouse xy reports.
        :type raw_xy: ``bool``
        :param persist: Flag indicating that the control is being persistently diverted.
        :type persist: ``bool``
        :param divert: Flag indicating that the control is being temporarily diverted.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused1 = 0
        self.raw_xy = raw_xy
        self.unused2 = 0
        self.persist = persist
        self.unused3 = 0
        self.divert = divert
        self.remap = remap
    # end def __init__
# end class GetCidReportingV2Response


class GetCidReportingV3Response(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidReporting response version 3 implementation class

    Returns  the current reporting method for a control ID. The current reporting method will have been previously
    configured via the function SetCidReportingV3

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused1                || 1            ||
    || ForceRawXY             || 1            ||
    || Unused2                || 1            ||
    || RawXY                  || 1            ||
    || Unused3                || 1            ||
    || Persist                || 1            ||
    || Unused4                || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Padding                || 88           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCidReporting,)
    VERSION = (3,)
    FUNCTION_INDEX = 2

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED1 = 0xF9
        FORCE_RAW_XY = 0xF8
        UNUSED2 = 0xF7
        RAW_XY = 0xF6
        UNUSED3 = 0xF5
        PERSIST = 0xF4
        UNUSED4 = 0xF3
        DIVERT = 0xF2
        REMAP = 0xF1
        PADDING = 0xF0
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED1 = 0x01
        FORCE_RAW_XY = 0x01
        UNUSED2 = 0x01
        RAW_XY = 0x01
        UNUSED3 = 0x01
        PERSIST = 0x01
        UNUSED4 = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED1,
                 LEN.UNUSED1,
                 title='Unused1',
                 name='unused1',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.UNUSED2,
                 LEN.UNUSED2,
                 title='Unused2',
                 name='unused2',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.UNUSED3,
                 LEN.UNUSED3,
                 title='Unused3',
                 name='unused3',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.UNUSED4,
                 LEN.UNUSED4,
                 title='Unused4',
                 name='unused4',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED4) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy=False, raw_xy=False, persist=False,
                 divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy: Flag indicating that the control is being force diverted by SW. i.e. no need of user
                             action to send raw XY.
        :type force_raw_xy: ``bool``
        :param raw_xy: Flag indicating that the control is being temporarily diverted along with mouse xy reports.
        :type raw_xy: ``bool``
        :param persist: Flag indicating that the control is being persistently diverted.
        :type persist: ``bool``
        :param divert: Flag indicating that the control is being temporarily diverted.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused1 = 0
        self.force_raw_xy = force_raw_xy
        self.unused2 = 0
        self.raw_xy = raw_xy
        self.unused3 = 0
        self.persist = persist
        self.unused4 = 0
        self.divert = divert
        self.remap = remap
    # end def __init__
# end class GetCidReportingV3Response


class GetCidReportingV4Response(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidReporting response version 4 implementation class

    Returns  the current reporting method for a control ID. The current reporting method will have been previously
    configured via the function SetCidReportingV4

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused1                || 1            ||
    || ForceRawXY             || 1            ||
    || Unused2                || 1            ||
    || RawXY                  || 1            ||
    || Unused3                || 1            ||
    || Persist                || 1            ||
    || Unused4                || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Unused5                || 7            ||
    || AnalyticsKeyEvt        || 1            ||
    || Padding                || 80           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCidReporting,)
    VERSION = (4,)
    FUNCTION_INDEX = 2

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED1 = 0xF9
        FORCE_RAW_XY = 0xF8
        UNUSED2 = 0xF7
        RAW_XY = 0xF6
        UNUSED3 = 0xF5
        PERSIST = 0xF4
        UNUSED4 = 0xF3
        DIVERT = 0xF2
        REMAP = 0xF1
        UNUSED5 = 0xF0
        ANALYTICS_KEY_EVT = 0xEF
        PADDING = 0xEE
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED1 = 0x01
        FORCE_RAW_XY = 0x01
        UNUSED2 = 0x01
        RAW_XY = 0x01
        UNUSED3 = 0x01
        PERSIST = 0x01
        UNUSED4 = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        UNUSED5 = 0x07
        ANALYTICS_KEY_EVT = 0x01
        PADDING = 0x50
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED1,
                 LEN.UNUSED1,
                 title='Unused1',
                 name='unused1',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.UNUSED2,
                 LEN.UNUSED2,
                 title='Unused2',
                 name='unused2',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.UNUSED3,
                 LEN.UNUSED3,
                 title='Unused3',
                 name='unused3',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.UNUSED4,
                 LEN.UNUSED4,
                 title='Unused4',
                 name='unused4',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED4) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED5,
                 LEN.UNUSED5,
                 title='Unused5',
                 name='unused5',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED5) - 1),)),
        BitField(FID.ANALYTICS_KEY_EVT,
                 LEN.ANALYTICS_KEY_EVT,
                 title='AnalyticsKeyEvt',
                 name='analytics_key_evt',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVT) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy=False, raw_xy=False, persist=False,
                 divert=False, remap=0, analytics_key_evt=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy: Flag indicating that the control is being force diverted by SW. i.e. no need of user
                             action to send raw XY.
        :type force_raw_xy: ``bool``
        :param raw_xy: Flag indicating that the control is being temporarily diverted along with mouse xy reports.
        :type raw_xy: ``bool``
        :param persist: Flag indicating that the control is being persistently diverted.
        :type persist: ``bool``
        :param divert: Flag indicating that the control is being temporarily diverted.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        :param analytics_key_evt: Flag indicating that the control is temporarily reporting project-dependent
                                  analytics key events to the SW.
        :type analytics_key_evt: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused1 = 0
        self.force_raw_xy = force_raw_xy
        self.unused2 = 0
        self.raw_xy = raw_xy
        self.unused3 = 0
        self.persist = persist
        self.unused4 = 0
        self.divert = divert
        self.remap = remap
        self.unused5 = 0
        self.analytics_key_evt = analytics_key_evt
    # end def __init__
# end class GetCidReportingV4Response


class GetCidReportingV5toV6Response(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons GetCidReporting response version 5 implementation class

    Returns  the current reporting method for a control ID. The current reporting method will have been previously
    configured via the function SetCidReportingV4

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused1                || 1            ||
    || ForceRawXY             || 1            ||
    || Unused2                || 1            ||
    || RawXY                  || 1            ||
    || Unused3                || 1            ||
    || Persist                || 1            ||
    || Unused4                || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Unused5                || 5            ||
    || RawWheel               || 1            ||
    || Unused6                || 1            ||
    || AnalyticsKeyEvt        || 1            ||
    || Padding                || 80           ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCidReporting,)
    VERSION = (5, 6,)
    FUNCTION_INDEX = 2

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED1 = 0xF9
        FORCE_RAW_XY = 0xF8
        UNUSED2 = 0xF7
        RAW_XY = 0xF6
        UNUSED3 = 0xF5
        PERSIST = 0xF4
        UNUSED4 = 0xF3
        DIVERT = 0xF2
        REMAP = 0xF1
        UNUSED5 = 0xF0
        RAW_WHEEL = 0xEF
        UNUSED6 = 0xEE
        ANALYTICS_KEY_EVT = 0xED
        PADDING = 0xEC
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED1 = 0x01
        FORCE_RAW_XY = 0x01
        UNUSED2 = 0x01
        RAW_XY = 0x01
        UNUSED3 = 0x01
        PERSIST = 0x01
        UNUSED4 = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        UNUSED5 = 0x05
        RAW_WHEEL = 0x01
        UNUSED6 = 0x01
        ANALYTICS_KEY_EVT = 0x01
        PADDING = 0x50
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED1,
                 LEN.UNUSED1,
                 title='Unused1',
                 name='unused1',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.UNUSED2,
                 LEN.UNUSED2,
                 title='Unused2',
                 name='unused2',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.UNUSED3,
                 LEN.UNUSED3,
                 title='Unused3',
                 name='unused3',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED1) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.UNUSED4,
                 LEN.UNUSED4,
                 title='Unused4',
                 name='unused4',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED4) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED5,
                 LEN.UNUSED5,
                 title='Unused5',
                 name='unused5',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED5) - 1),)),
        BitField(FID.RAW_WHEEL,
                 LEN.RAW_WHEEL,
                 title='RawWheel',
                 name='raw_wheel',
                 checks=(CheckInt(0, pow(2, LEN.RAW_WHEEL) - 1),)),
        BitField(FID.UNUSED6,
                 LEN.UNUSED6,
                 title='Unused6',
                 name='unused6',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED6) - 1),)),
        BitField(FID.ANALYTICS_KEY_EVT,
                 LEN.ANALYTICS_KEY_EVT,
                 title='AnalyticsKeyEvt',
                 name='analytics_key_evt',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVT) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy=False, raw_xy=False, persist=False,
                 divert=False, remap=0, raw_wheel=False, analytics_key_evt=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy: Flag indicating that the control is being force diverted by SW. i.e. no need of user
                             action to send raw XY.
        :type force_raw_xy: ``bool``
        :param raw_xy: Flag indicating that the control is being temporarily diverted along with mouse xy reports.
        :type raw_xy: ``bool``
        :param persist: Flag indicating that the control is being persistently diverted.
        :type persist: ``bool``
        :param divert: Flag indicating that the control is being temporarily diverted.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        :param raw_wheel: Flag which causes this control and all raw mouse wheel reports to temporarily be diverted
                          to software via [event4] divertedRawWheelEvent during wheel scrolling.
        :type raw_wheel: ``bool``
        :param analytics_key_evt: Flag indicating that the control is temporarily reporting project-dependent
                                  analytics key events to the SW.
        :type analytics_key_evt: ``bool``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused1 = 0
        self.force_raw_xy = force_raw_xy
        self.unused2 = 0
        self.raw_xy = raw_xy
        self.unused3 = 0
        self.persist = persist
        self.unused4 = 0
        self.divert = divert
        self.remap = remap
        self.unused5 = 0
        self.raw_wheel = raw_wheel
        self.unused6 = 0
        self.analytics_key_evt = analytics_key_evt
    # end def __init__
# end class GetCidReportingV5toV6Response


class SetCidReportingV0(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons SetCidReporting version 0 implementation class

    This configures the current reporting method for a control ID. If successful, the request packet is echoed
    as the response.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused                 || 4            ||
    || PersistValid           || 1            ||
    || Persist                || 1            ||
    || DivertValid            || 1            ||
    || Divert                 || 1            ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED = 0xF9
        PERSIST_VALID = 0xF8
        PERSIST = 0xF7
        DIVERT_VALID = 0xF6
        DIVERT = 0xF5
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED = 0x04
        PERSIST_VALID = 0x01
        PERSIST = 0x01
        DIVERT_VALID = 0x01
        DIVERT = 0x01
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.PERSIST_VALID,
                 LEN.PERSIST_VALID,
                 title='PersistValid',
                 name='persist_valid',
                 aliases=('p_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.PERSIST_VALID) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.DIVERT_VALID,
                 LEN.DIVERT_VALID,
                 title='DivertValid',
                 name='divert_valid',
                 aliases=('d_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.DIVERT_VALID) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, persist_valid=False, persist=False, divert_valid=False,
                 divert=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = SetCidReportingV0Response.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused = 0
        self.persist_valid = persist_valid
        self.persist = persist
        self.divert_valid = divert_valid
        self.divert = divert
    # end def __init__
# end class SetCidReportingV0


class SetCidReportingV1(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons SetCidReporting version 1 implementation class

    This configures the current reporting method for a control ID. If successful, the request packet is echoed
    as the response.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused                 || 4            ||
    || PersistValid           || 1            ||
    || Persist                || 1            ||
    || DivertValid            || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Padding                || 88           ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED = 0xF9
        PERSIST_VALID = 0xF8
        PERSIST = 0xF7
        DIVERT_VALID = 0xF6
        DIVERT = 0xF5
        REMAP = 0xF4
        PADDING = 0xF3
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED = 0x04
        PERSIST_VALID = 0x01
        PERSIST = 0x01
        DIVERT_VALID = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.PERSIST_VALID,
                 LEN.PERSIST_VALID,
                 title='PersistValid',
                 name='persist_valid',
                 aliases=('p_valid',),    # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.PERSIST_VALID) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.DIVERT_VALID,
                 LEN.DIVERT_VALID,
                 title='DivertValid',
                 name='divert_valid',
                 aliases=('d_valid',),    # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.DIVERT_VALID) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, persist_valid=False, persist=False, divert_valid=False,
                 divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID to remap this control to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = SetCidReportingV1Response.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused = 0
        self.persist_valid = persist_valid
        self.persist = persist
        self.divert_valid = divert_valid
        self.divert = divert
        self.remap = remap
    # end def __init__
# end class SetCidReportingV1


class SetCidReportingV2(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons SetCidReporting version 2 implementation class

    This configures the current reporting method for a control ID. If successful, the request packet is echoed
    as the response.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || Unused                 || 2            ||
    || RawXYValid             || 1            ||
    || RawXY                  || 1            ||
    || PersistValid           || 1            ||
    || Persist                || 1            ||
    || DivertValid            || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Padding                || 88           ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        UNUSED = 0xF9
        RAW_XY_VALID = 0xF8
        RAW_XY = 0xF7
        PERSIST_VALID = 0xF6
        PERSIST = 0xF5
        DIVERT_VALID = 0xF4
        DIVERT = 0xF3
        REMAP = 0xF2
        PADDING = 0xF1
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        UNUSED = 0x02
        RAW_XY_VALID = 0x01
        RAW_XY = 0x01
        PERSIST_VALID = 0x01
        PERSIST = 0x01
        DIVERT_VALID = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.RAW_XY_VALID,
                 LEN.RAW_XY_VALID,
                 title='RawXYValid',
                 name='raw_xy_valid',
                 aliases=('r_valid',),    # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY_VALID) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.PERSIST_VALID,
                 LEN.PERSIST_VALID,
                 title='PersistValid',
                 name='persist_valid',
                 aliases=('p_valid',),    # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.PERSIST_VALID) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.DIVERT_VALID,
                 LEN.DIVERT_VALID,
                 title='DivertValid',
                 name='divert_valid',
                 aliases=('d_valid',),    # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.DIVERT_VALID) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, raw_xy_valid=False, raw_xy=False, persist_valid=False,
                 persist=False, divert_valid=False, divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param raw_xy_valid: Flag which indicates that the raw xy flag is valid and device should update the
                              temporary divert state of this control ID.
        :type raw_xy_valid: ``bool``
        :param raw_xy: Flag which causes this control and all raw mouse move reports to temporarily be diverted to
                       software via divertedRawMouseXYEvent.
        :type raw_xy: ``bool``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID to remap this control to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = SetCidReportingV2Response.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.unused = 0
        self.raw_xy_valid = raw_xy_valid
        self.raw_xy = raw_xy
        self.persist_valid = persist_valid
        self.persist = persist
        self.divert_valid = divert_valid
        self.divert = divert
        self.remap = remap
    # end def __init__
# end class SetCidReportingV2


class SetCidReportingV3(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons SetCidReporting version 3 implementation class

    This configures the current reporting method for a control ID. If successful, the request packet is echoed
    as the response.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || ForceRawXYValid        || 1            ||
    || ForceRawXY             || 1            ||
    || RawXYValid             || 1            ||
    || RawXY                  || 1            ||
    || PersistValid           || 1            ||
    || Persist                || 1            ||
    || DivertValid            || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Padding                || 88           ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        FORCE_RAW_XY_VALID = 0xF9
        FORCE_RAW_XY = 0xF8
        RAW_XY_VALID = 0xF7
        RAW_XY = 0xF6
        PERSIST_VALID = 0xF5
        PERSIST = 0xF4
        DIVERT_VALID = 0xF3
        DIVERT = 0xF2
        REMAP = 0xF1
        PADDING = 0xF0
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        FORCE_RAW_XY_VALID = 0x01
        FORCE_RAW_XY = 0x01
        RAW_XY_VALID = 0x01
        RAW_XY = 0x01
        PERSIST_VALID = 0x01
        PERSIST = 0x01
        DIVERT_VALID = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.FORCE_RAW_XY_VALID,
                 LEN.FORCE_RAW_XY_VALID,
                 title='ForceRawXYValid',
                 name='force_raw_xy_valid',
                 aliases=('f_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY_VALID) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.RAW_XY_VALID,
                 LEN.RAW_XY_VALID,
                 title='RawXYValid',
                 name='raw_xy_valid',
                 aliases=('r_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY_VALID) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.PERSIST_VALID,
                 LEN.PERSIST_VALID,
                 title='PersistValid',
                 name='persist_valid',
                 aliases=('p_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.PERSIST_VALID) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.DIVERT_VALID,
                 LEN.DIVERT_VALID,
                 title='DivertValid',
                 name='divert_valid',
                 aliases=('d_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.DIVERT_VALID) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy_valid=False, force_raw_xy=False,
                 raw_xy_valid=False, raw_xy=False, persist_valid=False, persist=False, divert_valid=False,
                 divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy_valid: Flag which indicates that the forceRawXY flag is valid and device should update the
                                   persistant forceRawXY state of this control ID.
        :type force_raw_xy_valid: ``bool``
        :param force_raw_xy: Flag which causes this control is being force diverted by SW.
        :type force_raw_xy: ``bool``
        :param raw_xy_valid: Flag which indicates that the raw xy flag is valid and device should update the
                              temporary divert state of this control ID.
        :type raw_xy_valid: ``bool``
        :param raw_xy: Flag which causes this control and all raw mouse move reports to temporarily be diverted to
                       software via divertedRawMouseXYEvent.
        :type raw_xy: ``bool``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID to remap this control to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = SetCidReportingV3Response.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.force_raw_xy_valid = force_raw_xy_valid
        self.force_raw_xy = force_raw_xy
        self.raw_xy_valid = raw_xy_valid
        self.raw_xy = raw_xy
        self.persist_valid = persist_valid
        self.persist = persist
        self.divert_valid = divert_valid
        self.divert = divert
        self.remap = remap
    # end def __init__
# end class SetCidReportingV3


class SetCidReportingV4(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons SetCidReporting version 4 implementation class

    This configures the current reporting method for a control ID. If successful, the request packet is echoed
    as the response.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || ForceRawXYValid        || 1            ||
    || ForceRawXY             || 1            ||
    || RawXYValid             || 1            ||
    || RawXY                  || 1            ||
    || PersistValid           || 1            ||
    || Persist                || 1            ||
    || DivertValid            || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Unused                 || 6            ||
    || AnalyticsKeyEventValid || 1            ||
    || AnalyticsKeyEvent      || 1            ||
    || Padding                || 80           ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        FORCE_RAW_XY_VALID = 0xF9
        FORCE_RAW_XY = 0xF8
        RAW_XY_VALID = 0xF7
        RAW_XY = 0xF6
        PERSIST_VALID = 0xF5
        PERSIST = 0xF4
        DIVERT_VALID = 0xF3
        DIVERT = 0xF2
        REMAP = 0xF1
        UNUSED = 0xF0
        ANALYTICS_KEY_EVENT_VALID = 0xEF
        ANALYTICS_KEY_EVENT = 0xEE
        PADDING = 0xED
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        FORCE_RAW_XY_VALID = 0x01
        FORCE_RAW_XY = 0x01
        RAW_XY_VALID = 0x01
        RAW_XY = 0x01
        PERSIST_VALID = 0x01
        PERSIST = 0x01
        DIVERT_VALID = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        UNUSED = 0x06
        ANALYTICS_KEY_EVENT_VALID = 0x01
        ANALYTICS_KEY_EVENT = 0x01
        PADDING = 0x50
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.FORCE_RAW_XY_VALID,
                 LEN.FORCE_RAW_XY_VALID,
                 title='ForceRawXYValid',
                 name='force_raw_xy_valid',
                 aliases=('f_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY_VALID) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.RAW_XY_VALID,
                 LEN.RAW_XY_VALID,
                 title='RawXYValid',
                 name='raw_xy_valid',
                 aliases=('r_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY_VALID) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.PERSIST_VALID,
                 LEN.PERSIST_VALID,
                 title='PersistValid',
                 name='persist_valid',
                 aliases=('p_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.PERSIST_VALID) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.DIVERT_VALID,
                 LEN.DIVERT_VALID,
                 title='DivertValid',
                 name='divert_valid',
                 aliases=('d_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.DIVERT_VALID) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.ANALYTICS_KEY_EVENT_VALID,
                 LEN.ANALYTICS_KEY_EVENT_VALID,
                 title='AnalyticsKeyEventValid',
                 name='analytics_key_event_valid',
                 aliases=('a_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVENT_VALID) - 1),)),
        BitField(FID.ANALYTICS_KEY_EVENT,
                 LEN.ANALYTICS_KEY_EVENT,
                 title='AnalyticsKeyEvent',
                 name='analytics_key_event',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVENT) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy_valid=False, force_raw_xy=False,
                 raw_xy_valid=False, raw_xy=False, persist_valid=False, persist=False, divert_valid=False,
                 divert=False, remap=0, analytics_key_event_valid=False, analytics_key_event=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy_valid: Flag which indicates that the forceRawXY flag is valid and device should update the
                                   persistant forceRawXY state of this control ID.
        :type force_raw_xy_valid: ``bool``
        :param force_raw_xy: Flag which causes this control is being force diverted by SW.
        :type force_raw_xy: ``bool``
        :param raw_xy_valid: Flag which indicates that the raw xy flag is valid and device should update the
                              temporary divert state of this control ID.
        :type raw_xy_valid: ``bool``
        :param raw_xy: Flag which causes this control and all raw mouse move reports to temporarily be diverted to
                       software via divertedRawMouseXYEvent.
        :type raw_xy: ``bool``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID to remap this control to. 0 means no remap.
        :type remap: ``int``
        :param analytics_key_event_valid: Flag which indicates that the analyticsKeyEvt flag of the CId is
                                          valid and device should temporarily update it.
        :type analytics_key_event_valid: ``bool``
        :param analytics_key_event: Flag which causes this control to temporarily report project-dependent analytics
                                    key events to software via AnalyticsKeyEvents. This flag is ignored by the device if
                                                      analytics_key_event_valid is not set.
        :type analytics_key_event: ``bool``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = SetCidReportingV4Response.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.force_raw_xy_valid = force_raw_xy_valid
        self.force_raw_xy = force_raw_xy
        self.raw_xy_valid = raw_xy_valid
        self.raw_xy = raw_xy
        self.persist_valid = persist_valid
        self.persist = persist
        self.divert_valid = divert_valid
        self.divert = divert
        self.remap = remap
        self.unused = 0
        self.analytics_key_event_valid = analytics_key_event_valid
        self.analytics_key_event = analytics_key_event
    # end def __init__
# end class SetCidReportingV4


class SetCidReportingV5toV6(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons SetCidReporting version 5 implementation class

    This configures the current reporting method for a control ID. If successful, the request packet is echoed
    as the response.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId                 || 16           ||
    || ForceRawXYValid        || 1            ||
    || ForceRawXY             || 1            ||
    || RawXYValid             || 1            ||
    || RawXY                  || 1            ||
    || PersistValid           || 1            ||
    || Persist                || 1            ||
    || DivertValid            || 1            ||
    || Divert                 || 1            ||
    || Remap                  || 16           ||
    || Unused                 || 4            ||
    || RawWheelValid          || 1            ||
    || RawWheel               || 1            ||
    || AnalyticsKeyEventValid || 1            ||
    || AnalyticsKeyEvent      || 1            ||
    || Padding                || 80           ||
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID = 0xFA
        FORCE_RAW_XY_VALID = 0xF9
        FORCE_RAW_XY = 0xF8
        RAW_XY_VALID = 0xF7
        RAW_XY = 0xF6
        PERSIST_VALID = 0xF5
        PERSIST = 0xF4
        DIVERT_VALID = 0xF3
        DIVERT = 0xF2
        REMAP = 0xF1
        UNUSED = 0xF0
        RAW_WHEEL_VALID = 0xEF
        RAW_WHEEL = 0xEE
        ANALYTICS_KEY_EVENT_VALID = 0xED
        ANALYTICS_KEY_EVENT = 0xEC
        PADDING = 0xEB
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID = 0x10
        FORCE_RAW_XY_VALID = 0x01
        FORCE_RAW_XY = 0x01
        RAW_XY_VALID = 0x01
        RAW_XY = 0x01
        PERSIST_VALID = 0x01
        PERSIST = 0x01
        DIVERT_VALID = 0x01
        DIVERT = 0x01
        REMAP = 0x10
        UNUSED = 0x04
        RAW_WHEEL_VALID = 0x01
        RAW_WHEEL = 0x01
        ANALYTICS_KEY_EVENT_VALID = 0x01
        ANALYTICS_KEY_EVENT = 0x01
        PADDING = 0x50
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID,
                 LEN.CTRL_ID,
                 title='CtrlId',
                 name='ctrl_id',
                 aliases=('cid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.FORCE_RAW_XY_VALID,
                 LEN.FORCE_RAW_XY_VALID,
                 title='ForceRawXYValid',
                 name='force_raw_xy_valid',
                 aliases=('f_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY_VALID) - 1),)),
        BitField(FID.FORCE_RAW_XY,
                 LEN.FORCE_RAW_XY,
                 title='ForceRawXY',
                 name='force_raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.FORCE_RAW_XY) - 1),)),
        BitField(FID.RAW_XY_VALID,
                 LEN.RAW_XY_VALID,
                 title='RawXYValid',
                 name='raw_xy_valid',
                 aliases=('r_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY_VALID) - 1),)),
        BitField(FID.RAW_XY,
                 LEN.RAW_XY,
                 title='RawXY',
                 name='raw_xy',
                 checks=(CheckInt(0, pow(2, LEN.RAW_XY) - 1),)),
        BitField(FID.PERSIST_VALID,
                 LEN.PERSIST_VALID,
                 title='PersistValid',
                 name='persist_valid',
                 aliases=('p_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.PERSIST_VALID) - 1),)),
        BitField(FID.PERSIST,
                 LEN.PERSIST,
                 title='Persist',
                 name='persist',
                 checks=(CheckInt(0, pow(2, LEN.PERSIST) - 1),)),
        BitField(FID.DIVERT_VALID,
                 LEN.DIVERT_VALID,
                 title='DivertValid',
                 name='divert_valid',
                 aliases=('d_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.DIVERT_VALID) - 1),)),
        BitField(FID.DIVERT,
                 LEN.DIVERT,
                 title='Divert',
                 name='divert',
                 checks=(CheckInt(0, pow(2, LEN.DIVERT) - 1),)),
        BitField(FID.REMAP,
                 LEN.REMAP,
                 title='Remap',
                 name='remap',
                 checks=(CheckHexList(LEN.REMAP // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.UNUSED,
                 LEN.UNUSED,
                 title='Unused',
                 name='unused',
                 checks=(CheckInt(0, pow(2, LEN.UNUSED) - 1),)),
        BitField(FID.RAW_WHEEL_VALID,
                 LEN.RAW_WHEEL_VALID,
                 title='RawWheelValid',
                 name='raw_wheel_valid',
                 checks=(CheckInt(0, pow(2, LEN.RAW_WHEEL_VALID) - 1),)),
        BitField(FID.RAW_WHEEL,
                 LEN.RAW_WHEEL,
                 title='RawWheel',
                 name='raw_wheel',
                 checks=(CheckInt(0, pow(2, LEN.RAW_WHEEL) - 1),)),
        BitField(FID.ANALYTICS_KEY_EVENT_VALID,
                 LEN.ANALYTICS_KEY_EVENT_VALID,
                 title='AnalyticsKeyEventValid',
                 name='analytics_key_event_valid',
                 aliases=('a_valid',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVENT_VALID) - 1),)),
        BitField(FID.ANALYTICS_KEY_EVENT,
                 LEN.ANALYTICS_KEY_EVENT,
                 title='AnalyticsKeyEvent',
                 name='analytics_key_event',
                 checks=(CheckInt(0, pow(2, LEN.ANALYTICS_KEY_EVENT) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy_valid=False, force_raw_xy=False,
                 raw_xy_valid=False, raw_xy=False, persist_valid=False, persist=False, divert_valid=False,
                 divert=False, remap=0, raw_wheel_valid=False, raw_wheel=False, analytics_key_event_valid=False,
                 analytics_key_event=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy_valid: Flag which indicates that the forceRawXY flag is valid and device should update the
                                   persistant forceRawXY state of this control ID.
        :type force_raw_xy_valid: ``bool``
        :param force_raw_xy: Flag which causes this control is being force diverted by SW.
        :type force_raw_xy: ``bool``
        :param raw_xy_valid: Flag which indicates that the raw xy flag is valid and device should update the
                              temporary divert state of this control ID.
        :type raw_xy_valid: ``bool``
        :param raw_xy: Flag which causes this control and all raw mouse move reports to temporarily be diverted to
                       software via divertedRawMouseXYEvent.
        :type raw_xy: ``bool``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID to remap this control to. 0 means no remap.
        :type remap: ``int``
        :param raw_wheel_valid: Flag which indicates that thedivert rawWheel flag is valid and
                                device should update the temporary divert state of this control ID
        :type raw_wheel_valid: ``bool``
        :param raw_wheel: Flag which causes this control and all raw mouse wheel reports to temporarily be diverted
                          to software via [event4] divertedRawWheelEvent during wheel scrolling.
        :type raw_wheel: ``bool``
        :param analytics_key_event_valid: Flag which indicates that the analyticsKeyEvt flag of the CId is
                                          valid and device should temporarily update it.
        :type analytics_key_event_valid: ``bool``
        :param analytics_key_event: Flag which causes this control to temporarily report project-dependent analytics
                                    key events to software via AnalyticsKeyEvents. This flag is ignored by the device if
                                    analytics_key_event_valid is not set.
        :type analytics_key_event: ``bool``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = SetCidReportingV4Response.FUNCTION_INDEX
        self.ctrl_id = ctrl_id
        self.force_raw_xy_valid = force_raw_xy_valid
        self.force_raw_xy = force_raw_xy
        self.raw_xy_valid = raw_xy_valid
        self.raw_xy = raw_xy
        self.persist_valid = persist_valid
        self.persist = persist
        self.divert_valid = divert_valid
        self.divert = divert
        self.remap = remap
        self.unused = 0
        self.raw_wheel_valid = raw_wheel_valid
        self.raw_wheel = raw_wheel
        self.analytics_key_event_valid = analytics_key_event_valid
        self.analytics_key_event = analytics_key_event
    # end def __init__
# end class SetCidReportingV5toV6


class SetCidReportingV0Response(SetCidReportingV0):
    """
    SpecialKeysMSEButtons SetCidReporting response version 0 implementation class

    Echo of the request SetCidReporting if successful.

    Same format as SetCidReportingV0

    Format:
    || @b Name                  || @b Bit count ||
    || SetCidReportingV0 fields || 56           ||
    || Padding                  || 104          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCidReportingV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    class FID(SetCidReportingV0.FID):
        """
        Field Identifiers
        """
        PADDING = 0xF4
    # end class FID

    class LEN(SetCidReportingV0.LEN):
        """
        Field Lengths
        """
        PADDING = 0x68
    # end class LEN

    FIELDS = SetCidReportingV0.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id=0, persist_valid=False, persist=False, divert_valid=False,
                 divert=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        """
        super().__init__(device_index, feature_index, ctrl_id, persist_valid, persist, divert_valid, divert)
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
    # end def __init__
# end class SetCidReportingV0Response


class SetCidReportingV1Response(SetCidReportingV1):
    """
    SpecialKeysMSEButtons SetCidReporting response version 1 implementation class

    Echo of the request SetCidReporting if successful.

    Same format as SetCidReportingV1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCidReportingV1,)
    VERSION = (1,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, ctrl_id=0, persist_valid=False, persist=False, divert_valid=False,
                 divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, ctrl_id, persist_valid, persist, divert_valid, divert, remap)
    # end def __init__
# end class SetCidReportingV1Response


class SetCidReportingV2Response(SetCidReportingV2):
    """
    SpecialKeysMSEButtons SetCidReporting response version 2 implementation class

    Echo of the request SetCidReporting if successful.

    Same format as SetCidReportingV2
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCidReportingV2,)
    VERSION = (2,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, ctrl_id=0, raw_xy_valid=False, raw_xy=False, persist_valid=False,
                 persist=False, divert_valid=False, divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param raw_xy_valid: Flag which indicates that the raw xy flag is valid and device should update the
                              temporary divert state of this control ID.
        :type raw_xy_valid: ``bool``
        :param raw_xy: Flag which causes this control and all raw mouse move reports to temporarily be diverted to
                       software via divertedRawMouseXYEvent.
        :type raw_xy: ``bool``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, ctrl_id, raw_xy_valid, raw_xy, persist_valid, persist,
                         divert_valid, divert, remap)
    # end def __init__
# end class SetCidReportingV2Response


class SetCidReportingV3Response(SetCidReportingV3):
    """
    SpecialKeysMSEButtons SetCidReporting response version 3 implementation class

    Echo of the request SetCidReporting if successful.

    Same format as SetCidReportingV3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCidReportingV3,)
    VERSION = (3,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy_valid=False, force_raw_xy=False,
                 raw_xy_valid=False, raw_xy=False, persist_valid=False, persist=False, divert_valid=False,
                 divert=False, remap=0):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy_valid: Flag which indicates that the forceRawXY flag is valid and device should update the
                                   persistant forceRawXY state of this control ID.
        :type force_raw_xy_valid: ``bool``
        :param force_raw_xy: Flag which causes this control is being force diverted by SW.
        :type force_raw_xy: ``bool``
        :param raw_xy_valid: Flag which indicates that the raw xy flag is valid and device should update the
                              temporary divert state of this control ID.
        :type raw_xy_valid: ``bool``
        :param raw_xy: Flag which causes this control and all raw mouse move reports to temporarily be diverted to
                       software via divertedRawMouseXYEvent.
        :type raw_xy: ``bool``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        """
        super().__init__(device_index, feature_index, ctrl_id, force_raw_xy_valid, force_raw_xy, raw_xy_valid,
                         raw_xy, persist_valid, persist, divert_valid, divert, remap)
    # end def __init__
# end class SetCidReportingV3Response


class SetCidReportingV4Response(SetCidReportingV4):
    """
    SpecialKeysMSEButtons SetCidReporting response version 4 implementation class

    Echo of the request SetCidReporting if successful.

    Same format as SetCidReportingV4
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCidReportingV4,)
    VERSION = (4,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy_valid=False, force_raw_xy=False,
                 raw_xy_valid=False, raw_xy=False, persist_valid=False, persist=False, divert_valid=False,
                 divert=False, remap=0, analytics_key_event_valid=False, analytics_key_event=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy_valid: Flag which indicates that the forceRawXY flag is valid and device should update the
                                   persistant forceRawXY state of this control ID.
        :type force_raw_xy_valid: ``bool``
        :param force_raw_xy: Flag which causes this control is being force diverted by SW.
        :type force_raw_xy: ``bool``
        :param raw_xy_valid: Flag which indicates that the raw xy flag is valid and device should update the
                              temporary divert state of this control ID.
        :type raw_xy_valid: ``bool``
        :param raw_xy: Flag which causes this control and all raw mouse move reports to temporarily be diverted to
                       software via divertedRawMouseXYEvent.
        :type raw_xy: ``bool``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        :param analytics_key_event_valid: Flag which indicates that the analyticsKeyEvt flag of the CId is
                                          valid and device should temporarily update it.
        :type analytics_key_event_valid: ``bool``
        :param analytics_key_event: Flag which causes this control to temporarily report project-dependent analytics
                                    key events to software via AnalyticsKeyEvents. This flag is ignored by the device if
                                    analytics_key_event_valid is not set.
        :type analytics_key_event: ``bool``
        """
        super().__init__(device_index, feature_index, ctrl_id, force_raw_xy_valid, force_raw_xy, raw_xy_valid, raw_xy,
                         persist_valid, persist, divert_valid, divert, remap, analytics_key_event_valid,
                         analytics_key_event)
    # end def __init__
# end class SetCidReportingV4Response


class SetCidReportingV5ToV6Response(SetCidReportingV5toV6):
    """
    SpecialKeysMSEButtons SetCidReporting response version 5 implementation class

    Echo of the request SetCidReporting if successful.

    Same format as SetCidReportingV5toV6
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCidReportingV5toV6,)
    VERSION = (5, 6,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, ctrl_id=0, force_raw_xy_valid=False, force_raw_xy=False,
                 raw_xy_valid=False, raw_xy=False, persist_valid=False, persist=False, divert_valid=False,
                 divert=False, remap=0, raw_wheel_valid=False, raw_wheel=False, analytics_key_event_valid=False,
                 analytics_key_event=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id: The control ID whose reporting method is being requested.
        :type ctrl_id: ``int``
        :param force_raw_xy_valid: Flag which indicates that the forceRawXY flag is valid and device should update the
                                   persistant forceRawXY state of this control ID.
        :type force_raw_xy_valid: ``bool``
        :param force_raw_xy: Flag which causes this control is being force diverted by SW.
        :type force_raw_xy: ``bool``
        :param raw_xy_valid: Flag which indicates that the raw xy flag is valid and device should update the
                              temporary divert state of this control ID.
        :type raw_xy_valid: ``bool``
        :param raw_xy: Flag which causes this control and all raw mouse move reports to temporarily be diverted to
                       software via divertedRawMouseXYEvent.
        :type raw_xy: ``bool``
        :param persist_valid: Flag which indicates that the persist flag is valid and device should update the
                              persistent divert state of this control ID.
        :type persist_valid: ``bool``
        :param persist: Flag which causes this control to be persistently diverted to software via divertedButtonsEvent.
                        This flag is ignored by the device if persist_valid is not set.
        :type persist: ``bool``
        :param divert_valid: Flag which indicates that the persist flag is valid and device should update the
                             temporary divert state of this control ID.
        :type divert_valid: ``bool``
        :param divert: Flag which causes this control to be temporarily  diverted to software via divertedButtonsEvent.
                       This flag is ignored by the device if divert_valid is not set.
        :type divert: ``bool``
        :param remap: The control ID that this control has been remapped to. 0 means no remap.
        :type remap: ``int``
        :param raw_wheel_valid: Flag which indicates that thedivert rawWheel flag is valid and
                                device should update the temporary divert state of this control ID
        :type raw_wheel_valid: ``bool``
        :param raw_wheel: Flag which causes this control and all raw mouse wheel reports to temporarily be diverted
                          to software via [event4] divertedRawWheelEvent during wheel scrolling.
        :type raw_wheel: ``bool``
        :param analytics_key_event_valid: Flag which indicates that the analyticsKeyEvt flag of the CId is
                                          valid and device should temporarily update it.
        :type analytics_key_event_valid: ``bool``
        :param analytics_key_event: Flag which causes this control to temporarily report project-dependent analytics
                                    key events to software via AnalyticsKeyEvents. This flag is ignored by the device if
                                    analytics_key_event_valid is not set.
        :type analytics_key_event: ``bool``
        """
        super().__init__(device_index, feature_index, ctrl_id, force_raw_xy_valid, force_raw_xy, raw_xy_valid, raw_xy,
                         persist_valid, persist, divert_valid, divert, remap, raw_wheel_valid, raw_wheel,
                         analytics_key_event_valid, analytics_key_event)
    # end def __init__
# end class SetCidReportingV5ToV6Response


class GetCapabilitiesV6(SpecialKeysMSEButtons):
    """
    Define ``GetCapabilities`` implementation class for version 6

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Define field identifier(s)
        """
        PADDING = SpecialKeysMSEButtons.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         report_id=self.DEFAULT.REPORT_ID_SHORT)

        self.functionIndex = GetCapabilitiesV6Response.FUNCTION_INDEX
    # end def __init__
# end class GetCapabilitiesV6


class GetCapabilitiesV6Response(SpecialKeysMSEButtons):
    """
    Define ``GetCapabilitiesV6Response`` implementation class for version 6

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Flags                         8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilitiesV6,)
    VERSION = (6,)
    FUNCTION_INDEX = 4

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        FLAGS = SpecialKeysMSEButtons.FID.SOFTWARE_ID - 1
        PADDING = FLAGS - 1
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        FLAGS = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.FLAGS,
                 LEN.FLAGS,
                 title='Flags',
                 name='flags',
                 checks=(CheckHexList(LEN.FLAGS // 8),
                         CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    class Flags(BitFieldContainerMixin):
        """
       Define the optional functions supported by the ``SpecialKeysMSEButtons`` feature

       Format:

       ============================  ==========
       Name                          Bit count
       ============================  ==========
       Reserved                      7
       resetAllCidReportSettings     1
       ============================  ==========
        """
        class FID:
            """
            Field identifiers
            """
            RESERVED = 0xFF
            RESET_ALL_CID_REPORT_SETTINGS_FLAG = RESERVED - 1
        # end class FID

        class LEN:
            """
            Field lengths in bits
            """
            RESERVED = 7
            RESET_ALL_CID_REPORT_SETTINGS_FLAG = 1
        # end class LEN

        class DEFAULT:
            """
            Field default values
            """
            RESERVED = 0x00
            RESET_ALL_CID_REPORT_SETTINGS_FLAG = 0
        # end class DEFAULT

        FIELDS = (
            BitField(FID.RESERVED,
                     LEN.RESERVED,
                     title='Reserved',
                     name='reserved',
                     default_value=DEFAULT.RESERVED,
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
            BitField(FID.RESET_ALL_CID_REPORT_SETTINGS_FLAG,
                     LEN.RESET_ALL_CID_REPORT_SETTINGS_FLAG,
                     title='Reset all cid report settings flag',
                     name='reset_all_cid_report_settings_flag',
                     default_value=DEFAULT.RESET_ALL_CID_REPORT_SETTINGS_FLAG,
                     checks=(CheckInt(0, pow(2, LEN.RESET_ALL_CID_REPORT_SETTINGS_FLAG) - 1),)),
        )
    # end class Flags

    def __init__(self, device_index, feature_index, reset_all_cid_report_settings_flag=False):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param reset_all_cid_report_settings_flag: Flag indicating if the firmware supports the
                                                   ``ResetAllCidReportSettingsV6`` function - OPTIONAL
        :type reset_all_cid_report_settings_flag: ``bool``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.flags = self.Flags(reset_all_cid_report_settings_flag=reset_all_cid_report_settings_flag)
    # end def __init__
# end class GetCapabilitiesV6Response


class ResetAllCidReportSettingsV6(SpecialKeysMSEButtons):
    """
    Define ``ResetAllCidReportSettingsV6`` implementation class for version 6

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(SpecialKeysMSEButtons.FID):
        """
        Define field identifier(s)
        """
        PADDING = SpecialKeysMSEButtons.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         report_id=self.DEFAULT.REPORT_ID_SHORT)

        self.functionIndex = ResetAllCidReportSettingsV6Response.FUNCTION_INDEX
    # end def __init__
# end class ResetAllCidReportSettingsV6


class ResetAllCidReportSettingsV6Response(SpecialKeysMSEButtons):
    """
    Define ``ResetAllCidReportSettingsV6Response`` implementation class for version 6

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ResetAllCidReportSettingsV6,)
    VERSION = (6,)
    FUNCTION_INDEX = 5

    class FID(SpecialKeysMSEButtons.FID):
        """
        Define field identifier(s)
        """
        PADDING = SpecialKeysMSEButtons.FID.SOFTWARE_ID - 1

    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x80

    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         report_id=self.DEFAULT.REPORT_ID_LONG)
    # end def __init__
# end class ResetAllCidReportSettingsV6Response


class DivertedButtonsEvent(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons DivertButtonEvent event

    This event reports a list of diverted buttons which are currently pressed. It is sent in response to changes in
    the pressed state of diverted buttons.

    This event reports from zero to four simultaneously pressed keys. Keys are packed from the beginning of the report
    so that there are no gaps. Note that the position of a pressed key in the report might move if a key preceding it
    in the report is released. Newly pressed keys are added to the end of the report so that keys appear in the order
    they were pressed.

    Configuration changes such as diverting or undiverting a pressed button does not trigger this report. While a
    button remains pressed, changes to the divert status are stored in the device memory but do not affect the button's
    current divert state. The button's current divert state is updated only on the event of physical button press.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId1                || 16           ||
    || CtrlId2                || 16           ||
    || CtrlId3                || 16           ||
    || CtrlId4                || 16           ||
    || Padding                || 64           ||
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1, 2, 3, 4, 5, 6, )
    FUNCTION_INDEX = 0

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID1 = 0xFA
        CTRL_ID2 = 0xF9
        CTRL_ID3 = 0xF8
        CTRL_ID4 = 0xF7
        PADDING = 0xF6
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID1 = 0x10
        CTRL_ID2 = 0x10
        CTRL_ID3 = 0x10
        CTRL_ID4 = 0x10
        PADDING = 0x40
    # end class LEN

    class DEFAULT(SpecialKeysMSEButtons.DEFAULT):
        """
        Field defautl values
        """
        CTRL_ID1 = 0x00
        CTRL_ID2 = 0x00
        CTRL_ID3 = 0x00
        CTRL_ID4 = 0x00
    # end class DEFAULT

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID1,
                 LEN.CTRL_ID1,
                 title='CtrlId1',
                 name='ctrl_id_1',
                 aliases=('cid_1',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID1 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.CTRL_ID2,
                 LEN.CTRL_ID2,
                 title='CtrlId2',
                 name='ctrl_id_2',
                 aliases=('cid_2',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID2 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.CTRL_ID3,
                 LEN.CTRL_ID3,
                 title='CtrlId3',
                 name='ctrl_id_3',
                 aliases=('cid_3',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID3 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.CTRL_ID4,
                 LEN.CTRL_ID4,
                 title='CtrlId4',
                 name='ctrl_id_4',
                 aliases=('cid_4',),  # Name of that field in v1 to v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID4 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id_1, ctrl_id_2, ctrl_id_3, ctrl_id_4):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id_1: First control ID associated to the event.
        :type ctrl_id_1: ``int`` or ``HexList``
        :param ctrl_id_2: Second control ID associated to the event.
        :type ctrl_id_2: ``int`` or ``HexList``
        :param ctrl_id_3: Third control ID associated to the event.
        :type ctrl_id_3: ``int`` or ``HexList``
        :param ctrl_id_4: Fourth control ID associated to the event.
        :type ctrl_id_4: ``int`` or ``HexList``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id_1 = ctrl_id_1
        self.ctrl_id_2 = ctrl_id_2
        self.ctrl_id_3 = ctrl_id_3
        self.ctrl_id_4 = ctrl_id_4
    # end def __init__
# end class DivertButtonEvent


class DivertedRawMouseXYEventV2toV6(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons DivertedRawMouseXYEventV2toV6 event

    This event reports the mouse XY data when the diverted button is pressed and mouse move happens.
    The reports are sent in response to pressed state of diverted button and mouse move.

    This event does not report button pressed/released information, the button pressed and released events are still
    sent via DivertedButtonEvent.


    Configuration changes such as diverting or undiverting a pressed button does not trigger this report. While a
    button remains pressed, changes to the divert status are stored in the device memory but do not affect the
    button's current divert state. The button's current divert state is updated only on the event of physical
    button press.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Dx                     || 16           ||
    || Dy                     || 16           ||
    || Padding                || 96           ||
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (2, 3, 4, 5, 6,)
    FUNCTION_INDEX = 1

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        DX = 0xFA
        DY = 0xF9
        PADDING = 0xF8
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        DX = 0x10
        DY = 0x10
        PADDING = 0x60
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.DX,
                 LEN.DX,
                 title='Dx',
                 name='dx',
                 checks=(CheckHexList(LEN.DX // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.DY,
                 LEN.DY,
                 title='Dy',
                 name='dy',
                 checks=(CheckHexList(LEN.DY // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, dx, dy):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param dx: Raw value on X
        :type dx: ``int``
        :param dy: Raw value on Y
        :type dy: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.dx = dx
        self.dy = dy
    # end def __init__
# end class DivertedRawMouseXYEvent


class AnalyticsKeyEventsV4toV6(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons AnalyticsKeyEventsV4toV6 event

    This event reports up to five analytics key events associated to the CIds defined in this feature.
    This event is independent from the divertable state of the controls The analytics key events reported by this
    notification (labeled as "event_x") are project-dependent and notified to the SW for analytics purposes.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || CtrlId1                || 16           ||
    || Event1                 || 8            ||
    || CtrlId2                || 16           ||
    || Event2                 || 8            ||
    || CtrlId3                || 16           ||
    || Event3                 || 8            ||
    || CtrlId4                || 16           ||
    || Event4                 || 8            ||
    || CtrlId5                || 16           ||
    || Event5                 || 8            ||
    || Padding                || 8            ||
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (4, 5, 6,)
    FUNCTION_INDEX = 2

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        CTRL_ID1 = 0xFA
        EVENT1 = 0xF9
        CTRL_ID2 = 0xF8
        EVENT2 = 0xF7
        CTRL_ID3 = 0xF6
        EVENT3 = 0xF5
        CTRL_ID4 = 0xF4
        EVENT4 = 0xF3
        CTRL_ID5 = 0xF2
        EVENT5 = 0xF1
        PADDING = 0xF0
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        CTRL_ID1 = 0x10
        EVENT1 = 0x08
        CTRL_ID2 = 0x10
        EVENT2 = 0x08
        CTRL_ID3 = 0x10
        EVENT3 = 0x08
        CTRL_ID4 = 0x10
        EVENT4 = 0x08
        CTRL_ID5 = 0x10
        EVENT5 = 0x08
        PADDING = 0x08
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.CTRL_ID1,
                 LEN.CTRL_ID1,
                 title='CtrlId1',
                 name='ctrl_id_1',
                 aliases=('cid_1',),  # Name of that field in v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID1 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.EVENT1,
                 LEN.EVENT1,
                 title='Event1',
                 name='event_1',
                 checks=(CheckHexList(LEN.EVENT1 // 8),
                         CheckByte(),), ),
        BitField(FID.CTRL_ID2,
                 LEN.CTRL_ID2,
                 title='CtrlId2',
                 name='ctrl_id_2',
                 aliases=('cid_2',),  # Name of that field in v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID2 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.EVENT2,
                 LEN.EVENT2,
                 title='Event2',
                 name='event_2',
                 checks=(CheckHexList(LEN.EVENT2 // 8),
                         CheckByte(),), ),
        BitField(FID.CTRL_ID3,
                 LEN.CTRL_ID3,
                 title='CtrlId3',
                 name='ctrl_id_3',
                 aliases=('cid_3',),  # Name of that field in v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID3 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.EVENT3,
                 LEN.EVENT3,
                 title='Event3',
                 name='event_3',
                 checks=(CheckHexList(LEN.EVENT3 // 8),
                         CheckByte(),), ),
        BitField(FID.CTRL_ID4,
                 LEN.CTRL_ID4,
                 title='CtrlId4',
                 name='ctrl_id_4',
                 aliases=('cid_4',),  # Name of that field in v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID4 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.EVENT4,
                 LEN.EVENT4,
                 title='Event4',
                 name='event_4',
                 checks=(CheckHexList(LEN.EVENT4 // 8),
                         CheckByte(),), ),
        BitField(FID.CTRL_ID5,
                 LEN.CTRL_ID5,
                 title='CtrlId5',
                 name='ctrl_id_5',
                 aliases=('cid_5',),  # Name of that field in v4 in specification in specification
                 checks=(CheckHexList(LEN.CTRL_ID5 // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.EVENT5,
                 LEN.EVENT5,
                 title='Event5',
                 name='event_5',
                 checks=(CheckHexList(LEN.EVENT5 // 8),
                         CheckByte(),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ctrl_id_1, event_1, ctrl_id_2, event_2, ctrl_id_3, event_3,
                 ctrl_id_4, event_4, ctrl_id_5, event_5):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ctrl_id_1: First control ID associated to the first event.
        :type ctrl_id_1: ``int``
        :param event_1: First event.
        :type event_1: ``int``
        :param ctrl_id_2: Second control ID associated to the second event.
        :type ctrl_id_2: ``int``
        :param event_2: Second event.
        :type event_2 ``int``
        :param ctrl_id_3: Third control ID associated to the third event.
        :type ctrl_id_3: ``int``
        :param event_3: Third event.
        :type event_3 ``int``
        :param ctrl_id_4: Fourth control ID associated to the fourth event.
        :type ctrl_id_4: ``int``
        :param event_4: Fourth event.
        :type event_4 ``int``
        :param ctrl_id_5: Fifth control ID associated to the fifth event.
        :type ctrl_id_5: ``int``
        :param event_5: Fifth event.
        :type event_5 ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.ctrl_id_1 = ctrl_id_1
        self.event_1 = event_1
        self.ctrl_id_2 = ctrl_id_2
        self.event_2 = event_2
        self.ctrl_id_3 = ctrl_id_3
        self.event_3 = event_3
        self.ctrl_id_4 = ctrl_id_4
        self.event_4 = event_4
        self.ctrl_id_5 = ctrl_id_5
        self.event_5 = event_5
    # end def __init__
# end class AnalyticsKeyEventsV4toV6


class DivertedRawWheelV5toV6(SpecialKeysMSEButtons):
    """
    SpecialKeysMSEButtons Diverted RawWheel event

    This event reports the mouse wheel data when the diverted button is pressed and mouse wheel move happens.
    The reports are sent in response to pressed state of diverted button and mouse wheel move.
    The wheel scrolling value reported is taking into account the invertion of wheel (done via x2121).

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Reserved                      3
    Resolution                    1
    Periods                       4
    Delta V                       16
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (5, 6,)
    FUNCTION_INDEX = 4

    class FID(SpecialKeysMSEButtons.FID):
        """
        Field Identifiers
        """
        RESERVED_0 = 0xFA
        RESOLUTION = 0xF9
        PERIODS = 0xF8
        DELTA_V = 0xF7
        PADDING = 0xF6
    # end class FID

    class LEN(SpecialKeysMSEButtons.LEN):
        """
        Field Lengths
        """
        RESERVED_0 = 0x03
        RESOLUTION = 0x01
        PERIODS = 0x4
        DELTA_V = 0x10
        PADDING = 0x68
    # end class LEN

    FIELDS = SpecialKeysMSEButtons.FIELDS + (
        BitField(FID.RESERVED_0,
                 LEN.RESERVED_0,
                 title='Reserved_0',
                 name='reserved_0',
                 checks=(CheckInt(0, pow(2, LEN.RESERVED_0) - 1),)),
        BitField(FID.RESOLUTION,
                 LEN.RESOLUTION,
                 title='Resolution',
                 name='resolution',
                 checks=(CheckInt(0, pow(2, LEN.RESOLUTION) - 1),)),
        BitField(FID.PERIODS,
                 LEN.PERIODS,
                 title='Periods',
                 name='periods',
                 checks=(CheckInt(0, pow(2, LEN.PERIODS) - 1),)),
        BitField(FID.DELTA_V,
                 LEN.DELTA_V,
                 name='delta_v',
                 checks=(CheckHexList(LEN.DELTA_V // 8),
                         CheckInt(max_value=0xFFFF),), ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SpecialKeysMSEButtons.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, resolution, periods, delta_v):
        """
        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param resolution: Low or High resolution
        :type resolution: ``int``
        :param periods: Number of sampling periods combined in this report
        :type periods: ``int``
        :param delta_v: Vertical wheel motion delta. Moving away from the user produces positive values.
        :type delta_v: ``int``
        """
        super().__init__(device_index, feature_index, report_id=HidppMessage.DEFAULT.REPORT_ID_LONG)

        self.functionIndex = self.FUNCTION_INDEX
        self.resolution = resolution
        self.periods = periods
        self.delta_v = delta_v
    # end def __init__
# end class DivertedRawWheelV5toV6

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
