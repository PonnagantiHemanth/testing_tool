#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.context
:brief:  Context implementation
         The context provides access to global, read-only information, that the test should not modify.
:author: christophe.roquebert <croquebert@logitech.com>
:date: 2018/09/11
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from copy import deepcopy
from os import R_OK
from os import access
from os import listdir
from os import makedirs
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import isabs
from os.path import join
from os.path import normpath
from os.path import sep
from threading import Lock
from threading import RLock

from pyharness.consts import DEFAULT_INPUT_DIRECTORY
from pyharness.consts import DEFAULT_OUTPUT_DIRECTORY
from pyharness.debuggers import DEBUGGERS_MAPPING
from pyharness.subsystem.ini.subsysteminstantiationconnector import IniSubSystemInstantiationImporter
from pyharness.subsystem.python.subsystemdefinitionconnector import PythonSubSystemDefinitionImporter
from pyharness.subsystem.subsystembuilder import SubSystemBuilder
from pyharness.subsystem.subsystemdefinitionconnector import SubSystemDefinitionImporterComposite
from pyharness.subsystem.subsysteminstantiationconnector import SubSystemInstantiationImporterComposite
from pyharness.subsystem.xml.subsysteminstantiationconnector import XmlSubSystemInstantiationImporter
from pylibrary.emulator.emulatorinterfaces import EmulatorInterface
from pylibrary.tools.config import ConfigParser
from pylibrary.tools.importutils import getResourceStream
from pylibrary.tools.importutils import importFqn
from pylibrary.tools.threadutils import LockingProxy
from pylibrary.tools.threadutils import wait_for_any_lock


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
DEFAULT_CONFIG_HEADER = '''\
# ------------------------------------------------------------------------------
# This is the main configuration file for your validation project.
#
# This file is divided into four main sections, allowing you to customize each
# validation run.
# This file can be overridden by version-specific configuration files, local to
# the current machine, located in LOCAL/Settings.ini
# 
# 1. The [PRODUCT] section.
# This section contains the value for the product currently under test.
# 
# Example:
# [PRODUCT]
# value = "PYTESTBOX"
# 
# 2. The [VARIANT] section.
# This section contain the value for the product's version currently under test.
# 
# Example:
# [VARIANT]
# value = "AUTO_TESTS"
#
# ------------------------------------------------------------------------------\n''' # Hack for py2dox

DEFAULT_CONFIG_TEMPLATE = '''
[PRODUCT]
value = None

[VARIANT]
value = None
'''


class FeaturesProvider(object):                                                                                         # pylint:disable=R0922
    '''
    An object able to give access to a root feature
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor

        @param  args   [in] (tuple) arguments
        @param  kwargs [in] (dict) keyword arguments
        '''
        pass
    # end def __init__

    def getFeatures(self):
        '''
        Obtains the root feature.

        @return The root feature
        '''
        raise NotImplementedError
    # end def getFeatures
# end class FeaturesProvider

