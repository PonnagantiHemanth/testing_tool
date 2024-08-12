#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Pylint Logi
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylint_logi.end_comment_checker
:brief: custom pylint checkers for pytestbox coding style
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/03/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import re

from collections import deque
from enum import Enum
from re import split
from token import COMMENT
from token import DEDENT
from token import INDENT
from token import NAME
from token import NEWLINE
from token import NL

from pylint.checkers import BaseTokenChecker

LIKELY_END_COMMENT = r"#( |)(end|if).*"

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
MISSING_END_COMMENT = "E5401"
WRONG_END_COMMENT = "E5402"
END_COMMENT_TOO_EARLY = "E5403"

MISSING_END_COMMENT_SYMBOL = "end-comment-missing"
WRONG_END_COMMENT_SYMBOL = "end-comment-no-match"
END_COMMENT_TOO_EARLY_SYMBOL = "end-comment-too-early"

LEN_END_DEF = len("# end def ")

INDENT_LENGTH = 4  # In number of spaces, indentation is done with spaces and not tabulation


class IndentType(Enum):
    """
    Enum indents
    """
    CLASS_INDENT = "class"
    DEF_INDENT = "def"
    ASYNC_INDENT = "async"
    IF_INDENT = "if"
    TRY_INDENT = "try"
    FOR_INDENT = "for"
    WHILE_INDENT = "while"
    WITH_INDENT = "with"
    MATCH_INDENT = "match"
    CASE_INDENT = "case"

    def __repr__(self):
        return self.value
    # end def __repr__
# end class IndentType


# sub indent at the same level as main indent
SUB_INDENTS = ["else", "elif", "except", "finally", "case"]

# indents that start a block without a matching end comment
IGNORED_INDENTS = [IndentType.CASE_INDENT]

IGNORED_SUPER_INDENTS = [IndentType.MATCH_INDENT]

COMPREHENSION_LEVEL_IN = ['[', '{', '(']
COMPREHENSION_LEVEL_OUT = [']', '}', ')']

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
def get_indent_level(token):
    """
    get the level of indent from a token

    :param token: Token to check
    :type token: ``TokenInfo``
    :return: level of indentation
    :rtype: ``int``
    """
    if token.type == INDENT:
        return int(len(token.string) / INDENT_LENGTH)
    else:
        line = token.line
        return int((len(line)-len(line.lstrip())) / INDENT_LENGTH)
    # end if
# end def get_indent_level


