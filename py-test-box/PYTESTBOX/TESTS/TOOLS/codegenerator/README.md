# Code Generation Tool

### [Presentation](https://docs.google.com/presentation/d/1vR-QnqTAsNCqr_8jXxQRuu3mP-W5g2HJTBIyR6tvEdQ/view)
### [Documentation](https://docs.google.com/document/d/1Ywx3AR8q7_9pSB-FaNRse7kSp02HSGrFukUQIK3RCE8/view)
### [Documentation for fields](https://docs.google.com/spreadsheets/d/1TO4UOiJ7zWza0wuIIOrqqig43kEY-Tm2O0cgQmEQ-TU/view#gid=1209747976)

# Section 1: What type of files generated?
The tool generates set of files.

In the below example,

- **Manual** refers to the file written by any author.

- **Tool** refers to the file written by this code generation tool.

Folder location and file name given are for a given example (0007: DeviceFriendlyName).

Actual folder & file name will vary based on the feature id.

#### Version 1.0
- LIBS: Feature Test File
    - **Manual**: PYTESTBOX/LIBS/PYHID/pyhid/hidpp/features/common/devicefriendlyname.py
    - **Tool**: PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/LIBS/PYHID/pyhid/hidpp/features/common/devicefriendlyname.py
- LIBS: Feature Unitary Test File
    - **Manual**: PYTESTBOX/LIBS/PYHID/pyhid/hidpp/features/common/test/devicefriendlyname_test.py
    - **Tool**: PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/LIBS/PYHID/pyhid/hidpp/features/common/test/devicefriendlyname_test.py
- LIBS: Hid Dispatcher File Registration
    - **Manual**: PYTESTBOX/LIBS/PYHID/pyhid/hiddispatcher.py
    - **Tool**: PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/LIBS/PYHID/pyhid/hiddispatcher.py
- Settings: Product Settings
    - **Manual**: PYTESTBOX/TESTS/SETTINGS/PYTESTBOX/PRODUCT/STM32L100/SCHUMACHER/SCHUMACHER.settings.ini
    - **Tool**: PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/TESTS/SETTINGS/SPECIFIC_PRODUCT.settings.ini
- Test Suite: Feature SubSystem
    - **Manual**: PYTESTBOX/TESTS/TESTSUITES/pytestbox/base/features.py
    - **Tool**: PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/TESTS/TESTSUITES/pytestbox/base/features.py
- Test Suite: Feature Utility
    - **Manual**: PYTESTBOX/TESTS/TESTSUITES/pytestbox/device/base/devicefriendlynameutils.py
    - **Tool**: PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/TESTS/TESTSUITES/pytestbox/device/base/devicefriendlynameutils.py
- Test Suite: Feature Package
    - **Manual**: PYTESTBOX/TESTS/TESTSUITES/pytestbox/device/hidpp20/common/feature_0007
    - **Tool** : PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/TESTS/TESTSUITES/pytestbox/device/hidpp20/common/feature_0007
        - \_\_init\_\_.py
        - devicefriendlyname.py
        - business.py
        - errorhandling.py
        - functionality.py
        - interface.py
        - robustness.py
        - testrunner.py

#### Version 1.2
- Test Suite: Feature Package
    - **Manual**: PYTESTBOX/TESTS/TESTSUITES/pytestbox/device/hidpp20/common/feature_0007
    - **Tool** : PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/TESTS/TESTSUITES/pytestbox/device/hidpp20/common/feature_0007
        - performance.py
        - security.py

#### Version 1.3
- Test Suite: Feature Registration
    - **Manual**: PYTESTBOX/TESTS/TESTSUITES/pytestbox/base/registration.py
    - **Tool**: PYTESTBOX/TESTS/TOOLS/codegenerator/**output**/TESTS/TESTSUITES/pytestbox/base/registration.py

[Reference 1: Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)