class AContext(FeaturesProvider):
    r'''
    Provides access to a test context: features, debuggers, devices...

    The global context is initialized by the framework.
    The core runner in the TestCase class initializes a run-specific context,
    which can be obtained by the @c TestCase.getContext method.

    Specialized test classes may provide utility methods to access specific
    instances of the objects provided by the context.

    The context provides access to:
    - Debuggers, as specified in the features under the RUNTIME subsystem
    - SmartDevices, as specified in the features under the RUNTIME subsystem
    - Input directory(ies), as specified by:
      - The Settings.ini file (PRODUCT, VARIANT)
      - The features file (pattern to use, in F_InputDirPattern and F_OutputDirPattern)
      .
    .

    <b>Locked resources</b>

    Resources are locked on a per-thread basis: A thread that needs to access,
    say, a SmartDevice only needs to use the @c getDevice API.

    However, for this to work, the underlying framework needs to ensure that
    non-threadsafe resources are only provided one thread at a time.
    For the sake of efficiency, matches against the same predicated are cached
    across threads.

    The algorithm used to provide such locked resources uses three sets of key/locks:
    - The first set contains locks on resources known to be valid for the given predicate
    - The second set contains locks on resources known to be invalid for the given predicate
    - The third set contains locks on resources as yet unknown for the given predicate
    .

    The algorithm is as follows:
    @dot
    digraph G
    {
        graph [bgcolor=transparent]
        node    [fontname=Arial, fontsize = 10, align=center, shape=diamond, width=1.0, style=filled bgcolor="#FFFFFF"];
        edge    [fontname=Arial, fontsize = 8, len=0.5];
        ranksep = 0.1;
        rankdir = TB;

        {
            rankdir = LR;
            rank    = same;

            INITIALIZATION   [label="Initialization", shape=box, bgcolor=white];
        }

        {
            rankdir = LR;
            rank    = same;

            KEYINCACHE       [label="Key in cache", shape=diamond];
            KEYINCACHECORNER [shape=point, width=0.0];
        }

        {
            rankdir = LR;
            rank    = same;

            INSERTKEYINCACHE [label="Insert key in cache:\l- invalid locks: empty\l- valid locks: empty\l- unknown locks: all", shape=box];
        }

        {
            rankdir = LR;
            rank    = same;

            PREEXTRACT1      [shape=point, width=0.0];
            PREEXTRACT2      [shape=point, width=0.0];
            PREEXTRACT3      [shape=point, width=0.0];
        }

        {
            rankdir = LR;
            rank    = same;

            EXTRACTLOCKSFROMCACHE       [label="Extract locks from cache\l- valid locks \l- unknown locks\l", shape=box];
        }

        {
            rankdir = LR;
            rank    = same;

            RETURNNONE    [label="Return None", shape=box, style=filled, color="#CC4C4C"];
            NOMORE        [label="No valid or\nunknown locks ?", shape=diamond];
        }

        {
            rankdir = LR;
            rank    = same;

            WAIT [label="Wait for\l- valid locks\l- unknown locks", shape=box];
        }

        {
            rankdir = LR;
            rank    = same;

            LOCKUNKNOWN        [label="Lock is unknown", shape=diamond];
            RETURNOBJECT1      [label="Return locked object", shape=box, style=filled, color="#66CC99"];
        }

        {
            rankdir = LR;
            rank    = same;

            APPLYPREDICATE     [label="Apply predicate", shape=box];
        }

        {
            rankdir = LR;
            rank    = same;

            MATCHPREDICATE        [label="Predicate matches ?", shape=diamond];
        }

        {
            rankdir = LR;
            rank    = same;

            VALIDPREDICATE        [label="Move lock to valid locks\lRemove lock from unknown locks", shape=box];
            INVALIDPREDICATE      [label="Move lock to invalid locks\lRemove lock from unknown locks", shape=box];
        }

        {
            rankdir = LR;
            rank    = same;

            RELEASELOCKCORNER     [shape=point, width=0.0];
            RELEASELOCK           [label="Release lock", shape=box];
            RETURNOBJECT2         [label="Return locked object", shape=box, style=filled, color="#66CC99"];
        }

        INITIALIZATION         -> KEYINCACHE;
        KEYINCACHE             -> KEYINCACHECORNER      [label="          Yes", dir=none];
        KEYINCACHECORNER       -> PREEXTRACT3           [dir=none];
        KEYINCACHE             -> INSERTKEYINCACHE      [label="  No", dir=none];
        INSERTKEYINCACHE       -> PREEXTRACT2           [dir=none];
        PREEXTRACT1            -> RELEASELOCKCORNER     [dir=none];
        PREEXTRACT1            -> PREEXTRACT2           [dir=none];
        PREEXTRACT2            -> PREEXTRACT3           [dir=none];
        PREEXTRACT2            -> EXTRACTLOCKSFROMCACHE;

        EXTRACTLOCKSFROMCACHE  -> NOMORE;
        NOMORE                 -> RETURNNONE            [label="  Yes"];
        NOMORE                 -> WAIT                  [label="  No"];
        WAIT                   -> LOCKUNKNOWN;
        LOCKUNKNOWN            -> RETURNOBJECT1         [label="  No"];
        LOCKUNKNOWN            -> APPLYPREDICATE        [label="  Yes"];

        APPLYPREDICATE         -> MATCHPREDICATE;

        MATCHPREDICATE         -> INVALIDPREDICATE      [label="  No"];
        MATCHPREDICATE         -> VALIDPREDICATE        [label="  Yes"];

        INVALIDPREDICATE       -> RELEASELOCK;
        VALIDPREDICATE         -> RETURNOBJECT2;

        RELEASELOCKCORNER      -> RELEASELOCK           [dir=none];

    }
    @enddot
    '''

    ## Object locks. The entry 0 is reserved as a reference contents.
    DEVICE_LOCKS         = {}
    SYNCHRONIZATION_LOCK    = Lock()
    INT_PREDICATES          = {}

    def __init__(self, rootFeatures,
                       smartDevices = None,
                       debuggers  = None,
                       config     = None,
                       manualUi   = None):
        '''
        Constructor

        @param  rootFeatures [in]  (AbstractSubSystem) The root element of the
                                   features tree. This element has sub-features,
                                   such as RUNTIME as its attributes.
        @option smartDevices   [in]  (tuple) Device instances list
        @option debuggers    [in]  (tuple) Debuggers instances list
        @option config       [in]  (ConfigParser) Configuration of the context
        @option manualUi     [in]  (callable) An API callback used to check manual TestCase.
                                   It depends on the currentUI
        '''
        super(AContext, self).__init__()

        self.__features   = rootFeatures

        if smartDevices is None or isinstance(smartDevices, dict):
            self.__smartDevices = []
            objectDict = smartDevices or {}
            for key in sorted(objectDict.keys()):
                self.__smartDevices.append((RLock(), objectDict[key],))
            # end for
        else:
            self.__smartDevices = smartDevices
        # end if
        self.__smartDevicePredicates = []

        if debuggers is None or isinstance(debuggers, dict):
            self.__debuggers = []
            objectDict = debuggers or {}
            for key in sorted(objectDict.keys()):
                self.__debuggers.append((RLock(), objectDict[key],))
            # end for
        else:
            self.__debuggers = debuggers
        # end if
        self.__debuggerPredicates = []

        self.__config     = config
        self.abort        = False
        self.kill         = False
        self.filter       = lambda test, context = None: True
        self.sorter       = lambda x, y: 0

        # A cache of smartdevice keys, used in conjunction with predicates
        self.__smartDeviceKeyCache = {}

        # The API that will be called to validate manual TestCases
        self.manualTestCaseUi = manualUi

        self._keyCache = {}

        self._threads = 1

        self._parent = None

    # end def __init__

    def getParent(self):
        '''
        Get parent

        @return (AContext) Parent link
        '''
        return self._parent
    # end def getParent

    def setParent(self, parent):
        '''
        Set link to parent

        @param  parent [in] (AContext) Link to parent
        '''
        if not isinstance(parent, AContext):
            raise TypeError('Wrong parent type: %s. Should be AContext instead')
        # end if
        self._parent = parent
    # end def setParent

    parent = property(getParent, setParent)

    def getThreadCount(self):
        '''
        Get thread count for this run

        @return (int) Thread count
        '''
        return self._threads
    # end def getThreadCount

    def __del__(self):
        '''
        Destructor
        '''
        self.close()
    # end def __del__

    def __str__(self):
        '''
        Converts the current object to its string representation

        @return The current context, as a readable string
        '''
        try:
            return "%s/%s/%s (%s)" % (self.getCurrentProduct(),
                                      self.getCurrentVariant(),
                                      self.getCurrentTarget(),
                                      self.getCurrentMode())
        except Exception:                                                                                               # pylint:disable=W0703
            return "Unable to obtain context contents"
        # end try
    # end def __str__

    def __repr__(self):
        '''
        Obtains a representation of the current object

        @return The current object, as a string.
        '''
        return str(self)
    # end def __repr__

    def getLockedObject(self, lockObjectPairs,                                                                          # pylint:disable=R0912
                              predicate):
        '''
        Obtains a locked object for the given predicate.
        If no locked object matches the predicate, returns None.

        This method is BLOCKING.

        This uses an internal cache for storing lock objects associated with
        predicates.

        @param  lockObjectPairs [in] (tuple<tuple<lock, object>>) containing pairs
                                    of Lock instance and object instance.
        @param  predicate       [in] (callable) The predicate that is used to lookup the object.

        @return a LockingProxy wrapping one of the objects, on its associated lock.
        '''

        # Step 0: If the predicate is an int, directly access the lock and object
        if (isinstance(predicate, int)):
            if (predicate < len(lockObjectPairs)):
                lock, instance = lockObjectPairs[predicate]
                return LockingProxy(instance, lock, is_locked = False)
            # end if
            return None
        # end if

        # Step 1: Initialize lock cache if necessary
        cacheKey = predicate
        with self.SYNCHRONIZATION_LOCK:
            # _keyCache contains a map id(predicate) -> tuple(predicateLock,
            #                                                 set(lock),
            #                                                 set(lock),
            #                                                 set(lock))
            if (cacheKey not in self._keyCache):
                allLocks = [pair[0] for pair in lockObjectPairs]


                # Create the list of unknown locks for this predicate
                allUnknownLocks = set(allLocks)
                for validLocks in iter(list(self._keyCache.values())):
                    # TODO use set.difference
                    for validLock in validLocks:
                        allUnknownLocks.discard(validLock)
                    # end for
                # end for

                # allUnknownLocks now contains the list of locks
                # that do not match any predicate.
                validLocks    = set()
                for unknownLock in allUnknownLocks:
                    with unknownLock:
                        # Otherwise, apply the predicate to the object associated with the lock.
                        for innerLock, innerObject in lockObjectPairs:
                            # This is the object to test
                            if innerLock is unknownLock:
                                # Apply the predicate.
                                if (predicate(innerObject)):
                                    # The predicates tells us it is a valid object.
                                    # Move the lock to valid locks
                                    # Remove the lock from unknown locks
                                    validLocks.add(unknownLock)
                                # end if
                                break
                            # end if
                        # end for
                    # end with
                # end for

                if validLocks != set():
                    # validLocks now contains the valid locks for the current predicate.
                    self._keyCache[cacheKey] = validLocks
                # end if
            # end if
        # end with

        # Re-obtain the list of locks, as the list may have changed from
        # the previous loop.
        with self.SYNCHRONIZATION_LOCK:
            if cacheKey in self._keyCache:
                validLocks  = self._keyCache[cacheKey]
            else:
                validLocks = set()
            # end if
        # end with

        # Only examine valid objects (return immediately) or
        # unknown objects (evaluate, update the cache and return)
        locksToWaitOn  = validLocks

        # No objects to wait on: return None
        if (len(locksToWaitOn) == 0):
            return None
        # end if

        # Wait for any valid or unknown object.
        lock = wait_for_any_lock(locksToWaitOn)

        # Additional check, there once was a difficult-to-find bug here
        if (lock not in locksToWaitOn):
            pass
        # end if

        # The lock is valid, use it and return.
        resultLock = lock

        # We are now at the end of the lock search.
        # resultLock contains either a valid lock, already acquired,
        # or is None if no matching object could be found.
        result = None
        if (resultLock is not None):
            # Find the object associated with the lock.
            for innerLock, innerObject in lockObjectPairs:
                # This is the object to test
                if innerLock is resultLock:
                    result = LockingProxy(innerObject, innerLock, is_locked = True)
                    break
                # end if
            else:
                # The lock was not found in the list.
                # This is an error, so we release the lock and raise an error.
                resultLock.release()
                raise ValueError("Unable to find lock in the list of objects.")
            # end for
        # end if

        return result
    # end def getLockedObject

    def clearLockCache(self, predicate = None):
        '''
        Clears the lock cache.

        This will force later calls to getLockedObject to re-scan the entries

        @option predicate [in] (callable) The predicate for which to clear the cache.
                              If None, the full cache is cleared
        '''

        with self.SYNCHRONIZATION_LOCK:
            if (predicate is None):
                self._keyCache.clear()
            elif (not isinstance(predicate, int)):
                cacheKey = predicate
                if (cacheKey in self._keyCache):
                    del self._keyCache[cacheKey]
                # end if
            # end if
        # end with
    # end def clearLockCache



    @staticmethod
    def _assertLocksConsistency(locksToWaitOn,
                                lockObjectPairs):
        '''
        Checks the consistency of the locks to be waited on, and the list of lock/object pairs.

        @param  locksToWaitOn   [in] (tuple) The list of locks that will be checked.
        @param  lockObjectPairs [in] (tuple) The list to check against.
        '''
        for lock in locksToWaitOn:
            found = False

            for testLock in [pair[0] for pair in lockObjectPairs]:
                found = found or (testLock is lock)
            # end for

            assert found, "The locks to wait on are inconsistent with the list of locked objects"
        # end for
    # end def _assertLocksConsistency

    def _removeFromUnknownLocks(self, lock):
        '''
        Removes a specific lock from the list of unknown locks for ALL keys in the cache.

        @param  lock [in] (Lock) The lock to remove from the list of unknown locks.
        '''
        with self.SYNCHRONIZATION_LOCK:
            for unknownLocks, listLock in [(unknownLocks, listLock) for unusedPredicateLock,
                                                                        listLock,
                                                                        unusedValidLocks,
                                                                        unusedInvalidLocks,
                                                                        unknownLocks
                                                                    in iter(list(self._keyCache.values()))]:
                with listLock:
                    unknownLocks.discard(lock)
                # end with
            # end for
        # end with
    # end def _removeFromUnknownLocks

    def _updateUnknownLocks(self, listLock,
                                  invalidLocks,
                                  unknownLocks):
        '''
        Updates the list of unknown locks, moving the locks from unknown to
        invalid if they are known by in at least one other predicate

        @param  listLock     [in] (tuple) The lock on the current list.
        @param  invalidLocks [in] (tuple) The known invalid locks for the current predicate.
        @param  unknownLocks [in] (tuple) The unknown locks for the current predicate.
        '''

        # Additional filtering: The lock must not belong to another key or predicate.
        # That is, if the lock can be found in the list of valid locks
        # of any predicate other than the current predicate, this is an error.
        for unusedPredicateLock, otherListLock, otherValidLocks, unusedInvalidLocks, unusedUnknownLocks in iter(list(self._keyCache.values())):

            # The other valid locks may be added to before the current filtering
            # is done with.
            # This cannot be solved by having the whole API encapsulated
            # within the SYNCHRONIZATION_LOCK, because ANY retrieval
            # that blocks on a predicate would block the whole retrieval
            # mechanism.
            # The alternative is to introduce yet another lock, to guard
            # the access to the predicate locks list.
            with otherListLock:
                for otherValidLock in set(otherValidLocks):
                    with listLock:
                        for unknownLock in unknownLocks:
                            if unknownLock is otherValidLock:
                                unknownLocks.remove(unknownLock)
                                invalidLocks.add(unknownLock)
                                break
                            # end if
                        # end for
                    # end with
                # end for
            # end with
        # end for
    # end def _updateUnknownLocks


    @staticmethod
    def collectOnly():
        '''
        Whether this run only collects the tests to be run, or whether it
        executes each test.

        This method is useful as it allow the @c TestCase.run method to decide
        whether it should actually run the tests, or only notify the listeners
        that the tests have started/stopped.

        This allows a TestRunner to deduce the hierarchy of the test calls,
        @e before the tests are actually run. It is especially useful for a GUI,
        which can show the test hierarchy prior to the actual run.

        @return (bool) Whether the run will collect results (True)
                          or tests will run (False)
        '''
        return False
    # end def collectOnly

    def getFeatures(self):
        '''
        @copydoc pyharness.context.FeaturesProvider.getFeatures
        '''
        return self.__features
    # end def getFeatures

    def getDevice(self, indexOrPredicate = 0):
        '''
        Obtains a device instance

        Note that the parameter used to specify which device is to be used serves
        as a key to cache the device retrieval.

        Therefore, when using a filter to obtain the appropriate device, it is
        advised to use a global filter (i.e. a global function) instead of a
        local closure.

        For instance, do not do:
        @code
        def myFunction(self, context):
            def innerFilter(device):
                return True
            # end def innerFilter
            context.getDevice(innerFilter)
        # end def myFunction
        @endcode

        But use instead:
        @code
        @staticmethod
        def innerFilter(device):
            return True
        # end def innerFilter

        def myFunction(self, context):
            context.getDevice(self.innerFilter)
        # end def myFunction
        @endcode

        @todo This API must be rendered thread-safe.
        It should acquire a lock on the specified reader, which should be
        released at the end of the test.

        @par Note on lock implementation
        The lock is implemented by a proxy around the device object, the
        destructor of this proxy being in charge of releasing the lock.
        \n
        This allow a simple implementation (the lock is held only for the
        life duration of the device object), but for this to work effectively
        on a single test run (throughout the setUp/test_xyz/tearDown sequence,
        the DeviceTestCase class must implement a caching mechanism that will
        re-use the device instance through setUp, test_xyz and tearDown.
        \n
        Those modifications should be done in the @c pyharness.device.DevicetestCase.getDevice
        API, and in the @c pyharness.device.DeviceTestCase.tearDown API.

        @option indexOrPredicate    [in] (int, callable) Index of the device, or a predicate taking a SmartDevice
                                         instance as a parameter.

        @return (SmartDevice) Instance of a SmartDevice object.
        '''

        if (isinstance(indexOrPredicate, int)):
            with self.SYNCHRONIZATION_LOCK:
                if (indexOrPredicate not in self.INT_PREDICATES):
                    self.INT_PREDICATES[indexOrPredicate] = lambda x: x.number == indexOrPredicate
                # end if

                predicate = self.INT_PREDICATES[indexOrPredicate]
            # end with
        else:
            predicate = indexOrPredicate
        # end if

        return self.getLockedObject(self.__smartDevices, predicate)
    # end def getDevice

    def getDeviceCount(self):
        '''
        Obtains the number of devices available in this context.

        @return The number of available devices in this context.
        '''
        return len(self.__smartDevices)
    # end def getDeviceCount

    def getDebugger(self, indexOrPredicate = 0):
        '''
        Obtains a debugger instance

        Note that the parameter used to specify which debugger is to be used serves
        as a key to cache the debugger retrieval.

        Therefore, when using a filter to obtain the appropriate debugger, it is
        advised to use a global filter (i.e. a global function) instead of a
        local closure.

        For instance, do not do:
        @code
        def myFunction(self, context):
            def innerFilter(debugger):
                return True
            # end def innerFilter
            context.getDebugger(innerFilter)
        # end def myFunction
        @endcode

        But use instead:
        @code
        @staticmethod
        def innerFilter(debugger):
            return True
        # end def innerFilter

        def myFunction(self, context):
            context.getDebugger(self.innerFilter)
        # end def myFunction
        @endcode

        @par Note on lock implementation
        The lock is implemented by a proxy around the device object, the
        destructor of this proxy being in charge of releasing the lock.
        \n
        This allow a simple implementation (the lock is held only for the
        life duration of the object), but for this to work effectively
        on a single test run (throughout the setUp/test_xyz/tearDown sequence,
        the DebuggerTestCase class must implement a caching mechanism that will
        re-use the device instance through setUp, test_xyz and tearDown.
        \n
        Those modifications should be done in the @c pyharness.debugger.DebuggerTestCase.get_dbg
        API, and in the @c pyharness.debugger.DebuggerTestCase.tearDown API.

        @option indexOrPredicate    [in] (int, callable) Index of the debugger, or a predicate taking an Debugger
                                                         instance as a parameter.

        @return (Debugger) Instance of an Debugger object.
        '''

        return self.getLockedObject(self.__debuggers, indexOrPredicate)
    # end def getDebugger

    def getDebuggerCount(self):
        '''
        Obtains the number of debuggers available in this context.

        @return The number of debuggers available in this context.
        '''
        return len(self.__debuggers)
    # end def getDebuggerCount

    def getDebuggerPredicates(self):
        '''
        Get tall the debugger predicates

        @return (list) List of debugger predicates
        '''
        return self.__debuggerPredicates
    # end def getDebuggerPredicates

    def appendDebuggerPredicate(self, predicate):
        '''
        Memorize debugger predicate

        @param  predicate [in] (int,callable) Predicate
        '''
        self.__debuggerPredicates.append(predicate)
    # end def appendDebuggerPredicate

    def getConfig(self):
        '''
        Obtains the configuration

        The configuration is obtained by overriding the contents of the root
        LOCAL/Settings.ini with the contents of xx.settings.ini files present in the SETTINGS 
        folders.

        @return Configuration of the context
        '''
        return self.__config
    # end def getConfig

    def getRootDir(self):
        '''
        Obtain the validation's root directory, as specified in the --root command line option.

        @return The application's root directory.
        '''
        root = self.__config.get(ContextLoader.SECTION_CONFIG,
                                 ContextLoader.OPTION_ROOTPATHS)[0]

        root = abspath(root)

        return root
    # end def getRootDir

    def getLoopCount(self):
        '''
        Obtain the loop count, as specified by the --loop-count command line option

        @return The loop count
        '''
        return self.__config.get(ContextLoader.SECTION_CONFIG,
                                 ContextLoader.OPTION_LOOPCOUNT,
                                 1)
    # end def getLoopCount

    def _getRootRelativePath(self, pattern):
        '''
        Obtains the root-relative path for the given pattern.

        @param  pattern [in] (str) The pattern to apply to the MODE, PRODUCT, VARIANT keys.

        @return (str) The path to a directory, relative to the root directory
        '''
        mode         = self.getCurrentMode()
        product      = self.getCurrentProduct()
        variant      = self.getCurrentVariant()

        rootRelativePath = pattern % {"MODE":    mode,
                                      "PRODUCT": product,
                                      "VARIANT": variant,
                                      }
        return normpath(rootRelativePath)
    # end def _getRootRelativePath

    def getInputDir(self):
        '''
        Obtains the input directory for this version.

        The input directory is deduced in the following way:
        - The Settings.ini file contains the definition of:
          - The current mode (WORKING, RELEASE...)
          - The current PRODUCT (formerly, the first element of a VERSION path)
          - The current VARIANT (the rest of the VERSION path)
        - These can be overridden by lower-level Settings.ini files, dedicated
          to a specific variant
        - The configuration then obtains the format of the InputDir/OutputDir
          by reading the contents of the F_InputDirPattern and F_OutputDirPattern
          features
        - Finally, the obtained pattern is applied to the MODE, PRODUCT and VARIANT keywords
        .

        This depends on the root directory, the current version, and the current target.

        @return the current run's input directory.
        '''
        rootDir  = self.getRootDir()
        features = self.getFeatures()
        pattern  = features.RUNTIME.F_InputDirPattern
        result = normpath(join(rootDir, self._getRootRelativePath(pattern)))

        return result
    # end def getInputDir

    def getOutputDir(self):
        '''
        Obtains the output directory for this version.

        The input directory is deduced in the following way:
        - The Settings.ini file contains the definition of:
          - The current mode (WORKING, RELEASE...)
          - The current PRODUCT (formerly, the first element of a VERSION path)
          - The current VARIANT (the rest of the VERSION path)
        - These can be overridden by lower-level Settings.ini files, dedicated
          to a specific variant
        - The configuration then obtains the format of the InputDir/OutputDir
          by reading the contents of the F_InputDirPattern and F_OutputDirPattern
          features
        - Finally, the obtained pattern is applied to the MODE, PRODUCT and VARIANT keywords
        .

        This depends on the root directory, the current version, and the current target.

        @return the current run's input directory.
        '''
        rootDir  = self.getRootDir()
        features = self.getFeatures()
        pattern  = features.RUNTIME.F_OutputDirPattern
        result = normpath(join(rootDir, self._getRootRelativePath(pattern)))

        return result
    # end def getOutputDir

    def getInputFilePath(self, relativeFilePath):
        '''
        Search for the existence of a file on the input path.

        @param  relativeFilePath [in] (str) A relative file path.

        @return The absolute file path to the actual file, which can be in the hierarchy of the directory.

        The file can be anywhere, starting from the designated path, upwards to the MODE directory.

        Example:
        - The project has a version @c V1_0 and a subversion @c PATCH_1.
        - The designated file is @c test.ini, which is under @c V1_0
        - The project is on mode WORKING, with the target SIMULATOR
        - a call to @c getInputFilePath("test.ini") will result in the file being looked up successively in:
          - @c WORKING/V1_0/PATCH_1/SIMULATOR/test.ini
          - @c WORKING/V1_0/PATCH_1/test.ini
          - @c WORKING/V1_0/test.ini, where it is found. The absolute path to this file is returned
          .
        .

        '''
        rootDir = self.getRootDir()

        features = self.getFeatures()
        pattern  = features.RUNTIME.F_InputDirPattern
        rootRelativeDir = self._getRootRelativePath(pattern)

        # The segments contain non-empty path elements, relative to the root path.
        # for instance, "V1_0//PATCH_1/" will be translated to
        # ["V1_0", "PATCH_1"]

        # Iterate on the segments.
        # For the previous example, this will lookup the file in
        # rootDir/V1_0/PATCH_1
        # rootDir/V1_0
        # NOT in rootDir
        # The odd case is when the the 'relative path' is actually an absolute
        # path: The search goes up in the hierarchy.
        filePathsLog = []
        currentDir = normpath(rootRelativeDir)
        loop = True
        while (loop):

            if not isabs(rootRelativeDir):
                dirPath  = join(rootDir, currentDir)
            else:
                dirPath = currentDir
            # end if

            filePath = abspath(join(dirPath, relativeFilePath))
            if (access(filePath, R_OK)):
                return filePath
            # end if

            filePathsLog.append(filePath)

            previousDir = currentDir
            currentDir = dirname(currentDir)

            loop = (previousDir != currentDir)
        # end while

        raise ValueError("Could not find file: %s in %s" % (relativeFilePath, filePathsLog))
    # end def getInputFilePath

    def makeReadOnly(self):
        '''
        Switch this context to read-only mode.

        This is a permanent switch, it should be done when the context has been
        completely read

        It causes some member variables to be read-only:
        - Features (recursive)
        .
        '''
        # Make read-only:

        self.__features.makeReadOnly()
    # end def makeReadOnly

    def checkManualTestCase(self, testCase, shortText=None, longText=None):
        '''
        Ask the user for confirmation of a manual TestCase.

        By default, if no UI is provided, this causes the test to fail.
        This method should be overridden by the context creator.

        @param  testCase  [in] (str) The identifier of the TestCase
        @option shortText [in] (str) A onle-line explanation of the TestCase.
        @option longText  [in] (str) A longer, multi-line explanation of the TestCase.

        @return The result of the manual TestCase validation, as a tuple (status, author, comment)
        '''
        if (self.manualTestCaseUi is None):
            raise AssertionError("Manual TestCase skipped: %s" % (testCase))
        # end if

        return self.manualTestCaseUi(testCase, shortText, longText)
    # end def checkManualTestCase

    def getCurrentMode(self):
        '''
        Obtains the currently selected mode from the config file.

        @return (str) The currently selected mode.
        '''
        config = self.getConfig()
        return config.get(ContextLoader.SECTION_MODE,
                          ContextLoader.OPTION_VALUE)
    # end def getCurrentMode

    def getCurrentProduct(self):
        '''
        Obtains the currently selected product from the config file.

        @return (str) The currently selected product.
        '''
        config = self.getConfig()
        return config.get(ContextLoader.SECTION_PRODUCT,
                   ContextLoader.OPTION_VALUE)
    # end def getCurrentProduct

    def getCurrentVariant(self):
        '''
        Obtains the currently selected variant from the config file.

        @return (str) The currently selected variant.
        '''
        config = self.getConfig()
        return config.get(ContextLoader.SECTION_VARIANT,
                          ContextLoader.OPTION_VALUE)
    # end def getCurrentVariant

    def getCurrentTarget(self):
        '''
        Obtains the currently selected target from the config file.

        @return (str) The currently selected target.
        '''
        config = self.getConfig()
        return config.get(ContextLoader.SECTION_TARGET,
                          ContextLoader.OPTION_VALUE)
    # end def getCurrentTarget

    def close(self):
        '''
        Closes the context.

        Once closed, the context is NOT accessible:
        - Its inner variables may be reset to 0
        - Its inner debuggers and devices are terminated
        .
        '''
        raise NotImplementedError()
    # end def close
