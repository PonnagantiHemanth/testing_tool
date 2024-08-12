#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.source.spreadsheet
:brief: Main application to access google spreadsheet api
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/06/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import datetime
import os
import os.path as op
import re
import sys
from argparse import ArgumentParser
from enum import IntEnum
from string import Template

# noinspection PyUnresolvedReferences,PyPackageRequirements
from google.auth.transport.requests import Request
# noinspection PyUnresolvedReferences,PyPackageRequirements
from google.oauth2.credentials import Credentials
# noinspection PyUnresolvedReferences
from google_auth_oauthlib.flow import InstalledAppFlow
# noinspection PyUnresolvedReferences,PyPackageRequirements
from googleapiclient.discovery import build


FILE_PATH = op.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("TESTS")]
TOOLS_DIR = op.join(WS_DIR, "TESTS", "TOOLS")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
# end if

# noinspection PyUnresolvedReferences
from codegenerator.manager.engine import ConstantTextManager
# noinspection PyUnresolvedReferences
from codegenerator.manager.engine import FileManager
# noinspection PyUnresolvedReferences
from codegenerator.input.templates import UserInputTemplate
# noinspection PyUnresolvedReferences
from codegenerator.validator.engine import FileValidator


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# File operations
TOKEN_FILE = "token.json"
CLIENT_SECRET_FILE = "client_secret.json"
WRITE_MODE = "w"

# The ID and range of the spreadsheet.
CODE_GENERATION_TOOL_SHEET_ID = "1TO4UOiJ7zWza0wuIIOrqqig43kEY-Tm2O0cgQmEQ-TU"
CODE_GENERATION_TOOL_SHEET_URL = "https://docs.google.com/spreadsheets/d/1TO4UOiJ7zWza0wuIIOrqqig43kEY-Tm2O0cgQmEQ-TU"
FEATURE_INFO_RANGE = "Feature Info!A2:Z"
FUNCTION_INFO_RANGE = "API Info!A2:Z"
EVENT_INFO_RANGE = "Event Info!A2:Z"
MAP_RANGE = "Map!A2:Z"
# Populate this dictionary on need basis and use it in other places needed.
FeatureInfo = dict()


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TestDesignDocument(IntEnum):
    COL_A = 0  # Function/Event Index (0..N)
    COL_B = 1  # Function/Event Name
    COL_C = 2  # Parameter Type (Request/Response/Event)
    COL_D = 3  # Field Index (0..N)
    COL_E = 4  # Field Size (1..128)
    COL_F = 5  # Field Name
    COL_G = 6  # Field Type (int, bool, ...)
    COL_H = 7  # Reusable Containers Name (if any)(default: MixedContainer 1..N)
    COL_I = 8  # Parameter Comment (if any) (default: Field Name)
    COL_J = 9  # NVS BACKUP/RESTORE (if any) (default: False)
    COL_K = 10  # SETTINGS.ini data type (if any) (default: None)
    COL_L = 11  # Field Default Value (if any)
    COL_M = 12  # Field Name Prefix (if any)
    COL_N = 13  # Inner Class Name (if any)
    COL_O = 14  # Inner Class Index (0..N)
    COL_P = 15  # Parameter Exclusion (if any) (default: False)
    COL_Q = 16  # Parameter Default Value (if any)
    COL_R = 17  # Version Info
# end class TestDesignDocument


class TestCaseDocument(IntEnum):
    COL_A = 0  # Test Case Identifier
    COL_B = 1  # Synopsis
    COL_C = 2  # Test description
    COL_L = 11  # Test Name (if any)
# end class TestCaseDocument


class CodeGenerationMap(IntEnum):
    COL_A = 0  # Entry Date
    COL_B = 1  # Feature Identifier
    COL_C = 2  # Test Design Document Identifier
    COL_D = 3  # Test Case Document Identifier
# end class CodeGenerationMap


def authenticate():
    """
    Authenticate the user to access the Google spreadsheet.

    :return: Authenticated user credential
    :rtype: ``Credentials``
    """
    credential = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        credential = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # end if

    # If there are no (valid) credentials available, let the user log in.
    if not credential or not credential.valid:
        if credential and credential.expired and credential.refresh_token:
            credential.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credential = flow.run_local_server(port=0)
        # end if

        # Save the credentials for the next run
        with open(TOKEN_FILE, WRITE_MODE) as token:
            token.write(credential.to_json())
        # end with
    # end if
    return credential
# end def authenticate


