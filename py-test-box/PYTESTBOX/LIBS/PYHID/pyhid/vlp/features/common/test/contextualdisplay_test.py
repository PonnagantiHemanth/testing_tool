#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.vlp.features.common.test.contextualdisplay_test
:brief: VLP 1.0 ``ContextualDisplay`` test module
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/11/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.vlp.features.common.contextualdisplay import ButtonEvent
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplayFactory
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplayV0
from pyhid.vlp.features.common.contextualdisplay import DeviceStateEvent
from pyhid.vlp.features.common.contextualdisplay import GetCapabilities
from pyhid.vlp.features.common.contextualdisplay import GetCapabilitiesResponse
from pyhid.vlp.features.common.contextualdisplay import GetConfig
from pyhid.vlp.features.common.contextualdisplay import GetConfigResponse
from pyhid.vlp.features.common.contextualdisplay import GetDeviceState
from pyhid.vlp.features.common.contextualdisplay import GetDeviceStateResponse
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfo
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfoResponse
from pyhid.vlp.features.common.contextualdisplay import GetSupportedDeviceStates
from pyhid.vlp.features.common.contextualdisplay import GetSupportedDeviceStatesResponse
from pyhid.vlp.features.common.contextualdisplay import SetConfig
from pyhid.vlp.features.common.contextualdisplay import SetConfigResponse
from pyhid.vlp.features.common.contextualdisplay import SetDeviceState
from pyhid.vlp.features.common.contextualdisplay import SetDeviceStateResponse
from pyhid.vlp.features.common.contextualdisplay import SetImage
from pyhid.vlp.features.common.contextualdisplay import SetImageResponse
from pyhid.vlp.features.test.vlp_root_test import VLPRootTestCase
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ContextualDisplayInstantiationTestCase(TestCase):
    """
    Test ``ContextualDisplay`` testing classes instantiations
    """

    @staticmethod
    def test_contextual_display():
        """
        Test ``ContextualDisplay`` class instantiation
        """
        my_class = ContextualDisplay(device_index=0, feature_index=0)

        VLPRootTestCase._top_level_class_checker(my_class)

        my_class = ContextualDisplay(device_index=0xFF, feature_index=0xFF)

        VLPRootTestCase._top_level_class_checker(my_class)
    # end def test_contextual_display

    @staticmethod
    def test_get_capabilities():
        """
        Test ``GetCapabilities`` class instantiation
        """
        my_class = GetCapabilities(device_index=0, feature_index=0)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetCapabilities(device_index=0xFF, feature_index=0xFF)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_display_info():
        """
        Test ``GetDisplayInfo`` class instantiation
        """
        my_class = GetDisplayInfo(device_index=0, feature_index=0,
                                  display_index=0)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetDisplayInfo(device_index=0xFF, feature_index=0xFF,
                                  display_index=0xFF)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_display_info

    @staticmethod
    def test_set_image():
        """
        Test ``SetImage`` class instantiation
        """
        my_class = SetImage(device_index=0, feature_index=0,
                            vlp_payload=HexList("00" * 4094))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = SetImage(device_index=0xFF, feature_index=0xFF,
                            vlp_payload=HexList("FF" * 4094),)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_set_image

    @staticmethod
    def test_get_supported_device_states():
        """
        Test ``GetSupportedDeviceStates`` class instantiation
        """
        my_class = GetSupportedDeviceStates(device_index=0, feature_index=0)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetSupportedDeviceStates(device_index=0xFF, feature_index=0xFF)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_supported_device_states

    @staticmethod
    def test_set_device_state():
        """
        Test ``SetDeviceState`` class instantiation
        """
        my_class = SetDeviceState(device_index=0, feature_index=0,
                                  device_state=HexList(0))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = SetDeviceState(device_index=0xFF, feature_index=0xFF,
                                  device_state=HexList("FF" * (SetDeviceState.LEN.DEVICE_STATE // 8)))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_set_device_state

    @staticmethod
    def test_get_device_state():
        """
        Test ``GetDeviceState`` class instantiation
        """
        my_class = GetDeviceState(device_index=0, feature_index=0)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetDeviceState(device_index=0xFF, feature_index=0xFF)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_device_state

    @staticmethod
    def test_set_config():
        """
        Test ``SetConfig`` class instantiation
        """
        my_class = SetConfig(device_index=0, feature_index=0,
                             device_adopted=False)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = SetConfig(device_index=0xFF, feature_index=0xFF,
                             device_adopted=True)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_set_config

    @staticmethod
    def test_get_config():
        """
        Test ``GetConfig`` class instantiation
        """
        my_class = GetConfig(device_index=0, feature_index=0)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetConfig(device_index=0xFF, feature_index=0xFF)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_config

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           device_screen_count=0,
                                           max_image_size=HexList(Numeral(0,2)),
                                           max_image_fps=HexList(0),
                                           deferrable_display_update_capability=False,
                                           rgb_565=False,
                                           rgb_888=False,
                                           jpeg=False,
                                           calibrated=False,
                                           origin=False)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           device_screen_count=0xFF,
                                           max_image_size=HexList("FF" * (GetCapabilitiesResponse.LEN.MAX_IMAGE_SIZE // 8)),
                                           max_image_fps=HexList("FF" * (GetCapabilitiesResponse.LEN.MAX_IMAGE_FPS // 8)),
                                           deferrable_display_update_capability=True,
                                           rgb_565=True,
                                           rgb_888=True,
                                           jpeg=True,
                                           calibrated=True,
                                           origin=True)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_display_info_response():
        """
        Test ``GetDisplayInfoResponse`` class instantiation
        """
        my_class = GetDisplayInfoResponse(device_index=0, feature_index=0, vlp_payload=HexList("00"))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetDisplayInfoResponse(device_index=0xFF, feature_index=0xFF, vlp_payload=HexList("FF"))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_display_info_response

    @staticmethod
    def test_set_image_response():
        """
        Test ``SetImageResponse`` class instantiation
        """
        my_class = SetImageResponse(device_index=0, feature_index=0,
                                    result_code=HexList(0),
                                    count=HexList(0))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = SetImageResponse(device_index=0xFF, feature_index=0xFF,
                                    result_code=HexList("FF" * (SetImageResponse.LEN.RESULT_CODE // 8)),
                                    count=HexList("FF" * (SetImageResponse.LEN.COUNT // 8)))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_set_image_response

    @staticmethod
    def test_get_supported_device_states_response():
        """
        Test ``GetSupportedDeviceStatesResponse`` class instantiation
        """
        my_class = GetSupportedDeviceStatesResponse(device_index=0, feature_index=0,
                                                      device_state=HexList(0))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetSupportedDeviceStatesResponse(
            device_index=0xFF, feature_index=0xFF,
            device_state=HexList("FFFF"))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_supported_device_states_response

    @staticmethod
    def test_set_device_state_response():
        """
        Test ``SetDeviceStateResponse`` class instantiation
        """
        my_class = SetDeviceStateResponse(device_index=0, feature_index=0,
                                          device_state=HexList(0))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = SetDeviceStateResponse(device_index=0xFF, feature_index=0xFF,
                                          device_state=HexList("FF" * (SetDeviceStateResponse.LEN.DEVICE_STATE // 8)))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_set_device_state_response

    @staticmethod
    def test_get_device_state_response():
        """
        Test ``GetDeviceStateResponse`` class instantiation
        """
        my_class = GetDeviceStateResponse(device_index=0, feature_index=0,
                                          device_state=HexList(0))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetDeviceStateResponse(device_index=0xFF, feature_index=0xFF,
                                          device_state=HexList("FF" * (GetDeviceStateResponse.LEN.DEVICE_STATE // 8)))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_device_state_response

    @staticmethod
    def test_set_config_response():
        """
        Test ``SetConfigResponse`` class instantiation
        """
        my_class = SetConfigResponse(device_index=0, feature_index=0,
                                     device_adopted=False)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = SetConfigResponse(device_index=0xFF, feature_index=0xFF,
                                     device_adopted=True)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_set_config_response

    @staticmethod
    def test_get_config_response():
        """
        Test ``GetConfigResponse`` class instantiation
        """
        my_class = GetConfigResponse(device_index=0, feature_index=0,
                                     device_adopted=False)

        VLPRootTestCase._function_class_checker(my_class)

        my_class = GetConfigResponse(device_index=0xFF, feature_index=0xFF,
                                     device_adopted=True)

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_get_config_response

    @staticmethod
    def test_button_event():
        """
        Test ``ButtonEvent`` class instantiation
        """
        my_class = ButtonEvent(device_index=0, feature_index=0,
                               display_index=HexList(0),
                               button_index=HexList(0))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = ButtonEvent(device_index=0xFF, feature_index=0xFF,
                               display_index=HexList("FF" * (
                                       ContextualDisplay.ButtonEventInfo.LEN.DISPLAY_INDEX // 8)),
                               button_index=HexList("FF" * (
                                       ContextualDisplay.ButtonEventInfo.LEN.BUTTON_INDEX // 8)))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_button_event

    @staticmethod
    def test_device_state_event():
        """
        Test ``DeviceStateEvent`` class instantiation
        """
        my_class = DeviceStateEvent(device_index=0, feature_index=0,
                                    device_state=HexList(0))

        VLPRootTestCase._function_class_checker(my_class)

        my_class = DeviceStateEvent(device_index=0xFF, feature_index=0xFF,
                                    device_state=HexList("FF" * (DeviceStateEvent.LEN.DEVICE_STATE // 8)))

        VLPRootTestCase._function_class_checker(my_class)
    # end def test_device_state_event
# end class ContextualDisplayInstantiationTestCase


class ContextualDisplayTestCase(TestCase):
    """
    Test ``ContextualDisplay`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ContextualDisplayV0.VERSION: {
                "cls": ContextualDisplayV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_display_info_cls": GetDisplayInfo,
                    "get_display_info_response_cls": GetDisplayInfoResponse,
                    "set_image_cls": SetImage,
                    "set_image_response_cls": SetImageResponse,
                    "get_supported_device_states_cls": GetSupportedDeviceStates,
                    "get_supported_device_states_response_cls": GetSupportedDeviceStatesResponse,
                    "set_device_state_cls": SetDeviceState,
                    "set_device_state_response_cls": SetDeviceStateResponse,
                    "get_device_state_cls": GetDeviceState,
                    "get_device_state_response_cls": GetDeviceStateResponse,
                    "set_config_cls": SetConfig,
                    "set_config_response_cls": SetConfigResponse,
                    "get_config_cls": GetConfig,
                    "get_config_response_cls": GetConfigResponse,
                    "button_event_cls": ButtonEvent,
                    "device_state_event_cls": DeviceStateEvent,
                },
                "max_function_index": 7
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ContextualDisplayFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ContextualDisplayFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ContextualDisplayFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                ContextualDisplayFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ContextualDisplayFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ContextualDisplayFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(obj, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(obj, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check ``get_max_function_index`` returns correct value at each version

        :raise ``AssertionError``: Assert max_function_index that raise an exception
        """
        for version, expected in self.expected.items():
            obj = ContextualDisplayFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ContextualDisplayTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
