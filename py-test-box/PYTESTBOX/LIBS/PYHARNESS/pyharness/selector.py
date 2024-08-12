#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.selector
:brief:  Test script "features" decorator implementation module
:author: Christophe Roquebert <croquebert@logitech.com>
:date:   2018/06/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from re import compile
from threading import RLock
from types import MethodType
from warnings import warn

from pylibrary.tools.checks import checkCallable
from pylibrary.tools.checks import checkType
from pylibrary.tools.threadutils import synchronized


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
SYNCHRONIZATION_LOCK = RLock()


class Features(object):
    """
    Function decorator, that associates a feature with a function definition.

    This should be used in tests, on test methods, to declare the test feature.

    Example:
    @code
    from pyharness.device                   import PyHarnessCase
    from pyharness.selector                 import features

    class MyTest(PyHarnessCase):
        @features("requirement")
        def test_Example(self):
            self.fail("Test not implemented")
        # end def test_Example
    # end class MyTest
    @endcode
    """
    _INSTANCE = None

    __EMPTY_SET = frozenset()

    _decoratorToFeatures = {}
    _decoratorToId = {}
    _idToFeatures = {}
    _featureHelp = {}

    @classmethod
    @synchronized(SYNCHRONIZATION_LOCK)
    def __new__(cls, *args, **kwargs):
        """
        :param args: Potential child argument - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential child keyword argument - OPTIONAL
        :type kwargs: ``object``

        :return:  Same Features instance for every creation
        :rtype: ``Features``
        """
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Features, cls).__new__(*args, **kwargs)
        # end if
        return cls._INSTANCE
    # end def __new__

    def __call__(self, *featureValues):
        """
        feature decorator call function

        :param featureValues: The requirements the following function will be associated with (the first value should
                              be the feature, then other values can be the parameters of the feature)
        :type featureValues: ``[str,str]``

        :return:  An inner decorator that associates the function with the requirements.
        :rtype: ``MethodType``

        NB: This function will be called when using a feature decorator.
        """
        # Check that feature is defined
        if not isFeatureReversed(featureValues[0]):
            base_feature = featureValues[0][:]
        else:
            base_feature = featureValues[0][len(REVERSED_MARK):]
        # end if

        if base_feature not in self._decoratorToFeatures:
            warn(f"Unspecified feature: {base_feature}. The test will still be unreachable until feature specification "
                 "by feature.registerFeature method.", category=SyntaxWarning, stacklevel=1)
        # end if

        def featureAssigner(f):
            """
            Inner decorator, that performs the actual association.

            :param f:The function to decorate with the feature
            :type f: ``MethodType``

            :return: The decorated function (Same as the input)
            :rtype: ``MethodType``
            """
            f_id = id(f)
            SYNCHRONIZATION_LOCK.acquire()
            try:
                ids = self._decoratorToId.get(featureValues[0], None)
                if ids is None:
                    ids = set()
                    self._decoratorToId[featureValues[0]] = ids
                # end if
                ids.add(f_id)

                _feature = self._idToFeatures.get(f_id, None)
                if _feature is None:
                    _feature = set()
                    self._idToFeatures[f_id] = _feature
                # end if
                _feature.add((featureValues[0], featureValues[1:]))
            finally:
                SYNCHRONIZATION_LOCK.release()
            # end try

            return f
        # end def featureAssigner
        return featureAssigner
    # end def __call__

    def registerFeature(self, feature, function, featureHelp=None):
        """
        Register a feature name and the function to resolve it

        :param feature: Feature name
        :type feature: ``str``
        :param function: Function to resolve the feature
        :type function: ``callable``
        :param featureHelp: Help of the feature
        :type featureHelp: ``str``

        NB: The function shall have only one parameter, which is the pyharness context to have access to features
        """
        # Check parameters type
        checkType(feature, str)
        checkCallable(function)
        if featureHelp is not None:
            checkType(featureHelp, str)
        # end if

        if feature in self._decoratorToFeatures:
            raise ValueError('Duplicate feature: %s, already registered' % feature)
        # end if

        # Register process
        self._decoratorToFeatures[feature] = function
        if featureHelp is not None:
            self._featureHelp[feature] = featureHelp
        # end if
    # end def registerFeature

    @staticmethod
    def __realFunction(f):
        """
        Extract the inner FunctionType object from a MethodType object.

        :param f: A MethodType object, from which the FunctionType object is extracted
        :type f: ``MethodType``

        :return:  The FunctionType object associated with the parameter
        :rtype: ``FunctionType``
        """
        func = f
        while isinstance(func, MethodType):
            func = func.__func__
        # end while
        return func
    # end def __realFunction

    @staticmethod
    def __getFid(f):
        """
        Get id of inner function

        :param f: A MethodType object, from which the FunctionType object is extracted
        :type f: ``MethodType``

        :return:  ID of the function
        :rtype: ``int``
        """
        return id(Features.__realFunction(f))
    # end def __getFid

    @synchronized(SYNCHRONIZATION_LOCK)
    def getFeatures(self, f=None):
        """
        Obtain the list of feature for which a function is registered.

        :param f: The function to check, None to obtain _all_ feature
        :type f: ``FunctionType``

        :return:  The list of registered feature
        :rtype: ``list``
        """
        if f is not None:
            f_id = Features.__getFid(f)
            result = self._idToFeatures.get(f_id, self.__EMPTY_SET)
        else:
            result = list(self._decoratorToId.keys())
        # end if

        return result
    # end def getFeatures

    def hasFeatures(self, f, featureList):
        """
        Test whether a function is associated with a set of feature

        :param f: The MethodType object to test
        :type f: ``MethodType``
        :param featureList: Single or list of feature to test against
        :type featureList: ``str|tuple``

        :return:  True if the function has been registered with one of the feature with the feature decorator
        :rtype: ``bool``
        """
        f_id = Features.__getFid(f)

        result = False
        if isinstance(featureList, str):
            featureList = (featureList, )
        # end if
        checkType(featureList, (list, tuple))
        for currentFeatures in featureList:
            feature_set = self._decoratorToId.setdefault(currentFeatures, set())
            if f_id in feature_set:
                result = True
                break
            # end if
        # end for

        return result
    # end def hasFeatures

    def isDecorated(self, f):
        """
        Test whether a function has defined a feature.

        :param f: The function to test
        :type f: ``FunctionType``

        :return:  True if the function has defined a feature with the feature decorator
        :rtype: ``bool``
        """
        f_id = Features.__getFid(f)

        result = False
        for fIds in iter(list(self._decoratorToId.values())):
            if f_id in fIds:
                result = True
                break
            # end if
        # end for

        return result
    # end def isDecorated

    def setHelp(self, feature, help):
        """
        Set the help string associated with a feature

        :param feature: The feature value
        :type feature: ``str``
        :param help: The help string
        :type help: ``str``
        """
        self._featureHelp[feature] = help
    # end def setHelp

    def getHelp(self, feature=None):
        """
        Obtain the help string associated with the feature, or None if no help is defined.

        :param feature: The feature value
        :type feature: ``str``

        :return:  The associated help string, or None if not defined.
        :rtype: ``str``
        """
        if feature is None:
            result = self._featureHelp
        else:
            result = self._featureHelp.get(feature, None)
        # end if

        return result
    # end def getHelp

    def class_decorator(self, *feature, inheritance=None):
        """
        Apply decorator to all tests in a class

        :param feature: Feature name and parameters
        :type feature: ``tuple``
        :param inheritance: Inheriting class, if any
        :type inheritance: ``object|None``
        """

        def inner(class_test_case):
            for elt in dir(class_test_case):
                if elt.startswith("test_") and callable(getattr(class_test_case, elt)):
                    decorator = (feature[0], feature[1:])
                    if inheritance is not None:
                        # Function has to be reassigned to have different ids, else decorator would be applied to all
                        # other classes. But decorators from inherited class should be kept.
                        setattr(class_test_case, elt, lambda this, test=elt: getattr(inheritance, test)(this))

                        for inherited_feature in features.getFeatures(f=getattr(inheritance, elt)):
                            features(inherited_feature[0], *inherited_feature[1])(getattr(class_test_case, elt))
                        # end for
                        # Set here to prevent circular import
                        from pyharness.extensions import level
                        for inherited_level in level.get_levels(f=getattr(inheritance, elt)):
                            level(inherited_level)(getattr(class_test_case, elt))
                        # end for
                        for inherited_service in services.getFeatures(f=getattr(inheritance, elt)):
                            services(inherited_service[0], *inherited_service[1])(getattr(class_test_case, elt))
                        # end for
                        for inherited_bugtracker in bugtracker.getFeatures(f=getattr(inheritance, elt)):
                            bugtracker(inherited_bugtracker)(getattr(class_test_case, elt))
                        # end for
                    # end if
                    self(decorator[0], *decorator[1])(getattr(class_test_case, elt))
                # end if
            # end for
            return class_test_case
        # end def inner
        return inner
    # end def class_decorator