def get_feature_info(service, sheet_id):
    """
    Get the 'Feature Info' tab information from the sheet.

    :param service: Google API service
    :type service: ``googleapiclient.discovery.Resource``
    :param sheet_id: Sheet identifier
    :type sheet_id: ``str``

    :return: Feature information
    :rtype: ``str``

    :raise ``AssertionError``: Assert spreadsheet values that raise an exception
    """
    # noinspection PyUnresolvedReferences
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=FEATURE_INFO_RANGE).execute()
    values = result.get('values', [])

    assert values is not None

    col_heading = 1
    output = []
    for row in values:
        if row[col_heading] == "HIDPP_FEATURE_NAME":
            # store FeatureName in the dictionary for other place usages.
            FeatureInfo["FeatureName"] = row[2]
        # end if
        output.append(Template(UserInputTemplate.FEATURE_INFO_TEXT).substitute(dict(
            Key=row[col_heading],
            Value=get_text(row)
        )))
    # end for
    return "".join(output)
# end def get_feature_info


def get_text(row):
    """
    Get the text value for feature information

    :param row: Row in the Google sheet
    :type row: ``list[str]``

    :return: Text in appropriate (double/triple/empty) quote
    :rtype: ``str``
    """
    col_heading = 1
    col_value = 2
    col_type = 3
    text = str(row[col_value])
    quote = ConstantTextManager.EMPTY_STRING
    if row[col_type] == "Comment":
        quote = ConstantTextManager.TRIPLE_QUOTE
        updated_text = ""
        for txt in text.split(ConstantTextManager.NEW_LINE):
            updated_text += ConstantTextManager.NEW_LINE
            if txt != "":
                updated_text += ConstantTextManager.TAB + txt
            # end if
        # end for
        text = updated_text
    elif row[col_type] == "Auto":
        date_value = row[col_value]
        if date_value == "":
            date_heading = row[col_heading]
            if date_heading == "YEAR":
                text = "datetime.today().year"
            elif date_heading == "MONTH":
                text = "f\"{datetime.today().month:02}\""
            elif date_heading == "DAY":
                text = "f\"{datetime.today().day:02}\""
            # end if
        # end if
    elif row[col_type] == "String":
        quote = ConstantTextManager.DOUBLE_QUOTE
    # end if

    return Template(UserInputTemplate.FEATURE_VALUE_TEXT).substitute(dict(Quote=quote, Value=text))
# end def get_text


def get_function_info(service, sheet_id):
    """
    Get the 'API Info' tab information from the sheet.

    :param service: Google API service
    :type service: ``googleapiclient.discovery.Resource``
    :param sheet_id: Sheet identifier
    :type sheet_id: ``str``

    :return: API information
    :rtype: ``str``

    :raise ``AssertionError``: Assert spreadsheet values that raise an exception
    """
    # noinspection PyUnresolvedReferences
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=FUNCTION_INFO_RANGE).execute()
    values = result.get('values', [])

    assert values is not None

    records = get_records(values)

    assert records is not None

    output = []
    for record in records:
        output.append(Template(UserInputTemplate.FUNCTION_INFO_ITEM).substitute(dict(
            Index=record["Index"],
            Name=record["Name"],
            Request=get_parameter_value("Request", record),
            Response=get_parameter_value("Response", record),
            NvsBackup=record["NvsBackup"],
            VersionInfo=get_function_version_info(record)
        )))
    # end for

    return Template(UserInputTemplate.FUNCTION_INFO_TEXT).substitute(dict(List=",".join(output)))
# end def get_function_info


def get_function_version_info(record):
    """
    Get function version value for the given record

    :param record: Record information
    :type record: ``dict``

    :return: Formatted output
    :rtype: ``str | None``
    """
    if record["Request"].get("Parameters") is not None:
        return
    # end if
    if record["Response"].get("Parameters") is not None:
        return
    # end if
    return record.get("VersionInfo")
# end def get_function_version_info


def get_event_version_info(record):
    """
    Get function version value for the given record

    :param record: Record information
    :type record: ``dict``

    :return: Formatted output
    :rtype: ``str | None``
    """
    if record["Event"].get("Parameters") is not None:
        return
    # end if
    return record.get("VersionInfo")
# end def get_event_version_info


