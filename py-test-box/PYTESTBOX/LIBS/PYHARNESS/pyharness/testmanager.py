# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.testmanager

@brief  Defines the interface necessary to control the execution of a test run.

@author christophe.roquebert

@date   2018/02/04
 '''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                             import abspath
from os.path                             import normpath
from pylibrary.tools.config              import CachingConfigParser
from pylibrary.tools.config              import ConfigParser
from pylibrary.tools.importutils         import importFqn
from pylibrary.tools.listener            import Listenable
from pylibrary.tools.threadutils         import synchronized
from pyharness.arguments                 import KeywordArguments
from pyharness.consts                    import DEFAULT_INPUT_DIRECTORY
from pyharness.consts                    import DEFAULT_OUTPUT_DIRECTORY
from pyharness.context                   import CollectContext
from pyharness.context                   import ContextLoader
from pyharness.core                      import MonoThreadTestRunner
from pyharness.core                      import MultiThreadTestRunner as TestRunner
from pyharness.core                      import TestAccess
from pyharness.core                      import TestCase
from pyharness.core                      import TestListener
from pyharness.core                      import TestLoader
from pyharness.core                      import TestSuite
from pyharness.extensions                import level
from pyharness.files.jrl                 import JrlFile
from os                                 import F_OK
from os                                 import R_OK
from os                                 import access
from os                                 import listdir
from os.path                            import exists
from os.path                            import isdir
from os.path                            import join
from types                              import MethodType
from types                              import FunctionType
from weakref                            import ref
import re

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TestDescriptor(Listenable):
    '''
    The description of a test, sufficient for piloting the validation.
    '''

    STATE_UNKNOWN = 0
    STATE_SUCCESS = 10
    STATE_FAILURE = 20
    STATE_ERROR = 30
    STATE_MISSING = 40
    STATE_RUNNING = 100

    ## @name The descriptor types
    ##@{
    TYPE_UNKNOWN = 0
    TYPE_TEST = 10
    TYPE_SUITE = 20
    TYPE_RUN = 30
    ##@}

    class Actions(object):
        '''
        A constants class that contains the notifications available for this descriptor.

        These constants should be powers of 2, to that a mask can be applied to the notification.
        '''
        ACTION_MODIFY_STATE     = 1 ##< The descriptor state was changed
        ACTION_MODIFY_CHILDREN  = 2 ##< The list of children was changed (add, remove... This is not used for a child state change.)

        ACTION_ALL = (  ACTION_MODIFY_STATE
                      | ACTION_MODIFY_CHILDREN)
    # end class Actions

    def __init__(self, testId,
                       state            = STATE_UNKNOWN,
                       descriptorType   = TYPE_UNKNOWN):
        '''
        Constructor.

        @param  testId         [in] (str) The test id wrapped by this descriptor.
        @option state          [in] (str) The initial state of the test, from STATE_xyz constants.
        @option descriptorType [in] (int) The type of the described test, from TYPE_xyz constants.
        '''
        Listenable.__init__(self)

        self._children = []
        self.parent = None
        self.testId = testId
        self._state = state
        self.type = descriptorType
    # end def __init__

    def getType(self):
        '''
        Obtain the descriptor type.

        @return (int) The descriptor type, from the list:
        - TYPE_UNKNOWN
        - TYPE_TEST
        - TYPE_SUITE
        - TYPE_RUN
        '''
        return self.type
    # end def getType

    def getParent(self):
        '''
        Obtains the parent Descriptor, None if not found

        @return The parent of the current TestDescriptor
        '''
        if (self.parent is not None):
            return self.parent()
        # end if

        return None
    # end def getParent

    def setParent(self, parent):
        '''
        Sets the parent descriptor

        @param  parent [in] (TestDescriptor) The parent TestDescriptor.
        '''
        if (parent is None):
            self.parent = None
        else:
            self.parent = ref(parent)
        # end if
    # end def setParent

    def getState(self):
        '''
        Obtains the state of the test.

        @return The state of the test.
        '''
        return self._state
    # end def getState

    def setState(self, state):
        '''
        Sets the state of the test.

        This will send change notifications to the listeners, if any

        @param  state [in] (str) The state to set
        '''
        if (self._state != state):
            self._state = state

            self.notifyListeners(source=self,
                                 action=TestDescriptor.Actions.ACTION_MODIFY_STATE)

            parent = self.getParent()
            if (parent is not None):
                parent.updateState(state)
            # end if
        # end if
    # end def setState

    def updateState(self, childState=None):
        '''
        Updates the current state from the children.

        If childState is None, perform a full update.
        If childState is not None, optimize the update.

        @option childState [in] (int) The new child state
        '''
        currentState = self.getState()

        if ((childState is None) or (childState < currentState)):
            # Child state is better: We have to rescan the children
            # TODO Using a cache would probably be much more efficient.
            childStates = [child.getState() for child in self.getChildren()]
            childStates.append(-1)
            newState = max(childStates)

            if (    (newState > -1)
                and (newState != currentState)):
                self.setState(newState)
            # end if

        elif (childState > currentState):
            # Child state is worse: Align to the worst state
            self.setState(childState)

        else:
            # No change
            pass
        # end if

    # end def updateState

    def addChild(self, child):
        '''
        Adds a child to the current descriptor.

        @param  child [in] (TestDescriptor) The child to add to the current object.

        This sets the child's parent reference to the current object
        '''
        child.setParent(self)
        self._children.append(child)

        self.notifyListeners(source=self,
                             action=TestDescriptor.Actions.ACTION_MODIFY_CHILDREN)
    # end def addChild

    def removeChild(self, child):
        '''
        Removes a child from the current descriptor.

        This also clears the child's parent reference to the current object.

        @param  child [in] (TestDescriptor) The child to remove from the current object.
        '''
        if (child.getParent() is self):
            child.setParent(None)
        # end if

        self._children.remove(child)

        self.notifyListeners(source=self,
                             action=TestDescriptor.Actions.ACTION_MODIFY_CHILDREN)
    # end def removeChild

    def getChildren(self):
        '''
        Obtains the list of children for the current descriptor.

        @return (tuple) an immutable list of children.
        '''
        return tuple(self._children)
    # end def getChildren

    def __toString(self, indent=0):
        '''
        Pretty-prints the test descriptor

        @option indent [in] (int) The number of spaces to prefix each line with.

        @return (string) The pretty-printed object
        '''

        resultList = []
        resultList.append("   " * indent + self.testId)

        for child in self._children:
            resultList.append(child.__toString(indent + 1))                                                               # pylint:disable=W0212
        # end for

        return '\n'.join(resultList)
    # end def __toString

    def __str__(self):
        '''
        Converts the current object to a string

        @return The current object, as a string.
        '''
        return self.__toString(0)
    # end def __str__

    def __repr__(self):
        '''
        Converts the current object to a string

        @return The current object, as a string.
        '''
        return str(self)
    # end def __repr__

    def deepClone(self):
        '''
        Creates a deep copy of the current descriptor.

        @return (TestDescriptor) A clone of the current object.
        '''
        result = TestDescriptor(self.testId, self._state, self.type)
        for child in self._children:
            result.addChild(child.deepClone())
        # end for

        return result
    # end def deepClone
# end class TestDescriptor

class VersionDescriptor(object):
    '''
    A node that describes a version.

    A version has a name (matching its on-disk directory name),
    children (themselves VersionDescriptor) and a selectable character
    (The root VersionDescriptor cannot be selected for instance).
    '''

    def __init__(self, name,
                       selectable=True):
        '''
        Constructor for this version, that takes a given name.

        @param  name       [in] (str)  The name for this version
        @option selectable [in] (bool) Whether this version can be selected by the user.
        '''
        self.name = name
        self.selectable = selectable
        self.children = []
    # end def __init__

    def flatten(self, leavesOnly=True, root=None):
        '''
        Obtains a flattened list of child paths to the child versions

        @option leavesOnly [in] (bool) Whether nodes should be added as well as leaves.
        @option root       [in] (str)  The parent prefix

        @return A list of paths to the children.
        '''
        result = []

        current = None
        if (root is None):
            current = self.name
        elif (self.name is not None):
            current = root + "/" + self.name
        # end if

        if (   (not leavesOnly)
            or (len(self.children) == 0)):
            if (current is not None):
                result.append(current)
            # end if
        # end if

        for child in self.children:
            result.extend(child.flatten(root=current))
        # end for

        return result
    # end def flatten

    def __str__(self):
        '''
        Converts the current object to a string

        @return The current object, as a string.
        '''
        return str(self.name)
    # end def __str__

    __repr__ = __str__
# end class VersionDescriptor


class CollectListener(TestListener):
    '''
    Local test listener, used to collect the hierarchy of the test run.
    '''
    def __init__(self):
        '''
        Constructor.

        Initializes the collection test listener
        '''

        TestListener.__init__(self, None, None, None, None)
        self.ignoreCollection = False

        self.descriptorStack = []
        self.descriptorStack.append(TestDescriptor("Root",
                                                   state=TestDescriptor.STATE_UNKNOWN,
                                                   descriptorType=TestDescriptor.TYPE_RUN))
    # end def __init__

    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''

        if (isinstance(test, TestSuite)):
            testType = TestDescriptor.TYPE_SUITE
        elif (isinstance(test, TestCase)):
            testType = TestDescriptor.TYPE_TEST
        else:
            testType = TestDescriptor.TYPE_UNKNOWN
        # end if


        descriptor = TestDescriptor(test.id(),
                                    state=TestDescriptor.STATE_UNKNOWN,
                                    descriptorType=testType)
        self.descriptorStack[-1].addChild(descriptor)
        self.descriptorStack.append(descriptor)
    # end def startTest

    def stopTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.stopTest
        '''
        del self.descriptorStack[-1]
    # end def stopTest
