#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.test.context_test
:brief:  ContextLoader test implementation
         This module contains the test cases for the context module.
:author: Christophe Roquebert <croquebert@logitech.com>
:date:   2018/09/11
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
import unittest
from os import mkdir
from os import remove
from os.path import abspath
from os.path import join
from random import random
from shutil import rmtree
from time import sleep
from time import time
from unittest import TestCase

from pyharness.consts import DEFAULT_INPUT_DIRECTORY
from pyharness.context import CollectContext
from pyharness.context import ContextLoader
from pyharness.context import FeaturesProvider
from pyharness.subsystem.ini.subsysteminstantiationconnector import IniSubSystemInstantiationImporter
from pyharness.subsystem.python.subsystemdefinitionconnector import PythonSubSystemDefinitionImporter
from pyharness.subsystem.subsystembuilder import SubSystemBuilder
from pylibrary.tools.tempfile import mkdtemp
from pylibrary.tools.threadutils import ThreadedExecutor


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class FeaturesProviderTestCase(TestCase):
    """
    Tests for FeaturesProvider class
    """
    RefClass = FeaturesProvider

    @classmethod
    def _createInstance(cls):
        """
        Create an instance of referenced class

        @return (object) Instance of referenced class
        """
        return cls.RefClass()
    # end def _createInstance

    def testConstructor(self):
        """
        Tests the constructor
        """
        self.assertIsNotNone(self._createInstance(),
                             'An instance should be created')
    # end def testConstructor

    def testGetFeatures(self):
        """
        Tests getFeatures method
        """
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.getFeatures)

    # end def testGetFeatures

# end class FeaturesProviderTestCase


class CollectContextTestCase(TestCase):
    """
    Tests for CollectContext class
    """
    RefClass = CollectContext

    RESULT = 0

    @classmethod
    def _createInstance(cls, proxi=None):
        """
        Create an instance of referenced class

        @option proxi [in] (object) Proxyed object

        @return (object) Instance of referenced class
        """

        if proxi is None:
            proxi = CollectContextTestCase.TestNextClass()
        # end if

        return cls.RefClass(proxi)

    # end def _createInstance

    class TestNextClass(object):
        """
        Testing class for next parameter
        """
        @staticmethod
        def get_result():
            """
            Get result value

            @return (int) Result value
            """
            return CollectContextTestCase.RESULT
        # end def get_result
    # end class TestNextClass

    def testCollectOnly(self):
        """
        Tests collectOnly class method
        """
        self.assertTrue(self.RefClass.collectOnly(),
                        'Wrong collectOnly result')

    # end def testCollectOnly

    def testGetAttr(self):
        """
        Tests __getattr__ method
        """
        instance = self._createInstance()

        self.assertEqual(self.RESULT,
                         instance.get_result(),
                         'Wrong result value')

    # end def testGetAttr

# end class CollectContextTestCase