def get_test_case_document_info(service, sheet_id):
    """
    Get the 'Feature Name' tab information from the test case document sheet.

    :param service: Google API service
    :type service: ``googleapiclient.discovery.Resource``
    :param sheet_id: Sheet identifier
    :type sheet_id: ``str``

    :return: API information
    :rtype: ``str | None``

    :raise ``AssertionError``: Assert spreadsheet values that raise an exception
    """
    # noinspection PyUnresolvedReferences
    sheet = service.spreadsheets()
    feature_name = FeatureInfo["FeatureName"]
    # noinspection PyBroadException
    try:
        result = sheet.values().get(spreadsheetId=sheet_id, range=feature_name+"!A3:Z").execute()
    except Exception:
        # sheet not found
        sys.stdout.write(f"\n'{feature_name}' tab is not in the test case document."
                         f" Verify and add in https://docs.google.com/spreadsheets/d/{sheet_id}")
        return
    # end try
    values = result.get('values', [])

    assert values is not None
    if not op.isdir("../output"):
        os.mkdir("../output")
    # end if

    valid_items = []
    for row in values:
        # Minimum field validation (id, synopsis, description)
        if len(row) < TestCaseDocument.COL_C:
            if row[TestCaseDocument.COL_A][:3] in ["INT", "BUS", "FUN", "ROB", "ERR", "SEC", "PER"]:
                sys.stdout.write("\nCheck id, synopsis and description:\n" + str(row))
                return
            # end if
            # may be a sub header row
            sys.stdout.write("\nIgnore the row: " + str(row))
            continue
        # end if
        dictionary = get_test_case_item_dictionary(row)
        if dictionary is None:
            return
        # end if

        valid_items.append(dictionary)
    # end for

    return get_test_case_document_records(valid_items)
# end def get_test_case_document_info


def get_event_info(service, sheet_id):
    """
    Get the 'Event Info' tab information from the sheet.

    :param service: Google API service
    :type service: ``googleapiclient.discovery.Resource``
    :param sheet_id: Sheet identifier
    :type sheet_id: ``str``

    :return: Event information
    :rtype: ``tuple[str, str]``

    :raise ``AssertionError``: Assert spreadsheet values that raise an exception
    """
    import_text = ""
    # noinspection PyUnresolvedReferences
    sheet = service.spreadsheets()
    # noinspection PyBroadException
    try:
        result = sheet.values().get(spreadsheetId=sheet_id, range=EVENT_INFO_RANGE).execute()
    except Exception:
        # sheet not found
        return import_text, Template(UserInputTemplate.EVENT_INFO_TEXT).substitute(dict(List=""))
    # end try

    values = result.get('values', [])

    assert values is not None

    records = get_records(values)

    output = []
    for record in records:
        output.append(Template(UserInputTemplate.EVENT_INFO_ITEM).substitute(dict(
            Index=record["Index"],
            Name=record["Name"],
            Event=get_parameter_value("Event", record),
            NvsBackup=record["NvsBackup"],
            VersionInfo=get_event_version_info(record)
        )))
    # end for

    import_text = UserInputTemplate.EVENT_IMPORT
    event_text = Template(UserInputTemplate.EVENT_INFO_TEXT).substitute(dict(List=",".join(output)))
    return import_text, event_text
# end def get_event_info


def get_parameter_value(parameter_type, record):
    """
    Get parameter value for the given type

    :param parameter_type: Parameter type (Request/Response/Event)
    :type parameter_type: ``str``
    :param record: Record information
    :type record: ``dict``

    :return: Formatted output
    :rtype: ``str``
    """
    input_items = dict(
        Base="",
        Parameters=""
    )
    base_value = record[parameter_type].get("Base", "")
    if base_value != "":
        input_items["Base"] = Template(UserInputTemplate.BASE_ITEM).substitute(dict(Base=base_value))
    # end if
    parameters = record[parameter_type].get("Parameters")
    if parameters is not None:
        output = []
        for parameter in parameters:
            sub_parameters = parameter.get("SubParameters")
            if sub_parameters is None:
                output.append(Template(UserInputTemplate.PARAMETER_ITEM).substitute(dict(
                    Index=parameter["Index"],
                    Size=parameter["Size"],
                    Type=parameter["Type"],
                    Name=parameter["Name"],
                    Comment=parameter.get("Comment", None),
                    SettingsDataType=parameter.get("SettingsDataType", None),
                    SettingsDefaultValue=parameter.get("SettingsDefaultValue", None),
                    SubParameters="",
                    Prefix=parameter.get("Prefix", None),
                    Exclusion=parameter.get("Exclusion", False),
                    DefaultValue=parameter.get("DefaultValue", None),
                    VersionInfo=parameter.get("VersionInfo")
                )))
            else:
                sub_output = []
                size = 0
                for sub_parameter in sub_parameters:
                    size += int(sub_parameter["Size"])
                    sub_output.append(Template(UserInputTemplate.SUB_PARAMETER_ITEM).substitute(dict(
                        Index=sub_parameter["Index"],
                        Size=sub_parameter["Size"],
                        Type=sub_parameter["Type"],
                        Name=sub_parameter["Name"],
                        Comment=sub_parameter.get("Comment", None),
                        SettingsDataType=sub_parameter.get("SettingsDataType", None),
                        SettingsDefaultValue=sub_parameter.get("SettingsDefaultValue", None),
                        Prefix=sub_parameter.get("Prefix", None),
                        Exclusion=sub_parameter.get("Exclusion", False),
                        DefaultValue=sub_parameter.get("DefaultValue", None),
                        VersionInfo=sub_parameter.get("VersionInfo")
                    )))
                # end for
                output.append(Template(UserInputTemplate.PARAMETER_ITEM).substitute(dict(
                    Index=parameter["Index"],
                    Size=size,
                    Type="HexList",
                    Name=parameter["Name"],
                    Comment=None,
                    SettingsDataType=None,
                    SettingsDefaultValue=None,
                    Prefix=None,
                    Exclusion=False,
                    DefaultValue=None,
                    SubParameters=",".join(sub_output),
                    VersionInfo=parameter.get("VersionInfo")
                )))
        # end for
        input_items["Parameters"] = ",".join(output)
    # end if
    return Template(UserInputTemplate.REQ_RES_ITEM).substitute(input_items)
