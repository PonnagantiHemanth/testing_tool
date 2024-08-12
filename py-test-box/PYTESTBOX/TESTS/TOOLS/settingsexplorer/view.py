#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: settingsexplorer.view
:brief: Settings Explorer View
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/04/12
"""


# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import tkinter as tk
from re import findall
from tkinter import ttk as ttk
from webbrowser import open_new_tab

from settingsexplorer.constants import EDIT_MODE_ENABLED
from settingsexplorer.constants import MATCH_URL_REGEX
from settingsexplorer.utils import extract_section_dict


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------

class ConfigurationView:
    """
    View of the model data in the Model-View-Controller design pattern
    """

    APPLICATION_NAME = 'Settings Explorer'

    def __init__(self):
        # Create root window
        self.root = tk.Tk()
        self.root.title(self.APPLICATION_NAME)

        # Configure the grid layout
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Define window size
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.maxsize(width=screen_w, height=screen_h)
        rw = int(screen_w / 2)
        rh = int(screen_h / 2)
        self.root.geometry('{}x{}+{:g}+{:g}'.format(rw, rh, rw / 2, rh / 2))

        # Add top menu
        top_menu = tk.Menu(self.root)
        self.root.config(menu=top_menu)

        # Add File menu
        self.file_menu = tk.Menu(top_menu, tearoff=False)
        top_menu.add_cascade(label='File', menu=self.file_menu)

        # Add paned window
        paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.grid(row=0, column=0, columnspan=2, sticky='eswn')

        tree_area = tk.Frame(paned_window)
        tree_area.grid_rowconfigure(0, weight=1)
        tree_area.grid_columnconfigure(0, weight=1)
        paned_window.add(tree_area)

        # Create a treeview
        self.tree_view = ttk.Treeview(tree_area)
        self.tree_view.heading('#0', text='', anchor=tk.W)

        # Place the Treeview widget on the root window
        self.tree_view.grid(row=0, column=0, sticky=tk.NSEW)

        # Add Y scrollbar
        scroll_ty = tk.Scrollbar(tree_area, orient=tk.VERTICAL, command=self.tree_view.yview)
        scroll_ty.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.tree_view['yscrollcommand'] = scroll_ty.set

        # Add X scrollbar
        scroll_tx = tk.Scrollbar(tree_area, orient=tk.HORIZONTAL, command=self.tree_view.xview)
        scroll_tx.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.tree_view['xscrollcommand'] = scroll_tx.set

        # Add detail area
        detail_area = tk.Frame(paned_window)
        detail_area.grid_rowconfigure(0, weight=1)
        detail_area.grid_columnconfigure(0, weight=1)
        paned_window.add(detail_area)

        # Add list view in detail area
        self.list_view = ttk.Treeview(detail_area)
        self.list_view['columns'] = ('#1', '#2', '#3')
        self.list_view.column("#0", width=150, minwidth=150, stretch=tk.YES)
        self.list_view.column("#1", width=150, minwidth=150, stretch=tk.YES)
        self.list_view.column("#2", width=150, minwidth=150, stretch=tk.YES)
        self.list_view.column("#3", width=150, minwidth=150, stretch=tk.YES)
        self.list_view.heading("#0", text="Name", anchor=tk.W)
        self.list_view.heading("#1", text="Value", anchor=tk.W)
        self.list_view.heading("#2", text="Comment", anchor=tk.W)
        self.list_view.heading("#3", text="Source", anchor=tk.W)
        self.list_view.grid(row=0, column=0, sticky='nsew')

        # Add Y and X scrollbars
        scroll_fy = tk.Scrollbar(detail_area, orient=tk.VERTICAL, command=self.list_view.yview)
        scroll_fy.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.list_view['yscrollcommand'] = scroll_fy.set
        scroll_fx = tk.Scrollbar(detail_area, orient=tk.HORIZONTAL, command=self.list_view.xview)
        scroll_fx.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.list_view['xscrollcommand'] = scroll_fx.set

        # Add info panel in detail area
        info_panel = tk.Frame(detail_area)
        info_panel.grid(row=1, column=0, sticky='nsew')

        self._info_title_var = tk.StringVar(self.root, value="")
        self._info_title = ttk.Label(info_panel, textvariable=self._info_title_var)
        self._info_title.configure(font=('Helvetica', 11, 'bold'))
        self._info_title.pack(fill='x')

        separator1 = ttk.Separator(info_panel, orient=tk.HORIZONTAL)
        separator1.pack(fill='x')

        self._info_comment_var = tk.StringVar(self.root, value="")
        self._info_comment = ttk.Label(
            info_panel, textvariable=self._info_comment_var, justify="left")
        self._info_comment.pack(fill='x')

        self._info_links_list = []
        self._info_link_pane = ttk.Frame(info_panel)
        self._info_link_pane.pack(fill='x')

        self._info_source_var = tk.StringVar(self.root, value="")
        self._info_source = ttk.Label(
            info_panel, textvariable=self._info_source_var, justify="left")
        self._info_source.pack(fill='x')

        separator2 = ttk.Separator(info_panel, orient=tk.HORIZONTAL)
        separator2.pack(fill='x')

        state = tk.NORMAL if EDIT_MODE_ENABLED else tk.DISABLED
        info_value_label = ttk.Label(info_panel, text="Value")
        info_value_label.pack(fill='x')

        self._info_value_var = tk.StringVar(self.root, value="")
        self._info_value = ttk.Entry(info_panel, state=state, textvariable=self._info_value_var)
        self._info_value.pack(fill='x')

        # Add Frame for buttons
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.grid(row=1, column=1, sticky="e", padx=15, pady=10)

        # Add a frame for root folder selection

        self._error_string_var = tk.StringVar(self.root, value="")
        self._error_label = None

        self.folder_frame = tk.Frame(self.btn_frame)
        self.folder_frame.grid(row=0, column=0, sticky="e", padx=15)

        self.root_folder_label_text = None
        self.root_folder_label = None
        self.root_folder_button = None
    # end def __init__

    @property
    def info_title(self):
        """
        Property getter of ``info_title``

        :return: ``info_title`` value
        :rtype: ``str``
        """
        return self._info_title_var.get()
    # end def property getter info_title

    @info_title.setter
    def info_title(self, value):
        """
        Property setter of ``info_title``

        :param value: ''info_title'' value
        :type value: ``str``
        """
        self._info_title_var.set(value=value)
    # end def property setter info_title

    @property
    def info_comment(self):
        """
        Property getter of ``info_comment``

        :return: ``info_comment`` value
        :rtype: ``str``
        """
        return self._info_comment_var.get()
    # end def property getter info_comment

    @info_comment.setter
    def info_comment(self, value):
        """
        Property setter of ``info_comment``

        :param value: ``info_comment`` value
        :type value: ``str``
        """
        for label in self._info_links_list:
            label.destroy()
        # end for
        self._info_links_list.clear()

        links = findall(MATCH_URL_REGEX, value)
        for link_index, link in enumerate(links):
            value = value.replace(link, f"LINK N°{link_index + 1}", 1)
            link_label = ttk.Label(
                self._info_link_pane, text=f"{link_index + 1}°: {link}", cursor="hand2", foreground="blue")
            link_label.pack()
            link_label.bind("<Button-1>", self._open_link(link))
            self._info_links_list.append(link_label)
        # end for

        self._info_comment_var.set(value=value)
    # end def property setter info_comment

    @property
    def info_source(self):
        """
        Property getter of ``info_source``

        :return: ``info_source`` value
        :rtype: ``str``
        """
        return self._info_source_var.get()
    # end def property getter info_source

    @info_source.setter
    def info_source(self, value):
        """
        Property setter of ``info_source``

        :param value: ``info_source`` value
        :type value: ``str``
        """
        if value != "":
            value = "Source: " + value
        # end if
        self._info_source_var.set(value=value)
    # end def property setter info_source

    @property
    def info_value(self):
        """
        Property getter of ``info_value``

        :return: ``info_value`` value
        :rtype: ``str``
        """
        return self._info_value_var.get()
    # end def property getter info_value

    @info_value.setter
    def info_value(self, value):
        """
        Property setter of ``info_value``

        :param value: ``info_value`` value
        :type value: ``str``
        """

        self._info_value_var.set(value=value)
    # end def property setter info_value

    @property
    def error_string(self):
        """
        Property getter of ``error_string``

        :return: ``error_string`` value
        :rtype: ``str``
        """
        return self._error_string_var.get()
    # end def property getter error_string

    @error_string.setter
    def error_string(self, value):
        """
        Property setter of ``error_string``

        :param value: ``error_string`` value
        :type value: ``str``
        """
        self._error_string_var.set(value)

        if value != "" and self._error_label is None:
            self._error_label = tk.Label(self.btn_frame, textvariable=self._error_string_var, fg="red", justify="left")
            self._error_label.grid(row=1, column=0, sticky="e", padx=5, pady=10)
        elif value == "" and self._error_label is not None:
            self._error_label.destroy()
            self._error_label = None
        # end if
    # end def property setter error_string

    def add_root_folder_elements(self, path_variable, command):
        """
        Add root folders elements with the variable and callback in comment to the view.

        :param path_variable: Root folder path
        :type path_variable: ``str``
        :param command: Callback method on the select root directory button
        :type command: ``func``
        """
        self.root_folder_label_text = tk.StringVar(value=path_variable)
        self.root_folder_label = tk.Label(self.folder_frame, textvariable=self.root_folder_label_text)
        self.root_folder_label.grid(row=0, column=0, sticky="e", padx=2)
        self.root_folder_button = tk.Button(self.folder_frame, text="Select Root directory", command=command)
        self.root_folder_button.grid(row=0, column=1, sticky="e", padx=2)
    # end def add_root_folder_elements

    def add_checkboxes(self, variables, commands):
        """
        Add checkboxes

        :param variables: Variables attached to the checkboxes
        :type variables: ``list[tk.BooleanVar]``
        :param commands: Commands attached to the checkboxes
        :type commands: ``list[callable]``
        """
        checkbox_frame = tk.Frame(self.root)
        checkbox_frame.grid(row=1, column=0, sticky="w")
        include_hierarchy_checkbox = tk.Checkbutton(checkbox_frame,
                                                    text='Include hierarchy',
                                                    variable=variables[0],
                                                    onvalue=True,
                                                    offvalue=False,
                                                    command=commands[0],
                                                    )
        include_hierarchy_checkbox.grid(row=0, column=0, sticky="w")
        include_default_checkbox = tk.Checkbutton(checkbox_frame,
                                                  text='Include default',
                                                  variable=variables[1],
                                                  onvalue=True,
                                                  offvalue=False,
                                                  command=commands[1],
                                                  )
        include_default_checkbox.grid(row=0, column=1, sticky="w")
    # end def add_checkboxes

    def start(self):
        """
        Start main application
        """
        # Run the app
        self.root.mainloop()
    # end def start

    def update_tree_view(self, filename, config_dict):
        """
        Update tree view

        :param filename: Filename
        :type filename: ``str``
        :param config_dict: Configuration data model
        :type config_dict: ``dict``
        """
        if filename:
            self.tree_view.delete(*self.tree_view.get_children())
            self.list_view.delete(*self.list_view.get_children())
            self.tree_view.heading('#0', text=filename, anchor=tk.W)
            self.dict_tree_view(config_dict)
        # end if
    # end def update_tree_view

    def dict_tree_view(self, dict_to_view, parent_iid=0):
        """
        Render tree view from dictionary

        :param dict_to_view: Dictionary to render
        :type dict_to_view: ``dict``
        :param parent_iid: Parent iid - OPTIONAL
        :type parent_iid: ``str``

        :return: Last iid
        :rtype: ``str``
        """
        iid = parent_iid
        for index, key in enumerate(dict_to_view.keys()):
            iid += 1
            if isinstance(dict_to_view[key], dict):
                self.tree_view.insert('', tk.END, text=key, iid=iid, open=False)
                if parent_iid != 0:
                    self.tree_view.move(iid, parent_iid, index)
                # end if
                iid = self.dict_tree_view(dict_to_view[key], iid)
            # end if
        # end for
        return iid
    # end def dict_tree_view

    def get_section(self, node):
        """
        Get section

        :param node: Node in the section
        :type node: ``ttk.Treeview``

        :return: Section text
        :rtype: ``str``
        """

        node_text = ''
        while node:
            node_text = self.tree_view.item(node, 'text') + '/' + node_text
            node = self.tree_view.parent(node)
        # end while
        return node_text[:-1]
    # end def get_section

    def set_section(self, node_text):
        """
        Put a section into focus

        :param node_text: Section text
        :type node_text: ``str`` or ``None``
        """
        if node_text is None:
            return
        # end if

        node = None
        for text in node_text.split("/"):
            children = self.tree_view.get_children(node)
            for child in children:
                if self.tree_view.item(child, "text").strip() == text.strip():
                    node = child
                    break
                # end if
            # end for
        # end for
        if node is not None:
            self.tree_view.selection_set(node)
            self.tree_view.see(node)
        # end if
    # end def set_section

    def insert_keys(self, config_dict, comments, section, filled_keys=None):
        """
        Insert keys of a section

        :param config_dict: Configuration
        :type config_dict: ``dict``
        :param comments: Comments dictionary
        :type comments: ``dict``
        :param section: Section
        :type section: ``str``
        :param filled_keys: List of keys of the section already filled - OPTIONAL
        :type filled_keys: ``list`` or ``None``

        :return: the list of keys with added keys
        :rtype: ``list``
        """
        filled_keys = [] if filled_keys is None else filled_keys
        config_dict = extract_section_dict(config_dict, section)
        for key in config_dict:
            if isinstance(config_dict[key], dict):
                continue
            # end if
            if key not in filled_keys:
                comment = comments.get(section + "/" + str(key), "").split("\n")[0]

                value, source = config_dict[key]
                self.list_view.insert(
                    '', 'end', str(len(filled_keys)), text=str(key),
                    values=(value, comment, source))
                filled_keys.append(key)
            # end if
        # end for
        return filled_keys
    # end def insert_keys

    def display_error_popup(self, error=None):
        """
        Display a new popup with the error passed in parameter.
        Only displays when an error is given.

        :param error: Error to display - Optional
        :type error: ``str`` or ``None``

        :return: flag indicating the user is retrying
        :rtype: ``bool``
        """

        if error:
            self.error_popup = tk.messagebox.Message(
                self.root,
                title="Parsing error",
                message=error,
                icon=tk.messagebox.WARNING,
                type=tk.messagebox.RETRYCANCEL
            )
            choice = self.error_popup.show()
            return choice == tk.messagebox.RETRY
        # end if
        return False
    # end def display_error_popup

    @staticmethod
    def _open_link(link):
        """
        Create a lambda to open a given link
        """
        return lambda _: open_new_tab(link)
    # end def _open_link
# end class ConfigurationView

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
