#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.base.receivermanagedeactivatablefeaturesauthutils
:brief:  Helpers for Manage Deactivatable Features (based on authentication mechanism) feature for receiver
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesDisableFeaturesRequest
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesDisableFeaturesResponse
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesEnableFeaturesRequest
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesEnableFeaturesResponse
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesGetInfoRequest
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesGetInfoResponse
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import GetRegisterRequest
from pylibrary.tools.numeral import Numeral
from pytestbox.receiver.base.passwordauthenticationutils import ReceiverPasswordAuthenticationTestUtils
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils
from pytestbox.shared.base.managedeactivatablefeaturesauthutils import SharedManageDeactivatableFeaturesAuthTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverManageDeactivatableFeaturesAuthTestUtils(SharedManageDeactivatableFeaturesAuthTestUtils,
                                                       ReceiverBaseTestUtils):
    """
    Test utils for Manage Deactivatable Features feature with a receiver as a DUT.
    """
    class HIDppHelper(SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper,
                      ReceiverBaseTestUtils.HIDppHelper):
        # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper``

        @classmethod
        def get_feature_interface(cls, test_case):
            # See ``SharedManageDeactivatableFeaturesAuthTestCase.get_feature_interface``
            class FeatureInterface:
                """
                Feature interface
                """
                get_info_cls = ManageDeactivatableFeaturesGetInfoRequest
                get_info_response_cls = ManageDeactivatableFeaturesGetInfoResponse

                disable_features_cls = ManageDeactivatableFeaturesDisableFeaturesRequest
                disable_features_response_cls = ManageDeactivatableFeaturesDisableFeaturesResponse

                enable_features_cls = ManageDeactivatableFeaturesEnableFeaturesRequest
                enable_features_response_cls = ManageDeactivatableFeaturesEnableFeaturesResponse

            # end class
            return FeatureInterface
        # end def get_feature_interface

        @classmethod
        def feature_response_queue(cls, test_case):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.feature_response_queue``
            return test_case.hidDispatcher.receiver_response_queue
        # end def feature_response_queue

        @classmethod
        def get_info(cls, test_case, device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_info``
            get_info_resp = test_case.send_report_wait_response(
                report=ManageDeactivatableFeaturesGetInfoRequest(),
                response_queue=test_case.hidDispatcher.receiver_response_queue,
                response_class_type=ManageDeactivatableFeaturesGetInfoResponse)
            return get_info_resp
        # end def get_info

        @classmethod
        def get_disable_features_req(cls, test_case, disable_all=False, manufacturing=False, compliance=False,
                                     gotthard=False, device_index=None, port_index=None):
            """
            Get disable features with manage deactivatable features (based on authentication mechanism) feature request.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param disable_all: Disable all features - OPTIONAL
            :type disable_all: ``bool``
            :param manufacturing: Disable Manufacturing features - OPTIONAL
            :type manufacturing: ``bool``
            :param compliance: Disable Compliance features - OPTIONAL
            :type compliance: ``bool``
            :param gotthard: Disable Gotthard - OPTIONAL
            :type gotthard: ``bool``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: disableFeatures request
            :rtype: ``ManageDeactivatableFeaturesDisableFeaturesRequest``
            """
            return ManageDeactivatableFeaturesDisableFeaturesRequest(disable_all_bit=disable_all,
                                                                     disable_gothard=gotthard,
                                                                     disable_compliance=compliance,
                                                                     disable_manufacturing=manufacturing)
        # end def get_disable_features_req

        @classmethod
        def disable_features(cls, test_case, disable_all=False, manufacturing=False, compliance=False, gotthard=False,
                             device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features``
            disable_features_resp = test_case.send_report_wait_response(
                report=ManageDeactivatableFeaturesDisableFeaturesRequest(disable_all_bit=disable_all,
                                                                         disable_gothard=gotthard,
                                                                         disable_compliance=compliance,
                                                                         disable_manufacturing=manufacturing),
                response_queue=test_case.hidDispatcher.receiver_response_queue,
                response_class_type=ManageDeactivatableFeaturesDisableFeaturesResponse)
            return disable_features_resp
        # end def disable_features

        @classmethod
        def get_enable_features_req(cls, test_case, enable_all=False, manufacturing=False, compliance=False,
                                    gotthard=False, device_index=None, port_index=None):
            """
            Get enable features with manage deactivatable features (based on authentication mechanism) feature request.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param enable_all: Enable all features - OPTIONAL
            :type enable_all: ``bool``
            :param manufacturing: Enable Manufacturing features - OPTIONAL
            :type manufacturing: ``bool``
            :param compliance: Enable Compliance features - OPTIONAL
            :type compliance: ``bool``
            :param gotthard: Enable Gotthard - OPTIONAL
            :type gotthard: ``bool``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: enableFeatures request
            :rtype: ``ManageDeactivatableFeaturesEnableFeaturesRequest``
            """
            return ManageDeactivatableFeaturesEnableFeaturesRequest(enable_all_bit=enable_all,
                                                                    enable_gothard=gotthard,
                                                                    enable_compliance=compliance,
                                                                    enable_manufacturing=manufacturing)
        # end def get_enable_features_req

        @classmethod
        def enable_features(cls, test_case, enable_all=False, manufacturing=False, compliance=False, gotthard=False,
                            start_session=True, device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features``
            if start_session and (manufacturing or enable_all):
                # Note: Complaince and Gothard are not yet supported by receiver. Enable them when supported.
                ReceiverPasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
                    test_case=test_case,
                    account_name=ReceiverPasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value)
            # end if
            enable_features_req = ManageDeactivatableFeaturesEnableFeaturesRequest(
                enable_all_bit=enable_all,
                enable_gothard=gotthard,
                enable_compliance=compliance,
                enable_manufacturing=manufacturing)
            enable_features_resp = test_case.send_report_wait_response(
                report=enable_features_req,
                response_queue=test_case.hidDispatcher.receiver_response_queue,
                response_class_type=ManageDeactivatableFeaturesEnableFeaturesResponse)

            return enable_features_resp
        # end def enable_features

        @classmethod
        def get_features(cls, test_case, manufacturing=False, compliance=False, gotthard=False):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_features``
            manufacturing_features = None
            compliance_features = None
            gotthard_features = None
            if manufacturing:
                manufacturing_features = [
                    Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS,
                    Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
                    Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
                    Hidpp1Data.Hidpp1RegisterAddress.SET_LTK_KEY,
                    Hidpp1Data.Hidpp1RegisterAddress.SET_IRK_KEY_CENTRAL,
                    Hidpp1Data.Hidpp1RegisterAddress.SET_IRK_KEY_PERIPHERAL,
                    Hidpp1Data.Hidpp1RegisterAddress.SET_CSRK_KEY_CENTRAL,
                    Hidpp1Data.Hidpp1RegisterAddress.SET_CSRK_KEY_PERIPHERAL,
                    Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
                ]
            # end if
            if compliance:
                # Not supported yet
                compliance_features = None
            # end if
            if gotthard:
                # Not supported yet
                gotthard_features = None
            # end if
            return manufacturing_features, compliance_features, gotthard_features
        # end def get_features

        @classmethod
        def check_enabled_features(cls, test_case, features, device_index=None, port_index=None):
            # See ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_enabled_features``
            asserted_once = False
            for feature_reg_addr in features:
                request_cls = cls.get_check_enabled_request_cls(feature_reg_addr)
                if request_cls is not None:
                    request = request_cls()
                    test_case.send_report_to_device(report=request, timeout=1)

                    test_case.assertListEqual(
                        test_case.clean_message_type_in_queue(
                            test_case.hidDispatcher.receiver_error_message_queue, Hidpp1ErrorCodes),
                        [],
                        f"No error should be raised when sending {hex(feature_reg_addr)} read command")
                    # TODO (Martin Cryonnet): clean received message
                    asserted_once = True
                # end if
            # end for
            if not asserted_once:
                test_case.log_warning("No feature available to check the current features set",
                                      force_console_print=True)
            # end if
        # end check_enabled_features

        @classmethod
        def check_disabled_features(cls, test_case, features, device_index=None, port_index=None):
            # ``SharedManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_disabled_features``
            asserted_once = False
            for feature_reg_addr in features:
                request_cls = cls.get_check_enabled_request_cls(feature_reg_addr)
                if request_cls is not None:
                    request = request_cls()
                    err_resp = test_case.send_report_wait_response(
                        report=request,
                        response_queue=test_case.hidDispatcher.receiver_error_message_queue,
                        response_class_type=Hidpp1ErrorCodes)
                    assert isinstance(err_resp, Hidpp1ErrorCodes)
                    cls.check_hidpp10_error_message(test_case,
                                                    err_resp,
                                                    sub_id=int(Numeral(request.sub_id)),
                                                    register_address=int(Numeral(request.address)),
                                                    error_codes=[Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])
                    asserted_once = True
                # end if
            # end for
            if not asserted_once:
                test_case.log_warning("No feature available to check the current features set",
                                      force_console_print=True)
            # end if
        # end def check_disabled_features

        @classmethod
        def get_check_enabled_request_cls(cls, feature_reg_addr):
            """
            Get request class to be sent to check if the feature is enabled

            Notes:
             * Currently, not all features are supported. It is possible to extend the coverage.
             * Some features can not be used for this kind of check because it could change the state of the device (
             i.e., Reset should not be used)

            :param feature_reg_addr: Feature Register Address
            :type feature_reg_addr: ``int``
            """
            supported_for_check = [
                Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
            ]
            request_cls = None

            if feature_reg_addr in supported_for_check:
                for get_sub_id in [Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                                   Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                                   Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER]:
                    request_cls = Hidpp1Model.get_message_cls(
                        sub_id=get_sub_id, message_type="request", address=feature_reg_addr)
                    if request_cls is not None and request_cls not in [GetRegisterRequest, GetLongRegisterRequest]:
                        break
                    # end if
                # end for
            # end if

            if request_cls is not None:
                assert issubclass(request_cls, Hidpp1Message), "Request class should be a Hidpp1Message"
            # end if

            return request_cls
        # end def get_check_enabled_request
    # end class HIDppHelper
# end class ReceiverManageDeactivatableFeaturesAuthTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