# end def get_parameter_value


def is_option_enabled(row, pos):
    """
    Get value on the position

    :param row: All the data contained in a row of the spreadsheet
    :type row: ``list[str]``
    :param pos: Index of the column from which to extract the required value
    :type pos: ``int``

    :return: Flag indicating if the option is enabled
    :rtype: ``bool``
    """
    return row[pos].lower().strip() == "true" if row[pos] != "" else False
# end def is_option_enabled


def get_text_in_quote(row, pos, quote):
    """
    Get value on the position

    :param row: All the data contained in a row of the spreadsheet
    :type row: ``list[str]``
    :param pos: Index of the column from which to extract the required value
    :type pos: ``int``
    :param quote: Quote type. NB: single/double/triple quote shall be used.
    :type quote: ``str``

    :return: Value on the row position
    :rtype: ``str | None``
    """
    return f'{quote}{row[pos]}{quote}' if row[pos] != "" else None
# end def get_text_in_quote


def get_default_settings_value(row, pos):
    """
    Get value on the position

    :param row: All the data contained in a row of the spreadsheet
    :type row: ``list[str]``
    :param pos: Index of the column from which to extract the required value
    :type pos: ``int``

    :return: Value on the row position
    :rtype: ``str | None``
    """
    return row[pos] if row[pos] != "" else None
# end def get_default_settings_value


def get_default_value(row, pos):
    """
    Get string/bool value on the position

    :param row: All the data contained in a row of the spreadsheet
    :type row: ``list[str]``
    :param pos: Index of the column from which to extract the required value
    :type pos: ``int``

    :return: Value on the row position
    :rtype: ``str | None``
    """
    if row[pos].strip() == "":
        return None
    # end if
    if row[pos].lower().strip() == "true":
        return "True"
    elif row[pos].lower().strip() == "false":
        return "False"
    elif row[pos].lower().strip() == "none":
        return '"None"'
    # end if
    return row[pos]
# end def get_default_value


def get_test_case_document_records(values):
    """
    Get records from the test case document

    :param values: Spreadsheet data
    :type values: ``list[dict]``

    :return: Formatted output of test case information
    :rtype: ``str | None``
    """
    interface_test_cases = []
    business_test_cases = []
    functionality_test_cases = []
    error_handling_test_cases = []
    robustness_test_cases = []
    security_test_cases = []
    performance_test_cases = []
    setup_section_test_cases = []
    teardown_section_test_cases = []

    for dictionary in values:
        value = Template(UserInputTemplate.TEST_CASE_INFO_ITEM).substitute(dictionary)
        identifier = dictionary["Identifier"].replace('"""', '')
        if identifier.startswith("INT"):
            interface_test_cases.append(value)
        elif identifier.startswith("BUS"):
            business_test_cases.append(value)
        elif identifier.startswith("FUN"):
            functionality_test_cases.append(value)
        elif identifier.startswith("ROB"):
            robustness_test_cases.append(value)
        elif identifier.startswith("ERR"):
            error_handling_test_cases.append(value)
        elif identifier.startswith("SEC"):
            security_test_cases.append(value)
        elif identifier.startswith("PER"):
            performance_test_cases.append(value)
        elif identifier.startswith("CODE_GENERATION_TOOL_SETUP_SECTION"):
            # common pre-requisites for every test case.
            # https://docs.google.com/spreadsheets/d/1eEJRkuAhjIWr7dkyHNE7fWHuzUsP7I9BZivZj6-8j9c/view#gid=1988673015
            setup_section_test_cases.append(value)
        elif identifier.startswith("CODE_GENERATION_TOOL_TEARDOWN_SECTION"):
            # common post-requisites for every test case.
            # https://docs.google.com/spreadsheets/d/103t33gMZFEd4EsVuAfXxaw8_pJbzL5diBO_Is9mvF44/view#gid=1
            teardown_section_test_cases.append(value)
        else:
            sys.stdout.write(f"\nTODO: new identifier found: {identifier}")
        # end if
    # end for

    return Template(UserInputTemplate.TEST_CASE_INFO_TEXT).substitute(dict(
        Interface=",".join(interface_test_cases),
        Business=",".join(business_test_cases),
        ErrorHandling=",".join(error_handling_test_cases),
        Functionality=",".join(functionality_test_cases),
        Robustness=",".join(robustness_test_cases),
        Security=",".join(security_test_cases),
        Performance=",".join(performance_test_cases),
        Setup=",".join(setup_section_test_cases),
        Teardown=",".join(teardown_section_test_cases)
    ))
