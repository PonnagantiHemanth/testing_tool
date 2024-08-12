#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.profiling

@brief  Profiling tools

@author christophe.roquebert

@date   2018/11/25
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from collections                        import deque
from time                               import time
import sys
import threading

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

# pylint:disable=C0103
try:
    from resource                       import RUSAGE_SELF                                                              # pylint:disable=F0401
    from resource                       import getrusage                                                                # pylint:disable=F0401
except ImportError:
    RUSAGE_SELF = 0
    def getrusage(who   = 0):                                                                                           # pylint:disable=W0613
        '''
        Return fake values for non-unix platforms of CPU usage

        @option who [in] (int) who requested the usage.

        @return (tuple) CPU usage
        '''
        return [0.0, 0.0] # on non-UNIX platforms cpu_time always 0.0
    # end def getrusage
# end try

p_stats = None
p_start_time = None

def profiler(frame, event, arg):                                                                                        # pylint:disable=W0613
    '''
    Main profiling API.

    @param  frame [in] (Frame)   The frame object for which the profiler was called.
    @param  event [in] (Event)   The event for which the profiler was called.
    @param  arg   [in] (unknown) Unused

    @return The profiler method.
    '''
    if (event not in ('call', 'return')):
        return profiler
    # end if

    #### gather stats ####
    rusage = getrusage(RUSAGE_SELF)
    t_cpu = rusage[0] + rusage[1] # user time + system time
    code = frame.f_code
    fun = (code.co_name, code.co_filename, code.co_firstlineno)
    #### get stack with functions entry stats ####
    ct = threading.currentThread()
    try:
        p_stack = ct.p_stack
    except AttributeError:
        ct.p_stack = deque()
        p_stack = ct.p_stack
    # end try

    #### handle call and return ####
    if (event == 'call'):
        p_stack.append((time(), t_cpu, fun))

    elif (event == 'return'):
        try:
            t, t_cpu_prev, f = p_stack.pop()
            assert (f == fun)
        except IndexError: # TODO investigate
            t, t_cpu_prev, f = p_start_time, 0.0, None
        # end try

        call_cnt, t_sum, t_cpu_sum = p_stats.get(fun, (0, 0.0, 0.0))
        p_stats[fun] = (call_cnt+1, t_sum+time()-t, t_cpu_sum+t_cpu-t_cpu_prev)

    # end if

    return profiler

# end def profiler

def profile_on():
    '''
    Activates profiling.
    '''
    global p_stats, p_start_time                                                                                        # pylint:disable=W0603
    p_stats = {}
    p_start_time = time()
    threading.setprofile(profiler)
    sys.setprofile(profiler)
# end def profile_on

def profile_off():
    '''
    Deactivate profiling.
    '''
    threading.setprofile(None)
    sys.setprofile(None)
# end def profile_off

def get_profile_stats():
    '''
    @return dict[function_tuple] -> stats_tuple
    where
      function_tuple = (function_name, filename, lineno)
      stats_tuple = (call_cnt, real_time, cpu_time)
    '''
    return p_stats
# end def get_profile_stats

#### EXAMPLE ##################################################################


#def test_function():
#    pass
#
#class T(Thread):
#    def __init__(self):
#        Thread.__init__(self)
#    def run(self):                  # takes about 5 seconds
#        for i in xrange(100):
#            self.test_method()
#            test_function()
#    def test_method(self):
#        sleep(random.random() / 10)
#
#profile_on()
########################
#threads = [T() for i in xrange(3)]
#for t in threads:
#    t.start()
#for i in xrange(100):
#    test_function()
#for t in threads:
#    t.join()
########################
#profile_off()
#
#pprint(get_profile_stats())

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
