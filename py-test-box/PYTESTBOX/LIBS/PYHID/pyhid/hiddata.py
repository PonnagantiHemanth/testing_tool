#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hiddata
:brief: HID Data
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import Enum
from enum import IntEnum

# noinspection PyUnresolvedReferences
from pyhid.hid.hidcallstatemanagementcontrol import HidCallStateManagementControl
# noinspection PyUnresolvedReferences
from pyhid.hid.hidconsumer import HidConsumer
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.hidkeyboardbitmap import HidKeyboardBitmap
# noinspection PyUnresolvedReferences
from pyhid.hid.hidmouse import HidMouse
# noinspection PyUnresolvedReferences
from pyhid.hid.hidmouse import HidMouseNvidiaExtension
# noinspection PyUnresolvedReferences
from pyhid.hid.hidsystemcontrol import HidSystemControl
from pyhid.hid.usbhidusagetable import ConsumerHidUsage as CS_Usage
from pyhid.hid.usbhidusagetable import KEYBOARD_HID_USAGE as KDB_USAGE
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
# Field strings
RESP_CLASS = 'Responses_class'
FIELDS_NAME = 'Fields_name'
FIELDS_VALUE = 'Fields_value'


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class OS:
    """
    List of OS impacting the HID report translation
    """
    WINDOWS = 'windowsOS'
    MAC = 'macOS'
    INVERTED_MAC = 'invertedMacOS'
    IPAD = 'iPadOS'
    # Chrome with a BLE Pro receiver
    CHROME = 'chromeOS'
    # Chrome BLE stack
    CHROME_BLE_DIRECT = 'chromeBleDirect'
    WIN_EMB = 'windowsEmbedded'
    LINUX = 'linuxOS'
    ANDROID = 'androidOS'
    WEB_OS = 'webOS'
    TIZEN = 'tizenOS'
    BOOT = 'bootProtocol'
    ALL = 'all'
# end class OS


def _none_on_make_none_on_break():
    """
    Sequence of HID messages returned on a stimulus with no report on make or break

    :return: dictionary with 'make' and 'break' keys
    :rtype: ``dict``
    """
    return {
        MAKE: {
            RESP_CLASS: (),
            FIELDS_NAME: ((),),
            FIELDS_VALUE: ((),)
        },
        BREAK: {
            RESP_CLASS: (),
            FIELDS_NAME: ((),),
            FIELDS_VALUE: ((),)
        }
    }
# end def _none_on_make_none_on_break


def _none_on_make_2_on_break(response_class, field_name, field_value):
    """
    Sequence of HID messages returned on a stimulus with no report on make and two reports on break

    :param response_class: The expected HID report class
    :type response_class: ``BitFieldContainerMixin``
    :param field_name: The HID report field name which is modified.
    :type field_name: ``str`` or ``tuple``
    :param field_value: The new value of the modified HID report field
    :type field_value: ``int`` or ``tuple``

    :return: dictionary with 'make' and 'break' keys
    :rtype: ``dict``
    """
    return {
        MAKE: {
            RESP_CLASS: (),
            FIELDS_NAME: ((),),
            FIELDS_VALUE: ((),)
        },
        BREAK: {
            RESP_CLASS: (response_class, response_class),
            FIELDS_NAME: ((field_name,), (field_name,)),
            FIELDS_VALUE: ((field_value,), (-field_value,))
        }
    }
# end def _none_on_make_2_on_break


def _make_break(response_class, field_names, field_values, is_switch_key=False):
    """
    Sequence of HID messages with the same number of reports on the make than on the break

    :param response_class: The expected HID report class
    :type response_class: ``BitFieldContainerMixin``
    :param field_names: The list of HID report fields names which are modified.
    :type field_names: ``list[str]`` or ``str``
    :param field_values: The list of new values of the modified HID report fields
    :type field_values: ``list[int]`` or ``int``
    :param is_switch_key: Flag indicating if the switch key implementation is followed on key press - OPTIONAL
                     cf https://docs.google.com/document/d/1L5hMnkgN0yU2sijrk0jW7mJ2iRFqbeNleYshjAd45C8/edit?usp=sharing
    :type is_switch_key: ``bool``

    :return: dictionary with 'make' and 'break' keys
    :rtype: ``dict``
    """
    field_names = [field_names] if not isinstance(field_names, list) else field_names
    field_values = [field_values] if not isinstance(field_values, list) else field_values
    for index in range(len(field_values)):
        if response_class == HidKeyboard and int(field_values[index]) > int(KDB_USAGE.KEYBOARD_ERROR_ROLLOVER):
            # Keep the HID usage
            field_names[index] = 'key_code1'
        elif response_class == HidKeyboardBitmap and int(field_values[index]) > int(KDB_USAGE.KEYBOARD_ERROR_ROLLOVER):
            # Keep the field name to raise the correct bit in the Bitmap
            field_values[index] = 1
        # end if
    # end for

    make_reports = {
        RESP_CLASS: [response_class for _ in range(len(field_values))],
        FIELDS_NAME: [[x, ] for x in field_names],
        FIELDS_VALUE: [[x, ] for x in field_values]
    }
    break_reports = {
        RESP_CLASS: [response_class for _ in range(len(field_values))],
        FIELDS_NAME: [[x, ] for x in reversed(field_names)],
        FIELDS_VALUE: [[-x, ] for x in reversed(field_values)]
    }

    if is_switch_key:
        resp_class = break_reports[RESP_CLASS].pop(0)
        fields_name = break_reports[FIELDS_NAME].pop(0)
        fields_value = break_reports[FIELDS_VALUE].pop(0)

        make_reports[RESP_CLASS].append(resp_class)
        make_reports[FIELDS_NAME].append(fields_name)
        make_reports[FIELDS_VALUE].append(fields_value)
    # end if

    return {
        MAKE: make_reports,
        BREAK: break_reports
    }
# end def _make_break


def _double_click(response_class, field_name, field_value):
    """
    Sequence of 4 reports on the make than nothing on the break

    :param response_class: The expected HID report class
    :type response_class: ``BitFieldContainerMixin``
    :param field_name: HID report field name which are modified.
    :type field_name: ``str``
    :param field_value: new value of the modified HID report field
    :type field_value: ``int``

    :return: dictionary with 'make' and 'break' keys
    :rtype: ``dict``
    """
    if response_class == HidKeyboard and int(field_value) > int(KDB_USAGE.KEYBOARD_ERROR_ROLLOVER):
        # Keep the HID usage
        field_name = 'key_code1'
    elif response_class == HidKeyboardBitmap and int(field_value) > int(KDB_USAGE.KEYBOARD_ERROR_ROLLOVER):
        # Keep the field name to raise the correct bit in the Bitmap
        field_value = 1
    # end if

    return {
        MAKE: {RESP_CLASS: tuple(response_class for _ in range(4)),
               FIELDS_NAME: ((field_name,), (field_name,), (field_name,), (field_name,),),
               FIELDS_VALUE: ((field_value,), (-field_value,), (field_value,), (-field_value,),)},
        BREAK: {RESP_CLASS: (), FIELDS_NAME: ((),), FIELDS_VALUE: ((),)}
    }
# end def _double_click