# end def get_test_case_document_records


def get_text_in_col(row, column):
    """
    Get the column text for the given row

    :param row: Single row of the sheet
    :type row: ``list[str]``
    :param column: Column id of the sheet
    :type column: ``TestCaseDocument``

    :return: Text in the column
    :rtype: ``str | None``
    """
    if len(row) > column and row[column] != "":
        return row[column]
    # end if
    return None
# end def get_text_in_col


def get_test_case_item_dictionary(row):
    """
    Get test case information in dictionary format

    :param row: Single row of the sheet
    :type row: ``list[str]``
    """

    # Structure of the document.
    # Ex: https://docs.google.com/spreadsheets/d/1KghpBFmAqF9puiNRVO93m_0lDWAGNpGQsbsP64e-VSM/view#gid=1&range=A5
    # ['Test Case Id',  'Synopsis',  'Test description',  'Targeted requirements',  'Status',  'Author',
    # 'Quality risk category',  'Test design technique',  'Comments',  'Reviewer', 'Review',
    # 'Test Case Name' - This column may not be available in older documents
    # ]

    # name: Column L (test case name) or column A (id)
    name = f'"""fill_column_l_in_test_case_document"""'
    identifier = row[TestCaseDocument.COL_A].replace("\n", ", ")
    col_l_text = get_text_in_col(row, TestCaseDocument.COL_L)
    if col_l_text is not None:
        if " " in col_l_text:
            col_l_text = "_".join(col_l_text.split(" "))
        # end if
        if not col_l_text.startswith("test_"):
            col_l_text = f"test_{col_l_text}"
        # end if
        name = f'"""{col_l_text.lower()}"""'
    # end if

    synopsis = '"""TODO: Check the test case document and fill the synopsis"""'
    col_b_text = get_text_in_col(row, TestCaseDocument.COL_B)
    if col_b_text is not None:
        synopsis = f'"""{convert_double_quote_to_single_quote(col_b_text.strip())}"""'
    # end if
    description = '"""TODO: Check the test case document and fill the description"""'
    col_c_text = get_text_in_col(row, TestCaseDocument.COL_C)
    if col_c_text:
        text = col_c_text.strip()

        if not identifier.startswith("CODE_GENERATION_TOOL"):
            assert re.search(pattern="Test [Ss]tep", string=text),\
                f'"{identifier}": At least one "Test Step" is mandatory in Description (Col C).'
            assert re.search(pattern="Test [Cc]heck", string=text),\
                f'"{identifier}": At least one "Test Check" is mandatory in Description (Col C).'
            if re.search(pattern="[Tt]est [Ll]oop", string=text):
                a = re.findall(pattern="[Tt]est [Ll]oop", string=text)
                b = re.findall(pattern="[Ee]nd [Tt]est [Ll]oop", string=text)
                assert len(a) == (2 * len(b)),\
                    f'"{identifier}": Each "Test loop" must have a "End test loop" in Description (Col C).'
            # end if
        # end if

        description = f'"""{convert_double_quote_to_single_quote(text)}"""'
    # end if
    dictionary = dict(
        Identifier=f'"""{identifier}"""',
        Synopsis=synopsis,
        Description=description,
        Name=name
    )
    if not validate_test_case_item_dictionary(dictionary):
        return
    # end if
    return dictionary
# end def get_test_case_item_dictionary


def validate_test_case_item_dictionary(dictionary):
    """
    Validate the test case item dictionary

    :param dictionary: Dictionary
    :type dictionary: ``dict``

    :return: Flag indicating if the dictionary values are valid
    :rtype: ``bool``
    """
    for item in dictionary.items():
        if not FileValidator.write_file("../output/dummy_test_case_validation.py", [str(item[1])]):
            return False
        # end if
    # end for
    return True
# end def validate_test_case_item_dictionary


def convert_double_quote_to_single_quote(text):
    """
    Convert double quote to single quote

    :param text: The text which needs conversion
    :type text: ``str``

    :return: Updated text with single quote
    :rtype: ``str``
    """
    return text.replace("\"", "'")
# end def convert_double_quote_to_single_quote


