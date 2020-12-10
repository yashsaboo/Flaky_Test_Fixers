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
    parser = argparse.ArgumentParser(description='Get minimised polluters')
    parser.add_argument('-if', '--input_file', help='This specifies the input filename which is generated using pytest-random-order flaky-test-finder capability.')
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

def minimize_polluters(args):

    if args.input_file is None or not os.path.isfile(args.input_file):
        print("Invalid Input File")
        return

    if args.tests_path is None:
        args.tests_path = ""
    elif not os.path.exists(args.tests_path):
        print("Invalid Test Directory Path")
        return

    # Stores the "original_test_name": { "flaky_failed_order" = [list of tests], "polluter" = [list of tests], "sofware_defect" = True/False}
    outputDict = {}

    with open(args.input_file, "r") as inputFlakyTestListFile:
        flaky_test_log_data = json.load(inputFlakyTestListFile)
        # print(flaky_test_log_data)

        # Get the flaky tests
        list_of_flaky_tests = []
        for keys in flaky_test_log_data:
            if isinstance(flaky_test_log_data[keys],dict):
                list_of_flaky_tests.append(keys)
                outputDict[keys] = {}
        print(list_of_flaky_tests)

        # Get the order in which the test fails
        for flaky_test in list_of_flaky_tests:
            for runs in flaky_test_log_data[flaky_test]:
                if flaky_test_log_data[flaky_test][runs]['outcome'] == 'failed': #Get the failed order
                    failed_order = flaky_test_log_data[flaky_test][runs]['order']
                    outputDict[flaky_test]["flaky_failed_order"] = flaky_test_log_data[flaky_test][runs]['order']
                    # Isolation Check for Flaky test or software defect
                    testRunOutput = executeTests(args,[flaky_test])
                    print(testRunOutput)

                    if testRunOutput.find('1 passed') != -1:
                        print(flaky_test.strip() + " is NOT a Software Defect")
                        outputDict[flaky_test]["sofware_defect"] = False
                    else:
                        print(flaky_test.strip() + " is a Software Defect")
                        outputDict[flaky_test]["sofware_defect"] = True

                    print("Isolation Check done")

                    # Perform Binary Search to minimise the set of polluters
                    # print("flaky_test:", flaky_test)
                    try:
                        print("failed_order:",failed_order)
                        flakyTestIndexInTestOrder = int(failed_order.index(flaky_test))
                        print("::::::::::::::::::::::::::::::::::flakyTestIndexInTestOrder:",flakyTestIndexInTestOrder)
                        
                        #Perform Binary Search = lb - Lower Bound, ub - Upper bound 
                        lb = 0
                        ub = flakyTestIndexInTestOrder-1
                        while(lb<=ub):
                            mid = int(lb + (ub-lb)/2)
                            
                            testRunOutput = executeTests(args,failed_order[mid:flakyTestIndexInTestOrder+1])
                            print("\nxxxxxxxxxxxxxxxxxxxxxxxxx")
                            print(testRunOutput)
                            print("\nxxxxxxxxxxxxxxxxxxxxxxxxx")

                            if testRunOutput.find(flaky_test + ' PASSED') != -1:
                                ub = mid - 1
                            else:
                                lb = mid + 1

                        # print("Lower Bound:", lb)

                        outputDict[flaky_test]["polluter"] = failed_order[lb-1:flakyTestIndexInTestOrder]
                        print("--------------------outputDict[flaky_test][polluter]:",outputDict[flaky_test]["polluter"])

                    except ValueError:
                        print(flaky_test + " is not present in the test order")

                    print()
                    print("-------------------------------------------------")

                print("Binary Search done")

        # add additional fields to the logged dictionary: "list_of_tests_ran", "random_order_seed", "random_order_bucket", flaky_test_repeat_count"
        outputDict["list_of_tests_ran"] =  flaky_test_log_data["list_of_tests_ran"]
        outputDict["random_order_seed"] = flaky_test_log_data["random_order_seed"]
        outputDict["random_order_bucket"] = flaky_test_log_data["random_order_bucket"]
        outputDict["flaky_test_finder"] = flaky_test_log_data["flaky_test_finder"]

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
    minimize_polluters(args)