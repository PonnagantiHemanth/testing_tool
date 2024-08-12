#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.gitversion
:brief: Kosmos Git Version Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/10/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from os import path
from re import compile as re_compile
from re import finditer
from re import fullmatch
from string import hexdigits
from subprocess import CalledProcessError
from subprocess import STDOUT
from subprocess import check_output
from typing import Optional

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.fpgatransport import FPGATransport
from pyraspi.services.kosmos.protocol.generated.messages import MSG_CMD_REPLY_FLAG
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_BRANCH_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_BRANCH_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_HASH_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_GIT_HASH_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS_CMD_VERSION
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

# Path of the Kosmos folder inside py-test-box project
# Path of the Kosmos Protocol submodule folder inside py-test-box project
_kosmos_folder = path.dirname(__file__)
GIT_MODULE = {
    'py-test-box': _kosmos_folder,
    'kosmos-protocol': _kosmos_folder + '/protocol'
}

# Regex for git describe string format. Online tester: https://regex101.com/r/iHCEFY/1
_re_git_describe = re_compile(r"(?P<tag>\w+)(-(?P<count>\d{1,6})-g(?P<hash>[0-9a-f]{7,}))?(-(?P<dirty>dirty))?")

# Regex format: version tag "v1.2.3[-modifier]" or "v1-23-456[-modifier]"
_re_tag_version = re_compile(r'^v(?P<major>\d+)[.-](?P<minor>\d+)[.-](?P<patch>\d+)(-(?P<modifier>[-\w]+))?$')


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class VersionTag:
    """
    Semantic Versioning dataclass.

    `major`, `minor`, `patch` fields:
        Refer to specification: https://semver.org/spec/v2.0.0.html

    `modifier` field: optional text tag, such as "dev", "alpha", "beta", "rc1", and so on.
        Nomenclature is taken from https://calver.org/#scheme
    """
    major: int
    minor: int
    patch: int

    modifier: Optional[str] = None
# end class VersionTag


@dataclass
class GitDescribeOutput:
    """
    Dataclass representing the various parts of a Git Describe string.
    """
    tag: Optional[str] = None
    count: Optional[int] = None
    hash: Optional[str] = None
    dirty: Optional[bool] = None
    version: Optional[VersionTag] = None
# end class GitDescribeOutput


