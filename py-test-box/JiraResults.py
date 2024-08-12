'''
This file extracts list of known issue from Jira

IMPORTANT: a text file named "credentials.txt" is needed in the same directory. Only the *second* line is taken into
consideration. It shall contains the username and the jira token of the user  separated by a white space:
<username> <TOKEN>

Do not commit this files as it contains secure and personal info!

Depends on "jira" (pip3 install jira)

CUSTOMIZATION:
 - 'PROJECT_KEY': name of the Jira project to consider
 - 'features': mapping between high level features and Jira epics
 '''

from jira import JIRA


JIRA_HOST = u"https://jira.logitech.io"
CREDENTIALS_FILENAME = "credentials.txt"

PROJECT_KEY = "BPRO"

Feature = {"BLE PRO - Platform Improvements": "Platform",
           "BLE PRO - Pairing": "Pairing",
           "BLE PRO - Connection Scheme": "Connection Scheme",
           "BLE PRO - Receiver DFU":  "DFU receiver",
           "BLE PRO - Peripheral DFU": "DFU device",
           "BLE PRO - Secure DFU": "DFU Protection",
           "BLE PRO - TDE / Gothard / Compliance Protection": "TDE Commands",
           "BLE PRO - TDE": "TDE Protection",
           "BLE PRO - Mezzy core features": "Mezzie",
           "BLE PRO - Zaha": "Zaha BLE PRO",
           "BLE PRO - Honolulu": "Honolulu BLE PRO",
           "BLE PRO - Heka": "Honolulu BLE PRO",
           "BLE PRO - Herzog": "Herzog BLE PRO",
           "BLE PRO - Foster": "Foster BLE PRO",
           }


if __name__ == "__main__":
    # -- get credentials and connect to jira
    with open(CREDENTIALS_FILENAME, "r") as f:
        f.readline()
        (username, token) = f.readline().split(" ")
    try:
        jira = JIRA(server=JIRA_HOST, auth=(username, token))

    except Exception as e:
        token = ""
        username = ""
        raise e

    # get project PROJECT_KEYS
    projects = jira.projects()

    for p in projects:
        if str(p) == PROJECT_KEY:
            project = p
            break

    if project is None:
        print("cannot find project {} in {}".format(JIRA_HOST, PROJECT_KEY))
        raise NameError()

    # get list of epics
    epic_keys = [(t.key, t.fields.summary) for t in jira.search_issues("project={} and type='Epic'".format(PROJECT_KEY))]
    lkp = {}

    # get list of open bugs per epic
    for epic in epic_keys:
        f = Feature[epic[1]] if epic[1] in Feature else "UNMAPPED {}".format(epic[1])
        lkp[f] = [t.key for t in jira.search_issues("'Epic Link'={} and status!=Done and type=Bug".format(epic[0]))]
    lkp["UNMAPPED"] = jira.search_issues("Project={} and 'Epic Link'=None and status!=Done and type=Bug".format(PROJECT_KEY,
                                                                                                                epic_keys[0]))

    # get all opened and closed bugs
    opened_bugs = jira.search_issues("project={} and type=Bug".format(PROJECT_KEY))
    closed_bugs = jira.search_issues("project={} and type=Bug and status=Done".format(PROJECT_KEY))

    # display results
    title = "Bugs reporting"
    print("\n{}\n{}".format(title, "=" * len(title)))
    print("total opened: {:3}".format(len(opened_bugs)))
    print("total closed: {:3}".format(len(closed_bugs)))
    print("")
    for k,v in lkp.items():
        print(" - {}: {}".format(k, v))