[Reference 2: Create a project and enable the API](https://developers.google.com/workspace/guides/create-project)

## Section 2: How to configure ``Google Sheets API``
Note:
- This has to be configured only once.
- The below steps were done already by Suresh Thiyagarajan and documented here for understanding purpose.
- To run the tool, every user has to download the client_secret.json (refer step 3).
- Open the [Google Cloud Console](https://console.cloud.google.com/).

#### Step 1: Enable a Google Workspace API
- Next to "Google Cloud Platform," click the Down arrow and select a project.
    - Choose **``LOGITECH.COM``** in the ``select from`` drop down list.
    - From the ``Recent`` tab, select the already created project ``MyAuthentication (myauthentication-7dffd)``.
      - If you do not see the project, please send a mail
        to ``sthiyagarajan@logitech.com`` to get your email id added to the project.
    - Click ``OPEN`` button.
- Below actions are already done (No action required)
  - In the top-left corner, click ``Menu > APIs & Services > Dashboard``.
  - Click ``Enable APIs and Services``. The Welcome to API Library page appears.
  - In the search field, enter the name of the API you want to enable.
  For example, type ``Google sheet api`` to find the Google Sheet API.
  - Click the API to enable. The API page appears.
  - Click Enable. The Overview page appears.

#### Step 2: Credentials
Credentials are used to obtain an access token from a Google authorization server.
- This token is used to call Google Workspace APIs.
- The type of credentials you use depends on the type of data your app accesses.
- All Google Workspace APIs access data owned by the end-user.
- You can use either an OAuth client ID or a service account with domain delegation of authority to access user data.

To configure the OAuth consent screen:
- Open the Google Cloud Console.
- Next to Google Cloud Platform, click the Down arrow and select the project ``MyAuthentication``.
- Click ``Menu`` from the top-left corner.
- Click ``APIs & Services > Credentials``.
- The credential page for your project appears.

#### Step 3 Create/Download Desktop application credentials
If you're creating Desktop application credentials:
- Below actions are already done (No action required)
  - Click Create Credentials. Select OAuth Client ID. The OAuth client created screen appears.
  - Select the Application Type ``Desktop app``.
  - Provide a name for the app ``Code Generation Tool``.
  - Click Create.
  - This screen shows the Client ID and Client secret.
  - Click OK. The newly created credential appears under "OAuth 2.0 Client IDs".
- Download the secret file (action required)
  - Click the download button to the right of the newly-created OAuth 2.0 Client ID.
  - This copies a client secret JSON file to your desktop.
  - Note the location of this file.
  - (Optional) Rename the client secret JSON file to "client_secret.json".
  - Copy the downloaded file to this ``[PYTESTBOX/TESTS/TOOLS/codegenerator/source]`` folder location.

## Section 3: How to access ``Test Design & Test Case Spec Documents``

Pre-requisite: Install the Google client library

`pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

Auto generate PYTESTBOX/TESTS/TOOLS/codegenerator/input/UserInput.py

1. Open console and go to directory ``PYTESTBOX/TESTS/TOOLS/codegenerator/source``
2. Run ``python3 spreadsheet.py -f 0x<FeatureId>``
3. For more information run ``python3 spreadsheet.py -h``

Note:

- Remove token.json anytime if you want to re-authenticate.
- If token.json does not exist or expired, a browser window will open and ask you to authenticate the project '
  MyAuthentication'.
- Allow the project with your credentials.
- Close the browser.
- Re-run the spreadsheet.py if required.

## Section 4: Output
What next with the output files.

---
Three type of files are generated.

1. `File which is partially exist`

    Ex: hiddispatcher.py and features.py

    The tool generates only related the hidpp feature. You have to copy/paste the code in respective place.

2. `File which is fully exist`

    Ex: devicefriendlyname.py

    Assume the feature is already available in the develop branch. In case you re-run the tool for latest changes,
    the target files will be already available.
    In such scenario, use a text file comparison tool like [diffmerge](https://sourcegear.com/diffmerge/webhelp/chapter_introduction.html).

3. `File which does not exist`

    Ex: All files except hiddispatcher.py and features.py

    Assume the feature is not already available in the develop branch. When the tool is run for first time,
    the target files will not be available.
    In such scenario, copy the files to the target location.
---

#### Section 5: THANK YOU

**THANK YOU FOR USING THIS ``CODE GENERATION TOOL`` AND FEEL FREE TO CONTACT ``(Suresh Thiyagarajan <sthiyagarajan@logitech.com)``
FOR BUGS/FEATURES/IMPROVEMENT/IDEAS ON THIS TOOL.**
