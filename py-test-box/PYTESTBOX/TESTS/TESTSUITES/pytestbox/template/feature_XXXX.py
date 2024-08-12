#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------

# TODO : CUSTOM SECTION 1 :
#  Edit file header
#  This is a template, you should copy it and change some things before it can work.
#  You can find a "How to" documentation on how to implement a feature's test case from this
#  template here:
#  https://spaces.logitech.com/pages/viewpage.action?pageId=61916761
#  In addition, if you add a new HID++ feature, please read "How to add a new HID++ feature into
#  py-test-box" :
#  https://spaces.logitech.com/pages/viewpage.action?pageId=52200581
# TODO : End of CUSTOM SECTION 1 : Remove TODOs when finished
"""
    :package: XXXX.XXXX.XXXX.XXXX
    :brief: Validates HID++ XXXX feature 0xXXXX
    :author: XXXX XXXX
    :date: YYYY/MM/DD
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import BaseTestCase
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level
# TODO : Import required packages, e.g. the feature and the feature's factory:
from pyhid.hidpp.features.common.featureXXXX import FeatureXXXX
from pyhid.hidpp.features.common.featureXXXX import FeatureXXXXFactory


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
# TODO : Replace XXXX with the feature under test name
class XXXXTestCase(BaseTestCase):
    """
    Validates XXXX TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        # TODO : CUSTOM SECTION 2 :
        #  ADD the declaration of useful attributes, it is important to
        #  do them before the super setUp() to avoid problems with tearDown()
        #  EXAMPLE:
        self.post_requisite_needed = False
        # TODO : End of CUSTOM SECTION 2 : Remove TODOs when finished

        # Start with super setUp()
        super().setUp()

        # TODO : Replace XXXX with the feature under test
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0xXXXX)')
        # ---------------------------------------------------------------------------
        self.feature_xxxx_index = self.updateFeatureMapping(feature_id=FeatureXXXX.FEATURE_ID)

        # TODO : CUSTOM SECTION 3 :
        #  ADD the Pre-requisites that will be common to every tests,
        #  there should be one getting the feature index
        #  EXAMPLE:
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Log \'Pre-requisite#2\'')
        # ---------------------------------------------------------------------------
        self.logTrace('Pre-requisite#2')
        # TODO : End of CUSTOM SECTION 3 : Remove TODOs when finished

        # TODO : Create the feature under test object : Replace XXXX with the feature under test
        #  Tip: ConfigurationManager provides "get_feature_version" method to get version as int from
        #  feature's configuration
        # Get the feature under test
        self.feature_under_test = FeatureXXXXFactory.create(version)
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # Do all custom tear down actions into a try / except statement to ensure the super
        # tear down is always executed
        # noinspection PyBroadException
        try:
            # TODO : CUSTOM SECTION 4 :
            #  ADD the Post-requisites
            #  EXAMPLE:
            if self.post_requisite_needed:
                # ---------------------------------------------------------------------------
                self.logTitle2('Post-requisite#1: Log \'Post-requisite#1\'')
                # ---------------------------------------------------------------------------
                self.logTrace('Post-requisite#1')
            # end if
            # TODO : End of CUSTOM SECTION 4 : Remove TODOs when finished
        except:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        # End with super tearDown()
        super().tearDown()
    # end def tearDown

    # TODO : CUSTOM SECTION 5 :
    #  ADD test methods.
    #  Good practice :
    #   * Use feature test utils to implement reusable functions (see FeatureXXXXTestUtils class
    #   below
    #   * Use feature under test object (create in test setup) to access feature's interfaces
    #  EXAMPLE:
    @features('FeatureXXXX')
    @level('Functionality')
    @services('PowerSupply')
    def test_action_test_1(self):
        """
        Do action with parameter 1.
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Do action with argument_1 = 1')
        # ---------------------------------------------------------------------------
        var = self.feature_under_test.get_something()

        FeatureXXXXTestUtils.check_something(var)

        if not var:
            # Add a warning if needed, check API to see possibilities
            self.log_warning(message="Warning message")
        # end if

        # TODO : End the test with the test ID. Each test should be documented in the test case
        #  specification.
        self.testCaseChecked("FNT_XXXX_0001")
    # end def test_action_test_1
    # TODO : End of CUSTOM SECTION 5 : Remove TODOs when finished
# end class XXXXTestCase


# TODO : CUSTOM SECTION 6 : Feature test utils class
#  Implement a class to provide reusable generic functions to be used in tests related to the
#  feature
class FeatureXXXXTestUtils(object):
    """
    This class provides helpers for common checks on XXXX feature
    """
    @staticmethod
    def check_something(var):
        """
        Check something relative to var

        :param var: Variable to check
        :type var: ``type of var``
        """
        # TODO : function code goes here
    # end def check_something
# end class FeatureXXXXTestUtils
# TODO : End of CUSTOM SECTION 6 : Remove TODOs when finished


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