class HidData:
    """
    HID Report translation tables
    """
    HidKeyboardGuidelinesVersion = None
    HidMouseReport = None
    HidKeyboardReport = None
    HidConsumerReport = None
    HidSystemControlsReport = None
    HidCallStateManagementControlReport = None
    HidOptions = None
    # Backup classes to handle boot mode switching
    HidMouseReportProtocol = None
    HidKeyboardReportProtocol = None

    IsGaming = None

    class Versions(float, Enum):
        """
        Guidelines for Keyboard Keys document supported versions
        """
        V1_0 = 1.0
        V1_1 = 1.1
        V2_0 = 2.0
        V2_1 = 2.1
        V2_2 = 2.2
        V2_3 = 2.3
        V2_4 = 2.4
        V2_5 = 2.5
        V2_6 = 2.6
        V2_7 = 2.7
        V2_8 = 2.8
        V3_0 = 3.0
        V3_1 = 3.1
    # end class Versions

    class Options:
        """
        List of product features that could impact the HID report translation
        """
        HORIZONTAL_SCROLLING = 'horizontal_scrolling'
        EMOJI_MENU_BUTTON = 'emoji_menu_button'
        KATAHIRA = 'katahira'
    # end class Options

    class Protocol(IntEnum):
        """
        USB protocol modes
        """
        BOOT = 0
        REPORT = 1
    # end class Protocol

    KEY_ID_TO_HID_MAP = None

    NOT_SINGLE_ACTION_KEYS = None

    CONSUMER_KEYS = None
    # Bit set in report
    SET = 1

    @classmethod
    def configure(cls, version, is_gaming, mouse_report_type='HidMouse', keyboard_report_type='HidKeyboardBitmap',
                  consumer_report_type='HidConsumer', options=None):
        """
        Configure HID reports type and HID Guidelines version.

        :param version: Keyboard HID Guidelines version
        :type version: ``float`` or ``None``
        :param is_gaming: DUT is gaming product or not
        :type is_gaming: ``bool``
        :param mouse_report_type: Format of the HID Mouse report supported by the DUT - OPTIONAL
        :type mouse_report_type: ``str`` or ``None``
        :param keyboard_report_type: Format of the HID Keyboard report supported by the DUT - OPTIONAL
        :type keyboard_report_type: ``str`` or ``None``
        :param consumer_report_type: Format of the HID Consumer report supported by the DUT - OPTIONAL
        :type consumer_report_type: ``str`` or ``None``
        :param options: Options that could impact the HID report translation cf Options class - OPTIONAL
        :type options: ``list[str]`` or ``None``

        :raise ``AssertionError``: Unsupported mouse report type, keyboard report type consumer report type or HID
            Guidelines version
        """
        assert mouse_report_type in [None, 'HidMouse', 'HidMouseNvidiaExtension']
        mouse_report_type = 'HidMouse' if mouse_report_type is None else mouse_report_type
        cls.HidMouseReport = globals()[mouse_report_type]
        cls.HidMouseReportProtocol = cls.HidMouseReport

        assert keyboard_report_type in [None, 'HidKeyboard', 'HidKeyboardBitmap']
        keyboard_report_type = 'HidKeyboardBitmap' if keyboard_report_type is None else keyboard_report_type
        cls.HidKeyboardReport = globals()[keyboard_report_type]
        cls.HidKeyboardReportProtocol = cls.HidKeyboardReport

        assert consumer_report_type in [None, 'HidConsumer']
        consumer_report_type = 'HidConsumer' if consumer_report_type is None else consumer_report_type
        cls.HidConsumerReport = globals()[consumer_report_type]

        cls.HidSystemControlsReport = globals()['HidSystemControl']
        cls.HidCallStateManagementControlReport = globals()['HidCallStateManagementControl']

        assert version in [v.value for v in cls.Versions] + [None]
        cls.HidKeyboardGuidelinesVersion = version

        if options is None:
            cls.HidOptions = []
        else:
            cls.HidOptions = options
        # end if

        cls.IsGaming = is_gaming

        cls.KEY_ID_TO_HID_MAP = {**cls._get_common_table(), **cls._get_mouse_table(),
                                 **cls._get_kdb_table(), **cls._get_options_table()}

        if cls.CONSUMER_KEYS is None:
            cls.collect_consumer_keys()
        # end if
    # end def configure

    @classmethod
    def set_protocol(cls, mode=Protocol.REPORT):
        """
        Configure HID reports type based on the USB protocol mode.

        :param mode: Boot or Report protocol - OPTIONAL
        :type mode: ``int``

        :raise ``AssertionError``: Unsupported USB protocol mode
        """
        assert mode in [cls.Protocol.BOOT, cls.Protocol.REPORT]
        if mode == cls.Protocol.REPORT:
            cls.HidMouseReport = cls.HidMouseReportProtocol
            cls.HidKeyboardReport = cls.HidKeyboardReportProtocol
        else:
            cls.HidMouseReport = globals()['HidMouse']
            cls.HidKeyboardReport = globals()['HidKeyboard']
        # end if

        cls.KEY_ID_TO_HID_MAP = {**cls._get_common_table(), **cls._get_mouse_table(),
                                 **cls._get_kdb_table(), **cls._get_options_table()}
    # end def set_protocol

    @classmethod
    def _get_common_table(cls):
        """
        Generate the generic part of the HID translation table.

        :return: HID translation table
        :rtype: ``dict``
        """
        return {
            # Mouse keys
            KEY_ID.LEFT_BUTTON: {OS.ALL: _make_break(cls.HidMouseReport, 'button1', cls.SET)},
            KEY_ID.RIGHT_BUTTON: {OS.ALL: _make_break(cls.HidMouseReport, 'button2', cls.SET)},
            KEY_ID.MIDDLE_BUTTON: {OS.ALL: _make_break(cls.HidMouseReport, 'button3', cls.SET)},

            # Keyboard keys
            KEY_ID.HOST_1: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.HOST_2: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.HOST_3: {OS.ALL: _none_on_make_none_on_break()},
        }
    # end def _get_common_table

    @classmethod
    def _get_mouse_table(cls):
        """
        Generate the mouse part of the HID translation table.

        :return: HID translation table
        :rtype: ``dict``
        """
        return {
            # Mouse keys
            KEY_ID.BACK_BUTTON: {OS.ALL: _make_break(cls.HidMouseReport, 'button4', cls.SET)},
            KEY_ID.FORWARD_BUTTON: {OS.ALL: _make_break(cls.HidMouseReport, 'button5', cls.SET)},
            KEY_ID.SMART_SHIFT: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.VIRTUAL_GESTURE_BUTTON: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.DPI_CHANGE: {OS.ALL: _make_break(cls.HidMouseReport, 'button6', cls.SET)},
            KEY_ID.DPI_SWITCH: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.APP_SWITCH_GESTURE: {
                OS.WINDOWS: {
                    MAKE: {
                        RESP_CLASS: (HidKeyboard, HidKeyboard, HidKeyboard),
                        FIELDS_NAME: (('keyboard_control4',),
                                      ('keyboard_control4', 'key_code1'),
                                      ('keyboard_control4', 'key_code1')),
                        FIELDS_VALUE: ((1,), (1, KDB_USAGE.KEYBOARD_TAB), (1, 0))
                    },
                    BREAK: {
                        RESP_CLASS: (HidKeyboard,),
                        FIELDS_NAME: (('keyboard_control4',),),
                        FIELDS_VALUE: ((0,),)
                    }
                },
            },
            KEY_ID.BUTTON_1: {OS.ALL: _make_break(cls.HidMouseReport, 'button1', cls.SET)},
            KEY_ID.BUTTON_2: {OS.ALL: _make_break(cls.HidMouseReport, 'button2', cls.SET)},
            KEY_ID.BUTTON_3: {OS.ALL: _make_break(cls.HidMouseReport, 'button3', cls.SET)},
            KEY_ID.BUTTON_4: {OS.ALL: _make_break(cls.HidMouseReport, 'button4', cls.SET)},
            KEY_ID.BUTTON_5: {OS.ALL: _make_break(cls.HidMouseReport, 'button5', cls.SET)},
            KEY_ID.BUTTON_6: {OS.ALL: _make_break(cls.HidMouseReport, 'button6', cls.SET)},
            KEY_ID.BUTTON_7: {OS.ALL: _make_break(cls.HidMouseReport, 'button7', cls.SET)},
            KEY_ID.BUTTON_8: {OS.ALL: _make_break(cls.HidMouseReport, 'button8', cls.SET)},
            KEY_ID.BUTTON_9: {OS.ALL: _make_break(cls.HidMouseReport, 'button9', cls.SET)},
            KEY_ID.BUTTON_10: {OS.ALL: _make_break(cls.HidMouseReport, 'button10', cls.SET)},
            KEY_ID.BUTTON_11: {OS.ALL: _make_break(cls.HidMouseReport, 'button11', cls.SET)},
            KEY_ID.BUTTON_12: {OS.ALL: _make_break(cls.HidMouseReport, 'button12', cls.SET)},
            KEY_ID.BUTTON_13: {OS.ALL: _make_break(cls.HidMouseReport, 'button13', cls.SET)},
            KEY_ID.BUTTON_14: {OS.ALL: _make_break(cls.HidMouseReport, 'button14', cls.SET)},
            KEY_ID.BUTTON_15: {OS.ALL: _make_break(cls.HidMouseReport, 'button15', cls.SET)},
            KEY_ID.BUTTON_16: {OS.ALL: _make_break(cls.HidMouseReport, 'button16', cls.SET)},

            KEY_ID.LAUNCH_DIDOT: {OS.ALL: _none_on_make_none_on_break()},
        }
    # end def _get_mouse_table

    @classmethod
    def _get_options_table(cls):
        """
        Generate some project specific translation based on supported options.

        :return: HID translation table
        :rtype: ``dict``
        """
        optional_map = {}
        if cls.Options.HORIZONTAL_SCROLLING in cls.HidOptions:
            # Virtual thumb wheel feature
            optional_map[KEY_ID.BACK_BUTTON] = {
                OS.ALL: _none_on_make_2_on_break(cls.HidMouseReport, 'button4', cls.SET)}
            optional_map[KEY_ID.FORWARD_BUTTON] = {
                OS.ALL: _none_on_make_2_on_break(cls.HidMouseReport, 'button5', cls.SET)}
        # end if
        if cls.Options.EMOJI_MENU_BUTTON in cls.HidOptions:
            # Reconfigurable island button for emoji menu
            optional_map[KEY_ID.EMOJI_PANEL] = {OS.ALL: _make_break(cls.HidMouseReport, 'button6', cls.SET)}
        # end if
        if cls.Options.KATAHIRA in cls.HidOptions:
            # KataHira (Line 102) - Only implemented on POLLUX
            optional_map[KEY_ID.KATAHIRA] = {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2)}
        # end if
        return optional_map
    # end def _get_options_table

    @classmethod
    def _get_kdb_table(cls):
        """
        Generate the keyboard part of the HID translation table.

        :return: HID translation table
        :rtype: ``dict``

        :raise ``ValueError``: Unsupported HID Keyboard Guidelines version
        """
        if cls.IsGaming:
            if cls.HidKeyboardGuidelinesVersion is None:
                return {}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V1_0:
                return {**cls._get_kdb_common_table(), **cls._get_gaming_kdb_guidelines_v1_0()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V1_1:
                return {**cls._get_kdb_common_table(), **cls._get_gaming_kdb_guidelines_v1_1()}
            else:
                raise ValueError(f'Unsupported Gaming keyboard guideline version: {cls.HidKeyboardGuidelinesVersion}')
            # end if
        else:
            if cls.HidKeyboardGuidelinesVersion is None:
                return {}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_0:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_0()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_1:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_1()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_2:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_2()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_3:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_3()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_4:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_4()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_5:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_5()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_6:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_6()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_7:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_7()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V2_8:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v2_8()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V3_0:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v3_0()}
            elif cls.HidKeyboardGuidelinesVersion == cls.Versions.V3_1:
                return {**cls._get_kdb_common_table(), **cls._get_pws_kdb_guidelines_v3_1()}
            else:
                raise ValueError(f'Unsupported PWS keyboard guideline version: {cls.HidKeyboardGuidelinesVersion}')
            # end if
        # end if
    # end def _get_kdb_table

    @classmethod
    def _get_kdb_common_table(cls):
        """
        Generate the generic HID Keyboard translation table for PWS and Gaming KBD guideline.
        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/#gid=1598546599 PWS v2.0
        https://docs.google.com/spreadsheets/d/1rY01b28rLEhpvsTUykMTK9KN2khjRY9L_ZD1_6oyMpI/#gid=1472794435 Gaming v1.0

        :return: HID translation table
        :rtype: ``dict``
        """
        return {
            # STANDARD HID USAGE(KEYBOARD/KEYPAD/CONSUMER PAGES)
            KEY_ID.KEYBOARD_A: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_A', KDB_USAGE.KEYBOARD_A_AND_A)},
            KEY_ID.KEYBOARD_B: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_B', KDB_USAGE.KEYBOARD_B_AND_B)},
            KEY_ID.KEYBOARD_C: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_C', KDB_USAGE.KEYBOARD_C_AND_C)},
            KEY_ID.KEYBOARD_D: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_D', KDB_USAGE.KEYBOARD_D_AND_D)},
            KEY_ID.KEYBOARD_E: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_E', KDB_USAGE.KEYBOARD_E_AND_E)},
            KEY_ID.KEYBOARD_F: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F', KDB_USAGE.KEYBOARD_F_AND_F)},
            KEY_ID.KEYBOARD_G: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_G', KDB_USAGE.KEYBOARD_G_AND_G)},
            KEY_ID.KEYBOARD_H: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_H', KDB_USAGE.KEYBOARD_H_AND_H)},
            KEY_ID.KEYBOARD_I: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_I', KDB_USAGE.KEYBOARD_I_AND_I)},
            KEY_ID.KEYBOARD_J: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_J', KDB_USAGE.KEYBOARD_J_AND_J)},
            KEY_ID.KEYBOARD_K: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_K', KDB_USAGE.KEYBOARD_K_AND_K)},
            KEY_ID.KEYBOARD_L: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_L', KDB_USAGE.KEYBOARD_L_AND_L)},
            KEY_ID.KEYBOARD_M: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_M', KDB_USAGE.KEYBOARD_M_AND_M)},
            KEY_ID.KEYBOARD_N: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_N', KDB_USAGE.KEYBOARD_N_AND_N)},
            KEY_ID.KEYBOARD_O: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_O', KDB_USAGE.KEYBOARD_O_AND_O)},
            KEY_ID.KEYBOARD_P: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_P', KDB_USAGE.KEYBOARD_P_AND_P)},
            KEY_ID.KEYBOARD_Q: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_Q', KDB_USAGE.KEYBOARD_Q_AND_Q)},
            KEY_ID.KEYBOARD_R: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_R', KDB_USAGE.KEYBOARD_R_AND_R)},
            KEY_ID.KEYBOARD_S: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_S', KDB_USAGE.KEYBOARD_S_AND_S)},
            KEY_ID.KEYBOARD_T: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_T', KDB_USAGE.KEYBOARD_T_AND_T)},
            KEY_ID.KEYBOARD_U: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_U', KDB_USAGE.KEYBOARD_U_AND_U)},
            KEY_ID.KEYBOARD_V: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_V', KDB_USAGE.KEYBOARD_V_AND_V)},
            KEY_ID.KEYBOARD_W: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_W', KDB_USAGE.KEYBOARD_W_AND_W)},
            KEY_ID.KEYBOARD_X: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_X', KDB_USAGE.KEYBOARD_X_AND_X)},
            KEY_ID.KEYBOARD_Y: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_Y', KDB_USAGE.KEYBOARD_Y_AND_Y)},
            KEY_ID.KEYBOARD_Z: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_Z', KDB_USAGE.KEYBOARD_Z_AND_Z)},
            # 0 and )
            KEY_ID.KEYBOARD_0: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_0', KDB_USAGE.KEYBOARD_0_AND_)},
            # 1 and !
            KEY_ID.KEYBOARD_1: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_1', KDB_USAGE.KEYBOARD_1_AND_)},
            # 2 and @
            KEY_ID.KEYBOARD_2: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_2', KDB_USAGE.KEYBOARD_2_AND_)},
            # 3 and #
            KEY_ID.KEYBOARD_3: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_3', KDB_USAGE.KEYBOARD_3_AND_)},
            # 4 and $
            KEY_ID.KEYBOARD_4: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_4', KDB_USAGE.KEYBOARD_4_AND_)},
            # 5 and %
            KEY_ID.KEYBOARD_5: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_5', KDB_USAGE.KEYBOARD_5_AND_)},
            # 6 and ^
            KEY_ID.KEYBOARD_6: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_6', KDB_USAGE.KEYBOARD_6_AND_)},
            # 7 and &
            KEY_ID.KEYBOARD_7: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_7', KDB_USAGE.KEYBOARD_7_AND_)},
            # 8 and *
            KEY_ID.KEYBOARD_8: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_8', KDB_USAGE.KEYBOARD_8_AND_)},
            # 9 and (
            KEY_ID.KEYBOARD_9: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_9', KDB_USAGE.KEYBOARD_9_AND_)},
            KEY_ID.KEYBOARD_F1: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F1', KDB_USAGE.KEYBOARD_F1)},
            KEY_ID.KEYBOARD_F2: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F2', KDB_USAGE.KEYBOARD_F2)},
            KEY_ID.KEYBOARD_F3: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F3', KDB_USAGE.KEYBOARD_F3)},
            KEY_ID.KEYBOARD_F4: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F4', KDB_USAGE.KEYBOARD_F4)},
            KEY_ID.KEYBOARD_F5: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F5', KDB_USAGE.KEYBOARD_F5)},
            KEY_ID.KEYBOARD_F6: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F6', KDB_USAGE.KEYBOARD_F6)},
            KEY_ID.KEYBOARD_F7: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F7', KDB_USAGE.KEYBOARD_F7)},
            KEY_ID.KEYBOARD_F8: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F8', KDB_USAGE.KEYBOARD_F8)},
            KEY_ID.KEYBOARD_F9: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F9', KDB_USAGE.KEYBOARD_F9)},
            KEY_ID.KEYBOARD_F10: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F10', KDB_USAGE.KEYBOARD_F10)},
            KEY_ID.KEYBOARD_F11: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F11', KDB_USAGE.KEYBOARD_F11)},
            KEY_ID.KEYBOARD_F12: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F12', KDB_USAGE.KEYBOARD_F12)},
            KEY_ID.KEYBOARD_F13: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F13', KDB_USAGE.KEYBOARD_F13)},
            KEY_ID.KEYBOARD_F14: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F14', KDB_USAGE.KEYBOARD_F14)},
            KEY_ID.KEYBOARD_F15: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F15', KDB_USAGE.KEYBOARD_F15)},
            KEY_ID.KEYBOARD_F16: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F16', KDB_USAGE.KEYBOARD_F16)},
            KEY_ID.KEYBOARD_F17: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F17', KDB_USAGE.KEYBOARD_F17)},
            KEY_ID.KEYBOARD_F18: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F18', KDB_USAGE.KEYBOARD_F18)},
            KEY_ID.KEYBOARD_F19: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F19', KDB_USAGE.KEYBOARD_F19)},
            KEY_ID.KEYBOARD_F20: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F20', KDB_USAGE.KEYBOARD_F20)},
            KEY_ID.KEYBOARD_F21: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F21', KDB_USAGE.KEYBOARD_F21)},
            KEY_ID.KEYBOARD_F22: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F22', KDB_USAGE.KEYBOARD_F22)},
            KEY_ID.KEYBOARD_F23: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F23', KDB_USAGE.KEYBOARD_F23)},
            KEY_ID.KEYBOARD_F24: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F24', KDB_USAGE.KEYBOARD_F24)},
            KEY_ID.KEYBOARD_RIGHT_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ARROW', KDB_USAGE.KEYBOARD_RIGHT_ARROW)},
            KEY_ID.KEYBOARD_LEFT_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ARROW', KDB_USAGE.KEYBOARD_LEFT_ARROW)},
            KEY_ID.KEYBOARD_DOWN_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_DOWN_ARROW', KDB_USAGE.KEYBOARD_DOWN_ARROW)},
            KEY_ID.KEYBOARD_UP_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_UP_ARROW', KDB_USAGE.KEYBOARD_UP_ARROW)},
            KEY_ID.FN_KEY: {OS.ALL: _none_on_make_none_on_break()},
            # ` and ~
            KEY_ID.KEYBOARD_GRAVE_ACCENT_AND_TILDE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_GRAVE_ACCENT_AND_TILDE', KDB_USAGE.KEYBOARD_GRAVE_ACCENT_AND_TILDE)},
            # Enter
            KEY_ID.KEYBOARD_RETURN_ENTER: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_RETURN_ENTER', KDB_USAGE.KEYBOARD_RETURN_ENTER)},
            # \ and |
            KEY_ID.KEYBOARD_BACKSLASH_AND_PIPE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_BACKSLASH_AND_PIPE', KDB_USAGE.KEYBOARD_BACKSLASH_AND_PIPE)},
            # Esc
            KEY_ID.KEYBOARD_ESCAPE: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_ESCAPE', KDB_USAGE.KEYBOARD_ESCAPE)},
            # = and +
            KEY_ID.KEYBOARD_EQUAL_AND_PLUS: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_EQUAL_AND_PLUS', KDB_USAGE.KEYBOARD_EQUAL_AND_PLUS)},
            # Delete(backspace)
            KEY_ID.KEYBOARD_BACKSPACE: {
                OS.ALL: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_BACKSPACE', KDB_USAGE.KEYBOARD_DELETE_BACKSPACE)},
            # - and _
            KEY_ID.KEYBOARD_DASH_AND_UNDERSCORE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_DASH_AND_UNDERSCORE', KDB_USAGE.KEYBOARD_DASH_AND_UNDERSCORE)},
            # [ and {
            KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_LEFT_BRACKET_AND_BRACE', KDB_USAGE.KEYBOARD_LEFT_BRACKET_AND_BRACE)},
            # ] and }
            KEY_ID.KEYBOARD_RIGHT_BRACKET_AND_BRACE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_RIGHT_BRACKET_AND_BRACE', KDB_USAGE.KEYBOARD_RIGHT_BRACKET_AND_BRACE)},
            # ; and :
            KEY_ID.KEYBOARD_SEMICOLON_AND_COLON: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_SEMICOLON_AND_COLON', KDB_USAGE.KEYBOARD_SEMICOLON_AND_COLON)},
            # ' and "
            KEY_ID.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK',
                                    KDB_USAGE.KEYBOARD_APOSTROPHE_AND_QUOTATION_MARK)},
            # / and ?
            KEY_ID.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK',
                KDB_USAGE.KEYBOARD_FORWARD_SLASH_AND_QUESTION_MARK)},
            # . and >
            KEY_ID.KEYBOARD_PERIOD_AND_MORE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_PERIOD_AND_MORE', KDB_USAGE.KEYBOARD_PERIOD_AND_MORE)},
            # , and <
            KEY_ID.KEYBOARD_COMMA_AND_LESS: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_COMMA_AND_LESS', KDB_USAGE.KEYBOARD_COMMA_AND_LESS)},
            KEY_ID.KEYBOARD_SPACE_BAR: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_SPACE_BAR', KDB_USAGE.KEYBOARD_SPACE_BAR)},
            # Non-US # and ~
            KEY_ID.KEYBOARD_NON_US_AND_TILDE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_NON_US_AND_TILDE', KDB_USAGE.KEYBOARD_NON_US_AND_TILDE)},
            # Non-US \ and |
            KEY_ID.KEYBOARD_NON_US_BACKSLASH_AND_PIPE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_NON_US_BACKSLASH_AND_PIPE',
                KDB_USAGE.KEYBOARD_NON_US_BACKSLASH_AND_PIPE)},
            KEY_ID.KEYBOARD_PRINT_SCREEN: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PRINT_SCREEN', KDB_USAGE.KEYBOARD_PRINT_SCREEN)},

            # Language input keys
            KEY_ID.KEYBOARD_INTERNATIONAL1: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL1', KDB_USAGE.KEYBOARD_INTERNATIONAL1)},
            KEY_ID.KEYBOARD_INTERNATIONAL2: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2)},
            KEY_ID.KEYBOARD_INTERNATIONAL3: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL3', KDB_USAGE.KEYBOARD_INTERNATIONAL3)},
            KEY_ID.KEYBOARD_INTERNATIONAL4: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL4', KDB_USAGE.KEYBOARD_INTERNATIONAL4)},
            KEY_ID.KEYBOARD_INTERNATIONAL5: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL5', KDB_USAGE.KEYBOARD_INTERNATIONAL5)},
            # Muhenkan (Win/ChromeOS only) + Alphanumeric (MAC only)
            KEY_ID.MUHENKAN: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL5', KDB_USAGE.KEYBOARD_INTERNATIONAL5),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL5', KDB_USAGE.KEYBOARD_INTERNATIONAL5)},
            # Henkan (Win/ChromeOS only) + Kana (MAC only)
            KEY_ID.HENKAN: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL4', KDB_USAGE.KEYBOARD_INTERNATIONAL4),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL4', KDB_USAGE.KEYBOARD_INTERNATIONAL4)},
            KEY_ID.YEN: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL3', KDB_USAGE.KEYBOARD_INTERNATIONAL3)},
            # KataHira (Win/ChromeOS only)
            KEY_ID.KATAHIRA: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2)},
            KEY_ID.RO: {
                OS.ALL: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL1', KDB_USAGE.KEYBOARD_INTERNATIONAL1)},
            # Kana (MAC only)
            KEY_ID.KANA: {
                OS.WINDOWS: _none_on_make_none_on_break(),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.CHROME: _none_on_make_none_on_break()},
            KEY_ID.HANJA: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2)},
            KEY_ID.HANGUEL: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1)},

            # Keypad
            KEY_ID.KEYPAD_EQUAL: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_EQUAL', KDB_USAGE.KEYPAD_EQUAL)},
            KEY_ID.KEYPAD_FORWARD_SLASH: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_FORWARD_SLASH', KDB_USAGE.KEYPAD_FORWARD_SLASH)},
            KEY_ID.KEYPAD_ASTERISK: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_ASTERISK', KDB_USAGE.KEYPAD_ASTERISK)},
            KEY_ID.KEYPAD_MINUS: {_make_break: _make_break(
                cls.HidKeyboardReport, 'KEYPAD_MINUS', KDB_USAGE.KEYPAD_DASH)},
            KEY_ID.KEYPAD_PLUS: {_make_break: _make_break(cls.HidKeyboardReport, 'KEYPAD_PLUS', KDB_USAGE.KEYPAD_PLUS)},
            KEY_ID.KEYPAD_ENTER: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER)},
            KEY_ID.KEYPAD_1_AND_END: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_1_AND_END', KDB_USAGE.KEYPAD_1_AND_END)},
            KEY_ID.KEYPAD_2_AND_DOWN_ARROW: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYPAD_2_AND_DOWN_ARROW', KDB_USAGE.KEYPAD_2_AND_DOWN_ARROW)},
            KEY_ID.KEYPAD_3_AND_PAGE_DN: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_3_AND_PAGE_DN', KDB_USAGE.KEYPAD_3_AND_PAGE_DN)},
            KEY_ID.KEYPAD_4_AND_LEFT_ARROW: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYPAD_4_AND_LEFT_ARROW', KDB_USAGE.KEYPAD_4_AND_LEFT_ARROW)},
            KEY_ID.KEYPAD_5: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_5', KDB_USAGE.KEYPAD_5)},
            KEY_ID.KEYPAD_6_AND_RIGHT_ARROW: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYPAD_6_AND_RIGHT_ARROW', KDB_USAGE.KEYPAD_6_AND_RIGHT_ARROW)},
            KEY_ID.KEYPAD_7_AND_HOME: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_7_AND_HOME', KDB_USAGE.KEYPAD_7_AND_HOME)},
            KEY_ID.KEYPAD_8_AND_UP_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_8_AND_UP_ARROW', KDB_USAGE.KEYPAD_8_AND_UP_ARROW)},
            KEY_ID.KEYPAD_9_AND_PAGE_UP: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_9_AND_PAGE_UP', KDB_USAGE.KEYPAD_9_AND_PAGE_UP)},
            KEY_ID.KEYPAD_0_AND_INSERT: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYPAD_0_AND_INSERT', KDB_USAGE.KEYPAD_0_AND_INSERT)},
            KEY_ID.KEYPAD_PERIOD_AND_DELETE: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYPAD_COMMA_AND_DELETE', KDB_USAGE.KEYPAD_COMMA_AND_DELETE)},
            # Pause / Break
            KEY_ID.KEYBOARD_PAUSE: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAUSE',
                                                        KDB_USAGE.KEYBOARD_PAUSE)},
            # Power button
            KEY_ID.KEYBOARD_POWER: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_POWER', KDB_USAGE.KEYBOARD_POWER)},
            # Menu button
            KEY_ID.KEYBOARD_MENU: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_MENU', KDB_USAGE.KEYBOARD_MENU),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break()
            },
            # Stop
            KEY_ID.KEYBOARD_STOP: {OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.STOP),
                                   OS.BOOT: _none_on_make_none_on_break()},
            # Eject
            KEY_ID.EJECT: {
                OS.MAC: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.EJECT),
                OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.EJECT)},
            # Not 'US'
            KEY_ID.KEYBOARD_NO_US_42: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_NON_US_AND_TILDE',
                                        KDB_USAGE.KEYBOARD_NON_US_AND_TILDE),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_BACKSLASH_AND_PIPE',
                                    KDB_USAGE.KEYBOARD_BACKSLASH_AND_PIPE),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_BACKSLASH_AND_PIPE',
                                     KDB_USAGE.KEYBOARD_BACKSLASH_AND_PIPE),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_NON_US_AND_TILDE',
                                       KDB_USAGE.KEYBOARD_NON_US_AND_TILDE)},
            KEY_ID.KEYBOARD_NO_US_1: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_GRAVE_ACCENT_AND_TILDE',
                                        KDB_USAGE.KEYBOARD_GRAVE_ACCENT_AND_TILDE),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_NON_US_BACKSLASH_AND_PIPE',
                                    KDB_USAGE.KEYBOARD_NON_US_BACKSLASH_AND_PIPE),
                OS.INVERTED_MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_GRAVE_ACCENT_AND_TILDE',
                                             KDB_USAGE.KEYBOARD_GRAVE_ACCENT_AND_TILDE),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_NON_US_BACKSLASH_AND_PIPE',
                                     KDB_USAGE.KEYBOARD_NON_US_BACKSLASH_AND_PIPE),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_GRAVE_ACCENT_AND_TILDE',
                                       KDB_USAGE.KEYBOARD_GRAVE_ACCENT_AND_TILDE)},
            KEY_ID.KEYBOARD_NO_US_45: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_NON_US_BACKSLASH_AND_PIPE',
                                        KDB_USAGE.KEYBOARD_NON_US_BACKSLASH_AND_PIPE),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_GRAVE_ACCENT_AND_TILDE',
                                    KDB_USAGE.KEYBOARD_GRAVE_ACCENT_AND_TILDE),
                OS.INVERTED_MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_NON_US_BACKSLASH_AND_PIPE',
                                             KDB_USAGE.KEYBOARD_NON_US_BACKSLASH_AND_PIPE),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_GRAVE_ACCENT_AND_TILDE',
                                     KDB_USAGE.KEYBOARD_GRAVE_ACCENT_AND_TILDE),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_NON_US_BACKSLASH_AND_PIPE',
                                       KDB_USAGE.KEYBOARD_NON_US_BACKSLASH_AND_PIPE)},

            # COMMON KEYS ON BOTH KBD GUIDELINE
            # Scroll Lock (PWS v2.0 Line 5, G v1.0 Line 5)
            KEY_ID.KEYBOARD_SCROLL_LOCK: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_SCROLL_LOCK', KDB_USAGE.KEYBOARD_SCROLL_LOCK),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _none_on_make_none_on_break()},
            # Previous Track(PWS v2.0 Line 13, G v1.0 Line 7)
            KEY_ID.PREV_TRACK: {OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.SCAN_PREVIOUS_TRACK),
                                OS.BOOT: _none_on_make_none_on_break()},
            # Play / Pause(PWS v2.0 Line 14, G v1.0 Line 8)
            KEY_ID.PLAY_PAUSE: {OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.PLAY_PAUSE),
                                OS.BOOT: _none_on_make_none_on_break()},
            # Next Track(PWS v2.0 Line 15, G v1.0 Line 9)
            KEY_ID.NEXT_TRACK: {OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.SCAN_NEXT_TRACK),
                                OS.BOOT: _none_on_make_none_on_break()},
            # Mute Sound(PWS v2.0 Line 16, G v1.0 Line 10)
            KEY_ID.KEYBOARD_MUTE: {OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.MUTE),
                                   OS.BOOT: _none_on_make_none_on_break()},
            # Contextual menu(PWS v2.0 Line 21, G v1.0 Line 6)
            KEY_ID.CONTEXTUAL_MENU: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_MENU', KDB_USAGE.KEYBOARD_APPLICATION),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_MENU', KDB_USAGE.KEYBOARD_APPLICATION)},
            # Insert Key (Windows only) (PWS v2.0 Line 32, G v1.0 Line 28)
            KEY_ID.KEYBOARD_INSERT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_INSERT', KDB_USAGE.KEYBOARD_INSERT),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _none_on_make_none_on_break()},
            # Delete key (PWS v2.0 Line 33, G v1.0 Line 29)
            KEY_ID.KEYBOARD_DELETE_FORWARD: {OS.ALL: _make_break(
                cls.HidKeyboardReport, 'KEYBOARD_DELETE_FORWARD', KDB_USAGE.KEYBOARD_DELETE_FORWARD)},
            # Home Key (text editing) (PWS v2.0 Line 34, G v1.0 Line)
            KEY_ID.KEYBOARD_HOME: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_LEFT_ARROW'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW]),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME), },
            # End key (text editing) (PWS v2.0 Line 35, G v1.0 Line 31)
            KEY_ID.KEYBOARD_END: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_RIGHT_ARROW'],
                    [cls.SET, KDB_USAGE.KEYBOARD_RIGHT_ARROW]),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END)},
            # Page Up (PWS v2.0 Line 36, G v1.0 Line 32)
            KEY_ID.KEYBOARD_PAGE_UP: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAGE_UP', KDB_USAGE.KEYBOARD_PAGE_UP)},
            # Page Up (PWS v2.0 Line 37, G v1.0 Line 33)
            KEY_ID.KEYBOARD_PAGE_DOWN: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAGE_DOWN', KDB_USAGE.KEYBOARD_PAGE_DOWN)},
            # Num Lock / Clear (PWS v2.0 Line 49, G v1.0 Line 93)
            KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_CLEAR', KDB_USAGE.KEYBOARD_CLEAR)},

            # Modifier keys
            # Windows Left (Win only) / Option Left (Mac only) (PWS v2.0 Line 64&68, G v1.0 Line 124)
            KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET)},
            # Windows Right (Win only) / Option Right (Mac only) (PWS v2.0 Line 65&69, G v1.0 Line 126)
            KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET)},
            # Alt Left (Win only) / Command Left (Mac only) (PWS v2.0 Line 66, G v1.0 Line 123)
            KEY_ID.KEYBOARD_LEFT_ALT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET)},
            # Alt Right (Win only) / Command Right (Mac only) (PWS v2.0 Line 67, G v1.0 Line 125)
            KEY_ID.KEYBOARD_RIGHT_ALT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET)},
            # Shift (Left) (PWS v2.0 Line 72, G v1.0 Line 24)
            KEY_ID.KEYBOARD_LEFT_SHIFT: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_SHIFT', cls.SET)},
            # Shift (Right) (PWS v2.0 Line 73, G v1.0 Line 27)
            KEY_ID.KEYBOARD_RIGHT_SHIFT: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_SHIFT', cls.SET)},
            # Ctrl (Left) (PWS v2.0 Line 74, G v1.0 Line 25)
            KEY_ID.KEYBOARD_LEFT_CONTROL: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_CONTROL', cls.SET)},
            # Ctrl (Right) (PWS v2.0 Line 75, G v1.0 Line 26)
            KEY_ID.KEYBOARD_RIGHT_CONTROL: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_CONTROL', cls.SET)},
            # Ctrl (Right) / Option Right - R-option is printed on the same key as R-Ctrl
            # (PWS v2.0 Line 69,75 & G v1.0 Line 26,126)
            KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_CONTROL', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_CONTROL', cls.SET)},
            # Caps Lock (PWS v2.0 Line 76 & G v1.0 Line 23)
            KEY_ID.KEYBOARD_CAPS_LOCK: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_CAPS_LOCK', KDB_USAGE.KEYBOARD_CAPS_LOCK)},
            # Tab (PWS v2.0 Line 77 & G v1.0 Line 22)
            KEY_ID.KEYBOARD_TAB: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_TAB', KDB_USAGE.KEYBOARD_TAB)},

            # OTHERS(NOT DEFINED ON BOTH KBD GUIDELINE)
            KEY_ID.CONNECT_BUTTON: {OS.ALL: _none_on_make_none_on_break()},
            # Screen lock test key on Quark platform
            KEY_ID.DESKTOP_SYSTEM_SLEEP: {OS.ALL: _make_break(
                cls.HidSystemControlsReport, 'POWER_STATE', cls.HidSystemControlsReport.POSITION.SYSTEM_SLEEP)},
            # Platform code compound keys translation
            KEY_ID.COMPOUND_ALT_TAB: {OS.ALL: _make_break(
                cls.HidKeyboardReport, ['keyboard_left_shift', 'keyboard_left_gui', 'KEYBOARD_P'],
                [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_P_AND_P]), },
            KEY_ID.COMPOUND_CTRL_ALT_DEL: {OS.ALL: _make_break(
                cls.HidKeyboardReport, ['keyboard_left_control', 'keyboard_left_alt', 'keyboard_delete_forward'],
                [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_DELETE_FORWARD]), },
            # Fn+'6' (default) -> h-o-m-e
            KEY_ID.COMPOUND_HOME: {OS.ALL: _make_break(
                cls.HidKeyboardReport, ['KEYBOARD_H', 'KEYBOARD_O', 'KEYBOARD_M', 'KEYBOARD_E'],
                [KDB_USAGE.KEYBOARD_H_AND_H, KDB_USAGE.KEYBOARD_O_AND_O, KDB_USAGE.KEYBOARD_M_AND_M,
                 KDB_USAGE.KEYBOARD_E_AND_E]), },
            # Fn+'6' (ISO-104) -> d-o-m
            KEY_ID.COMPOUND_HOME_ISO_104: {OS.ALL: _make_break(
                cls.HidKeyboardReport, ['KEYBOARD_D', 'KEYBOARD_O', 'KEYBOARD_M'],
                [KDB_USAGE.KEYBOARD_D_AND_D, KDB_USAGE.KEYBOARD_O_AND_O, KDB_USAGE.KEYBOARD_M_AND_M]), },
            # Fn+'6' (ISO-105) -> m-a-i-s-o-n
            KEY_ID.COMPOUND_HOME_ISO_105: {OS.ALL: _make_break(
                cls.HidKeyboardReport,
                ['KEYBOARD_M', 'KEYBOARD_A', 'KEYBOARD_I', 'KEYBOARD_S', 'KEYBOARD_O', 'KEYBOARD_N'],
                [KDB_USAGE.KEYBOARD_M_AND_M, KDB_USAGE.KEYBOARD_A_AND_A, KDB_USAGE.KEYBOARD_I_AND_I,
                 KDB_USAGE.KEYBOARD_S_AND_S, KDB_USAGE.KEYBOARD_O_AND_O, KDB_USAGE.KEYBOARD_N_AND_N]), },
            # Fn+'6' (ISO-107) -> l-a-r
            KEY_ID.COMPOUND_HOME_ISO_107: {OS.ALL: _make_break(
                cls.HidKeyboardReport, ['KEYBOARD_L', 'KEYBOARD_A', 'KEYBOARD_R'],
                [KDB_USAGE.KEYBOARD_L_AND_L, KDB_USAGE.KEYBOARD_A_AND_A, KDB_USAGE.KEYBOARD_R_AND_R]), },
            # Fn+'6' (JIS-109) -> j-i-t-a-k-u
            KEY_ID.COMPOUND_HOME_JIS_109: {OS.ALL: _make_break(
                cls.HidKeyboardReport,
                ['KEYBOARD_J', 'KEYBOARD_I', 'KEYBOARD_T', 'KEYBOARD_A', 'KEYBOARD_K', 'KEYBOARD_U'],
                [KDB_USAGE.KEYBOARD_J_AND_J, KDB_USAGE.KEYBOARD_I_AND_I, KDB_USAGE.KEYBOARD_T_AND_T,
                 KDB_USAGE.KEYBOARD_A_AND_A, KDB_USAGE.KEYBOARD_K_AND_K, KDB_USAGE.KEYBOARD_U_AND_U]), },
            KEY_ID.COMPOUND_PASTE: {OS.ALL: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'KEYBOARD_V'],
                                                        [cls.SET, KDB_USAGE.KEYBOARD_V_AND_V]), },
        }
    # end def _get_kdb_common_table

    @classmethod
    def _get_pws_kdb_guidelines_v2_0(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.0.

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/edit#gid=1598546599

        :return: The HID translation table for the Guidelines for Keyboard version 2.0.
        :rtype: ``dict``
        """
        return {
            # Fn Lock (Line 4)
            KEY_ID.FN_LOCK: {OS.ALL: _none_on_make_none_on_break()},
            # Brightness Down(Line 6)
            KEY_ID.BRIGHTNESS_DOWN: {OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.BRIGHTNESS_DOWN),
                                     OS.BOOT: _none_on_make_none_on_break()},
            # Brightness Up(Line 7)
            KEY_ID.BRIGHTNESS_UP: {OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.BRIGHTNESS_UP),
                                   OS.BOOT: _none_on_make_none_on_break()},
            # Task View (Win) / Mission Control (Mac) (Line 8)
            KEY_ID.MISSION_CTRL_TASK_VIEW: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_TAB'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_TAB]),
                OS.MAC: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.OVERVIEW),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_TAB'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_TAB]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.OVERVIEW)},
            # App Switch/ Launchpad (Line 9)
            KEY_ID.APP_SWITCH_LAUNCHPAD: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_ALT', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_TAB], is_switch_key=True),
                OS.MAC: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_LAUNCHPAD),
                OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.MENU),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_DESKTOP_SHOW_ALL_APPLICATIONS)},
            # Show Desktop(Line 10)
            KEY_ID.SHOW_DESKTOP: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_D'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_D_AND_D]),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F11', KDB_USAGE.KEYBOARD_F11),
                OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.MENU),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_VIEW_TOGGLE)},
            # Backlight Decrease(Line 10)
            KEY_ID.BACKLIGHT_DOWN: {OS.ALL: _none_on_make_none_on_break()},
            # Backlight Increase(Line 11)
            KEY_ID.BACKLIGHT_UP: {OS.ALL: _none_on_make_none_on_break()},
            # Volume Down(Line 17)
            KEY_ID.KEYBOARD_VOLUME_DOWN: {
                OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.VOLUME_DOWN),
                OS.BOOT: _none_on_make_none_on_break()},
            # Volume Up(Line 18)
            KEY_ID.KEYBOARD_VOLUME_UP: {
                OS.ALL: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.VOLUME_UP),
                OS.BOOT: _none_on_make_none_on_break()},
            # Calculator(Line 19)
            KEY_ID.CALCULATOR: {
                OS.WINDOWS: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AL_CALCULATOR),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AL_CALCULATOR),
                OS.BOOT: _none_on_make_none_on_break()},
            # Screen Capture(Line 20)
            KEY_ID.SCREEN_CAPTURE: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_SHIFT', 'KEYBOARD_S'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_S_AND_S]),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_SHIFT', 'KEYBOARD_4'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_4_AND_]),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_SHIFT', 'KEYBOARD_3'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_3_AND_]),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_PRINT_SCREEN', KDB_USAGE.KEYBOARD_PRINT_SCREEN)},
            # Screen Lock(Line 22)
            KEY_ID.SCREEN_LOCK: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_L'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_L_AND_L]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_Q'],
                                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_Q_AND_Q]),
                OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.POWER),
                OS.CHROME: _make_break(
                    cls.HidSystemControlsReport, 'POWER_STATE', cls.HidSystemControlsReport.POSITION.SYSTEM_SLEEP)
            },
            # Search / SpotLight (Line 23)
            KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT: {OS.ALL: _make_break(cls.HidConsumerReport, 'key_1',
                                                                      CS_Usage.AC_SEARCH),
                                                  OS.BOOT: _none_on_make_none_on_break()},
            # Home (Line 24)
            KEY_ID.HOME: {OS.WINDOWS: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_HOME),
                          OS.MAC: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.OVERVIEW),
                          OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.MENU),
                          OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_HOME),
                          OS.BOOT: _none_on_make_none_on_break()},
            # Back (Line 25)
            KEY_ID.MULTI_PLATF_BACK: {
                OS.WINDOWS: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_BACK),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_ARROW'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_ARROW'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_BACK),
                OS.BOOT: _none_on_make_none_on_break()},
            # Emoji (Line 26)
            KEY_ID.EMOJI_PANEL: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_PERIOD_AND_MORE'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_PERIOD_AND_MORE]),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.EMOJI_PICKER)},
            # Dictation (Line 27)
            KEY_ID.DICTATION: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_H'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_H_AND_H]),
                OS.MAC: _double_click(cls.HidKeyboardReport, 'KEYBOARD_LEFT_CONTROL', cls.SET),
                OS.IPAD: _double_click(cls.HidKeyboardReport, 'KEYBOARD_LEFT_CONTROL', cls.SET),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.VOICE_DICTATION)},
            # Do not Disturb (Mac only) (Line 28)
            KEY_ID.DO_NOT_DISTURB: {OS.WINDOWS: _none_on_make_none_on_break(),
                                    OS.MAC: _make_break(cls.HidSystemControlsReport, 'DO_NOT_DISTURB', cls.SET),
                                    OS.IPAD: _none_on_make_none_on_break(),
                                    OS.CHROME: _none_on_make_none_on_break()},
            # Mute microphone (Line 29)
            KEY_ID.MUTE_MICROPHONE: {OS.ALL: _none_on_make_none_on_break()},
            # Language switch (Line 30)
            KEY_ID.LANGUAGE_SWITCH: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR], is_switch_key=True),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_NEXT_KEYBOARD_LAYOUT_SELECT)},
            # Lightning Patterns (Line 31)
            KEY_ID.LIGHTNING_PATTERNS: {OS.ALL: _none_on_make_none_on_break()},

            # Fn + KP 7 i.e. Home (Line 38)
            KEY_ID.FN_KEYPAD_7: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_LEFT_ARROW'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW]),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME), },
            # Fn + KP 8 i.e. Up Arrow (Line 39)
            KEY_ID.FN_KEYPAD_8: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_UP_ARROW', KDB_USAGE.KEYBOARD_UP_ARROW)},
            # Fn + KP 9 i.e. Page Up (Line 40)
            KEY_ID.FN_KEYPAD_9: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAGE_UP', KDB_USAGE.KEYBOARD_PAGE_UP)},
            # Fn + KP 4 i.e. Left Arrow (Line 41)
            KEY_ID.FN_KEYPAD_4: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ARROW', KDB_USAGE.KEYBOARD_LEFT_ARROW)},
            # Fn + KP 6 i.e. Right Arrow (Line 42)
            KEY_ID.FN_KEYPAD_6: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ARROW', KDB_USAGE.KEYBOARD_RIGHT_ARROW)},
            # Fn + KP 1 i.e. End (Line 43)
            KEY_ID.FN_KEYPAD_1: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_RIGHT_ARROW'],
                    [cls.SET, KDB_USAGE.KEYBOARD_RIGHT_ARROW]),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END)},
            # Fn + KP 2 i.e. Down Arrow (Line 44)
            KEY_ID.FN_KEYPAD_2: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_DOWN_ARROW', KDB_USAGE.KEYBOARD_DOWN_ARROW)},
            # Fn + KP 3 i.e. Page Down (Line 45)
            KEY_ID.FN_KEYPAD_3: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAGE_DOWN', KDB_USAGE.KEYBOARD_PAGE_DOWN)},
            # Fn + KP 0 i.e. Ins (Line 46)
            KEY_ID.FN_KEYPAD_0: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_INSERT', KDB_USAGE.KEYBOARD_INSERT),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYPAD_0_AND_INSERT', KDB_USAGE.KEYPAD_0_AND_INSERT),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYPAD_0_AND_INSERT', KDB_USAGE.KEYPAD_0_AND_INSERT),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYPAD_0_AND_INSERT', KDB_USAGE.KEYPAD_0_AND_INSERT)},
            # Fn + KP Period i.e. Delete (Line 47)
            KEY_ID.FN_KEYPAD_PERIOD: {OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_DELETE_FORWARD',
                                                          KDB_USAGE.KEYBOARD_DELETE_FORWARD)},
            # Fn + KP Enter (Line 48)
            KEY_ID.FN_KEYPAD_ENTER: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYPAD_EQUAL', KDB_USAGE.KEYPAD_EQUAL),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYPAD_EQUAL', KDB_USAGE.KEYPAD_EQUAL),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER)},
            # NON PRINTED FN KEY FUNCTIONS
            # Fn + Backspace (Line 51)
            KEY_ID.FN_KEYBOARD_BACKSPACE: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_BACKSPACE', KDB_USAGE.KEYBOARD_DELETE_BACKSPACE),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_FORWARD', KDB_USAGE.KEYBOARD_DELETE_FORWARD),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_FORWARD', KDB_USAGE.KEYBOARD_DELETE_FORWARD),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_BACKSPACE', KDB_USAGE.KEYBOARD_DELETE_BACKSPACE)},
            # Fn + U (short press) (Line 52)
            KEY_ID.FN_KEYBOARD_U: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_U', KDB_USAGE.KEYBOARD_U_AND_U)},
            # Fn + O (short press) (Line 53)
            KEY_ID.FN_KEYBOARD_O: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_O', KDB_USAGE.KEYBOARD_O_AND_O)},
            # Fn + I (short press) (Line 54)
            KEY_ID.FN_KEYBOARD_I: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_I', KDB_USAGE.KEYBOARD_I_AND_I)},
            # Fn + C (short press) (Line 55)
            KEY_ID.FN_KEYBOARD_C: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_C', KDB_USAGE.KEYBOARD_C_AND_C)},
            # Fn + P (short press) (Line 56)
            KEY_ID.FN_KEYBOARD_P: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_P', KDB_USAGE.KEYBOARD_P_AND_P)},
            # Fn + Enter (Line 57)
            KEY_ID.FN_KEYBOARD_ENTER: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_RETURN_ENTER', KDB_USAGE.KEYBOARD_RETURN_ENTER),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER)},
            # Fn + B (Line 58)
            KEY_ID.FN_KEYBOARD_B: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAUSE', KDB_USAGE.KEYBOARD_PAUSE),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_B', KDB_USAGE.KEYBOARD_B_AND_B),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_B', KDB_USAGE.KEYBOARD_B_AND_B),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAUSE', KDB_USAGE.KEYBOARD_PAUSE)},
            # Fn + Left Arrow (Line 59)
            KEY_ID.FN_KEYBOARD_LEFT_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME)},
            # Fn + Right Arrow (Line 60)
            KEY_ID.FN_KEYBOARD_RIGHT_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END)},
            # Fn + Up Arrow (Line 61)
            KEY_ID.FN_KEYBOARD_UP_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAGE_UP', KDB_USAGE.KEYBOARD_PAGE_UP)},
            # Fn + Down Arrow (Line 62)
            KEY_ID.FN_KEYBOARD_DOWN_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAGE_DOWN', KDB_USAGE.KEYBOARD_PAGE_DOWN)},
            # The following Fn combination is defined on v2.4 but some products already implement it
            # Fn + Space (Line 70)
            KEY_ID.FN_KEYBOARD_SPACE_BAR: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1)},
            # Fn + R-Alt (Line 68)
            KEY_ID.FN_KEYBOARD_RIGHT_ALT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1)},
            # Fn + R-Ctrl (Line 69)
            KEY_ID.FN_KEYBOARD_RIGHT_CONTROL: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_CONTROL', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_CONTROL', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2)},
            # Fn + R-Ctrl / Option Right: R-option is printed on the same key as R-Ctrl (Line 69,78)
            KEY_ID.FN_KEYBOARD_RIGHT_CONTROL_OR_OPTION: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2)},

            # Easy Switch (Add on PWS v2.3 Line 87, but should support them since v2.0)
            # Easy Switch channel 1
            KEY_ID.HOST_1: {OS.ALL: _none_on_make_none_on_break()},
            # Easy Switch channel 2 (PWS v2.3 Line 88)
            KEY_ID.HOST_2: {OS.ALL: _none_on_make_none_on_break()},
            # Easy Switch channel 3 (PWS v2.3 Line 89)
            KEY_ID.HOST_3: {OS.ALL: _none_on_make_none_on_break()},

            # Not defined in guideline, but should support them for PWS KBD
            KEY_ID.SMILING_FACE_WITH_HEART_SHAPED_EYES: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.LOUDLY_CRYING_FACE: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.EMOJI_SMILEY: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.EMOJI_SMILEY_WITH_TEARS: {OS.ALL: _none_on_make_none_on_break()},
        }
    # end def _get_pws_kdb_guidelines_v2_0

    @classmethod
    def _get_pws_kdb_guidelines_v2_1(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.1.

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/edit#gid=856308430

        :return: The HID translation table for the Guidelines for Keyboard version 2.1.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_0(),
            # Mute microphone (Line 29)
            KEY_ID.MUTE_MICROPHONE: {
                OS.ALL: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.START_OR_STOP_MICROPHONE_CAPTURE)},
            # Refresh (Line 32)
            KEY_ID.REFRESH: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_R_AND_R]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_R_AND_R]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_R_AND_R]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_REFRESH)},
            # Open New Tab (Line 33)
            KEY_ID.OPEN_NEW_TAB: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_T_AND_T]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_T_AND_T]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_T_AND_T]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_NEW)},
            # Close Tab (Line 34)
            KEY_ID.CLOSE_TAB: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_W_AND_W]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_W_AND_W]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_W_AND_W]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_CLOSE)},
            # Print (panel) (Line 35)
            KEY_ID.PRINT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_P_AND_P]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_P_AND_P]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_P_AND_P]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_PRINT)},
            # OS Settings (Line 36)
            KEY_ID.OS_SETTINGS: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_I_AND_I]),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AL_CONTROL_PANEL)},
        }
    # end def _get_pws_kdb_guidelines_v2_1

    @classmethod
    def _get_pws_kdb_guidelines_v2_2(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.2

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/view#gid=1099061666

        :return: The HID translation table for the Guidelines for Keyboard version 2.2.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_1(),
        }
    # end def _get_pws_kdb_guidelines_v2_2

    @classmethod
    def _get_pws_kdb_guidelines_v2_3(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.3

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/view?gid=654322446#gid=654322446

        :return: The HID translation table for the Guidelines for Keyboard version 2.3.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_2(),
            # Do not Disturb (Line 28)
            KEY_ID.DO_NOT_DISTURB: {OS.WINDOWS: _none_on_make_none_on_break(),
                                    OS.MAC: _make_break(cls.HidSystemControlsReport, 'DO_NOT_DISTURB', cls.SET),
                                    OS.IPAD: _make_break(cls.HidSystemControlsReport, 'DO_NOT_DISTURB', cls.SET),
                                    OS.CHROME: _none_on_make_none_on_break()},
            # Fn + KP 0 i.e. Ins (Line 51)
            KEY_ID.FN_KEYPAD_0: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_INSERT', KDB_USAGE.KEYBOARD_INSERT),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _none_on_make_none_on_break()},
            # Num Lock / Clear (Line 54)
            KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_DELETE_FORWARD',
                                       KDB_USAGE.KEYBOARD_DELETE_FORWARD)},

        }
    # end def _get_pws_kdb_guidelines_v2_3

    @classmethod
    def _get_pws_kdb_guidelines_v2_4(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.4

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/edit#gid=1830877639

        :return: The HID translation table for the Guidelines for Keyboard version 2.4.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_3(),
            # Never used for NPI (e.g. NORMAN)
            # # Backlight Decrease
            # KEY_ID.BACKLIGHT_DOWN: {
            #     OS.ALL: _none_on_make_none_on_break(),
            #     OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.KBD_BACKLIGHT_DOWN)
            # },
            # # Backlight Increase
            # KEY_ID.BACKLIGHT_UP: {
            #     OS.ALL: _none_on_make_none_on_break(),
            #     OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.KBD_BACKLIGHT_UP)
            # },
            # Emoji (Overwrite definition in v2.0) (Line 26)
            KEY_ID.EMOJI_PANEL: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport,
                                        ['KEYBOARD_LEFT_SHIFT', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_LEFT_ALT',
                                         'KEYBOARD_LEFT_GUI', 'KEYBOARD_SPACE_BAR'],
                                        [cls.SET, cls.SET, cls.SET, cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.EMOJI_PICKER)},
        }
    # end def _get_pws_kdb_guidelines_v2_4

    @classmethod
    def _get_pws_kdb_guidelines_v2_5(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.5

        # cf https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/edit#gid=1830877639

        :return: The HID translation table for the Guidelines for Keyboard version 2.5.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_4(),
            # KataHira (Line 102) - Never implemented
            # KEY_ID.KATAHIRA: {
            #     OS.ALL: _make_break(
            #         cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2)},
        }
    # end def _get_pws_kdb_guidelines_v2_5

    @classmethod
    def _get_pws_kdb_guidelines_v2_6(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.6

        # cf https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/edit#gid=1276721922

        :return: The HID translation table for the Guidelines for Keyboard version 2.6.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_5(),
            # Mute microphone (Line 29)
            KEY_ID.MUTE_MICROPHONE: {
                OS.ALL: _none_on_make_none_on_break(),
                OS.CHROME_BLE_DIRECT: _make_break(cls.HidSystemControlsReport, 'MICROPHONE_MUTE', cls.SET),
                OS.CHROME:
                    _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.START_OR_STOP_MICROPHONE_CAPTURE)},
        }
    # end def _get_pws_kdb_guidelines_v2_6

    @classmethod
    def _get_pws_kdb_guidelines_v2_7(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.7

        https://docs.google.com/spreadsheets/d/1UUwbTajlxSR8fApVDQ1JU7nbJz0dHWp_iookALmZhZE/view#gid=1472794435

        :return: The HID translation table for the Guidelines for Keyboard version 2.7.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_6(),
            # Updated Chrome OS HID usage for Backlight Decrease / Increase to "No Key sent" (Line 6,7)
            KEY_ID.BACKLIGHT_DOWN: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.BACKLIGHT_UP: {OS.ALL: _none_on_make_none_on_break()},
            # Added new HID call mute for Windows 11 (Line 29)
            KEY_ID.MUTE_MICROPHONE: {
                OS.WINDOWS: _make_break(cls.HidCallStateManagementControlReport, 'CALL_MUTE_TOGGLE', cls.SET),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME:
                    _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.START_OR_STOP_MICROPHONE_CAPTURE),
                OS.CHROME_BLE_DIRECT: _make_break(cls.HidSystemControlsReport, 'MICROPHONE_MUTE', cls.SET)},
            # Updated Fn + Left/Right Arrow Fw key code for iPadOS (Line 64-67)
            KEY_ID.FN_KEYBOARD_LEFT_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_LEFT_ARROW'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW])},
            KEY_ID.FN_KEYBOARD_RIGHT_ARROW: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_RIGHT_ARROW'],
                    [cls.SET, KDB_USAGE.KEYBOARD_RIGHT_ARROW])},
        }
    # end def _get_pws_kdb_guidelines_v2_7

    @classmethod
    def _get_pws_kdb_guidelines_v2_8(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 2.8

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/view

        :return: The HID translation table for the Guidelines for Keyboard version 2.8.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_7(),
            # Fn + G (short press) / No key sent on long press (switch to Android) (Line 62)
            KEY_ID.FN_KEYBOARD_G: {
                OS.ALL: _make_break(cls.HidKeyboardReport, 'KEYBOARD_G', KDB_USAGE.KEYBOARD_G_AND_G)},
            # KataHira (Win/ChromeOS only) (Line 103)
            KEY_ID.KATAHIRA: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2)},
            # Globe Key (Mac only) (Line 90)
            KEY_ID.GLOBE_KEY: {
                OS.ALL: _none_on_make_none_on_break(),
                OS.MAC: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_NEXT_KEYBOARD_LAYOUT_SELECT),
                OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_NEXT_KEYBOARD_LAYOUT_SELECT)},
        }
    # end def _get_pws_kdb_guidelines_v2_8

    @classmethod
    def _get_pws_kdb_guidelines_v3_0(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 3.0

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/view?gid=317630667#gid=317630667

        :return: The HID translation table for the Guidelines for Keyboard version 3.0.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v2_8(),
            # Scroll Lock (Line 5)
            KEY_ID.KEYBOARD_SCROLL_LOCK: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_SCROLL_LOCK', KDB_USAGE.KEYBOARD_SCROLL_LOCK),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _none_on_make_none_on_break(),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_SCROLL_LOCK', KDB_USAGE.KEYBOARD_SCROLL_LOCK)},
            # Task View (Win) / Mission Control (Mac) (Line 8)
            KEY_ID.MISSION_CTRL_TASK_VIEW: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_TAB'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_TAB]),
                OS.MAC: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.OVERVIEW),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_TAB'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_TAB]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.OVERVIEW),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_ALT', 'KEYBOARD_TAB'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_TAB])},
            # App Switch/ Launchpad (Line 9)
            KEY_ID.APP_SWITCH_LAUNCHPAD: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_ALT', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_TAB], is_switch_key=True),
                OS.MAC: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_LAUNCHPAD),
                OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.MENU),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_DESKTOP_SHOW_ALL_APPLICATIONS),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Show Desktop (Line 10)
            KEY_ID.SHOW_DESKTOP: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_D'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_D_AND_D]),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_F11', KDB_USAGE.KEYBOARD_F11),
                OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.MENU),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_VIEW_TOGGLE),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Calculator (Line 19)
            KEY_ID.CALCULATOR: {
                OS.WINDOWS: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AL_CALCULATOR),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AL_CALCULATOR),
                OS.ANDROID: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AL_CALCULATOR),
                OS.BOOT: _none_on_make_none_on_break()},
            # Screen Capture (Line 20)
            KEY_ID.SCREEN_CAPTURE: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_SHIFT', 'KEYBOARD_S'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_S_AND_S]),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_SHIFT', 'KEYBOARD_4'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_4_AND_]),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_SHIFT', 'KEYBOARD_3'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_3_AND_]),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_PRINT_SCREEN', KDB_USAGE.KEYBOARD_PRINT_SCREEN),
                OS.ANDROID: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_PRINT_SCREEN', KDB_USAGE.KEYBOARD_PRINT_SCREEN)},
            # Contextual menu (Line 21)
            KEY_ID.CONTEXTUAL_MENU: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_MENU', KDB_USAGE.KEYBOARD_APPLICATION),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_MENU', KDB_USAGE.KEYBOARD_APPLICATION),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_MENU', KDB_USAGE.KEYBOARD_APPLICATION)},
            # Screen Lock (Line 22)
            KEY_ID.SCREEN_LOCK: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_L'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_L_AND_L]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_Q'],
                                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_Q_AND_Q]),
                OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.POWER),
                OS.CHROME: _make_break(
                    cls.HidSystemControlsReport, 'POWER_STATE', cls.HidSystemControlsReport.POSITION.SYSTEM_SLEEP),
                OS.ANDROID: _make_break(
                    cls.HidSystemControlsReport, 'POWER_STATE', cls.HidSystemControlsReport.POSITION.SYSTEM_SLEEP)},
            # Home (Line 24)
            KEY_ID.HOME: {OS.WINDOWS: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_HOME),
                          OS.MAC: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.OVERVIEW),
                          OS.IPAD: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.MENU),
                          OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_HOME),
                          OS.ANDROID: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_HOME),
                          OS.BOOT: _none_on_make_none_on_break()},
            # Back (Line 25)
            KEY_ID.MULTI_PLATF_BACK: {
                OS.WINDOWS: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_BACK),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_ARROW'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_ARROW'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_BACK),
                OS.ANDROID: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_BACK),
                OS.BOOT: _none_on_make_none_on_break()},
            # Emoji (Line 26)
            KEY_ID.EMOJI_PANEL: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_PERIOD_AND_MORE'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_PERIOD_AND_MORE]),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.EMOJI_PICKER),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET)},
            # Dictation (Line 27)
            KEY_ID.DICTATION: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_H'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_H_AND_H]),
                OS.MAC: _double_click(cls.HidKeyboardReport, 'KEYBOARD_LEFT_CONTROL', cls.SET),
                OS.IPAD: _double_click(cls.HidKeyboardReport, 'KEYBOARD_LEFT_CONTROL', cls.SET),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.VOICE_DICTATION),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Do not Disturb (Mac only) (Line 28)
            KEY_ID.DO_NOT_DISTURB: {OS.WINDOWS: _none_on_make_none_on_break(),
                                    OS.MAC: _make_break(cls.HidSystemControlsReport, 'DO_NOT_DISTURB', cls.SET),
                                    OS.IPAD: _make_break(cls.HidSystemControlsReport, 'DO_NOT_DISTURB', cls.SET),
                                    OS.CHROME: _none_on_make_none_on_break(),
                                    OS.ANDROID: _none_on_make_none_on_break()},
            # Mute microphone (Line 29)
            KEY_ID.MUTE_MICROPHONE: {
                OS.WINDOWS: _make_break(cls.HidCallStateManagementControlReport, 'CALL_MUTE_TOGGLE', cls.SET),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME:
                    _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.START_OR_STOP_MICROPHONE_CAPTURE),
                OS.CHROME_BLE_DIRECT: _make_break(cls.HidSystemControlsReport, 'MICROPHONE_MUTE', cls.SET),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Language switch (Line 30)
            KEY_ID.LANGUAGE_SWITCH: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_SPACE_BAR'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR], is_switch_key=True),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_SPACE_BAR'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_NEXT_KEYBOARD_LAYOUT_SELECT),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_GUI', 'KEYBOARD_SPACE_BAR'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_SPACE_BAR])},
            # Refresh (Line 32)
            KEY_ID.REFRESH: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_R_AND_R]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_R_AND_R]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_R_AND_R]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_REFRESH),
                OS.ANDROID: _none_on_make_none_on_break()
            },
            # Open New Tab (Line 33)
            KEY_ID.OPEN_NEW_TAB: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_T_AND_T]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_T_AND_T]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_T_AND_T]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_NEW),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Close Tab (Line 34)
            KEY_ID.CLOSE_TAB: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_W_AND_W]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_W_AND_W]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_W_AND_W]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_CLOSE),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Print (panel) (Line 35)
            KEY_ID.PRINT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_control', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_P_AND_P]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                    [cls.SET, KDB_USAGE.KEYBOARD_P_AND_P]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_P_AND_P]),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AC_PRINT),
                OS.ANDROID: _none_on_make_none_on_break()},
            # OS Settings (Line 36)
            KEY_ID.OS_SETTINGS: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ['keyboard_left_gui', 'key_code1'],
                                        [cls.SET, KDB_USAGE.KEYBOARD_I_AND_I]),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(cls.HidConsumerReport, 'key_1', CS_Usage.AL_CONTROL_PANEL),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Insert Key (Windows only) (Line 37)
            KEY_ID.KEYBOARD_INSERT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_INSERT', KDB_USAGE.KEYBOARD_INSERT),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _none_on_make_none_on_break(),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Home Key (text editing) (Line 39)
            KEY_ID.KEYBOARD_HOME: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_LEFT_ARROW'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW]),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME)},
            # End key (text editing) (Line 40)
            KEY_ID.KEYBOARD_END: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_RIGHT_ARROW'],
                    [cls.SET, KDB_USAGE.KEYBOARD_RIGHT_ARROW]),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END)},

            # Fn + KP 7 i.e. Home (Line 43)
            KEY_ID.FN_KEYPAD_7: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_LEFT_ARROW'],
                                     [cls.SET, KDB_USAGE.KEYBOARD_LEFT_ARROW]),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_HOME', KDB_USAGE.KEYBOARD_HOME)},
            # Fn + KP 1 i.e. End (Line 48)
            KEY_ID.FN_KEYPAD_1: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, ['KEYBOARD_LEFT_CONTROL', 'KEYBOARD_RIGHT_ARROW'],
                    [cls.SET, KDB_USAGE.KEYBOARD_RIGHT_ARROW]),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_END', KDB_USAGE.KEYBOARD_END)},
            # Fn + KP 0 i.e. Ins (Line 51)
            KEY_ID.FN_KEYPAD_0: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_INSERT', KDB_USAGE.KEYBOARD_INSERT),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _none_on_make_none_on_break(),
                OS.ANDROID: _none_on_make_none_on_break()},
            # Fn + KP Enter (Line 53)
            KEY_ID.FN_KEYPAD_ENTER: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYPAD_EQUAL', KDB_USAGE.KEYPAD_EQUAL),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYPAD_EQUAL', KDB_USAGE.KEYPAD_EQUAL),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER)},
            # Num Lock / Clear (Line 54)
            KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_FORWARD', KDB_USAGE.KEYBOARD_DELETE_FORWARD),
                OS.ANDROID: _make_break(
                    cls.HidKeyboardReport, 'KEYPAD_NUM_LOCK_AND_CLEAR', KDB_USAGE.KEYPAD_NUM_LOCK_AND_CLEAR)},
            # Fn + Backspace (Line 56)
            KEY_ID.FN_KEYBOARD_BACKSPACE: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_BACKSPACE', KDB_USAGE.KEYBOARD_DELETE_BACKSPACE),
                OS.MAC: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_FORWARD', KDB_USAGE.KEYBOARD_DELETE_FORWARD),
                OS.IPAD: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_FORWARD', KDB_USAGE.KEYBOARD_DELETE_FORWARD),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_BACKSPACE', KDB_USAGE.KEYBOARD_DELETE_BACKSPACE),
                OS.ANDROID: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_DELETE_BACKSPACE', KDB_USAGE.KEYBOARD_DELETE_BACKSPACE)},
            # Fn + Enter (Line 63)
            KEY_ID.FN_KEYBOARD_ENTER: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_RETURN_ENTER', KDB_USAGE.KEYBOARD_RETURN_ENTER),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYPAD_ENTER', KDB_USAGE.KEYPAD_ENTER)},
            # Fn + B (Pause/Break) (Line 64)
            KEY_ID.FN_KEYBOARD_B: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAUSE', KDB_USAGE.KEYBOARD_PAUSE),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_B', KDB_USAGE.KEYBOARD_B_AND_B),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_B', KDB_USAGE.KEYBOARD_B_AND_B),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAUSE', KDB_USAGE.KEYBOARD_PAUSE),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_PAUSE', KDB_USAGE.KEYBOARD_PAUSE)},
            # Fn + R-Alt (Line 69)
            KEY_ID.FN_KEYBOARD_RIGHT_ALT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1)},
            # Fn + R-Ctrl (Line 70)
            KEY_ID.FN_KEYBOARD_RIGHT_CONTROL: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_CONTROL', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_CONTROL', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2)},

            # Modifier keys
            # Windows Left (Win only) / Option Left (Mac only) (Line 74)
            KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET)},
            # Windows Right (Win only) / Option Right (Mac only) (Line 75)
            KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET)},
            # Alt Left (Win only) / Command Left (Mac only) (Line 77)
            KEY_ID.KEYBOARD_LEFT_ALT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_GUI', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LEFT_ALT', cls.SET)},
            # Alt Right (Win only) / Command Right (Mac only) (Line 78)
            KEY_ID.KEYBOARD_RIGHT_ALT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_GUI', cls.SET),
                OS.CHROME: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET),
                OS.ANDROID: _make_break(cls.HidKeyboardReport, 'KEYBOARD_RIGHT_ALT', cls.SET)},

            # Language input keys
            # Muhenkan (Win/ChromeOS only) (Line 99) + Alphanumeric (MAC only) (Line 102)
            KEY_ID.MUHENKAN: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL5', KDB_USAGE.KEYBOARD_INTERNATIONAL5),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG2', KDB_USAGE.KEYBOARD_LANG2),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL5', KDB_USAGE.KEYBOARD_INTERNATIONAL5),
                OS.ANDROID: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL5', KDB_USAGE.KEYBOARD_INTERNATIONAL5)},
            # Henkan (Win/ChromeOS only) + Kana (MAC only) (Line 100)
            KEY_ID.HENKAN: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL4', KDB_USAGE.KEYBOARD_INTERNATIONAL4),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL4', KDB_USAGE.KEYBOARD_INTERNATIONAL4),
                OS.ANDROID: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL4', KDB_USAGE.KEYBOARD_INTERNATIONAL4)},
            # KataHira (Win/ChromeOS only) (Line 101)
            KEY_ID.KATAHIRA: {
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2),
                OS.MAC: _none_on_make_none_on_break(),
                OS.IPAD: _none_on_make_none_on_break(),
                OS.CHROME: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2),
                OS.ANDROID: _make_break(
                    cls.HidKeyboardReport, 'KEYBOARD_INTERNATIONAL2', KDB_USAGE.KEYBOARD_INTERNATIONAL2)},
            # Kana (MAC only) (Line 103)
            KEY_ID.KANA: {
                OS.WINDOWS: _none_on_make_none_on_break(),
                OS.MAC: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.IPAD: _make_break(cls.HidKeyboardReport, 'KEYBOARD_LANG1', KDB_USAGE.KEYBOARD_LANG1),
                OS.CHROME: _none_on_make_none_on_break(),
                OS.ANDROID: _none_on_make_none_on_break()},
        }
    # end def _get_pws_kdb_guidelines_v3_0

    @classmethod
    def _get_pws_kdb_guidelines_v3_1(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 3.1

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/view?gid=1197940329#gid=1197940329

        :return: The HID translation table for the Guidelines for Keyboard version 3.1.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v3_0(),
            # Backlight Cycling (Line 13)
            KEY_ID.BACKLIGHT_CYCLING: {OS.ALL: _none_on_make_none_on_break()},
            # Action1-4 (Line 109-112)
            KEY_ID.SMART_ACTION_1: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.SMART_ACTION_2: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.SMART_ACTION_3: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.SMART_ACTION_4: {OS.ALL: _none_on_make_none_on_break()},
        }
    # end def _get_pws_kdb_guidelines_v3_1

    @classmethod
    def _get_pws_kbd_guidelines_v3_2(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 3.2

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/view?gid=1981019139#gid=1981019139

        :return: The HID translation table for the Guidelines for Keyboard version 3.2.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kdb_guidelines_v3_1(),
            # Home (Apple Sku) (Line 26)
            KEY_ID.HOME_APPLE_SKU: {
                OS.ALL: _none_on_make_none_on_break(),
                OS.MAC: _make_break(cls.HidKeyboardReport, "KEYBOARD_ESCAPE", KDB_USAGE.KEYBOARD_ESCAPE),
                OS.IPAD: _make_break(cls.HidConsumerReport, "key_1", CS_Usage.MENU)},
            # Forward Delete (Apple Sku) (Line 40)
            KEY_ID.FW_DELETE_APPLE_SKU: {
                OS.ALL: _none_on_make_none_on_break(),
                OS.MAC: _make_break(cls.HidKeyboardReport, "KEYBOARD_DELETE_FORWARD",
                                    KDB_USAGE.KEYBOARD_DELETE_FORWARD),
                OS.IPAD: _make_break(cls.HidConsumerReport, "KEYBOARD_DELETE_FORWARD",
                                     KDB_USAGE.KEYBOARD_DELETE_FORWARD)},
        }
    # end def _get_pws_kbd_guidelines_v3_2

    @classmethod
    def _get_pws_kbd_guidelines_v3_3(cls):
        """
        Generate the HID translation table based on the Guidelines for Keyboard version 3.3

        https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/view?gid=535275233#gid=535275233

        :return: The HID translation table for the Guidelines for Keyboard version 3.3.
        :rtype: ``dict``
        """
        return {
            **cls._get_pws_kbd_guidelines_v3_2(),
            # Co-Pilot Key (Windows only) (Line 60)
            KEY_ID.WINDOWS_COPILOT: {
                OS.ALL: _none_on_make_none_on_break(),
                OS.WINDOWS: _make_break(
                    cls.HidKeyboardReport, ["KEYBOARD_LEFT_GUI", "KEYBOARD_LEFT_SHIFT", "KEYBOARD_F23"],
                    [cls.SET, cls.SET, KDB_USAGE.KEYBOARD_F23])},
            # Cut Key (Line 61)
            KEY_ID.CUT: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_CONTROL", "KEYBOARD_X"],
                                        [cls.SET, KDB_USAGE.KEYBOARD_X_AND_X]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_GUI", "KEYBOARD_X"],
                                    [cls.SET, KDB_USAGE.KEYBOARD_X_AND_X]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_GUI", "KEYBOARD_X"],
                                     [cls.SET, KDB_USAGE.KEYBOARD_X_AND_X]),
                OS.CHROME: _make_break(cls.HidConsumerReport, "key_1", CS_Usage.AC_CUT),
                OS.ANDROID: _make_break(cls.HidConsumerReport, "key_1", CS_Usage.AC_CUT)},
            # Copy Key (Line 62)
            KEY_ID.COPY: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_CONTROL", "KEYBOARD_C"],
                                        [cls.SET, KDB_USAGE.KEYBOARD_C_AND_C]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_GUI", "KEYBOARD_C"],
                                    [cls.SET, KDB_USAGE.KEYBOARD_C_AND_C]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_GUI", "KEYBOARD_C"],
                                     [cls.SET, KDB_USAGE.KEYBOARD_C_AND_C]),
                OS.CHROME: _make_break(cls.HidConsumerReport, "key_1", CS_Usage.AC_COPY),
                OS.ANDROID: _make_break(cls.HidConsumerReport, "key_1", CS_Usage.AC_COPY)},
            # Paste Key (Line 63)
            KEY_ID.PASTE: {
                OS.WINDOWS: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_CONTROL", "KEYBOARD_V"],
                                        [cls.SET, KDB_USAGE.KEYBOARD_V_AND_V]),
                OS.MAC: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_GUI", "KEYBOARD_V"],
                                    [cls.SET, KDB_USAGE.KEYBOARD_V_AND_V]),
                OS.IPAD: _make_break(cls.HidKeyboardReport, ["KEYBOARD_LEFT_GUI", "KEYBOARD_V"],
                                     [cls.SET, KDB_USAGE.KEYBOARD_V_AND_V]),
                OS.CHROME: _make_break(cls.HidConsumerReport, "key_1", CS_Usage.AC_PASTE),
                OS.ANDROID: _make_break(cls.HidConsumerReport, "key_1", CS_Usage.AC_PASTE)}
        }
    # end def _get_pws_kbd_guidelines_v3_3

    @classmethod
    def _get_gaming_kdb_guidelines_v1_0(cls):
        """
        Generate the HID translation table based on the gaming keyboard guidelines version 1.0

        https://docs.google.com/spreadsheets/d/1rY01b28rLEhpvsTUykMTK9KN2khjRY9L_ZD1_6oyMpI/#gid=1472794435

        :return: The HID translation table based on the gaming keyboard guidelines version 1.0
        :rtype: ``dict``
        """
        return {
            # Bluetooth (Line 82)
            KEY_ID.BLE_CONNECTION: {OS.ALL: _none_on_make_none_on_break()},
            # Lightspeed/Bluetooth (Line 115)
            KEY_ID.LS2_BLE_CONNECTION_TOGGLE: {OS.ALL: _none_on_make_none_on_break()},
            # Dimming: Cycle backlight brightness level (Line 116)
            KEY_ID.DIMMING_KEY: {OS.ALL: _none_on_make_none_on_break()},
            # Game mode (Line 117)
            KEY_ID.GAME_MODE_KEY: {OS.ALL: _none_on_make_none_on_break()},
            # Roller0 scroll up (Line 118)
            KEY_ID.ROLLER0_SCROLL_UP: {OS.ALL: _none_on_make_none_on_break()},
            # Roller0 scroll down (Line 119)
            KEY_ID.ROLLER0_SCROLL_DOWN: {OS.ALL: _none_on_make_none_on_break()},
            # Roller1 scroll up (Line 120)
            KEY_ID.ROLLER1_SCROLL_UP: {OS.ALL: _none_on_make_none_on_break()},
            # Roller1 scroll down (Line 121)
            KEY_ID.ROLLER1_SCROLL_DOWN: {OS.ALL: _none_on_make_none_on_break()},
            # Lightspeed (Line 122)
            KEY_ID.LS2_CONNECTION: {OS.ALL: _none_on_make_none_on_break()},
            # Color animation(ANIM) (Line 127)
            KEY_ID.CYCLE_THROUGH_ANIMATION_EFFECTS: {OS.ALL: _none_on_make_none_on_break()},
            # Color cycle(RGB) (Line 128)
            KEY_ID.CYCLE_THROUGH_COLOR_EFFECT_SUB_SETTINGS: {OS.ALL: _none_on_make_none_on_break()},
            # FKC toggle (Line 129)
            KEY_ID.FKC_TOGGLE: {OS.ALL: _none_on_make_none_on_break()},
            # Onboard Memory Profile 1 (Line 130)
            KEY_ID.ONBOARD_PROFILE_1: {OS.ALL: _none_on_make_none_on_break()},
            # Onboard Memory Profile 2 (Line 131)
            KEY_ID.ONBOARD_PROFILE_2: {OS.ALL: _none_on_make_none_on_break()},
            # Onboard Memory Profile 3 (Line 132)
            KEY_ID.ONBOARD_PROFILE_3: {OS.ALL: _none_on_make_none_on_break()},
            # Onboard Memory Base Profile
            KEY_ID.ONBOARD_BASE_PROFILE: {OS.ALL: _none_on_make_none_on_break()},
            # Onboard Analog Adjustment: Actuation Point
            KEY_ID.ONBOARD_ACTUATION_MODE: {OS.ALL: _none_on_make_none_on_break()},
            # Onboard Analog Adjustment: Rapid Trigger
            KEY_ID.ONBOARD_RAPID_TRIGGER_MODE: {OS.ALL: _none_on_make_none_on_break()},
            # Only for 60% Pro Gaming Keyboard (Line 133)
            KEY_ID.BACKLIGHT_DOWN: {OS.ALL: _none_on_make_none_on_break()},
            # Only for 60% Pro Gaming Keyboard (Line 134)
            KEY_ID.BACKLIGHT_UP: {OS.ALL: _none_on_make_none_on_break()},

            # Not defined in guideline, but should support them for gaming KBD
            KEY_ID.NO_ACTION: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.TILT_LEFT: {
                OS.ALL: {
                    MAKE: {RESP_CLASS: (cls.HidMouseReport,), FIELDS_NAME: (('ac_pan',),), FIELDS_VALUE: ((255,),)},
                    BREAK: {RESP_CLASS: (), FIELDS_NAME: ((),), FIELDS_VALUE: ((),)}
                },
            },
            KEY_ID.TILT_RIGHT: {
                OS.ALL: {
                    MAKE: {RESP_CLASS: (cls.HidMouseReport,), FIELDS_NAME: (('ac_pan',),), FIELDS_VALUE: ((1,),)},
                    BREAK: {RESP_CLASS: (), FIELDS_NAME: ((),), FIELDS_VALUE: ((),)}
                },
            },
            KEY_ID.SELECT_NEXT_DPI: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.SELECT_PREV_DPI: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.CYCLE_THROUGH_DPI: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.DEFAULT_DPI: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.DPI_SHIFT: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.SELECT_NEXT_ONBOARD_PROFILE: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.SELECT_PREV_ONBOARD_PROFILE: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_SHIFT: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.BATTERY_LIFE_INDICATOR: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE: {OS.ALL: _none_on_make_none_on_break()},
        }
    # end def _get_gaming_kdb_guidelines_v1_0

    @classmethod
    def _get_gaming_kdb_guidelines_v1_1(cls):
        """
        Generate the HID translation table based on the gaming keyboard guidelines version 1.1(WIP)

        https://docs.google.com/spreadsheets/d/1zeTfQ59XFGfPNjrcDWluWbf4OJ7yrzHANXxM_X0PspE/#gid=1472794435

        :return: The HID translation table based on the gaming keyboard guidelines version 1.1
        :rtype: ``dict``
        """
        return {
            **cls._get_gaming_kdb_guidelines_v1_0(),
            # G-key #1-9 (Line 127-135)
            KEY_ID.G_1: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_2: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_3: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_4: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_5: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_6: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_7: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_8: {OS.ALL: _none_on_make_none_on_break()},
            KEY_ID.G_9: {OS.ALL: _none_on_make_none_on_break()},
        }
    # end def _get_gaming_kdb_guidelines_v1_1

    @staticmethod
    def get_not_single_action_keys(variant=None):
        """
        Retrieve the list of ``KEY_ID`` which do not trigger a single HID report on make and break.

        :param variant: OS detected by the firmware - OPTIONAL
        :type variant: ``str``

        :return: The list of keys that do not generate a single HID report on make and break.
        :rtype: ``list[KEY_ID]``
        """
        if HidData.NOT_SINGLE_ACTION_KEYS is not None:
            return HidData.NOT_SINGLE_ACTION_KEYS
        # end if

        keys = []
        for key_id in HidData.KEY_ID_TO_HID_MAP:
            if variant is not None:
                variant_iterator = [variant]
            else:
                variant_iterator = iter(HidData.KEY_ID_TO_HID_MAP[key_id])
            # end if
            for next_variant in variant_iterator:
                report_sequence = HidData.KEY_ID_TO_HID_MAP[key_id][next_variant]
                if len(report_sequence[MAKE][RESP_CLASS]) != 1 or \
                        len(report_sequence[BREAK][RESP_CLASS]) != 1:
                    keys.append(key_id)
                    # At least one variant contains an HID sequence that does not fit our need, break the loop for the
                    # current key_id here
                    break
                # end if
            # end for
        # end for
        HidData.NOT_SINGLE_ACTION_KEYS = keys

        return keys
    # end def get_not_single_action_keys

    @classmethod
    def collect_consumer_keys(cls):
        """
        Collect consumer keys from HidData.KEY_ID_TO_HID_MAP to initialize CONSUMER_KEYS class variable.

        The format of CONSUMER_KEYS dictionary: dict[KEY_ID, dict[OS, ConsumerHidUsage]]
        """
        consumer_keys = {}
        for key_id, hid_map in cls.KEY_ID_TO_HID_MAP.items():
            consumer_key_in_os = {}
            for os, expected_report in hid_map.items():
                response_class = expected_report[MAKE][RESP_CLASS]
                field_value = expected_report[MAKE][FIELDS_VALUE]
                if response_class and response_class[0] == HidConsumer:
                    consumer_key_in_os[os] = field_value[0][0]
                # end if
            # end for
            if consumer_key_in_os:
                consumer_keys[key_id] = consumer_key_in_os
            # end if
        # end for
        cls.CONSUMER_KEYS = consumer_keys
    # end def collect_consumer_keys
# end class HidData

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