# end class Features


class Services(Features):
    """
    Function decorator, that associates a feature with a function definition.

    This should be used in tests, on test methods, to declare the test feature.
    """
    _INSTANCE = None

    __EMPTY_SET = frozenset()

    _decoratorToFeatures = {}
    _decoratorToId = {}
    _idToFeatures = {}
    _featureHelp = {}

    _false_decorators = []

    def get_filtering_summary(self):
        message = ''
        if self._false_decorators:
            false_decorators_set = {t[1] for t in self._false_decorators}
            decorator_with_count = {
                false_decorator: len({t[0] for t in self._false_decorators if t[1] == false_decorator})
                for false_decorator in false_decorators_set}
            join_str = "\n\t* "
            message = f'{len({t[0] for t in self._false_decorators})} test(s) skipped due to unavailable '\
                      f'services:{join_str}'\
                      f'{join_str.join([f"{key} ({value} tests)" for key, value in decorator_with_count.items()])}'
        # end if
        return message
    # end def get_filtering_summary
# end class Services


class BugTracker(Features):
    """
    Function decorator, that associates a feature with a function definition.

    This should be used in tests, on test methods, to declare the test feature.
    """
    _INSTANCE = None

    __EMPTY_SET = frozenset()

    _decoratorToFeatures = {}
    _decoratorToId = {}
    _idToFeatures = {}
    _featureHelp = {}
# end class BugTracker


# The global feature monitor. Its name should be ignored by pylint
features = Features()
services = Services()
# The global bugtracker monitor. Its name should be ignored by pylint
bugtracker = BugTracker()

UPPER_PATTERN = compile("[A-Z]")
REVERSED_MARK = 'No'


def isFeatureReversed(feature):
    """
    Check if feature means reversion of defined feature

    i.e.: if 'Foo' is a feature, '[REVERSED_MARK]Foo' is a reversed feature

    :param feature: Feature label to analyze
    :type feature: ``str``

    :return:  Flag indicating that the feature is reversed
    :rtype: ``bool``
    """
    result = (len(feature) >= (len(REVERSED_MARK) + 1))

    if result:
        result = (feature[:len(REVERSED_MARK)] == REVERSED_MARK and UPPER_PATTERN.match(feature[len(REVERSED_MARK)]))
    # end if

    return result
# end def isFeatureReversed

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
