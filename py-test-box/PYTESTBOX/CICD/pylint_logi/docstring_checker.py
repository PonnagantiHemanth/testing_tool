#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Pylint Logi
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylint_logi.docstring_checker
:brief: Custom pylint checker for pytest box docstring format
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/13
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------

from collections import deque
from enum import Enum
from enum import auto
from pathlib import Path
from re import M as re_M
from re import findall as re_findall
from re import fullmatch as re_fullmatch
from re import match as re_match
from re import split as re_split
from re import search as re_search

from astroid import Assert
from astroid import AssignName
from astroid import Attribute
from astroid import Call
from astroid import ExceptHandler
from astroid import Expr
from astroid import FunctionDef
from astroid import If
from astroid import Match
from astroid import Name
from astroid import Raise
from astroid import Return
from astroid import Try
from astroid import Yield
from pylint.checkers import BaseChecker

PATTERN_SPLIT_FIELDS = r"(^\s*:(?:\w+|\S+ \S+):)"

NOT_IMPLEMENTED_EXCEPTIONS = ["NotImplementedAbstractMethodError",
                              "NotImplementedError"]

NO_DESCRIPTION_PARAMS = ['self', 'cls']

NODES_TO_EXPEND = (If, Try, Match)

POTENTIAL_TEST_EXCEPTIONS_TOKEN = "@TestExceptionPlaceHolder"

TEST_EXCEPTIONS = ["AssertionError", "TestException"]

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
RULES_ON_CONFLUENCE = "refer to the docstring rules on Confluence"

OPTIONAL_TAG = "- OPTIONAL"


class FieldType(Enum):
    """
    types of field in a docstring
    """
    PLAIN = auto()
    PARAM = auto()
    TYPE = auto()
    RETURN = auto()
    RTYPE = auto()
    RAISE = auto()
    KWARGS = auto()

    UNSUPPORTED = auto()
