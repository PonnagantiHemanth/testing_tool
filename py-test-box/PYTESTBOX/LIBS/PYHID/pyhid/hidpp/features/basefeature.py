#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features
    :brief: HID++ 2.0 Feature Model, Factory and Interface base classes
    :author: Martin Cryonnet
    :date: 2020/02/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class FeatureModel(object):
    """
    Feature's simplified model view controller
    """
    @classmethod
    def _get_data_model(cls):
        """
        Feature's data model

        Empty example:
            {
                "feature_base": None,
                "versions": {
                    1: {
                        "main_cls": None,
                        "api": {
                            "functions": {
                                0: {"request": None, "response": None},
                            }
                        },
                    },
                    2: {
                        "main_cls": None,
                        "api": {
                            "functions": {
                                0: {"request": None, "response": None},
                                1: {"request": None, "response": None},
                            }
                            "events": {
                               0: {"report": None}
                            }
                        },
                    },
                }
            }
        """
        raise NotImplementedError(f"Feature data model not defined")
    # end def _get_data_model

    @classmethod
    def get_available_responses_classes(cls):
        return_responses = []
        for version_data in cls._get_data_model()["versions"].values():
            for interface in version_data["api"]["functions"].values():
                if interface["response"] is not None and interface["response"] not in return_responses:
                    return_responses.append(interface["response"])
                # end if
            # end for
        # end for
        return tuple(return_responses)
    # end def get_available_responses_classes

    @classmethod
    def get_available_responses_map(cls):
        return_map = {}
        for available_response_cls in cls.get_available_responses_classes():
            return_map[(available_response_cls.FEATURE_ID, available_response_cls.VERSION,
                        available_response_cls.FUNCTION_INDEX)] = available_response_cls
        # end for
        return return_map
    # end def get_available_responses_map

    @classmethod
    def get_available_events_classes(cls):
        return_responses = []
        for version_data in cls._get_data_model()["versions"].values():
            for interface in version_data["api"]["events"].values():
                if interface["report"] not in return_responses:
                    return_responses.append(interface["report"])
                # end if
            # end for
        # end for
        return tuple(return_responses)
    # end def get_available_events_classes

    @classmethod
    def get_available_events_map(cls):
        return_map = {}
        for available_event_cls in cls.get_available_events_classes():
            return_map[(available_event_cls.FEATURE_ID, available_event_cls.VERSION,
                        available_event_cls.FUNCTION_INDEX)] = available_event_cls
        # end for
        return return_map
    # end def get_available_events_map

    @classmethod
    def get_base_cls(cls):
        return cls._get_data_model()["feature_base"]
    # end def get_base_cls

    @classmethod
    def get_main_cls(cls, version):
        if version in cls._get_data_model()["versions"]:
            return cls._get_data_model()["versions"][version]["main_cls"]
        else:
            raise KeyError(f'Version {version} not supported')
        # end if
    # end def get_main_cls

    @classmethod
    def get_request_cls(cls, version, function_index):
        return cls.get_function_cls(version, function_index, "request")
    # end def get_request_cls

    @classmethod
    def get_response_cls(cls, version, function_index):
        return cls.get_function_cls(version, function_index, "response")
    # end def get_request_cls

    @classmethod
    def get_function_cls(cls, version, function_index, msg_type):
        try:
            return cls._get_data_model()["versions"][version]["api"]["functions"][function_index][msg_type]
        except IndexError:
            return None
        # end try
    # end def get_function_cls

    @classmethod
    def get_report_cls(cls, version, event_index):
        return cls.get_event_cls(version, event_index, "report")
    # end def get_request_cls

    @classmethod
    def get_event_cls(cls, version, event_index, msg_type):
        try:
            return cls._get_data_model()["versions"][version]["api"]["events"][event_index][msg_type]
        except IndexError:
            return None
        # end try
    # end def get_event_cls
# end class FeatureModel


class FeatureFactory(object):
    """
    Feature factory creates an object from a given version
    """
    @staticmethod
    def create(version):
        """
        A create method shall be implemented in each factory
        """
        raise NotImplementedError("Feature factory create method not implemented")
    # end def create
# end class FeatureFactory


class FeatureInterface(object):
    """
    Interface to feature
    """
    VERSION = None

    def __getattribute__(self, item):
        """
        Raise a Not Implemented Error if an attribute defined in the interface is not defined
        """
        value = super().__getattribute__(item)
        if value is not None:
            return value
        else:
            raise NotImplementedError(f"{item} not implemented in current version {self.VERSION}")
    # end def __getattribute__

    def get_max_function_index(self):
        """
        Get the max function index, which should be defined for each feature
        """
        raise NotImplementedError("Max function index getter not implemented in current version")
    # end def get_max_function_index

# end class FeatureInterface

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
