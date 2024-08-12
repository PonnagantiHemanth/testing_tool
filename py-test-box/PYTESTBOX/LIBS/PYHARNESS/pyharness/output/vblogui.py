#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.output.logui
:brief: Base module for loggers using a ValidVB-compatible format
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.core import _LEVEL_COMMAND
from pyharness.core import _LEVEL_DEBUG
from pyharness.core import _LEVEL_ERROR
from pyharness.core import _LEVEL_INFO
from pyharness.core import _LEVEL_RAW
from pyharness.core import _LEVEL_SEPARATOR
from pyharness.core import _LEVEL_TITLE1
from pyharness.core import _LEVEL_TITLE2
from pyharness.core import _LEVEL_TITLE3
from pyharness.core import _LEVEL_TRACE
from pyharness.core import _MASK_ALWAYS
from pyharness.core import _MASK_LEVEL
from pyharness.core import TestListener
from pyharness.core import TestSuite


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BaseVBLogTestListener(TestListener):
    """
    Base class for VB logging test listeners.

    This ensures a common format for VB logging test listeners.
    """
    # Hi-level separator
    separator0 = '#' * 70

    # Mid-level separator
    separator1 = '=' * 70

    # Lo-level separator.
    separator2 = '-' * 70

    def __init__(self, descriptions, verbosity, outputdir, args):
        # See ``pyharness.core.TestListener.__init__``
        super().__init__(descriptions, verbosity, outputdir, args)

        self.nonsuccesses = {}
    # end def __init__

    def addError(self, test, err):
        # See ``pyharness.core.TestListener.addError``
        super().addError(test, err)

        if not isinstance(test, TestSuite):
            # Log in the journal
            excp = err[1]
            message = str(excp.args[0]) if len(excp.args) == 1 else ''
            message = message.split('\n', 1)[0].strip()

            # Keep the message for later reference
            self.nonsuccesses[test.id()] = message
        # end if
    # end def addError

    def addFailure(self, test, err):
        # See ``pyharness.core.TestListener.addFailure``
        if not isinstance(test, TestSuite):
            # Log in the journal
            excp = err[1]
            message = str(excp.args[0]) if len(excp.args) == 1 else ''
            message = message.split('\n', 1)[0].strip()

            # Keep the message for later reference
            self.nonsuccesses[test.id()] = message
        # end if
    # end def addFailure

    def addSuccess(self, test, unused=None):
        # See ``pyharness.core.TestListener.addSuccess``
        test_id = test.id()
        if test_id in self.nonsuccesses:
            del self.nonsuccesses[test_id]
        # end if
    # end def addSuccess

    def addTestCase(self, test, test_case, author=None, comment=None):
        # See ``pyharness.core.TestListener.addTestCase``
        if not isinstance(test, TestSuite):

            if author is None:
                author = ""
            else:
                author = " " + author
            # end if

            if comment is None:
                comment = ""
            else:
                comment = f" ({comment})"
            # end if

            self.log(test, _LEVEL_TRACE, f"TestCase: {test_case}{author}{comment}")
        # end if
    # end def addTestCase

    def startTest(self, test):
        # See ``pyharness.core.TestListener.startTest``
        if not isinstance(test, TestSuite):
            self.nonsuccesses[test.id()] = "?"
        # end if
    # end def startTest

    def stopTest(self, test):
        # See ``pyharness.core.TestListener.stopTest``
        super().stopTest(test)

        if not isinstance(test, TestSuite):
            test_id = test.id()

            # Log a summary of the test at the end of the trace
            if test_id in self.nonsuccesses:
                message = self.nonsuccesses[test_id]
                self.log(test, _LEVEL_ERROR + _MASK_ALWAYS, f"{test_id} --> {message}")
            else:
                self.log(test, _LEVEL_TITLE1 + _MASK_ALWAYS, f"{test_id} --> Ok")
            # end if
        # end if
    # end def stopTest
# end class BaseVBLogTestListener


