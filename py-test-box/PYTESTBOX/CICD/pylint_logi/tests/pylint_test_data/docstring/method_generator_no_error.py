#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: method_generator_no_error
:brief: Sample code where the return statement is from a yield statement, without errors
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/06/28
"""
from astroid import FunctionDef
from astroid import If
from astroid import Match
from astroid import Try

NODES_TO_EXPEND = (If, Try, Match)


def _flatten_body(node):
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
    i = 0
    for inner_node in inner_list:
        yield inner_node
        if ((hasattr(inner_node, "body") and not isinstance(inner_node, FunctionDef))
                or isinstance(inner_node, NODES_TO_EXPEND)):
            yield from _flatten_body(inner_node)
        # end if
    # end for
# end def _flatten_body
