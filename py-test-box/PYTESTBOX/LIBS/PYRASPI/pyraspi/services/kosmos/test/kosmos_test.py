#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.kosmos_test
:brief: Tests for Kosmos class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/22
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.services.kosmos.protocol.generated.messages import SEQUENCER_STATE_RESET_DONE
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_t
from pyraspi.services.kosmos.test.common_test import KosmosCommonTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class KosmosTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos class.
    """
    def test_get_instance(self):
        """
        Validate get_instance() method.
        """
        self.assertEqual(self.kosmos, self.kosmos.get_instance())
    # end def test_get_instance

    def test_is_connected(self):
        """
        Validate is_connected() method.
        """
        self.assertTrue(self.kosmos.is_connected())
    # end def test_is_connected

    def test_has_capability(self):
        """
        Validate has_capability() method.
        """
        for dev_name in DeviceName:
            self.assertEqual(bool(self.kosmos.dt[dev_name]),
                             self.kosmos.has_capability(emulation_type=dev_name),
                             msg=(dev_name.name, self.kosmos.dt[dev_name]))
        # end for
        for dev_family in DeviceFamilyName:
            self.assertEqual(any(bool(self.kosmos.dt[dev_name]) for dev_name in dev_family),
                             self.kosmos.has_capability(emulation_type=dev_family),
                             msg=(dev_family.name, {dev.name: self.kosmos.dt[dev] for dev in dev_family}))
        # end for
    # end def test_has_capability

    def test_get_status(self):
        """
        Validate get_status() method.
        """
        self.kosmos.get_status()
    # end def test_get_status

    def test_clear_local(self):
        """
        Validate clear() method, on local buffers, with remote sequence not running.
        """
        # Fill each local buffers with instructions
        self.kosmos.dt.pes.append(data=pes_instruction_t())
        self.kosmos.dt.pes_cpu.action(cpu_event=self.kosmos.dt.pes_cpu.cpu_event.NOP_EVENT)

        # Validate local buffer length
        self.assertEqual(3, self.kosmos.dt.pes.length())
        self.assertEqual(1, self.kosmos.dt.pes_cpu.length())

        # Buffer clear
        self.kosmos.clear()

        # Validate local module clear operation (buffer reset)
        self.assertEqual(0, self.kosmos.dt.pes.length())
        self.assertEqual(0, self.kosmos.dt.pes_cpu.length())
    # end def test_clear_local

    def test_clear_remote(self):
        """
        Validate clear() method on remote modules, after remote sequence has terminated.
        """
        # Fill remote timer buffers
        self.kosmos.dt.timers.save(timers=TIMER)

        # Start sequence
        self.kosmos.dt.sequencer.play_sequence()

        # Validate remote Timers module: buffer are not empty
        status = self.kosmos.dt.timers.status()
        for t in TIMER:
            self.assertEqual(1, status[t].buffer_count, msg=(t, status))
        # end for

        # Buffer clear
        self.kosmos.clear()

        # Validate remote Timers module: buffer reset
        status = self.kosmos.dt.timers.status()
        for t in TIMER:
            self.assertEqual(0, status[t].buffer_count, msg=(t, status))
        # end for
    # end def test_clear_remote

    def test_clear_remote_force(self):
        """
        Validate clear(force=True) method on remote modules, while remote sequence is still running.
        """
        buffer_fill = 10

        # Fill each local buffers with instructions
        self.kosmos.dt.timers.save(timers=TIMER)       # PES TIMERS buffers (+1 PES:MARKER instruction)
        self.kosmos.dt.pes.wait_go_signal()            # PES buffer (1 PES:WAIT instruction)
        self.kosmos.dt.pes_cpu.action(cpu_event=self.kosmos.dt.pes_cpu.cpu_event.NOP_EVENT)  # PES_CPU(+2 PES:EXEC/WAIT)
        # fill PES, KBD_MATRIX, BAS FIFOs plus 10 instructions waiting in buffers
        for _ in range(self.kosmos.dt.pes.settings.fifo_size + buffer_fill):
            self.kosmos.dt.pes.execute(action=self.kosmos.dt.pes.action_event.NOP_EVENT)
        # end for

        # Validate local buffer length
        self.assertEqual(4 + self.kosmos.dt.pes.settings.fifo_size + buffer_fill, self.kosmos.dt.pes.length())
        self.assertEqual(1, self.kosmos.dt.pes_cpu.length())

        # Start sequence and make Sequencer stall on PES:WAIT:GO instruction
        self.kosmos.dt.sequencer.play_sequence(block=False)
        self.assertFalse(self.kosmos.dt.sequencer.is_end_of_sequence())

        # Validate remote buffers contains data (producer module)
        status = self.kosmos.dt.sequencer.status()
        for t in TIMER:
            self.assertEqual(1, status.pes_timer[t].buffer_count, msg=(t, status))
        # end for
        # Validate remote buffers contains instructions (consumer module)
        self.assertEqual(4 + buffer_fill, status.pes.buffer_count, msg=status)
        self.assertEqual(1, status.pes_cpu.buffer_count, msg=status)

        # Call default Kosmos clear method (expect exception)
        with self.assertRaisesRegex(AssertionError, r'Sequencer Reset was prevented'):
            self.kosmos.clear()  # default parameter is force=False
        # end with

        # Call default Kosmos clear method (expect exception)
        with self.assertRaisesRegex(AssertionError, r'Sequencer Reset was prevented'):
            self.kosmos.clear(force=False)
        # end with

        # Call Kosmos clear method (force-clear)
        self.kosmos.clear(force=True)

        # Sequencer should not be reset at this stage
        status = self.kosmos.dt.sequencer.status()
        self.assertEqual(SEQUENCER_STATE_RESET_DONE, status.state, msg=status)

        # Validate remote buffers are now empty
        for t in TIMER:
            self.assertEqual(0, status.pes_timer[t].buffer_count, msg=(t, status))
        # end for
        self.assertEqual(0, status.pes.buffer_count, msg=status)
        self.assertEqual(0, status.pes_cpu.buffer_count, msg=status)
    # end def test_clear_remote_force
# end class KosmosTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
