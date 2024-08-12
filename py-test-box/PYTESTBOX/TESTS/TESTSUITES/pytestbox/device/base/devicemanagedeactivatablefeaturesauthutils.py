#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils
:brief:  Helpers for Manage Deactivatable Features (based on authentication mechanism) feature for device
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import perf_counter

from pyharness.core import TestException
from pyharness.extensions import WarningLevel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import GetBattCalibrationInfo
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesFactory
from pyhid.hidpp.features.common.equaddjdebuginfo import EquadDJDebugInfo
from pyhid.hidpp.features.common.equaddjdebuginfo import ReadEquadDJDebugInfo
from pyhid.hidpp.features.common.equadpairingenc import EquadPairingEnc
from pyhid.hidpp.features.common.equadpairingenc import EquadPairingEncFactory
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthFactory
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pyhid.hidpp.features.common.powermodes import GetPowerModesTotalNumber
from pyhid.hidpp.features.common.powermodes import PowerModes
from pyhid.hidpp.features.common.rftest import RFTest
from pyhid.hidpp.features.common.rftest import RFTestFactory
from pyhid.hidpp.features.common.rftestble import RFTestBLE
from pyhid.hidpp.features.common.rftestble import RFTestBLEFactory
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvm
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvmFactory
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.featureset import FeatureSet
from pyhid.hidpp.features.featureset import FeatureSetFactory
from pyhid.hidpp.features.root import RootFactory
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.featuresetutils import FeatureSetTestUtils
from pytestbox.device.base.passwordauthenticationutils import DevicePasswordAuthenticationTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.managedeactivatablefeaturesauthutils import SharedManageDeactivatableFeaturesAuthTestUtils
from pytransport.usb.usbconstants import LogitechReceiverProductId
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceManageDeactivatableFeaturesAuthTestUtils(SharedManageDeactivatableFeaturesAuthTestUtils,
                                                     DeviceBaseTestUtils):
    """
    Test utils for Manage Deactivatable Features feature for device
    """
    class GetReactInfoResponseChecker(SharedManageDeactivatableFeaturesAuthTestUtils.MessageChecker):
        """
        Test utils to check getReactInfo response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "auth_feature": (cls.check_auth_feature,
                                 test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_AuthFeature),
            }
        # end def get_default_check_map

        @staticmethod
        def check_auth_feature(test_case, message, expected):
            """
            Check 2 bytes long 'authFeature' field value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetReactInfoResponse``
            :param expected: Authentication feature field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.auth_feature)), expected=expected,
                                  msg="Authentication feature is not as expected")
        # end def check_auth_feature
    # end class GetReactInfoResponseChecker

    class HIDppHelper(SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper,
                      DeviceBaseTestUtils.HIDppHelper):
        # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=ManageDeactivatableFeaturesAuth.FEATURE_ID,
                           factory=ManageDeactivatableFeaturesAuthFactory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_feature_interface(cls, test_case):
            # See ``SharedManageDeactivatableFeaturesAuthTestCase.get_feature_interface``
            # noinspection PyUnresolvedReferences
            # If manage_deactivatable_features_auth attribute does not exist, it will be set
            if not hasattr(test_case, "manage_deactivatable_features_auth") \
                    or test_case.manage_deactivatable_features_auth is None:
                setattr(test_case,
                        "manage_deactivatable_features_auth",
                        ManageDeactivatableFeaturesAuthFactory.create(test_case.config_manager.get_feature_version(
                            test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH)))
            # end if
            # noinspection PyUnresolvedReferences
            return test_case.manage_deactivatable_features_auth
        # end def get_feature_interface

        @classmethod
        def feature_response_queue(cls, test_case):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.feature_response_queue``
            return test_case.hidDispatcher.common_message_queue
        # end def feature_response_queue

        @classmethod
        def get_info(cls, test_case, device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_info``
            feature_1e02_index, feature_1e02, device_index, _ = cls.get_parameters(
                test_case,
                device_index=device_index,
                port_index=port_index)

            get_info_req = feature_1e02.get_info_cls(device_index, feature_1e02_index)
            get_info_resp = ChannelUtils.send(
                test_case=test_case,
                report=get_info_req,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e02.get_info_response_cls
            )
            return get_info_resp
        # end def get_info

        @classmethod
        def get_disable_features_req(cls, test_case, disable_all=False, manufacturing=False, compliance=False,
                                     gotthard=False, device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_disable_features_req``
            feature_1e02_index, feature_1e02, device_index, port_index = cls.get_parameters(
                test_case, ManageDeactivatableFeaturesAuth.FEATURE_ID, ManageDeactivatableFeaturesAuthFactory,
                device_index, port_index)

            disable_features_req = feature_1e02.disable_features_cls(
                device_index, feature_1e02_index, disable_all_bit=disable_all, disable_gothard=gotthard,
                disable_compliance=compliance, disable_manufacturing=manufacturing)
            return disable_features_req
        # end def get_disable_features_req

        @classmethod
        def disable_features(cls, test_case, disable_all=False, manufacturing=False, compliance=False, gotthard=False,
                             device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features``
            feature_1e02_index, feature_1e02, device_index, _ = cls.get_parameters(
                test_case,
                device_index=device_index,
                port_index=port_index)

            disable_features_req = feature_1e02.disable_features_cls(
                device_index, feature_1e02_index, disable_all_bit=disable_all, disable_gothard=gotthard,
                disable_compliance=compliance, disable_manufacturing=manufacturing)
            disable_features_resp = ChannelUtils.send(
                test_case=test_case,
                report=disable_features_req,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e02.disable_features_response_cls
            )
            return disable_features_resp
        # end def disable_features

        @classmethod
        def get_enable_features_req(cls, test_case, enable_all=False, manufacturing=False, compliance=False,
                                    gotthard=False, device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_enable_features_req``
            feature_1e02_index, feature_1e02, device_index, port_index = cls.get_parameters(
                test_case, ManageDeactivatableFeaturesAuth.FEATURE_ID, ManageDeactivatableFeaturesAuthFactory,
                device_index, port_index)

            enable_features_req = feature_1e02.enable_features_cls(device_index,
                                                                   feature_1e02_index,
                                                                   enable_all_bit=enable_all,
                                                                   enable_gothard=gotthard,
                                                                   enable_compliance=compliance,
                                                                   enable_manufacturing=manufacturing)
            return enable_features_req
        # end def get_enable_features_req

        @classmethod
        def enable_features(cls, test_case, enable_all=False, manufacturing=False, compliance=False, gotthard=False,
                            start_session=True, device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features``
            feature_1e02_index, feature_1e02, device_index, _ = cls.get_parameters(
                test_case,
                device_index=device_index,
                port_index=port_index)

            if start_session:
                get_react_info_req = feature_1e02.get_reactivation_info_cls(device_index, feature_1e02_index)
                get_react_info_resp = test_case.send_report_wait_response(
                    report=get_react_info_req,
                    response_queue=test_case.hidDispatcher.common_message_queue,
                    response_class_type=feature_1e02.get_reactivation_info_response_cls)

                test_case.assertEqual(obtained=int(Numeral(get_react_info_resp.auth_feature)),
                                      expected=PasswordAuthentication.FEATURE_ID,
                                      msg=f'Reactivation feature should be {PasswordAuthentication.FEATURE_ID}')

                manufacturing |= (
                    enable_all &
                    test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportManufacturing)
                compliance |= (
                        enable_all &
                        test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportCompliance)
                gotthard |= (
                        enable_all &
                        test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportGotthard)

                if manufacturing:
                    DevicePasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                        test_case=test_case,
                        account_name=DevicePasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value)
                # end if
                if compliance:
                    DevicePasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                        test_case=test_case,
                        account_name=DevicePasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value)
                # end if
                if gotthard:
                    DevicePasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                        test_case=test_case,
                        account_name=DevicePasswordAuthenticationTestUtils.AccountNames.GOTHARD.value)
                # end if
            # end if
            enable_features_req = feature_1e02.enable_features_cls(
                device_index=device_index,
                feature_index=feature_1e02_index,
                enable_all_bit=enable_all,
                enable_gothard=gotthard,
                enable_compliance=compliance,
                enable_manufacturing=manufacturing)
            enable_features_resp = test_case.send_report_wait_response(
                report=enable_features_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1e02.enable_features_response_cls)

            return enable_features_resp
        # end def enable_features

        @classmethod
        def get_reactivation_info(cls, test_case, device_index=None, port_index=None):
            """
            Send getReactInfo request

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: getReactInfo response
            :rtype: ``GetReactInfoResponse``
            """
            feature_1e02_index, feature_1e02, device_index, _ = cls.get_parameters(
                test_case,
                device_index=device_index,
                port_index=port_index)

            get_react_info_req = feature_1e02.get_reactivation_info_cls(device_index, feature_1e02_index)
            get_react_info_resp = ChannelUtils.send(
                test_case=test_case,
                report=get_react_info_req,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e02.get_reactivation_info_response_cls
            )

            return get_react_info_resp
        # end def get_reactivation_info

        @classmethod
        def get_features(cls, test_case, manufacturing=False, compliance=False, gotthard=False):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_features``
            manufacturing_features = None
            compliance_features = None
            gotthard_features = None
            if manufacturing:
                manufacturing_features = FeatureSetTestUtils.HIDppHelper.get_features_by_type(
                    test_case, [FeatureSetTestUtils.FeatureTypes.MANUFACTURING_DEACTIVATABLE])
            # end if
            if compliance:
                compliance_features = FeatureSetTestUtils.HIDppHelper.get_features_by_type(
                    test_case, [FeatureSetTestUtils.FeatureTypes.COMPLIANCE_DEACTIVATABLE])
            # end if
            if gotthard:
                gotthard_features = FeatureSetTestUtils.HIDppHelper.get_features(test_case)
            # end if
            return manufacturing_features, compliance_features, gotthard_features
        # end def get_features

        @classmethod
        def check_enabled_features(cls, test_case, features, device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_enabled_features``
            device_index = device_index if device_index is not None else ChannelUtils.get_device_index(test_case)
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(
                test_case=test_case)

            asserted_once = False
            for feature in features:
                request_cls = cls.get_check_enabled_request_cls(
                    test_case, feature.feature_id, feature.feature_version)
                if request_cls is not None:
                    feature_index = cls.get_feature_index(test_case, feature.feature_id, device_index, port_index)
                    # noinspection PyTypeChecker
                    request = request_cls(device_index, feature_index)
                    ChannelUtils.clean_messages(test_case, HIDDispatcher.QueueName.COMMON, HidppMessage)
                    ChannelUtils.clean_messages(test_case, HIDDispatcher.QueueName.IMPORTANT, HidppMessage)
                    ChannelUtils.send_only(test_case=test_case, report=request, timeout=1)

                    response_received = False
                    start_time = perf_counter()
                    # Wait maximum 2s for a response in one of the possible queues to let time to the device to respond
                    # No check that a response is received because some request does not have response and the goal
                    # here is only to check that the feature is enabled
                    while (not response_received) and (perf_counter() - start_time < 2):
                        com_resp = ChannelUtils.clean_messages(test_case, HIDDispatcher.QueueName.COMMON, HidppMessage)
                        imp_resp = ChannelUtils.clean_messages(
                            test_case, HIDDispatcher.QueueName.IMPORTANT, HidppMessage)
                        response_received = len(com_resp) > 0 or len(imp_resp) > 0
                    # end while

                    test_case.assertListEqual(
                        ChannelUtils.clean_messages(test_case, HIDDispatcher.QueueName.ERROR, Hidpp2ErrorCodes),
                        [],
                        f"No error should be raised when sending {hex(request.FEATURE_ID)} command")
                    ChannelUtils.clean_messages(test_case, HIDDispatcher.QueueName.COMMON, HidppMessage)
                    ChannelUtils.clean_messages(test_case, HIDDispatcher.QueueName.IMPORTANT, HidppMessage)
                    asserted_once = True
                # end if
            # end for
            if not asserted_once:
                test_case.log_warning("No feature available to check the current features set",
                                      force_console_print=True)
            # end if
        # end def check_enabled_features

        @classmethod
        def check_disabled_features(cls, test_case, features, device_index=None, port_index=None):
            # ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_disabled_features``
            device_index = device_index if device_index is not None else ChannelUtils.get_device_index(test_case)
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(
                test_case=test_case)

            asserted_once = False
            for feature in features:
                request_cls = cls.get_check_enabled_request_cls(
                    test_case, feature.feature_id, feature.feature_version)
                if request_cls is not None:
                    feature_index = cls.get_feature_index(test_case, feature.feature_id, device_index, port_index)
                    # noinspection PyTypeChecker
                    request = request_cls(device_index, feature_index)
                    err_resp = ChannelUtils.send(
                        test_case=test_case,
                        report=request,
                        response_queue_name=HIDDispatcher.QueueName.ERROR,
                        response_class_type=Hidpp2ErrorCodes)
                    assert isinstance(err_resp, Hidpp2ErrorCodes)
                    cls.check_hidpp20_error_message(test_case,
                                                    err_resp,
                                                    feature_index=feature_index,
                                                    function_index=request.functionIndex,
                                                    error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])
                    asserted_once = True
                # end if
            # end for
            if not asserted_once:
                test_case.log_warning("No feature available to check the current features set",
                                      force_console_print=True)
            # end if
        # end def check_disabled_features

        @classmethod
        def get_check_enabled_request_cls(cls, test_case, feature_id, feature_version):
            """
            Get request class to be sent to check if the feature is enabled

            Notes:
             * Currently, not all features are supported. It is possible to extend the coverage.
             * Some features can not be used for this kind of check because it could change the state of the device (
             e.g., Reset should not be used)

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param feature_id: Feature Identifier
            :type feature_id: ``int``
            :param feature_version: Feature version
            :type feature_version: ``int``
            """
            feature_id_map = {
                FeatureSet.FEATURE_ID: {
                    "factory": FeatureSetFactory,
                    "request_cls": "get_count_cls"
                },
                #######################################################
                # MANUFACTURING
                #######################################################
                # x1800_generictestcommands
                # x1801_manufacturingmode
                # x1802_devicereset -> specific case
                # x1803_gpioaccess
                # x1806_configurabledeviceproperties
                ConfigurableDeviceProperties.FEATURE_ID: {
                    "factory": ConfigurableDevicePropertiesFactory,
                    "request_cls": "get_device_name_max_count_cls"
                },
                # x1810_equadpairing
                # x1811_equadpairingenc
                EquadPairingEnc.FEATURE_ID: {
                    "factory": EquadPairingEncFactory,
                    "request_cls": "get_pairing_info_cls"
                },
                # x1812_equadmultihostpairing
                # x1813_equadmultihostpairingenc
                # x1816_bleproprepairing
                # BleProPrepairing.FEATURE_ID: {
                #     "factory": BleProPrepairingFactory,
                #     "request_cls": "get_prepairing_data_cls"
                # },
                # x1820_keystrokesimulation
                # x1830_powermodes
                PowerModes.FEATURE_ID: GetPowerModesTotalNumber,
                # x1840_pertest
                # x1850_squalshutter
                # x1860_adcValue
                # x1860_adcstatus
                # x1861_battcalibration
                BatteryLevelsCalibration.FEATURE_ID: GetBattCalibrationInfo,
                # x1862_battcalibration
                # x1863_batterylevelscalibration
                # x18a0_ledtest
                # x18a1_ledtest
                # x18b0_monitormode
                # x18b1_monitormode
                # x18c0_rollertest
                # x18d0_touchpadpowermodetest
                # x18e2_synafunc05
                # x18e3_synafunc09
                # x18e4_bm250accelerometer
                # x18e5_s7020testcommands
                # x18e6_cytra112003test
                # x1a20_alscalibration
                # x1df3_equaddjdebuginfo
                EquadDJDebugInfo.FEATURE_ID: ReadEquadDJDebugInfo,
                # x1e22_spidirectaccess
                # x1e80_memoryaccess
                # x1e90_otpmemoryaccess
                # x1ea1_fusebytes
                # x1eb0_tdemfgaccess
                TdeAccessToNvm.FEATURE_ID: {
                    "factory": TdeAccessToNvmFactory,
                    "request_cls": "get_tde_mem_length_cls"
                },
                # x1f01_beijingtouchpadaccess
                # x1f03_2dsensordirectaccess
                # x1f05_genericdebug
                # x1f07_beijingwin8touchpadaccess
                # x1f0a_eraseprepairinginfo
                # x1f10_calabletest
                # x1f11_generictouchpadaccess
                # x1f1f_firmware_properties
                # x9000_testag8020
                # x9001_testpmw3816
                # x9200_testlis3mdl
                # x9202_testbmm150
                # x9280_testtlc5949
                # x9300_testepmdrive
                #######################################################
                # COMPLIANCE
                #######################################################
                # x1890_rftest_eqmac
                RFTest.FEATURE_ID: {
                    "factory": RFTestFactory,
                    "request_cls": "rf_send_periodic_msg_cls"
                },
                # x1891_rftest_eqmac
                RFTestBLE.FEATURE_ID: {
                    "factory": RFTestBLEFactory,
                    "request_cls": "rf_send_periodic_msg_cls"
                },
            }

            feature_id = int(Numeral(feature_id))
            feature_version = int(Numeral(feature_version))
            if feature_id in feature_id_map:
                if isinstance(feature_id_map[feature_id], dict):
                    try:
                        request_cls = getattr(feature_id_map[feature_id]["factory"].create(feature_version),
                                              feature_id_map[feature_id]["request_cls"])
                    except KeyError:
                        test_case.log_warning(f'Feature version {feature_version} not available in feature model for '
                                              f'feature {feature_id}')
                        request_cls = None
                    # end try
                elif isinstance(feature_id_map[feature_id], HidppMessage):
                    request_cls = feature_id_map[feature_id]
                else:
                    test_case.log_warning(f"Unable to get request class for feature {feature_id}",
                                          warning_level=WarningLevel.ROBUSTNESS)
                    request_cls = None
                # end if
            else:
                test_case.log_warning(f"Feature {feature_id} not supported", warning_level=WarningLevel.ROBUSTNESS)
                request_cls = None
            # end if

            if request_cls is not None:
                assert issubclass(request_cls, HidppMessage), "Request class should be a HidppMessage"
            # end if

            return request_cls
        # end def get_check_enabled_request_cls
    # end class HIDppHelper

    class NvsHelper(SharedManageDeactivatableFeaturesAuthTestUtils.NvsHelper):
        # See ``SharedManageDeactivatableFeaturesAuthTestUtils.NvsHelper``
        pass
    # end class NvsHelper

    @classmethod
    def check_gotthard_enabled(cls, test_case, get_info_state=True, nvs=True, send_requests=True,
                               device_index_on_gotthard=None, gotthard_receiver_port_index=None):
        """
        Check Gotthard is enabled.

        Up to 3 checks can be used (all enabled per default):
         * HID++ getInfo state
         * NVS
         * Send requests using Gotthard

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param get_info_state: Flag to enable HID++ getInfo state check - OPTIONAL
        :type get_info_state: ``bool``
        :param nvs: Flag to enable NVS state check - OPTIONAL
        :type nvs: ``bool``
        :param send_requests: Flag to enable Gotthard request sending check - OPTIONAL
        :type send_requests: ``bool``
        :param device_index_on_gotthard: Device index on Gotthard receiver - OPTIONAL (required if get_info_state or
            send_request are set)
        :type device_index_on_gotthard: ``int``
        :param gotthard_receiver_port_index: Gotthard receiver port index - OPTIONAL (required if get_info_state or
            send_request are set)
        :type gotthard_receiver_port_index: ``int``
        """
        if nvs:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Read NVS and check Gotthard is enabled in NVS')
            # ----------------------------------------------------------------------------------------------------------
            expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=True)
            cls.NvsHelper.check_state(test_case, expected_nvs_state)
        # end if

        if (get_info_state or send_requests) and gotthard_receiver_port_index is None:
            test_case.log_warning("Gotthard receiver not available, some checks are skipped",
                                  force_console_print=True)
            return
        # end if

        if get_info_state or send_requests:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Switch to Gotthard receiver')
            # ----------------------------------------------------------------------------------------------------------

            if ChannelUtils.get_receiver_channel(test_case).get_transport_id() in \
                    LogitechReceiverProductId.unifying_pids():
                receiver_port_index = ChannelUtils.get_port_index(test_case=test_case)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f'Turn off current Unifying receiver on port {receiver_port_index}')
                # ------------------------------------------------------------------------------------------------------
                test_case.device.disable_usb_port(receiver_port_index)
            # end if

            ReceiverTestUtils.switch_to_receiver(
                test_case,
                gotthard_receiver_port_index,
                task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)

            try:
                ReceiverTestUtils.GotthardReceiver.init_connection(test_case)
            except TestException as e:
                test_case.log_warning(f'Gotthard receiver initialization failed with {e}. '
                                      'Reset the receiver via usb hub')
                try:
                    ChannelUtils.close_channel(test_case=test_case)
                    LibusbDriver.disable_usb_port(port_index=LibusbDriver.GOTTHARD)
                finally:
                    LibusbDriver.enable_usb_port(port_index=LibusbDriver.GOTTHARD)
                # end try
                ReceiverTestUtils.switch_to_receiver(
                    test_case,
                    gotthard_receiver_port_index,
                    task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
                ReceiverTestUtils.GotthardReceiver.init_connection(test_case)
            # end try

            DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(
                test_case,
                device_index=device_index_on_gotthard,
                port_index=gotthard_receiver_port_index)
        # end if

        if get_info_state:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Check Gotthard is enabled (get info state)')
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=True)
            cls.HIDppHelper.check_state(
                test_case, expected_state, device_index_on_gotthard, gotthard_receiver_port_index)
        # end if

        if send_requests:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Check Gotthard is enabled (send requests)')
            # ----------------------------------------------------------------------------------------------------------
            gotthard_all_features = FeatureSetTestUtils.HIDppHelper.get_features(
                test_case,
                device_index=device_index_on_gotthard,
                port_index=gotthard_receiver_port_index
            )

            gotthard_compliance_features = FeatureSetTestUtils.HIDppHelper.get_features_by_type(
                test_case,
                [FeatureSetTestUtils.FeatureTypes.COMPLIANCE_DEACTIVATABLE],
                device_index=device_index_on_gotthard,
                port_index=gotthard_receiver_port_index
            )

            gotthard_manufacturing_features = FeatureSetTestUtils.HIDppHelper.get_features_by_type(
                test_case,
                [FeatureSetTestUtils.FeatureTypes.MANUFACTURING_DEACTIVATABLE],
                device_index=device_index_on_gotthard,
                port_index=gotthard_receiver_port_index
            )

            not_deactivatable_features = []
            for feature in gotthard_all_features:
                if feature not in gotthard_manufacturing_features and feature not in gotthard_compliance_features:
                    not_deactivatable_features.append(feature)
                # end if
            # end for
            cls.HIDppHelper.check_enabled_features(test_case, not_deactivatable_features)
        # end if
    # end def check_gotthard_enabled

    @classmethod
    def check_gotthard_disabled(cls, test_case, get_info_state=True, nvs=True, send_requests=True,
                                device_index_on_gotthard=None, gotthard_receiver_port_index=None):
        """
        Check Gotthard is disabled.

        Up to 3 checks can be used (all enabled per default):
         * HID++ getInfo state
         * NVS
         * Send requests using Gotthard

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param get_info_state: Flag to enable HID++ getInfo state check - OPTIONAL
        :type get_info_state: ``bool``
        :param nvs: Flag to enable NVS state check - OPTIONAL
        :type nvs: ``bool``
        :param send_requests: Flag to enable Gotthard request sending check - OPTIONAL
        :type send_requests: ``bool``
        :param device_index_on_gotthard: Device index on Gotthard receiver - OPTIONAL (required if get_info_state or
            send_request are set)
        :type device_index_on_gotthard: ``int``
        :param gotthard_receiver_port_index: Gotthard receiver port index - OPTIONAL (required if get_info_state or
            send_request are set)
        :type gotthard_receiver_port_index: ``int``
        """
        if get_info_state:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Check Gotthard is disabled (get info state)')
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=False)
            cls.HIDppHelper.check_state(test_case, expected_state)
        # end if

        if nvs:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Read NVS and check Gotthard is disabled in NVS')
            # ----------------------------------------------------------------------------------------------------------
            expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=False)
            cls.NvsHelper.check_state(test_case, expected_nvs_state)
        # end if

        if send_requests and gotthard_receiver_port_index is None:
            test_case.log_warning("Gotthard receiver not available, some checks are skipped",
                                  force_console_print=True)
            return
        # end if

        if send_requests:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Switch to Gotthard receiver')
            # ----------------------------------------------------------------------------------------------------------
            ReceiverTestUtils.switch_to_receiver(
                test_case,
                gotthard_receiver_port_index,
                task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
            ReceiverTestUtils.GotthardReceiver.init_connection(test_case, assert_connection=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Check Gotthard is disabled')
            # ----------------------------------------------------------------------------------------------------------
            root_feature = RootFactory.create(test_case.config_manager.get_feature_version(
                test_case.f.PRODUCT.FEATURES.IMPORTANT.ROOT))
            get_feature = root_feature.get_feature_cls(deviceIndex=device_index_on_gotthard, featureId=0x0000)
            test_case.assertRaises(AssertionError,
                                   ChannelUtils.send,
                                   test_case=test_case,
                                   report=get_feature,
                                   response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                                   response_class_type=root_feature.get_feature_response_cls)
        # end if
    # end def check_gotthard_disabled
# end class DeviceManageDeactivatableFeaturesAuthTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
