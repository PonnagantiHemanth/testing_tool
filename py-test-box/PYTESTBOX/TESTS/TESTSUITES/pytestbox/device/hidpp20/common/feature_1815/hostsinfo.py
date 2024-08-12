#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1815.hostsinfo
:brief: HID++ 2.0 Hosts Info test case
:author: Christophe Roquebert
:date: 2021/03/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.hostsinfo import HostsInfo
from pyhid.hidpp.features.common.hostsinfo import HostsInfoFactory
from pyhid.hidpp.hidpp1.registers.uniqueidentifier import GetUniqueIdentifierRequest
from pyhid.hidpp.hidpp1.registers.uniqueidentifier import GetUniqueIdentifierResponse
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HostsInfoTestCase(DeviceBaseTestCase):
    """
    Validates Hosts Info TestCases in Application mode
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature 0x1815 index')
        # ---------------------------------------------------------------------------
        self.feature_1815_index = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, HostsInfo.FEATURE_ID)
        self.feature_1815 = HostsInfoFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.HOSTS_INFO))

        if isinstance(self.current_channel, ThroughReceiverChannel):
            # ---------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Get receiver unique identifier')
            # ---------------------------------------------------------------------------
            get_unique_identifier = GetUniqueIdentifierRequest()
            get_unique_identifier_response = ChannelUtils.send(
                test_case=self,
                channel=self.current_channel.receiver_channel,
                report=get_unique_identifier,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=GetUniqueIdentifierResponse)
            self.receiver_serial_numbers = [HexList(get_unique_identifier_response.unique_identifier), None, None]
        else:
            self.receiver_serial_numbers = [None, None, None]
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        if self.post_requisite_reload_nvs:
            # --------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Reload initial NVS")
            # --------------------------------------------------------------------------
            CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            self.post_requisite_reload_nvs = False
        # end if
        super().tearDown()
    # end def tearDown
# end class HostsInfoTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