# end class CollectListener

class TestManager(object):                                                                                              # pylint:disable=R0922
    '''
    Defines the interface used to pilot a test run.

    It provides additional methods that can audit the current test run, as well
    as the underlying structure of the test hierarchy.
    '''

    def __init__(self, kwArgs):
        '''
        Constructor.

        In order to be as generic as possible, the initialization of a TestManager
        only uses kwArgs: A dict to configuration parameters.
        It is up to the implementation to interpret these parameters.

        @param  kwArgs [in] (dict) The keyword parameters
        '''
        self._kwArgs = KeywordArguments.DEFAULT_ARGUMENTS.copy()
        self._kwArgs.update(kwArgs)
        self.verbosity = None
        self.root = None
        self.debug = None
        self.includepatterns = None
        self.excludepatterns = None
        self.levels = None
        self.nolevels = None
        self.outputdir = None
        self.rootsuite = None

        self.descriptorCache = {}

        self._handleParameters(kwArgs)
    # end def __init__

    def _handleParameters(self, kwArgs):
        '''
        Handles the keyword parameters for this TestRunner
        Depending on the actual implementation, some (re-)initialization may
        occur, or parameters may be forwarded to a server implementation.

        @param  kwArgs [in] (dict) A dictionary of keyword arguments extracted
                                  from the command line or GUI.
        '''
        self.verbosity = kwArgs.setdefault(KeywordArguments.KEY_VERBOSITY, KeywordArguments.VERBOSITY_COMPLETE)

        root = kwArgs.setdefault(KeywordArguments.KEY_ROOT, KeywordArguments.ROOT_DEFAULT)
        self.root = abspath(root)

        self.debug = eval(kwArgs.setdefault(KeywordArguments.KEY_DEBUG, KeywordArguments.DEBUG_DEFAULT))
        self.includepatterns = kwArgs.setdefault(KeywordArguments.KEY_INCLUDEDPATTERNS, KeywordArguments.INCLUDEDPATTERNS_DEFAULT)
        self.excludepatterns = kwArgs.setdefault(KeywordArguments.KEY_EXCLUDEDPATTERNS, KeywordArguments.EXCLUDEDPATTERNS_DEFAULT)
        self.levels = kwArgs.setdefault(KeywordArguments.KEY_LEVELS, KeywordArguments.LEVELS_DEFAULT)
        self.nolevels = kwArgs.setdefault(KeywordArguments.KEY_NO_LEVELS, KeywordArguments.NO_LEVELS_DEFAULT)
        self.outputdir = kwArgs.setdefault(KeywordArguments.KEY_OUTPUTDIR, KeywordArguments.OUTPUTDIR_DEFAULT)
        self.rootsuite = kwArgs.setdefault(KeywordArguments.KEY_SUITE, KeywordArguments.SUITE_DEFAULT)
    # end def _handleParameters

    def clearCache(self):
        '''
        Clears the descriptor cache, as well as the context cache.
        '''
        self.descriptorCache.clear()
    # end def clearCache

    def getSubSystemDefinitionAndInstantiations(self, additionalSubSystemInstantiations = tuple(),
                                                      updatedKwArgs                     = None):
        '''
        Obtains:
        - The root SubSystemDefinition
        - The root SubSystemInstantiation

        @param  additionalSubSystemInstantiations [in] (list) Additional instantiations
        @param  updatedKwArgs                     [in] (dict) Additional kwArgs, that complete the default ones
                                                             This is mainly used in the GUI, where user-defined
                                                             options may override default ones.
        @return (SubSystemDefinition,list<SubSystemInstantiation>)
        '''
        raise NotImplementedError
    # end def getSubSystemDefinitionAndInstantiations


    def hasTestDescriptor(self, testId):
        '''
        Test whether the TestDescriptor specified by the id is obtainable

        @param  testId    [in] (str)  The id of the test suite to obtain
        @return Whether a TestDescriptor is available for this id.
        '''
        raise NotImplementedError
    # end def hasTestDescriptor

    def getTestDescriptor(self, testId, recursive=True):
        '''
        Obtains the tree describing the tests that will execute in this run.

        @param  testId    [in] (str)  The id of the test suite
        @param  recursive [in] (bool) Whether the full tree or only the designated test is obtained.

        @return A TestDescriptor for the specified test suite.
        '''
        raise NotImplementedError
    # end def getTestDescriptor

    def getTestState(self, testId, product=None, variant=None, target=None):
        '''
        Obtains the state of the given test Id

        @param  testId  [in] (str) The test id to check
        @param  product [in] (str) The product for which the state is to be obtained.
                                     If None, the current product is used
        @param  variant [in] (str) The variant for which the state is to be obtained.
                                     If None, the current variant is used
        @param  target  [in] (str) The target for which the state is to be obtained.
                                     If None, the current target is used

        @return The state of the test id, as an int
        '''
        return self.getTestStates((testId,), product, variant, target)[testId]
    # end def getTestState

    def getTestStates(self, testIds, product=None, variant=None, target=None):
        '''
        Obtains the state of the given test Id tuple

        @param  testIds [in] (tuple)  The test ids to check
        @param  product [in] (str) The product for which the state is to be obtained.
                                     If None, the current product is used
        @param  variant [in] (str) The variant for which the state is to be obtained.
                                     If None, the current variant is used
        @param  target  [in] (str) The target for which the state is to be obtained.
                                     If None, the current target is used

        @return The state of the test id, as a map ids -> state
        '''
        raise NotImplementedError
    # end def getTestStates

    def getTestHistory(self, testId, product=None, variant=None, target=None):
        '''
        Obtains the history of the runs for the given test Id.

        The test history is a sequence of tuples, each tuple containing:
        - state     (string) The test run state result
        - startDate (long) The test run start date
        - endDate   (long) The test run end date
        - message   (string) The test run state message

        @param  testId  [in] (str) The testId for which to retrieve the history
        @param  product [in] (str) The product for which the history is to be obtained.
                                     If None, the current product is used
        @param  variant [in] (str) The variant for which the history is to be obtained.
                                     If None, the current variant is used
        @param  target  [in] (str) The target for which the history is to be obtained.
                                     If None, the current target is used
        @return The test history, as a list<tuple(string, long, long, string)
        '''
        raise NotImplementedError
    # end def getTestHistory

    def getStaticTestCases(self, testId):
        '''
        Obtains a tuple, containing both the list of all implemented TestCases for this test.

        @param  testId  [in] (str) The testId for which to retrieve the TestCases

        @return The TestCases as a list<string>
        '''
        raise NotImplementedError
    # end def getStaticTestCases

    def getTestLogPath(self, testId, product=None, variant=None, target=None):
        '''
        Obtains the local path of the log file of the given testId

        @param  testId [in] (tuple) The test ids to check
        @param  product [in] (str) The product for which the state is to be obtained.
                                     If None, the current product is used
        @param  variant [in] (str) The variant for which the state is to be obtained.
                                     If None, the current variant is used
        @param  target  [in] (str) The target for which the state is to be obtained.
                                     If None, the current target is used

        @return The local path
        '''
        raise NotImplementedError
    # end def getTestLogPath

    def getTestLog(self, testId, product=None, variant=None, target=None):
        '''
        Obtains the log of the given testId as a string

        @param  testId [in] (tuple) The test ids to check
        @param  product [in] (str) The product for which the state is to be obtained.
                                     If None, the current product is used
        @param  variant [in] (str) The variant for which the state is to be obtained.
                                     If None, the current variant is used
        @param  target  [in] (str) The target for which the state is to be obtained.
                                     If None, the current target is used

        @return The test log, as a string
        '''
        raise NotImplementedError
    # end def getTestLog

    def getTestSourceFile(self, testId):
        '''
        Obtains the source file contents of the given testId as a string

        @param  testId [in] (str) The test id for which to obtain the source

        @return The test source file, as a string
        '''
        raise NotImplementedError
    # end def getTestSourceFile

    def getTestSourceLine(self, testId):
        '''
        Obtains the line number of the test in its source file.

        @param  testId [in] (str) The test id for which to obtain the line number

        @return The test source file line number, as an int
        '''
        raise NotImplementedError
    # end def getTestSourceLine

    def setSelectedConfig(self, product, variant, target, mode):
        '''
        Set all the configuration

        @param  product [in] (str) The newly selected product.
        @param  variant [in] (str) The variant to set (as a string, version elements separated by "/"
        @param  target  [in] (str) The newly selected target.
        @param  mode    [in] (str) The newly selected mode.
        '''
        self.setSelectedProduct(product)
        self.setSelectedVariant(variant)
        self.setSelectedTarget(target)
        self.setSelectedMode(mode)
    # end def setSelectedConfig

    def getAvailableModes(self):
        '''
        Obtains the list of available modes.

        @return (tuple(str)) The list of available modes.
        '''
        raise NotImplementedError
    # end def getAvailableModes

    def getSelectedMode(self):
        '''
        Obtains the currently selected mode.

        @return The currently selected mode
        '''
        raise NotImplementedError
    # end def getSelectedMode

    def setSelectedMode(self, mode):
        '''
        Sets the currently selected mode.

        @param  mode [in] (str) The newly selected mode.
        '''
        raise NotImplementedError
    # end def setSelectedMode

    def getAvailableProducts(self):
        '''
        Obtains the list of available products.

        @return (tuple(str)) The list of available products.
        '''
        raise NotImplementedError
    # end def getAvailableProducts

    def getSelectedProduct(self):
        '''
        Obtains the currently selected product.

        @return The currently selected product
        '''
        raise NotImplementedError
    # end def getSelectedProduct

    def setSelectedProduct(self, product):
        '''
        Sets the currently selected product.

        @param  product [in] (str) The newly selected product.
        '''
        raise NotImplementedError
    # end def setSelectedProduct

    def getAvailableVariants(self, product=None):
        '''
        Obtains the list of available variants for the given product.
        If no product is specified, the currently selected product is used.

        @param  product [in] (str) The product for which to lookup variants.
        @return A root, dummy variant containing the child variants for the product.
        '''
        raise NotImplementedError
    # end def getAvailableVariants

    def getSelectedVariant(self):
        '''
        Obtains the currently selected variant
        '''
        raise NotImplementedError
    # end def getSelectedVariant

    def setSelectedVariant(self, variant):
        '''
        Sets the currently selected variant

        @param  variant [in] (str) The variant to set (as a string, version elements separated by "/"
        '''
        raise NotImplementedError
    # end def setSelectedVariant

    def getSelectedTarget(self):
        '''
        Obtains the currently selected target.

        @return The currently selected target.
        '''
        raise NotImplementedError
    # end def getSelectedTarget

    def setSelectedTarget(self, target):
        '''
        Sets the currently selected target

        @param  target [in] (str) The newly selected target.
        '''
        raise NotImplementedError
    # end def setSelectedTarget

    def getAvailableLevels(self, testId, recursive=False):
        '''
        Obtains a list of levels available for the given testId, and its children

        @param  testId    [in] (str)  The test id for which to collect the levels
        @option recursive [in] (bool) Whether to lookup levels in the testId's children.

        @return (list) A list of available test ids
        '''
        raise NotImplementedError
    # end def getAvailableLevels

    def resetTests(self, testIds, listeners=(), updatedKwArgs=None):
        '''
        Resets the state of the given tests, through the provided listeners.

        @param  testIds       [in] (tuple<string>) The fully qualified test id, or list of testIds.
        @param  listeners     [in] (tuple) The tests listeners used to collect test progress.
        @param  updatedKwArgs [in] (dict) Modified KeywordArguments for this operation.
        '''
        raise NotImplementedError
    # end def resetTests

    def run(self, testIds,
                  listeners                         = tuple(),
                  updatedKwArgs                     = None,
                  additionalSubSystemInstantiations = tuple()):
        '''
        Runs a specific test, using the testListeners to collect information.

        @param  testIds                           [in] (tuple<string>) The fully qualified test id, or list of testIds.
        @option listeners                         [in] (tuple) The tests listeners used to collect test progress.
        @option updatedKwArgs                     [in] (dict) Modified KeywordArguments for this run.
        @option additionalSubSystemInstantiations [in] (list) Additional instantiations, to be applied at end of construction.
        '''
        raise NotImplementedError
    # end def run

    def pause(self, forcefully=True):
        '''
        Pauses the test run.

        @param  forcefully [in] (bool) Whether the current test is aborted.
        '''
        raise NotImplementedError
    # end def pause

    def stop(self, forcefully=True):
        '''
        Stops the test run.

        @param  forcefully [in] (bool) Whether to perform a graceful stop or a kill.
        '''
        raise NotImplementedError
    # end def stop

    def resume(self):
        '''
        Resumes a previously stopped test.
        '''
        raise NotImplementedError
    # end def resume
