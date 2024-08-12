#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.module_test
:brief: Kosmos Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from typing import Iterable
from unittest import skipUnless
from unittest.mock import NonCallableMock
from unittest.mock import patch

from math import ceil

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.fpgatransport import UnderrunPayloadError
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.error import KosmosFatalError
from pyraspi.services.kosmos.module.module import BufferModuleBaseClass
from pyraspi.services.kosmos.module.module import DownloadModuleBaseClass
from pyraspi.services.kosmos.module.module import ModuleBaseClass
from pyraspi.services.kosmos.module.module import ModuleStatusSanityChecksError
from pyraspi.services.kosmos.module.module import StatusResetModuleBaseClass
from pyraspi.services.kosmos.module.module import UploadModuleBaseClass
from pyraspi.services.kosmos.test.common_test import KosmosCommonTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def require_kosmos_device(device, min_count=1):
    """
    Test decorator: Skip a test if the required Kosmos hardware is not present in the Kosmos `DeviceTree`.

    The device shall be one from `DeviceName` or from `DeviceFamilyName`. In the latter case, at least one `DeviceName`
    from the family should be present in the Kosmos `DeviceTree` to satisfy the condition.

    If more than one device instance is required, set `min_count` parameter.

    :param device: Required Kosmos device type
    :type device: ``DeviceName or DeviceFamilyName``
    :param min_count: Minimum count of emulator required; defaults to one - OPTIONAL
    :type min_count: ``int``

    :return: Decorated class or method
    :rtype: ``Callable``
    """
    return skipUnless(condition=Kosmos.discover_emulator(emulation_type=device, emulator_min_count=min_count),
                      reason='Test was skipped because the required Kosmos hardware is not present: '
                             f'{min_count} × {repr(device)}.')
# end def require_kosmos_device