class GitVersionInterface(object, metaclass=ABCMeta):
    """
    Read Git version information on specific folders of the project.
    """

    # List of Git properties that we can inspect
    module_properties = ['branch', 'date', 'describe', 'git_describe', 'hash', 'tag', 'timestamp', 'version']

    # Private attributes
    _branch: str
    _date: datetime
    _describe: str
    _hash: str
    _timestamp: int
    _is_dirty: bool
    _is_debug: bool
    _git_describe: GitDescribeOutput

    def __init__(self, module):
        """
        :param module: Parameter to be consumed by the class derived from the present interface.
        :type module: ``int or str``
        """
        self._module = module
        self.update()
    # end def __init__

    @property
    def branch(self):
        """
        Return the Git Branch property.

        :return: Git Branch property
        :rtype: ``str``
        """
        return self._branch
    # end def property getter branch

    @property
    def date(self):
        """
        Return the Git Date property.

        :return: Git Date property
        :rtype: ``datetime``
        """
        return self._date
    # end def property getter date

    @property
    def describe(self):
        """
        Return the Git Describe property.

        :return: Git Describe property
        :rtype: ``str``
        """
        return self._describe
    # end def property getter describe

    @property
    def hash(self):
        """
        Return the Git Hash property.

        :return: Git Hash property
        :rtype: ``str``
        """
        return self._hash
    # end def property getter hash

    @property
    def tag(self):
        """
        Return the Git Tag property.

        :return: Git Tag property
        :rtype: ``str``
        """
        return self._git_describe.tag
    # end def property getter tag

    @property
    def timestamp(self):
        """
        Return the Git Timestamp property (32-bit Unix epoch).

        :return: Git Timestamp property
        :rtype: ``int``
        """
        return self._timestamp
    # end def property getter timestamp

    @property
    def git_describe(self):
        """
        Return the Git Describe property.

        :return: Git Describe property
        :rtype: ``GitDescribeOutput``
        """
        return self._git_describe
    # end def property getter git_describe

    @property
    def version(self):
        """
        Return the Git Version Tag property.

        :return: Git Version Tag property
        :rtype: ``VersionTag``
        """
        return self._git_describe.version
    # end def property getter version

    @abstractmethod
    def update(self):
        """
        Update all properties' value.
        """
        raise NotImplementedAbstractMethodError()
    # end def update

    @classmethod
    def parse_git_describe(cls, git_describe_string):
        """
        Parse a git describe string to extract tag description, commit count, commit hash, and dirty flag.

        :param git_describe_string: 'git describe' command output string
        :type git_describe_string: ``str``

        :return: parsed information: tag description, commit count, commit hash, and dirty flag
        :rtype: ``GitDescribeOutput``

        :raise ``AssertionError``: When the Git Describe string syntax is invalid
        """
        matches = finditer(_re_git_describe, git_describe_string)
        output = GitDescribeOutput()

        for match in matches:
            # Concatenate all 'tag' matches
            new_tag = match.group('tag')
            assert new_tag is not None
            if output.tag is None:
                output.tag = new_tag
            else:
                output.tag += '-' + new_tag
            # end if

            # Only one 'count' match is allowed
            new_count = match.group('count')
            if output.count is None:
                output.count = new_count
            else:
                assert new_count is None
            # end if

            # Only one 'hash' match is allowed
            new_hash = match.group('hash')
            if output.hash is None:
                output.hash = new_hash
            else:
                assert new_hash is None
            # end if

            # Only one 'dirty' match is allowed
            new_dirty = match.group('dirty')
            if output.dirty is None:
                output.dirty = new_dirty
            else:
                assert new_dirty is None
            # end if
        # end for

        # Convert types & Validate
        output.dirty = (output.dirty == r'dirty')
        assert not ((output.hash is None) ^ (output.count is None))
        if output.count is not None:
            output.count = int(output.count)
            assert output.count > 0
            output.hash.lower()
        # end if

        # Convert tag string to tag version if possible
        output.version = cls.tag_to_version(tag_str=output.tag)

        return output
    # end def parse_git_describe

    @staticmethod
    def tag_to_version(tag_str):
        """
        Convert a Git Tag string to a Version Tag.
        Return None if the Git Tag string does not represent a version tag like 'v1.2.3' or 'v1-2-3'.

        :param tag_str: Git Tag string
        :type tag_str: ``str``

        :return: Converted Version Tag
        :rtype: ``VersionTag or None``
        """
        re_match = fullmatch(_re_tag_version, tag_str)
        if re_match is None:
            return None
        # end if
        return VersionTag(major=int(re_match['major']),
                          minor=int(re_match['minor']),
                          patch=int(re_match['patch']),
                          modifier=re_match['modifier'])
    # end def tag_to_version

    @staticmethod
    def is_hash_string(hash_string):
        """
        Test if the input string is longer than 7 characters and contains only hexadecimal characters.

        :param hash_string: A Git Hash string
        :type hash_string: ``str``

        :return: Flag indicating hash string validity
        :rtype: ``bool``
        """
        return len(hash_string) >= 7 and all(c in hexdigits for c in hash_string)
    # end def is_hash_string

    def __str__(self):
        """
        Return a string representation of all Git properties.

        :return: string representation
        :rtype: ``str``
        """
        str_out = ''
        for module_property in self.module_properties:
            version = self.__getattribute__(module_property)
            str_out += f' - {module_property:10}: {version}\n'
        # end for
        return str_out
    # end def __str__
# end class GitVersionInterface