def get_records(values):
    """
    Get records from the spreadsheet values

    :param values: Spreadsheet data for the sheet
    :type values: ``list``

    :return: List of records
    :rtype: ``list``

    :raise ``AssertionError``: Assert spreadsheet values that raise an exception
    """
    records = []
    record = None
    record_count = -1
    parameter_type = None

    for row in values:
        # Keep the FunctionIndex/EventIndex until next index changes.
        if row[TestDesignDocument.COL_A] != "":
            assert not str(row[TestDesignDocument.COL_B]).lower().endswith("event"), \
                f'"{row[TestDesignDocument.COL_B]}": Remove the suffix "Event" which is taken care by program'
            record = dict(
                Index=row[TestDesignDocument.COL_A],
                Name=row[TestDesignDocument.COL_B],
                Request=dict(),
                Response=dict(),
                Event=dict(),
                NvsBackup=is_option_enabled(row, TestDesignDocument.COL_J)
            )
            # Robustness in function index/name handling
            for item in records:
                assert item["Name"] != record["Name"], \
                    f'Duplicate name: ({item["Index"]}:{item["Name"]}, {record["Index"]}:{record["Name"]})'
            # end for
            records.append([])
            record_count += 1
            parameter_type = None
        # end if

        # Keep the ParameterType until the next type changes.
        if row[TestDesignDocument.COL_C] != "":
            parameter_type = row[TestDesignDocument.COL_C]
            assert record[parameter_type].get("Parameters") is None, \
                f'Duplicate parameter type "{parameter_type}" for the same function "{record["Name"]}"'
            record[parameter_type]["Parameters"] = []
        # end if

        if row[TestDesignDocument.COL_H] != "":
            record[parameter_type]["Base"] = "".join(str(row[TestDesignDocument.COL_H]).split())
        # end if

        if parameter_type is None:
            record["VersionInfo"] = get_text_in_quote(row, TestDesignDocument.COL_R, '"')
            # update record
            records[record_count] = record
            continue
        # end if
        assert_field_values(record, row)
        parameter = get_parameter_item(parameter_type, record, row)
        update_record_parameter_info(row, parameter)
        # update record
        records[record_count] = record
    # end for
    return records
# end def get_records


def update_record_parameter_info(row, parameter):
    """
    Update parameter information in the record

    :param row: Spreadsheet row
    :type row: ``list[str]``
    :param parameter: Parameter information
    :type parameter: ``dict``
    """
    if row[TestDesignDocument.COL_O] != "":
        if row[TestDesignDocument.COL_N] != "":
            # override name
            parameter["Name"] = row[TestDesignDocument.COL_N]
        # end if
        if parameter.get("SubParameters") is None:
            parameter["SubParameters"] = []
        # end if
        parameter["SubParameters"].append(dict(
            Index=row[TestDesignDocument.COL_O],
            Size=row[TestDesignDocument.COL_E],
            Name=row[TestDesignDocument.COL_F],
            Type=row[TestDesignDocument.COL_G],
            Comment=get_text_in_quote(row, TestDesignDocument.COL_I, '"""'),
            SettingsDataType=get_text_in_quote(row, TestDesignDocument.COL_K, '"'),
            SettingsDefaultValue=get_default_settings_value(row, TestDesignDocument.COL_L),
            Prefix=get_text_in_quote(row, TestDesignDocument.COL_M, '"'),
            Exclusion=is_option_enabled(row, TestDesignDocument.COL_P),
            DefaultValue=get_default_value(row, TestDesignDocument.COL_Q),
            VersionInfo=get_text_in_quote(row, TestDesignDocument.COL_R, '"')
        ))
    else:
        parameter["Size"] = row[TestDesignDocument.COL_E]
        parameter["Name"] = row[TestDesignDocument.COL_F]
        parameter["Type"] = row[TestDesignDocument.COL_G]
        parameter["Comment"] = get_text_in_quote(row, TestDesignDocument.COL_I, '"""')
        parameter["SettingsDataType"] = get_text_in_quote(row, TestDesignDocument.COL_K, '"')
        parameter["SettingsDefaultValue"] = get_default_settings_value(row, TestDesignDocument.COL_L)
        parameter["Prefix"] = get_text_in_quote(row, TestDesignDocument.COL_M, '"')
        parameter["Exclusion"] = is_option_enabled(row, TestDesignDocument.COL_P)
        parameter["DefaultValue"] = get_default_value(row, TestDesignDocument.COL_Q)
        parameter["VersionInfo"] = get_text_in_quote(row, TestDesignDocument.COL_R, '"')
    # end if
# end def update_record_parameter_info


