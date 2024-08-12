#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package    pylint.decorator_order_checker
@brief      Check decorator order defined on Confluence
            link: https://spaces.logitech.com/display/ptb/Decorator+sequence+and+usage
@author     Fred Chen
@date       2019/08/01
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylint.checkers import BaseChecker
from pylint.checkers.base import BasicChecker


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DecoratorOrderChecker(BaseChecker):
    """
    Checking decorator order according to `Project rules`
    written down on Confluence.

    Usage
    1. change directory to py-test-box
    2. command examples
         Single file: pylint --disable=all --enable=decorator-order-checker PYTESTBOX/TESTS/TESTSUITES/pytestbox/hid/important/feature_0000.py
         All: pylint --disable=all --enable=decorator-order-checker PYTESTBOX/TESTS/TESTSUITES/pytestbox
    """

    name = 'decorator-order-checker'
    NO_DECORATORS = 'no-decorators'
    NO_DECORATORS_SUBITEMS = 'no-decorators-subitems'
    UNSUPPORTED_TAG = 'unsupported-tag'
    UNSORTED_DECORATOR = 'unsorted-decorator'
    INVALID_LEVEL_TAG = 'invalid-level-tag'
    msgs = {
        'I0051': ('%s has not any decorators.',
                  NO_DECORATORS,
                  'Refer to decorator rules on Confluence'),
        'I0052': ('%s has not any sub-times in decorators.',
                  NO_DECORATORS_SUBITEMS,
                  'Refer to decorator rules on Confluence'),
        'I0053': ('Unsupported tag "%s" in %s',
                  UNSUPPORTED_TAG,
                  'Refer to decorator rules on Confluence'),
        'C0054': ('Decorator "%s" is in the wrong position. Move it above "%s".',
                  UNSORTED_DECORATOR,
                  'Refer to decorator rules on Confluence'),
        'C0055': ('Invalid level tag: "%s".',
                  INVALID_LEVEL_TAG,
                  'Refer to decorator rules on Confluence')
    }
    options = ()
    priority = -1

    _verbose = False

    def __init__(self, linter):
        """
        Constructor

        @param linter   [in](linter)    pylint object
        """
        super().__init__(linter)
        self.basic_checker = BasicChecker(self.linter)

        # priority of decorator order, the value 1 is the highest priority
        self.tag_priority = dict()
        self.tag_priority['features'] = 1
        self.tag_priority['level'] = 2
        self.tag_priority['services'] = 3
        self.tag_priority['bugtracker'] = 4
        self.tag_priority['skip'] = 5
        self.tag_priority['skipUnless'] = 5
        self.tag_priority['skipIf'] = 5
        self.tag_priority['expectedFailure'] = 5
        self.tag_priority['copy_doc'] = 6

        # Valid tag in LEVEL
        self.level_tag = dict()
        self.level_tag['Interface'] = 1
        self.level_tag['Business'] = 2
        self.level_tag['Functionality'] = 3
        self.level_tag['ErrorHandling'] = 4
        self.level_tag['Robustness'] = 5
        self.level_tag['Stress'] = 6
        self.level_tag['DeepSleepWaitingTime'] = 7
        self.level_tag['Deprecated'] = 8
        self.level_tag['Security'] = 9
        self.level_tag['Time-consuming'] = 10
        self.level_tag['Timing'] = 11
        self.level_tag['CiScript'] = 12
        self.level_tag['ReleaseCandidate'] = 13
        self.level_tag['Tools'] = 14
        self.level_tag['Performance'] = 15
        self.level_tag['SmokeTests'] = 16

        if self._verbose:
            print('')
        # end if
    # end def __init__

    def visit_classdef(self, node):
        """
        Be called while entering class definition

        @param node     [in](node)  class node object
        """
        if self._verbose:
            print(node.name)
        # end if
    # end def visit_classdef

    def visit_functiondef(self, node):
        """
        Be called while entering function definition

        @param node     [in](node)      function node object
        """
        if node.name.startswith('test_'):
            self._check_decorator_order(node)
            if self._verbose:
                print(f'- {node.name}')
            # end if
        # end if
    # end def visit_functiondef

    def _check_decorator_order(self, node):
        """
        Check decorator order shall follow the usage defined on Confluence.
        https://spaces.logitech.com/display/ptb/Decorator+sequence+and+usage

        @param node     [in](node)      function node object
        """
        if node.decorators is None:
            self.add_message(self.NO_DECORATORS, node=node, args=node.name)
        else:
            if node.decorators.nodes is None:
                self.add_message(self.NO_DECORATORS_SUBITEMS, node=node, args=node.name)
            else:
                prev_priority = 0
                prev_tag = None
                for n in node.decorators.nodes:
                    tag = None
                    try:
                        if not hasattr(n, 'func'):
                            if not hasattr(n, 'name'):
                                tag = n.attrname
                            else:
                                tag = n.name
                            # end if
                        else:
                            if not hasattr(n.func, 'name'):
                                tag = n.func.attrname
                            else:
                                tag = n.func.name
                            # end if
                        # end if

                        # check decorator order
                        if self.tag_priority[tag] < prev_priority:
                            # report error
                            args = tag, prev_tag
                            self.add_message(self.UNSORTED_DECORATOR, node=node, args=args)
                        # end if

                        # check level tag
                        if tag == 'level':
                            self._check_level_tag(node, n.args[0].value)
                        # end if

                        prev_priority = self.tag_priority[tag]
                        prev_tag = tag
                    except Exception as e:
                        print(e)
                        # ignore unsupported tag but display information
                        args = tag, node
                        print("tag", tag)
                        print("node", node)
                        print("n", n)
                        self.add_message(self.UNSUPPORTED_TAG, node=node, args=args)
                    # end try
                # end for
            # end if
        # end if
    # end def _check_decorator_order

    def _check_level_tag(self, node, tag):
        """
        Check the input level tag name is valid or not
        valid tag: Interface,Business,Functionality,ErrorHandling,Robustness,Stress,Time-consuming,ReleaseCandidate

        @param tag      [in](string) level tag name
        """
        try:
            self.level_tag[tag]
        except Exception:
            self.add_message(self.INVALID_LEVEL_TAG, node=node, args=tag)
        # end try
    # end def _check_level_tag

# end class DecoratorOrderChecker

# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------


def register(linter):
    """
    required method to auto register this checker
    """
    linter.register_checker(DecoratorOrderChecker(linter))
# end def register

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
