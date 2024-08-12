#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.hiddispatcher
:brief: Generator for hid dispatcher values
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.generator.common import CommonFileGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.templates import HidDispatcherTemplate


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class HidDispatcherGenerator(CommonFileGenerator):
    """
    Generate ``HidDispatcher`` section
    """

    def process(self):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        feature_table = Template(HidDispatcherTemplate.GET_FEATURE_TABLE).substitute(dictionary)
        event_table = ""
        if len(AutoInput.EVENT_LIST) > 0:
            event_table = Template(HidDispatcherTemplate.GET_EVENT_TABLE).substitute(dictionary)
        # end if
        dictionary["InitFunction"] = Template(HidDispatcherTemplate.GET_INIT_FUNCTION).substitute(
            dict(FeatureTable=feature_table, EventTable=event_table)
        )
        response_queue = Template(HidDispatcherTemplate.GET_RESPONSE_QUEUE).substitute(dictionary)
        event_queue = ""
        if len(AutoInput.EVENT_LIST) > 0:
            event_queue = Template(HidDispatcherTemplate.GET_EVENT_QUEUE).substitute(dictionary)
        # end if
        dictionary["InitFeatureMessageQueues"] = Template(HidDispatcherTemplate.GET_INIT_FEATURE_MESSAGE_QUEUES) \
            .substitute(dict(ResponseQueue=response_queue, EventQueue=event_queue))

        self.update_implementation_section(
            [Template(HidDispatcherTemplate.GET_HID_DISPATCHER).substitute(dictionary)])
    # end def process
# end class HidDispatcherGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
