#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.common.feature_0021
:brief: Validates HID common feature 0x0021
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/10/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel

from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.util import compute_wrong_range
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pyhid.hidpp.features.common.uniqueidentifier32bytes import UniqueIdentifier32Bytes
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte0To15
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte0To15Response
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte16To31
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte16To31Response
from pyhid.hidpp.features.common.uniqueidentifier32bytes import RegenId
from pyhid.hidpp.features.common.uniqueidentifier32bytes import RegenIdResponse
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.common.changehost import ChangeHost
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ApplicationUniqueIdentifier32BytesTestCase(BaseTestCase):
    """
    Validates 32 Bytes Unique Identifier TestCases
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x0021)')
        # ---------------------------------------------------------------------------
        self.feature_index = self.updateFeatureMapping(feature_id=UniqueIdentifier32Bytes.FEATURE_ID)
    # end def setUp

    @features('Feature0021')
    @level('Interface')
    def test_GetByte0To15API(self):
        """
        GetByte first Part API validation

        [0] getByte0_15() -> uniqueId[0..15]
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send getByte0_15 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for getByte0_15 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
        # If an error occurred it will be received instead of the response and raise an exception
        self.send_report_wait_response(report=get_byte_0_to_15,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=GetByte0To15Response)

        self.testCaseChecked("FNT_0021_0001")
    # end def test_GetByte0To15API

    @features('Feature0021')
    @level('Interface')
    def test_GetByte16To31API(self):
        """
        GetByte second Part API validation

        [1] getByte16_31() -> uniqueId[16..31]
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send getByte16_31 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for getByte16_31 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
        self.send_report_wait_response(report=get_byte_16_t_31,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=GetByte16To31Response)

        self.testCaseChecked("FNT_0021_0002")
    # end def test_GetByte16To31API

    @features('Feature0021')
    @level('Interface')
    def test_RegenIdAPI(self):
        """
        regenId API validation

        [2] regenId()
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send regenId request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check no error response')
        # ---------------------------------------------------------------------------
        regen_id = RegenId(device_index=self.deviceIndex, feature_index=self.feature_index)
        self.send_report_wait_response(report=regen_id,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=RegenIdResponse)

        self.testCaseChecked("FNT_0021_0003")
    # end def test_RegenIdAPI

    @features('Feature0021')
    @level('Business', 'SmokeTests')
    def test_GetUniqueIdentifierBusinessCase(self):
        """
        Business Case: generate a random number, get the first part then get the second part
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send regenId request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check no error response')
        # ---------------------------------------------------------------------------
        regen_id = RegenId(device_index=self.deviceIndex, feature_index=self.feature_index)
        self.send_report_wait_response(report=regen_id,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=RegenIdResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send getByte0_15 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for getByte0_15 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
        self.send_report_wait_response(report=get_byte_0_to_15,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=GetByte0To15Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send getByte16_31 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Wait for getByte16_31 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
        self.send_report_wait_response(report=get_byte_16_t_31,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=GetByte16To31Response)

        self.testCaseChecked("FNT_0021_0004")
    # end def test_GetUniqueIdentifierBusinessCase

    @features('Feature0021')
    @level('Functionality')
    def test_MultipleRegenId(self):
        """
        Calling multiple times 'regen' without getting the number thru 'getByte0_15' or 'getByte16_31' shall not
        raise any issue.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop 3 times')
        # ---------------------------------------------------------------------------
        for _ in range(3):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send regenId request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            regen_id = RegenId(device_index=self.deviceIndex, feature_index=self.feature_index)
            self.send_report_wait_response(report=regen_id,
                                           response_queue=self.hidDispatcher.common_message_queue,
                                           response_class_type=RegenIdResponse)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_0021_0008")
    # end def test_MultipleRegenId

    @features('Feature0021')
    @level('Security')
    def test_MultipleRegenIdNotSameGetByte0To15(self):
        """
        Randomness of uniqueId[0..15]: interleave calls to regenId and getByte0_15 to check new random identifier is
        generated every time. Test 10 tries at least and verify each byte is changed.
        """

        unique_identifiers = [[]] * 10

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop 10 times')
        # ---------------------------------------------------------------------------
        for i in range(len(unique_identifiers)):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send regenId request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            regen_id = RegenId(device_index=self.deviceIndex, feature_index=self.feature_index)
            self.send_report_wait_response(report=regen_id,
                                           response_queue=self.hidDispatcher.common_message_queue,
                                           response_class_type=RegenIdResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send getByte0_15 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for getByte0_15 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_0_to_15_response = self.send_report_wait_response(
                report=get_byte_0_to_15,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetByte0To15Response)

            unique_identifiers[i] = get_byte_0_to_15_response.bytes_0_to_15

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Compare the new uniqueId with the previous one (at least 1 out of the 16 '
                           'bytes shall be different)')
            # ---------------------------------------------------------------------------
            if i > 0:
                self.assertNotEqual(obtained=unique_identifiers[i],
                                    unexpected=unique_identifiers[i - 1],
                                    msg="The unique identifier is the same as the previous one")
            # end if
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Compare the 10 received numbers and validate each byte value had changed at '
                       'least once.')
        # ---------------------------------------------------------------------------
        results = [False] * 16
        for z in range(len(results)):
            for i in range(len(unique_identifiers)):
                for j in range(i + 1, len(unique_identifiers)):
                    if unique_identifiers[i][z] != unique_identifiers[j][z]:
                        results[z] = True
                        break
                    # end if
                # end for
                if results[z]:
                    break
                # end if
            # end for
        # end for

        self.assertEqual(obtained=results, expected=[True] * 16, msg="Some bytes never changes")

        self.testCaseChecked("FNT_0021_0009")
    # end def test_MultipleRegenIdNotSameGetByte0To15

    @features('Feature0021')
    @level('Security')
    def test_MultipleRegenIdNotSameGetByte16To31(self):
        """
        Randomness of uniqueId[16..31]: interleave calls to regenId and getByte16_31 to check new random identifier
        is generated every time. Test 10 tries at least and verify each byte is changed.
        """

        unique_identifiers = [[]] * 10

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop 10 times')
        # ---------------------------------------------------------------------------
        for i in range(len(unique_identifiers)):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send regenId request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            regen_id = RegenId(device_index=self.deviceIndex, feature_index=self.feature_index)
            self.send_report_wait_response(report=regen_id,
                                           response_queue=self.hidDispatcher.common_message_queue,
                                           response_class_type=RegenIdResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send getByte16_31 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for getByte16_31 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_16_t_31_response = self.send_report_wait_response(
                report=get_byte_16_t_31,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetByte16To31Response)

            unique_identifiers[i] = get_byte_16_t_31_response.bytes_16_to_31

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Compare the new uniqueId with the previous one (at least 1 out of the 16 '
                           'bytes shall be different)')
            # ---------------------------------------------------------------------------
            if i > 0:
                self.assertNotEqual(obtained=unique_identifiers[i],
                                    unexpected=unique_identifiers[i - 1],
                                    msg="The unique identifier is the same as the previous one")
            # end if
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Compare the 10 received numbers and validate each byte value had changed at '
                       'least once.')
        # ---------------------------------------------------------------------------
        results = [False] * 16
        for z in range(len(results)):
            for i in range(len(unique_identifiers)):
                for j in range(i + 1, len(unique_identifiers)):
                    if unique_identifiers[i][z] != unique_identifiers[j][z]:
                        results[z] = True
                        break
                    # end if
                # end for
                if results[z]:
                    break
                # end if
            # end for
        # end for

        self.assertEqual(obtained=results, expected=[True] * 16, msg="Some bytes never changes")

        self.testCaseChecked("FNT_0021_0010")
    # end def test_MultipleRegenIdNotSameGetByte16To31

    @features('Feature0021')
    @level('Functionality')
    def test_MultipleGetByteRequestStability(self):
        """
        Data storage stability: interleave calls to getByte0_15 and getByte16_31 to check the same identifier is
        returned every time. Test 10 tries at least.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Get a uniqueId thru getByte calls')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate no \'HW error\' is reported and save the initial unique identifier')
        # ---------------------------------------------------------------------------
        get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_0_to_15_response = self.send_report_wait_response(
            report=get_byte_0_to_15,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=GetByte0To15Response)

        get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_16_t_31_response = self.send_report_wait_response(
            report=get_byte_16_t_31,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=GetByte16To31Response)

        unique_identifier = get_byte_0_to_15_response.bytes_0_to_15 + get_byte_16_t_31_response.bytes_16_to_31

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop 10 times')
        # ---------------------------------------------------------------------------
        for _ in range(10):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send getByte0_15 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for getByte0_15 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_0_to_15_response = self.send_report_wait_response(
                report=get_byte_0_to_15,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetByte0To15Response)

            bytes_0_to_15 = get_byte_0_to_15_response.bytes_0_to_15

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send getByte16_31 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Wait for getByte16_31 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_16_t_31_response = self.send_report_wait_response(
                report=get_byte_16_t_31,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetByte16To31Response)

            bytes_16_to_31 = get_byte_16_t_31_response.bytes_16_to_31

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 4: Validate the returned uniqueId is always the same.')
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=bytes_0_to_15 + bytes_16_to_31,
                             expected=unique_identifier,
                             msg="The unique identifier is different from the expected one")
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_0021_0011")
    # end def test_MultipleGetByteRequestStability

    @features('Feature0021')
    @level('Stress')
    @services('PowerSwitch')
    def test_GetByteRequestStabilityAfterResetPowerSwitch(self):
        """
        Data storage stability: reset the device using the power switch between 2 calls to getByte0_15
        (or getByte16_31) and check the same identifier is returned every time.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Get a uniqueId thru getByte calls')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate no \'HW error\' is reported and save the initial unique identifier')
        # ---------------------------------------------------------------------------
        get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_0_to_15_response = self.send_report_wait_response(
            report=get_byte_0_to_15,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=GetByte0To15Response)

        get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_16_t_31_response = self.send_report_wait_response(
            report=get_byte_16_t_31,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=GetByte16To31Response)

        unique_identifier = get_byte_0_to_15_response.bytes_0_to_15 + get_byte_16_t_31_response.bytes_16_to_31

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop 2 times')
        # ---------------------------------------------------------------------------
        for _ in range(2):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Reset the device using the power switch')
            # ---------------------------------------------------------------------------
            # TODO

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send getByte0_15 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for getByte0_15 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_0_to_15_response = self.send_report_wait_response(
                report=get_byte_0_to_15,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetByte0To15Response)

            bytes_0_to_15 = get_byte_0_to_15_response.bytes_0_to_15

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 4: Send getByte16_31 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Wait for getByte16_31 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_16_t_31_response = self.send_report_wait_response(
                report=get_byte_16_t_31,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetByte16To31Response)

            bytes_16_to_31 = get_byte_16_t_31_response.bytes_16_to_31

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 4: Validate the returned uniqueId is always the same.')
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=bytes_0_to_15 + bytes_16_to_31,
                             expected=unique_identifier,
                             msg="The unique identifier is different from the expected one")
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_0021_0012")
    # end def test_GetByteRequestStabilityAfterResetPowerSwitch

    @features('Feature0021')
    @level('Stress')
    @services('PowerSupply')
    def test_GetByteRequestStabilityAfterResetPowerSupply(self):
        """
        Data storage stability: turn off the device using the power supply service between 2 calls to getByte0_15 and
        getByte16_31 and check same word is returned every time.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Get a uniqueId thru getByte calls')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate no \'HW error\' is reported and save the initial unique identifier')
        # ---------------------------------------------------------------------------
        get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_0_to_15_response = self.send_report_wait_response(
            report=get_byte_0_to_15,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=GetByte0To15Response)

        get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_16_t_31_response = self.send_report_wait_response(
            report=get_byte_16_t_31,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=GetByte16To31Response)

        unique_identifier = get_byte_0_to_15_response.bytes_0_to_15 + get_byte_16_t_31_response.bytes_16_to_31

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop 2 times')
        # ---------------------------------------------------------------------------
        for _ in range(2):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Turn off / on the power to the device using the power supply service')
            # ---------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send getByte0_15 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for getByte0_15 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_0_to_15_response = self.send_report_wait_response(
                report=get_byte_0_to_15,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetByte0To15Response)

            bytes_0_to_15 = get_byte_0_to_15_response.bytes_0_to_15

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 4: Send getByte16_31 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Wait for getByte16_31 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_16_t_31_response = self.send_report_wait_response(
                report=get_byte_16_t_31,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetByte16To31Response)

            bytes_16_to_31 = get_byte_16_t_31_response.bytes_16_to_31

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 4: Validate the returned uniqueId is always the same.')
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=bytes_0_to_15 + bytes_16_to_31,
                             expected=unique_identifier,
                             msg="The unique identifier is different from the expected one")
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_0021_0013")
    # end def test_GetByteRequestStabilityAfterResetPowerSupply

    @features('Feature0021')
    @level('ErrorHandling')
    def test_WrongFunctionIndex(self):
        """
        Invalid Function index shall raise an error INVALID_FUNCTION_ID (7).
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over functionIndex invalid range (typical wrong values)')
        # ---------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(UniqueIdentifier32Bytes.MAX_FUNCTION_INDEX + 1)),
                                                  max_value=0xF):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send regenId with functionIndex = {function_index}')
            # ---------------------------------------------------------------------------
            regen_id = RegenId(device_index=self.deviceIndex, feature_index=self.feature_index)
            regen_id.functionIndex = function_index
            regen_id_response = self.send_report_wait_response(report=regen_id,
                                                               response_queue=self.hidDispatcher.error_message_queue,
                                                               response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidFunctionId (0x07) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(regen_id_response.errorCode)),
                             expected=ErrorCodes.INVALID_FUNCTION_ID,
                             msg="The parameter errorCode differ from the one expected")
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_0021_0001")
    # end def test_WrongFunctionIndex

    @features('Feature0021')
    @level('Robustness')
    def test_IgnoreSoftwareId(self):
        """
        SoftwareId input is ignored by the firmware.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over softwareId range (several interesting values)')
        # ---------------------------------------------------------------------------
        for software_id in compute_inf_values(UniqueIdentifier32Bytes.DEFAULT.SOFTWARE_ID)[1:]:
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send getByte0_15 request with softwareId = {software_id}')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for getByte0_15 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_0_to_15.softwareId = software_id
            self.send_report_wait_response(report=get_byte_0_to_15,
                                           response_queue=self.hidDispatcher.common_message_queue,
                                           response_class_type=GetByte0To15Response)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_0021_0002")
    # end def test_IgnoreSoftwareId

    @features('Feature0021')
    @level('Robustness')
    def test_IgnorePadding(self):
        """
        Padding bytes shall be ignored by the firmware.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over padding range (several interesting values)')
        # ---------------------------------------------------------------------------
        for padding in compute_sup_values(HexList(Numeral(UniqueIdentifier32Bytes.DEFAULT.PADDING,
                                                          GetByte0To15.LEN.PADDING // 8))):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send getByte0_15 request with padding = {padding}')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Wait for getByte0_15 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
            get_byte_0_to_15.padding = padding
            self.send_report_wait_response(report=get_byte_0_to_15,
                                           response_queue=self.hidDispatcher.common_message_queue,
                                           response_class_type=GetByte0To15Response)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_0021_0003")
    # end def test_IgnorePadding
# end class ApplicationUniqueIdentifier32BytesTestCase


class ApplicationUniqueIdentifier32BytesSpecificFirmwareTestCase(BaseTestCase):
    """
    Validates 32 Bytes Unique Identifier that needs a specific firmware TestCases
    """

    def setUp(self):
        """
        Handles test pre-requisites.
        """
        super().setUp()

        # ------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)
        invalidated_chunk_count = self.memory_manager.invalidate_chunks(["NVS_X0021_32BYTE_ID_ID"], )
        if invalidated_chunk_count > 0:
            self.memory_manager.load_nvs()
        # end if

        # Empty message queues
        self.empty_queues()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Send Root.GetFeature(0x0021)')
        # ---------------------------------------------------------------------------
        self.feature_index = self.updateFeatureMapping(feature_id=UniqueIdentifier32Bytes.FEATURE_ID)
    # end def setUp

    @features('Feature0021')
    @level('Functionality')
    @services('Debugger')
    def test_GetByte0To15WithIdNotGenerated(self):
        """
        The call to 'getByte0_15' generate the random number if no call to 'regenId' done before.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send getByte0_15 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for getByte0_15 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_0_to_15_response = self.send_report_wait_response(
                                                            report=get_byte_0_to_15,
                                                            response_queue=self.hidDispatcher.common_message_queue,
                                                            response_class_type=GetByte0To15Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Dump the final NVS state and validate a chunk has been added and that it '
                       'matches the HID++ value')
        # ---------------------------------------------------------------------------
        final_nvs_parser = self.get_dut_nvs_parser()

        chunk_before = self.memory_manager.backup_nvs_parser.get_chunk("NVS_X0021_32BYTE_ID_ID")
        chunk_after = final_nvs_parser.get_chunk("NVS_X0021_32BYTE_ID_ID")

        self.assertNotEqual(unexpected=chunk_before,
                            obtained=chunk_after,
                            msg="No chunk added")

        self.assertEqual(expected=list(chunk_after.chunk_data)[:16],
                         obtained=list(get_byte_0_to_15_response.bytes_0_to_15),
                         msg="Data do not match")

        self.testCaseChecked("FNT_0021_0006")
    # end def test_GetByte0To15WithIdNotGenerated

    @features('Feature0021')
    @level('Functionality')
    @services('Debugger')
    def test_GetByte16To31WithIdNotGenerated(self):
        """
        The call to 'getByte16_31' generate the random number if no call to 'regenId' done before.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send getByte16_31 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for getByte16_31 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_16_t_31_response = self.send_report_wait_response(
                                                            report=get_byte_16_t_31,
                                                            response_queue=self.hidDispatcher.common_message_queue,
                                                            response_class_type=GetByte16To31Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Dump the final NVS state and validate a chunk has been added and that it '
                       'matches the HID++ value')
        # ---------------------------------------------------------------------------
        final_nvs_parser = self.get_dut_nvs_parser()

        chunk_before = self.memory_manager.backup_nvs_parser.get_chunk("NVS_X0021_32BYTE_ID_ID")
        chunk_after = final_nvs_parser.get_chunk("NVS_X0021_32BYTE_ID_ID")

        self.assertNotEqual(unexpected=chunk_before,
                            obtained=chunk_after,
                            msg="No chunk added")

        self.assertEqual(expected=list(chunk_after.chunk_data)[16:],
                         obtained=list(get_byte_16_t_31_response.bytes_16_to_31),
                         msg="Data do not match")

        self.testCaseChecked("FNT_0021_0007")
    # end def test_GetByte16To31WithIdNotGenerated

    @features('Feature0021')
    @level('Stress')
    @services('Debugger')
    def test_NvsEndurance(self):
        """
        NVS endurance: interleave a thousand calls to regenId and getByte0_15 to check NVS management.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop 1000 times')
        # ---------------------------------------------------------------------------
        for _ in range(1000):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send regenId request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check no error response')
            # ---------------------------------------------------------------------------
            regen_id = RegenId(device_index=self.deviceIndex, feature_index=self.feature_index)
            self.send_report_wait_response(report=regen_id,
                                           response_queue=self.hidDispatcher.common_message_queue,
                                           response_class_type=RegenIdResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send getByte0_15 request')
            # ---------------------------------------------------------------------------
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Wait for getByte0_15 response and validate no \'HW error\' is reported')
            # ---------------------------------------------------------------------------
            get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
            self.send_report_wait_response(report=get_byte_0_to_15,
                                           response_queue=self.hidDispatcher.common_message_queue,
                                           response_class_type=GetByte0To15Response)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Dump data in NVS and validate chunk structure')
        # ---------------------------------------------------------------------------
        nvs_parser_to_check = self.get_dut_nvs_parser()
        self.assertGreaterEqual(a=len(nvs_parser_to_check.get_chunk_history("NVS_X0021_32BYTE_ID_ID")),
                                b=1,
                                msg="Wrong chunk structure")
        self.assertTrue(expr=nvs_parser_to_check.is_last_chunk_id("NVS_X0021_32BYTE_ID_ID"),
                        msg="Last chunk is not NVS_X0021_32BYTE_ID_ID")

        self.testCaseChecked("FNT_0021_0014")
    # end def test_NvsEndurance
# end class ApplicationUniqueIdentifier32BytesSpecificFirmwareTestCase


class ApplicationUniqueIdentifier32BytesMultiReceiverTestCase(BaseTestCase):
    """
    Validates Change Host with Multi Receivers TestCases
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_set_back_current_host = False
        super().setUp()

        # ------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        if self.f.SHARED.PAIRING.F_BLEDevicePairing:
            # ---------------------------------------------------------------------------
            self.logTitle2('Pre-requisite#2: Pair device to a second dongle')
            # ---------------------------------------------------------------------------
            # Cleanup all pairing slots except the first one
            CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)

            # Initialize the authentication method parameter
            DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

            self.ble_pro_receiver_port_indexes = ReceiverTestUtils.get_receiver_port_indexes(
                self,
                ReceiverTestUtils.USB_PID_MEZZY_BLE_PRO,
                skip=[ChannelUtils.get_port_index(test_case=self)])

            self.post_requisite_set_back_current_host = True
            assert len(self.ble_pro_receiver_port_indexes) > 0, \
                "Cannot perform multi receiver tests if not enough receivers"
            DevicePairingTestUtils.pair_device_slot_to_other_receiver(
                test_case=self,
                device_slot=1,
                other_receiver_port_index=self.ble_pro_receiver_port_indexes[0],
                hid_dispatcher_to_dump=self.current_channel.hid_dispatcher)

            # Reconnect with the first receiver
            ReceiverTestUtils.switch_to_receiver(
                self, receiver_port_index=ChannelUtils.get_port_index(test_case=self, channel=self.backup_dut_channel))

            # Change host on Device
            DevicePairingTestUtils.change_host_by_link_state(
                self, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

            DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
            self.post_requisite_set_back_current_host = False
        # end if

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Send Root.GetFeature(0x0021)')
        # ---------------------------------------------------------------------------
        self.feature_index = self.updateFeatureMapping(feature_id=UniqueIdentifier32Bytes.FEATURE_ID)

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#3: Send Root.GetFeature(0x1814)')
        # ---------------------------------------------------------------------------
        self.feature_1814_index = self.updateFeatureMapping(feature_id=ChangeHost.FEATURE_ID)
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_set_back_current_host:
                # ---------------------------------------------------------------------------
                self.logTitle2('Post-requisite#1: Send SetCurrentHost with hostIndex=0')
                # ---------------------------------------------------------------------------
                current_host_number = self.port_index_to_host_number(
                    port_index=ChannelUtils.get_port_index(test_case=self))

                if current_host_number != 0:
                    ChangeHostTestUtils.HIDppHelper.set_current_host(
                        self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=0)

                    DeviceManagerUtils.switch_channel(
                        test_case=self,
                        new_channel=self.backup_dut_channel)
                # end if
            # end if
            if self.f.SHARED.PAIRING.F_BLEDevicePairing:
                # --------------------------------------------------------------------------
                CommonBaseTestUtils.LogHelper.log_post_requisite(self, "Reload initial NVS")
                # --------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super().tearDown()
    # end def tearDown

    @features('Feature0021')
    @features('Feature1814')
    @level('Business')
    @services('MultiHost')
    def test_GetUniqueIdentifierOnMultiHostBusinessCase(self):
        """
        'Flow' scenario: generate an identifier, retrieve it on current host, change to host 2, then check the same
        identifier is retrieve on host 2.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send regenId request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check no error response')
        # ---------------------------------------------------------------------------
        regen_id = RegenId(device_index=self.deviceIndex, feature_index=self.feature_index)
        self.send_report_wait_response(report=regen_id,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=RegenIdResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send getByte0_15 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for getByte0_15 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_0_to_15_response = self.send_report_wait_response(
                                                            report=get_byte_0_to_15,
                                                            response_queue=self.hidDispatcher.common_message_queue,
                                                            response_class_type=GetByte0To15Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send getByte16_31 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Wait for getByte16_31 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_16_t_31_response = self.send_report_wait_response(
                                                            report=get_byte_16_t_31,
                                                            response_queue=self.hidDispatcher.common_message_queue,
                                                            response_class_type=GetByte16To31Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Compute uniqueId with uniqueId[0..15] and uniqueId[16..31]')
        # ---------------------------------------------------------------------------
        unique_identifier_h0 = HexList(get_byte_0_to_15_response.bytes_0_to_15) + \
                               HexList(get_byte_16_t_31_response.bytes_16_to_31)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Send ChangeHost SetCurrentHost with hostIndex=1')
        # ---------------------------------------------------------------------------
        self.post_requisite_set_back_current_host = True
        current_host_number = self.port_index_to_host_number(
            port_index=ChannelUtils.get_port_index(test_case=self))

        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self,
            device_index=ChannelUtils.get_device_index(test_case=self),
            host_index=1)

        # It seems that equad devices do not send a connection event when sending SetCurrentHost with the
        # same host as the one currently used. In BLE Pro, it does.
        # TODO verify for LS2
        if not isinstance(self.current_channel, ThroughEQuadReceiverChannel) or current_host_number != 1:
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(
                    port_index=self.host_number_to_port_index(host_index=1), device_index=1))
        # end if

        # Empty queue
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 6: Send getByte0_15 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Wait for getByte0_15 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_0_to_15 = GetByte0To15(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_0_to_15_response = self.send_report_wait_response(
                                                            report=get_byte_0_to_15,
                                                            response_queue=self.hidDispatcher.common_message_queue,
                                                            response_class_type=GetByte0To15Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send getByte16_31 request')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 5: Wait for getByte16_31 response and validate no \'HW error\' is reported')
        # ---------------------------------------------------------------------------
        get_byte_16_t_31 = GetByte16To31(device_index=self.deviceIndex, feature_index=self.feature_index)
        get_byte_16_t_31_response = self.send_report_wait_response(
                                                            report=get_byte_16_t_31,
                                                            response_queue=self.hidDispatcher.common_message_queue,
                                                            response_class_type=GetByte16To31Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Verify the same uniqueId is retrieved on host 1')
        # ---------------------------------------------------------------------------
        unique_identifier_h1 = HexList(get_byte_0_to_15_response.bytes_0_to_15) + \
                               HexList(get_byte_16_t_31_response.bytes_16_to_31)
        self.assertEqual(obtained=unique_identifier_h1,
                         expected=unique_identifier_h0,
                         msg="Identifier not equal between hosts")

        self.testCaseChecked("FNT_0021_0005")
    # end def test_GetUniqueIdentifierOnMultiHostBusinessCase
# end class ApplicationUniqueIdentifier32BytesMultiReceiverTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