class LocalGitVersion(GitVersionInterface):
    """
    Handles Git version information on specific folders of the project.
    """
    def update(self):
        """
        Execute git commands to update all properties' value.

        :raise ``AssertionError``: Git hash contains some non-hexadecimal characters
        :raise ``FileNotFoundError``: detected dubious ownership
        """
        # Git Branch
        command_args = ['git', 'symbolic-ref', '--short', 'HEAD']
        try:
            self._branch = self._run_command(command_args, self._module)
        except CalledProcessError as e:
            # Handle 'Detached HEAD' case (when git index does not point to a branch, but to a specific commit hash)
            if e.returncode == 128 and b'fatal: ref HEAD is not a symbolic ref' in e.output:
                command_args = ['git', 'name-rev', '--name-only', 'HEAD']
                self._branch = self._run_command(command_args, self._module)
            # end if
        # end try

        try:
            # Git Date
            command_args = ['git', 'log', '-1', '--format=%cd', '--date=iso-strict']
            self._date = datetime.fromisoformat(self._run_command(command_args, self._module))

            # Git Describe
            command_args = ['git', 'describe', '--always', '--dirty', '--tags']
            self._describe = self._run_command(command_args, self._module)

            # Git Hash
            command_args = ['git', 'rev-parse', 'HEAD']
            self._hash = self._run_command(command_args, self._module).lower()

            # Git Timestamp
            command_args = ['git', 'log', '-1', '--format=%ct']
            self._timestamp = int(self._run_command(command_args, self._module))
        except CalledProcessError as e:
            # Handle fatal error: detected dubious ownership
            if e.returncode == 128 and b'fatal: detected dubious ownership' in e.output:
                raise FileNotFoundError("detected dubious ownership")
            else:
                raise e
            # end if
        # end try

        # Validate Git Hash
        assert self.is_hash_string(self._hash), \
               "Git hash contains some non-hexadecimal characters:\n" + \
               "\n".join([f"'{c}' {hex(ord(c))}" for c in self._hash])

        # Validate Git Describe string
        self._git_describe = self.parse_git_describe(self._describe)
        self._is_dirty = self._git_describe.dirty
        if self._git_describe.hash is not None:
            assert self._hash.startswith(self._git_describe.hash)
            assert self._git_describe.count > 0
        else:
            assert self._git_describe.count is None
        # end if
    # end def update

    @staticmethod
    def _run_command(command_args, module_path):
        """
        Wrapper to execute git command

        :param command_args: command to be executed, containing the programme name and arguments
        :type command_args: ``list[str]``
        :param module_path: The directory where the command will be executed from
        :type module_path: ``str``

        :return: The command's output
        :rtype: ``str``

        :raise ``FileNotFoundError``: When the '.git' folder can't be found, typically when running from PyCharm remote
                                      launcher.
        :raise ``CalledProcessError``: When the command fails
        """
        try:
            result = check_output(command_args, cwd=module_path, stderr=STDOUT).strip().decode()
        except CalledProcessError as e:
            if e.returncode == 128 and b'fatal: not a git repository' in e.output:
                msg = e.output.strip().decode() + '\n'
                msg += f'ERROR: No `.git` folder found in `{module_path}` or above.\n'
                msg += '       If you are running this python script remotely using PyCharm, ' \
                       'then this is to be expected.\n'
                msg += '       PyCharm does NOT synchronize the `.git` folder during deployment, by design.\n'
                msg += '       It is simply not possible to access git information using ' \
                       'PyCharm Remote Launcher/Debugger.\n'
                raise FileNotFoundError(msg) from e
            # end if
            raise e
        # end try
        return result
    # end def _run_command

    def __str__(self):
        """
        Return a string representation of the object, listing all Git properties.

        :return: string representation
        :rtype: ``str``
        """
        str_out = f'Local repository: {self._module}\n'
        str_out += super().__str__()
        return str_out
    # end def __str__
# end class LocalGitVersion


