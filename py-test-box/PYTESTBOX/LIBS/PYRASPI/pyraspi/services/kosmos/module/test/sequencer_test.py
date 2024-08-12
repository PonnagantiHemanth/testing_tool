#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.sequencer_test
:brief: Kosmos Sequencer Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from random import randint
from random import seed

from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.module import StatusResetModuleBaseClass
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SEQUENCER_CMD_STATUS_SIZE
from pyraspi.services.kosmos.protocol.generated.messages import PES_TIMER_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import bas_status_t
from pyraspi.services.kosmos.protocol.generated.messages import i2c_spy_status_t
from pyraspi.services.kosmos.protocol.generated.messages import kbd_matrix_status_t
from pyraspi.services.kosmos.protocol.generated.messages import led_spy_status_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_cpu_status_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_status_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_timer_status_t
from pyraspi.services.kosmos.protocol.generated.messages import sequencer_state_e
from pyraspi.services.kosmos.protocol.generated.messages import sequencer_status_t
from pyraspi.services.kosmos.test.common_test import KosmosCommonTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@require_kosmos_device(DeviceName.SEQUENCER)
class SequencerModuleTestCase(KosmosCommonTestCase):
    """
    Kosmos Sequencer Module Test Class.
    """
    def test_call_all(self):
        """
        Call each module connected to Sequencer module
        """
        # Validate remote status
        for module in self.kosmos.dt.flatmap.values():
            if isinstance(module, StatusResetModuleBaseClass):
                module.status()
            # end if
        # end for
    # end def test_call_all

    def test_sequencer_status_t(self):
        """
        Validate ``sequencer_status_t`` structure is correctly defined and no bitfield overlaps.
        """
        seed(42)
        for i in range(100):
            test_bytes = [randint(0x01, 0xFF) for _ in range(MSG_ID_SEQUENCER_CMD_STATUS_SIZE)]

            # Refer to sequencer_status_t in pyraspi/services/kosmos/protocol/definitions/data/internals.h
            # Byte 0, bits 0-2
            state = sequencer_state_e(test_bytes[0])
            # Bytes 1-4
            pes = pes_status_t.from_buffer_copy(bytes(test_bytes[1:5]))
            # Bytes 5-8
            kbd_matrix = kbd_matrix_status_t.from_buffer_copy(bytes(test_bytes[5:9]))
            # Bytes 9-10
            bas = bas_status_t.from_buffer_copy(bytes(test_bytes[9:11]))
            # Byte 11
            pes_cpu = pes_cpu_status_t.from_buffer_copy(bytes(test_bytes[11:12]))
            # Bytes 12-15
            pes_timers = (pes_timer_status_t * 4)()  # Create a ctypes array of 4 timer statuses
            for timer_idx in range(PES_TIMER_COUNT):
                pes_timers[timer_idx] = pes_timer_status_t.from_buffer_copy(bytes([test_bytes[12 + timer_idx]]))
            # end for
            # Bytes 16-21
            led_spy = led_spy_status_t.from_buffer_copy(bytes(test_bytes[16:22]))
            # Bytes 22-25
            i2c_spy = i2c_spy_status_t.from_buffer_copy(bytes(test_bytes[22:26]))

            sequencer_status = sequencer_status_t(state=state,
                                                  pes=pes,
                                                  kbd_matrix=kbd_matrix,
                                                  bas=bas,
                                                  pes_cpu=pes_cpu,
                                                  pes_timer=pes_timers,
                                                  led_spy=led_spy,
                                                  i2c_spy=i2c_spy)

            msg = f'test_iteration={i}\ntest_bytes={test_bytes}\nsequencer_status={sequencer_status!s}'
            self.assertEqual(bytes(test_bytes), bytes(sequencer_status), msg=msg)
            self.assertEqual(state.value, sequencer_status.state, msg=msg)
            self.assertEqual(pes, sequencer_status.pes, msg=msg)
            self.assertEqual(kbd_matrix, sequencer_status.kbd_matrix, msg=msg)
            self.assertEqual(bas, sequencer_status.bas, msg=msg)
            for timer_idx in range(PES_TIMER_COUNT):
                self.assertEqual(pes_timers[timer_idx], sequencer_status.pes_timer[timer_idx],
                                 msg=msg + f'\ntimer_idx={timer_idx}')
            # end for
            self.assertEqual(led_spy, sequencer_status.led_spy, msg=msg)
            self.assertEqual(i2c_spy, sequencer_status.i2c_spy, msg=msg)
        # end for
    # end def test_sequencer_status_t
# end class SequencerModuleTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
