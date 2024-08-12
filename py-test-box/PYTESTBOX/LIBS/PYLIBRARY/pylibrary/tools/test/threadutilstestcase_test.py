#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.threadutilstestcase

@brief Test case for thread utilities

@author christophe.roquebert

@date   2018/06/07
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

from pylibrary.tools.threadutils     import BasicExecutor
from pylibrary.tools.threadutils     import DLock
from pylibrary.tools.threadutils     import LockingProxy
from pylibrary.tools.threadutils     import ThreadedExecutor
from pylibrary.tools.threadutils     import synchronized
from pylibrary.tools.threadutils     import wait_for_any_lock
from threading                        import RLock
from threading                        import Thread
from pylibrary.tools.threadutils     import Task
from time                             import sleep
from unittest                         import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class ThreadUtilsTestCase(TestCase):
    '''
    TestCase fot the pylibrary.tools.threadutils module
    '''

    def test_synchronized(self):
        '''
        Tests the synchronized decorator
        '''

        quantum = 0.5

        # Simple call
        @synchronized
        def function1():
            '''
            A synchronized function that does nothing
            '''
            pass
        # end def function1

        function1()

        # Create 2 threads.
        # The first thread calls function2, increments value[0] and loops until stop[0] is True
        # The second thread calls function2, blocks.
        # The current thread checks that, after launching both threads
        # marker[0] is still False
        value  = [0]
        stop   = [False]

        @synchronized
        def function2():
            '''
            Wait until value is True
            '''
            value[0] += 1
            while (not stop[0]):
                pass
            # end while
        # end def function2

        thread1 = Thread(target = function2, name="UserThread 1")
        thread1.start()
        sleep(2*quantum)
        thread2 = Thread(target = function2, name="UserThread 2")
        thread2.start()
        sleep(2*quantum)

        self.assertNotEqual(0,
                            value[0],
                            "Thread 1 did not enter the synchronized function")
        self.assertNotEqual(2,
                            value[0],
                            "Thread 2 entered the synchronized function")
        stop[0] = True
        sleep(2*quantum)
        self.assertEqual(2,
                         value[0],
                         "Thread 2 did not enter the synchronized function")
    # end def test_synchronized

    def test_wait_for_any_lock(self):
        '''
        Test the wait_for_any_lock API
        '''

        quantum = 0.1

        # Create N locks, and N threads that lock them.
        # The main thread will wait for any of those locks to be released.
        nLocks = 10

        class LocalTask(object):
            '''
            A local task that locks the specified lock, and sleeps for value seconds
            '''
            def __init__(self, lock, value):
                '''
                Constructor.

                @param lock  [in] (Lock) The lock to handle.
                @param value [in] (int)  The number of seconds to wait.
                '''
                self._lock  = lock
                self._value = value
            # end def __init__

            def __call__(self):
                '''
                Functions that locks the specified lock, and sleeps for value seconds
                '''
                assert self._lock.acquire()

                sleep(self._value)

                self._lock.release()
            # end def __call__
        # end class LocalTask

        locks = set()
        tasks = []
        for unused in range(0, nLocks):
            lock = RLock()
            tasks.append(LocalTask(lock, 3*quantum))
            locks.add(lock)
        # end for

        self.assertEqual(nLocks,
                         len(locks),
                         "Invalid number of locks created")

        self.assertEqual(nLocks,
                         len(tasks),
                         "Invalid number of tasks created")

        def removingTask():
            '''
            Waits for locks and remove the
            '''
            sleep(quantum)
            while len(locks) > 0:
                lock = wait_for_any_lock(locks)
                locks.remove(lock)
                lock.release()
            # end while
        # end def removingTask
        thread = Thread(target = removingTask, name="Lock consumer")
        thread.start()

        executor = ThreadedExecutor(tasks,
                                    max_threads = nLocks,
                                    name       = "Lock worker")
        executor.execute()
    # end def test_wait_for_any_lock

    def test_LockingProxy(self):
        '''
        Tests the lockingProxy class (a destructor that unlocks a resource)
        '''

        # Create N threads that access the same resource through a lock

        nLocks = 2
        lock   = RLock()
        testObject = "1234"

        class LocalTask(object):
            '''
            Local task
            '''

            def __init__(self, localLock, localObject):
                '''
                Cosntructor.

                @param localLock   [in] (Lock)   The lock to acquire
                @param localObject [in] (str) The string to work on
                '''
                self._lock = localLock
                self._object = localObject
            # end def __init__

            def __call__(self):
                '''
                Worker function
                '''
                self._lock.acquire()
                lockingProxy = LockingProxy(self._object, self._lock, True)
                lockingProxy.find("23")
                lockingProxy = None
            # end def __call__
        # end class LocalTask

        tasks = []
        for unused in range(nLocks):
            tasks.append(LocalTask(lock, testObject))
        # end for

        executor = ThreadedExecutor(tasks,
                                    max_threads = nLocks,
                                    name       = "LockingProxy worker")
        executor.execute()

        # After 10 seconds, all lockingProxies should have been garbage collected
        self.assertNotEqual(None,
                            lock.acquire(False),
                            "LockingProxies did not release all locks")
    # end def test_LockingProxy

    def test_BasicExecutor(self):
        '''
        Tests the BasicExecutor class
        '''

        nTasks = 10
        value  = [0]
        def taskFunction():
            '''
            Task function. This increments value by 1
            '''
            value[0] += 1
        # end def taskFunction


        executor = BasicExecutor([taskFunction] * nTasks)
        executor.execute()

        self.assertEqual(nTasks,
                         value[0],
                         "Unexpected count: not all tasks executed")
    # end def test_BasicExecutor

    def test_ThreadedExecutor_execute(self):
        '''
        Tests the ThreadedExecutor when:
        - The executed threads take a long time to run.
        - Several tasks are queued
        - The @c Executor.execute method should block
        - No pause/stop is done

        The test takes at least 6 seconds to run.
        '''
        numTasks     = 60
        numThreads   = 6
        sleepQuantum = 0.01
        sleepCount   = 10

        class TaskClass(object):
            '''
            Task to execute
            '''
            def __init__(self, name):
                '''
                Constructor

                @param name [in] (str) The name of this task instance
                '''
                self.name = name
            # end def __init__

            def __call__(self):                                                                                         # pylint:disable=R0201
                '''
                Worker method, taking a loooong time to run.
                '''
                for unused in range(sleepCount):
                    sleep(sleepQuantum)
                # end for
            # end def __call__
        # end class TaskClass


        tasks = [TaskClass("Tasks #%d" % i) for i in range(numTasks)]

        from time import time
        tick = time()
        executor = ThreadedExecutor(tasks,
                                    max_threads = numThreads,
                                    name       = "ThreadedExecutorTest")
        executor.execute()

        tock = time()
        total = tock - tick
        self.assertEqual(True,
                         total > ((numTasks * sleepQuantum * sleepCount) / numThreads),
                         "The executor did not wait for all threads before exiting: took %s seconds" % total)
    # end def test_ThreadedExecutor_execute




    def test_ThreadedExecutor(self):
        '''
        Tests the BasicExecutor class
        '''

        nTasks   = 10
        nCount   = 3
        value    = [0]
        lock     = RLock()

        class TaskClass(object):
            '''
            Task class. This increments value by 1, 3 times
            '''
            def __init__(self):
                '''
                Constructor
                '''
                self.count = nCount
                self.lock  = RLock()
            # end def __init__

            def __call__(self):
                '''
                Worker method.

                @return The current task, until the count has reached the limit.
                '''
                assert lock.acquire()
                try:
                    assert self.lock.acquire()
                    try:
                        if (self.count > 0):
                            value[0]   += 1
                            self.count -= 1
                            return [self]
                        # end if
                    finally:
                        self.lock.release()
                    # end try

                finally:
                    lock.release()
                # end try
            # end def __call__
        # end class TaskClass

        tasks = []
        for unused in range(nTasks):
            tasks.append(TaskClass())
        # end for

        executor = ThreadedExecutor(tasks)
        executor.execute()

        self.assertEqual(nTasks * nCount,
                         value[0],
                         "Unexpected count: not all tasks executed")
    # end def test_ThreadedExecutor

    def _test_PauseResumeStop(self, executorClass, **kwargs):
        '''
        Tests an executor class, with the pause, resume and stop methods

        @param executorClass [in] (Executor) The executor class to test
        @param kwargs        [in] (dict) The keyword arguments passed to the constructor
        '''
        # there are 3 tasks, with lengths of 5 seconds each

        taskCount   = 3
        sleepFactor = 0.1

        tasks = []
        taskFlags = [None] * taskCount

        class TestTask(object):
            '''
            Worker class
            '''
            def __init__(self, index):
                '''
                Constructor

                @param index [in] (int) The index of the thread
                '''
                self._index = index
            # end def __init__

            def __call__(self):
                '''
                Worker method
                '''
                taskFlags[self._index] = False
                sleep(2 * sleepFactor)
                taskFlags[self._index] = True
            # end def __call__
        # end class TestTask

        for index in range(taskCount):
            tasks.append(TestTask(index))
        # end for

        # Create an executor instance, and run in a separate thread
        executor = executorClass(tasks, **kwargs)

        def threadProc():
            '''
            Executor runner
            '''
            executor.execute()
        # end def threadProc
        executorThread = Thread(target = threadProc,
                                name   = "Executor runner")
        executorThread.setDaemon(True)
        executorThread.start()

        # Wait for 1 second for the run to start
        sleep(1 * sleepFactor)

        self.assertEqual([False, None, None],
                         taskFlags,
                         "Invalid task state during run")

        # Pause the executor and wait
        executor.pause()
        sleep(2 * sleepFactor)

        try:
            self.assertEqual([True, None, None],
                             taskFlags,
                             "Executor incorrectly paused")

            # Resume the executor and wait
            executor.resume()
            sleep(1 * sleepFactor)

            self.assertEqual([True, False, None],
                             taskFlags,
                             "Executor incorrectly resumed")

            executor.stop()
            sleep(2 * sleepFactor)

            self.assertEqual([True, True, None],
                             taskFlags,
                             "Executor incorrectly stopped")
        finally:
            executor.stop()
        # end try
    # end def _test_PauseResumeStop


    def test_TE_PauseResumeStop(self):
        '''
        Tests an executor class, with the pause, resume and stop methods
        '''
        self._test_PauseResumeStop(ThreadedExecutor,
                                   max_threads = 1)
    # end def test_TE_PauseResumeStop

    def test_ME_PauseResumeStop(self):
        '''
        Tests an executor class, with the pause, resume and stop methods
        '''
        self._test_PauseResumeStop(BasicExecutor)
    # end def test_ME_PauseResumeStop

    def test_ME_ConcurrentPause(self):
        '''
        Tests an executor class, where:
        01. T=0    The test launches the ExecutorThread, that executes the Executor
        02. T=0+   The test sleeps for 2 quanta, waiting before executing 05
        03. T=0++  The Executor creates a child thread, that runs the SleepTask
        04. T=0+++ The SleepTask sleeps for 5 quanta, until event d' occurs
        05. T=2    The test pauses the executor
        06. T=2+   The test sleeps for 10 quanta
        07. T=5    The SleepTask completes
        08. T=5+   The SleepTask notifies the executor that it is complete
        09. T=5++  The SleepTask attempts to lock the _pause lock
        10. T=5++  AND The executor, noticing that no more tasks are being processed,
                   enqueues abort tasks before resuming execution.
        11. T=5+++ The tasks terminate (no more tasks to process), and the executor exits.
        12. T=10  The test attempts to resume the (already resumed and stopped) executor.
        '''

        quantum = 0.5

        taskSleepTime        = quantum * 5
        taskCount = 1
        afterStartSleepTime  = quantum * 2
        afterPauseSleepTime  = quantum * 10
        afterResumeSleepTime = quantum * taskCount * 2
        afterAllSleepTime    = quantum * taskCount

        def taskSleep():
            '''
            Sleeps for x seconds
            '''
            sleep(taskSleepTime)
        # end def taskSleep

        tasks = [Task(taskSleep) for _ in range(taskCount)]

        def setMarker(marker, value):
            '''
            Sets the specified marker to value

            @param marker [in] (list)   The marker to set
            @param value  [in] (object) The value to set
            '''
            marker[0] = value
        # end def setMarker

        startMarker   = [False]
        suspendMarker = [False]
        resumeMarker  = [False]
        stopMarker    = [False]

        executor = ThreadedExecutor(tasks,
                                    on_start           = lambda: setMarker(startMarker,   True),
                                    on_suspend         = lambda: setMarker(suspendMarker, True),
                                    on_resume          = lambda: setMarker(resumeMarker,  True),
                                    on_stop            = lambda: setMarker(stopMarker,    True),
                                    max_threads        = 1,
                                    name              = "Concurrent Pause",
                                    post_execute_thread = lambda: sleep(3))


        marker = [False]
        def executorRunner():
            '''
            ThreadProc for the executor runner.

            sets a marker when the executor has exited.
            '''
            executor.execute()
            marker[0] = True
        # end def executorRunner

        # The executor will run from a separate thread, so as not to block
        # this test.
        thread1 = Thread(target = executorRunner, name="Executor launcher")
        thread1.start()
        sleep(afterStartSleepTime)

        self.assertEqual(True,
                         startMarker[0],
                         "Executor not started")
        self.assertEqual(False,
                         suspendMarker[0],
                         "Executor suspended")
        self.assertEqual(False,
                         resumeMarker[0],
                         "Executor resumed")
        self.assertEqual(False,
                         stopMarker[0],
                         "Executor stopped")
        executor.pause()
        sleep(afterPauseSleepTime)

        try:
            self.assertEqual(True,
                             startMarker[0],
                             "Executor not started")
            self.assertEqual(False, # Normal: the task has finished sooner before the pause.
                             suspendMarker[0],
                             "Executor suspended")
            self.assertEqual(False,
                             resumeMarker[0],
                             "Executor resumed")
            self.assertEqual(True,
                             stopMarker[0],
                             "Executor not stopped")
        finally:
            executor.resume()
        # end try
        sleep(afterResumeSleepTime)

        self.assertEqual(True,
                         startMarker[0],
                         "Executor not started")
        self.assertEqual(False,
                         suspendMarker[0],
                         "Executor not suspended")
        self.assertEqual(False,
                         resumeMarker[0],
                         "Executor not resumed")
        self.assertEqual(True,
                         stopMarker[0],
                         "Executor not stopped")

        sleep(afterAllSleepTime)

        self.assertEqual(True,
                         marker[0],
                         "The executor did not complete normally (Probable deadlock)")
    # end def test_ME_ConcurrentPause

    def test_DLock(self):
        '''
        Tests the DLock object
        '''

        lock = DLock()
        self.assertEqual(True,
                         lock.acquire(False),
                         "Lock should have been acquired")
        self.assertEqual(True,
                         lock.acquire(False),
                         "Lock should have been acquired")

        lock.release()
        lock.release()
        lock = None
    # end def test_DLock

    def test_DLock_Blocked(self):
        '''
        Tests the DLock object
        '''

        lock = DLock()
        quantum = 0.1

        def blocker():
            '''
            A blocking method, that acquires a lock for 5 seconds
            '''
            lock.acquire()
            sleep(5*quantum)
            lock.release()
        # end def blocker

        thread = Thread(target=blocker, name="Lock blocker")
        thread.start()
        sleep(1*quantum)

        self.assertEqual(False,
                         lock.acquire(False),
                         "Could acquire an already locked lock")
        lock.acquire()

        lock.release()
        lock = None
    # end def test_DLock_Blocked
# end class ThreadUtilsTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
