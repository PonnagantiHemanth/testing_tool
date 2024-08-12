#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.common.feature_19a1.errorhandling
:brief: VLP 1.0 ``ContextualDisplay`` errorhandling test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/12/14
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from math import ceil
from math import log
from os.path import join

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfo
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImagePayloadMixin
from pyhid.vlp.features.common.contextualdisplay import SetImageResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_wrong_range
from pysetup import TESTS_PATH
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.displayinfoutils import ButtonInfoConfig
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.vlp.base.contextualdisplayutils import ContextualDisplayTestUtils
from pytestbox.device.vlp.common.feature_19a1.contextualdisplay import ContextualDisplayTestCase
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ContextualDisplayErrorHandlingTestCase(ContextualDisplayTestCase):
    """
   Validate ``ContextualDisplay`` errorhandling test cases
   """

    @features("Feature19A1")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        Tests function index error range [4..0xF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_19a1.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            ContextualDisplayTestUtils.HIDppHelper.get_capabilities_and_check_error(
                test_case=self, function_index=function_index, error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_19A1_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature19A1")
    @level("ErrorHandling")
    def test_incorrect_device_index(self):
        """
        Verify incorrect device Index is not allowed.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over multiple interesting values between (display_index+1)..0xFF")
        # --------------------------------------------------------------------------------------------------------------
        for display_index in compute_wrong_range(value=list(range(self.config.F_DeviceScreenCount + 1)),
                                                  max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDisplayInfo request with a wrong display index:{display_index}")
            # ----------------------------------------------------------------------------------------------------------
            ContextualDisplayTestUtils.HIDppHelper.get_display_info_and_check_error(
                test_case=self, display_index=display_index, error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_19A1_0002", _AUTHOR)
    # end def test_incorrect_device_index

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.JPEG,))
    @level("ErrorHandling")
    def test_unsupported_image_resolution(self):
        """
        Verify Unsupported image resolution is not allowed
        """
        image_count = 1
        # Incorrect resolution greater than image display
        x_res = pow(2, ceil(log(int(self.config.DISPLAY_INFO_TABLE.F_HorizontalRes[0], 16), 2)))
        y_res = int(self.config.DISPLAY_INFO_TABLE.F_DisplayDimension[0], 16)
        with open(join(TESTS_PATH, "IMAGE_FILES", "incorrect_resolution.jpeg"), "rb") as f:
            image = f.read()
            image_payload = HexList(bytearray(image))
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send Set Image and validate response returns unsupported image resolution.")
        # --------------------------------------------------------------------------------------------------------------
        self.set_image_and_validate(result_code=SetImageResponse.UNSUPPORTED_IMAGE_RESOLUTION,
                                    image_count=image_count,
                                    x_res=x_res,
                                    y_res=y_res,
                                    image_format=ImageFormat.JPEG,
                                    image_payload=image_payload)

        self.testCaseChecked("ERR_19A1_0003", _AUTHOR)
    # end def test_unsupported_image_resolution

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @level("ErrorHandling")
    @bugtracker("VLPUnsupportedImageFormat")
    def test_unsupported_image_format(self):
        """
        Verify Unsupported image format is not allowed
        """
        image_count = 1
        with open(join(TESTS_PATH, "IMAGE_FILES", "image.jpg"), "rb") as f:
            image = f.read()
            image_payload = HexList(bytearray(image))
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send incorrect Image format and validate unsupported image format error.")
        # --------------------------------------------------------------------------------------------------------------
        self.set_image_and_validate(result_code=SetImageResponse.UNSUPPORTED_IMAGE_FORMAT,
                                    image_count=image_count,
                                    image_format=ImageFormat.RGB_888 + 1,
                                    image_payload=image_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send Set Image and validate response returns unsupported image format.")
        # --------------------------------------------------------------------------------------------------------------
        self.set_image_and_validate(result_code=SetImageResponse.UNSUPPORTED_IMAGE_FORMAT,
                                    image_count=image_count,
                                    image_format=ImageFormat.RGB_565,
                                    image_payload=image_payload)

        self.testCaseChecked("ERR_19A1_0004", _AUTHOR)
    # end def test_unsupported_image_format

    @features("BootloaderAvailable")
    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.RGB_565,))
    @level("ErrorHandling")
    def test_display_update_at_invalid_device_state(self):
        """
        Verify display update at invalid device state is not allowed
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send Enable DFU")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enter_dfu=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send Set Image and validate response returns unsupported device state")
        # --------------------------------------------------------------------------------------------------------------
        self.set_image_and_validate(x_res=int(self.config.DISPLAY_INFO_TABLE.F_DisplayDimension[0], 16),
                                    y_res=int(self.config.DISPLAY_INFO_TABLE.F_DisplayDimension[0], 16),
                                    image_format=ImageFormat.RGB_565,
                                    result_code=SetImageResponse.UNSUPPORTED_DEVICE_STATE)

        self.testCaseChecked("ERR_19A1_0008", _AUTHOR)
    # end def test_display_update_at_invalid_device_state

    @features("VLP")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.RGB_565,))
    @level("ErrorHandling")
    def test_image_size_invalid_argument_zero(self):
        """
        Verify incorrect image size is not allowed
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Send Set Image with an image and image size = 0 and check error response = INVALID_ARGUMENT.")
        # --------------------------------------------------------------------------------------------------------------
        image_count = 1
        image_payload = HexList('')
        self.set_image_and_validate(image_payload=image_payload,
                                    image_size=0,
                                    image_format=ImageFormat.RGB_565,
                                    image_count=image_count,
                                    error_code=ErrorCodes.INVALID_ARGUMENT,
                                    ack=True)

        self.testCaseChecked("ERR_19A1_0009#1", _AUTHOR)
    # end def test_image_size_invalid_argument_zero

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.RGB_565,))
    @level("ErrorHandling")
    def test_image_size_invalid_argument(self):
        """
        Verify incorrect image size is not allowed
        """
        image_count = 1
        # Number of bytes available per request
        image_bytes_per_req = 4090
        image_bytes_first_req = 4075

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Send Set Image with an image and image size = 0 and check error response = INVALID_ARGUMENT.")
        # --------------------------------------------------------------------------------------------------------------
        image_payload = HexList('')
        self.set_image_and_validate(image_payload=image_payload,
                                    image_size=0,
                                    image_format=ImageFormat.RGB_565,
                                    image_count=image_count,
                                    error_code=ErrorCodes.INVALID_ARGUMENT,
                                    ack=True)

        for no_of_reqs in (1, 2, 10, 30):
            min_img_data_size = max(image_bytes_first_req + (no_of_reqs - 2) * image_bytes_per_req + 1, 0)
            max_img_data_size = image_bytes_first_req + (no_of_reqs - 1) * image_bytes_per_req
            mid_img_data_size = min_img_data_size + (max_img_data_size - min_img_data_size) // 2

            for img_data_size in (min_img_data_size, mid_img_data_size, max_img_data_size):
                image_payload = HexList(self.color_code[ImageFormat.RGB_565] * (img_data_size // 2))
                img_size = image_bytes_first_req + (no_of_reqs - 1) * image_bytes_per_req
                assert no_of_reqs == 1 + max(0, ceil((len(image_payload) - image_bytes_first_req) / image_bytes_per_req))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send Set Image with {len(image_payload)} bytes of image data "
                                         f"(i.e. {no_of_reqs} VLP requests) and invalid parameter image size value "
                                         f"(= {img_size + 1}) to get Invalid Argument error response")
                # ------------------------------------------------------------------------------------------------------
                self.set_image_and_validate(image_payload=image_payload,
                                            image_size=img_size + 1,
                                            image_format=ImageFormat.RGB_565,
                                            image_count=image_count,
                                            error_code=ErrorCodes.INVALID_ARGUMENT,
                                            ack=True)
            # end for
        # end for

        self.testCaseChecked("ERR_19A1_0009#2", _AUTHOR)
    # end def test_image_size_invalid_argument

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.RGB_565,))
    @level("ErrorHandling")
    def test_image_data_gt_buffer_out_of_memory(self):
        """
        Verify image data exceeding total buffer size is not allowed
        """
        image_count = 1
        image_payload = HexList('FF' * (self.f.PRODUCT.FEATURES.VLP.F_TransferBufferSize + 1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           "Send multi packet transfer using SetImage where the total ImagePayload > buffer Size")
        # --------------------------------------------------------------------------------------------------------------
        button_info = ButtonInfoConfig.from_index(
            self.f, 0, self.config_manager).button_info_payload

        image = ContextualDisplay.Image(image_format=ImageFormat.RGB_565,
                                        image_location_x=button_info.button_location_x,
                                        image_location_y=button_info.button_location_y,
                                        image_location_width=button_info.button_location_width,
                                        image_location_height=button_info.button_location_height,
                                        image_size=len(image_payload),
                                        image_data=image_payload)

        full_payload = HexList(SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                                    defer_display_update=0,
                                                    image_count=image_count,
                                                    images=[image]))
        VlpProtocolTestUtils.VlpHelper.vlp_transfer(
            test_case=self,
            payload=full_payload,
            report_payload_size=self.report_payload_size,
            report_type=self.feature_19a1.set_image_cls,
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_19a1_index,
            ack=False,
            start_seqn=0)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Error Codes Out of Memory (13) returned by the device')
        # ----------------------------------------------------------------------------------------------------------
        error_message = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR,
                                              class_type=ErrorCodes)

        self.assertEqual(expected=ErrorCodes.OUT_OF_MEMORY,
                         obtained=error_message.errorCode,
                         msg=f'The received error code {error_message.errorCode} '
                             f'do not match the expected one {ErrorCodes.OUT_OF_MEMORY}!')

        self.testCaseChecked("ERR_19A1_0010", _AUTHOR)
    # end def test_image_data_gt_buffer_out_of_memory

    @features("Feature19A1")
    @level("ErrorHandling")
    def test_unsupported_device_state(self):
        """
        Verify non SW supported device state returns invalid ERROR from setDeviceState
        """
        unsupported_device_states = [x for x in ContextualDisplay.DEVICE_STATES 
                                     if HexList(x) not in HexList(self.config.F_SetDeviceStates)]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over device states which are non SW invocable.")
        # --------------------------------------------------------------------------------------------------------------
        for device_state in unsupported_device_states:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, "Send SetDeviceState with selected state and Check Error Response = INVALID_ARGUMENT")
            # ----------------------------------------------------------------------------------------------------------
            ContextualDisplayTestUtils.HIDppHelper.set_device_state_and_check_error(
                test_case=self,
                device_state=HexList(device_state),
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_19A1_0011", _AUTHOR)
    # end def test_unsupported_device_state
# end class ContextualDisplayErrorHandlingTestCase
