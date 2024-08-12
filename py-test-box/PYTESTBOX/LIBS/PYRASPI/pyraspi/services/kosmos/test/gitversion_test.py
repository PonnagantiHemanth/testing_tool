#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.gitversion_test
:brief: Kosmos Version Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/10/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from os import sep
from unittest import TestCase
from unittest import skipIf

from pyraspi.raspi import UNSUPPORTED_SETUP_ERR_MSG
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.gitversion import GIT_MODULE
from pyraspi.services.kosmos.gitversion import GitDescribeOutput
from pyraspi.services.kosmos.gitversion import GitVersionInterface
from pyraspi.services.kosmos.gitversion import LocalGitVersion
from pyraspi.services.kosmos.gitversion import RemoteGitVersion
from pyraspi.services.kosmos.gitversion import VersionTag
from pyraspi.services.kosmos.gitversion import _kosmos_folder
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AbstractTestClass:
    """
    This class is used to wrap Abstract Test Case classes, so that they cannot be not automatically loaded and executed.

    This is the best way so far, in order to use `unittest.TestCase` along with `abc.ABCMeta` and inheritance.
    Refer to https://stackoverflow.com/a/25695512 and https://stackoverflow.com/a/35304339
    """
    class GitVersionTestCaseInterface(TestCase, metaclass=ABCMeta):
        """
        Interface class for Git Version Unitary Test class
        """
        git_version = None  # Must be set to an instance of a class derived from GitVersionInterface

        @classmethod
        @abstractmethod
        def setUpClass(cls):
            """
            Setup Class
            """
            cls.git_version = None  # Overriding method must set this member
            raise NotImplementedError('User must override this method in derived class')
        # end def setUpClass

        def test_properties(self):
            """
            Validate class properties
            """
            # Validate above property list is exhaustive
            module_properties_from_class = [p for p in dir(GitVersionInterface)
                                            if isinstance(getattr(GitVersionInterface, p), property)]
            self.assertListEqual(self.git_version.module_properties,
                                 module_properties_from_class,
                                 msg='This test case is not exhaustive.')

            # Validate each property for each git module
            for module_name, module_path in GIT_MODULE.items():
                for module_property in self.git_version.module_properties:
                    with self.subTest(module_name=module_name, module_property=module_property):
                        version = getattr(self.git_version, module_property)
                        if module_property == 'describe':
                            self.git_version.parse_git_describe(version)
                        elif module_property == 'hash':
                            self.assertTrue(self.git_version.is_hash_string(version),
                                            msg="Git hash contains some non-hexadecimal characters:\n" +
                                                "\n".join([f"'{c}' {hex(ord(c))}" for c in version]))
                        # end if
                    # end with
                # end for
            # end for
        # end def test_properties

        def test_parse_git_describe(self):
            """
            Validate 'parse_git_describe()' method
            """
            # Examples of valid git describe strings that will be parsed correctly
            test_str_good = [(r'MyTagName-012_34Tag-5678-gfbea866b2-dirty',
                              GitDescribeOutput(tag='MyTagName-012_34Tag', count=5678, hash='fbea866b2', dirty=True)),
                             (r'MyTagName-012_34Tag-1234-gfbea866b2',
                              GitDescribeOutput(tag='MyTagName-012_34Tag', count=1234, hash='fbea866b2', dirty=False)),
                             (r'MyTagName-012_34Tag-dirty',
                              GitDescribeOutput(tag='MyTagName-012_34Tag', count=None, hash=None, dirty=True))]

            # Examples of invalid git describe strings that cannot be parsed correctly, and do not throw any error.
            # The issue is that '-' character is allowed in tag field, in addition of being a field separator.
            # That prevents from having a strict syntax.
            test_str_bad = [(r'MyTagName-012_34Tag-1322',
                             GitDescribeOutput(tag='MyTagName-012_34Tag-1322', count=None, hash=None, dirty=False)),
                            (r'MyTagName-012_34Tag-gfbea866',
                             GitDescribeOutput(tag='MyTagName-012_34Tag-gfbea866', count=None, hash=None, dirty=False))]

            for test_str, expectation in test_str_good + test_str_bad:
                with self.subTest(str=test_str):
                    git_describe = self.git_version.parse_git_describe(test_str)
                    self.assertEqual(expectation, git_describe)
                # end with
            # end for
        # end def test_parse_git_describe

        def test_is_hash_string(self):
            """
            Validate 'is_hash_string()' method
            """
            self.assertTrue(self.git_version.is_hash_string(r'abcdef0123456789'), 'All allowed lowercase characters')
            self.assertTrue(self.git_version.is_hash_string(r'ABCDEF0123456789'), 'All allowed uppercase characters')
            self.assertFalse(self.git_version.is_hash_string(r'123456'), 'Must be at least 7 character long.')
            self.assertFalse(self.git_version.is_hash_string(r'hello'), 'Must be hexadecimal character')
        # end def test_is_hash_string

        def test_tag_to_version(self):
            """
            Validate ``tag_to_version()`` method.
            """
            # Validate Expected Success
            self.assertEqual(VersionTag(1, 2, 3, None), self.git_version.tag_to_version('v1.2.3'))
            self.assertEqual(VersionTag(1, 2, 3, 'dev'), self.git_version.tag_to_version('v1.2.3-dev'))
            self.assertEqual(VersionTag(1, 2, 3, 'rc'), self.git_version.tag_to_version('v1.2.3-rc'))
            self.assertEqual(VersionTag(1, 2, 3, 'dev-alpha'), self.git_version.tag_to_version('v1.2.3-dev-alpha'))
            self.assertEqual(VersionTag(111, 222, 333, 'aA09-bB09zZ_cC'),
                             self.git_version.tag_to_version('v111.222.333-aA09-bB09zZ_cC'))

            self.assertEqual(VersionTag(1, 2, 3, None), self.git_version.tag_to_version('v1-2-3'))
            self.assertEqual(VersionTag(1, 2, 3, 'dev'), self.git_version.tag_to_version('v1-2-3-dev'))
            self.assertEqual(VersionTag(1, 2, 3, 'rc'), self.git_version.tag_to_version('v1-2-3-rc'))
            self.assertEqual(VersionTag(1, 2, 3, 'dev-alpha'), self.git_version.tag_to_version('v1-2-3-dev-alpha'))
            self.assertEqual(VersionTag(111, 222, 333, 'aA09-bB09zZ_cC'),
                             self.git_version.tag_to_version('v111-222-333-aA09-bB09zZ_cC'))

            # Validate Expected Failure
            self.assertIsNone(self.git_version.tag_to_version('v1-2-3-'))
            self.assertIsNone(self.git_version.tag_to_version('v1-2-3-dot.dot'))
            self.assertIsNone(self.git_version.tag_to_version('v1-2-modifier'))
        # end def test_tag_to_version
    # end class GitVersionTestCaseInterface
