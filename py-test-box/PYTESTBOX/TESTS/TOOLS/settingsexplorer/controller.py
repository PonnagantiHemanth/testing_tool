#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: settingsexplorer.controller
:brief: Settings Explorer application controller
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/04/12
"""


# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import tkinter as tk
from json import JSONDecodeError
from json import dump
from json import load
from os.path import abspath
from os.path import curdir
from os.path import exists
from pathlib import Path
from tkinter import filedialog

from settingsexplorer.constants import EDIT_MODE_ENABLED
from settingsexplorer.constants import PERSISTENT_FILE_NAME
from settingsexplorer.utils import extract_section_dict


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConfigurationController:
    """
    Controller between the view and the model in the Model-View-Controller design pattern
    """
    def __init__(self, model, view, filename="", root_path=""):
        """
        :param model: Configuration model
        :type model: ``PYTESTBOX.TESTS.TOOLS.settingsexplorer.model.ConfigurationModel``
        :param view: Configuration view
        :type view: ``PYTESTBOX.TESTS.TOOLS.settingsexplorer.view.ConfigurationView``
        :param filename: Settings filename
        :type filename: ``str``
        :param root_path: Root directory path
        :type root_path: ``str``
        """
        self.model = model
        self.view = view

        self.model.model_error_callback = self.model_error_callback
        self.model.parsing_error_callback = self.parsing_error_callback

        self.include_hierarchy_status = None
        self.include_default_status = None
        self.section = None
        self.key = None
        self.filled_keys = []
        # TODO : should it be here ?
        self.entry = None
        self.top = None

        self.bind_view_events_and_commands()
        self.add_buttons()
        self.load_persistence()
        self.model.set_filename(filename if (filename is not None and filename.endswith(".settings.ini")) else "")
        self.model.root_path = root_path if root_path else self.model.root_path
        self.view.root_folder_label_text.set(self.model.root_path)
        self.update_all()
    # end def __init__

    def bind_view_events_and_commands(self):
        """
        Add commands
        """
        self.view.file_menu.add_command(label="Open", command=self.select_file)
        if EDIT_MODE_ENABLED:
            self.view.file_menu.add_command(label="Save", command=self.save)
            self.view.file_menu.add_command(label="Save As...", command=self.save_as)
        # end if
        self.view.file_menu.add_command(label="Exit", command=self.on_exit)

        # Bind event to select node
        self.view.tree_view.bind('<<TreeviewSelect>>', self.select_node)
        self.view.list_view.bind('<<TreeviewSelect>>', self.select_line)

        # Add checkboxes
        self.include_hierarchy_status = tk.BooleanVar()
        self.include_default_status = tk.BooleanVar()
        self.view.add_checkboxes([self.include_hierarchy_status, self.include_default_status],
                                 [self.update_all, self.update_all])

        # Bind exit event
        self.view.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Bind root folder elements
        self.view.add_root_folder_elements(self.model.root_path, self.set_root_folder)
    # end def bind_view_events_and_commands

    def add_buttons(self):
        """
        Add buttons
        """
        # TODO : it should not be here, but it is easier for now
        if EDIT_MODE_ENABLED:
            # Add Edit button
            edit_btn = tk.Button(self.view.btn_frame, text="Edit", command=self.edit)
            edit_btn.grid(row=0, column=2, sticky="e", padx=2)

            # Add Save button
            save_btn = tk.Button(self.view.btn_frame, text="Save", command=self.save)
            save_btn.grid(row=0, column=3, sticky="e", padx=2)
        # end if
        # Add Close button
        close_btn = tk.Button(self.view.btn_frame, text="Close", command=self.on_exit)
        close_btn.grid(row=0, column=4, sticky="e", padx=2)
    # end def add_buttons

    def start(self):
        """
        Start main application
        """
        self.view.start()
    # end def start

    def select_file(self):
        """
        Select file
        """
        filetypes = (
            ('settings files', '*.ini'),
            ('All files', '*.*')
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir=Path(self.model.filename).parent,
            filetypes=filetypes)

        self.model.set_filename(filename)
        self.update_all()
    # end def select_file

    def select_node(self, _event):
        """
        Select node in the tree view

        :param _event: Event
        :type _event: ``Event``
        """
        self.section = self.view.get_section(self.view.tree_view.selection())
        self.update_list_view()
    # end def select_node

    def select_line(self, _event):
        """
        Select line in the list view

        :param _event: Event
        :type _event: ``Event``
        """
        selection = self.view.list_view.selection()
        if len(selection):
            self.key = self.filled_keys[int(selection[0])]
        else:
            self.key = None
        # end if
        self.update_info_view()
    # end def select_line

    def model_error_callback(self):
        """
        Update the view with the new model errors state
        """
        error_strings = []
        if self.model.error_pytestbox_files:
            error_strings.append("Couldn't find pytestbox files in the given root path."
                                 "Comments and defaults unavailable")
        # end if

        if len(self.model.parsing_errors) > 0:
            error_strings.append("Parsing error may prevent correct displaying of defaults and comments")
        # end if

        error_string = "\n".join(error_strings)
        self.view.error_string = error_string
    # end def model_error_callback

    def parsing_error_callback(self):
        """
        Display a popup view with the new model parsing errors
        """
        if len(self.model.parsing_errors) > 0:
            parsing_errors = ';\n'.join(self.model.parsing_errors)
            retry = self.view.display_error_popup(parsing_errors)
            if retry:
                self.model.gather_features_comments_and_defaults()
            # end if
        # end if
    # end def parsing_error_callback

    def update_section(self):
        """
        Update section view
        """
        self.view.set_section(self.section)
        self.update_list_view()
    # end def update_section

    def update_list_view(self):
        """
        Update the list view
        """
        self.view.list_view.delete(*self.view.list_view.get_children())

        section = self.view.get_section(self.view.tree_view.selection())
        if len(section):
            self.filled_keys = self.view.insert_keys(self.model.config_dict, self.model.features_comments, section)
        # end if
    # end def update_list_view

    def update_info_view(self):
        """
        Update displayed information in the info view
        """
        if self.key is None:
            self.view.info_title = "Information Pane"
            self.view.info_comment = "Please select an entry"
            self.view.info_value = ""
            self.view.info_source = ""
            return
        # end if

        key = self.section + "/" + self.key
        self.view.info_title = key
        self.view.info_comment = self.model.features_comments.get(key, "")

        value, source = extract_section_dict(self.model.config_dict, self.section).get(self.key, ("", ""))
        self.view.info_value = value
        self.view.info_source = source
    # end def update_info_view

    def update_all(self):
        """
        Update data model and view
        """
        if self.model.filename:
            config_dict = self.model.update_model(self.include_hierarchy_status.get(),
                                                  self.include_default_status.get())
            self.view.update_tree_view(self.model.relative_path(self.model.filename), config_dict)
            self.update_section()
            self.update_info_view()
        # end if
    # end def update_all

    def set_value(self):
        """
        Set value
        """
        section = self.view.get_section(self.view.tree_view.focus())
        key = self.view.list_view.item(self.view.list_view.focus(), 'text')
        entry_value = self.entry.get()
        if not self.model.has_section(section):
            self.model.add_section(section)
        # end if
        self.model.config.set(section, str(key), str(entry_value))
        self.update_all()
        self.top.destroy()
    # end def set_value

    def edit(self):
        """
        Edit an item
        """
        # TODO : should it be here? This is an other view?
        details = self.view.list_view.item(self.view.list_view.selection())

        top = tk.Toplevel(self.view.root)
        top.title(f'Edit {details["text"]}')
        self.top = top
        label = tk.Label(top, text=details['text'])
        label.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        entry = tk.Entry(top)
        entry.insert(0, details['values'])
        entry.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.entry = entry
        ok_btn = tk.Button(top, text="Ok", command=self.set_value)
        ok_btn.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        cancel_btn = tk.Button(top, text="Cancel", command=top.destroy)
        cancel_btn.grid(row=0, column=3, sticky="e", padx=10, pady=10)
    # end def edit

    def save(self):
        """
        Save
        """
        with open(self.model.filename, "w") as ini_file:
            self.model.config.write(ini_file)
        # end with
    # end def save

    def save_as(self):
        """
        Save as
        """
        filetypes = (
            ('settings files', '*.ini'),
            ('All files', '*.*')
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        self.model.set_filename(filename)
        self.save()
        self.update_all()
    # end def save_as

    def update_persistence(self):
        """
        Update persistence file with current state
        """
        persistence = {
            "current_file":  self.model.filename,
            "include_hierarchy": self.include_hierarchy_status.get(),
            "include_defaults": self.include_default_status.get(),
            "current_section":  self.section,
            "root_path": self.model.root_path,
        }
        with open(PERSISTENT_FILE_NAME, "w") as f:
            dump(persistence, f)
        # end with
    # end def update_persistence

    def load_persistence(self):
        """
        Update persistence file with current state, use default values if load can't happen
        """
        if not exists(PERSISTENT_FILE_NAME):
            persistence = {}
        else:
            try:
                with open(PERSISTENT_FILE_NAME, "r") as f:
                    persistence: dict = load(f)
                # end with
            except JSONDecodeError:
                # Quietly use defaults values if no persistence can be loaded
                persistence = {}
            # end try
        # end if

        self.model.set_filename(persistence.get("current_file", ""))
        self.model.root_path = persistence.get("root_path", abspath(curdir))
        self.view.root_folder_label_text.set(self.model.root_path)

        # Without updating here, the internal state get confused.
        # It seems like hierarchy is only supported when off at the start
        self.update_all()

        self.include_hierarchy_status.set(persistence.get("include_hierarchy", False))
        self.include_default_status.set(persistence.get("include_defaults", False))
        self.section = persistence.get("current_section", "")

        return True
    # end def load_persistence

    def on_exit(self):
        """
        Handle exit button
        """
        self.update_persistence()
        self.view.root.quit()
    # end def on_exit

    def set_root_folder(self, *_args):
        """
        Callback method called for opening the dialogue to set the current root folder

        :param _args: ignored arguments
        :type _args: ``tuple(objects)``
        """
        root_dir = filedialog.askdirectory(
            title='Select directory',
            initialdir=self.model.root_path
        )
        if len(root_dir) > 0:
            self.model.root_path = root_dir
            self.view.root_folder_label_text.set(self.model.root_path)

            self.model.invalid_model()
            self.update_all()
        # end if
    # end def set_root_folder
# end class ConfigurationController

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
