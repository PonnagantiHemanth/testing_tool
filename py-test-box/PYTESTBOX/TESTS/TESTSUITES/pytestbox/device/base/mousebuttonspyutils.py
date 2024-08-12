#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.mousebuttonspyutils
:brief: Helpers for ``MouseButtonSpy`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.gaming.mousebuttonspy import MouseButtonSpy
from pyhid.hidpp.features.gaming.mousebuttonspy import MouseButtonSpyFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MouseButtonSpyTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers for common checks on ``MouseButtonSpy`` feature
    """
    class GetNbOfButtonsResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``GetNbOfButtons`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetNbOfButtonsResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "nb_buttons": (cls.check_nb_buttons, test_case.f.PRODUCT.FEATURES.GAMING.MOUSE_BUTTON_SPY.F_NbButtons)
            }
        # end def get_default_check_map

        @staticmethod
        def check_nb_buttons(test_case, response, expected):
            """
            Check nb_buttons field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetNbOfButtonsResponse to check
            :type response: ``GetNbOfButtonsResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.nb_buttons)),
                msg=f"The nb_buttons parameter differs "
                    f"(expected:{expected}, obtained:{response.nb_buttons})")
        # end def check_nb_buttons
    # end class GetNbOfButtonsResponseChecker

    class GetRemappingResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``GetRemapping`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetRemappingResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            default_button_mapping = [0] * 16
            for button_index in range(test_case.f.PRODUCT.FEATURES.GAMING.MOUSE_BUTTON_SPY.F_NbButtons):
                default_button_mapping[button_index] = button_index + 1
            # end for
            return {
                "button_1": (cls.check_button_1, default_button_mapping[0]),
                "button_2": (cls.check_button_2, default_button_mapping[1]),
                "button_3": (cls.check_button_3, default_button_mapping[2]),
                "button_4": (cls.check_button_4, default_button_mapping[3]),
                "button_5": (cls.check_button_5, default_button_mapping[4]),
                "button_6": (cls.check_button_6, default_button_mapping[5]),
                "button_7": (cls.check_button_7, default_button_mapping[6]),
                "button_8": (cls.check_button_8, default_button_mapping[7]),
                "button_9": (cls.check_button_9, default_button_mapping[8]),
                "button_10": (cls.check_button_10, default_button_mapping[9]),
                "button_11": (cls.check_button_11, default_button_mapping[10]),
                "button_12": (cls.check_button_12, default_button_mapping[11]),
                "button_13": (cls.check_button_13, default_button_mapping[12]),
                "button_14": (cls.check_button_14, default_button_mapping[13]),
                "button_15": (cls.check_button_15, default_button_mapping[14]),
                "button_16": (cls.check_button_16, default_button_mapping[15])
            }
        # end def get_default_check_map

        @staticmethod
        def check_button_1(test_case, response, expected):
            """
            Check button_1 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_1)),
                msg=f"The button_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_1})")
        # end def check_button_1

        @staticmethod
        def check_button_2(test_case, response, expected):
            """
            Check button_2 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_2)),
                msg=f"The button_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_2})")
        # end def check_button_2

        @staticmethod
        def check_button_3(test_case, response, expected):
            """
            Check button_3 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_3)),
                msg=f"The button_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_3})")
        # end def check_button_3

        @staticmethod
        def check_button_4(test_case, response, expected):
            """
            Check button_4 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_4)),
                msg=f"The button_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_4})")
        # end def check_button_4

        @staticmethod
        def check_button_5(test_case, response, expected):
            """
            Check button_5 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_5)),
                msg=f"The button_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_5})")
        # end def check_button_5

        @staticmethod
        def check_button_6(test_case, response, expected):
            """
            Check button_6 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_6)),
                msg=f"The button_6 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_6})")
        # end def check_button_6

        @staticmethod
        def check_button_7(test_case, response, expected):
            """
            Check button_7 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_7)),
                msg=f"The button_7 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_7})")
        # end def check_button_7

        @staticmethod
        def check_button_8(test_case, response, expected):
            """
            Check button_8 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_8)),
                msg=f"The button_8 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_8})")
        # end def check_button_8

        @staticmethod
        def check_button_9(test_case, response, expected):
            """
            Check button_9 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_9)),
                msg=f"The button_9 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_9})")
        # end def check_button_9

        @staticmethod
        def check_button_10(test_case, response, expected):
            """
            Check button_10 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_10)),
                msg=f"The button_10 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_10})")
        # end def check_button_10

        @staticmethod
        def check_button_11(test_case, response, expected):
            """
            Check button_11 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_11)),
                msg=f"The button_11 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_11})")
        # end def check_button_11

        @staticmethod
        def check_button_12(test_case, response, expected):
            """
            Check button_12 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_12)),
                msg=f"The button_12 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_12})")
        # end def check_button_12

        @staticmethod
        def check_button_13(test_case, response, expected):
            """
            Check button_13 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_13)),
                msg=f"The button_13 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_13})")
        # end def check_button_13

        @staticmethod
        def check_button_14(test_case, response, expected):
            """
            Check button_14 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_14)),
                msg=f"The button_14 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_14})")
        # end def check_button_14

        @staticmethod
        def check_button_15(test_case, response, expected):
            """
            Check button_15 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_15)),
                msg=f"The button_15 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_15})")
        # end def check_button_15

        @staticmethod
        def check_button_16(test_case, response, expected):
            """
            Check button_16 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetRemappingResponse to check
            :type response: ``GetRemappingResponse``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.button_16)),
                msg=f"The button_16 parameter differs "
                    f"(expected:{expected}, obtained:{response.button_16})")
        # end def check_button_16
    # end class GetRemappingResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=MouseButtonSpy.FEATURE_ID, factory=MouseButtonSpyFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_nb_of_buttons(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetNbOfButtons``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetNbOfButtonsResponse
            :rtype: ``GetNbOfButtonsResponse``
            """
            feature_8110_index, feature_8110, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8110.get_nb_of_buttons_cls(
                device_index, feature_8110_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8110.get_nb_of_buttons_response_cls)
            return response
        # end def get_nb_of_buttons

        @classmethod
        def start_spy(cls, test_case, device_index=None, port_index=None):
            """
            Process ``StartSpy``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: StartSpyResponse
            :rtype: ``StartSpyResponse``
            """
            feature_8110_index, feature_8110, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8110.start_spy_cls(
                device_index, feature_8110_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8110.start_spy_response_cls)
            return response
        # end def start_spy

        @classmethod
        def stop_spy(cls, test_case, device_index=None, port_index=None):
            """
            Process ``StopSpy``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: StopSpyResponse
            :rtype: ``StopSpyResponse``
            """
            feature_8110_index, feature_8110, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8110.stop_spy_cls(
                device_index, feature_8110_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8110.stop_spy_response_cls)
            return response
        # end def stop_spy

        @classmethod
        def get_remapping(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetRemapping``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetRemappingResponse
            :rtype: ``GetRemappingResponse``
            """
            feature_8110_index, feature_8110, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8110.get_remapping_cls(
                device_index, feature_8110_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8110.get_remapping_response_cls)
            return response
        # end def get_remapping

        @classmethod
        def set_remapping(cls, test_case, button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10, button_11, button_12, button_13, button_14, button_15, button_16, device_index=None, port_index=None):
            """
            Process ``SetRemapping``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
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
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRemappingResponse
            :rtype: ``SetRemappingResponse``
            """
            feature_8110_index, feature_8110, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8110.set_remapping_cls(
                device_index, feature_8110_index,
                button_1=HexList(button_1),
                button_2=HexList(button_2),
                button_3=HexList(button_3),
                button_4=HexList(button_4),
                button_5=HexList(button_5),
                button_6=HexList(button_6),
                button_7=HexList(button_7),
                button_8=HexList(button_8),
                button_9=HexList(button_9),
                button_10=HexList(button_10),
                button_11=HexList(button_11),
                button_12=HexList(button_12),
                button_13=HexList(button_13),
                button_14=HexList(button_14),
                button_15=HexList(button_15),
                button_16=HexList(button_16))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8110.set_remapping_response_cls)
            return response
        # end def set_remapping

        @classmethod
        def button_event(cls, test_case):
            """
            Process ``ButtonEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: ButtonEvent
            :rtype: ``ButtonEvent``
            """
            return test_case.getMessage(queue=test_case.hidDispatcher.event_message_queue,
                                        class_type=test_case.feature_8110.button_event_cls)
        # end def button_event
    # end class HIDppHelper
# end class MouseButtonSpyTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
