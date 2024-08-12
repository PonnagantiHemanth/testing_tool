#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.version
:brief: Kosmos Version Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/07/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from typing import Optional

from pyraspi.services.kosmos.fpgatransport import FPGATransport
from pyraspi.services.kosmos.gitversion import GIT_MODULE
from pyraspi.services.kosmos.gitversion import LocalGitVersion
from pyraspi.services.kosmos.gitversion import RemoteGitVersion
from pyraspi.services.kosmos.gitversion import VersionTag
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_KOSMOS
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PROTOCOL
from pyraspi.services.kosmos.protocol.generated.messages import fpga_version_t

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

# FPGA hardware revision & Firmware version tag
# Expected Major and Minor version numbers have to match the revision read from hardware.
# Expected Patch version number is a minimum.
EXPECTED_FPGA_HWREV = VersionTag(major=2, minor=2, patch=0)
EXPECTED_FIRMWARE_TAG = VersionTag(major=2, minor=2, patch=0)


# ------------------------------------------------------------------------------
# exceptions
# ------------------------------------------------------------------------------
class KosmosVersionError(Exception):
    """
    Exception base class for Kosmos Version errors.
    """
    pass
# end class KosmosVersionError


class KosmosProtocolVersionError(KosmosVersionError):
    """
    Exception class for Kosmos Protocol Version errors.
    """
    host: LocalGitVersion
    remote: RemoteGitVersion

    def __init__(self, host, remote):
        """
        :param host: Host Protocol version
        :type host: ``LocalGitVersion``
        :param remote: Remote Protocol version
        :type remote: ``RemoteGitVersion``
        """
        self.host = host
        self.remote = remote
        super().__init__(f'Kosmos Protocol version mismatch:\n'
                         f'  Host   (Python)  : {host.version}\n'
                         f'  Remote (firmware): {remote.version}\n'
                         f'The Host and Remote Kosmos Protocol modules do not share the same version.\n'
                         f'Verify both Host and Remote Git repositories are up-to-date '
                         f'and correct firmware is flashed.\n'
                         f'Host: {host}'
                         f'Remote: {remote}')
    # end def __init__
# end class KosmosProtocolVersionError


class KosmosFirmwareVersionError(KosmosVersionError):
    """
    Exception class for Kosmos Firmware Version errors.
    """
    expected: VersionTag
    actual: RemoteGitVersion

    def __init__(self, expected, actual):
        """
        :param expected: Expected Firmware version (Major, Minor have to match, Patch is a minimum)
        :type expected: ``VersionTag``
        :param actual: Actual Firmware version
        :type actual: ``RemoteGitVersion``
        """
        self.expected = expected
        self.actual = actual
        super().__init__(f'Kosmos Firmware version mismatch:\n'
                         f'  expected : {expected}\n'
                         f'  actual   : {actual.version}\n'
                         f'Details: {actual}')
    # end def __init__
# end class KosmosFirmwareVersionError


class KosmosFpgaRevisionError(KosmosVersionError):
    """
    Exception class for Kosmos FPGA Revision errors.
    """
    expected: VersionTag
    actual: VersionTag

    def __init__(self, expected, actual):
        """
        :param expected: Expected FPGA revision (Major, Minor have to match, Patch is a minimum)
        :type expected: ``VersionTag``
        :param actual: Actual FPGA revision
        :type actual: ``VersionTag``
        """
        self.expected = expected
        self.actual = actual
        super().__init__(f'Kosmos FPGA revision mismatch:\n'
                         f'  expected : {expected}\n'
                         f'  actual   : {actual}')
    # end def __init__