class VBLogFormatter(object):
    """
    Utility class that formats various logs with their appropriate level.
    """
    FORMATTER_MAP = {
            _LEVEL_COMMAND: '_formatCommand',
            _LEVEL_INFO: '_formatInfo',
            _LEVEL_DEBUG: '_formatDebug',
            _LEVEL_ERROR: '_formatError',
            _LEVEL_RAW: '_formatRaw',
            _LEVEL_SEPARATOR: '_formatSeparator',
            _LEVEL_TITLE1: '_formatTitle1',
            _LEVEL_TITLE2: '_formatTitle2',
            _LEVEL_TITLE3: '_formatTitle3',
            _LEVEL_TRACE: '_formatTrace',
    }

    @classmethod
    def getSeparator(cls, size=56):
        """
        Get separator information

        :param size: size of the text
        :type size: ``int``

        :return: Separator Text
        :rtype: ``str``
        """
        return '# ' + '=' * size + '\n'
    # end def getSeparator

    @classmethod
    def _formatCommand(cls, message):
        """
        Format a command message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message
        :rtype: ``str``
        """
        return message
    # end def _formatCommand

    @classmethod
    def _formatRaw(cls, message):
        """
        Format a raw message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message
        :rtype: ``str``
        """
        return message
    # end def _formatRaw

    @classmethod
    def _formatTrace(cls, message):
        """
        Format a trace message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message, prefixed by ' ' on each line
        :rtype: ``str``
        """
        return ' ' + '\n '.join(message.split('\n'))
    # end def _formatTrace

    @classmethod
    def _formatInfo(cls, message):
        """
        Format an info message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message, prefixed by 'Info '
        :rtype: ``str``
        """
        return cls._formatTrace(f'[Info] {message}')
    # end def _formatInfo

    @classmethod
    def _formatDebug(cls, message):
        """
        Format a trace message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message, prefixed by '## ' on each line
        :rtype: ``str``
        """
        return '## ' + '\n## '.join(message.split('\n'))
    # end def _formatDebug

    @classmethod
    def _formatTitle1(cls, message):
        """
        Format a title message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message, prefixed by [Title1]', each following line is split by '\\' + '\\n'.
        :rtype: ``str``
        """
        message_lines = message.split('\n')
        max_size = max([len(line) for line in message_lines])
        text = "[Title1]"
        line_prefix = "\\\n" + " " * len(text)
        hash_line = VBLogFormatter.getSeparator(len(text) + max_size)
        return f'\n{hash_line}{text}{line_prefix.join(message_lines)}\n{hash_line}'
    # end def _formatTitle1

    @classmethod
    def _formatTitle2(cls, message):
        """
        Format a title message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message, prefixed by [Title2]', each following line is split by '\\' + '\\n'.
        :rtype: ``str``
        """
        message_lines = message.split('\n')
        max_size = max([len(line) for line in message_lines])
        text = "[Title2]"
        line_prefix = "\\\n" + " " * len(text)
        hash_line = VBLogFormatter.getSeparator(len(text) + max_size)
        return f'\n{text}{line_prefix.join(message_lines)}\n{hash_line}'
    # end def _formatTitle2

    @classmethod
    def _formatTitle3(cls, message):
        """
        Format a title message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message, prefixed by [Title3]', each following line is split by '\\' + '\\n'.
        :rtype: ``str``
        """
        message_lines = message.split('\n')
        max_size = max([len(line) for line in message_lines])
        text = "[Title3]"
        line_prefix = "\\\n" + " " * len(text)
        hash_line = "-" * (len(text) + max_size)
        return f'{text}{line_prefix.join(message_lines)}\n# {hash_line}'
    # end def _formatTitle3

    @classmethod
    def _formatError(cls, message):
        """
        Format an error message.

        :param message: The message to format
        :type message: ``str``

        :return: Return the message, prefixed by [Error]' on each line.
        :rtype: ``str``
        """
        return '[Error] %s' % (' \n '.join(message.split('\n')),)
    # end def _formatError

    @classmethod
    def _formatSeparator(cls, unused):
        """
        Formats a separator.

        :param unused: The message to format
        :type unused: ``str``

        :return: A separator is a line of '# ====='
        :rtype: ``str``
        """
        if unused is not None:
            return cls.getSeparator(len(unused))
        # end if
        return cls.getSeparator()
    # end def _formatSeparator

    @classmethod
    def format(cls, level, message):  # @ReservedAssignment
        """
        Formats the message

        :param level: The level to format at
        :type level: ``int``
        :param message: The message to format
        :type level: ``str``

        :return: The formatted message
        :rtype: ``str``
        """
        level &= _MASK_LEVEL
        if level in cls.FORMATTER_MAP:
            formatter = getattr(cls, cls.FORMATTER_MAP[level])
        else:
            formatter = cls._formatDebug
        # end if
        return formatter(message)
    # end def format
# end class VBLogFormatter

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
