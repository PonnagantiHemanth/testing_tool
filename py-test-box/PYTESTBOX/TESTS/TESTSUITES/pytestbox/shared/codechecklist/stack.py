#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.codechecklist.stack
:brief: Shared Stack tests
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/08/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.memoryutils import SharedMemoryTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedStackTestCase(CommonBaseTestCase, ABC):
    """
    Validate Stack management
    """
    def setUp(self):
        # See ``CommonBaseTestCase.setUp``

        # Start with super setUp()
        super().setUp()

        # Stop Task executor
        ChannelUtils.close_channel(test_case=self, close_associated_channel=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.device_memory_manager.read_nvs(backup=True)
        if len(self.device_memory_manager.get_chunks_by_name(chunk_name='NVS_BLE_LAST_GAP_ADDR_USED')) == 0:
            DeviceBaseTestUtils.NvsHelper.force_last_gap_address(test_case=self)
        # end if
        self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
            test_case=self, memory_manager=self.device_memory_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Initialize the full stack with a pattern")
        # --------------------------------------------------------------------------------------------------------------
        SharedMemoryTestUtils.StackHelper.initialize_stack_area(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Wait for the DUT to be reconnected")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
            test_case=self,
            device_connection_optional=self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE)
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
    # end def setUp

    def tearDown(self):
        # See ``CommonBaseTestCase.tearDown``
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                self.device_memory_manager.load_nvs(backup=True)
            # end if
        # end with
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(test_case=self, text="Restore debugger cache settings")
            # ----------------------------------------------------------------------------------------------------------
            SharedMemoryTestUtils.StackHelper.restore_cache_settings(test_case=self)

            ChannelUtils.open_channel(test_case=self)
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with
        super().tearDown()
    # end def tearDown

    def execute_scenario(self):
        """
        Emulate a communication with the device.
        """
        raise NotImplementedError('users must define execute_scenario to use this base class')
    # end def execute_scenario

    @features('StackDepth')
    @level('Functionality')
    @services('Debugger')
    def test_stack_verification(self):
        """
        Verify STACK usage using a special pattern in RAM for stack usage.
        """
        self.execute_scenario()

        # Stop Task executor
        ChannelUtils.close_channel(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump stack after an HID++ request exchange')
        # --------------------------------------------------------------------------------------------------------------
        stack = SharedMemoryTestUtils.StackHelper.dump_stack_area(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check stack depth')
        # --------------------------------------------------------------------------------------------------------------
        margin = SharedMemoryTestUtils.StackHelper.check_stack_depth(test_case=self, stack=stack)
        LogHelper.log_info(self, f'Stack verification: {margin} unused bytes over {len(stack)}')

        self.testCaseChecked("FUN_STACK_0001")
    # end def test_stack_verification
# end class SharedStackTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
