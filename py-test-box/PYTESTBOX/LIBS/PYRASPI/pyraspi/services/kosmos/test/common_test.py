#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.common_test
:brief: KOSMOS test common utilities
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/10/15
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from time import sleep
from unittest import TestCase
from unittest import expectedFailure
from unittest import skipIf
from warnings import catch_warnings
from warnings import warn

from pyraspi.bus.spi import SpiTransactionTimeoutError
from pyraspi.raspi import UNSUPPORTED_SETUP_ERR_MSG
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.module.fpga import CPU_BOOT_TIME_S
from pyraspi.services.kosmos.module.error import KosmosFatalError
from pyraspi.services.kosmos.module.module import StatusResetModuleBaseClass
from pyraspi.services.kosmos.module.module import UploadModuleBaseClass
from pyraspi.services.kosmos.module.sequencer import SequencerError
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA_CMD_HW_REV_READ
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST_CMD_BREAKPOINT


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@skipIf(not Daemon.is_host_kosmos(), UNSUPPORTED_SETUP_ERR_MSG)
class KosmosCommonTestCase(TestCase):
    """
    Common Kosmos Unitary Test class.
    """
    # Top-level Kosmos instance to be tested
    kosmos: Kosmos

    # Enable verbose prints, for debug
    VERBOSE: bool = False

    # Internal flag: set to True to perform a Microblaze CPU soft-reset during Test's teardown() method
    _soft_reset_microblaze_during_teardown: bool

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos.

        :raise ``AssertionError``: Microblaze Core failed to restart after being reset
        """
        super().setUpClass()

        cls.kosmos = Kosmos.get_instance()

        # Soft-reset the Microblaze before starting the test suite
        try:
            cls.kosmos.dt.fpga.soft_reset_microblaze()
        except SpiTransactionTimeoutError:
            # Un-register the current reference to Kosmos instance, so that the associated threads can be stopped.
            cls.kosmos = None
            raise AssertionError('Microblaze Core failed to restart after being reset.')
        # end try

        # Re-initialize kosmos pods configuration after the soft reset
        cls.kosmos.pods_configuration.init_pods(device_tree=cls.kosmos.dt)
    # end def setUpClass

    def setUp(self):
        """
        Prepare the Kosmos hardware/software interfaces before executing a test case.

        :raise ``AssertionError``: The test case cannot be started because the Global Error Flag is raised
        """
        super().setUp()

        # Set this flag to soft-reset the Microblaze core during tearDown()
        self._soft_reset_microblaze_during_teardown = False

        # Validate Global Error Flag is not raised before starting test method
        if self.kosmos.dt.fpga.is_global_error_flag_raised():
            self.fail(msg=f'The test case "{self.test_name}" cannot be started '
                          'because the Global Error Flag is raised.')
        # end if

        # Validate Sequencer state before starting the test method
        status = self.kosmos.dt.sequencer.status()
        error_list = self.kosmos.dt.sequencer.is_sequencer_state_clean(status)
        if error_list:
            warn('Sequencer state is not clean.\n'
                 f'Microblaze will be reset before starting Test Case method <{self.test_name}>.\n'
                 'Error details:\n' + '\n'.join(error_list))
            # Soft-reset the Microblaze before starting the test method
            self.kosmos.dt.fpga.soft_reset_microblaze()
        # end if
    # end def setUp

    def tearDown(self):
        """
        Cleanup the Kosmos hardware/software interfaces after having executed a test case
        and before starting a new one.

        :raise ``AssertionError``: Issue detected in test case teardown
        """
        # Check if Kosmos Fatal Errors were raised during the previous test run
        if KosmosFatalError.has_exception():
            self._soft_reset_microblaze_during_teardown = True
            exceptions_names = ', '.join(f'<{exception.__class__.__name__}>'
                                         for exception in KosmosFatalError.get_exception())
            warn(f'{exceptions_names} was raised during the test case method <{self.test_name}>.\n'
                 '==> As a consequence, the Microblaze core will be soft-reset before continuing the test suite.')
        # end if

        # Check if Reset was requested
        if self._soft_reset_microblaze_during_teardown:
            # Soft-reset the Microblaze
            self.kosmos.dt.fpga.soft_reset_microblaze()
            # Reset flags
            self._soft_reset_microblaze_during_teardown = False
            KosmosFatalError.clear_exception()
        # end if

        # Re-initialize kosmos pods configuration after the soft reset
        self.kosmos.pods_configuration.init_pods(device_tree=self.kosmos.dt)

        # Note to developers: We always want to execute cleanup sequence, even if status errors are detected.
        # Log all errors for each module, then raise an exception only once in teardown().
        # Finally, force-reset local and remote modules.
        error_list = []

        # Assess if Global Error Flag was raised during test
        if self.kosmos.dt.fpga.is_global_error_flag_raised():
            error_list.append(
                'The Global Error Flag was raised during the execution of the test method '
                f'<{self.test_name}>.')
            self.kosmos.dt.fpga.reset_global_error_flag()
        # end if

        # Assess local modules status
        for name, module in self.kosmos.dt.flatmap.items():
            if isinstance(module, UploadModuleBaseClass):
                buffer_len = module.length()
                if buffer_len > 0:
                    error_list.append(
                        f'[{name}] local instruction buffer should be empty by the end of '
                        f'test method <{self.test_name}>. Got buffer_len={buffer_len}.')
                # end if
            # end if
        # end for

        # Assess remote modules status
        status = self.kosmos.dt.sequencer.status(sanity_checks=False)
        error_list.extend(self.kosmos.dt.sequencer.is_sequencer_state_clean(status))

        # Validate above status assessments
        try:
            if error_list:
                self.fail(msg=f'Issue detected in test case teardown.\n' + '\n'.join(error_list))
            # end if
        finally:
            # Abort any running sequence then clear modules consuming instructions or producing data
            self.kosmos.clear(force=True)
        # end try

        super().tearDown()
    # end def tearDown

    @property
    def test_name(self):
        """
        Return the full name of the current Test Case being executed (also valid in ``setUp()`` and ``tearDown()``).

        :return: full name of the current Test Case being executed.
        :rtype: ``str``
        """
        return f'{self.__module__}.{self.__class__.__name__}.{self._testMethodName}'
    # end def property getter test_name

    def printd(self, *args, **kwargs):
        """
        Debug Print method, enabled only if `self.VERBOSE` is True.

        :param args: list of values
        :type args: ``tuple[Any]``
        :param kwargs: dict of values
        :type kwargs: ``dict[str, Any]``
        """
        if self.VERBOSE:
            print(*args, **kwargs)
        # end if
    # end def printd
# end class KosmosCommonTestCase


class KosmosCommonTestCaseTestCase(KosmosCommonTestCase):
    """
    Unitary Test for KosmosCommonTestCase class (i.e. test the test).
    """

    # internal test flags
    _expect_reset_warning_message_in_teardown: bool
    _expect_issue_detected_in_teardown: bool

    def setUp(self):
        """
        Setup TestCase
        """
        super().setUp()

        # Ensure microblaze is up and alive
        self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ)

        # Reset flags
        self._expect_reset_warning_message_in_teardown = False
        self._expect_issue_detected_in_teardown = False
    # end def setUp

    def tearDown(self):
        """
        Validates that the method `KosmosCommonTestCase.tearDown()` has detected the exceptions raised by the
        test cases of the present test class.

        Rationale: After an exception was detected in tearDown(), the MicroBlaze core should have been reset,
                   and a warning message been printed on the console.

        :raise ``AssertionError``: Unexpected Warning
        """
        if self._expect_reset_warning_message_in_teardown:
            # Force clearing local PES buffer, because this is not what we want to test here.
            self.kosmos.dt.pes.clear()

            # Expect to catch a specific warning
            # Note this will intercept the warning and prevent it from being displayed
            with self.assertWarnsRegex(UserWarning,
                                       expected_regex=r'the Microblaze core will be soft-reset'):
                if self._expect_issue_detected_in_teardown:
                    with self.assertRaisesRegex(self.failureException,
                                                expected_regex=r'Issue detected in test case teardown'):
                        super().tearDown()
                    # end with
                else:
                    super().tearDown()
                # end if
            # end with
        else:
            # Expect to not catch any warning
            with catch_warnings(record=True) as warning_list:
                super().tearDown()
            # end with
            self.assertEqual(0, len(warning_list),
                             msg='Unexpected Warning:\n' + '\n'.join([str(w) for w in warning_list]))
        # end if

        # Ensure microblaze is up and alive
        self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ)
    # end def tearDown

    @expectedFailure
    def test_teardown_detect_sequencererror(self):
        """
        Validate handling of ``SequencerError`` exception by ``KosmosCommonTestCase.tearDown()`` method.

        Approach: Raising ``SequencerError`` exception on purpose.
        Expectation: the ``tearDown()`` method will detect the exception and trigger soft-reset of the Microblaze.
        Note: The test code will fail on purpose. The @expectedFailure decorator should make the test PASS.

        :raise ``SequencerError``: This exception is raised on purpose for this test
        """
        self._expect_reset_warning_message_in_teardown = True

        raise SequencerError('This exception was raised on purpose')
    # end def test_teardown_detect_sequencererror

    @expectedFailure
    def test_teardown_skip_other_exception(self):
        """
        Validate that ``KosmosCommonTestCase.tearDown()`` method does not catch exceptions other than specified.

        Approach: Raising ``Exception`` exception on purpose.
        Expectation: the ``tearDown()`` method skips the exception and does not trigger soft-reset of the Microblaze.
        Note: The test code will fail on purpose. The @expectedFailure decorator should make the test PASS.

        :raise ``Exception``: This exception is raised on purpose for this test
        """
        self._expect_reset_warning_message_in_teardown = False

        raise Exception('This exception was raised on purpose')
    # end def test_teardown_skip_other_exception

    @expectedFailure
    def test_teardown_detect_exception_in_subtest(self):
        """
        Validate exception detection by ``KosmosCommonTestCase.tearDown()`` method,
        when the test case method uses ``subTest()`` context manager.

        Approach: Raising ``TimeoutError`` exception on purpose, from inside a subTest block.
        Expectation: the ``tearDown()`` method will detect the exception and trigger soft-reset of the Microblaze.
        Note: The test code will fail on purpose. The @expectedFailure decorator should make the test PASS.

        :raise ``SpiTransactionTimeoutError``: This exception is raised on purpose for this test
        """
        self._expect_reset_warning_message_in_teardown = True

        for n in range(3):
            with self.subTest(n=n):
                raise SpiTransactionTimeoutError('This exception was raised on purpose')
            # end with
        # end for
    # end def test_teardown_detect_exception_in_subtest

    @expectedFailure
    def test_teardown_detect_sequencer_timeout(self):
        """
        Validate handling of ``SequencerTimeoutError`` exception by ``KosmosCommonTestCase.tearDown()`` method.

        Approach: Trigger the raise of ``SequencerTimeoutError``.
        Expectation: the ``tearDown()`` method will detect the exception and trigger soft-reset of the Microblaze.
        Note: The test code will fail on purpose. The @expectedFailure decorator should make the test PASS.
        """
        self._expect_reset_warning_message_in_teardown = True

        # Prepare test sequence
        self.kosmos.pes.delay(delay_s=10)
        # Upload and execute test sequence
        self.kosmos.sequencer.play_sequence(timeout=1)
    # end def test_teardown_detect_sequencer_timeout

    @expectedFailure
    def test_teardown_detect_spi_transaction_error(self):
        """
        Validate handling of ``SpiTransactionError`` exception by ``KosmosCommonTestCase.tearDown()`` method.

        Approach: Trigger the raise of ``SpiTransactionError``.
        Expectation: the ``tearDown()`` method will detect the exception and trigger soft-reset of the Microblaze.
        Note: The test code will fail on purpose. The @expectedFailure decorator should make the test PASS.
        """
        self._expect_reset_warning_message_in_teardown = True

        # Force a Microblaze CPU soft-reset without waiting for it to finnish rebooting.
        # The access to an internal method is intentional, as this raw feature is not exposed to the user.
        fpga_subclass: StatusResetModuleBaseClass = super(self.kosmos.dt.fpga.__class__, self.kosmos.fpga)

        # Send reset message
        try:
            # This should raise SpiTransactionError, as communication gets interrupted.
            fpga_subclass._reset_module()
        finally:
            # Wait for the CPU to start and initialize, before letting the test continue
            sleep(CPU_BOOT_TIME_S)

            # In any case, force a clean reboot using the Global Error line
            self.kosmos.dt.fpga.soft_reset_microblaze()
        # end try
    # end def test_teardown_detect_spi_transaction_error

    def test_test_name(self):
        """
        Validate ``self.test_name`` method
        """
        self.assertTrue(self.test_name.endswith(r'common_test.KosmosCommonTestCaseTestCase.test_test_name'),
                        msg=self.test_name)
    # end def test_test_name

    @expectedFailure
    def test_mb_breakpoint(self):
        """
        Check if the Test Class teardown is properly recovering after the microblaze triggered a breakpoint.

        This test case relates to ``pyraspi.services.kosmos.test.reset_test.KosmosResetTestCase``.
        """
        # Trigger a breakpoint on purpose in the microblaze, expects an SPI timeout exception
        with self.assertRaises(SpiTransactionTimeoutError) as cm:
            self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_TEST, MSG_ID_TEST_CMD_BREAKPOINT)
        # end with
        expected_exception = cm.exception

        # Raise the exception, which should be handled in KosmosCommonTestCase.tearDown() by resetting the microblaze
        self._expect_reset_warning_message_in_teardown = True
        self._expect_issue_detected_in_teardown = True
        raise expected_exception
    # end def test_mb_breakpoint
# end class KosmosCommonTestCaseTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
