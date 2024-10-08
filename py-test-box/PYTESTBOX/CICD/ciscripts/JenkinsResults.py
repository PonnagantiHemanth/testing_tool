"""
This file parse Jenkins latest test results (complete build) and extracts the amount of passed / failed / skipped
tests which are then presented as high level features

IMPORTANT: a text file named "credentials.txt" is needed in the same directory. Only the fisrt line is taken into
consideration. It shall contains the username (inc. @logitech.com) and the jenkins token of the user (17 bytes),
separated by a white space:
<user@logitech.ch> <TOKEN>

Do not commit this files as it contains secure and personal token!

Token can be generated in generated by clicking on the username (top left) > Configure > API token

Depends on "jenkinsapi" (pip3 install jenkinsapi)

CUSTOMIZATION:
 - 'jobs': list of jobs to consider to extract info (name + optional build_number)
 - 'features': mapping between high level features and the tests it contains
"""

import itertools
import re
from jenkinsapi.jenkins import Jenkins

JENKINS_HOST = "http://pytestbox.logitech.com:8080/"
CREDENTIALS_FILENAME = "credentials.txt"


class Job(object):
    def __init__(self, name, build_number=None):
        self.name = name
        self.build_number = build_number
    # end def __init__
# end class Job


class Feature(object):
    def __init__(self, tests):
        self.tests = tests
        self.passed = None
        self.failed = None
        self.skipped = None
    # end def __init__

    def reset(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
    # end def reset
# end class Feature


# --- Parameters

jobs = [Job('RECEIVERS/MEZZY/BLE_PRO/Master_Validation', build_number=237),
        Job('PRODUCTS/ZAHA_BLE_PRO/Master_Validation', build_number=41),
        Job('PRODUCTS/HERZOG_BLE_PRO/Master_Validation', build_number=16),
        Job('PRODUCTS/FOSTER_BLE_PRO/Mezzy_Integration', build_number=15),
        Job('PRODUCTS/HONOLULU_BLE_PRO/Master_Validation', build_number=23),
             ]


features = {"Legacy": Feature(["pytestbox.*.hidpp20.important.feature_0000",
                               "pytestbox.*.hidpp20.important.feature_0001",
                               "pytestbox.*.hidpp20.common.feature_0003",
                               "pytestbox.*.hidpp20.common.feature_0005",
                               "pytestbox.*.hidpp20.common.feature_0020",
                               "pytestbox.*.hidpp20.common.feature_0021",
                               "pytestbox.*.hidpp20.common.feature_00C2",
                               "pytestbox.*.hidpp20.common.feature_1D4B",
                               "pytestbox.device.hidpp20.common.feature_1000",
                               "pytestbox.device.hidpp20.common.feature_1004",
                               "pytestbox.device.hidpp20.common.feature_1802",
                               "pytestbox.device.hidpp20.common.feature_1814",
                               "pytestbox.device.hidpp20.common.feature_1830",
                               "pytestbox.device.hidpp20.common.feature_1861",
                               "pytestbox.device.hidpp20.common.feature_1B04",
                               "pytestbox.device.hidpp20.common.feature_1E00",
                               "pytestbox.device.hidpp20.mouse",
                               "pytestbox.device.hidpp20.keyboard",
                               "pytestbox.device.hidpp20.gaming",
                               "pytestbox.device.hidpp20.debounce",
                               "pytestbox.timings",
                               ]),
            "Pairing": Feature(["pytestbox.*.connectionscheme.discovery",
                                "pytestbox.receiver.connectionscheme.enumeration",
                                "pytestbox.*.connectionscheme.pairing",
                                "pytestbox.receiver.hidpp.quaddeviceconnection",
                                ]),
            "Connection Scheme": Feature(["pytestbox.*.connectionscheme.connectivity",
                                          "pytestbox.*.connectionscheme.safeprepairedreceiver",
                                          ]),
            "DFU receiver": Feature(["pytestbox.receiver.firmwareupgrade.receiverupgrade",
                                     "pytestbox.receiver.hidpp20.common.feature_00D0",
                                     ]),
            "DFU device": Feature(["pytestbox.device.hidpp20.common.feature_00D0",
                                   "pytestbox.device.recovery.recovery"]
                                  ),
            "DFU Protection": Feature(["pytestbox.*.hidpp20.common.feature_00c3",
                                       ]),
            "TDE Commands": Feature(["pytestbox.receiver.tde.prepairing",
                                     "pytestbox.receiver.tde.tde",
                                     "pytestbox.device.hidpp20.common.feature_1816",
                                     ]),
            "TDE Protection": Feature([]),
            }

if __name__ == '__main__':
    # -- make sure one tests is not assigned to a single feature
    tests = list(itertools.chain(*[f.tests for f in features.values()]))

    duplicated_tests = [x for n, x in enumerate(tests) if x in tests[:n]]
    if duplicated_tests:
        print("The following tests are duplicated: {}".format(duplicated_tests))
        raise ()

    # -- make sure one test is not contains in another test class
    included_tests = [min(x, y) for x in tests for y in tests if (x != y and (y + "." in x or x + "." in y))]
    if included_tests:
        included_tests_no_duplicates = [x for n, x in enumerate(included_tests) if x not in included_tests[:n]]
        print("The following tests is already included into another class {}".format(included_tests_no_duplicates))
        raise ()

    # -- create dictionary tests --> feature ; aim is to speed-up the parsing later
    tests_mapping = dict((x, f[0]) for f in features.items() for x in f[1].tests)

    # -- get credentials and connect to jenkins
    with open(CREDENTIALS_FILENAME, "r") as f:
        (username, token) = f.readline().split(" ")
    try:
        jenkins = Jenkins(JENKINS_HOST, username=username, password=token)
    except Exception as e:
        token = ""
        username = ""
        raise e

    # -- get tests results for each job
    for job in jobs:
        # clean counter
        for key in features.keys():
            features[key].reset()
        jenkins_job = jenkins.get_job(job.name)

        # try to get proposed build ID
        if job.build_number:
            jenkins_build = jenkins_job.get_build(job.build_number)
        else:
            jenkins_build = jenkins_job.get_last_completed_build()
        # end if

        jenkins_results = jenkins_build.get_resultset()

        # for each tests, count how much have passed, failed or has been skipped and keep track of failure
        unknown_status = []
        unmapped_tests = []

        for item in jenkins_results.items():
            for t in tests_mapping.keys():
                regex = re.compile(t)
                if regex.match(item[1].className):
                #if t in item[1].className:
                    if item[1].skipped:
                        features[tests_mapping[t]].skipped += 1
                    elif item[1].status in ["PASSED", "FIXED"]:
                        features[tests_mapping[t]].passed += 1
                    elif item[1].status in ["FAILED", "REGRESSION"]:
                        features[tests_mapping[t]].failed += 1
                    else:
                        unknown_status.append((item[1].status, item[1].className, item[1].name))
                    break
                # end if
            else:
                unmapped_tests.append(item[1].className)
            # enf for t
        # end for item

        # -- display results
        title = "{} ({})".format(jenkins_results, jenkins_build.get_timestamp())
        print("\n{}\n{}".format(title, "=" * len(title)))
        # report all issues at once (unknown status and unmapped tests)
        for us in unknown_status:
            print("unknown status '{}' for test {}.{}".format(us[0], us[1], us[2]))
        for ut in unmapped_tests:
            print("test class '{}' or its parent class is not mapped in the feature list".format(ut))
        if unknown_status or unmapped_tests:
            raise NameError()

        # report results
        DISPLAY_PATTERN = "  {:20}: PASSED = {:4}  -  FAILED = {:4}  -  SKIPPED = {:4}"
        for k, v in features.items():
            print(DISPLAY_PATTERN.format(k,
                                         v.passed,
                                         v.failed,
                                         v.skipped))
        print("  ------------------------------------------------------------------------")
        print(DISPLAY_PATTERN.format("TOTAL",
                                     sum(v.passed for v in features.values()),
                                     sum(v.failed for v in features.values()),
                                     sum(v.skipped for v in features.values())))

# end.
