#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.system.test.basedevicetestcase

@brief Base test case for device classes

@author christophe.roquebert

@date   2018/01/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from shutil import rmtree
from threading import Lock
from threading import RLock
from time import sleep
from unittest import TestCase

from pylibrary.tools.tempfile import mkdtemp
from pylibrary.tools.threadutils import ThreadedExecutor
from pylibrary.tools.threadutils import synchronized

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

SYNCHRONIZATION_LOCK = RLock()

class AbstractDeviceTestCase(TestCase):                                                                                  # pylint:disable=R0901
    '''
    Base class for classes that implement a device interface.

    Having a common base class for interface tests guarantees a consistent
    behaviour between instances.

    In order to test specific implementations, derived classes must override
    the getClass method.
    '''

    DEVICE_NUMBER = 0

    def _isAbstract(self):
        '''
        Checks whether the current test is virtual

        @return True for types other than AbstractDeviceTestCase
        '''
        return self.__class__.__name__.startswith('Abstract')
    # end def _isAbstract

    def getClass(self):
        '''
        Returns the class type for the object to test.

        This is NOT an instance, it is up to the caller to create the instance.

        @return the class type for the object to test.
        '''
        raise NotImplementedError
    # end def getClass

    def setUp( self ):
        '''
        Initialize test.
        '''
        TestCase.setUp(self)

        self.silentConfigure = False
    # end def setUp

    @synchronized(SYNCHRONIZATION_LOCK)
    def test_AllocateDeallocate(self):
        '''
        Tests the allocation/deallocation of a device.
        '''

        if not self._isAbstract():

            clazz = self.getClass()
            device = clazz(self.DEVICE_NUMBER)

            device.allocate()
            device.unallocate()
        # end if
    # end def test_AllocateDeallocate

    @synchronized(SYNCHRONIZATION_LOCK)
    def test_AllocateDeallocatePowerUp(self):
        '''
        Tests allocation/powerUp/deallocation
        '''

        if not self._isAbstract():

            clazz = self.getClass()
            device = clazz(self.DEVICE_NUMBER)

            self.assertRaises(Exception,
                              device.powerUp)

            device.allocate()

            device.powerUp()
            self.assertEqual(True,
                             device.isPoweredUp(),
                             "Device is not powered up as it should")

            device.unallocate()

            self.assertRaises(Exception,
                              device.powerUp)
        # end if
    # end def test_AllocateDeallocatePowerUp

    @synchronized(SYNCHRONIZATION_LOCK)
    def test_PowerUpResetPowerDown(self):
        '''
        Tests the powerUp/reset/powerDown cycle of a device.
        '''

        if not self._isAbstract():

            clazz = self.getClass()
            device = clazz(self.DEVICE_NUMBER)

            device.allocate()
            try:
                device.powerUp()
                device.reset()
                device.powerDown()
            finally:
                device.unallocate()
            # end try
        # end if
    # end def test_PowerUpResetPowerDown

    @synchronized(SYNCHRONIZATION_LOCK)
    def test_getDriverInfo(self):
        '''
        Tests the getDriverInfo command
        '''
        if not self._isAbstract():

            clazz = self.getClass()
            device = clazz(self.DEVICE_NUMBER)

            device.allocate()
            try:
                driverInfos = device.getDriverInfo()

                keys = ("NAME",
                        "VERSION",
                        )
                for key in keys:
                    self.assertEqual(True,
                                     key in driverInfos,
                                     "Key %s not found in driver infos" % key)

                    self.assertNotEqual(None,
                                        driverInfos[key],
                                        "None value for key: %s" % key)
                # end for
            finally:
                device.unallocate()
            # end try
        # end if
    # end def test_getDriverInfo

    @synchronized(SYNCHRONIZATION_LOCK)
    def test_Configure(self):
        '''
        Tests the configure method of the device class.
        '''

        if not self._isAbstract():

            tempdir = mkdtemp()
            try:
                clazz = self.getClass()

                if self.silentConfigure:
                    clazz.configure(path=tempdir)
                else:
                    self.assertRaises(ValueError,
                                      clazz.configure,
                                      path=tempdir)
                # end if
            finally:
                rmtree(tempdir, True)
            # end try
        # end if
    # end def test_Configure

    @synchronized(SYNCHRONIZATION_LOCK)
    def test_MultithreadedAccess(self):
        '''
        Tests a multithreaded access to the first device.

        Specifically, this validates that a device:
        - That is allocated in Thread1
        - That is accessed in Thread2
        - That is unallocated in Thread3
        is still available.
        '''
        if not self._isAbstract():
            clazz = self.getClass()
            locks  = [Lock() for unused in range(4)]
            for lock in locks:
                lock.acquire()
            # end for



            device = [None]
            def task0():
                '''
                Releases the first lock after 2 seconds
                '''
                sleep(2)
                locks[0].release()
            # end def task0

            def task1():
                '''
                Creates the first device
                '''
                locks[0].acquire()
                device[0] = clazz(self.DEVICE_NUMBER)
                locks[0].release()
                locks[1].release()
            # end def task1

            def task2():
                '''
                Allocates the first device
                '''
                locks[1].acquire()
                try:
                    device[0].allocate()
                    locks[1].release()
                    locks[2].release()
                except Exception:                                                                                           # pylint:disable=W0703
                    for lock in locks:
                        try:
                            lock.release()
                        except Exception:                                                                                   # pylint:disable=W0703
                            pass
                        # end try
                    # end for
                # end try
            # end def task2

            def task3():
                '''
                Powers up the first device
                '''
                locks[2].acquire()
                device[0].powerUp()
                locks[2].release()
                locks[3].release()
            # end def task3

            def task4():
                '''
                Unallocates the first device
                '''
                locks[3].acquire()
                device[0].unallocate()
                locks[3].release()
            # end def task4

            tasks = [task0, task1, task2, task3, task4]
            executor = ThreadedExecutor(tasks,
                                        max_threads = len(tasks),
                                        name       = "MultithreadedReaderAccessTest")
            executor.execute()
        # end if
    # end def test_MultithreadedAccess
# end class AbstractDeviceTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