# end class AContext

class RootContext(AContext):
    '''
    Root context for tests

    Close method will free all device and debugger resources
    '''
    def __init__(self, rootFeatures,
                       smartDevices = None,
                       debuggers  = None,
                       config     = None,
                       manualUi   = None):
        '''
        @copydoc pyharness.context.AContext.__init__
        '''
        super(RootContext, self).__init__(rootFeatures,
                                          smartDevices = smartDevices,
                                          debuggers  = debuggers,
                                          config     = config,
                                          manualUi   = manualUi)
        self.setParent(self)
    # end def __init__

    def close(self):
        '''
        @copydoc pyharness.context.AContext.close
        '''
        self.__features = None

        # Clean the smart devices
        smartDevices = getattr(self, '_AContext__smartDevices')
        for _, smartDevice in smartDevices:
            while smartDevice.is_allocated():
                smartDevice.unallocate()
            # end while
        # end for
        del smartDevices[:]

        debuggers = getattr(self, '_AContext__debuggers')
        for _, debugger in debuggers:
            try:
                while debugger.isOpen():
                    debugger.close()
                # end while
            except Exception:                                                                                           # pylint:disable=W0703
                # This should not happen, but some debuggers are known to misbehave...
                pass
            # end try
        # end for
        del debuggers[:]

        # Clean the emulator manager
        emulators_manager = getattr(EmulatorInterface, '_EmulatorInterface__instance')
        if emulators_manager is not None:
            emulators_manager.__del__()
        # end if
    # end def close
