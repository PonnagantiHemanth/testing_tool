#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: settingsexplorer.model
:brief: Settings Explorer Data Model
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/04/12
"""


# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import tokenize
from enum import Enum
from enum import auto
from os import listdir
from os.path import dirname
from os.path import join
from os.path import relpath
from pathlib import Path

from settingsexplorer.constants import PYTESTBOX_BASE_FOLDER
from settingsexplorer.utils import CaseSensitiveConfigParser


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
class ScanningStates(Enum):
    """
        State for the feature source code parser
        """
    INITIAL = auto()
    LOOKING_FOR_INIT = auto()
    VALIDATING_INIT = auto()
    LOOKING_FOR_NEW_SUB_NAME = auto()
    COMPILING_COMMENTS = auto()
    GET_NAME = auto()
    ADDING_DEFAULTS = auto()
    ADDING_MULTILINE_DEFAULTS_DETECT_NEW_LINE = auto()
    ADDING_MULTILINE_DEFAULTS_NEW_LINE = auto()
    LOOKING_FOR_NEXT_SUB = auto()
# end class ScanningStates


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConfigurationModel:
    """
    Data model in the Model-View-Controller design pattern
    """
    def __init__(self):
        self.filename = ""
        self.root_path = ""
        # Base config parser representing the top file
        self.base_config = None
        # Config dictionary of the current hierarchy of config
        self.config_dict = {}
        self._default_config = None
        self.ini_files = []
        self._features_comments = None
        self._features_default_dict = {}
        self._current_comment_stack = []
        self._error_pytestbox_files = False
        self._parsing_errors = []
        self.model_error_callback = None
        self.parsing_error_callback = None
    # end def __init__

    @property
    def default_config(self):
        """
        Property getter of ``default_config``
        gather the default features and comments if not existing

        :return: ``default_config`` value
        :rtype: ``ConfigParser``
        """
        if self._default_config is None:
            self.gather_features_comments_and_defaults()
        # end if
        return self._default_config
    # end def default_config

    @property
    def features_comments(self):
        """
        Property getter of ``features_comments``
        gather the default features and comments if not existing

        :return: ``default_config`` value
        :rtype: ``ConfigParser``
        """
        if self._features_comments is None:
            self.gather_features_comments_and_defaults()
        # end if
        return self._features_comments
    # end def features_comments

    @property
    def error_pytestbox_files(self):
        """
        Property getter of ``error_pytestbox_files``,
        the flag indicating an error on finding pytestbox files

        :return: ``error_pytestbox_files`` value
        :rtype: ``bool``
        """
        return self._error_pytestbox_files
    # end def property getter error_pytestbox_files

    @error_pytestbox_files.setter
    def error_pytestbox_files(self, value):
        """
        Property getter of ``error_pytestbox_files``,
        the flag indicating an error on finding pytestbox files

        :param value: ``error_pytestbox_files`` value
        :type value: ``bool``
        """
        self._error_pytestbox_files = value
        self.model_error()
    # end def property setter error_pytestbox_files

    @property
    def parsing_errors(self):
        """
        Property getter of ``parsing_errors``
        list of parsing error errors from features.py files

        :return: List of string for each error
        :rtype: ``list[str]``
        """
        return self._parsing_errors
    # end def property getter parsing_errors

    def add_section(self, config, config_dict, section=''):
        """
        Add a section taken from a config dict into a config parser object

        :param config: Config parser object to add the section into
        :type config: ``ConfigParser``
        :param config_dict: Config dictionary containing the section to add
        :type config_dict: ``dict``
        :param section: Name of the section where to add the config dict, for subsection in recursive calls - OPTIONAL
        :type section: ``str``
        """
        for key, value in config_dict.items():
            if isinstance(value, dict):
                self.add_section(config, value, section + '/' + key)
            else:
                section_name = section.removeprefix("/")
                if not config.has_section(section_name) and section_name != '':
                    config.add_section(section_name)
                # end if
                config.set(section_name, key.removeprefix("F_"), str(value))
            # end if
        # end for
    # end def add_section

    def set_filename(self, filename):
        """
        Set filename, if changed it will invalid the current model

        :param filename: Filename
        :type filename: ``str``
        """
        if filename:
            self.filename = filename
            self.invalid_model()
        # end if
    # end def set_filename

    def invalid_model(self):
        """
        Invalid the currently set model cache
        """
        self.base_config = None
        self.config_dict = {}
        self._default_config = None
        self.ini_files = []
        self._features_comments = None
        self._features_default_dict = {}
        self._current_comment_stack = []
    # end def invalid_model

    def gather_features_comments_and_defaults(self):
        """
        Gather information on feature's comments and defaults by parsing features.py located in the same project
        as the root folder
        """
        self._parsing_errors = []

        path = self.find_py_test_box_root()
        self._default_config = CaseSensitiveConfigParser()
        self._features_comments = {}

        if path is not None:
            paths = path.rglob("features.py")

            for path in paths:
                self.parse_features_file(path.absolute())
            # end for
            if self.parsing_error_callback is not None:
                self.parsing_error_callback()
            # end if
            self.error_pytestbox_files = False
        else:
            self.error_pytestbox_files = True
        # end if
    # end def gather_features_comments_and_defaults

    def find_py_test_box_root(self):
        """
        Find root of pytestbox below root path if exists

        examples:
            for the current root path:
                some/local/path/PYTESTBOX/TESTS/SETTINGS/PYTESTBOX/PRODUCT/QUARK/PLATFORM/HEAD
            returns:
                some/local/path/PYTESTBOX

            for the current root path:
                some/path/completely/unrelated
            returns:
                None

        :return: root path of pytextbox or None if
        :rtype: ``Path`` or ``None``
        """
        root_path = Path(self.root_path)
        if root_path.name == PYTESTBOX_BASE_FOLDER and not self._is_pytestbox_in_path(root_path):
            return root_path
        # end if

        for path in root_path.resolve().parents:
            if path.name == PYTESTBOX_BASE_FOLDER and not self._is_pytestbox_in_path(path):
                return path
            # end if
        # end for
        return None
    # end def find_py_test_box_root

    @staticmethod
    def _is_pytestbox_in_path(path):
        """
        Compute if parent's have repeated pytestbox path,

        :param path: File's path
        :type path: ``Path``

        :return: flag indicating if PYTESTBOX pattern was found in the given path
        :rtype: ``bool``
        """
        return PYTESTBOX_BASE_FOLDER in str(path.resolve().parent)
    # end def _is_pytestbox_in_path

    def parse_features_file(self, path):
        """
        Parse a feature file

        :param path: File's path
        :type path: ``Path``
        """

        # Root file has a NONE submodule it's not good for parsing, ignored for now
        # autotest file is not used for pytestbox and so not used for parsing. Ignored
        # Possible improvement, a setting file where ignored paths are added
        if (path.match(r"PYTESTBOX\TESTS\TESTSUITES\features.py")
                or path.match(r"PYTESTBOX\TESTS\TESTSUITES\autotests\base\features.py")):
            return
        # end if

        self._features_default_dict = {}
        with tokenize.open(path) as features_file:
            tokens = tokenize.generate_tokens(features_file.readline)
            state = ScanningStates.INITIAL
            current_name_stack = []
            self._current_comment_stack = []
            for token in tokens:
                token_type = token.type
                token_string = token.string
                match state:
                    case ScanningStates.INITIAL | ScanningStates.LOOKING_FOR_NEXT_SUB:
                        if token_type == tokenize.NAME and token_string == "class":
                            state = ScanningStates.LOOKING_FOR_INIT
                        elif token_type == tokenize.COMMENT and token_string.startswith("# end class"):
                            current_name_stack.pop(-1)
                        # end if
                    case ScanningStates.LOOKING_FOR_INIT:
                        if token_type == tokenize.NAME and token_string == "def":
                            state = ScanningStates.VALIDATING_INIT
                        # end if
                    case ScanningStates.VALIDATING_INIT:
                        if token_type == tokenize.NAME and token_string == "__init__":
                            state = ScanningStates.LOOKING_FOR_NEW_SUB_NAME
                        else:
                            state = ScanningStates.LOOKING_FOR_INIT
                        # end if
                    case ScanningStates.LOOKING_FOR_NEW_SUB_NAME:
                        if token_type == tokenize.STRING and not token_string.startswith('"""'):  # ignore docstrings
                            subsystem_name = token_string.strip("\"'")
                            current_name_stack.append(subsystem_name)
                            self._current_comment_stack.clear()
                            state = ScanningStates.COMPILING_COMMENTS
                        elif token_type == tokenize.NAME and token_string == "None":
                            current_name_stack.append(None)
                            self._current_comment_stack.clear()
                            state = ScanningStates.COMPILING_COMMENTS
                        # end if
                    case ScanningStates.COMPILING_COMMENTS:
                        if token_type == tokenize.COMMENT:
                            if token_string.startswith("# end def"):
                                state = ScanningStates.LOOKING_FOR_NEXT_SUB
                            else:
                                self._current_comment_stack.append(token_string.removeprefix("# "))
                            # end if
                        elif token_type == tokenize.NAME and token_string == "self":
                            state = ScanningStates.GET_NAME
                        elif token_type == tokenize.NAME and token_string == "class":
                            self._parsing_errors.append(f"line '{token.line}' start a class before end of init")
                            state = ScanningStates.LOOKING_FOR_INIT
                        # end if
                    case ScanningStates.GET_NAME:
                        if token_type == tokenize.NAME:
                            if token_string.startswith("F_"):
                                name = token_string.removeprefix("F_")
                                path = ""
                                for n in current_name_stack + [name]:
                                    if n is not None:
                                        path += "/" + n
                                    # end if
                                # end for
                                path = path.lstrip("/")

                                self._features_comments[path] = "\n".join(self._current_comment_stack)
                                self._current_comment_stack = []
                                state = ScanningStates.ADDING_DEFAULTS
                            else:
                                self._current_comment_stack.clear()
                                state = ScanningStates.COMPILING_COMMENTS
                            # end if
                        # end if
                    case ScanningStates.ADDING_DEFAULTS:
                        if token_string == "=":
                            line_split = token.line.split("=")
                            if len(line_split) != 2:
                                self._parsing_errors.append(f"line '{token.line}' has two equal signs")
                                pass
                            # end if
                            default_value = line_split[1].strip()
                            state = self.state_choice_multiline(default_value, name, current_name_stack)
                        else:
                            self._parsing_errors.append(
                                f"line '{token.line}' doesn't have equal sign in expected place")
                            self._current_comment_stack.clear()
                            state = ScanningStates.COMPILING_COMMENTS
                        # end if
                    case ScanningStates.ADDING_MULTILINE_DEFAULTS_DETECT_NEW_LINE:
                        if token_type in [tokenize.NEWLINE, tokenize.NL]:
                            state = ScanningStates.ADDING_MULTILINE_DEFAULTS_NEW_LINE
                        elif token_type == tokenize.NAME and token_string == "self":
                            self._parsing_errors.append(f"line `{token.line}` is still looking for the end "
                                                        f"of previous multi line default value")
                            state = ScanningStates.GET_NAME
                        elif token_type == tokenize.COMMENT and token_string.startswith("# end def"):
                            self._parsing_errors.append(f"line `{token.line}` is still looking for the end "
                                                        f"of previous multi line default value")
                            state = ScanningStates.LOOKING_FOR_NEXT_SUB
                        # end if
                    case ScanningStates.ADDING_MULTILINE_DEFAULTS_NEW_LINE:
                        default_value += (token.line.strip())
                        state = self.state_choice_multiline(default_value, name, current_name_stack)
                    case _:
                        raise NotImplementedError
                # end match
            # end for
        # end with
        self.add_section(self._default_config, self._features_default_dict)
    # end def parse_features_file

    def state_choice_multiline(self, default_value, name, current_name_stack):
        """
        Choose the next state depending on the multiline status of default

        :return: the next state to use
        :rtype: ``ScanningStates``
        """
        if default_value.strip() == "\\":
            return ScanningStates.ADDING_MULTILINE_DEFAULTS_DETECT_NEW_LINE
        # end if

        number_open_parentheses = default_value.count("(") + default_value.count("[")
        number_close_parentheses = default_value.count(")") + default_value.count("]")
        if number_open_parentheses > number_close_parentheses:
            state = ScanningStates.ADDING_MULTILINE_DEFAULTS_DETECT_NEW_LINE
        else:
            dictionary = self._features_default_dict
            for subsystem in current_name_stack:
                if subsystem is None:
                    continue
                # end if
                if subsystem not in dictionary.keys():
                    dictionary[subsystem] = {}
                # end if
                dictionary = dictionary[subsystem]
            # end for
            dictionary[name] = default_value
            self._current_comment_stack.clear()
            state = ScanningStates.COMPILING_COMMENTS
        # end if
        return state
    # end def state_choice_multiline

    def relative_path(self, path):
        """
        Get path relative to model's root path

        :return: Relative path
        :rtype: ``LiteralString``
        """
        if not Path:
            return r""
        # end if
        if not self.root_path:
            return path
        # end if

        return relpath(path, self.root_path)
    # end def relative_path

    def update_model(self, include_hierarchy_status, include_default_status):
        """
        Update data model

        :param include_hierarchy_status: Status of the include hierarchy option
        :type include_hierarchy_status: ``bool``
        :param include_default_status: Status of the include default option
        :type include_default_status: ``bool``

        :return: Configuration data model as a dictionary, ``None`` is returned if not filename has been given
        :rtype: ``dict`` or ``None``
        """
        if self.filename:
            if include_hierarchy_status:
                self.config_dict = self._include_hierarchy()
                if include_default_status:
                    self.config_dict = self.config_to_dict(self.default_config, self.config_dict, "Default")
                # end if
            else:
                self.config_dict = self._exclude_hierarchy()
            # end if
        # end if
        return self.config_dict
    # end def update_model

    def _include_hierarchy(self):
        """
        Include hierarchy in the data model

        :return: Configuration data model as a dictionary
        :rtype: ``dict``
        """
        ini_file = self.filename
        cur_dir = dirname(self.filename)
        config_dict = {}

        while ini_file:
            list_files = listdir(cur_dir)
            cur_ini_files = [file_in_dir for file_in_dir in list_files if file_in_dir.endswith(".settings.ini")]
            if len(cur_ini_files) == 0:
                break
            elif len(cur_ini_files) == 1:
                ini_file = join(cur_dir, cur_ini_files[0])
                self.ini_files.append(ini_file)
                cur_dir = dirname(cur_dir)
                if ini_file == self.filename and self.base_config is not None:
                    config = self.base_config
                else:
                    config = self.read_config_file(ini_file)
                # end if
                config_dict = self.config_to_dict(config, config_dict, self.relative_path(ini_file))
            else:
                raise KeyError(f"Too many .ini files found : {len(cur_ini_files)} files found")
            # end if
        # end while
        return config_dict
    # end def _include_hierarchy

    def _exclude_hierarchy(self):
        """
        Exclude hierarchy in the data model

        :return: Configuration data model as a dictionary
        :rtype: ``dict``
        """
        self.ini_files = []
        self.base_config = self.read_config_file(self.filename) if self.base_config is None else self.base_config
        config_dict = self.config_to_dict(self.base_config, source=self.relative_path(self.filename))
        return config_dict
    # end def _exclude_hierarchy

    def model_error(self):
        """
        Send callback of model error
        """
        if self.model_error_callback is not None:
            self.model_error_callback()
        # end if
    # end def model_error

    @staticmethod
    def read_config_file(config_file):
        """
        Read configuration file

        :param config_file: Configuration file name
        :type config_file: ``str``

        :return: Returns configuration read from file
        :rtype: ``ConfigParser``
        """
        config = CaseSensitiveConfigParser()
        config.read(config_file)
        return config
    # end def read_config_file

    @staticmethod
    def config_to_dict(config, config_dict=None, source=""):
        """
        Configuration to dictionary data model

        :param config: Configuration
        :type config: ``ConfigParser``
        :param config_dict: Configuration dictionary - OPTIONAL
        :type config_dict: ``dict``  or ``None``
        :param source: Name of the source of the config. It can be a path or "Default" - OPTIONAL
        :type source: ``str``

        :return: Configuration data model as a dictionary
        :rtype: ``dict``
        """
        config_dict = {} if config_dict is None else config_dict
        for section in config.sections():
            current_dict = config_dict
            for level in section.split('/'):
                if level not in current_dict.keys():
                    current_dict[level] = {}
                # end if
                current_dict = current_dict[level]
            # end for
            for key, values in config.items(section, raw=True):
                if key not in current_dict:
                    current_dict[key] = (values, source)
                # end if
            # end for
        # end for
        return config_dict
    # end def config_to_dict
# end class ConfigurationModel

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