# end class AbstractTestClass


class LocalGitVersionTestCase(AbstractTestClass.GitVersionTestCaseInterface):
    """
    Local Git Version Unitary Test class
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the class, by instantiating LocalGitVersion class

        In the case where the git folder is missing, refer to comment in 'setUp' method.
        """
        try:
            cls.git_version = LocalGitVersion(module=_kosmos_folder)
        except FileNotFoundError:
            cls._not_a_git_repository = True
        else:
            cls._not_a_git_repository = False
        # end try
    # end def setUpClass

    def setUp(self):
        """
        Allow to skip all Test Cases in the situation where the current project deployment is not done using Git,
        but with PyCharm remote launcher for example.
        In that latter case, the '.git' folder is not synchronised with the remote.
        That renders all call to git executable useless.
        """
        if self._not_a_git_repository:
            self.skipTest('Test is skipped because this is not a git project.')
        # end if
    # end def setUp

    def test_run_command(self):
        """
        Validate _run_command() static method
        """
        command_args = ['git', '--version']
        result = LocalGitVersion._run_command(command_args=command_args, module_path=_kosmos_folder)
        self.assertRegex(result, r'^git version \d{1,3}\.\d{1,3}\.\d{1,3}')
    # end def test_run_command

    def test_invalid_module_argument(self):
        """
        Validate behavior in case of invalid git path
        """
        # Find the path of the folder containing the present py-test-box project (this should not be a git repository).
        split_path = _kosmos_folder.split(sep)  # `os.sep` is the platform-dependant path separator
        not_a_git_path = sep.join(split_path[0:split_path.index('PYTESTBOX') - 1])

        # Expect error
        with self.assertRaises(FileNotFoundError):
            LocalGitVersion(module=not_a_git_path)
        # end with
    # end def test_invalid_module_argument
# end class LocalGitVersionTestCase


@skipIf(not Daemon.is_host_kosmos(), UNSUPPORTED_SETUP_ERR_MSG)
class RemoteGitVersionTestCase(AbstractTestClass.GitVersionTestCaseInterface):
    """
    Remote Git Version Unitary Test class
    """
    kosmos = None
    git_version = None

    @classmethod
    def setUpClass(cls):
        """
        Setup the class, by instantiating RemoteGitVersion class
        """
        cls.kosmos = Kosmos.get_instance()
        cls.git_version = cls.kosmos.version.remote_protocol
    # end def setUpClass

    def test_invalid_module_argument(self):
        """
        Validate behavior in case of invalid module ID.
        Valid values for module argument are '[MSG_ID_PROTOCOL, MSG_ID_KOSMOS]'
        """
        # Expect error
        with self.assertRaises(AssertionError):
            RemoteGitVersion(module=(MSG_ID_KOSMOS+1), fpga_transport=self.kosmos.fpga_transport)
        # end with
    # end def test_invalid_module_argument
# end class RemoteGitVersionTestCase