# end class RootContext

class SubContext(AContext):
    '''
    Sub context used by derivation of context, for example by patching of code
    '''
    def close(self):
        '''
        @copydoc pyharness.context.AContext.close
        '''
        self.__features = None

        # Clean the smart devices
        smartDevices = getattr(self, '_AContext__smartDevices')
        for _, smartDevice in smartDevices:
            if smartDevice.is_allocated():
                smartDevice.unallocate()
            # end if
        # end for

        debuggers = getattr(self, '_AContext__debuggers')
        for _, debugger in debuggers:
            try:
                if debugger.isOpen():
                    debugger.close()
                # end if
            except Exception:                                                                                           # pylint:disable=W0703
                # This should not happen, but some debuggers are known to misbehave...
                pass
            # end try
        # end for
    # end def close
# end class SubContext

class CollectContext(object):
    '''
    This is a local access to the context, that overrides themethod used to
    check the collectOnly flag
    '''

    def __init__(self, next):                                                                                           # @ReservedAssignment # pylint:disable=W0622
        '''
        Constructor for this decorator

        @param  next [in] (Context) The context to decorate.
        '''
        self.next = next
    # end def __init__

    @staticmethod
    def collectOnly():
        '''
        Overrides the collectOnly method from Context.

        @return (bool) Whether the context only collects information (True)
                          or if tests must be run
        '''
        return True
    # end def collectOnly

    def __getattr__(self, name):
        '''
        This implements the proxy mechanism to the next object.

        @param  name [in] (str) The name of the attribute to obtain

        @return The proxied attribute.
        '''
        return getattr(self.__dict__["next"], name)
    # end def __getattr__