# end class FieldType

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LogiDocstringChecker(BaseChecker):
    """
    Pylint checker verifying format and content of docstrings
    """

    BASE_ID = "55" # Arbitrary number for the checker id, chosen in the range available for custom checkers

    name = "docstring_checker"

    NO_DOCSTRING = "no-docstring"
    WRONG_QUOTE = "docstring-wrong-quote"
    MODULE_FORMAT = "module-wrong-format"
    INIT_BRIEF = "init-has-brief"
    INIT_FORMAT = "init-wrong-format"
    CLASS_FORMAT = "class-wrong-format"
    METHOD_BRIEF = "method-no-brief"
    METHOD_FORMAT = "method-wrong-format"
    MISSING_PARAM = "missing-parameter"
    MISSING_TYPE = "missing-type"
    MISSING_PARAM_BRIEF = "missing-parameter-brief"
    MISSING_TYPE_BRIEF = "missing-type-brief"
    MISSING_OPTIONAL = "missing-optional"
    ORDER_PARAM = "wrong-order-param"
    ORDER_TYPE = "wrong-order-type"
    DUPLICATED_PARAM = "duplicated-param"
    DUPLICATED_TYPE = "duplicated-type"
    UNSUPPORTED_FIELD = "unsupported-field"
    PARAM_UNNEEDED_DESCRIPTION = "unneeded-param-descriptions"
    TYPE_HINT_FORMAT_ERROR = "type-hint-format-error"
    MISSING_RETURN = "missing-return"
    MISSING_RTYPE = "missing-rtype"
    MISSING_RETURN_BRIEF = "missing-return-brief"
    MISSING_RTYPE_BRIEF = "missing-rtype-brief"
    DUPLICATED_RETURN = "duplicated-return"
    DUPLICATED_RTYPE = "duplicated-rtype"
    RTYPE_FORMAT_ERROR = "rtype-format-error"
    EXPECTED_NO_RETURN = "expected-no-return"
    INIT_WITH_RETURN = "init-with-return"
    UNKNOWN_PARAM = "unknown-param"
    RAISE_FORMAT = "raise-wrong-format"
    RAISE_MISSING = "raise-missing"
    EXPECTED_NO_RAISE = "expected-no-raise"

    msgs = {

        "W" + BASE_ID + "00": ("%s has no docstring%s",
                               NO_DOCSTRING,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "01": ('%s should use """ quotations',
                               WRONG_QUOTE,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "02": ("%s module's format is invalid:\n\t *%s\n",
                               MODULE_FORMAT,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "03": ("%s's init method's should not have a brief ",
                               INIT_BRIEF,
                               RULES_ON_CONFLUENCE),
        "C" + BASE_ID + "04": ("%s's init method's format is invalid \n\t *%s\n",
                               INIT_FORMAT,
                               RULES_ON_CONFLUENCE),
        "C" + BASE_ID + "05": ("%s class's format is invalid \n\t *%s\n",
                               CLASS_FORMAT,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "06": ("%s%s method lacks a brief",
                               METHOD_BRIEF,
                               RULES_ON_CONFLUENCE),
        "C" + BASE_ID + "07": ("%s%s method's format is invalid \n\t *%s\n",
                               METHOD_FORMAT,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "08": ("%s%s method's docstring is missing the following parameters:\n\t *%s\n",
                               MISSING_PARAM,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "09": ("%s%s method's docstring is missing the following types hint:\n\t *%s\n",
                               MISSING_TYPE,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "10": ("%s%s method's docstring is missing description of the following parameters:\n\t *%s\n",
                               MISSING_PARAM_BRIEF,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "11": ("%s%s method's docstring is missing type "
                               "hint details of the following parameters:\n\t *%s\n",
                               MISSING_TYPE_BRIEF,
                               RULES_ON_CONFLUENCE),
        "C" + BASE_ID + "12": ("%s%s method's docstring has the following parameters in the wrong position:\n\t *%s\n",
                               ORDER_PARAM,
                               RULES_ON_CONFLUENCE),
        "C" + BASE_ID + "13": ("%s%s method's docstring has the following parameters' type hint in the "
                               "wrong position (not after the parameter definition):\n\t *%s\n",
                               ORDER_TYPE,
                               RULES_ON_CONFLUENCE),
        "C" + BASE_ID + "14": ("%s%s method's docstring has the following optional parameters without the '- OPTIONAL'"
                               " tag at the end of the brief:\n\t *%s\n",
                               MISSING_OPTIONAL,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "15": ("%s%s method's docstring has the following parameters duplicated:\n\t *%s\n",
                               DUPLICATED_PARAM,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "16": ("%s%s method's docstring has the following type hint duplicated:\n\t *%s\n",
                               DUPLICATED_TYPE,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "17": ("%s%s method's docstring has the following unsupported field: %s",
                               UNSUPPORTED_FIELD,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "18": ("%s%s method's docstring has the following parameters who should not be described: %s",
                               PARAM_UNNEEDED_DESCRIPTION,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "19": ("%s%s method's docstring has the following type hint with an invalid format:\n\t *%s\n",
                               TYPE_HINT_FORMAT_ERROR,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "20": ("%s%s method is expected to return something but doesn't define it in the docstring:",
                               MISSING_RETURN,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "21": ("%s%s method's docstring is expected has a return field but has no rtype:",
                               MISSING_RTYPE,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "22": ("%s%s method's docstring is expected has a return field "
                               "but no corresponding description",
                               MISSING_RETURN_BRIEF,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "23": ("%s%s method's docstring is expected has a rtype field "
                               "but no corresponding description",
                               MISSING_RTYPE_BRIEF,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "24": ("%s%s method's docstring is expected has a duplicated return field",
                               DUPLICATED_RETURN,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "25": ("%s%s method's docstring is expected has a duplicated rtype field",
                               DUPLICATED_RTYPE,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "26": ("%s%s method's docstring has the rtype hint with an invalid format",
                               RTYPE_FORMAT_ERROR,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "27": ("%s%s method's docstring has a return but no corresponding statement is in the code",
                               EXPECTED_NO_RETURN,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "28": ("%s's init's docstring has a return described in the docstring "
                               "while inits should not return",
                               INIT_WITH_RETURN,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "29": ("%s%s method's docstring has the following unknown parameters:\n\t *%s\n",
                               UNKNOWN_PARAM,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "30": ("%s%s method's docstring has the following "
                               "raise field with an invalid format:\n\t *%s\n",
                               RAISE_FORMAT,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "31": ("%s%s method's docstring is missing the following raise field:\n\t *%s\n",
                               RAISE_MISSING,
                               RULES_ON_CONFLUENCE),
        "W" + BASE_ID + "32": ("%s%s method's docstring has the following raise fields but no corresponding "
                               "raise statement in the code:\n\t *%s\n",
                               EXPECTED_NO_RAISE,
                               RULES_ON_CONFLUENCE),
    }

    # extra message text
    TXT_DOCSTRING_START = "Doc string should start with a line break"
    TXT_DOCSTRING_END = "Doc string should end with a line break"
    TXT_REFERENCE_MAYBE_BROKEN = "(could be malformed comment referring to inherited docstring)"
    TXT_MODULE_PLACE_PACKAGE = "Module doc first field should be the package field"
    TXT_MODULE_PLACE_BRIEF = "Module doc second field should be the brief field"
    TXT_MODULE_PLACE_AUTHOR = "Module doc third field should be the author field"
    TXT_MODULE_PLACE_DATE = "Module doc fourth field should be the date field"
    TXT_MODULE_FORMAT_PACKAGE = "Package field in wrong format"
    TXT_MODULE_FORMAT_AUTHOR = "Author field is in the wrong format"
    TXT_MODULE_FORMAT_DATE = "Date field is in the wrong format"
    TXT_MODULE_PATH_PACKAGE = "Package doesn't correspond to file, not in module"
    TXT_PARAM = ":param %s:"
    TXT_TYPE = ":type %s:"

    def __init__(self, linter=None):
        """
        :param linter: linter used - OPTIONAL
        :type linter: ``Linter`` or ``None``
        """
        super().__init__(linter)
        self.current_class_stack = deque()
        self.lines = None
    # end def __init__

    @property
    def class_name(self):
        """
        current name of a class to be used in display

        :return: the name or a message for functions
        :rtype: ``str``
        """
        return f"{self.current_class_stack[-1].name}." if len(self.current_class_stack) > 0 else "top level function "
    # end def property getter class_name

    def visit_module(self, node):
        """
        check a module's docstring

        called when the linter enters a new module.

        :param node: module node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.Module``
        """
        with open(node.path[0], 'r') as file:
            self.lines = file.readlines()
        # end with

        if node.doc_node is not None:
            self._check_module_doc_format(node)
        else:
            self.add_message(self.NO_DOCSTRING, node=node, args=(node.name, ""))
        # end if
    # end def visit_module

    def visit_classdef(self, node):
        """
        check a class docstring and store its name in the stack

        called when entering class definition

        :param node: class node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.ClassDef``
        """

        self.current_class_stack.append(node)
        if node.doc_node is not None:
            self._check_class_doc_format(node)
            return
        # end if

        start = node.position.end_lineno
        end = node.body[0].end_lineno - 1

        comment_line = ' '.join(self.lines[start:end]).strip()

        if node.bases and re_match(r"# See ``[\w.]+``(?: and ``[\w.]+``)*", comment_line):
            return
        # end if

        if (len(self.current_class_stack) >= 2 and self.current_class_stack[-2].bases
                and re_findall(fr"^# See ``[\w.]+\.{node.name}``", comment_line)):
            return
        # end if

        extra_message = self.TXT_REFERENCE_MAYBE_BROKEN if comment_line.startswith("#") else ""

        self.add_message(self.NO_DOCSTRING, node=node, args=(node.name, extra_message))
    # end def visit_classdef

    def leave_classdef(self, _node):
        """
        remove the top level class

        called when exiting class definition

        :param _node: class node (unused)
        :type _node: ``astroid.nodes.scoped_nodes.scoped_nodes.ClassDef``
        """
        self.current_class_stack.pop()
    # end def leave_classdef

    def visit_functiondef(self, node):
        """
        check a function or method docstring and store its name in the stack

        called when entering class definition

        :param node: function node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.FunctionDef``
        """

        extra_message = ""
        if node.name == "__init__":
            if node.doc_node is not None:
                self._check_init_doc_format(node)
                return
            # end if
            if len(node.args.args) == 1:
                return
            # end if
        elif re_fullmatch(r"__.*__", node.name) and node.doc_node is None:  # skip magic methods without docstring
            return
        # end if

        if node.doc_node is not None:
            self._check_method_doc_format(node)
            return
        # end if

        if self.current_class_stack and self.current_class_stack[-1].bases:
            start = node.position.end_lineno
            end = node.body[0].lineno - 1

            comment_line = ' '.join(self.lines[start:end]).split(":", maxsplit=1)[-1].strip().split("\n")[0].strip()

            if re_search(fr"^# See ``[\w.]+\.{node.name}``", comment_line):
                return
            # end if
            extra_message = self.TXT_REFERENCE_MAYBE_BROKEN if comment_line.startswith("#") else ""
        # end if
        self.add_message(self.NO_DOCSTRING, node=node, args=(node.name, extra_message))
    # end def visit_functiondef

    # noinspection DuplicatedCode
    def _check_generic_params(self, node, processed_fields):
        """
        verify if the parameters correspond to the current docstring

        :param node: function node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.FunctionDef``
        :param processed_fields: list of field tuples of the docstring preparsed
        :type processed_fields: ``list[tuple]``

        :raise ``ValueError``: if the argument type in the node is not supported
        """
        params = list(filter(lambda x: x[0] == FieldType.PARAM, processed_fields))
        types = list(filter(lambda x: x[0] == FieldType.TYPE, processed_fields))
        # make a set of params to ignore duplicate it will be used to check if a param is unknown from the definition
        set_params_name = set([x[2] for x in params])
        missing_param_name = []
        missing_type_name = []
        missing_param_description = []
        missing_type_description = []
        missing_optional = []
        wrong_order_param = []
        wrong_order_type = []
        duplicated_param_name = []
        duplicated_type_name = []
        type_format_errors = []

        index_offset = 0
        args = list(node.args.args)
        first_default = len(args) - len(node.args.defaults)

        varargs = node.args.vararg
        if varargs:
            args.append(varargs)
        # end if

        kwargs = node.args.kwarg
        if kwargs:
            args.append(kwargs)
        # end if

        for index, argument_from_definition in enumerate(args):

            if isinstance(argument_from_definition, AssignName):
                definition_name = argument_from_definition.name
            elif isinstance(argument_from_definition, str):
                definition_name = argument_from_definition
            else:
                raise ValueError(f"Unexpected argument type {type(argument_from_definition)}")
            # end if

            params_with_the_right_name = list(filter(lambda x: x[2] == definition_name, params))
            types_with_the_right_name = list(filter(lambda x: x[2] == definition_name, types))
            if definition_name in NO_DESCRIPTION_PARAMS:
                if len(params_with_the_right_name) == 0:
                    index_offset = -1
                else:
                    set_params_name.remove(definition_name)
                    self.add_message(self.PARAM_UNNEEDED_DESCRIPTION, node=node, args=(self.class_name, node.name,
                                                                                       definition_name))
                # end if
                continue
            # end if

            if len(params_with_the_right_name) == 0:
                missing_param_name.append(self.TXT_PARAM % definition_name)
            elif len(params_with_the_right_name) == 1:
                set_params_name.remove(definition_name)
                param_arg_index = params.index(params_with_the_right_name[0])
                if param_arg_index != index + index_offset:
                    wrong_order_param.append(params_with_the_right_name[0][2])
                # end if

                param_field_index = processed_fields.index(params_with_the_right_name[0])

                if param_field_index == len(processed_fields) - 1:
                    missing_param_description.append(params_with_the_right_name[0][2])
                elif (processed_fields[param_field_index+1][0] == FieldType.PLAIN and
                      len(processed_fields[param_field_index + 1][1].strip()) > 0):

                    if index >= first_default and definition_name not in [varargs, kwargs]:
                        lines = processed_fields[param_field_index + 1][1].split("\n")
                        optional_tag_found = False
                        for line in lines:
                            if line.strip().endswith(OPTIONAL_TAG):
                                optional_tag_found = True
                                break
                            # end if
                        # end for
                        if not optional_tag_found:
                            missing_optional.append(params_with_the_right_name[0][2])
                        # end if
                    # end if
                else:
                    missing_param_description.append(params_with_the_right_name[0][2])
                # end if

                if len(types_with_the_right_name) == 0:
                    missing_type_name.append(self.TXT_TYPE % definition_name)
                elif len(types_with_the_right_name) == 1:
                    type_index = processed_fields.index(types_with_the_right_name[0])

                    if type_index < param_field_index or type_index > param_field_index + 2:
                        wrong_order_type.append(params_with_the_right_name[0][2])
                    # end if

                    if type_index == len(processed_fields) - 1:
                        missing_type_description.append(types_with_the_right_name[0][2])
                    elif (processed_fields[type_index + 1][0] == FieldType.PLAIN and
                          len(processed_fields[type_index + 1][1].strip()) > 0):
                        type_definition = processed_fields[type_index + 1][1].strip()

                        self._check_generic_type_hint(type_definition)
                        if not self._check_generic_type_hint(type_definition):
                            type_format_errors.append(self.TXT_TYPE % definition_name)
                        # end if
                    else:
                        missing_type_description.append(types_with_the_right_name[0][2])
                    # end if
                else:
                    duplicated_type_name.append(self.TXT_TYPE % definition_name)
                # end if
            else:
                set_params_name.remove(definition_name)
                duplicated_param_name.append(self.TXT_PARAM % definition_name)
            # end if
        # end for

        if len(missing_param_name) > 0:
            self.add_message(self.MISSING_PARAM, node=node, args=(self.class_name, node.name,
                                                                  self.concatenate_sub_errors(missing_param_name)))
        # end if

        if len(missing_type_name) > 0:
            self.add_message(self.MISSING_TYPE, node=node, args=(self.class_name, node.name,
                                                                 self.concatenate_sub_errors(missing_type_name)))
        # end if

        if len(missing_param_description) > 0:
            self.add_message(self.MISSING_PARAM_BRIEF, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(missing_param_description)))
        # end if

        if len(missing_type_description) > 0:
            self.add_message(self.MISSING_TYPE_BRIEF, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(missing_type_description)))
        # end if

        if len(missing_optional) > 0:
            self.add_message(self.MISSING_OPTIONAL, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(missing_optional)))
        # end if

        if len(type_format_errors) > 0:
            self.add_message(self.TYPE_HINT_FORMAT_ERROR, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(type_format_errors)))
        # end if

        if set_params_name:
            unknown_params = [self.TXT_PARAM % name for name in set_params_name]
            self.add_message(self.UNKNOWN_PARAM, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(unknown_params)))
        elif duplicated_param_name:
            self.add_message(self.DUPLICATED_PARAM, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(duplicated_param_name)))
        elif wrong_order_param:
            self.add_message(self.ORDER_PARAM, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(wrong_order_param)))
        # end if

        if duplicated_type_name:
            self.add_message(self.DUPLICATED_TYPE, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(duplicated_type_name)))
        elif wrong_order_type:
            self.add_message(self.ORDER_TYPE, node=node,
                             args=(self.class_name, node.name, self.concatenate_sub_errors(wrong_order_type)))
        # end if
    # end def _check_generic_params

    def _check_return(self, node, processed_fields):
        """
        verify if the returns correspond to the current docstring

        :param node: function node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.FunctionDef``
        :param processed_fields: list of field tuples of the docstring preparsed
        :type processed_fields: ``list[tuple]``
        """
        returns_in_body = list(filter(lambda element:
                                      (isinstance(element, Return) and element.value is not None) or
                                      (isinstance(element, (Expr)) and isinstance(element.value, Yield)
                                       and element.value.value is not None),
                                      self._flatten_body(node)))

        unimplemented = (len(node.body) == 1 and isinstance(node.body[0], Raise)
                         and isinstance(node.body[0].exc, Call)
                         and node.body[0].exc.func.name in NOT_IMPLEMENTED_EXCEPTIONS)

        expects_return = len(returns_in_body) > 0

        returns_in_docstring = list(filter(lambda x: x[0] == FieldType.RETURN, processed_fields))
        rtypes_in_docstring = list(filter(lambda x: x[0] == FieldType.RTYPE, processed_fields))

        if len(returns_in_docstring) == 1:
            if expects_return or unimplemented:
                index = processed_fields.index(returns_in_docstring[0])

                if index == len(processed_fields) - 1 or not (
                        processed_fields[index + 1][0] == FieldType.PLAIN and
                        len(processed_fields[index + 1][1].strip()) > 0):
                    self.add_message(self.MISSING_RETURN_BRIEF, node=node, args=(self.class_name, node.name))
                # end if

                if len(rtypes_in_docstring) == 0:
                    self.add_message(self.MISSING_RTYPE, node=node, args=(self.class_name, node.name))
                elif len(rtypes_in_docstring) > 1:
                    self.add_message(
                        LogiDocstringChecker.DUPLICATED_RTYPE, node=node, args=(self.class_name, node.name))
                else:
                    index = processed_fields.index(rtypes_in_docstring[0])

                    if index == len(processed_fields) - 1 or not (
                            processed_fields[index + 1][0] == FieldType.PLAIN and
                            len(processed_fields[index + 1][1].strip()) > 0):
                        self.add_message(self.MISSING_RTYPE_BRIEF, node=node, args=(self.class_name, node.name))
                    elif not self._check_generic_type_hint(processed_fields[index + 1][1].strip()):
                        self.add_message(self.RTYPE_FORMAT_ERROR, node=node, args=(self.class_name, node.name))
                    # end if
                # end if

            elif not expects_return:
                self.add_message(self.EXPECTED_NO_RETURN, node=node, args=(self.class_name, node.name))
            # end if
        elif len(returns_in_docstring) > 1:
            self.add_message(LogiDocstringChecker.DUPLICATED_RETURN, node=node, args=(self.class_name, node.name))
        else:
            if expects_return:
                self.add_message(self.MISSING_RETURN, node=node, args=(self.class_name, node.name))
            # end if
        # end if
    # end def _check_return
    
    def _check_raise(self, node, processed_fields):
        """
        verify if the raise correspond to the current docstring

        :param node: function node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.FunctionDef``
        :param processed_fields: list of field tuples of the docstring preparsed
        :type processed_fields: ``list[tuple]``
        """
        raises_in_body_set = set()
        is_test = node.name.startswith("test_")
        assertion_in_body = False
        except_dict = dict()
        for body_node in self._flatten_body(node):
            if isinstance(body_node, Raise) and body_node.exc:
                if hasattr(body_node.exc, "func") and body_node.exc.func:
                    if isinstance(body_node.exc.func, Attribute):
                        return # skip checks on attribute exceptions, as they are complicated to check
                    elif body_node.exc.func.name in NOT_IMPLEMENTED_EXCEPTIONS:
                        return  # skip checks on not implemented methods
                    # end if
                    raises_in_body_set.add(body_node.exc.func.name)
                elif isinstance(body_node.exc, Name):
                    name = body_node.exc.name
                    if name in except_dict:
                        raises_in_body_set.add(except_dict[name])
                    # end if
                # end if
            elif isinstance(body_node, Raise):
                raises_in_body_set.add(except_dict[""])
            elif isinstance(body_node, Assert):
                raises_in_body_set.add("AssertionError")
                assertion_in_body = True
            elif not is_test and isinstance(body_node, Expr) and isinstance(body_node.value, Call) and isinstance(
                    body_node.value.func, Attribute) and re_match(r"assert[A-Z]\w*|fail",
                                                                  body_node.value.func.attrname):
                raises_in_body_set.add(POTENTIAL_TEST_EXCEPTIONS_TOKEN)
            elif isinstance(body_node, ExceptHandler):
                if body_node.name is not None:
                    except_dict[body_node.name.name] = body_node.type.repr_name()
                else:
                    except_dict[""] = body_node.type.repr_name()
                # end if
            # end if
        # end for
        raises_in_docstring = list(filter(lambda x: x[0] == FieldType.RAISE, processed_fields))
        invalid_format = []
        not_found = []
        for raise_field in raises_in_docstring:
            regex_match = re_match(r"``(\S+)``", raise_field[2])
            if not regex_match:
                invalid_format.append(raise_field[1].strip())
            elif regex_match.group(1) not in raises_in_body_set:
                if regex_match.group(1) in TEST_EXCEPTIONS and POTENTIAL_TEST_EXCEPTIONS_TOKEN in raises_in_body_set:
                    raises_in_body_set.remove(POTENTIAL_TEST_EXCEPTIONS_TOKEN)
                else:
                    not_found.append(raise_field[1].strip())
                # end if
            else:
                raises_in_body_set.remove(regex_match.group(1))
            # end if
        # end for

        if invalid_format:
            self.add_message(
                self.RAISE_FORMAT, node=node, args=(self.class_name,
                                                    node.name,
                                                    self.concatenate_sub_errors(invalid_format)))
        elif not_found:
            self.add_message(
                self.EXPECTED_NO_RAISE, node=node, args=(self.class_name,
                                                         node.name,
                                                         self.concatenate_sub_errors(not_found)))
        else:
            # replace the placeholder to a more explicit message
            if POTENTIAL_TEST_EXCEPTIONS_TOKEN in raises_in_body_set:
                raises_in_body_set.remove(POTENTIAL_TEST_EXCEPTIONS_TOKEN)
                if not assertion_in_body:
                    raises_in_body_set.add("A test exception is expected and raised by a function call, "
                                           "however, the linter could not detect the exception type.")
                # end if
            # end if
            if raises_in_body_set:
                self.add_message(
                    self.RAISE_MISSING, node=node, args=(self.class_name,
                                                         node.name,
                                                         self.concatenate_sub_errors(raises_in_body_set)))
            # end if
        # end if
    # end def _check_raise

    @staticmethod
    def _check_generic_type_hint(type_definition):
        """
        Generic check on a type hint formating

        :param type_definition: definitions string extracted from the docstring
        :type type_definition: ``str``

        :return: True if the format is correct
        :rtype: ``bool``
        """
        if re_fullmatch(r"``[][()\w,. |\n]+``(?: or[\n ]``[][\w,. |\n]+``)*", type_definition):
            # a brief that is in the correct format is present, this could be improved by checking types
            return True
        else:
            return False
        # end if
    # end def _check_generic_type_hint

    def _check_module_doc_format(self, node):
        """
        Verify the check docstring format of a module

        :param node: module node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.Module``
        """
        format_errors = self._check_global_format(node)
        doc = node.doc_node

        if len(format_errors) == 0:
            lines = doc.value.split("\n")
            index = 1

            # The first line is allowed to be tool generation declaration
            if lines[index].startswith(":tool: "):
                index += 1
            # end if

            if not lines[index].startswith(":package: "):
                format_errors.append(self.TXT_MODULE_PLACE_PACKAGE)
            elif re_fullmatch(r":package: \w+[\w.]*", lines[index]) is None:
                format_errors.append(self.TXT_MODULE_FORMAT_PACKAGE)
            else:
                path = list(Path(node.path[0]).parts)
                package = lines[index].removeprefix(":package: ").split(".")
                if path[-1] == "__init__.py":
                    path.remove("__init__.py")
                # end if
                path[-1] = path[-1].removesuffix(".py")

                for i, package_level in enumerate(reversed(package)):
                    if package_level != path[-(1 + i)]:
                        format_errors.append(f"{self.TXT_MODULE_PATH_PACKAGE} {package_level}")
                    # end if
                # end for
            # end if
            index += 1

            if not lines[index].startswith(":brief: "):
                format_errors.append(self.TXT_MODULE_PLACE_BRIEF)
                index += 1
            else:
                # allows brief to be multiline
                index += 1
                while not lines[index].startswith(":"):
                    index += 1
                # end while
            # end if

            if not lines[index].startswith(":author: "):
                format_errors.append(self.TXT_MODULE_PLACE_AUTHOR)
            elif re_fullmatch(
                    r":author: [\w -]+ <[\w.-]+@[\w.-]+.[\w]+>(:?,[\w -]+ <[\w.-]+@[\w.-]+.[\w]+>)*",
                    lines[index]) is None:
                format_errors.append(self.TXT_MODULE_FORMAT_AUTHOR)
            # end if
            index += 1

            if not lines[index].startswith(":date: "):
                format_errors.append(self.TXT_MODULE_PLACE_DATE)
            elif re_fullmatch(r":date: 20\d{2}/(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])", lines[index]) is None:
                format_errors.append(self.TXT_MODULE_FORMAT_DATE)
            # end if
        # end if

        if len(format_errors) > 0:
            errors_str = self.concatenate_sub_errors(format_errors)
            self.add_message(self.MODULE_FORMAT, node=node, args=(node.name, errors_str))
        # end if
    # end def _check_module_doc_format

    def _check_class_doc_format(self, node):
        """
        Verify the check docstring format of a class

        :param node: class node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.ClassDef``
        """
        format_errors = self._check_global_format(node)

        if format_errors:
            errors_str = self.concatenate_sub_errors(format_errors)
            self.add_message(self.CLASS_FORMAT, node=node, args=(node.name, errors_str))
        # end if
    # end def _check_class_doc_format

    def _check_method_doc_format(self, node):
        """
        Verify the check docstring format of a method

        :param node: function node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.FunctionDef``
        """
        format_errors = self._check_global_format(node)

        processed_fields = self._extract_method_fields(node)

        index = 0
        if processed_fields[0][0] != FieldType.PLAIN or len(processed_fields[0][1].strip()) == 0:
            self.add_message(self.METHOD_BRIEF, node=node, args=(self.class_name, node.name))
        else:
            index += 1
        # end if

        self._check_generic_params(node, processed_fields)
        self._check_return(node, processed_fields)
        self._check_raise(node, processed_fields)

        if format_errors:
            errors_str = self.concatenate_sub_errors(format_errors)
            self.add_message(self.METHOD_FORMAT, node=node, args=(self.class_name, node.name, errors_str))
        # end if
    # end def _check_method_doc_format

    @staticmethod
    def concatenate_sub_errors(sub_errors):
        """
        Concatenate sub errors in a new line as a list

        :param sub_errors: list of the sub errors texts
        :type sub_errors: ``list[str]`` or ``set[str]``

        :return: a string of all the list
        :rtype: ``str``
        """
        return "\n\t *".join(sub_errors)
    # end def concatenate_sub_errors

    def _check_init_doc_format(self, node):
        """
        Verify the check docstring format of an init method

        :param node: function node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.FunctionDef``
        """
        format_errors = self._check_global_format(node)

        processed_fields = self._extract_method_fields(node)

        index = 0
        if processed_fields[0][0] == FieldType.PLAIN and len(processed_fields[0][1].strip()) != 0:
            self.add_message(self.INIT_BRIEF, node=node, args=self.class_name)
            index += 1
        # end if

        self._check_generic_params(node, processed_fields)

        return_info_in_docstring = list(filter(lambda x: x[0] in [FieldType.RETURN, FieldType.RTYPE], processed_fields))
        if len(return_info_in_docstring) > 0:
            self.add_message(self.INIT_WITH_RETURN, node=node, args=self.class_name)
        # end if

        self._check_raise(node, processed_fields)

        if format_errors:
            errors_str = self.concatenate_sub_errors(format_errors)
            self.add_message(self.INIT_FORMAT, node=node, args=(self.class_name, errors_str))
        # end if
    # end def _check_init_doc_format

    def _extract_method_fields(self, node):
        """
        parse a docstring to create a list of fields, with type information

        :param node: function node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.FunctionDef``

        :return: list of fields
        :rtype: ``list[tuple]``
        """
        fields = re_split(PATTERN_SPLIT_FIELDS, node.doc_node.value, maxsplit=0, flags=re_M)

        processed_fields = []
        for field in fields:
            if param_tag := re_findall(r"^\s*:param (\w+):", field):
                processed_fields.append((FieldType.PARAM, field, param_tag[0]))
            elif type_tag := re_findall(r"^\s*:type (\w+):", field):
                processed_fields.append((FieldType.TYPE, field, type_tag[0]))
            elif re_match(r"^\s*:return:", field):
                processed_fields.append((FieldType.RETURN, field))
            elif re_match(r"^\s*:rtype:", field):
                processed_fields.append((FieldType.RTYPE, field))
            elif raise_tag := re_findall(r"^\s*:raise (\S+):", field):
                processed_fields.append((FieldType.RAISE, field, raise_tag[0]))
            elif kwargs_tag := re_findall(r"^\s*:kwargs:", field):
                processed_fields.append((FieldType.KWARGS, field, kwargs_tag[0]))
            elif unsupported := re_findall(r"^\s*(:.*:)", field):
                self.add_message(self.UNSUPPORTED_FIELD, node=node, args=(self.class_name, node.name, unsupported[0]))
            else:
                processed_fields.append((FieldType.PLAIN, field))
            # end if
        # end for
        return processed_fields
    # end def _extract_method_fields

    def _check_global_format(self, node):
        """
        Check if the right quotes are applied

        :param node: node
        :type node: ``astroid.nodes.scoped_nodes.scoped_nodes.NodeNG``

        :return: list of format error sub errors that applies to all formating
        :rtype: ``list[str]``
        """
        start = node.doc_node.lineno - 1
        end = node.doc_node.end_lineno + 1

        self.raw = ' '.join(self.lines[start:end]).strip()

        if not self.raw.startswith('"""'):
            self.add_message(self.WRONG_QUOTE, node=node, args=node.name)
        # end if

        errors = []

        if not node.doc_node.value or node.doc_node.value[0] != "\n":
            errors.append(self.TXT_DOCSTRING_START)
        elif re_fullmatch(".*\n\s*", node.doc_node.value) and node.doc_node.value.strip("\n "):
            # the second condition ignore the warning on empty doc string as it causes repeated errors
            errors.append(self.TXT_DOCSTRING_END)
        # end if

        return errors
    # end def _check_global_format

    def _flatten_body(self, node):
        """
        flatten a node body field into statements at the same level, loose the hierarchical information
        but allows searching specific statements, does not look inside inner functions

        :param node: an astro node that has a body
        :type node: ``MultiLineBlockNode``

        :return: Generators of statements
        :rtype: ``Generator[astroid.nodes.NodeNG]``
        """

        inner_list = list(node.body) if hasattr(node, "body") else []

        if isinstance(node, If):
            inner_list.extend(node.orelse)
        elif isinstance(node, Try):
            inner_list.extend(node.handlers)
        elif isinstance(node, Match):
            inner_list.extend(node.cases)
        # end if
        for inner_node in inner_list:
            yield inner_node
            if ((hasattr(inner_node, "body") and not isinstance(inner_node, FunctionDef))
                    or isinstance(inner_node, NODES_TO_EXPEND)):
                yield from self._flatten_body(inner_node)
            # end if
        # end for
    # end def _flatten_body
# end class LogiDocstringChecker


def register(linter):
    """
    This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    :type linter: ``PyLinter``
    """
    linter.register_checker(LogiDocstringChecker(linter))
# end def register

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
