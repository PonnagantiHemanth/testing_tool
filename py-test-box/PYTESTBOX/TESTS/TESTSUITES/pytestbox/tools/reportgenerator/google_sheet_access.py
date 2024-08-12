#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.tools.reportgenerator.google_sheet_access
:brief: Google Sheet API Report generator
:author: Gautham S B <gsb@logitech.com>
:date: 2024/01/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import calendar
import datetime
import json
import os
import os.path as path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.tools.reportgenerator.config.evt_typing import EvtTypingConfig


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GoogleSheetReport(object):
    """
    The Google Sheet Report Generator class
    """
    _instance = None
    BUILD_NUMBER_CELL = EvtTypingConfig.BUILD_NUMBER_CELL
    TEST_RESULT_DATA_RANGE = EvtTypingConfig.TEST_RESULT_DATA_RANGE
    TEST_RESULT_TABLE_RANGE = EvtTypingConfig.TEST_RESULT_TABLE_RANGE
    TEST_RESULT_TABLE_RANGE_AFTER_MOVING_DOWN = EvtTypingConfig.TEST_RESULT_TABLE_RANGE_AFTER_MOVING_DOWN
    TIMESTAMP_CELL = EvtTypingConfig.TIMESTAMP_CELL
    SHEET_NAME = EvtTypingConfig.TYPING_SHEET_NAME

    def __new__(cls, test_case, *args, **kwargs):
        """
        Constructor for new instance

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param args: Arguments - OPTIONAL
        :type args: ``list``
        :param kwargs: Keyword Arguments - OPTIONAL
        :type kwargs: ``dict``

        :return: New instance of GoogleSheetReport class
        :rtype: ``GoogleSheetReport``
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._init_services()
            cls._update_config(test_case)
            cls._create_test_report_table()
        # end if

        return cls._instance
    # end def __new__

    @classmethod
    def _create_test_report_table(cls):
        """
        Create a new test report table and move the old table down if last table created is not empty then update
        general test related info
        """
        if not cls._check_if_cell_range_empty(cls.TEST_RESULT_DATA_RANGE):
            cls._move_table_down()
            cls._copy_new_table()
            cls._clear_test_results()
        # end if
        cls._update_general_test_info()
    # end def _create_test_report_table

    @classmethod
    def _check_if_cell_range_empty(cls, cell_range):
        """
        Check if a given range of cells inside the 'Typing' sheet is empty

        :param cell_range: The range of cells
        :type cell_range: ``str``

        :retrun: Returns true if empty else false
        :rtype: ``bool``
        """
        range_name = f"{cls.SHEET_NAME}!{cell_range}"
        result = cls.service_for_sheet.spreadsheets().values().get(
            spreadsheetId=cls.evt_report_spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        return True if not values else False
    # end def _check_if_cell_range_empty

    @classmethod
    def _get_row_col_index(cls, range_name):
        """
        Get the maximum and minimum row and column index from a range of cells

        :param range_name: The range of cells
        :type range_name: ``str``

        :return: The max and min row and column index
        :rtype: ``[int, int, int, int]``
        """
        start_cell, end_cell = range_name.split(':')

        min_col_index = ord(start_cell[0].upper()) - 65
        min_row_index = int(start_cell[1:]) - 1
        max_col_index = ord(end_cell[0].upper()) - 65
        max_row_index = int(end_cell[1:]) - 1

        return min_row_index, max_row_index, min_col_index, max_col_index
    # end def _get_row_col_index

    @classmethod
    def _get_sheet_id(cls):
        """
        Get the 'Typing' sheet ID inside the EVT Report spreadsheet

        :return: The 'Typing' sheet ID or None if the sheet does not exist
        :rtype: ``str`` or ``None``
        """
        sheet_metadata = cls.service_for_sheet.spreadsheets().get(
            spreadsheetId=cls.evt_report_spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        for sheet in sheets:
            if sheet['properties']['title'] == cls.SHEET_NAME:
                return sheet['properties']['sheetId']
            # end if
        # end for
    # end def _get_sheet_id

    @classmethod
    def _move_table_down(cls):
        """
        Move the old table with test results in 'Typing' sheet down to make room for the new table from latest test
        execution
        """
        min_row, max_row, _, _ = cls._get_row_col_index(cls.TEST_RESULT_TABLE_RANGE)
        requests = [{"insertDimension": {"range": {
            "sheetId": cls.sheet_id, "dimension": "ROWS", "startIndex": min_row,
            "endIndex": max_row + 2}}}]

        cls.service_for_sheet.spreadsheets().batchUpdate(
            spreadsheetId=cls.evt_report_spreadsheet_id, body={'requests': requests}).execute()
    # end def _move_table_down

    @classmethod
    def _copy_new_table(cls):
        """
        Create new table by copying from a pre-existing table and insert it at top of the spreadsheet
        """
        new_table_min_row, new_table_max_row, min_col, max_col = cls._get_row_col_index(cls.TEST_RESULT_TABLE_RANGE)
        old_table_min_row, old_table_max_row, _, _ = cls._get_row_col_index(
            cls.TEST_RESULT_TABLE_RANGE_AFTER_MOVING_DOWN)

        # Create the request body to copy and paste the range
        request_body = {
            "requests": [{
                "copyPaste": {
                    "source":
                        {"sheetId": cls.sheet_id,
                         "startRowIndex": old_table_min_row,
                         "endRowIndex": old_table_max_row + 1,
                         "startColumnIndex": min_col,
                         "endColumnIndex": max_col + 1},
                    "destination":
                        {"sheetId": cls.sheet_id,
                         "startRowIndex": new_table_min_row,
                         "endRowIndex": new_table_max_row + 1,
                         "startColumnIndex": min_col,
                         "endColumnIndex": max_col + 1},
                    "pasteType": "PASTE_NORMAL"}}
            ]}

        # Execute the request to copy and paste the range
        cls.service_for_sheet.spreadsheets().batchUpdate(
            spreadsheetId=cls.evt_report_spreadsheet_id, body=request_body).execute()
    # end def _copy_new_table

    @classmethod
    def _clear_test_results(cls):
        """
        Clear the obsolete test results in the new table that was included with it while making a copy from the
        old table
        """
        request = cls.service_for_sheet.spreadsheets().values().clear(
            spreadsheetId=cls.evt_report_spreadsheet_id, range=f"Typing!{cls.TEST_RESULT_DATA_RANGE}", body={})
        request.execute()
    # end def _clear_test_results

    @classmethod
    def _update_config(cls, test_case):
        """
        Update configuration parameters for report generation services

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        """
        cls.fw_build = f"B{test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_Build[0]}"
        cls.date = cls._get_date()
        cls.evt_report_spreadsheet_id = test_case.f.PRODUCT.DEVICE.EVT_AUTOMATION.TYPING_TEST.F_EVTReportSpreadsheetID
        cls.sheet_id = cls._get_sheet_id()
    # end def _update_config

    @classmethod
    def write_sheet(cls, value, cell_range):
        """
        Writes values to the provided row

        :param value: Data to be written to Sheet
        :type value: ``list[list]``
        :param cell_range: target Cell ID to be written
        :type cell_range: ``str``
        """
        cls.service_for_sheet.spreadsheets().values().update(
            spreadsheetId=cls.evt_report_spreadsheet_id, range=f"Typing!{cell_range}",
            valueInputOption="USER_ENTERED", body={"values": value}).execute()
    # end def write_sheet

    @classmethod
    def _init_services(cls):
        """
        Get scope for Google sheet and drive from credentials (client_secret.json and token.json)
        """
        # Initialize Sheet API and get Drive Objects
        creds = None
        _FILE_PATH = path.abspath(__file__)
        working_dir = _FILE_PATH[:_FILE_PATH.rfind("TESTS")]
        client_secret = path.join(
            working_dir, "TESTSUITES", "pytestbox", "tools", "reportgenerator", "client_secret.json")
        token_json_path = path.join(working_dir, "TESTSUITES", "pytestbox", "tools", "reportgenerator", "token.json")
        token_json_secret = "TOKEN_JSON"
        google_api_scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time

        token_str = os.environ.get(token_json_secret)
        if token_str:
            token_json = json.loads(token_str)
            creds = Credentials.from_authorized_user_info(token_json, google_api_scopes)
        elif os.path.exists(token_json_path):
            creds = Credentials.from_authorized_user_file(token_json_path, google_api_scopes)
        else:
            raise Exception("The file 'token.json' does not exist and the 'TOKEN_JSON' environment variable is not set."
                            " At least one of them should be set or available.")
        # end if

        if not creds or not creds.valid:  # If there are no (valid) credentials available, let the user log in.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret, google_api_scopes)
                creds = flow.run_local_server(port=0)
            # end if

            """Save the credentials only if the token.json file is present in advance (for local testing)
            This is to avoid exposing the secret token JSON when the test is triggered by the CI/CD pipeline"""
            if os.path.exists(token_json_path):
                with open(token_json_path, 'w') as token:
                    token.write(creds.to_json())
                # end with
            # end if
        # end if

        cls.service_for_sheet = build('sheets', 'v4', credentials=creds)
        cls.service_for_drive = build('drive', 'v3', credentials=creds)
    # end def _init_services

    @classmethod
    def _get_date(cls):
        """
        Return date time in Month Date, Year format (ex: January 27, 2024)

        :return: The date value
        :rtype: ``str``
        """
        now = datetime.datetime.now()
        return f"{calendar.month_name[now.month]} {now.day}, {now.year}"
    # end def _get_date

    @classmethod
    def _update_general_test_info(cls):
        """
        Update General test info like FW build version and timestamp
        """
        range_name = f"{cls.SHEET_NAME}!{cls.BUILD_NUMBER_CELL}:{cls.TIMESTAMP_CELL}"
        new_values = [[cls.fw_build, cls.date]]
        value_range_body = {"range": range_name, "majorDimension": "ROWS", "values": new_values}

        cls.service_for_sheet.spreadsheets().values().update(
            spreadsheetId=cls.evt_report_spreadsheet_id, range=range_name, valueInputOption="USER_ENTERED",
            body=value_range_body).execute()
    # end def _update_general_test_info
# end class GoogleSheetReport

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
