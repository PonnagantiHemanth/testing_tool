#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.base.contextualdisplayutils
:brief: Helpers for ``ContextualDisplay`` feature
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/11/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import time

# noinspection PyUnresolvedReferences
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hid.interfacedescriptors import VlpInterfaceDescriptor
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.vlp.features.common.contextualdisplay import ButtonEvent
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfo
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfoResponsePayloadMixin
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplayFactory
from pyhid.vlp.features.common.contextualdisplay import DeviceStateEvent
from pyhid.vlp.features.common.contextualdisplay import GetCapabilitiesResponse
from pyhid.vlp.features.common.contextualdisplay import GetConfigResponse
from pyhid.vlp.features.common.contextualdisplay import GetDeviceStateResponse
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfoResponse
from pyhid.vlp.features.common.contextualdisplay import GetSupportedDeviceStatesResponse
from pyhid.vlp.features.common.contextualdisplay import SetConfigResponse
from pyhid.vlp.features.common.contextualdisplay import SetDeviceStateResponse
from pyhid.vlp.features.common.contextualdisplay import SetImagePayloadMixin
from pyhid.vlp.features.common.contextualdisplay import SetImageResponse
from pyhid.vlp.vlpmessage import VlpMessage
from pyhid.vlp.vlpmessage import VlpMessageRawPayload
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.displayinfoutils import ButtonInfoConfig, DisplayInfoConfig
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ContextualDisplayTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ContextualDisplay`` feature
    """

    @staticmethod
    def _get_multi_packet_set_image_payload(test_case, image_format, img_count=1, display_index=1,
                                            defer_display_update=True):
        """
        Get full data to send VLP multi-packet transfer

        :param img_count: Number of images
        :type img_count: ``int``
        :param image_format: Format of image
        :type image_format: ``int``
        :param display_index: Index of Display to be updated
        :type display_index: ``int``
        :param defer_display_update: Flag to defer Display update
        :type defer_display_update: ``int | bool``

        :return: Full VLP multi-packet payload
        :rtype: ``HexList``
        """
        button_info = ButtonInfoConfig.from_index(
            test_case.f, 0, test_case.config_manager).button_info_payload
        display_info = DisplayInfoConfig.from_index(
            test_case.f, display_index - 1, test_case.config_manager).display_info_payload
        img_width = to_int(button_info.button_location_width)
        img_height = to_int(button_info.button_location_height)

        # Images positions
        x_y_img = []
        for button_index in range(to_int(display_info.button_count)):
            button_info = ButtonInfoConfig.from_index(
                test_case.f, button_index, test_case.config_manager).button_info_payload
            x_y_img.append((button_info.button_location_x, button_info.button_location_y))
        # end for

        images = [ContextualDisplay.Image(image_format=image_format,
                                          image_location_x=x_y_img[image_index][0],
                                          image_location_y=x_y_img[image_index][1],
                                          image_location_width=img_width,
                                          image_location_height=img_height,
                                          image_size=len(test_case.img),
                                          image_data=test_case.img)
                  for image_index in range(img_count)
                  ]

        set_image_payload = SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                                 defer_display_update=defer_display_update,
                                                 image_count=img_count,
                                                 images=images)
        return HexList(set_image_payload)
    # end def _get_multi_packet_set_image_payload

    class DeviceCapabilitiesChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``DeviceCapabilities``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version in [cls.Version.ZERO]:
                return {
                    "deferrable_display_update_capability": (cls.check_deferrable_display_update_capability,
                                                             int(config.F_CapabilitiesFlags[0])),
                    "rgb_565": (cls.check_rgb_565, int(config.F_CapabilitiesFlags[1])),
                    "rgb_888": (cls.check_rgb_888, int(config.F_CapabilitiesFlags[2])),
                    "jpeg": (cls.check_jpeg, int(config.F_CapabilitiesFlags[3])),
                    "calibrated": (cls.check_calibrated, int(config.F_CapabilitiesFlags[4])),
                    "origin": (cls.check_origin, int(config.F_CapabilitiesFlags[5])),
                    "reserved": (cls.check_reserved, 0)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_deferrable_display_update_capability(test_case, bitmap, expected):
            """
            Check deferrable_display_update_capability field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: DeviceCapabilities to check
            :type bitmap: ``ContextualDisplay.DeviceCapabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert deferrable_display_update_capability that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The deferrable_display_update_capability shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.deferrable_display_update_capability),
                msg="The deferrable_display_update_capability parameter differs from the one expected")
        # end def check_deferrable_display_update_capability

        @staticmethod
        def check_rgb_565(test_case, bitmap, expected):
            """
            Check rgb_565 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: DeviceCapabilities to check
            :type bitmap: ``ContextualDisplay.DeviceCapabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert rgb_565 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The rgb_565 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.rgb_565),
                msg="The rgb_565 parameter differs from the one expected")
        # end def check_rgb_565

        @staticmethod
        def check_rgb_888(test_case, bitmap, expected):
            """
            Check rgb_888 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: DeviceCapabilities to check
            :type bitmap: ``ContextualDisplay.DeviceCapabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert rgb_888 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The rgb_888 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.rgb_888),
                msg="The rgb_888 parameter differs from the one expected")
        # end def check_rgb_888

        @staticmethod
        def check_jpeg(test_case, bitmap, expected):
            """
            Check jpeg field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: DeviceCapabilities to check
            :type bitmap: ``ContextualDisplay.DeviceCapabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert jpeg that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The jpeg shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.jpeg),
                msg="The jpeg parameter differs from the one expected")
        # end def check_jpeg

        @staticmethod
        def check_calibrated(test_case, bitmap, expected):
            """
            Check calibrated field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: DeviceCapabilities to check
            :type bitmap: ``ContextualDisplay.DeviceCapabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert calibrated that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The calibrated shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.calibrated),
                msg="The calibrated parameter differs from the one expected")
        # end def check_calibrated

        @staticmethod
        def check_origin(test_case, bitmap, expected):
            """
            Check origin field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: DeviceCapabilities to check
            :type bitmap: ``ContextualDisplay.DeviceCapabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert origin that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The origin shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.origin),
                msg="The origin parameter differs from the one expected")
        # end def check_origin

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check origin field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: DeviceCapabilities to check
            :type bitmap: ``ContextualDisplay.DeviceCapabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert origin that raise an exception
            """
            test_case.assertNotNone(
                expected, msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg=f"The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved
    # end class DeviceCapabilitiesChecker

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ZERO:
                return {
                    "device_screen_count": (cls.check_device_screen_count, HexList(config.F_DeviceScreenCount)),
                    "max_image_size": (cls.check_max_image_size, HexList(config.F_MaxImageSize)),
                    "max_image_fps": (cls.check_max_image_fps, HexList(config.F_MaxImageFPS)),
                    "device_capabilities": (
                        cls.check_device_capabilities,
                        ContextualDisplayTestUtils.DeviceCapabilitiesChecker.get_default_check_map(test_case)),
                    "reserved": (cls.check_reserved, 0)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_device_screen_count(test_case, response, expected):
            """
            Check device_screen_count field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert device_screen_count that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The device_screen_count shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.device_screen_count),
                msg="The device_screen_count parameter differs from the one expected")
        # end def check_device_screen_count

        @staticmethod
        def check_max_image_size(test_case, response, expected):
            """
            Check max_image_size field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_image_size that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The max_image_size shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=Numeral(expected),
                obtained=Numeral(response.max_image_size),
                msg="The max_image_size parameter differs from the one expected")
        # end def check_max_image_size

        @staticmethod
        def check_max_image_fps(test_case, response, expected):
            """
            Check max_image_fps field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_image_fps that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The max_image_fps shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.max_image_fps),
                msg="The max_image_fps parameter differs from the one expected")
        # end def check_max_image_fps

        @staticmethod
        def check_device_capabilities(test_case, message, expected):
            """
            Check ``device_capabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetCapabilitiesResponse to check
            :type message: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ContextualDisplayTestUtils.DeviceCapabilitiesChecker.check_fields(
                test_case, message.device_capabilities, ContextualDisplay.DeviceCapabilities, expected)
        # end def check_device_capabilities

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class GetCapabilitiesResponseChecker

    class ButtonInfoChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ButtonInfo``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ZERO:
                return {
                    "button_shape": (cls.check_button_shape, None),
                    "button_location_x": (cls.check_button_location_x, None),
                    "button_location_y": (cls.check_button_location_y, None),
                    "button_location_width": (cls.check_button_location_width, None),
                    "button_location_height": (cls.check_button_location_height, None)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_button_shape(test_case, bitmap, expected):
            """
            Check button_shape field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonInfo to check
            :type bitmap: ``ContextualDisplay.ButtonInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert button_shape that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The button_shape shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.button_shape),
                msg="The button_shape parameter differs from the one expected")
        # end def check_button_shape

        @staticmethod
        def check_button_location_x(test_case, bitmap, expected):
            """
            Check button_location_x field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonInfo to check
            :type bitmap: ``ContextualDisplay.ButtonInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert button_location_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The button_location_x shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.button_location_x),
                msg="The button_location_x parameter differs from the one expected")
        # end def check_button_location_x

        @staticmethod
        def check_button_location_y(test_case, bitmap, expected):
            """
            Check button_location_y field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonInfo to check
            :type bitmap: ``ContextualDisplay.ButtonInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert button_location_y that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The button_location_y shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.button_location_y),
                msg="The button_location_y parameter differs from the one expected")
        # end def check_button_location_y

        @staticmethod
        def check_button_location_width(test_case, bitmap, expected):
            """
            Check button_location_width field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonInfo to check
            :type bitmap: ``ContextualDisplay.ButtonInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert button_location_width that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The button_location_width shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.button_location_width),
                msg="The button_location_width parameter differs from the one expected")
        # end def check_button_location_width

        @staticmethod
        def check_button_location_height(test_case, bitmap, expected):
            """
            Check button_location_height field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonInfo to check
            :type bitmap: ``ContextualDisplay.ButtonInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert button_location_height that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The button_location_height shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.button_location_height),
                msg="The button_location_height parameter differs from the one expected")
        # end def check_button_location_height
    # end class ButtonInfoChecker

    class VisibleAreaInfoChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``VisibleAreaInfo``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ZERO:
                return {
                    "visible_area_shape": (cls.check_visible_area_shape, None),
                    "visible_area_location_x": (cls.check_visible_area_location_x, None),
                    "visible_area_location_y": (cls.check_visible_area_location_y, None),
                    "visible_area_width": (cls.check_visible_area_width, None),
                    "visible_area_height": (cls.check_visible_area_height, None)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_visible_area_shape(test_case, bitmap, expected):
            """
            Check visible_area_shape field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: VisibleAreaInfo to check
            :type bitmap: ``ContextualDisplay.VisibleAreaInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert visible_area_shape that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The visible_area_shape shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.visible_area_shape),
                msg="The visible_area_shape parameter differs from the one expected")
        # end def check_visible_area_shape

        @staticmethod
        def check_visible_area_location_x(test_case, bitmap, expected):
            """
            Check visible_area_location_x field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: VisibleAreaInfo to check
            :type bitmap: ``ContextualDisplay.VisibleAreaInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert visible_area_location_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The visible_area_location_x shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.visible_area_location_x),
                msg="The visible_area_location_x parameter differs from the one expected")
        # end def check_visible_area_location_x

        @staticmethod
        def check_visible_area_location_y(test_case, bitmap, expected):
            """
            Check visible_area_location_y field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: VisibleAreaInfo to check
            :type bitmap: ``ContextualDisplay.VisibleAreaInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert visible_area_location_y that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The visible_area_location_y shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.visible_area_location_y),
                msg="The visible_area_location_y parameter differs from the one expected")
        # end def check_visible_area_location_y

        @staticmethod
        def check_visible_area_width(test_case, bitmap, expected):
            """
            Check visible_area_width field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: VisibleAreaInfo to check
            :type bitmap: ``ContextualDisplay.VisibleAreaInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert visible_area_width that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The visible_area_width shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.visible_area_width),
                msg="The visible_area_width parameter differs from the one expected")
        # end def check_visible_area_width

        @staticmethod
        def check_visible_area_height(test_case, bitmap, expected):
            """
            Check visible_area_height field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: VisibleAreaInfo to check
            :type bitmap: ``ContextualDisplay.VisibleAreaInfo``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert visible_area_height that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The visible_area_height shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.visible_area_height),
                msg="The visible_area_height parameter differs from the one expected")
        # end def check_visible_area_height
    # end class VisibleAreaInfoChecker

    class GetDisplayInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetDisplayInfoResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ZERO:
                return {
                    "display_shape": (cls.check_display_shape, None),
                    "display_dimension": (cls.check_display_dimension, None),
                    "horizontal_resolution": (cls.check_horizontal_resolution, None),
                    "vertical_resolution": (cls.check_vertical_resolution, None),
                    "button_count": (cls.check_button_count, None),
                    "visible_area_count": (cls.check_visible_area_count, None),
                    "button_info": (
                        cls.check_button_info,
                        ContextualDisplayTestUtils.ButtonInfoChecker.get_default_check_map(test_case)),
                    "visible_area_info": (
                        cls.check_visible_area_info,
                        ContextualDisplayTestUtils.VisibleAreaInfoChecker.get_default_check_map(test_case))
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_display_shape(test_case, response, expected):
            """
            Check display_shape field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetDisplayInfoResponse to check
            :type response: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert display_shape that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The display_shape shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.display_shape),
                msg="The display_shape parameter differs from the one expected")
        # end def check_display_shape

        @staticmethod
        def check_display_dimension(test_case, response, expected):
            """
            Check display_dimension field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetDisplayInfoResponse to check
            :type response: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert display_dimension that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The display_dimension shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.display_dimension),
                msg="The display_dimension parameter differs from the one expected")
        # end def check_display_dimension

        @staticmethod
        def check_horizontal_resolution(test_case, response, expected):
            """
            Check horizontal_resolution field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetDisplayInfoResponse to check
            :type response: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert horizontal_resolution that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The horizontal_resolution shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.horizontal_resolution),
                msg="The horizontal_resolution parameter differs from the one expected")
        # end def check_horizontal_resolution

        @staticmethod
        def check_vertical_resolution(test_case, response, expected):
            """
            Check vertical_resolution field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetDisplayInfoResponse to check
            :type response: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert vertical_resolution that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The vertical_resolution shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.vertical_resolution),
                msg="The vertical_resolution parameter differs from the one expected")
        # end def check_vertical_resolution

        @staticmethod
        def check_button_count(test_case, response, expected):
            """
            Check button_count field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetDisplayInfoResponse to check
            :type response: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert button_count that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The button_count shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.button_count),
                msg="The button_count parameter differs from the one expected")
        # end def check_button_count

        @staticmethod
        def check_visible_area_count(test_case, response, expected):
            """
            Check visible_area_count field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetDisplayInfoResponse to check
            :type response: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert visible_area_count that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The visible_area_count shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.visible_area_count),
                msg="The visible_area_count parameter differs from the one expected")
        # end def check_visible_area_count

        @staticmethod
        def check_button_info(test_case, message, expected):
            """
            Check ``button_info``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetDisplayInfoResponse to check
            :type message: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``ContextualDisplay.ButtonInfo|dict``
            """
            field_name = expected.pop("field_name")
            ContextualDisplayTestUtils.ButtonInfoChecker.check_fields(
                test_case, message.__getattr__(field_name), ContextualDisplay.ButtonInfo, expected)
        # end def check_button_info

        @staticmethod
        def check_visible_area_info(test_case, message, expected):
            """
            Check ``visible_area_info``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetDisplayInfoResponse to check
            :type message: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``ContextualDisplay.VisibleAreaInfo|dict``
            """
            field_name = expected.pop("field_name")
            ContextualDisplayTestUtils.VisibleAreaInfoChecker.check_fields(
                test_case, message.__getattr__(field_name), ContextualDisplay.VisibleAreaInfo, expected)
        # end def check_visible_area_info
    # end class GetDisplayInfoResponseChecker

    class SetImageResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetImageResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ZERO:
                return {
                    "result_code": (cls.check_result_code, 0),
                    "count": (cls.check_count, 0)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_result_code(test_case, response, expected):
            """
            Check result_code field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetImageResponse to check
            :type response: ``SetImageResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert result_code that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The result_code shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.result_code),
                msg="The result_code parameter differs from the one expected")
        # end def check_result_code

        @staticmethod
        def check_count(test_case, response, expected):
            """
            Check count field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetImageResponse to check
            :type response: ``SetImageResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert count that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The count shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.count),
                msg="The count parameter differs from the one expected")
        # end def check_count
    # end class SetImageResponseChecker

    class GenericDeviceStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define reusable helper class to be used for several messages in this feature
            - GetSupportedDeviceStatesResponse
            - SetDeviceStateResponse
            - GetDeviceStateResponse
            - DeviceStateEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ZERO:
                return {
                    "device_state": (cls.check_device_state, config.F_DefaultDeviceState)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_device_state(test_case, response, expected):
            """
            Check device_state field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetDeviceStateResponse to check
            :type response: ``SetDeviceStateResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert device_state that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The device_state shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.device_state),
                msg="The device_state parameter differs from the one expected")
        # end def check_device_state
    # end class GenericDeviceStateResponseChecker

    class GetSupportedDeviceStatesResponseChecker(GenericDeviceStateResponseChecker):
        """
        Define Helper to check ``GetSupportedDeviceStatesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ZERO:
                return {}
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_device_state_info(test_case, message, expected):
            """
            Check ``button_info``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetDisplayInfoResponse to check
            :type message: ``GetDisplayInfoResponse``
            :param expected: Expected value
            :type expected: ``ContextualDisplay.DeviceStateInfo|dict``
            """
            field_name = expected.pop("field_name")
            ContextualDisplayTestUtils.GenericDeviceStateResponseChecker.check_fields(
                test_case, message.__getattr__(field_name), ContextualDisplay.DeviceStateInfo, expected)
        # end def check_device_state_info
    # end class GetSupportedDeviceStatesResponseChecker

    class GetDeviceStateResponseChecker(GenericDeviceStateResponseChecker):
        """
        Define Helper to check ``GetDeviceStateResponse``
        """
    # end class GetDeviceStateResponseChecker

    class SetDeviceStateResponseChecker(GenericDeviceStateResponseChecker):
        """
        Define Helper to check ``SetDeviceStateResponse``
        """
    # end class SetDeviceStateResponseChecker

    class SetConfigResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetConfigResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "device_adopted": (cls.check_device_adopted, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_device_adopted(test_case, message, expected):
            """
            Check ``device_adopted``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetConfigResponse to check
            :type message: ``GetConfigResponse``
            :param expected: Expected value
            :type expected: ``bool | int``
            """
            test_case.assertNotNone(
                expected, msg="device_adopted shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(message.device_adopted),
                msg=f"The device_adopted parameter differs "
                    f"(expected:{expected}, obtained:{message.device_adopted})")
        # end def check_device_adopted

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check origin field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GetConfigResponse to check
            :type bitmap: ``GetConfigResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert origin that raise an exception
            """
            test_case.assertNotNone(
                expected, msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg=f"The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved
    # end class SetConfigResponseChecker

    class GetConfigResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetConfigResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "device_adopted": (cls.check_device_adopted, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_device_adopted(test_case, message, expected):
            """
            Check ``device_adopted``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetConfigResponse to check
            :type message: ``GetConfigResponse``
            :param expected: Expected value
            :type expected: ``bool | int``
            """
            test_case.assertNotNone(
                expected, msg="device_adopted shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(message.device_adopted),
                msg=f"The device_adopted parameter differs "
                    f"(expected:{expected}, obtained:{message.device_adopted})")
        # end def check_device_adopted

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check origin field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: GetConfigResponse to check
            :type bitmap: ``GetConfigResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert origin that raise an exception
            """
            test_case.assertNotNone(
                expected, msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg=f"The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved
    # end class GetConfigResponseChecker

    class ButtonEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ButtonEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ONE:
                return {
                    "display_index": (cls.check_display_index, config.F_DeviceScreenCount),
                    "button_index": (cls.check_button_index, config.BUTTON_TABLE.F_ButtonIndex[0])
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_display_index(test_case, event, expected):
            """
            Check display_index field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: ButtonEvent to check
            :type event: ``ButtonEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert display_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The display_index shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(event.display_index),
                msg="The display_index parameter differs from the one expected")
        # end def check_display_index

        @staticmethod
        def check_button_index(test_case, event, expected):
            """
            Check button_index field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: ButtonEvent to check
            :type event: ``ButtonEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert button_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The button_index shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(event.button_index),
                msg="The button_index parameter differs from the one expected")
        # end def check_button_index
    # end class ButtonEventChecker

    class DeviceStateEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``DeviceStateEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ONE:
                return {
                    "device_state": (cls.check_device_state, config.F_DefaultDeviceState)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_device_state(test_case, event, expected):
            """
            Check device_state field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: DeviceStateEvent to check
            :type event: ``DeviceStateEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert device_state that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The device_state shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(event.device_state),
                msg="The device_state parameter differs from the one expected")
        # end def check_device_state
    # end class DeviceStateEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_vlp_parameters(cls, test_case,
                           feature_id=ContextualDisplay.FEATURE_ID,
                           factory=ContextualDisplayFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_vlp_parameters``
            return super().get_vlp_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_vlp_parameters

        @staticmethod
        def parse_multi_packet_payload(vlp_messages, payload_parsing_class):
            """
            Get parsed payload of VLP multi-packet transfer

            :param vlp_messages: VLP messages
            :type vlp_messages: ``list[VlpMessageRawPayload]``
            :param payload_parsing_class: Class to parse the full payload
            :type payload_parsing_class: ``BitFieldContainerMixin``

            :return: Parsed payload
            :rtype: ``BitFieldContainerMixin``
            """
            payload = HexList()
            for vlp_message in vlp_messages:
                payload += vlp_message.payload
            # end for
            return payload_parsing_class.fromHexList(payload)
        # end def parse_multi_packet_payload

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None,
                             vlp_reserved=0, vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0, report_id=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: GetCapabilitiesResponse (if not error)
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                response_class_type=feature_19a1.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_capabilities_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None,
                vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def get_display_info(cls, test_case, display_index=None, device_index=None, port_index=None, software_id=None,
                             vlp_reserved=0, vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0, report_id=None):
            """
            Process ``GetDisplayInfo``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param display_index: Display Index - OPTIONAL
            :type display_index: ``int | HexList | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: GetDisplayInfoResponse (if not error)
            :rtype: ``GetDisplayInfoResponse``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_display_info_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                display_index=HexList(display_index),
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if
            response = VlpProtocolTestUtils.VlpHelper.send(
                test_case=test_case, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                response_class_type=feature_19a1.get_display_info_response_cls)
            return ContextualDisplayTestUtils.HIDppHelper.parse_multi_packet_payload(
                response, GetDisplayInfoResponsePayloadMixin)
        # end def get_display_info

        @classmethod
        def get_display_info_and_check_error(
                cls, test_case, error_codes, display_index=None, function_index=None, device_index=None,
                port_index=None, vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0):
            """
            Process ``GetDisplayInfo``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param display_index: Display Index - OPTIONAL
            :type display_index: ``int | HexList | None``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_display_info_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                display_index=HexList(display_index),
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_display_info_and_check_error

        @classmethod
        def get_supported_device_states(cls, test_case, device_index=None, port_index=None, software_id=None,
                                        vlp_reserved=0, vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0,
                                        report_id=None):
            """
            Process ``GetSupportedDeviceStates``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: GetSupportedDeviceStatesResponse (if not error)
            :rtype: ``GetSupportedDeviceStatesResponse``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_supported_device_states_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                response_class_type=feature_19a1.get_supported_device_states_response_cls)
        # end def get_supported_device_states

        @classmethod
        def get_supported_device_states_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None,
                vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0):
            """
            Process ``GetSupportedDeviceStates``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_supported_device_states_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_supported_device_states_and_check_error

        @classmethod
        def set_device_state(cls, test_case, device_state=None, device_index=None, port_index=None, software_id=None,
                             vlp_reserved=0, vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0, report_id=None):
            """
            Process ``SetDeviceState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_state: Device State - OPTIONAL
            :type device_state: ``HexList | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: SetDeviceStateResponse (if not error)
            :rtype: ``SetDeviceStateResponse``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.set_device_state_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                device_state=device_state,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                response_class_type=feature_19a1.set_device_state_response_cls)
        # end def set_device_state

        @classmethod
        def set_device_state_and_check_error(
                cls, test_case, error_codes, device_state=None, function_index=None, device_index=None, port_index=None,
                vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0):
            """
            Process ``SetDeviceState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param device_state: Device State - OPTIONAL
            :type device_state: ``HexList | None``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.set_device_state_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                device_state=device_state,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_device_state_and_check_error

        @classmethod
        def get_device_state(cls, test_case, device_index=None, port_index=None, software_id=None,
                             vlp_reserved=0, vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0, report_id=None):
            """
            Process ``GetDeviceState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: GetDeviceStateResponse (if not error)
            :rtype: ``GetDeviceStateResponse``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_device_state_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                response_class_type=feature_19a1.get_device_state_response_cls)
        # end def get_device_state

        @classmethod
        def get_device_state_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None,
                vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0):
            """
            Process ``GetDeviceState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_device_state_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_device_state_and_check_error

        @classmethod
        def set_config(cls, test_case, device_adopted, device_index=None, port_index=None, software_id=None,
                       vlp_reserved=0, vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0, report_id=None,
                       reserved=None):
            """
            Process ``SetConfig``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_adopted: Device Adopted
            :type device_adopted: ``bool | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: SetConfigResponse (if not error)
            :rtype: ``SetConfigResponse``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.set_config_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                device_adopted=device_adopted,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if reserved is not None:
                report.reserved = reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                response_class_type=feature_19a1.set_config_response_cls)
        # end def set_config

        @classmethod
        def set_config_and_check_error(
                cls, test_case, error_codes, device_adopted, function_index=None, device_index=None, port_index=None,
                vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0):
            """
            Process ``SetConfig``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param device_adopted: Device Adopted
            :type device_adopted: ``bool | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.set_config_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                device_adopted=device_adopted,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_config_and_check_error

        @classmethod
        def get_config(cls, test_case, device_index=None, port_index=None, software_id=None,
                       vlp_reserved=0, vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0, report_id=None):
            """
            Process ``GetConfig``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: GetConfigResponse (if not error)
            :rtype: ``GetConfigResponse``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_config_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                response_class_type=feature_19a1.get_config_response_cls)
        # end def get_config

        @classmethod
        def get_config_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None,
                vlp_begin=1, vlp_end=1, vlp_ack=1, vlp_sequence_number=0):
            """
            Process ``GetConfig``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            """
            feature_19a1_index, feature_19a1, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19a1.get_config_cls(
                device_index=device_index,
                feature_index=feature_19a1_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_config_and_check_error

        @classmethod
        def button_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=False, allow_no_message=False, skip_error_message=False):
            """
            Process ``ButtonEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: ButtonEvent
            :rtype: ``ButtonEvent``
            """
            _, feature_19a1, _, _ = cls.get_vlp_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.VLP_EVENT,
                class_type=feature_19a1.button_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def button_event

        @classmethod
        def device_state_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=False, allow_no_message=False, skip_error_message=False, get_internal_event=False):
            """
            Process ``DeviceStateEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``
            :param get_internal_event: Flag to allow internal Device state events catching mechanism - OPTIONAL
            :type get_internal_event: ``bool``

            :return: DeviceStateEvent
            :rtype: ``DeviceStateEvent``
            """
            expected_event = False
            event_response = None
            remaining_time = 5
            _, feature_19a1, _, _ = cls.get_vlp_parameters(test_case)

            start_time = time()
            while not expected_event and remaining_time > 0:
                event_response = ChannelUtils.get_only(
                    test_case=test_case,
                    queue_name=HIDDispatcher.QueueName.VLP_EVENT,
                    class_type=feature_19a1.device_state_event_cls,
                    timeout=timeout,
                    check_first_message=check_first_message,
                    allow_no_message=allow_no_message,
                    skip_error_message=skip_error_message)
                expected_event = True if get_internal_event else \
                    int(Numeral(event_response.device_state)) not in \
                    ContextualDisplay().DeviceState.INTERNAL_EVENT_LIST
                # end if
                remaining_time = remaining_time - (time() - start_time)
            # end while
            return event_response
        # end def device_state_event
    # end class HIDppHelper
# end class ContextualDisplayTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