# end class CollectContext

class ContextLoader(object):
    '''
    An object that groups the utility methods used to load a context.

    Loading a context is a complex operation:
    1. Find out, from the LOCAL/Settings.ini, which is the current PRODUCT and VARIANT.
    2. From the PRODUCT and VARIANT, look up nested Settings.ini files,
       and override the contents of the initial Settings.ini file.
       This permits variant-dependent configurations.
    3. Load the default features, from the subsystems defined in the
       features.py files.
    4. Override the features, from the main.settings.ini file
    5. Recursively override the features, from the nested VERSION.settings.ini files.
    '''

    ##@name Section
    #@{
    SECTION_MODE    = 'MODE'
    SECTION_PRODUCT = 'PRODUCT'
    SECTION_VARIANT = 'VARIANT'
    SECTION_TARGET  = 'TARGET'
    SECTION_CONFIG  = 'INTERNALCONFIG'

    SECTION_READER  = 'READER'
    SECTION_VAL     = 'RUNTIME'
    #@}

    ##@name Option
    #@{
    OPTION_VALUE     = 'value'
    OPTION_ROOTPATHS = 'rootPaths'
    OPTION_COVERAGE  = 'auto_coverage'
    OPTION_LOOPCOUNT = 'loopCount'
    #@}

    ##@name Reader
    #@{
    VALUE_READER_NONE               = 'None'
    VALUE_READER_DEVICEREADER       = 'DeviceReader'
    VALUE_READER_DEBUGGERREADER     = 'DebuggerReader'
    READER_CLASSDICT = {
                        VALUE_READER_DEVICEREADER:
                            'pylibrary.system.device.smartDeviceFactory',
                        }
    #@}

    ##@name Debugger
    #@{
    VALUE_DEBUGGER_NONE       = 'None'
    VALUE_DEBUGGER_DUMMY      = 'DummyEmulator'
    DEBUGGER_CLASSDICT = {
                          VALUE_DEBUGGER_DUMMY:
                            'pylibrary.system.dummydebugger.DummyDebugger',
                          }
    #@}

    ##@name Default target
    #@{
    DEFAULT_TARGET_ID   = 'DEVICE'
    #@}

    ##@name Version size
    #@{
    MIN_VERSION_SIZE    = 1
    MAX_VERSION_SIZE    = None
    #@}

    ##@name Marker
    #@{
    MARKER_DEVICESET      = 1
    MARKER_DEBUGGERSET  = 2
    MARKER_FOLDERSET    = 4
    MARKER_ALLSET       = MARKER_DEVICESET | MARKER_DEBUGGERSET | MARKER_FOLDERSET
    #@}


    def __init__(self, subSystemBuilder = None):
        '''
        Constructor

        subSystemBuilder should be None in most cases, assigning a value is only useful when running autotests.

        @option subSystemBuilder [in] (SubSystemBuilder) The subsystem builder to use.
        '''
        if (subSystemBuilder is not None):
            self.subSystemBuilder = subSystemBuilder

        else:
            subSystemDefinitionImporterComposite = SubSystemDefinitionImporterComposite()
            subSystemDefinitionImporterComposite.add(PythonSubSystemDefinitionImporter())

            subSystemInstantiationImporterComposite = SubSystemInstantiationImporterComposite()
            subSystemInstantiationImporterComposite.add(IniSubSystemInstantiationImporter())
            subSystemInstantiationImporterComposite.add(XmlSubSystemInstantiationImporter())

            self.subSystemBuilder = SubSystemBuilder(subSystemDefinitionImporter    = subSystemDefinitionImporterComposite,
                                                     subSystemInstantiationImporter = subSystemInstantiationImporterComposite)

        # end if
    # end def __init__

    @classmethod
    def __loadFromDefaults(cls, config,
                                rootPaths):
        '''
        Loads the configuration from the default ini file.

        @param  config    [inout] (ConfigParser) The configuration to load.
        @param  rootPaths [in]    (list) The list of root paths to initialize in the configuration
        '''
        config.load_string(DEFAULT_CONFIG_TEMPLATE)

        config.set(cls.SECTION_CONFIG,
                   cls.OPTION_ROOTPATHS,
                   rootPaths)

        config.set(cls.SECTION_CONFIG,
                   cls.OPTION_COVERAGE,
                   False)
    # end def __loadFromDefaults

    @staticmethod
    def __loadFromIniFile(config, pathToIniFile):
        '''
        Loads the configuration from an ini file.

        @param  config        [inout] (ConfigParser) The configuration to load.
        @param  pathToIniFile [in]    (str) The path to the ini file to read.
        '''

        stream = getResourceStream(pathToIniFile)
        if (stream is not None):
            config.load_string(stream.read())
        # end if
    # end def __loadFromIniFile

    @classmethod
    def __createIniFile(cls, config,
                             rootPath,
                             pathToIniFile,
                             overrides):
        '''
        Creates a settings.ini file

        @param  config        [in] (ConfigParser) The config to create
        @param  rootPath      [in] (str) The validation root path.
        @param  pathToIniFile [in] (str) The path to the ini file to create.
        @param  overrides     [in] (dict) Parameters overriding the default values

        @return Whether the creation was complete (True), or default values were supplied
        '''

        mustExit = False

        overrides = dict([override.split('=', 1) for override in overrides])

        # The path to the INI file must exist.
        # If not, it is created.
        localPath = dirname(pathToIniFile)
        if not access(localPath, R_OK):
            makedirs(localPath)
        # end if

        path = join(rootPath, DEFAULT_INPUT_DIRECTORY)

        # Create the [PRODUCT].value option
        key = '%s.%s' % (cls.SECTION_PRODUCT,
                         cls.OPTION_VALUE)
        if (key in overrides):
            product = overrides[key]
        else:
            product  = cls.findDefaultProduct(path)
            mustExit = True
        # end if

        config.set(cls.SECTION_PRODUCT,
                   cls.OPTION_VALUE,
                   product)

        # Insert the list of products before the option
        availableProducts = cls.findAllProducts(path)
        config.add_comment('Possible values are:',
                           cls.SECTION_PRODUCT,
                           cls.OPTION_VALUE)
        for availableProduct in availableProducts:
            config.add_comment('- %s' % (availableProduct,),
                               cls.SECTION_PRODUCT,
                               cls.OPTION_VALUE)
        # end for

        if (product is None):
            raise ValueError('The %s directory does not contain any product' % (DEFAULT_INPUT_DIRECTORY,))
        # end if

        # Create the [VARIANT].value option
        path = join(rootPath, DEFAULT_INPUT_DIRECTORY, product)

        key = '%s.%s' % (cls.SECTION_VARIANT,
                         cls.OPTION_VALUE)
        if (key in overrides):
            versions = overrides[key].split('/')
        else:
            versions = cls.findDefaultVersion(path)
            mustExit = True
        # end if

        config.set(cls.SECTION_VARIANT,
                   cls.OPTION_VALUE,
                   '/'.join(versions))

        backedUpOptions = {}
        for option in config.options(cls.SECTION_CONFIG):
            backedUpOptions[option] = config.get(cls.SECTION_CONFIG, option)
        # end for
        # Remove the [INNERCONFIGURATION].rootPath option
        config.remove_section(cls.SECTION_CONFIG)

        # save default file
        with open(pathToIniFile, 'w+') as configFile:
            # Write a default header to this ini file
            configFile.write(DEFAULT_CONFIG_HEADER)

            config.write(configFile)
        # end with

        config.add_section(cls.SECTION_CONFIG)
        for option, value in backedUpOptions.items():
            config.set(cls.SECTION_CONFIG,
                       option,
                       value)
        # end for

        return mustExit
    # end def __createIniFile

    @staticmethod
    def __loadFromOverrides(config,
                            overrides):
        '''
        Loads the configuration from overridden command-line parameters

        @param  config    [inout] (ConfigParser) The configuration to load.
        @param  overrides [in]    (dict) The overridden values.
        '''

        # override config file parameters with the overrides
        for name in overrides:
            namevalue = name.split('=')
            sectionoption = namevalue[0].split('.')

            section = sectionoption[0].strip()
            option = sectionoption[1].strip()
            value = namevalue[1].strip()

            # create the section if absent
            if (not config.has_section(section)):
                config.add_section(section)
            # end if

            # Handle int overrides
            try:
                value = int(value)
            except ValueError:
                pass
            # end try

            if (value == 'False'):
                value = False

            elif (value == 'True'):
                value = True
            # end if


            config.set(section, option, value)
        # end for
    # end def __loadFromOverrides

    @classmethod
    def __get_root_relative_path(cls, config, pattern):
        """
        Get the root-relative path for the given pattern.

        :param config: The configuration from which to extract the path
        :type config: ``ConfigParser``
        :param pattern: The pattern to apply to the MODE, PRODUCT, VARIANT keys.
        :type pattern: ``str``

        :return: The path to a directory, relative to the root directory
        :rtype: ``str``
        """
        mode = config.get(cls.SECTION_MODE, cls.OPTION_VALUE)
        product = config.get(cls.SECTION_PRODUCT, cls.OPTION_VALUE)
        variant = config.get(cls.SECTION_VARIANT, cls.OPTION_VALUE)
        return pattern % {'MODE': mode, 'PRODUCT': product, 'VARIANT': variant}
    # end def __get_root_relative_path

    @classmethod
    def __collect_usb_context(cls, features):
        """
        Collect the USB context class reference as a string.

        :param features: The root features
        :type features: ``SubSystem``

        :return: the USB context class
        :rtype: ``str`` or ``None``
        """
        return features.RUNTIME.F_UsbContextClass
    # end def __collect_usb_context

    @classmethod
    def __collect_device_manager_class(cls, features):
        """
        Collect the device manager class from the features

        :param features: The root features
        :type features: ``SubSystem``

        :return: The device manager class
        :rtype: ``str``
        """
        return features.RUNTIME.F_DeviceManager
    # end def __collect_targets

    @staticmethod
    def __collect_debuggers(features):
        """
        Collect the debuggers from the features

        :param features: The root features
        :type features: ``SubSystem``

        :return: A dict of the debuggers
        :rtype: ``dict``
        """
        debuggers = {}
        debugger_types = list(features.RUNTIME.DEBUGGERS.F_Types)
        if '' in debugger_types:
            debugger_types.remove('')
        # end if
        for index, debugger_type in enumerate(debugger_types):
            debuggers[index] = DEBUGGERS_MAPPING[debugger_type]
        # end for
        return debuggers
    # end def __collect_debuggers

    @classmethod
    def __initialize_device_manager(cls, device_manager_class, output_dir, usb_context_class, features):
        """
        Initialize the device manager.

        :param device_manager_class: The device manager class
        :type device_manager_class: ``str``
        :param output_dir: The output directory
        :type output_dir: ``str``
        :param usb_context_class: The USB context class reference
        :type usb_context_class: ``str`` or ``None``
        :param features: The context features
        :type features: ``AggregatingSubSystemDefinition`` or ``None``

        :return: The initialized device manager.
        :rtype: ``BaseSmartDevice``
        """
        device_manager_class = importFqn(device_manager_class)

        if usb_context_class not in (None, "None"):
            usb_context_class_fqn = usb_context_class
            try:
                usb_context_class = importFqn(usb_context_class_fqn)
            except ImportError:
                raise ImportError(f"Unable to use the specified USB context class ({usb_context_class_fqn})")
            # end try
        # end if
        device_manager_class.configure(path=output_dir, usb_context_class=usb_context_class, features=features)

        return device_manager_class(device_number=0)
    # end def __initialize_smart_devices

    @classmethod
    def __initialize_debuggers(cls, target_debuggers, output_dir, input_dir):
        """
        Initialize the debuggers for the target
        
        :param target_debuggers: The target debuggers description
        :type target_debuggers: ``dict``
        :param output_dir: The output directory
        :type output_dir: ``str``
        :param input_dir: The input directory
        :type input_dir: ``str``
        
        :return: The initialized target debuggers.
        :rtype: ``dict``
        """
        debuggers = {}
        for index, debugger_type in target_debuggers.items():
            debugger_class = importFqn(debugger_type)
            debugger = debugger_class(abspath(input_dir), abspath(output_dir), index)
            debuggers[index] = debugger
        # end for
        return debuggers
    # end def __initialize_debuggers

    def createContext(self, config, manualUi=None, additionalSubSystemInstantiations=tuple()):
        """
        Creates a context from the given configuration.

        :param config: The configuration to translate into a context.
        :type config: ``ConfigParser``
        :param manualUi: A callback used for the validation of manual TestCases - OPTIONAL
        :type manualUi: ``callable``
        :param additionalSubSystemInstantiations: Additional instantiations,
                                                  to be applied at end of construction. - OPTIONAL
        :type additionalSubSystemInstantiations: ``tuple``

        :return: A new context matching the given configuration.
        :rtype: ``Context``
        """
        # Load the features
        features = self.loadFeatures(config, additionalSubSystemInstantiations=additionalSubSystemInstantiations)

        # Extract the root path
        root_path = config.get(self.SECTION_CONFIG, self.OPTION_ROOTPATHS)[0]
        # Fix some missing features if needed.
        if not hasattr(features.RUNTIME, 'F_InputDirPattern'):
            features.RUNTIME.F_InputDirPattern = '../%(MODE)s/%(PRODUCT)s/%(VARIANT)s'
        # end if
        if not hasattr(features.RUNTIME, 'F_OutputDirPattern'):
            features.RUNTIME.F_OutputDirPattern = '../%(MODE)s/%(PRODUCT)s/%(VARIANT)s'
        # end if

        # Get input directory
        input_dir = self.__get_root_relative_path(config, features.RUNTIME.F_InputDirPattern)
        if not isabs(input_dir):
            input_dir = join(root_path, input_dir)
        # end if

        # Get output directory
        output_dir = join(root_path, DEFAULT_OUTPUT_DIRECTORY)

        # Collect device manager class
        device_manager_class = self.__collect_device_manager_class(features)

        # Collect USB context class
        usb_context_class = self.__collect_usb_context(features=features)

        # Create and initialize Smart Devices
        device_manager = self.__initialize_device_manager(
            device_manager_class=device_manager_class, output_dir=output_dir, usb_context_class=usb_context_class,
            features=features)

        # Collect and initialize the target debuggers
        target_debuggers = self.__collect_debuggers(features)
        debuggers = self.__initialize_debuggers(target_debuggers, output_dir, input_dir)

        result = RootContext(features, {device_manager.number: device_manager}, debuggers, config, manualUi)
        result.makeReadOnly()
        return result
    # end def createContext

    def deriveContext(self, context,
                            mode    = None,
                            product = None,
                            variant = None,
                            target  = None):
        '''
        Derives a new context from the specified one, where:
        - The config is altered to match the the specified parameters
        - The features are altered to reflect the new configuration

        Example:
        @code
        # We start with a context, already initialized on a product and the
        # variant ORIGINAL_VARIANT
        # We want to switch to the same product, with variant NEW_VARIANT
        newContext = ContextLoader.deriveContext(context, variant="NEW_VARIANT")
        @endcode

        @param  context [in] (Context) The context to derive the result from.
        @option mode    [in] (str) The new mode. If None, the current mode is used.
        @option product [in] (str) The new product. If None, the current product is used.
        @option variant [in] (str) The new variant. If None, the current variant is used.
        @option target  [in] (str) The new target. If None, the current target is used.

        @return A new context (actually a proxy on the original context.
        '''
        assert (   (mode is not None)
                or (product is not None)
                or (variant is not None)
                or (target is not None)), \
            'At least one parameter (mode, product, variant, target) must be specified'

        oldMode    = context.getCurrentMode()
        oldProduct = context.getCurrentProduct()
        oldVariant = context.getCurrentVariant()
        oldTarget  = context.getCurrentTarget()
        oldConfig  = context.getConfig()

        mode    = (mode is not None)    and mode    or oldMode
        product = (product is not None) and product or oldProduct
        variant = (variant is not None) and variant or oldVariant
        target  = (target is not None)  and target  or oldTarget

        if target != oldTarget:
            raise ValueError('Target switch not allowed')
        # end if

        assert (   (mode    != oldMode)
                or (product != oldProduct)
                or (variant != oldVariant)
                or (target  != oldTarget)), \
            'At least one parameter (mode, product, variant, target) must be differ from the current settings'

        # Work on a copy of the current config, with its values changed.
        config = deepcopy(oldConfig)
        config.set(self.SECTION_MODE,    self.OPTION_VALUE, mode)
        config.set(self.SECTION_PRODUCT, self.OPTION_VALUE, product)
        config.set(self.SECTION_VARIANT, self.OPTION_VALUE, variant)
        config.set(self.SECTION_TARGET,  self.OPTION_VALUE, target)

        features = self.loadFeatures(config)

        smartDevices = getattr(context, '_AContext__smartDevices')
        debuggers = getattr(context, '_AContext__debuggers')
        result = SubContext(features,
                            smartDevices = smartDevices,
                            debuggers  = debuggers,
                            config     = config,
                            manualUi   = context.manualTestCaseUi)

        return result
    # end def deriveContext


    @staticmethod
    def findAllProducts(path, suffix="main.settings.ini"):
        r'''
        Finds all available products in the SETTINGS directory

        @param  path   [in]  (str) The current SETTINGS directory (or sub-version
                             directory)
        @option suffix [in]  (str) Suffix of the .ini file to lookup. Normally "main.settings.ini"

        @return (tuple) A lis of all available products
        '''
        result = []

        for element in sorted(listdir(path)):
            currentProduct = element.strip()
            currentProductFilePath = join(path, currentProduct, suffix)
            if (access(currentProductFilePath, R_OK)):
                # recursive call
                result.append(currentProduct)
            # end if
        # end for

        return result
    # end def findAllProducts

    @classmethod
    def findDefaultProduct(cls, path,
                                suffix = 'main.settings.ini'):
        r'''
        Finds the first available, valid, product in the SETTINGS directory

        @param  path   [in] (str) The current SETTINGS directory (or sub-version
                             directory)
        @option suffix [in] (str) Suffix of the <i>\<version\></i>.settings.ini file to lookup. Normally "main.settings.ini"

        @return (str) The default product
        '''
        allProducts = cls.findAllProducts(path, suffix)
        if (len(allProducts) > 0):
            return allProducts[-1]
        # end if

        return None
    # end def findDefaultProduct

    SUFFIX_LIST = ['.settings.ini', '.settings.xml']

    @classmethod
    def findDefaultVersion(cls, path,
                                suffix = None):
        r'''
        Finds the first available, valid, version in the SETTINGS directory

        @param  path   [in] (str)  The current SETTINGS directory (or sub-version
                             directory)
        @option suffix [in] (str, list) Suffix of the <i>\<version\></i>.settings.ini file to lookup. Normally ".settings.ini"

        @return The default version, as a tuple of versions and subversions
        '''
        if (suffix is None):
            suffix = cls.SUFFIX_LIST
        # end if

        for element in sorted(listdir(path)):
            currentVersion = element.strip()
            if isinstance(suffix, str):
                currentVersionFilePath = join(path, currentVersion, currentVersion+suffix)
                if (access(currentVersionFilePath, R_OK)):
                    # recursive call
                    result = [currentVersion]
                    subVersion = cls.findDefaultVersion(join(path, currentVersion), suffix)
                    result.extend(subVersion)
                    return result
                # end if
            elif isinstance(suffix, list):
                for suf in suffix:
                    currentVersionFilePath = join(path, currentVersion, currentVersion+suf)
                    if (access(currentVersionFilePath, R_OK)):
                        # recursive call
                        result = [currentVersion]
                        subVersion = cls.findDefaultVersion(join(path, currentVersion), suf)
                        result.extend(subVersion)
                        return result
                    # end if
                # end for
            else:
                raise TypeError('Wrong suffix type: %s. Should be string or list' % (type(suffix).__name__,))
            # end if
        # end for

        return []
    # end def findDefaultVersion

    def loadFeatures(self, config,
                           additionalSubSystemInstantiations = tuple()):
        '''
        Loads the features for the given config

        @param  config                            [in] (ConfigParser) The config to load the features for.
        @option additionalSubSystemInstantiations [in] (list) Additional instantiations, to be applied at end of construction.

        @return The newly created features
        '''
        # Obtain the target features directory
        product = config.get(self.SECTION_PRODUCT,
                             self.OPTION_VALUE)
        variant = config.get(self.SECTION_VARIANT,
                             self.OPTION_VALUE)

        relativePath = normpath(join(product, variant))
        pathElements = relativePath.split(sep)
        pathElements = [pathElement.strip() for pathElement in pathElements
                                            if len(pathElement.strip()) > 0]
                                            # end if

        if (    (not (self.MIN_VERSION_SIZE <= len(pathElements)))
            or  (    self.MAX_VERSION_SIZE is not None
                 and (len(pathElements) > self.MAX_VERSION_SIZE))):
            raise ValueError('Invalid version depth for version %s: version'
                             ' depth must be between %d and %d'
                             % ('/'.join(pathElements),
                                self.MIN_VERSION_SIZE,
                                self.MAX_VERSION_SIZE))
        # end if

        # Load the global subsystem, containing all the features, from disk
        rootPaths = config.get(self.SECTION_CONFIG,
                               self.OPTION_ROOTPATHS)
        rootPaths = [abspath(r) for r in rootPaths]

        subSystemInstantiationPaths = [join(rootPath, DEFAULT_INPUT_DIRECTORY, *pathElements) for rootPath in rootPaths]
        subSystemInstantiationPaths = [path for path in subSystemInstantiationPaths if exists(path)]

        rootPaths = [join(r, 'TESTSUITES') if exists(join(r, 'TESTSUITES')) else r for r in rootPaths]
        features = self.subSystemBuilder.load(rootPaths,
                                             subSystemInstantiationPaths,
                                             additionalSubSystemInstantiations = additionalSubSystemInstantiations)

        return features
    # end def loadFeatures

    @classmethod
    def loadConfigFromDefaults(cls, rootPaths, config=None, overrides = ()):
        '''
        Loads the configuration from the default configuration file

        @param  rootPaths  [in] (str) The root paths.
        @option config    [in] (ConfigParser) The existing configuration. If None, an instance is created.
        @option overrides [in] (tuple) Overrides for this configuration.

        @return The updated configuration
        '''
        if (config is None):
            config = ConfigParser()
        # end if

        cls.__loadFromDefaults(config, rootPaths)
        cls.__loadFromOverrides(config, overrides)

        return config
    # end def loadConfigFromDefaults

    @classmethod
    def loadConfigFromIni(cls, rootPath, config=None, overrides = (), failOnError=True):
        '''
        Loads the configuration from the Settings.ini file.

        @param  rootPath    [in] (str) The root path.
        @option config      [in] (ConfigParser) The existing configuration. If None, an instance is created.
        @option overrides   [in] (tuple) Overrides for this configuration.
        @option failOnError [in] (bool) Whether a missing config file fails (True) or is ignored

        @return The updated configuration
        '''
        if (config is None):
            config = ConfigParser()
        # end if

        mustExit = False

        localPath = join(rootPath, DEFAULT_OUTPUT_DIRECTORY)
        pathToConfig = join(localPath, 'Settings.ini')
        if (not access(pathToConfig, R_OK)):
            #--- Step 2.b If no Settings.ini file is found, create it, and warn the user
            mustExit = cls.__createIniFile(config, rootPath, pathToConfig, overrides) and failOnError
        # end if

        if (mustExit):
            raise IOError('Could not open Settings.ini file.\n' +
                          'A default file has been created, YOU MUST CHECK ITS CONTENTS NOW !\n' +
                          'File "%s", line 1' % (pathToConfig,))
        else:
            cls.__loadFromIniFile(config, pathToConfig)
            cls.__loadFromOverrides(config, overrides)

            # There may be Settings.ini files in the subdirectories.
            # These ini files are loaded, and overload the parent config.

            versionPath = normpath(join(str(config.get(cls.SECTION_PRODUCT,
                                                       cls.OPTION_VALUE)),
                                        str(config.get(cls.SECTION_VARIANT,
                                                       cls.OPTION_VALUE))))
            path = join(rootPath, DEFAULT_OUTPUT_DIRECTORY)
            elements = versionPath.split(sep)

            # This For version V1_0_1/PATCH_1, this will contain:
            # - The root Settings.ini
            # - overridden by a possible PRODUCT/Settings.ini
            # - overridden by a possible PRODUCT/V1_0_1/Settings.ini
            # - overridden by a possible PRODUCT/V1_0_1/PATCH_1/Settings.ini
            for element in elements:
                currentVersion = element.strip()
                path = join(path, currentVersion)
                filePath = join(path, 'Settings.ini')
                if (access(filePath, R_OK)):
                    cls.__loadFromIniFile(config, filePath)

                    # As always, the overrides take precedence
                    cls.__loadFromOverrides(config, overrides)
                # end if
            # end for

            cls.__loadFromOverrides(config, overrides)
            # end if
        # end if

        return config
    # end def loadConfigFromIni

    @classmethod
    def loadConfigFromFeatures(cls, rootPath, config=None, overrides = ()):
        '''
        Loads the configuration from the main.settings.ini and *.settings.ini files in the features tree.

        @param  rootPath  [in] (str) The root path.
        @option config    [in] (ConfigParser) The existing configuration. If None, an instance is created.
        @option overrides [in] (tuple) Overrides for this configuration.

        @return The updated configuration
        '''
        if (config is None):
            config = ConfigParser()
        # end if

        # Load from overloaded <version>.ini files, taken from the version
        product = config.get(cls.SECTION_PRODUCT,
                             cls.OPTION_VALUE)
        assert product is not None, 'No product selected'

        variant = config.get(cls.SECTION_VARIANT,
                             cls.OPTION_VALUE)
        assert variant is not None, 'No variant selected'

        target = config.get(cls.SECTION_TARGET,
                            cls.OPTION_VALUE)
        assert target is not None, 'No target selected'

        mode = config.get(cls.SECTION_MODE,
                          cls.OPTION_VALUE)
        assert mode is not None, 'No mode selected'

        relativePath = normpath(join(str(product), str(variant)))
        elements = [element.strip() for element in relativePath.split(sep)
                                    if (len(element) > 0)]

        path = join(rootPath, DEFAULT_INPUT_DIRECTORY)
        suffix = '.settings.ini'
        for element in elements:
            currentNode = element.strip()
            path = join(path, currentNode)
            filePath = join(path, currentNode + suffix)
            if (not access(filePath, R_OK)):
                raise IOError('Unable to open feature file: %s' % (filePath,))
            # end if
            cls.__loadFromIniFile(config, filePath)
            #suffix = '.ini'
        # end for

        cls.__loadFromOverrides(config, overrides)

        return config
    # end def loadConfigFromFeatures

    @classmethod
    def loadConfig(cls, rootPaths   = ('.',),
                        overrides   = (),
                        failOnError = True):
        '''
        Load a configuration from a root path.

        @option rootPaths   [in] (str)  Root paths to the validation (and possibly eggs).
        @option overrides   [in] (dict) The overriding properties
        @option failOnError [in] (bool) Whether a missing settings file fails (True) or is ignored

        @return A ConfigParser object, containing the merged configurations

        The LOCAL path should contain a Settings.ini file.
        Sub-directories @e may contain @c xx.settings.ini files per version.
        Any property from overrides takes precedence over the main configuration.
        '''
        config = ConfigParser()

        #--- Step 1. Load values from default template
        config = cls.loadConfigFromDefaults(rootPaths, config, overrides)

        rootPath = rootPaths[0]
        #--- Step 2. Load from main.settings.ini and xx.settings.ini files
        config = cls.loadConfigFromIni(rootPath, config, overrides, failOnError)

        return config
    # end def loadConfig

    def load(self, rootPaths = ('.',),
                   overrides = ()):
        '''
        Load a context from a root path.

        @option rootPaths [in] (str)  Root paths to the validation. Normally ('.',)
        @option overrides [in] (dict) The overriding properties

        The root path should contain a Settings.ini file
        Any property from overrides takes precedence over the main configuration.

        @return New context
        '''
        config = self.loadConfig(rootPaths, overrides)

        # Create the context
        return self.createContext(config)
    # end def load
# end class ContextLoader

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