# end class KosmosFpgaRevisionError


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosVersion:
    """
    Kosmos Version Class: Fetch and check Protocol (Host & Remote), Firmware, FPGA versions.
    """
    # Remote FPGA revision
    fpga: VersionTag

    # Remote & Host Protocol Git Versions
    remote_protocol: RemoteGitVersion
    host_protocol: Optional[LocalGitVersion]

    # Remote Firmware Git Versions
    firmware: RemoteGitVersion

    def __init__(self, fpga_transport):
        """
        :param fpga_transport: FPGATransport instance
        :type fpga_transport: ``FPGATransport``
        """
        # Initialize Kosmos Version for: Protocol (Host & Remote), Firmware, FPGA

        # Remote FPGA revision
        _fpga: fpga_version_t = fpga_transport.fpga_revision.version
        self.fpga = VersionTag(major=_fpga.major, minor=_fpga.minor, patch=_fpga.patch)

        # Remote Protocol Git Versions
        self.remote_protocol = RemoteGitVersion(module=MSG_ID_PROTOCOL, fpga_transport=fpga_transport)

        # Remote Firmware Git Versions
        self.firmware = RemoteGitVersion(module=MSG_ID_KOSMOS, fpga_transport=fpga_transport)

        # Host Protocol Git Versions
        # Handle case where the current project deployment is not done using Git,
        # but with PyCharm remote launcher for example. In that latter case, the '.git' folder is not synchronised
        # with the remote, which renders all call to git executable useless.
        try:
            self.host_protocol = LocalGitVersion(module=GIT_MODULE['kosmos-protocol'])
        except FileNotFoundError:
            self.host_protocol = None
        # end try
    # end def __init__

    def check(self):
        """
        Run assertion checks on Kosmos Protocol, Firmware and FPGA versions.
        """
        self.assert_protocol_versions(host=self.host_protocol, remote=self.remote_protocol)
        self.assert_firmware_version(expected=EXPECTED_FIRMWARE_TAG, firmware=self.firmware)
        self.assert_fpga_revision(expected=EXPECTED_FPGA_HWREV, fpga=self.fpga)
    # end def check

    @staticmethod
    def test_protocol_versions(host, remote):
        """
        Test if Host and Remote Protocol versions match (patch excluded)

        Rationale:
         - major and minor have to match
         - host patch can be higher

        :param host: Host Protocol version structure (major, minor, patch)
        :type host: ``VersionTag``
        :param remote: Remote Protocol version structure (major, minor, patch)
        :type remote: ``VersionTag``

        :return: Host vs Remote Protocol Versions comparison result.
        :rtype: ``bool or None``
        """
        return (remote.major == host.major and
                remote.minor == host.minor and
                remote.patch <= host.patch)
    # end def test_protocol_versions

    @staticmethod
    def test_tag_versions(expected, actual):
        """
        Test if actual version is above or equal expected version.

        Rationale:
         - Major and Minor version numbers: Expected == Actual.
         - Patch version number: Expected <= Actual.

        :param expected: Expected version structure (major, minor, patch)
        :type expected: ``VersionTag``
        :param actual: Actual version structure (major, minor, patch)
        :type actual: ``VersionTag``

        :return: actual vs expected versions comparison result
        :rtype: ``bool``
        """
        return (expected.major == actual.major and
                expected.minor == actual.minor and
                expected.patch <= actual.patch)
    # end def test_tag_versions

    @classmethod
    def assert_protocol_versions(cls, host, remote):
        """
        Assertion for Kosmos Protocol version.

        :param host: Host Protocol version (set to None if not available)
        :type host: ``LocalGitVersion or None``
        :param remote: Remote Protocol version
        :type remote: ``RemoteGitVersion``

        :raise ``KosmosProtocolVersionError``: Kosmos Protocol version mismatch
        """
        if host is not None and cls.test_protocol_versions(host=host.version, remote=remote.version) is False:
            raise KosmosProtocolVersionError(host=host, remote=remote)
        # end if
    # end def assert_protocol_versions

    @classmethod
    def assert_firmware_version(cls, expected, firmware):
        """
        Assertion for Kosmos Firmware version.

        :param expected: Expected Firmware version (Major, Minor have to match, Patch is a minimum)
        :type expected: ``VersionTag``
        :param firmware: Actual Firmware version
        :type firmware: ``RemoteGitVersion``

        :raise ``KosmosVersionError``: Kosmos Firmware version tag could not be parsed from tag string
        :raise ``KosmosFirmwareVersionError``: Kosmos Firmware version mismatch
        """
        if firmware.version is None:
            raise KosmosVersionError(f'Firmware version tag could not be parsed from tag string: {firmware.tag}.\n'
                                     f'  expected : {expected}\n'
                                     f'  actual   : {firmware}')
        # end if

        if cls.test_tag_versions(expected=expected, actual=firmware.version) is False:
            raise KosmosFirmwareVersionError(expected=expected, actual=firmware)
        # end if
    # end def assert_firmware_version

    @classmethod
    def assert_fpga_revision(cls, expected, fpga):
        """
        Assertion for Kosmos FPGA revision.

        :param expected: Expected FPGA revision (Major, Minor have to match, Patch is a minimum)
        :type expected: ``VersionTag``
        :param fpga: Actual FPGA revision
        :type fpga: ``VersionTag``

        :raise ``KosmosFpgaRevisionError``: Kosmos FPGA revision mismatch
        """
        if cls.test_tag_versions(expected=expected, actual=fpga) is False:
            raise KosmosFpgaRevisionError(expected=expected, actual=fpga)
        # end if
    # end def assert_fpga_revision

    @staticmethod
    def test_daemon_versions(expected, actual):
        """
        Test if actual version is above or equal expected version.

        Rationale:
         - Major, Minor or Patch version numbers: Expected <= Actual.

        :param expected: Expected version structure (major, minor, patch)
        :type expected: ``VersionTag``
        :param actual: Actual version structure (major, minor, patch)
        :type actual: ``VersionTag``

        :return: actual vs expected versions comparison result
        :rtype: ``bool``
        """
        return expected.major <= actual.major or \
            (expected.major == actual.major and expected.minor <= actual.minor) or \
            (expected.major == actual.major and expected.minor == actual.minor and expected.patch <= actual.patch)
    # end def test_daemon_versions

    def __str__(self):
        """
        Return a human-readable string of Remote FPGA, Remote & Host Protocols and Remote Firmware versions.

        :return: Kosmos versions
        :rtype: ``str``
        """
        return f'Remote FPGA revision:         {self.fpga}\n' \
               f'Remote Protocol Git Version:  {self.remote_protocol}\n' \
               f'Host Protocol Git Version:    {self.host_protocol}\n' \
               f'Remote Firmware Git Versions: {self.firmware}'
    # end def __str__
# end class KosmosVersion

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