class AbstractTestClass:
    """
    This class is used to wrap Abstract Module Test classes, so that they cannot be not automatically get discovered
    and executed by test executors (unittest, pytest...).

    This is the best way so far, in order to use `unittest.TestCase` along with `abc.ABCMeta` and inheritance.
    Refer to https://stackoverflow.com/a/25695512 and https://stackoverflow.com/a/35304339.
    """

    class ModuleInterfaceTestCase(KosmosCommonTestCase, metaclass=ABCMeta):
        """
        Kosmos ModuleBaseClass Test Class.
        """

        # Reference to the module instance to be tested, set via setUpClass()
        module: ModuleBaseClass = None

        @classmethod
        def setUpClass(cls):
            """
            Set up the Module to be tested.
            """
            super().setUpClass()
            cls.module = cls._get_module_under_test()
            assert cls.module, 'Module is not present in the Device Tree'
            assert isinstance(cls.module, ModuleBaseClass), [c.__name__ for c in cls.module.__class__.mro()]
        # end def setUpClass

        @classmethod
        @abstractmethod
        def _get_module_under_test(cls):
            """
            Return the module instance to be tested.

            :return: The module instance to be tested.
            :rtype: ``ModuleBaseClass``
            """
            raise NotImplementedAbstractMethodError()
        # end def _get_module_under_test
    # end class ModuleInterfaceTestCase

    class StatusResetModuleInterfaceTestCase(ModuleInterfaceTestCase, metaclass=ABCMeta):
        """
        Kosmos StatusResetModuleBaseClass Test Class.
        """

        # Reference to the module instance to be tested, set via setUpClass()
        module: StatusResetModuleBaseClass = None

        @classmethod
        def setUpClass(cls):
            """
            Set up the Module to be tested.
            """
            super().setUpClass()
            assert isinstance(cls.module, StatusResetModuleBaseClass), [c.__name__ for c in cls.module.__class__.mro()]
        # end def setUpClass

        @abstractmethod
        def test_status(self):
            """
            Call status() method
            """
            raise NotImplementedAbstractMethodError()
        # end def test_status

        @patch('pyraspi.services.kosmos.module.module.StatusResetModuleBaseClass.is_status_reply_valid')
        def test_status_sanity_checks(self, mock_is_status_reply_valid):
            """
            Validate ``StatusResetModuleBaseClass.status()`` error raising: ModuleStatusSanityChecksError

            :param mock_is_status_reply_valid: Test Mock of function ``StatusResetModuleBaseClass.is_status_reply_valid``
            :type mock_is_status_reply_valid: ``NonCallableMock``
            """
            expected_error_list = ['[MOCK] This is a mock error', '[-_-] Oh no, another error!']
            mock_is_status_reply_valid.return_value = expected_error_list

            try:
                # 1st case: sanity_checks=True, should raise the exception
                with self.assertRaises(ModuleStatusSanityChecksError) as context:
                    self.module.status(sanity_checks=True)
                # end with
                self.assertTrue(KosmosFatalError.has_exception())
                self.assertEqual('\n'.join(expected_error_list), str(context.exception))
                mock_is_status_reply_valid.assert_called_once()

                # 2nd case: sanity_checks=False, should not raise any exception
                self.module.status(sanity_checks=False)
                mock_is_status_reply_valid.assert_called_once()
            finally:
                KosmosFatalError.clear_exception()
            # end try
        # end def test_status_sanity_checks

        @abstractmethod
        def test_reset_module(self):
            """
            Call reset_module() method
            """
            raise NotImplementedAbstractMethodError()
        # end def test_reset_module

        @patch('pyraspi.services.kosmos.module.module.StatusResetModuleBaseClass.is_reset_reply_valid')
        def test_reset_module_sanity_checks(self, mock_is_reset_reply_valid):
            """
            Validate ``StatusResetModuleBaseClass.reset_module()`` error raising: ModuleStatusSanityChecksError

            :param mock_is_reset_reply_valid: Test Mock of function ``StatusResetModuleBaseClass.is_reset_reply_valid``
            :type mock_is_reset_reply_valid: ``NonCallableMock``
            """
            expected_error_list = ['[MOCK] This is a mock error', '[-_-] Oh no, another error!']
            mock_is_reset_reply_valid.return_value = expected_error_list

            try:
                # 1st case: sanity_checks=True, should raise the exception
                with self.assertRaises(ModuleStatusSanityChecksError) as context:
                    self.module.reset_module(sanity_checks=True)
                # end with
                self.assertTrue(KosmosFatalError.has_exception())
                self.assertEqual('\n'.join(expected_error_list), str(context.exception))
                mock_is_reset_reply_valid.assert_called_once()

                # 2nd case: sanity_checks=False, should not raise any exception
                self.module.reset_module(sanity_checks=False)
                mock_is_reset_reply_valid.assert_called_once()
            finally:
                KosmosFatalError.clear_exception()
            # end try
        # end def test_reset_module_sanity_checks
    # end class StatusResetModuleInterfaceTestCase

    class BufferModuleInterfaceTestCase(StatusResetModuleInterfaceTestCase, metaclass=ABCMeta):
        """
        Kosmos BufferModuleBaseClass Test Class.
        """

        # Reference to the module instance to be tested, set via setUpClass()
        module: BufferModuleBaseClass

        @classmethod
        def setUpClass(cls):
            """
            Set up the Module to be tested.
            """
            super().setUpClass()
            assert isinstance(cls.module, BufferModuleBaseClass), [c.__name__ for c in cls.module.__class__.mro()]
        # end def setUpClass

        def test_status(self):
            """
            Call status() method.
            """
            status = self.module.status()
            self.assertEqual(0, status.buffer_count)
            if self.module.settings.fifo_size is not None:
                self.assertEqual(0, status.fifo_count)
            # end if
        # end def test_status

        def test_reset_module(self):
            """
            Call reset_module() method.
            """
            status = self.module.reset_module()
            self.assertEqual(0, status.buffer_count)
            if self.module.settings.fifo_size is not None:
                self.assertEqual(0, status.fifo_count)
            # end if
        # end def test_reset_module
    # end class BufferModuleInterfaceTestCase

    class UploadModuleInterfaceTestCase(BufferModuleInterfaceTestCase, metaclass=ABCMeta):
        """
        Kosmos UploadModuleBaseClass Test Class.
        """

        # Reference to the module instance to be tested, set via setUpClass()
        module: UploadModuleBaseClass

        @classmethod
        def setUpClass(cls):
            """
            Set up the Module to be tested.
            """
            super().setUpClass()
            assert isinstance(cls.module, UploadModuleBaseClass), [c.__name__ for c in cls.module.__class__.mro()]
        # end def setUpClass

        def test_buffer(self):
            """
            Validate the following methods:
             - append()
             - extend()
             - length()
             - messages()
             - send()
             - clear()
            """

            # Get data types as a list
            if not isinstance(self.module.settings.data_type, Iterable):
                data_types = [self.module.settings.data_type]
            else:
                data_types = list(self.module.settings.data_type)
            # end if

            # Compute the maximum number of message to (almost) fill the remote buffer
            dataset_repeat = (self.module.settings.buffer_size - 1) // (2 * len(data_types))

            # Fill local module instruction buffer
            instruction_count = 0
            for _ in range(dataset_repeat):
                instructions = [data_type() for data_type in data_types]

                # Fill instruction buffer using append()
                for instruction in instructions:
                    self.module.append(instruction)
                # end for
                instruction_count += len(data_types)
                self.assertEqual(instruction_count, self.module.length())

                # Fill instruction buffer using extend()
                self.module.extend(instructions)
                instruction_count += len(data_types)
                self.assertEqual(instruction_count, self.module.length())
            # end for

            # Validate transformation of local instruction buffer into list of MessageFrames
            tx_frames = self.module.messages()
            instructions_per_payload = self.module.settings.msg_cmd_write_max - self.module.settings.msg_cmd_write_one + 1
            self.assertEqual(ceil(instruction_count / instructions_per_payload), len(tx_frames))
            data_index = 0
            for _ in range(dataset_repeat):
                for _ in range(2):  # one loop for append() and another for extend()
                    for data_type in data_types:
                        frame_index = data_index // instructions_per_payload
                        payload_index = data_index % instructions_per_payload
                        payload = getattr(tx_frames[frame_index].frame.payload, self.module.settings.msg_payload_name)
                        data = payload[payload_index]

                        self.assertEqual(0, sum(bytes(data)), msg=f'{data_index} {data_type}')
                        data_index += 1
                    # end for
                # end for
            # end for
            self.assertEqual(data_index, instruction_count)

            self.module.clear()
            self.module.reset_module()
        # end def test_buffer
    # end class UploadModuleInterfaceTestCase

    class DownloadModuleInterfaceTestCase(StatusResetModuleInterfaceTestCase, metaclass=ABCMeta):
        """
        Kosmos DownloadModuleBaseClass Test Class.
        """

        # Reference to the module instance to be tested, set via setUpClass()
        module: DownloadModuleBaseClass

        @classmethod
        def setUpClass(cls):
            """
            Set up the Module to be tested.
            """
            super().setUpClass()
            assert isinstance(cls.module, DownloadModuleBaseClass), [c.__name__ for c in cls.module.__class__.mro()]
        # end def setUpClass

        def test_download(self):
            """
            Validate the following methods:
             - download
            """
            # Empty read
            status = self.module.status()
            self.assertEqual(0, status.buffer_count, status)
            self.assertEqual([], self.module.download())

            # Requesting more data than the remote buffer can hold
            with self.assertRaises(AssertionError):
                self.module.download(count=self.module.size())
            # end with

            # Requesting data, expect remote buffer underrun message reply
            with self.assertRaises(UnderrunPayloadError):
                self.module.download(count=1)
            # end with
        # end def test_download
    # end class DownloadModuleInterfaceTestCase
# end class AbstractTestClass

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
