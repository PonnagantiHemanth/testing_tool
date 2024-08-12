#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.version_test
:brief: Tests for Kosmos Version Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/07/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from copy import copy

from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase
from pyraspi.services.kosmos.version import KosmosFirmwareVersionError
from pyraspi.services.kosmos.version import KosmosFpgaRevisionError
from pyraspi.services.kosmos.version import KosmosProtocolVersionError
from pyraspi.services.kosmos.version import KosmosVersion
from pyraspi.services.kosmos.version import KosmosVersionError
from pyraspi.services.kosmos.version import VersionTag


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosVersionTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos Version class
    """

    # Object under test
    mock_version: KosmosVersion

    def setUp(self):
        """
        Prepare Unit Test
        """
        super().setUp()

        # Run Unit Tests on a copy of the instantiated KosmosVersion class
        self.mock_version = copy(self.kosmos.version)

        # If Host Protocol Version cannot be read, copy from Remote Protocol
        if self.mock_version.host_protocol is None:
            self.mock_version.host_protocol = copy(self.mock_version.remote_protocol)
        # end if
    # end def setUp

    def test_check(self):
        """
        Validate ``KosmosVersion.check()`` method.
        """
        self.mock_version.check()
    # end def test_check

    def test_protocol_versions(self):
        """
        Validate ``KosmosVersion.test_protocol_versions()``
             and ``KosmosVersion.assert_protocol_versions()`` methods.
        """
        # Validate Expected Success
        self.assertTrue(self.mock_version.test_protocol_versions(host=self.mock_version.host_protocol,
                                                                 remote=self.mock_version.remote_protocol))

        for _property in self.mock_version.host_protocol.module_properties:
            self.assertEqual(getattr(self.mock_version.host_protocol, _property),
                             getattr(self.mock_version.remote_protocol, _property),
                             msg=(_property, self.mock_version.host_protocol, self.mock_version.remote_protocol))
        # end for

        # Validate Expected Failure
        self.mock_version.host_protocol._hash = reversed(self.mock_version.host_protocol._hash)  # modify Git Hash
        self.assertFalse(self.mock_version.test_protocol_versions(host=self.mock_version.host_protocol,
                                                                  remote=self.mock_version.remote_protocol))
        self.assertRaises(KosmosProtocolVersionError,
                          self.mock_version.assert_protocol_versions,
                          host=self.mock_version.host_protocol,
                          remote=self.mock_version.remote_protocol)
    # end def test_protocol_versions

    def test_tag_versions(self):
        """
        Validate ``KosmosVersion.test_tag_versions()`` method.
        """
        # Validate Expected Success
        self.assertTrue(self.mock_version.test_tag_versions(expected=VersionTag(major=1, minor=2, patch=3),
                                                            actual=VersionTag(major=1, minor=2, patch=3)))
        self.assertTrue(self.mock_version.test_tag_versions(expected=VersionTag(major=4, minor=5, patch=6),
                                                            actual=VersionTag(major=4, minor=5, patch=7)))

        # Validate Expected Failure
        self.assertFalse(self.mock_version.test_tag_versions(expected=VersionTag(major=1, minor=2, patch=3),
                                                             actual=VersionTag(major=1, minor=2, patch=2)))
        self.assertFalse(self.mock_version.test_tag_versions(expected=VersionTag(major=4, minor=5, patch=6),
                                                             actual=VersionTag(major=4, minor=4, patch=6)))
        self.assertFalse(self.mock_version.test_tag_versions(expected=VersionTag(major=4, minor=5, patch=6),
                                                             actual=VersionTag(major=4, minor=6, patch=6)))
        self.assertFalse(self.mock_version.test_tag_versions(expected=VersionTag(major=7, minor=8, patch=9),
                                                             actual=VersionTag(major=6, minor=8, patch=9)))
        self.assertFalse(self.mock_version.test_tag_versions(expected=VersionTag(major=7, minor=8, patch=9),
                                                             actual=VersionTag(major=8, minor=8, patch=9)))
    # end def test_tag_versions

    def test_tag_parsing(self):
        """
        Validate ``KosmosVersion.assert_firmware_version()`` method.
        """
        # Validate Expected Success
        self.assertIsNotNone(self.mock_version.firmware.git_describe.version)

        # Validate Expected Failure
        self.mock_version.firmware.git_describe.version = None  # this should make the assert fail
        self.assertRaises(KosmosVersionError,
                          self.mock_version.assert_firmware_version,
                          expected=VersionTag(major=1, minor=2, patch=3),
                          firmware=self.mock_version.firmware)
    # end def test_tag_parsing

    def test_firmware_version(self):
        """
        Validate ``KosmosVersion.assert_firmware_version`` method.
        """
        # Validate Expected Success
        # Set firmware version to a know value
        self.mock_version.firmware._git_describe.version = VersionTag(major=4, minor=5, patch=6)

        self.assertTrue(self.mock_version.test_tag_versions(expected=VersionTag(major=4, minor=5, patch=6),
                                                            actual=self.mock_version.firmware.version))
        self.mock_version.assert_firmware_version(expected=VersionTag(major=4, minor=5, patch=6),
                                                  firmware=self.mock_version.firmware)
        # Validate Expected Failure
        self.assertRaises(KosmosFirmwareVersionError,
                          self.mock_version.assert_firmware_version,
                          expected=VersionTag(major=1, minor=2, patch=3),
                          firmware=self.mock_version.firmware)
    # end def test_firmware_version

    def test_fpga_revision(self):
        """
        Validate ``KosmosVersion.assert_fpga_revision`` method.
        """
        # Validate Expected Success
        self.assertTrue(self.mock_version.test_tag_versions(expected=VersionTag(major=4, minor=5, patch=6),
                                                            actual=VersionTag(major=4, minor=5, patch=6)))
        self.mock_version.assert_fpga_revision(expected=VersionTag(major=4, minor=5, patch=6),
                                               fpga=VersionTag(major=4, minor=5, patch=6))
        # Validate Expected Failure
        self.assertRaises(KosmosFpgaRevisionError,
                          self.mock_version.assert_fpga_revision,
                          expected=VersionTag(major=1, minor=2, patch=3),
                          fpga=VersionTag(major=4, minor=5, patch=6))
    # end def test_fpga_revision
# end class KosmosVersionTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