def get_parameter_item(parameter_type, record, row):
    """
    Get parameter item

    :param parameter_type: Type of parameter (Request/Response/Event)
    :type parameter_type: ``str``
    :param record: Record information
    :type record: ``dict``
    :param row: Spreadsheet row
    :type row: ``list[str]``

    :return: Parameter information
    :rtype: ``dict``
    """
    parameter = dict()
    if len(record[parameter_type]["Parameters"]) == 0:
        parameter["Index"] = row[TestDesignDocument.COL_D]
        record[parameter_type]["Parameters"].append(parameter)
    else:
        item_found = None
        for item in record[parameter_type]["Parameters"]:
            if item["Index"] == row[TestDesignDocument.COL_D]:
                item_found = True
                parameter = item
                break
            # end if
        # end for
        if not item_found:
            parameter["Index"] = row[TestDesignDocument.COL_D]
            record[parameter_type]["Parameters"].append(parameter)
        # end if
    # end if
    return parameter
# end def get_parameter_item


def assert_field_values(record, row):
    """
    Assert duplicate record (if already present)

    :param record: Single record to check
    :type record: ``dict``
    :param row: Spreadsheet row
    :type row: ``list``

    :raise ``AssertionError``: Assert duplicate values that raise an exception
    """
    # validate the version info column first to simplify other column validation
    record_name = record["Name"]
    col_f_value = row[TestDesignDocument.COL_F]

    assert len(row) < TestDesignDocument.COL_R or row[TestDesignDocument.COL_R].strip() != "", \
        f'"{record_name}" => "{col_f_value}": version info is mandatory since v1.3'

    assert row[TestDesignDocument.COL_D] != "", f'"{record_name}" => "{col_f_value}": field index is mandatory'
    assert col_f_value != "", f'"{record_name}" => "{row[TestDesignDocument.COL_D]}": field name is mandatory'
    assert row[TestDesignDocument.COL_G] != "", f'"{record_name}" => "{col_f_value}": field type is mandatory'
    assert row[TestDesignDocument.COL_E] != "", f'"{record_name}" => "{col_f_value}": field size is mandatory'
    assert col_f_value.lower() != "padding", f'"{record_name}": Remove Padding which is taken care by program'

    assert col_f_value.lower() != "timestamp", \
        f'"{record_name}" => "{col_f_value}": ' \
        'The field name timestamp is used in TimestampedBitFieldContainerMixin line 1090.  ' \
        'The tool recommends to alter your field name like "Timestamp Value".'

    if row[TestDesignDocument.COL_G] == "bool":
        assert int(row[TestDesignDocument.COL_E]) == 1, f'"{record_name}" => "{col_f_value}": field size should be 1'
    elif row[TestDesignDocument.COL_G] == "Reserved":
        assert col_f_value.startswith("Reserved"), \
            f'"{record_name}" => "{col_f_value}": name should start with keyword "Reserved"'
    # end if
# end def assert_field_values


def get_parser():
    """
    Get argument parser

    :return: Argument parser
    :rtype: ``ArgumentParser``
    """
    parser = ArgumentParser(description="Access the Google Spreadsheet for the given feature id")
    parser.add_argument('--version', action='version', version=ConstantTextManager.TOOL_VERSION)
    parser.add_argument('-f', '--feature', dest='feature', help='Provide the Hid++ Feature ID as input')
    parser.add_argument('-g', '--generate', dest='generate', help='skip generate code',
                        default=False, action='store_true')
    parser.add_argument('-p', '--pull', dest='pull', help='skip pull code',
                        default=False, action='store_true')
    parser.add_argument('-t', '--testcase', dest='testcase', help='skip test case (if pulled from backend)',
                        default=False, action='store_true')
    parser.add_argument('-o', '--objref', dest='object_reference', default='IMPORT_SECTION',
                        help='The class name reference format', choices=['IMPORT_SECTION', 'NAME_WITH_PATH'])
    return parser
# end def get_parser


def get_feature_id():
    """
    Get the feature id from the arguments

    :return: Feature identifier
    :rtype: ``tuple[str, argparse.Namespace]``
    """
    parser = get_parser()
    args = parser.parse_args()
    if not args.feature:
        parser.error("Feature id is mandatory. Run again in format -f 0x0007")
    # end if
    feature_id = args.feature.upper()
    if not feature_id.startswith("0X"):
        parser.error("Start the feature id with 0x")
    elif len(feature_id) != 6:
        parser.error("Feature id should be 4 characters")
    # end if
    # store FeatureId in the dictionary for other place usages.
    FeatureInfo["FeatureId"] = feature_id
    return feature_id, args
# end def get_feature_id


