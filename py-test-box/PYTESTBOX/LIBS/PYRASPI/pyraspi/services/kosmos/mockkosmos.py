#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.mockkosmos
:brief: Mock Kosmos implementation Class
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/03/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import KosmosInterface


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MockKosmos(KosmosInterface):
    """
    Mock Kosmos discovery and configuration.
    """
    class MockSequencerModule:
        """
        Mock sequencer module
        """
        def __init__(self):
            self.set_offline_mode = False
        # end def __init__

        def play_sequence(self, repetition=0, timeout=0, block=True):
            # See ``KosmosInterface.play_sequence``
            pass
        # end def play_sequence

        def wait_end_of_sequence(self):
            # See ``KosmosInterface.wait_end_of_sequence``
            pass
        # end def wait_end_of_sequence
    # end class MockSequencerModule

    sequencer: MockSequencerModule

    @staticmethod
    def get_instance():
        """
        Get MockKosmos singleton instance.
        Shall not instantiate ``MockKosmos`` object by any other way.

        :return: MockKosmos instance
        :rtype: ``MockKosmos``
        """
        if MockKosmos._instance is None:
            MockKosmos()
        # end if
        return MockKosmos._instance
    # end def get_instance

    def __init__(self):
        """
        :raise ``AssertionError``: If ``MockKosmos`` was already instantiated
        """
        assert MockKosmos._instance is None, 'A single MockKosmos instance is allowed!'

        # Setup MockKosmos and all related MockKosmos modules
        self.sequencer = MockKosmos.MockSequencerModule()
        MockKosmos._instance = self
    # end def __init__

    @staticmethod
    def is_connected():
        # See ``KosmosInterface.is_connected``
        return False
    # end def is_connected

    @staticmethod
    def discover_emulator(emulation_type, emulator_min_count=1):
        # See ``KosmosInterface.discover_emulator``
        return False
    # end def discover_emulator

    @staticmethod
    def has_capability(emulation_type=None, emulator_min_count=1):
        # See ``KosmosInterface.has_capability``
        return False
    # end def has_capability

    @staticmethod
    def get_capabilities():
        # See ``KosmosInterface.get_capabilities``
        return dict()
    # end def get_capabilities

    @staticmethod
    def is_fake():
        # See ``KosmosInterface.is_fake``
        return True
    # end def is_fake

    def get_status(self):
        # See ``KosmosInterface.get_status``
        return True
    # end def get_status

    def clear(self, force=False):
        # See ``KosmosInterface.clear``
        pass
    # end def clear
# end class MockKosmos
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