# end class TestManager

class LocalTestManager(TestManager):
    '''
    A local implementation of a test manager.

    This is the first actual implementation of a test manager, that is used to
    pilot a local test run.

    The LocalTestManager is responsible for:
    - Obtaining the root configuration file.
    - From the root configuration file, it rebuilds the (possibly) overridden
      configuration file.
    '''

    ## Zope-compatible implementation definition.
    __implements__ = TestManager
    CONFIGFILE_NAME = "Settings.ini"

    class DescriptorTestListener(TestListener):
        '''
        A TestListener that updates the testDescriptor cache
        '''

        def __init__(self, testManager):
            '''
            Attaches to the target TestManager

            @param  testManager [in] (TestManager) The test manager to notify
            '''
            TestListener.__init__(self, None, None, None, None)

            self._testManager = testManager
        # end def __init__

        def stateChanged(self, testId,
                               state):
            '''
            Notified when a test state changed.

            The first option must be the test id

            @param  testId [in] (str) The test Id that changed.
            @param  state  [in] (str) The new state of the test.

            '''
            testDescriptor = self._testManager.getTestDescriptor(testId, False)
            testDescriptor.setState(state)
        # end def stateChanged

        def resetTest(self, test, context):                                                                             # pylint:disable=W0613
            '''
            @copydoc pyharness.core.TestListener.resetTest
            '''
            self.stateChanged(test.id(), TestDescriptor.STATE_UNKNOWN)
        # end def resetTest

        def startTest(self, test):
            '''
            @copydoc pyharness.core.TestListener.startTest
            '''
            self.stateChanged(test.id(), TestDescriptor.STATE_RUNNING)
        # end def startTest


        def stopTest(self, test):
            '''
            @copydoc pyharness.core.TestListener.stopTest
            '''
            # self.stateChanged(test.id(), TestDescriptor.STATE_UNKNOWN)
            pass
        # end def stopTest

        def addSuccess(self, test, unused=None):
            '''
            @copydoc pyharness.core.TestListener.addSuccess
            '''
            self.stateChanged(test.id(), TestDescriptor.STATE_SUCCESS)
        # end def addSuccess

        def addError(self, test, err):
            '''
            @copydoc pyharness.core.TestListener.addError
            '''
            self.stateChanged(test.id(), TestDescriptor.STATE_ERROR)
        # end def addError

        def addFailure(self, test, err):
            '''
            @copydoc pyharness.core.TestListener.addFailure
            '''
            self.stateChanged(test.id(), TestDescriptor.STATE_FAILURE)
        # end def addFailure
    # end class DescriptorTestListener

    def __init__(self, kwArgs):
        '''
        Constructor.

        @param  kwArgs [in] (dict) The keyword arguments extracted from the
                                  command line/GUI.
        '''
        TestManager.__init__(self, kwArgs)
        self.context = None
        self._testRunner = None
        self.__config = None

        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        configFileRelPath = join(root,
                                 DEFAULT_OUTPUT_DIRECTORY,
                                 self.CONFIGFILE_NAME)
        self.__configFilePath = configFileRelPath

    # end def __init__

    def clearCache(self):
        '''
        @copydoc pyharness.testmanager.TestManager.clearCache
        '''
        TestManager.clearCache(self)
        self.context = None
    # end def clearCache

    def __createFilter(self, kwArgs):                                                                                   #pylint:disable=R0912
        '''
        Creates a filtering function, that will be used to filter tests

        @param  kwArgs [in] (dict) The KeywordArguments that provide enough information
                           to create the filter
        @return The new filtering function, which is a closure on instance
                attributes.
        '''
        includedPatterns = kwArgs[KeywordArguments.KEY_INCLUDEDPATTERNS]
        excludedPatterns = kwArgs[KeywordArguments.KEY_EXCLUDEDPATTERNS]
        levelsPattern = "".join(('(?:^',
                                  '$)|(?:^'.join(kwArgs[KeywordArguments.KEY_LEVELS].split(",")),
                                  '$)'))
        noLevelsPattern = "".join(('(?:^',
                                   '$)|(?:^'.join(kwArgs[KeywordArguments.KEY_NO_LEVELS].split(",")),
                                   '$)'))

        try:
            includedRegex = re.compile(includedPatterns)
        except:
            raise ValueError("The regular expression <%s> is incorrectly formatted." % (includedPatterns,))
        # end try

        try:
            excludedRegex = re.compile(excludedPatterns)
        except:
            raise ValueError("The regular expression <%s> is incorrectly formatted." % (excludedPatterns,))
        # end try

        levelsRegex = re.compile(levelsPattern)

        noLevelsRegex = re.compile(noLevelsPattern)

        def filteringFunction(test, context=None):                                                                      # pylint:disable=R0912
            '''
            Filters the test.

            This filters a single test, and tests whether:
            - It conforms with the excluded regular expression.
              If true, the test is rejected.
            - It conforms with the included regular expression.
              If false, the test is rejected.
            - Its level, if any, is in the list of filtered-out levels.
              If false, the test is rejected.
            - Otherwise, the test succeeds.

            @param  test [in] (TestCase) The test to filter.
            @param  context [in] (Context) The context in which the evaluation is to be done.
            @return True if the test can be run, False otherwise
            '''
            if (isinstance(test, TestCase)):

                testId = test.id()

                # Test against excluded patterns
                if (excludedRegex.match(testId)):
                    return False
                # end if

                # Test against included patterns
                if (not (includedRegex.match(testId))):
                    return False
                # end if

                # Test against the level
                testLevels = tuple()
                if (hasattr(test, "_testMethodName")):
                    testFunction = getattr(test, test._testMethodName)                                                  # pylint:disable=W0212
                    if (isinstance(testFunction, MethodType)):

                        # The function is only filtered out if it defines a level
                        if (level.defines_level(testFunction)):
                            result = False
                            for functionLevel in level.get_levels(testFunction):
                                result = levelsRegex.match(functionLevel)
                                if (result):
                                    if (kwArgs[KeywordArguments.KEY_NO_LEVELS] != KeywordArguments.NO_LEVELS_DEFAULT):
                                        result = noLevelsRegex.match(functionLevel)
                                        if (result):
                                            # Level excluded
                                            return False
                                        else:
                                            result = levelsRegex.match(functionLevel)
                                            break
                                        # end if
                                    else:
                                        break
                                    # end if
                                # end if
                            # end for

                            if (not result):
                                return False
                            # end if

                            testLevels = level.get_levels(testFunction)
                        # end if
                    # end if
                # end if


                # Create a TestAccess object wrapping the current object.
                testId = test.id()
                testAccess = TestAccess(testId,
                                        testLevels,
                                        self.getTestHistory(testId),
                                        self.getStaticTestCases(testId))

                # Use the custom filter defined in the UI
                customFilter = kwArgs[KeywordArguments.KEY_CUSTOM_FILTER]
                if not customFilter(testAccess, context):
                    return False
                # end if
            # end if

            return True
        # end def filteringFunction

        return filteringFunction
    # end def __createFilter

    def __createSorter(self, kwArgs):
        '''
        Creates a sorting function, that will be used to sort tests befor a run

        @param  kwArgs [in] (dict) The KeywordArguments that provide enough information
                           to create the sorter
        @return The new sorting function, which is a closure on instance
                attributes.
        '''

        def sortingFunction(test1, test2):
            '''
            Compares two tests.

            This compares two tests according to the settings in the KeywordArguments.
            (Typically, these are set from the SortingProfile selected in the GUI)

            @param  test1 [in] (TestCase) The first test to compare
            @param  test2 [in] (TestCase) The second test to compare
            @return (int) The result of the comparison
            '''
            result = 0
            if ((isinstance(test1, TestCase))
                and (isinstance(test2, TestCase))):

                testAccesses = []
                for test in (test1, test2):

                    testId = test.id()

                    # Test against the level
                    testLevels = tuple()
                    if (hasattr(test, "_testMethodName")):
                        testFunction = getattr(test, test._testMethodName)                                              # pylint:disable=W0212
                        if ((isinstance(testFunction, MethodType))
                            and (level.defines_level(testFunction))):
                            testLevels = level.get_levels(testFunction)
                        # end if
                    # end if

                    # Create a TestAccess object wrapping the current object.
                    testId = test.id()
                    testAccess = TestAccess(testId,
                                            testLevels,
                                            self.getTestHistory(testId),
                                            self.getStaticTestCases(testId))

                    testAccesses.append(testAccess)
                # end for

                # Use the custom filter defined in the UI
                customSorter = kwArgs[KeywordArguments.KEY_CUSTOM_SORTER]
                result = customSorter(testAccesses[0], testAccesses[1])
            # end if

            return result
        # end def sortingFunction

        return sortingFunction
    # end def __createSorter

    def __createContext(self, updatedKwArgs                     = None,
                              forceCreation                     = False,
                              additionalSubSystemInstantiations = tuple()):
        '''
        Creates a local context for the current test run.

        The context is cached, and will only be re-built if the cache flag
        is cleared.

        @option updatedKwArgs                     [in] (dict)     Additional kwArgs, that complete the default ones
                                                                 This is mainly used in the GUI, where user-defined
                                                                 options may override default ones.
        @option additionalSubSystemInstantiations [in] (list) Additional instantiations, to be applied at end of construction.
        @option forceCreation                     [in] (bool)  Do not reuse any pre-existing context.

        @return The cached context (if any), or a new context, which is the cached.
        '''
        if (    (self.context is not None)
            and (not forceCreation)
            and (updatedKwArgs is None)):
            return self.context
        # end if

        # If additional kwArgs are provided, create a temporary value
        # Otherwise, re-use the default instance.
        kwArgs = self._kwArgs.copy()
        if (updatedKwArgs is not None):
            kwArgs.update(updatedKwArgs)
        # end if

        root = abspath(self.root)
        # If the root path can be accessed, create a new context, that
        # works on this root path (extracting versions, etc...)
        if (access(root, R_OK)):
            rootPaths = [root]
            rootPaths.extend(kwArgs[KeywordArguments.KEY_EXTENDEDROOTS])
            contextLoader = ContextLoader()
            config = contextLoader.loadConfig(rootPaths,
                                              kwArgs[KeywordArguments.KEY_OVERRIDES])
            context = contextLoader.createContext(config,
                                                  manualUi                          = kwArgs[KeywordArguments.KEY_MANUALUI],
                                                  additionalSubSystemInstantiations = additionalSubSystemInstantiations)
        else:
            raise ValueError("Unable to accesspath <%s>" % (root,))
        # end if

        # Initialize the filter for this context.
        # The filter will decide whether a test can run or not.
        context.filter = self.__createFilter(kwArgs)

        # Initialize the sorter for this context.
        # The sorter will decide the order in which the tests will run
        context.sorter = self.__createSorter(kwArgs)

        # Get thread count to give access of this information to tests.
        # We assume that this information is an integer and no accessor has been
        # created to avoid miss modification of thread count used by test runner
        # This attribute shall not be updated elsewere.
        # Look at help to know where to update test runner thread count.
        context._threads = int(kwArgs[KeywordArguments.KEY_THREADS])            # pylint:disable=W0212

        # Only cache the default context.
        if (updatedKwArgs is None):
            self.context = context
        # end if

        return context
    # end def __createContext

    def getSubSystemDefinitionAndInstantiations(self, additionalSubSystemInstantiations = tuple(),
                                                      updatedKwArgs                     = None):
        '''
        @copydoc pyharness.testmanager.TestManager.getSubSystemDefinitionAndInstantiations
        '''
        # If additional kwArgs are provided, create a temporary value
        # Otherwise, re-use the default instance.
        kwArgs = self._kwArgs.copy()
        if (updatedKwArgs is not None):
            kwArgs.update(updatedKwArgs)
        # end if

        root = abspath(self.root)

        # If the root path can be accessed, create a new context, that
        # works on this root path (extracting versions, etc...)
        if (access(root, R_OK)):
            rootPaths = [root]
            rootPaths.extend(kwArgs[KeywordArguments.KEY_EXTENDEDROOTS])
            config = ContextLoader.loadConfig(rootPaths,
                                              kwArgs[KeywordArguments.KEY_OVERRIDES])

            product = self.getSelectedProduct()
            variant = self.getSelectedVariant()

            relativePath = normpath(join(product, variant))
            from os                     import sep
            pathElements = relativePath.split(sep)
            pathElements = [pathElement.strip() for pathElement in pathElements]
            pathElements = [pathElement for pathElement in pathElements if len(pathElement)]

            # Load the global subsystem, containing all the features, from disk
            subSystemDefinitionPaths = config.get(ContextLoader.SECTION_CONFIG,
                                                  ContextLoader.OPTION_ROOTPATHS)
            subSystemDefinitionPaths = [abspath(p) for p in subSystemDefinitionPaths]
            subSystemDefinitionPaths = [join(p, 'TESTSUITES') if exists(join(p, 'TESTSUITES')) else p for p in subSystemDefinitionPaths]

            from pysetup                import TESTS_PATH                                                                #@UnresolvedImport #pylint:disable=E0611
            leafInstantiationPaths  = [join(TESTS_PATH, DEFAULT_INPUT_DIRECTORY, *pathElements)]
            subSystemDefinition     = ContextLoader().subSystemBuilder.loadRootSubSystemDefinition(subSystemDefinitionPaths)
            subSystemInstantiations = ContextLoader().subSystemBuilder.loadSubSystemInstantiations(leafInstantiationPaths)

            return subSystemDefinition, subSystemInstantiations
        else:
            raise ValueError("Unable to accesspath <%s>" % (root,))
        # end if
    # end def getSubSystemDefinitionAndInstantiations

    def hasTestDescriptor(self, testId):
        '''
        @copydoc pyharness.testmanager.TestManager.hasTestDescriptor
        '''
        return testId in self.descriptorCache
    # end def hasTestDescriptor

    def getTestDescriptor(self, testId, recursive=True):                                                                # pylint:disable=R0912
        '''
        @copydoc pyharness.testmanager.TestManager.getTestDescriptor

        This implementation collects the test tree by locally running the tests,
        with the collectOnly flag set in the context.
        '''
        result = self.descriptorCache.get(testId, None)
        if (result is not None):
            return result
        # end if

        # First step: import the root test suite
        testLoader = TestLoader()
        suite = testLoader.loadTestsFromNames((testId,))

        # Create a local context, to collect the tests without actually
        # running them.
        context = self.__createContext()
        localContext = CollectContext(context)
        localListener = CollectListener()

        # Run the test suite. This will NOT actually run the
        # setUp/tearDown/test_XYZ on TestCases instances, but will only
        # collect the test call hierarchy
        testRunner = MonoThreadTestRunner([localListener, ])
        testRunner.run(suite, localContext)

        # Keep a cache of the test descriptors, only for recursive calls
        testDescriptor = localListener.descriptorStack[0]
        if (recursive):

            # Update the test states, using the default kwArgs
            root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
            outputRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)
            product = None
            variant = None

            if (product is None):
                product = self.getSelectedProduct()
            # end if

            if (variant is None):
                variant = self.getSelectedVariant()
            # end if

            # Collect the test state from the journal file.
            # This has the drawback of REQUIRING the presence of the journal file.
            pathToJournal = normpath(join(outputRoot, product, variant, "Journal.jrl"))
            if (access(pathToJournal, F_OK)):
                journal = JrlFile.create(pathToJournal)
            else:
                journal = None
            # end if

            def _addToCache(descriptor):
                '''
                Local closure, that adds the contents of the descriptor tree to the cache

                @param  descriptor [in] (TestDescriptor) The TestDescriptor to add to the cache.
                '''
                testId = descriptor.testId

                # Retrieve the state from the journal.
                testState = None
                jrlEntry = (journal is not None) and journal.getLastEntry(testId) or None
                if (jrlEntry is not None):
                    # Convert the entry to the TestDescriptor state
                    jrlEntryState = jrlEntry.getTestState()
                    testState = self.__jrlStateToDescriptorState(jrlEntryState)
                # end if

                if (testState is not None):
                    descriptor.setState(testState)
                # end if

                # Cache the descriptor
                self.descriptorCache[testId] = descriptor

                # Cache the descriptor's children
                for child in descriptor.getChildren():
                    _addToCache(child)
                # end for
            # end def _addToCache
            # Cache descriptors, starting with the root TestDescriptor.
            # This will speed up later searches.
            _addToCache(testDescriptor)

            def _updateState(descriptor):
                '''
                Update the state of the descriptor, depending on the max of
                its children.

                The state is that of the most important state of the
                TestDescriptor's children, i.e.:
                - If at least one of the descendants of the TestDescriptor is
                  in error, then the descriptor is in error.
                - Otherwise, if at least one of the descendants of the
                  TestDescriptor is in failure, then the descriptor is in failure.
                - Etc...

                This is a recursive function.

                @param  descriptor [in] (TestDescriptor) The descriptor to update
                '''
                children = descriptor.getChildren()
                if (len(children) > 0):
                    for childDescriptor in children:
                        _updateState(childDescriptor)
                    # end for

                    childStates = [child.getState() for child in descriptor.getChildren()]
                    childStates.append(TestDescriptor.STATE_UNKNOWN)
                    newState = max(childStates)

                    descriptor.setState(newState)
                # end if
            # end def _updateState

            # Update the state of the root descriptor, recursively
            _updateState(testDescriptor)
        # end if

        return testDescriptor
    # end def getTestDescriptor

    def resetTests(self, testIds, listeners=(), updatedKwArgs=None):
        '''
        @copydoc pyharness.testmanager.TestManager.resetTests
        '''
        # Append a DescriptorTestListener that will keep track of the
        # state of the tests

        innerListeners = []
        innerListeners.extend(listeners)
        innerListeners.append(self.DescriptorTestListener(self))

        # Initialize the tree, recursively.
        # Otherwise, each notification will cause a getTestDescriptor
        # to explore the entire tree
        if (isinstance(testIds, str)):
            testIds = (testIds,)
        # end if

        for testId in testIds:
            self.getTestDescriptor(testId)
        # end for

        kwArgs = self._kwArgs.copy()
        if (updatedKwArgs is not None):
            kwArgs.update(updatedKwArgs)
        # end if

        # First step: import the root test suite
        testLoader = TestLoader()
        suite = testLoader.loadTestsFromNames(testIds)
        context = self.__createContext(updatedKwArgs)

        for listener in innerListeners:
            if hasattr(suite, '_tests'):
                for test in suite._tests:                                                                               # pylint:disable=W0212
                    listener.resetTest(test, context)
                # end for
            else:
                listener.resetTest(suite, context)
            # end if
        # end for

        context.close()
    # end def resetTests

    def run(self, testIds,
                  listeners                         = tuple(),
                  updatedKwArgs                     = None,
                  additionalSubSystemInstantiations = tuple()):
        '''
        @copydoc pyharness.testmanager.TestManager.run
        '''

        # Append a DescriptorTestListener that will keep track of the
        # state of the tests

        innerListeners = []
        innerListeners.extend(listeners)
        innerListeners.append(LocalTestManager.DescriptorTestListener(self))

        # Initialize the tree, recursively.
        # Otherwise, each notification will cause a getTestDescriptor
        # to explore the entire tree
        if (isinstance(testIds, str)):
            testIds = (testIds,)
        # end if

        for testId in testIds:
            self.getTestDescriptor(testId)
        # end for

        kwArgs = self._kwArgs.copy()
        if (updatedKwArgs is not None):
            kwArgs.update(updatedKwArgs)
        # end if

        nThreads = int(kwArgs[KeywordArguments.KEY_THREADS])


        # First step: import the root test suite
        testLoader = TestLoader()
        suite = testLoader.loadTestsFromNames(testIds)
        context = self.__createContext(updatedKwArgs,
                                       additionalSubSystemInstantiations  = additionalSubSystemInstantiations)

        # This will only work if no other test run has been launched
        self._testRunner = TestRunner(innerListeners, nThreads)

        self._testRunner.run(suite, context)
        context.close()

        self._testRunner = None
    # end def run

    def pause(self, forcefully=False):
        '''
        @copydoc pyharness.testmanager.TestManager.pause
        '''
        if self._testRunner is not None:
            self._testRunner.pause(forcefully)
        # end if
    # end def pause

    def stop(self, forcefully=True):                                                                                    # pylint:disable=W0613
        '''
        @copydoc pyharness.testmanager.TestManager.stop

        Note: the @c forcefully parameter is not available as Python does not
              support killing threads. The tests will stop as soon as possible.
        '''
        if self._testRunner is not None:
            self._testRunner.stop()
        # end if
    # end def stop

    def resume(self):
        '''
        @copydoc pyharness.testmanager.TestManager.resume
        '''
        if self._testRunner is not None:
            self._testRunner.resume()
        # end if
    # end def resume

    def __collectVariants(self, parent, parentDir, recursive=True):
        '''
        Collects variants from a directory.

        @param  parent    [in] (str)  The parent VersionDescriptor
        @param  parentDir [in] (str)  The parent directory.
        @param  recursive [in] (bool) Whether the search is recursive
        '''
        childDirs = listdir(parentDir)
        for childDir in childDirs:
            fullChildDir = join(parentDir, childDir)
            if (isdir(fullChildDir)):
                # Build the variant ini file path
                childIniPath = join(fullChildDir, childDir + ".settings.ini")
                if (access(childIniPath, R_OK)):
                    child = VersionDescriptor(childDir, True)
                    parent.children.append(child)
                    if (recursive):
                        self.__collectVariants(child, fullChildDir)
                    # end if
                else:
                    childXmlPath = join(fullChildDir, childDir + ".xml")
                    if (access(childXmlPath, R_OK)):
                        child = VersionDescriptor(childDir, True)
                        parent.children.append(child)
                        if (recursive):
                            self.__collectVariants(child, fullChildDir)
                        # end if
                    # end if
                # end if
            # end if
        # end for
    # end def __collectVariants

    def __collectProducts(self, parent, parentDir, recursive=False):
        '''
        Collects products from a directory.

        @param  parent    [in] (str)  The parent VersionDescriptor
        @param  parentDir [in] (str)  The parent directory.
        @param  recursive [in] (bool) Whether the search is recursive
        '''
        childDirs = listdir(parentDir)
        for childDir in childDirs:
            fullChildDir = join(parentDir, childDir)
            if (isdir(fullChildDir)):
                # Build the variant ini file path
                if (   (access(join(fullChildDir, "main.settings.ini"), R_OK))
                    or (access(join(fullChildDir, childDir + ".main.xml"), R_OK))):
                    child = VersionDescriptor(childDir, True)
                    parent.children.append(child)
                    if (recursive):
                        self.__collectVariants(child, fullChildDir)
                    # end if
                # end if
            # end if
        # end for
    # end def __collectProducts

    def __getConfigValue(self, section, option):
        '''
        Obtains a property from the settings.

        @param  section [in] (str) The section for which to obtain the value
        @param  option  [in] (str) The option for which to obtain the value
        @return The value for the specified section/option
        '''

        # If the value is overridden, do not use the config file
        overrides = self._kwArgs[KeywordArguments.KEY_OVERRIDES]
        startKey = "%s.%s=" % (section, option)
        for override in overrides:
            if override.startswith(startKey):
                return override[len(startKey):]
            # end if
        # end for

        if (self.__config is None):
            configFile = CachingConfigParser(ConfigParser())

            if (access(self.__configFilePath, R_OK)):
                configFile.read([self.__configFilePath])
                self.__config = configFile
            # end if
        # end if

        result = None
        if (self.__config is not None):
            result = self.__config.get(section,
                                    option)
        # end if

        return result
    # end def __getConfigValue

    def __setConfigValue(self, section,
                               option,
                               value):
        '''
        Sets a property in the config file.

        @param  section [in] (str)     The section for which to set the value
        @param  option  [in] (str)     The option for which to set the value
        @param  value   [in] (int,string) The value for the specified section/option
        '''
        if (self.__config is None):
            configFile = CachingConfigParser(ConfigParser())

            configFile.read([self.__configFilePath])
        # end if

        self.__config.set(section,
                          option,
                          value)
        self.__config.write(self.__configFilePath)
    # end def __setConfigValue

    @staticmethod
    def __jrlStateToDescriptorState(jrlEntryState):
        '''
        Converts a state obtained from a JrlEntry to a Descriptor constant

        @param  jrlEntryState [in] (str) State, as obtained from a JrlFile.JrlEntry
        @return The TestDescriptor state
        '''
        if jrlEntryState == JrlFile.JrlEntry.STATE_SUCCESS:
            testState = TestDescriptor.STATE_SUCCESS
        elif jrlEntryState == JrlFile.JrlEntry.STATE_FAILURE:
            testState = TestDescriptor.STATE_FAILURE
        elif jrlEntryState == JrlFile.JrlEntry.STATE_ERROR:
            testState = TestDescriptor.STATE_ERROR
        else:
            testState = TestDescriptor.STATE_UNKNOWN
        # end if

        return testState
    # end def __jrlStateToDescriptorState

    def getAvailableModes(self):
        '''
        @copydoc pyharness.testmanager.TestManager.getAvailableModes
        '''
        return ("RELEASE", "WORKING")
    # end def getAvailableModes

    def getSelectedMode(self):
        '''
        @copydoc pyharness.testmanager.TestManager.getSelectedMode
        '''
        return self.__getConfigValue(ContextLoader.SECTION_MODE,
                                     ContextLoader.OPTION_VALUE)
    # end def getSelectedMode

    def setSelectedMode(self, mode):
        '''
        @copydoc pyharness.testmanager.TestManager.setSelectedMode
        '''
        self.__setConfigValue(ContextLoader.SECTION_MODE,
                              ContextLoader.OPTION_VALUE,
                              mode)
    # end def setSelectedMode

    def getAvailableProducts(self):
        '''
        @copydoc pyharness.testmanager.TestManager.getAvailableProducts
        '''
        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        configRoot = join(root, DEFAULT_INPUT_DIRECTORY)

        root = VersionDescriptor(None, False)
        self.__collectProducts(root, configRoot, False)

        return [version.name for version in root.children]
    # end def getAvailableProducts

    def getSelectedProduct(self):
        '''
        @copydoc pyharness.testmanager.TestManager.getSelectedProduct

        This reads the currently selected product from the Settings.ini file
        '''
        return self.__getConfigValue(ContextLoader.SECTION_PRODUCT,
                                     ContextLoader.OPTION_VALUE)
    # end def getSelectedProduct

    def setSelectedProduct(self, product):
        '''
        @copydoc pyharness.testmanager.TestManager.setSelectedProduct

        This reads the currently selected variant from the Settings.ini file
        '''
        self.__setConfigValue(ContextLoader.SECTION_PRODUCT,
                              ContextLoader.OPTION_VALUE,
                              product)
    # end def setSelectedProduct

    def getAvailableVariants(self, product=None):
        '''
        @copydoc pyharness.testmanager.TestManager.getAvailableProducts

        @param  product [in] (str) The product to obtain the variants with
        '''

        if (product is None):
            product = self.getSelectedProduct()
        # end if

        # The root of the variant tree. This is placeholder will generally
        # stand to be the product.
        rootVariant = VersionDescriptor(None, False)
        if (product is None):
            return rootVariant
        # end if

        # The root path of the variants.
        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        variantRoot = join(root, DEFAULT_INPUT_DIRECTORY, product)

        # Collect the root variants for this product.
        # These are infered from the VALIDATION definitions, and NOT the
        # RELEASE directory.
        # i.e., a variant that is defined in the PROJECT project source will not
        # appear unless is has been defined as a VALIDATION variant.
        self.__collectVariants(rootVariant, variantRoot)

        return rootVariant
    # end def getAvailableVariants

    def getSelectedVariant(self):
        '''
        @copydoc pyharness.testmanager.TestManager.getSelectedVariant

        This reads the currently selected variant from the Settings.ini file
        '''
        return self.__getConfigValue(ContextLoader.SECTION_VARIANT,
                                     ContextLoader.OPTION_VALUE)
    # end def getSelectedVariant

    def setSelectedVariant(self, variant):
        '''
        @copydoc pyharness.testmanager.TestManager.setSelectedVariant

        This writes the currently selected variant to the Settings.ini file
        '''
        self.__setConfigValue(ContextLoader.SECTION_VARIANT,
                              ContextLoader.OPTION_VALUE,
                              variant)
    # end def setSelectedVariant

    def getSelectedTarget(self):
        '''
        @copydoc pyharness.testmanager.TestManager.getSelectedTarget
        '''
        return self.__getConfigValue(ContextLoader.SECTION_TARGET,
                                     ContextLoader.OPTION_VALUE)
    # end def getSelectedTarget

    def setSelectedTarget(self, target):
        '''
        @copydoc pyharness.testmanager.TestManager.setSelectedTarget

        This writes the currently selected target to the Settings.ini file
        '''
        self.__setConfigValue(ContextLoader.SECTION_TARGET,
                              ContextLoader.OPTION_VALUE,
                              target)
    # end def setSelectedTarget

    def getAvailableLevels(self, testId, recursive=False):
        '''
        @copydoc pyharness.testmanager.TestManager.getAvailableLevels
        '''
        result = set()
        testDescriptor = self.getTestDescriptor(testId, recursive)

        def collectFromTestDescriptor(innerTestDescriptor):
            '''
            Collects the levels from the test descriptor

            @param  innerTestDescriptor [in] (TestDescriptor) The test descriptor to collect the levels from.
            '''
            if (innerTestDescriptor is not None):
                innerTestId = innerTestDescriptor.testId

                # Attempt to import the specified test id.
                obj = importFqn(innerTestId, False)

                if (obj is not None):
                    # The target has been found, lookup the list of levels from
                    # the repository
                    result.update(level.get_levels(obj))
                # end if

                if (recursive):
                    for childDescriptor in innerTestDescriptor.getChildren():
                        collectFromTestDescriptor(childDescriptor)
                    # end for
                # end if
            # end if
        # end def collectFromTestDescriptor

        collectFromTestDescriptor(testDescriptor)

        return list(result)
    # end def getAvailableLevels

    def getTestStates(self, testIds, product=None, variant=None, target=None):
        '''
        @copydoc pyharness.testmanager.TestManager.getTestStates
        '''

        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        versionRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)

        if (product is None):
            product = self.getSelectedProduct()
        # end if

        if (variant is None):
            variant = self.getSelectedVariant()
        # end if

        if (target is None):
            target = self.getSelectedTarget()
        # end if

        pathToJournal = join(versionRoot, product, variant, target, "Journal.jrl")
        if (access(pathToJournal, F_OK)):
            journal = JrlFile.create(pathToJournal)
        else:
            journal = None
        # end if

        result = {}
        for testId in testIds:
            jrlEntry = (journal is not None) and journal.getLastEntry(testId) or None
            testState = TestDescriptor.STATE_UNKNOWN
            if (jrlEntry is not None):
                testState = self.__jrlStateToDescriptorState(jrlEntry.getTestState())
            # end if
            result[testId] = (testState,)
        # end for

        return result
    # end def getTestStates

    def getTestHistory(self, testId, product=None, variant=None, target=None):
        '''
        @copydoc pyharness.testmanager.TestManager.getTestHistory
        '''

        jrlStateToDescriptorState = self.__jrlStateToDescriptorState
        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        versionRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)

        _self = self

        class TestHistory(object):                                                                                      # pylint:disable=R0924
            '''
            Lazy evaluator for test history.

            This emulates a cached sequence, which is evaluated on first access.
            '''
            def __init__(self):
                '''
                Constructor
                '''
                self._cache = None
            # end def __init__

            @synchronized
            def _getCache(self):
                '''
                Obtains the cached history

                @return The cached history
                '''
                if (self._cache is None):
                    product = _self.getSelectedProduct()
                    variant = _self.getSelectedVariant()
                    target = _self.getSelectedTarget()

                    pathToJournal = join(versionRoot, product, variant, target, "Journal.jrl")
                    pathToJournal = normpath(pathToJournal)
                    if (access(pathToJournal, F_OK)):
                        journal = JrlFile.create(pathToJournal)
                    else:
                        journal = None
                    # end if

                    jrlEntries = (journal is not None) and journal.getAllEntries(testId) or []

                    self._cache = [(jrlStateToDescriptorState(jrlEntry.getTestState()),
                                    jrlEntry.getTestStartDate(),
                                    jrlEntry.getTestStopDate(),
                                    jrlEntry.getTestMessage()) for jrlEntry in jrlEntries]
                # end if

                return self._cache
            # end def _getCache

            def __len__(self):
                '''
                Obtains the length

                @return The length
                '''
                return len(self._getCache())
            # end def __len__

            def __getitem__(self, index):
                '''
                Obtains the item at the given position

                @param  index [in] (int) The item index

                @return The item
                '''
                return self._getCache()[index]
            # end def __getitem__
        # end class TestHistory

        return TestHistory()
    # end def getTestHistory

    def getTestLog(self, testId, product=None, variant=None, target=None):
        '''
        @copydoc pyharness.testmanager.TestManager.getTestLog
        '''
        pathToTest = self.getTestLogPath (testId, product, variant, target)

        try:
            with open(pathToTest, 'r') as testFile:
                result = testFile.read()
            # end with
        except IOError:
            result = ""
        # end try

        return result
    # end def getTestLog

    def getTestLogPath (self, testId, product=None, variant=None, target=None):
        '''
        @copydoc pyharness.testmanager.TestManager.getTestLogPath
        '''

        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        versionRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)

        product = product if product is not None else self.getSelectedProduct()
        variant = variant if variant is not None else self.getSelectedVariant()
        target  = target  if target  is not None else self.getSelectedTarget()

        testLogName = "%s.log" % testId
        pathToTest = normpath(join(versionRoot, product, variant, target, "log", testLogName))

        if (access(pathToTest, F_OK)):
            result = pathToTest
        else:
            result = ""
        # end if

        return result
    # end def getTestLogPath

    def getStaticTestCases(self, testId):
        '''
        @copydoc pyharness.testmanager.TestManager.getStaticTestCases
        '''
        testIds = []
        if (testId is None):
            testIds = list(self.descriptorCache.keys())
        else:
            testIds = [testId]
        # end if

        results = set()
        for testId in testIds:
            innerResults = set()
            try:
                testMethod = importFqn(testId)
                if (    (testMethod is not None)
                    and (isinstance(testMethod, MethodType))):
                    func = testMethod.__func__
                    glob = func.__globals__

                    # Look for strings whose value are equal to their name
                    for key, value in glob.items():
                        if (isinstance(value, str)):
                            if (key == value):
                                innerResults.add(value)
                            # end if
                        # end if
                    # end for
                # end if
            except AttributeError:
                innerResults.clear()
            except ImportError:
                innerResults.clear()
            # end try
            results |= innerResults
        # end for

        return list(sorted(results))
    # end def getStaticTestCases

    def getTestSourceFile(self, testId):
        '''
        @copydoc pyharness.testmanager.TestManager.getTestSourceFile
        '''

        obj = importFqn(testId)

        # Handle decorators and proxies
        while (hasattr(obj, "next")) and (obj is not obj.__next__):
            obj = obj.__next__
        # end while

        result = ""
        # If it is a function, its location should be available in obj...
        # contents = [(name, getattr(obj, name)) for name in dir(obj)]
        if (isinstance(obj, type)):
            func = obj.__func__
            code = func.__code__

            with open(code.co_filename) as inputFile:
                result = inputFile.read()
            # end with
        # end if

        return result
    # end def getTestSourceFile

    def getTestSourceLine(self, testId):
        '''
        @copydoc pyharness.testmanager.TestManager.getTestSourceLine
        '''
        obj = importFqn(testId)

        # Handle decorators and proxies
        while (hasattr(obj, "next")) and (obj is not obj.__next__):
            obj = obj.__next__
        # end while

        result = 1
        # If it is a function, its location should be available in obj...
        # contents = [(name, getattr(obj, name)) for name in dir(obj)]
        if (isinstance(obj, FunctionType)):
            code = obj.__code__

            result = code.co_firstlineno - 1
        # end if

        return result
    # end def getTestSourceLine
# end class LocalTestManager

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