def get_sheet_id(service, feature_id, skip_test_case):
    """
    Get the spreadsheet id for the given feature id.

    :param service: Google API service
    :type service: ``googleapiclient.discovery.Resource``
    :param feature_id: Feature identifier
    :type feature_id: ``str``
    :param skip_test_case: Flag indicating if this test case can be skipped
    :type skip_test_case: ``bool``

    :return: Sheet id of test design & test case documents
    :rtype: ``dict | None``

    :raise ``AssertionError``: Assert spreadsheet values that raise an exception
    """
    # noinspection PyUnresolvedReferences
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=CODE_GENERATION_TOOL_SHEET_ID, range=MAP_RANGE).execute()
    values = result.get('values', [])

    assert values is not None

    for row in values:
        if len(row) < CodeGenerationMap.COL_B:
            sys.stdout.write(f"\nA blank line is found in map. Verify and remove in {CODE_GENERATION_TOOL_SHEET_URL}\n")
            return
        # end if
        if len(row) < CodeGenerationMap.COL_C:
            sys.stdout.write(
                f"\nFeature id is not in then map. Verify and add in {CODE_GENERATION_TOOL_SHEET_URL}\n")
            return
        # end if
        if len(row) < CodeGenerationMap.COL_D:
            sys.stdout.write(
                f"\nTest design document id is not in then map. Verify and add in {CODE_GENERATION_TOOL_SHEET_URL}\n")
            return
        # end if
        if row[CodeGenerationMap.COL_B].upper() != feature_id:
            continue
        # end if
        if len(row) > CodeGenerationMap.COL_D:
            return dict(TestDesignDocument=row[CodeGenerationMap.COL_C], TestCaseDocument=row[CodeGenerationMap.COL_D])
        # end if
        if skip_test_case:
            return dict(TestDesignDocument=row[CodeGenerationMap.COL_C], TestCaseDocument="")
        # end if
        sys.stdout.write(
            f"\nTest case document id is not in then map."
            f"\n\tOption 1: Run the program again with skip test case [-t or --testcase]"
            f"\n\tOption 2: Verify and add in {CODE_GENERATION_TOOL_SHEET_URL}")
        return
    # end for
    sys.stdout.write(f"\nFeature id is not in the map. Verify and add in {CODE_GENERATION_TOOL_SHEET_URL}")
# end def get_sheet_id


def main():
    """
    Define main operations on the Google spreadsheet
    """
    feature_id, args = get_feature_id()

    # Should pull from the backend?
    if not args.pull:
        sys.stdout.write("\nAuthenticate google login")
        credential = authenticate()

        sys.stdout.write("\nGet google service api v4 for spreadsheets")
        service = build('sheets', 'v4', credentials=credential)

        sys.stdout.write("\nAccess [Map] tab from code generation tool document")
        sheet_id = get_sheet_id(service, feature_id, args.testcase)
        if sheet_id is None:
            return
        # end if

        sys.stdout.write("\nAccess [Feature Info] [API Info] [Event Info] tabs from test design document")
        import_text, event_text = get_event_info(service, sheet_id["TestDesignDocument"])
        # Execution Order 1
        feature_info = get_feature_info(service, sheet_id["TestDesignDocument"])
        function_info = get_function_info(service, sheet_id["TestDesignDocument"])
        if args.testcase:
            test_case_info = Template(UserInputTemplate.TEST_CASE_INFO_TEXT).substitute(
                dict(
                    Business="",
                    ErrorHandling="",
                    Functionality="",
                    Interface="",
                    Robustness="",
                    Security="",
                    Performance="",
                    Setup="",
                    Teardown=""
                ))
        else:
            feature_name = FeatureInfo["FeatureName"]
            sys.stdout.write(f"\nAccess [{feature_name}] tab from test case document")
            # Execution Order 2 (depends on previous order result)
            test_case_info = get_test_case_document_info(service, sheet_id["TestCaseDocument"])
            if test_case_info is None:
                return
            # end if
        # end if
        status = FileManager.write_file(
            file_name="../input/userinput.py",
            data=[Template(UserInputTemplate.FILE_TEXT).substitute(
                dict(
                    DateValue=str(datetime.date.today()),
                    EventInfo=event_text,
                    FeatureInfo=feature_info,
                    FunctionInfo=function_info,
                    ImportEvent=import_text,
                    ObjectReference=args.object_reference,
                    TestCaseInfo=test_case_info))])
        if not status:
            return
        # end if
    # end if

    # Should generate the code?
    if not args.generate:
        os.chdir("..")
        # noinspection PyUnresolvedReferences
        from codegenerator.main import CodeGenerator

        sys.stdout.write("\n\nGenerate code")
        CodeGenerator().generate()
        sys.stdout.write("\nReset file: input/userinput.py -> ")
        os.system("git checkout input/userinput.py")
    # end if
    sys.stdout.write("\nProcess completed\n")
# end def main


# ----------------------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