class ContextLoaderTestCase(TestCase):
    """
    Test case for the ContextLoader class
    """

    def setUp(self):
        """
        Initialize test
        """
        TestCase.setUp(self)

        self.srcPath = None

        # Create the TESTSUITES path
        # Create a convenient hierarchy
        self.__tempDirPath = abspath(mkdtemp("", "test_%s" % self.id()))

        # Create the Settings.ini file
        local_path = join(self.__tempDirPath, "LOCAL")
        mkdir(local_path)

        config_path = join(local_path, "Settings.ini")
        with open(config_path, "w+") as configIni:
            configIni.writelines(("[PRODUCT]\n",
                                  "value = \"V_1_0\"\n",
                                  "[VARIANT]\n",
                                  "value = \"PATCH_1\"\n",
                                  "[MODE]\n",
                                  "value = \"RELEASE\"\n",
                                  "[TARGET]\n",
                                  "value = \"SIMULATOR\"\n",
                                  ))
        # end with

        src_path = join(self.__tempDirPath, "TESTSUITES")
        mkdir(src_path)

        random_element = self.__tempDirPath[-4:]
        feature_file_path = join(src_path, "features" + random_element + "_internal.py")
        with open(feature_file_path, "w+") as featuresFile:
            featuresFile.writelines(("from pyharness.systems import AbstractSubSystem\n",
                                     "class RootSubSystem( AbstractSubSystem ):\n",
                                     "    def __init__(self):\n",
                                     "        AbstractSubSystem.__init__(self, \"ROOT\")\n",
                                     "        \n"
                                     "        self.RUNTIME = AbstractSubSystem(\"RUNTIME\")\n",
                                     "        self.RUNTIME.F_Enabled = True\n"
                                     "        self.RUNTIME.F_SAMPLE              = 0\n",
                                     '        self.RUNTIME.F_DeviceManager = "pyusb.libusbdriver.DeviceManagerMock"\n',
                                     '        self.RUNTIME.F_UsbContextClass = "pytransport.usb.logiusbcontext.logiusbcontext.LogiusbUsbContext"\n',
                                     '        self.RUNTIME.DEBUGGERS = self.DebuggersSubSystem()\n',
                                     "        \n"
                                     '        self.LOGGING = AbstractSubSystem(\"LOGGING\")\n',
                                     "        self.LOGGING.F_EmulatorVerbose = False\n",
                                     '    # end def __init__\n',
                                     '\n',
                                     '    class DebuggersSubSystem(AbstractSubSystem):\n',
                                     '        def __init__(self):\n',
                                     '            AbstractSubSystem.__init__(self, "DEBUGGERS")\n',
                                     '            self.F_Enabled = True\n',
                                     '            self.F_Targets = ()\n',
                                     '            self.F_Types = ()\n',
                                     '        # end def __init__\n',
                                     '    # end class DebuggersSubSystem\n',
                                     '# end class RuntimeSubSystem\n',
                                     ))
        # end with

        base_path = join(self.__tempDirPath, "TESTSUITES", "base")
        mkdir(base_path)

        file_path = join(base_path, "features" + random_element + "_internal.py")
        with open(file_path, "w+") as featuresFile:
            featuresFile.writelines(
                ("from pyharness.systems import AbstractSubSystem\n",
                 'class ProductSubSystem(AbstractSubSystem):\n',
                 '    def __init__(self):\n',
                 '        AbstractSubSystem.__init__(self, "PRODUCT")\n',
                 '        self.F_Enabled = True\n',
                 '        self.F_IsMice = False\n',
                 '        self.F_IsKeyPad = False\n',
                 '        self.F_ProductReference = None\n',
                 '        self.FEATURES = self.FeaturesSubSystem()\n',
                 '        self.DEVICE = self.DeviceSubSystem()\n',
                 '        self.NVS_CHUNK_IDS = self.NvsChunkIdsSubSystem()\n',
                 '        self.DUAL_BANK = self.DualBankSubSystem()\n',
                 '    # end def __init__\n',
                 '    class FeaturesSubSystem(AbstractSubSystem):\n',
                 '        def __init__(self):\n',
                 '            AbstractSubSystem.__init__(self, "FEATURES")\n',
                 '            self.COMMON = self.CommonFeatureSubSystem()\n',
                 '            self.VLP = self.VariableLengthProtocolSubSystem()\n',
                 '            self.GAMING = self.GamingSubSystem()\n',
                 '        # end def __init__\n',
                 '        class CommonFeatureSubSystem(AbstractSubSystem):\n',
                 '            def __init__(self):\n',
                 '                AbstractSubSystem.__init__(self, "COMMON")\n',
                 '                self.SPECIAL_KEYS_MSE_BUTTONS = self.SpecialKeysMSEButtonsSubSystem()\n',
                 '                self.OPTICAL_SWITCHES = self.OpticalSwitchesSubSystem()\n',
                 '                self.CONFIGURABLE_PROPERTIES = self.ConfPropSubSystem()\n',
                 '                self.PROPERTY_ACCESS = self.PropertyAccessSubSystem()\n',
                 '            # end def __init__\n',
                 '            class SpecialKeysMSEButtonsSubSystem(AbstractSubSystem):\n',
                 '                def __init__(self):\n',
                 '                    AbstractSubSystem.__init__(self, "SPECIAL_KEYS_MSE_BUTTONS")\n',
                 '                    self.F_CidInfoTable = None\n',
                 '                    self.CID_INFO_TABLE = self.CidInfoTable()\n',
                 '                # end def __init__\n',
                 '                class CidInfoTable(AbstractSubSystem):\n',
                 '                    def __init__(self):\n',
                 '                        AbstractSubSystem.__init__(self, "CID_INFO_TABLE")\n',
                 '                        self.F_Enabled = False\n',
                 '                    # end def __init__\n',
                 '                # end class CidInfoTable\n',
                 '            # end class SpecialKeysMSEButtonsSubSystem\n',
                 '            class OpticalSwitchesSubSystem(AbstractSubSystem):\n',
                 '                def __init__(self):\n',
                 '                    AbstractSubSystem.__init__(self, "OPTICAL_SWITCHES")\n',
                 '                    self.F_NbColumns = None\n',
                 '                    self.F_SupportedKeyLayout = ()\n',
                 '                # end def __init__\n',
                 '            # end class OpticalSwitchesSubSystem\n',
                 '            class ConfPropSubSystem(AbstractSubSystem):\n',
                 '                def __init__(self):\n',
                 '                    AbstractSubSystem.__init__(self, "CONFIGURABLE_PROPERTIES")\n',
                 '                    self.F_SupportedProperties = ()\n',
                 '                    self.F_SpecificPropertiesSizes = ()\n',
                 '                # end def __init__\n',
                 '            # end class ConfPropSubSystem\n',
                 '            class PropertyAccessSubSystem(AbstractSubSystem):\n',
                 '                def __init__(self):\n',
                 '                    AbstractSubSystem.__init__(self, "PROPERTY_ACCESS")\n',
                 '                    self.F_SwAccessibleProperties = ()\n',
                 '                    self.F_SwAccessiblePropertiesSizes = ()\n',
                 '                # end def __init__\n',
                 '            # end class PropertyAccessSubSystem\n',
                 '        # end class CommonFeatureSubSystem\n',
                 '        class VariableLengthProtocolSubSystem(AbstractSubSystem):\n',
                 '            def __init__(self):\n',
                 '                AbstractSubSystem.__init__(self, "VLP")\n',
                 '                self.COMMON = self.CommonFeatureSubSystem()\n',
                 '            # end def __init__\n',
                 '            class CommonFeatureSubSystem(AbstractSubSystem):\n',
                 '                def __init__(self):\n',
                 '                    AbstractSubSystem.__init__(self, "COMMON")\n',
                 '                    self.CONTEXTUAL_DISPLAY = self.ContextualDisplaySubSystem()\n',
                 '                # end def __init__\n',
                 '                class ContextualDisplaySubSystem(AbstractSubSystem):\n',
                 '                    def __init__(self):\n',
                 '                        AbstractSubSystem.__init__(self, "CONTEXTUAL_DISPLAY")\n',
                 '                        self.DISPLAY_INFO_TABLE = self.DisplayInfoTable()\n',
                 '                        self.BUTTON_TABLE = self.ButtonTable()\n',
                 '                        self.VISIBLE_AREA_TABLE = self.VisibleAreaTable()\n',
                 '                    # end def __init__\n',
                 '                    class DisplayInfoTable(AbstractSubSystem):\n',
                 '                        def __init__(self):\n',
                 '                            AbstractSubSystem.__init__(self, "DISPLAY_INFO_TABLE")\n',
                 '                            self.F_Enabled = False\n',
                 '                            self.F_DisplayIndex = ()\n',
                 '                            self.F_DisplayShape = ()\n',
                 '                            self.F_DisplayDimension = ()\n',
                 '                            self.F_HorizontalRes = ()\n',
                 '                            self.F_VerticalRes = ()\n',
                 '                            self.F_ButtonCount = ()\n',
                 '                            self.F_VisibleAreaCount = ()\n',
                 '                        # end def __init__\n',
                 '                    # end class DisplayInfoTable\n',
                 '                    class ButtonTable(AbstractSubSystem):\n',
                 '                        def __init__(self):\n',
                 '                            AbstractSubSystem.__init__(self, "BUTTON_TABLE")\n',
                 '                            self.F_Enabled = False\n',
                 '                            self.F_ButtonIndex = ()\n',
                 '                            self.F_ButtonShape = ()\n',
                 '                            self.F_ButtonLocationX = ()\n',
                 '                            self.F_ButtonLocationY = ()\n',
                 '                            self.F_ButtonLocationWidth = ()\n',
                 '                            self.F_ButtonLocationHeight = ()\n',
                 '                        # end def __init__\n',
                 '                    # end class ButtonTable\n',
                 '                    class VisibleAreaTable(AbstractSubSystem):\n',
                 '                        def __init__(self):\n',
                 '                            AbstractSubSystem.__init__(self, "VISIBLE_AREA_TABLE")\n',
                 '                            self.F_Enabled = False\n',
                 '                            self.F_VisibleAreaIndex = ()\n',
                 '                            self.F_VisibleAreaShape = ()\n',
                 '                            self.F_VisibleAreaLocationX = ()\n',
                 '                            self.F_VisibleAreaLocationY = ()\n',
                 '                            self.F_VisibleAreaLocationWidth = ()\n',
                 '                            self.F_VisibleAreaLocationHeight = ()\n',
                 '                        # end def __init__\n',
                 '                    # end class VisibleAreaTable\n',
                 '                # end class ContextualDisplaySubSystem\n',
                 '            # end class CommonFeatureSubSystem\n',
                 '        # end class VariableLengthProtocolSubSystem\n',
                 '        class GamingSubSystem(AbstractSubSystem):\n',
                 '            def __init__(self):\n',
                 '                AbstractSubSystem.__init__(self, "GAMING")\n',
                 '                self.RGB_EFFECTS = self.RGBEffectsSubSystem()\n',
                 '                self.ONBOARD_PROFILES = self.OnboardProfilesSubSystem()\n',
                 '            # end def __init__\n',
                 '            class RGBEffectsSubSystem(AbstractSubSystem):\n',
                 '                def __init__(self):\n',
                 '                    AbstractSubSystem.__init__(self, "RGB_EFFECTS")\n',
                 '                    self.F_Enabled = False\n',
                 '                # end def __init__\n',
                 '            # end class RGBEffectsSubSystem\n',
                 '            class OnboardProfilesSubSystem(AbstractSubSystem):\n',
                 '                def __init__(self):\n',
                 '                    AbstractSubSystem.__init__(self, "ONBOARD_PROFILES")\n',
                 '                    self.F_Enabled = False\n',
                 '                # end def __init__\n',
                 '            # end class OnboardProfilesSubSystem\n',
                 '        # end class GamingSubSystem\n',
                 '    # end class FeaturesSubSystem\n',
                 '    class NvsChunkIdsSubSystem(AbstractSubSystem):\n',
                 '        def __init__(self):\n',
                 '            AbstractSubSystem.__init__(self, "NVS_CHUNK_IDS")\n',
                 '            self.F_IsGamingVariant = False\n',
                 '            self.F_ChunkIdNames = ()\n',
                 '            self.F_ChunkIdValues = ()\n',
                 '        # end def __init__\n',
                 '    # end class NvsChunkIdsSubSystem\n',
                 '    class DeviceSubSystem(AbstractSubSystem):\n',
                 '        def __init__(self):\n',
                 '            AbstractSubSystem.__init__(self, "DEVICE")\n',
                 '            self.BATTERY = self.BatterySubSystem()',
                 '        # end def __init__\n',
                 '        class BatterySubSystem(AbstractSubSystem):\n',
                 '            def __init__(self):\n',
                 '                AbstractSubSystem.__init__(self, "BATTERY")\n',
                 '                self.F_NominalVoltage = 1.3\n',
                 '            # end def __init__\n',
                 '        # end class BatterySubSystem\n',
                 '    # end class DeviceSubSystem\n',
                 '    class DualBankSubSystem(AbstractSubSystem):\n',
                 '        def __init__(self):\n',
                 '            AbstractSubSystem.__init__(self, "DUAL_BANK")\n',
                 '            self.SLOTS = self.SlotsSubSystem()\n',
                 '            self.BOOTLOADER_IMAGE_COMMUNICATION = self.BootImgCommSubSystem()\n',
                 '        # end def __init__\n',
                 '        class SlotsSubSystem(AbstractSubSystem):\n',
                 '            def __init__(self):\n',
                 '                AbstractSubSystem.__init__(self, "SLOTS")\n',
                 '                self.F_Base = ()\n',
                 '                self.F_VersionMajor = ()\n',
                 '                self.F_VersionMinor = ()\n',
                 '                self.F_VersionRevision = ()\n',
                 '                self.F_VersionBuildNumber = ()\n',
                 '                self.F_LoadAddr = ()\n',
                 '                self.F_HeaderSize = ()\n',
                 '                self.F_ProtectTLVSize = ()\n',
                 '            # end def __init__\n',
                 '        # end class SlotsSubSystem\n',
                 '        class BootImgCommSubSystem(AbstractSubSystem):\n',
                 '            def __init__(self):\n',
                 '                AbstractSubSystem.__init__(self, "BOOTLOADER_IMAGE_COMMUNICATION")\n',
                 '                self.F_GitHash = None\n',
                 '            # end def __init__\n',
                 '        # end class BootImgCommSubSystem\n',
                 '    # end class DualBankSubSystem\n',
                 '# end class ProductSubSystem\n',
                 ))
        # end with
        
        path = join(self.__tempDirPath, DEFAULT_INPUT_DIRECTORY)
        mkdir(path)

        path = join(path, "V_1_0")
        mkdir(path)

        # Create main settings file
        main_ini_file_path = join(path, "main.settings.ini")
        with open(main_ini_file_path, "w+") as fs:
            fs.write('\n'.join(('',
                                '[RUNTIME]',
                                'SAMPLE=1',
                                '[RUNTIME/DEBUGGERS]',
                                'Targets = ("Device",             "Receiver",                   )',
                                'Types   = ("QuarkJlinkDebugger", "ReceiverMesonJlinkDebugger", )',
                                )))
        # end with

        path = join(path, "PATCH_1")
        mkdir(path)

        # Create variant settings file
        ini_file_path = join(path, "PATCH_1.settings.ini")
        with open(ini_file_path, "w+") as fs:
            fs.write('\n'.join(('',
                                '[RUNTIME]',
                                'SAMPLE=2')))
        # end with

        path = join(path, "SUBPATCH_1")
        mkdir(path)

        # Create sub variant settings file
        ini_file_path = join(path, "SUBPATCH_1.settings.ini")
        with open(ini_file_path, "w+") as fs:
            fs.write('\n'.join(('',
                                '[RUNTIME]',
                                'SAMPLE=3')))
        # end with

        # The TESTSUITES directory of the created fixture is appended to the
        # PYTHONPATH for the remainder of the test.
        # This should only be done for the current thread,
        sys.path.insert(0, src_path)
        self.srcPath = src_path
    # end def setUp

    @staticmethod
    def _createInstance():
        """
        Creates a new instance of the ContextLoader

        @return A new instance of a ContextLoader
        """
        sub_system_builder = SubSystemBuilder(subSystemDefinitionImporter=PythonSubSystemDefinitionImporter(),
                                              subSystemInstantiationImporter=IniSubSystemInstantiationImporter())
        return ContextLoader(subSystemBuilder=sub_system_builder)
    # end def _createInstance

    def tearDown(self):
        """
        Clean up test
        """
        if self.srcPath is not None:
            sys.path.remove(self.srcPath)
        # end if

        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    def test_Load(self):
        """
        Test context loading, from a temporary directory
        """
        context_loader = self._createInstance()

        local_path = join(self.__tempDirPath, "LOCAL")
        path_to_ini = join(local_path, "Settings.ini")
        remove(path_to_ini)

        # The first access raises an error and creates the Settings.ini file.
        self.assertRaises(IOError, context_loader.load, (self.__tempDirPath,))

        context = context_loader.load((self.__tempDirPath,), overrides=('TARGET.value=DEVICE',))

        self.assertNotEqual(None, context, "Unable to load simple context")
    # end def test_Load

    def test_ContextSwitch(self):
        """
        Test context loading, from a temporary directory

        Switchs back and forth between variants
        """
        context_loader = self._createInstance()
        context = context_loader.load((self.__tempDirPath,))

        self.assertNotEqual(None, context, "Unable to load simple context")

        # We are now on variant V_1_0/PATCH_1
        self.assertEqual(2,
                         context.getFeatures().RUNTIME.F_SAMPLE,
                         "Unexpected initial feature value")
        self.assertEqual("PATCH_1",
                         context.getCurrentVariant(),
                         "Unexpected initial variant")

        # Switch to the sub-context
        new_context = context_loader.deriveContext(context, variant="PATCH_1/SUBPATCH_1")
        self.assertEqual(3,
                         new_context.getFeatures().RUNTIME.F_SAMPLE,
                         "Unexpected feature value after context switch")
        self.assertEqual("PATCH_1/SUBPATCH_1",
                         new_context.getCurrentVariant(),
                         "Unexpected derived variant")

        # Check that the old context has not been modified
        self.assertEqual(2,
                         context.getFeatures().RUNTIME.F_SAMPLE,
                         "Unexpected initial feature value")
        self.assertEqual("PATCH_1",
                         context.getCurrentVariant(),
                         "Unexpected initial variant")
    # end def test_ContextSwitch

    def testGetDebugger_Index(self):
        """
        Tests Debugger obtaining, based on the index (0)
        """
        context_loader = self._createInstance()

        context = context_loader.load((self.__tempDirPath,))

        debugger = context.getDebugger(0)
        self.assertNotEqual(None,
                            debugger,
                            "Unable to retrieve debugger by index")
    # end def testGetDebugger_Index

    @unittest.skip("skipping if debugger not available")
    def testGetDebugger_Predicate(self):
        """
        Tests Debugger obtaining, based on a predicate.

        The predicate test for a device, that understands the SELEC MF command
        """
        context_loader = self._createInstance()

        context = context_loader.load((self.__tempDirPath,))

        def predicate_ok(device):
            """
            Filter a Device.

            @param  device [in] (SmartDevice) The device object to test

            @return (bool) Whether the device is accepted or not.
            """
            device.powerUp()
            sleep(0.5)
            return True
        # end def predicate_ok

        def predicate_nok(local_debugger):
            """
            Filter a debugger.

            @param  local_debugger [in] (Debugger) The debugger object to test

            @return (bool) Whether the debugger is accepted or not.
            """
            local_debugger.powerUp()
            sleep(0.5)
            return False
        # end def predicate_nok

        def predicate_true(unused):
            """
            Always returns True

            @param  unused [in] (object) The element to test

            @return Always True
            """
            return True
        # end def predicate_true
        debugger = context.getDebugger(predicate_true)
        self.assertNotEqual(None,
                            debugger,
                            "Unable to retrieve Debugger by True predicate")
        del debugger
        context.clearLockCache(predicate_true)

        debugger = context.getDebugger(predicate_nok)
        self.assertEqual(None,
                         debugger,
                         "Able to retrieve debugger by conditional False predicate")
        del debugger
        context.clearLockCache(predicate_nok)

        tick = time()
        debugger = context.getDebugger(predicate_ok)
        first_time = time() - tick
        self.assertNotEqual(None,
                            debugger,
                            "Unable to retrieve debugger by conditional True predicate")
        del debugger

        # The OK predicate should use the cache, therefore taking a lot less
        # time the second time round.
        tick = time()
        context.getDebugger(predicate_ok)
        second_time = time() - tick
        self.assertEqual(True,
                         second_time < (first_time / 10),
                         "Caching should have occured for a second predicate call.")
    # end def testGetDevice_Predicate

    def DebuggertestGetDevice_MultiThread(self):
        """
        Test multi-threaded access to the Debugger from the context.

        With enough threads running in parallel for enough time, this
        should cover most deadlocks...
        """

        context_loader = self._createInstance()

        context = context_loader.load((self.__tempDirPath,))

        def predicate_true(unused):
            """
            Matches a device against a predicate

            @param  unused [in] (object) The object to test.

            @return True
            """
            return True
        # end def predicate_true

        n_locks = 1
        marker = [True]
        corruption = [False]
        error = []

        def task():
            """
            Thread worker function

            @return A sequence of additional tasks to perform, or None.
            """
            try:
                if marker[0]:
                    debugger = context.getDebugger(predicate_true)

                    random_marker = random()
                    debugger.randomMarker = random_marker
                    debugger.powerUp()
                    sleep(random())

                    if random_marker != debugger.randomMarker:
                        corruption[0] = True
                    # end if

                    return (task,)
                # end if
            except Exception as excp:                                                                                   # pylint:disable=W0703
                # Ignore exceptions for this function
                error.append(excp)
                import traceback
                traceback.print_exc()
                marker[0] = False
            # end try
        # end def task

        tasks = [task] * n_locks*3

        def stop():
            """
            Stopping task
            """
            marker[0] = False
        # end def stop
        tasks.append(stop)
        executor = ThreadedExecutor(tasks,
                                    max_threads=n_locks,
                                    name="Test")
        executor.execute()

        if len(error) > 0:
            raise error[0]
        # end if

        self.assertEqual(False,
                         corruption[0],
                         "Data was corrupted: Thread safety not guaranteed")
    # end def testGetDebugger_MultiThread

    def test_GetCurrentMode(self):
        """
        Tests mode obtaining, from the Settings.ini file
        """
        context_loader = self._createInstance()

        context = context_loader.load((self.__tempDirPath,))

        self.assertEqual("RELEASE",
                         context.getCurrentMode(),
                         "Unable to extract the correct MODE from the context")
    # end def test_GetCurrentMode

    def test_GetCurrentProduct(self):
        """
        Tests product obtaining, from the Settings.ini file
        """
        context_loader = self._createInstance()

        context = context_loader.load((self.__tempDirPath,))

        self.assertEqual("V_1_0",
                         context.getCurrentProduct(),
                         "Unable to extract the correct PRODUCT from the context")
    # end def test_GetCurrentProduct

    def test_GetCurrentVariant(self):
        """
        Tests variant obtaining, from the Settings.ini file
        """
        context_loader = self._createInstance()

        context = context_loader.load((self.__tempDirPath,))

        self.assertEqual("PATCH_1",
                         context.getCurrentVariant(),
                         "Unable to extract the correct VARIANT from the context")
    # end def test_GetCurrentVariant

    def test_GetInputDir(self):
        """
        Test Input directory formatting
        """
        context_loader = self._createInstance()

        context = context_loader.load((self.__tempDirPath,))

        expected_input_dir = abspath(join(self.__tempDirPath, '..', 'RELEASE', 'V_1_0', 'PATCH_1'))

        obtained_input_dir = context.getInputDir()

        self.assertEqual(expected_input_dir,
                         obtained_input_dir,
                         "Unable to build the correct input directory")
    # end def test_GetInputDir

    def test_GetInputFilePath(self):
        """
        Test Input directory formatting
        """
        context_loader = self._createInstance()

        context = context_loader.load((self.__tempDirPath,))
        f = context.getFeatures()
        f.RUNTIME._AbstractSubSystem__readOnlyAttr.remove(r'F_InputDirPattern')                                         # pylint:disable=W0212
        context.getFeatures().RUNTIME.F_InputDirPattern = r'C:\This is a Non-Existing directory'

        self.assertRaises(ValueError,
                          context.getInputFilePath,
                          'test.c')
    # end def test_GetInputFilePath
# end class ContextLoaderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
