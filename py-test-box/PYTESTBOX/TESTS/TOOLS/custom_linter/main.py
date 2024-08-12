#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: custom_linter.main
:brief: main script for custom linter
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/03/09
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import re
from argparse import ArgumentParser
from pathlib import Path
from sys import stdout


try:
    import pylint.lint
    from git import Repo
    from pylint.reporters import CollectingReporter
    from pylint.reporters import MultiReporter
    from pylint.reporters.text import TextReporter
except ModuleNotFoundError:
    from sys import stderr
    from sys import exit
    print(
        "For local interpreter, install linting requirements:"
        " 'pip install -r PYTESTBOX/TESTS/TOOLS/custom_linter/lint_requirements.txt'", file=stderr)
    exit(-1)
# end try


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
# for each pattern on the path, give a list of enabled messages
ENABLED_CONFIG = {
    r".*" : ["end-comments","docstring_checker","encoding_checker"],
    r"^.*PYTESTBOX(\\|\/)TESTS(\\|\/)TESTSUITES(\\|\/)pytestbox.*": ["decorator-order-checker"],
}

# Never lint files that match this regex
GLOBAL_EXCLUDE_REGEX = r"^.*pylint_test_data.*$"

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
def run_linter(source, file=False, fix=False):
    """
    Run the linter
    :param source: source code to analyse, can be a raw string(s) of python code or a
    list of file paths depending on the file flag
    :type source: ``str`` or ``list[str]``
    :param file: flag indicating if the linter is expecting flag paths - OPTIONAL
    :type file: ``bool``
    :param fix: flag indicating if the linter will attempt to fix directly the code instead of raising warning - OPTIONAL
    :type fix: ``bool``
    """
    stdout.write(f"Linter running with args: source={source}, file={file}, fix={fix}\n")
    passes = dict()

    if file:
        source_absolute = set()

        # extend directories in source to a list of files
        for path_of_list in source:
            path_object = path_of_list if isinstance(path_of_list, Path) else Path(path_of_list)
            if path_object.is_file():
                source_absolute.add(str(path_object.absolute()))
            elif path_object.is_dir():
                for python_file in path_object.rglob("*.py"):
                    source_absolute.add(str(python_file.absolute()))
                # end for
            else:
                stdout.write(f"path: {path_object.absolute()} was ignored due to being unsupported\n")
            # end if
        # end for

        # match each file of the extended list to configs to determine which checkers to enable
        for path in source_absolute:
            enabled_for_path = []
            for pattern, config in ENABLED_CONFIG.items():
                if re.match(pattern, path) and not re.match(GLOBAL_EXCLUDE_REGEX, path):
                    enabled_for_path.extend(config)
                # end if
            # end for
            enabled_str = ','.join(enabled_for_path)
            if enabled_str in passes.keys():
                passes[enabled_str].append(path)
            elif enabled_str != "":
                passes[enabled_str] = [path]
            # end if
        # end for
    else:
        stdout.write("direct code linter not implemented\n")
        return
    # end if

    stdout.write(f"current config need to do {len(passes)} pass(es)\n")
    collecting_reporter = CollectingReporter()
    print_reporter = TextReporter()
    reporter = MultiReporter([collecting_reporter, print_reporter], close_output_files=lambda: None)
    for config, source_for_pass in passes.items():
        source_for_pass.sort()
        stdout.write(f"Checking: {config}\n for {source_for_pass}\n")
        pylint_obs = ["--disable=all", f"--enable={config}",
                      *source_for_pass]
        # following comment disable type checking, ``MultiReporter`` is compatible but not explicitly a ``BaseReporter``
        # noinspection PyTypeChecker
        pylint.lint.Run(pylint_obs, exit=False, reporter=reporter)
    # end for

    if fix:
        stdout.write("Fix not applied, not implemented\n")
    # end if

    # exit based on the message reported for CI
    exit_code = 0
    # if there is any error or fatal message, exit with -1
    for msg in collecting_reporter.messages:
        if msg.msg_id.startswith("E") or msg.msg_id.startswith("F"):
            exit_code = -1
            break
        # end if
    # end for
    exit(exit_code)
# end def run_linter


def current_repo():
    """
    find the current repository in which this script is situated.

    :return: the repository object, and the root path
    :rtype: ``tuple[Repo, str]``
    """
    repository = Repo(search_parent_directories=True)
    git_root_path = repository.git.rev_parse("--show-toplevel") + '/'
    return repository, git_root_path
# end def current_repo


# ----------------------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    parser = ArgumentParser(
        prog='CustomLinter',
        description='A custom linter for pytestbox coding style',
        epilog='work in progress, use with supervision')

    parser.add_argument('-f', '--file', nargs='+')
    parser.add_argument('-r', '--raw')
    parser.add_argument('-b', '--branch')
    parser.add_argument('-p', '--pattern')
    parser.add_argument('--fix', action='store_true')

    args = parser.parse_args()
    repo, git_root = current_repo()

    os.chdir(git_root)

    files = [f for f in os.listdir('.') if os.path.isfile(f)]

    if args.file is not None:
        run_linter(source=[*args.file], file=True, fix=args.fix)
    elif args.raw is not None:
        run_linter(source=[args.raw], file=False, fix=args.fix)
    elif args.pattern is not None:
        files = [str(path) for path in Path(".").rglob(args.pattern)]
        run_linter(source=files, file=True, fix=args.fix)
    else:
        # if branch is set, compare with the branch (change on both side) otherwise compare staged
        changedFiles = [item.a_path for item in repo.index.diff(args.branch)]
        if len(changedFiles) == 0:
            stdout.write("No changes\n")
        else:
            run_linter(source=changedFiles, file=True, fix=args.fix)
        # end if
    # end if
# end if


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