class EndCommentChecker(BaseTokenChecker):
    """
    Pylint checker verifying end comments of indents
    """
    name = "end-comments"
    msgs = {
        MISSING_END_COMMENT: (
            "End comment missing, expected ``%s``",
            MISSING_END_COMMENT_SYMBOL,
            "All indented blocks should have an end comment",
        ),
        WRONG_END_COMMENT: (
            "End comment doesn't match block, expected ``%s``",
            WRONG_END_COMMENT_SYMBOL,
            "All end comments should match the name of their indent block",
        ),
        END_COMMENT_TOO_EARLY: (
            "End comment appears too early for block ``%s``",
            END_COMMENT_TOO_EARLY_SYMBOL,
            "All an end comments should match the name of their indent block",
        ),
    }

    def __init__(self, linter=None):
        """
        :param linter: linter used - OPTIONAL
        :type linter: ``Linter`` or ``None``
        """
        BaseTokenChecker.__init__(self, linter)
        self.message_list = []
        self.sub_indent_group_stack = deque()
        self.tokens_to_confirm = dict()
        self.sub_indents_seen = dict()
    # end def __init__

    def process_tokens(self, tokens):
        """
        perform the check of end comment presence in a list of tokens

        :param tokens: List of python tokens to process
        :type tokens: ``list[TokenInfo]``
        """

        start_new_line = True
        in_list_comprehension_level = 0
        indent_level = -1
        indent_stack = deque()

        self.sub_indent_group_stack = deque()
        self.tokens_to_confirm = dict()
        self.sub_indents_seen = dict()
        for token in tokens:
            # consider the numbers of [ and ] to determine if the following tokens are inside a list comprehension
            if token.string in COMPREHENSION_LEVEL_IN:
                in_list_comprehension_level += 1
            elif token.string in COMPREHENSION_LEVEL_OUT:
                in_list_comprehension_level -= 1
            # end if

            if token.type in [NEWLINE, NL]:
                start_new_line = True
                indent_level = -1
            elif token.type in [INDENT, DEDENT]:
                indent_level = get_indent_level(token)
            elif start_new_line:  # only check for new indents block at the start of a new line
                start_new_line = False
                # bypass the check if we are in a list comprehension
                if in_list_comprehension_level > 0:
                    continue
                # end if

                if indent_level == -1:
                    indent_level = get_indent_level(token)
                # end if

                if self.sub_indent_group_stack and token.string not in SUB_INDENTS and \
                        ((self.sub_indent_group_stack[-1] == indent_level and token.type != COMMENT) or
                        self.sub_indent_group_stack[-1] > indent_level):
                    level = self.sub_indent_group_stack.pop()
                    self._confirm_token(level, token.start[0], top_type.value)
                    if indent_stack and indent_stack[-1][0] in [IndentType.IF_INDENT, IndentType.TRY_INDENT, IndentType.MATCH_INDENT]:
                        indent_stack.pop()
                    # end if
                # end if

                if (self.sub_indent_group_stack and token.type == NAME
                        and self.sub_indent_group_stack[-1] in [indent_level, indent_level - 1]
                        and token.string in SUB_INDENTS):
                    self.sub_indents_seen[self.sub_indent_group_stack[-1]].append(token.start[0])
                # end if

                if indent_level >= len(indent_stack):
                    if token.type == NAME:

                        for indent_type in IndentType:
                            if token.string == indent_type.value:
                                indent_stack.append((indent_type, token.line, indent_level))
                                if indent_type in [IndentType.IF_INDENT, IndentType.TRY_INDENT, IndentType.MATCH_INDENT]:
                                    self.sub_indent_group_stack.append(indent_level)
                                    self.tokens_to_confirm[indent_level] = []
                                    self.sub_indents_seen[indent_level] = []
                                # end if
                                break
                            # end if
                        # end for
                    # end if
                elif len(indent_stack) > 0:
                    top_indent = indent_stack.pop()

                    top_type, top_line, top_level = top_indent

                    if top_type in IGNORED_INDENTS:
                        # check if a new indent is here
                        if token.type == NAME:
                            for indent_type in IndentType:
                                if token.string == indent_type.value:
                                    indent_stack.append((indent_type, token.line, indent_level))
                                    break
                                # end if
                            # end for
                            continue
                        # end if

                        # check if further tests are needed
                        if token.type == COMMENT:
                            # this might be an end comment for the next level, check if that's the case
                            top_indent = indent_stack.pop()
                            top_type, top_line, top_level = top_indent
                            adjusted_indent_level = indent_level if top_type != IndentType.CASE_INDENT \
                                else indent_level - 1
                            if (self.sub_indent_group_stack
                                and self.sub_indent_group_stack[-1] == adjusted_indent_level):
                                self.validate_comment(indent_level, False, token, top_line, top_type)
                                indent_stack.append(top_indent)
                                continue
                            # end if
                        # end if
                    elif indent_stack and top_type in IGNORED_SUPER_INDENTS:
                        top_indent = indent_stack.pop()
                        top_type, top_line, top_level = top_indent

                    # end if

                    if token.type == COMMENT and indent_level == top_level:
                        if self.sub_indent_group_stack and self.sub_indent_group_stack[-1] == indent_level:
                            notify = False
                        else:
                            notify = True
                        # end if
                        self.validate_comment(indent_level, notify, token, top_line, top_type)
                        if top_type in [IndentType.IF_INDENT, IndentType.TRY_INDENT, IndentType.MATCH_INDENT]:
                            indent_stack.append(top_indent)
                        # end if
                    elif token.type == COMMENT and indent_level == top_level + 1 and top_type == IndentType.MATCH_INDENT:
                        notify = False
                        self.validate_comment(indent_level-1, notify, token, top_line, top_type)
                    elif token.type == NAME and token.string in SUB_INDENTS:
                        indent_stack.append(top_indent)
                    elif top_type not in IGNORED_INDENTS:
                        if top_type in [IndentType.IF_INDENT, IndentType.TRY_INDENT, IndentType.MATCH_INDENT]:
                            indent_stack.append(top_indent)
                        # end if
                        self._store_messages('end-comment-missing',
                                             line=token.start[0],
                                             argument=self._get_expected_end_comment(top_line, top_type)[0])
                    # end if
                # end if
            # end if
        # end for

        # confirm the tokens that were not yet confirmed
        while self.sub_indent_group_stack:
            indent_level = self.sub_indent_group_stack.pop()
            self._confirm_token(indent_level, token.line, "<unknown>")
        # end while
        # sort the messages by line number
        self.message_list.sort(key=lambda x: x[1])
        for (msgid, line, arguments) in self.message_list:
            self.add_message(msgid, line=line, args=arguments)
        # end for
        self.message_list = []
    # end def process_tokens

    def validate_comment(self, indent_level, notify, token, top_line, top_type):
        """
        Validate a current comment if matches the expected end comment

        :param indent_level: level of the indent
        :type indent_level: ``int``
        :param notify: Flag indicating if the error is immediately added to the notification
            or if further checks are needed
        :type notify: ``bool``
        :param token: Token to check
        :type token: ``TokenInfo``
        :param top_line: line of the top indent
        :type top_line: ``str``
        :param top_type: type of the top indent
        :type top_type: ``IndentType``
        """
        matches = self._get_expected_end_comment(top_line, top_type)
        is_wrong = token.string not in matches
        if notify and is_wrong:
            self._store_messages('end-comment-no-match', line=token.start[0], argument=matches[0])
        elif not notify:
            # to confirm later
            self.tokens_to_confirm[indent_level].append((token, is_wrong, matches))
        # end if
    # end def validate_comment

    @staticmethod
    def _get_expected_end_comment(top_line, top_type):
        """
        get the expected end comment for a given indent

        :param top_line: line of the top indent
        :type top_line: ``str``
        :param top_type: type of the top indent
        :type top_type: ``IndentType``

        :return: list of expected end comments values
        :rtype: ``list[str]``
        """
        if top_type in [IndentType.DEF_INDENT, IndentType.ASYNC_INDENT, IndentType.CLASS_INDENT]:
            line = split('[(:]', top_line)[0].strip()
            if line.startswith(IndentType.ASYNC_INDENT.value):
                line = line[len(IndentType.ASYNC_INDENT.value):].strip()
            # end if
            raw_match = f"# end {line}"
            matches = [raw_match, ]

            if top_type == IndentType.DEF_INDENT:
                # add option to support getter and setter of property end comment, these are additional
                # correct option so will cause a false negative when used on methods
                # that aren't linked to a property
                ""
                matches.append(raw_match[:LEN_END_DEF] + "property getter " + raw_match[LEN_END_DEF:])
                matches.append(raw_match[:LEN_END_DEF] + "property setter " + raw_match[LEN_END_DEF:])
            # end if
        else:
            matches = [f"# end {top_type.value}", ]
        # end if
        return matches
    # end def _get_expected_end_comment

    def _confirm_token(self, indent_level, line, top_type):
        """
        Confirm all pending tokens for a given sub indent group and check if they are correct

        :param indent_level: level of the indent
        :type indent_level: ``int``
        :param line: line number
        :type line: ``int``
        :param top_type: type of the top indent
        :type top_type: ``str``
        """
        tokens_to_confirm_for_this = self.tokens_to_confirm.pop(indent_level)
        sub_indents_seen_for_this = self.sub_indents_seen.pop(indent_level)

        if not tokens_to_confirm_for_this:
            self._store_messages('end-comment-missing', line=line, argument=f"# end {top_type}")
        # end if

        end_comment_seen = False
        for token_to_confirm, is_wrong, matches in tokens_to_confirm_for_this:
            line_start = token_to_confirm.start[0]

            count_after = len([subs for subs in sub_indents_seen_for_this if subs > line_start])
            likely_an_end_comment = re.match(LIKELY_END_COMMENT, token_to_confirm.string)

            if likely_an_end_comment and count_after > 0:
                self._store_messages('end-comment-too-early', line=token_to_confirm.start[0], argument=top_type)
            elif is_wrong and likely_an_end_comment:
                self._store_messages('end-comment-no-match', line=token_to_confirm.start[0], argument=matches)
            else:
                end_comment_seen = True
            # end if
        # end for
    # end def _confirm_token

    def _store_messages(self, msgid, line, argument):
        """
        store a message to be added later

        :param msgid: message id
        :type msgid: ``str``
        :param line: line number
        :type line: ``int``
        :param argument: text to add to the message
        :type argument: ``str`` or ``tuple[str]``
        """
        self.message_list.append((msgid, line, argument))
    # end def _store_messages
# end class EndCommentChecker


def register(linter):
    """
    This required method auto registers the checker during initialization.
    
    :param linter: The linter to register the checker to.
    :type linter: ``PyLinter``
    """
    linter.register_checker(EndCommentChecker(linter))
# end def register
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
