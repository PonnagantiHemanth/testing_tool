#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.error
:brief: Kosmos Fatal Error class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/04/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from typing import List

# ------------------------------------------------------------------------------
# global variables
# ------------------------------------------------------------------------------

# Global variable listing the current exceptions fatal to the continuation of Kosmos Emulator run
_global_kosmos_fatal_error_exceptions: List[Exception] = []


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosFatalError:
    """
    Namespace class for function handling the state of Kosmos Fatal Error Exceptions.
    This class is not meant to be instantiated.
    """
    @staticmethod
    def register_exception(exception: Exception):
        """
        Register the given exception in the global list of exception that will trigger a Kosmos Microblaze reset.

        Do not call this method directly. Instead, make your exception class derive from `KosmosFatalErrorException`.
        See to `KosmosFatalErrorException.__init__` method.

        :param exception: exception instance
        :type exception: ``Type[Exception]``
        """
        global _global_kosmos_fatal_error_exceptions
        _global_kosmos_fatal_error_exceptions.append(exception)
    # end def register_exception

    @staticmethod
    def has_exception():
        """
        Return True if one or more exceptions has been registered.

        :return: True if one or more exceptions has been registered, False otherwise
        :rtype: ``bool``
        """
        global _global_kosmos_fatal_error_exceptions
        return len(_global_kosmos_fatal_error_exceptions) > 0
    # end def has_exception

    @staticmethod
    def get_exception():
        """
        Return the list of exceptions that were registered.

        :return: list of exceptions that were registered
        :rtype: ``List[Exception]``
        """
        global _global_kosmos_fatal_error_exceptions
        return _global_kosmos_fatal_error_exceptions
    # end def get_exception

    @staticmethod
    def clear_exception():
        """
        Clear the list of exceptions.
        To be called once the Kosmos Microblaze reset was reset.
        """
        global _global_kosmos_fatal_error_exceptions
        _global_kosmos_fatal_error_exceptions.clear()
    # end def clear_exception
# end class KosmosFatalError


class KosmosFatalErrorException(Exception, metaclass=ABCMeta):
    """
    Abstract base class for Kosmos Fatal Error Exceptions.

    Rationale: any exception class derived from `KosmosFatalError`, that is raised during a test run, will trigger a
    Kosmos Microblaze CPU reset during test tear down.

    Refer to error handling code:
     - pyraspi.services.kosmos.test.common_test.KosmosCommonTestCase.tearDown
     - pytestbox.base.basetest.CommonBaseTestCase.kosmos_tear_down

    Examples of Exception classes derived from `KosmosFatalError`:
     - pyraspi.bus.spi.SpiTransactionError
     - pyraspi.services.kosmos.fpgatransport.FpgaTransportError
     - pyraspi.services.kosmos.module.sequencer.SequencerError
    """

    def __init__(self, *args):
        """
        :param args: Positional arguments
        :type args: ``tuple[Any]``
        """
        super().__init__(*args)
        KosmosFatalError.register_exception(self)
    # end def __init__
# end class KosmosFatalErrorException

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