class RemoteGitVersion(GitVersionInterface):
    """
    Handles Git version information on remote hardware
    """
    def __init__(self, module, fpga_transport):
        """
        :param module: MessageFrame ID, indicating which Git module is targeted
        :type module: ``MSG_ID_PROTOCOL or MSG_ID_KOSMOS``
        :param fpga_transport: instance of ``FPGATransport``
        :type fpga_transport: ``FPGATransport``

        :raise ``AssertionError``: unexpected argument type
        """
        assert isinstance(fpga_transport, FPGATransport), fpga_transport
        self._fpga_transport = fpga_transport
        super().__init__(module)
    # end def __init__

    def update(self):
        """
        Request versions from Remote hardware and update all properties' value

        :raise ``AssertionError``: Invalid module ID
        """
        # Prepare message requests
        commands = range(MSG_ID_KOSMOS_CMD_VERSION, MSG_ID_KOSMOS_CMD_GIT_HASH_2 + 1)
        tx_frames = []
        assert self._module in [MSG_ID_PROTOCOL, MSG_ID_KOSMOS]
        for frame_cmd in commands:
            tx_frame = MessageFrame()
            tx_frame.frame.id = self._module
            tx_frame.frame.cmd = frame_cmd
            tx_frames.append(tx_frame)
        # end for

        # Send message requests and get replies
        rxtx_frames = self._fpga_transport.send_control_message_list(tx_frames)

        # Git Version
        _, rx_frame = rxtx_frames[0]
        assert rx_frame.frame.id == self._module
        assert rx_frame.frame.cmd == MSG_ID_KOSMOS_CMD_VERSION | MSG_CMD_REPLY_FLAG
        self._timestamp = rx_frame.frame.payload.git_version.timestamp
        self._is_dirty = rx_frame.frame.payload.git_version.is_dirty
        self._is_debug = rx_frame.frame.payload.git_version.is_debug
        self._date = datetime.fromtimestamp(self._timestamp, tz=timezone.utc)

        # Git Describe
        _, rx_frame = rxtx_frames[1]
        assert rx_frame.frame.id == self._module
        assert rx_frame.frame.cmd == MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_1 | MSG_CMD_REPLY_FLAG
        self._describe = ''.join([chr(x) for x in rx_frame.frame.payload.git_info.value if x])

        _, rx_frame = rxtx_frames[2]
        assert rx_frame.frame.id == self._module
        assert rx_frame.frame.cmd == MSG_ID_KOSMOS_CMD_GIT_DESCRIBE_2 | MSG_CMD_REPLY_FLAG
        self._describe += ''.join([chr(x) for x in rx_frame.frame.payload.git_info.value if x])

        # Git Branch
        _, rx_frame = rxtx_frames[3]
        assert rx_frame.frame.id == self._module
        assert rx_frame.frame.cmd == MSG_ID_KOSMOS_CMD_GIT_BRANCH_1 | MSG_CMD_REPLY_FLAG
        self._branch = ''.join([chr(x) for x in rx_frame.frame.payload.git_info.value if x])

        _, rx_frame = rxtx_frames[4]
        assert rx_frame.frame.id == self._module
        assert rx_frame.frame.cmd == MSG_ID_KOSMOS_CMD_GIT_BRANCH_2 | MSG_CMD_REPLY_FLAG
        self._branch += ''.join([chr(x) for x in rx_frame.frame.payload.git_info.value if x])

        # Git Hash
        _, rx_frame = rxtx_frames[5]
        assert rx_frame.frame.id == self._module
        assert rx_frame.frame.cmd == MSG_ID_KOSMOS_CMD_GIT_HASH_1 | MSG_CMD_REPLY_FLAG
        self._hash = ''.join([chr(x) for x in rx_frame.frame.payload.git_info.value if x])

        _, rx_frame = rxtx_frames[6]
        assert rx_frame.frame.id == self._module
        assert rx_frame.frame.cmd == MSG_ID_KOSMOS_CMD_GIT_HASH_2 | MSG_CMD_REPLY_FLAG
        self._hash += ''.join([chr(x) for x in rx_frame.frame.payload.git_info.value if x])

        # Validate Git Hash
        assert self.is_hash_string(self._hash), \
               "Git hash contains some non-hexadecimal characters:\n" + \
               "\n".join([f"'{c}' {hex(ord(c))}" for c in self._hash])

        # Validate Git Describe string
        self._git_describe = self.parse_git_describe(self._describe)
        assert self._is_dirty == self._git_describe.dirty
        if self._git_describe.hash is not None:
            assert self._hash.startswith(self._git_describe.hash)
            assert self._git_describe.count > 0
        # end if
    # end def update

    def __str__(self):
        """
        Return a string representation of the object, listing all Git properties.

        :return: string representation
        :rtype: ``str``
        """
        str_out = f'Remote repository: '
        if self._module == MSG_ID_KOSMOS:
            str_out += 'Kosmos FPGA + Firmware\n'
        else:
            str_out += 'Kosmos Communication Protocol\n'
        # end if
        str_out += super().__str__()
        return str_out
    # end def __str__
# end class RemoteGitVersion

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
