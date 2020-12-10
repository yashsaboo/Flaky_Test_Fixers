import os, sys
from subprocess import check_output
from subprocess import PIPE,Popen
import json 
import argparse
import os.path

"""
Available Flags
    '-if', '--input_file', 
    '-of', '--output_file',
    '-tp', '--tests_path'
"""
def parse_options():
    '''Gets command line arguments'''
    parser = argparse.ArgumentParser(description='Get cleaners for the polluters of the flaky test')
    parser.add_argument('-if', '--input_file', help='This specifies the input filename whic has been generated from polluterMinimiser.')
    parser.add_argument('-of', '--output_file', help='This specifies the output filename.')
    parser.add_argument('-tp', '--tests_path', help='This is the directory path for tests to be ran. It is relative to where the script is being run from. If this flag is not on the the tests will be looked in the current directory')
    return parser.parse_args()

def executeTests(args, listOfTests):
    argumentVal = ['pytest', '-v']
    
    for test in listOfTests:
        # print(str(test).strip())
        argumentVal.append(str(args.tests_path+test).strip())
    # print(argumentVal)
    testRunOutput = Popen(argumentVal,stdout=PIPE)
    testRunOutput = testRunOutput.communicate()[0]
    # print(testRunOutput.decode("utf-8"))
    return testRunOutput.decode("utf-8")

def find_cleaner(args):

    if args.input_file is None or not os.path.isfile(args.input_file):
        print("Invalid Input File")
        return

    if args.tests_path is None:
        args.tests_path = ""
    elif not os.path.exists(args.tests_path):
        print("Invalid Test Directory Path")
        return

    # Stores the "original_test_name": { "order" = [list of tests], "polluter" = [list of tests], "sofware_defect" = True/False}
    outputDict = {}

    with open(args.input_file, "r") as inputPolluterFile:
        polluter_log_data = json.load(inputPolluterFile)
        # print(polluter_log_data)

        # Get the flaky tests
        list_of_flaky_tests = []
        for keys in polluter_log_data:
            if isinstance(polluter_log_data[keys],dict):
                list_of_flaky_tests.append(keys)
                outputDict[keys] = {}
        print(list_of_flaky_tests)

        list_of_tests = polluter_log_data["list_of_tests_ran"]

        # Stores the "original_test_name": { "flaky_failed_order" = [list of tests], "polluter" = [list of tests], "cleaner" = test_name}
        outputDict = polluter_log_data

        # Get the order in which the test fails
        for flaky_test in list_of_flaky_tests:
            polluter_test_order = polluter_log_data[flaky_test]["polluter"]
            outputDict[flaky_test]["cleaner"] = ""
            for test in list_of_tests:
                if test != flaky_test and test not in polluter_test_order:
                    testRunOutput = executeTests(args, polluter_test_order + [test] + [flaky_test])
                    print(testRunOutput)
                    if testRunOutput.find(flaky_test + ' PASSED') != -1:
                        print("Cleaner Found")
                        outputDict[flaky_test]["cleaner"] = test
                        break
                    else:
                        print("Cleaner Not Found")

            
    #Export the flaky test log data to file
    try:
        with open(args.output_file,"w+") as f:
            json.dump(outputDict,f)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except: #handle other exceptions such as attribute errors
        print('Unexpected error raised by pytest-random-order plugin: {}. {}, line: {}'.format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))

if __name__ == '__main__':
    args = parse_options()
    print(args)
    find_cleaner(args)