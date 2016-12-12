"""Main point of entrance to the application"""

import os
import sys

from golem.core import utils, cli, test_runner, test_execution
from golem.gui import gui_start


def execute_from_command_line(root_path):

    parser = cli.get_golem_parser()
    args = parser.parse_args()

    # set test_execution values
    test_execution.root_path = root_path
    test_execution.settings = utils.get_global_settings()

    import golem.core
    golem.core.temp = test_execution.settings
    # main action == gui
    if args.main_action == 'gui':
        gui_start.run_gui()
        sys.exit()

    # main action == run
    if args.main_action == 'run':
        test_execution.thread_amount = args.threads
        test_execution.settings['driver'] = args.driver
        if not args.project:
            print('Usage:', parser.usage, '\n\n', 'Project List:')
            for proj in utils.get_projects(root_path):
                print('> {}'.format(proj))
            sys.exit()
        # check if selected project does not exist
        elif not args.project in utils.get_projects(root_path):
            sys.exit('Error: the project {0} does not exist'
                     .format(test_execution.project))
        else:
            test_execution.project = args.project
            test_execution.settings = utils.get_project_settings(
                                                    args.project,
                                                    test_execution.settings)

            # check if test_or_suite value is present
            if not args.test_or_suite:
                print('Usage:', parser.usage)
                print('\nTest Cases:')
                test_cases = utils.get_test_cases(root_path,
                                                  test_execution.project)
                utils.display_tree_structure_command_line(test_cases)
                print('\nTest Suites:')
                test_suites = utils.get_suites(root_path,
                                               test_execution.project)
                utils.display_tree_structure_command_line(test_suites)
                sys.exit()

            # check if test_or_suite value matches an existing test suite
            elif utils.test_suite_exists(root_path,
                                       test_execution.project,
                                       args.test_or_suite):
                test_execution.suite = args.test_or_suite
                # execute test suite
                test_runner.run_suite(root_path,
                                      test_execution.project,
                                      test_execution.suite)

            # check if test_or_suite value matches a first level directory
            # in the test cases directory. this allows to execute all the 
            # test cases in a directory as a test suite

            elif utils.is_first_level_directory(root_path,
                                                test_execution.project,
                                                args.test_or_suite):
                test_execution.suite = args.test_or_suite
                # execute test suite
                test_runner.run_suite(root_path,
                                      test_execution.project,
                                      test_execution.suite,
                                      is_directory=True)

            # check if test_or_suite value matches an existing test case
            elif utils.test_case_exists(root_path,
                                        test_execution.project,
                                        args.test_or_suite):
                test_execution.test = args.test_or_suite
                # execute test case
                test_runner.run_single_test_case(root_path,
                                                 test_execution.project,
                                                 test_execution.test)
            
            else:
                # test_or_suite does not match any existing suite or test
                sys.exit('Error: the value {0} does not match an existing '
                         'suite or test'
                         .format(args.test_or_suite))

    # main action == startproject
    if args.main_action == 'startproject':
        if args.project in utils.get_projects(root_path):
            sys.exit('Error: a project with that name already exists'
                     .format(args.project))
        else:
            utils.create_new_project(root_path, args.project)

    # main action == createuser
    if args.main_action == 'createuser':
        sys.exit('To be defined')
        