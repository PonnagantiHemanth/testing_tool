#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyharness.device

@brief DeviceTestCase implementation

This module provides utility classes, that initialize the Device for derived tests.

@author christophe.roquebert

@date   2018/11/11
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.system.context           import ContextSmartDevice
from pylibrary.system.device            import DeviceProvider
from pylibrary.system.device            import SmartDeviceException
from pylibrary.tools.hexlist            import HexList
from pyharness.core                     import _LEVEL_COMMAND
from pyharness.core                     import _LEVEL_ERROR
from pyharness.core                     import _LEVEL_SEPARATOR
from pyharness.core                     import _LEVEL_TRACE
from pyharness.core                     import _MASK_ALWAYS
from pyharness.extensions               import PyHarnessCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class DeviceTestCaseMixin(DeviceProvider):
    """
    A Mixin that adds getDevice support to an DeviceTestCase instance.

    This is only marginally useful not pure-Device test case classes,
    but it allows implementations to create Device-And-Debugger test case classes
    that do not call the TestCase.setUp and TestCase.tearDown methods twice.
    """

    def setUp(self):
        """
        Test initialisation
        """
        self.__devices = {}
    # end def setUp

    def tearDown(self):
        """
        Destructor of the test
        """
        for device in self.__devices.values():
            if device is not None:
                device.unallocate()
            # end if
        # end for

        self.__devices.clear()
    # end def tearDown

    def getDevice(self, indexOrPredicate=0, keepForTestduration=False):
        """
        @copydoc pylibrary.system.device.DeviceProvider.getDevice

        In a mono-threaded environment, the parameter @c keepForTestduration
        has no effect, as the SmartDevice instance is only accesses by the
        testing thread.

        In a multi-threaded environment, however, it may be necessary to reserve
        access to a SmartDevice for the whole duration of the test, throughout
        setUp(), test() and tearDown() methods.

        It is therefore advised (even in a mono-threaded context), to reserve
        access to the SmartDevice by performing a call to @c getDevice with the
        @c keepForTestduration parameter set to True in the setUp() method.

        API Workflow:
        @dot
        digraph G
        {
            node    [fontname=Arial, fontsize = 10, align=center, shape=diamond, width=1.0];
            edge    [fontname=Arial, fontsize = 8, len=0.5];
            ranksep = 0.1;
            rankdir = TB;

            {
                rankdir = LR;
                rank    = same;

                INITIALIZATION [label="Initialization", shape=box];
            }

            {
                rankdir = LR;
                rank    = same;

                KEYINCACHE       [label="Key in cache", shape=diamond];
            }

            {
                rankdir = LR;
                rank    = same;

                RETRIEVEFROMCACHE   [label="Retrieve from\ncache", shape=box];
                RETRIEVEFROMCONTEXT [label="Retrieve from\ncontext", shape=box];
            }

            {
                rankdir = LR;
                rank    = same;

                KEEPFORTESTDURATION      [label="keep for test\nduration ?", shape=diamond];
                KEEPFORTESTDURATIONPOINT [shape=point, width=0.0];
            }

            {
                rankdir = LR;
                rank    = same;

                ADDTOCACHE               [label="Add to cache", shape=box];
            }

            {
                rankdir = LR;
                rank    = same;

                EXITPOINT1 [shape=point, width=0.0];
                EXITPOINT2 [shape=point, width=0.0];
            }

            {
                rankdir = LR;
                rank    = same;

                RETURN                  [label="Return object", shape=box, style=filled, color="#66CC99"];
            }

            INITIALIZATION           -> KEYINCACHE;
            KEYINCACHE               -> RETRIEVEFROMCACHE        [label=" Yes"]
            KEYINCACHE               -> RETRIEVEFROMCONTEXT      [label="   No"]
            RETRIEVEFROMCACHE        -> KEEPFORTESTDURATION
            RETRIEVEFROMCONTEXT      -> KEEPFORTESTDURATION
            KEEPFORTESTDURATION      -> KEEPFORTESTDURATIONPOINT [label="      No"dir=none]
            KEEPFORTESTDURATION      -> ADDTOCACHE               [label="  Yes"]
            ADDTOCACHE               -> EXITPOINT1               [dir=none]
            KEEPFORTESTDURATIONPOINT -> EXITPOINT2               [dir=none]
            EXITPOINT1               -> EXITPOINT2               [dir=none]
            EXITPOINT1               -> RETURN
        }
        @enddot
        @option indexOrPredicate    [in] (int,callable) The index of the reader to obtain.
                                         It may also be a predicate, used to scan
                                         the available readers for a proper device.
        @option keepForTestduration [in] (bool) Whether the SmartDevice instance is to
                                         be used for the duration of the test
                                         case, or it is only a one-shot retrieval.

        @return The context smart device.
        """
        key    = id(indexOrPredicate)
        result = None
        if (key in self.__devices):
            result = self.__devices[key]
        else:
            device = self.getContext().getDevice(indexOrPredicate)

            if (device is not None):
                device = ContextSmartDevice(device, self)

                # Log the reader configuration
                try:
                    device.allocate()
                except Exception:                                                                                       # pylint:disable=W0703
                    self.log(_LEVEL_ERROR + _MASK_ALWAYS,
                             "Unable to access reader for %s" % (str(indexOrPredicate),))
                    raise
                # end try

                result = device

                if (keepForTestduration):
                    self.__devices[key] = result
                # end if
            # end if
        # end if
        
        if (result is None):
            self.fail("\n".join(("No device or reader available.",
                "This is is usually due to one of the following:",
                "1. The Config.ini file may be incorrect (check the TARGET section)",
                "2. The Libusb.ini file may be incorrect (wrong host/port combination)",
                "3. The SmartDevice's ProductID is different than the configuration one")))
        # end if

        return result
    # end def getDevice

    def assertDataOut(self, expected, msg = None):
        """
        Checks that the last response data matches the expected value

        @param  expected [in] (HexList) The expected value, as a HexList
        @option msg      [in] (str)    The error message
        """
        self.assertEqual(expected, self.getDevice().dataOut, msg)
    # end def assertDataOut

    def logCommand(self, msg, *args, **kwargs):
        """
        Set log of the command

        @param  msg    [in] (str)   Log text
        @param  args   [in] (tuple) Arguments
        @param  kwargs [in] (dict)  Keyword arguments
        """
        self.log(_LEVEL_COMMAND, msg, *args, **kwargs)
    # end def logCommand

    def assertResponse(self, responseValue, message, index = 0):
        """
        Utility function to check the value of the last sent sw on the specified
        device.

        @param  responseValue [in] (HexList) Value of the response
        @param  message       [in] (str) Message if error occurres
        @option index         [in] (int,callable) Device number or predicate
        """
        device = self.getDevice(index)
        expectedResponse = HexList(responseValue)
        self.assertEqual(expectedResponse, device.getResponse(), message)
    # end def assertResponse

    def assertMutes(self, func, *args, **kwargs):
        """
        Check if device mutes

        @param  func      [in] (callable) Function to run, mutinsm expected
        @param  args      [in] (tuple)    Arguments of the function
        @option kwargs    [in] (dict)     Keyword arguments of the function.

        If the keyword arguments contain the key "message", this key is used
        as the message to display in case of error.

        @attention  It is recommended to Reset the device every time it mutes.

        Example: We want to test the following function:
        @code
        def myFunction(a, b, c=None, d=None):
            # ...
            return None
        # end def myFunction
        @endcode

        Depending on the parameters, the following code will be used:
        - In order to test @c myFunction(1,2) :
          @code
          # Will call myFunction, with a set to 1, b set to 2,
          # c and d with their default values
          self.assertMutes(myFunction, (1,2))
          @endcode
        - In order to test @c myFunction(1,2,3) :
          @code
          # Will call myFunction, with a set to 1, b set to 2,
          # c set to 3 and d with their default values
          # Note the use of the dict for keyword arguments
          self.assertMutes(myFunction, (1,2), {'c': 3})
          @endcode
        - In order to test @c myFunction(1,2,c=3) (same as above):
          @code
          # Will call myFunction, with a set to 1, b set to 2,
          # c set to 3 and d with their default values
          # Note the use of the dict for keyword arguments
          self.assertMutes(myFunction, (1,2), {'c': 3})
          @endcode
        - In order to test @c myFunction(1,2,c=3,d=4) :
          @code
          # Will call myFunction, with a set to 1, b set to 2,
          # c set to 3 and d set to 4
          # Note the use of the dict for keyword arguments
          self.assertMutes(myFunction,
                           (1,2),
                           {'c': 3, 'd': 4})
          @endcode
        .
        """
        message = None
        failed  = None
        try:
            funcArgs = ()
            funcKwArgs = {}

            # variable -type arguments: We expect:
            # - A tuple (args)
            # - A dictionnary (kwargs)
            # - A string (optional: the message)

            for arg in args:
                # The tuple is the funcArgs
                if (isinstance(arg, tuple)):
                    funcArgs = arg
                elif (isinstance(arg, dict)):
                    funcKwArgs = arg
                elif (isinstance(arg, bytes)):
                    message = arg
                else:
                    raise ValueError("Invalid argument: %s" % (str(arg),))
                # end if
            # end for
            message = kwargs.setdefault("message", message)

            func(*funcArgs, **funcKwArgs)
        except SmartDeviceException as excp:
            if not (excp.getCause() in (SmartDeviceException.CAUSE_MUTE,
                                        SmartDeviceException.CAUSE_MUTE_RESET,)):
                raise
            # end if
            failed = False
        except Exception as excp:
            raise
        # end try

        if (    (failed is None)
            or  (failed)):
            self.fail(message or "The target did not mute")
        # end if
    # end def assertMutes
# end class DeviceTestCaseMixin

class DeviceTestCase(PyHarnessCase, DeviceTestCaseMixin):                                                                    # pylint:disable=R0901
    """
    DeviceTestCase implementation

    Provides additional testing methods, useful in a device context.
    """

    def setUp(self):
        """
        Test initialisation
        """
        PyHarnessCase.setUp(self)
        DeviceTestCaseMixin.setUp(self)
    # end def setUp

    def tearDown(self):
        """
        Destructor of the test
        """
        DeviceTestCaseMixin.tearDown(self)
        PyHarnessCase.tearDown(self)
    # end def tearDown
# end class DeviceTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
