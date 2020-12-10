# Flaky_Test_Fixers

This new feature is useful for developers who want to fix the flaky tests in pytest framework found by [pytest-random-order](https://pypi.org/project/pytest-random-order/) plugin when `--flaky-test-finder` flag is enabled. 

Currently the plugin is yet to be integrated with the plugin, but can be found [here](https://github.com/yashsaboo/pytest-random-order/tree/add_flaky_test_finder).

## Dependencies

- pytest
```
pip install pytest
```

## Files

### polluter_minimiser
This file helps in minimising list of tests which can be "potential" polluter(s).

#### How to Run
```
python polluterMinimiser.py -if <input_file> -of <output_file> -tp <tests_path>
```

#### Available Flags
```
'-if', '--input_file', 'This specifies the input filename which is generated using pytest-random-order flaky-test-finder capability.'
'-of', '--output_file', 'This specifies the output filename.'
'-tp', '--tests_path', 'This is the directory path for tests to be ran. It is relative to where the script is being run from. If this flag is not on the the tests will be looked in the current directory'
```

#### Test Run On Dummy Example

##### Run
```
python polluterMinimiser.py -if flaky_test.json -of polluter_minimised_file.json
```

##### Input
*flaky_test.json* has the output generated from pytest-random-order flaky-test-finder which has list of flaky tests featuing both the passed order and failed orders. It looks like the following:
```
{
  "dummyPytestFile.py::test_example_3": {
    "run_0": {
      "outcome": "passed",
      "order": [
        "dummyPytestFile.py::test_example_3"
      ]
    },
    "run_1": {
      "outcome": "failed",
      "order": [
        "dummyPytestFile.py::test_example_4",
        "dummyPytestFile.py::test_example_2",
        "dummyPytestFile.py::test_example_1",
        "dummyPytestFile.py::test_example_3"
      ]
    }
  },
  "list_of_tests_ran": [
    "dummyPytestFile.py::test_example_2",
    "dummyPytestFile.py::test_example_1",
    "dummyPytestFile.py::test_example_3",
    "dummyPytestFile.py::test_example_4"
  ],
  "random_order_seed": "309034",
  "random_order_bucket": "module",
  "flaky_test_finder": 2
}
```

##### Output
The output *polluterminimisedfile.json* looks like this which identifies the correct polluter:
```
{
  "dummyPytestFile.py::test_example_3": {
    "flaky_failed_order": [
      "dummyPytestFile.py::test_example_4",
      "dummyPytestFile.py::test_example_2",
      "dummyPytestFile.py::test_example_1",
      "dummyPytestFile.py::test_example_3"
    ],
    "software_defect": false,
    "polluter": [
      "dummyPytestFile.py::test_example_1"
    ]
  },
  "list_of_tests_ran": [
    "dummyPytestFile.py::test_example_2",
    "dummyPytestFile.py::test_example_1",
    "dummyPytestFile.py::test_example_3",
    "dummyPytestFile.py::test_example_4"
  ],
  "random_order_seed": "309034",
  "random_order_bucket": "module",
  "flaky_test_finder": 2
}
```

#### Test Run On xarray
The current commit has no flaky tests since we fixed in our [Pull Request](https://github.com/pydata/xarray/pull/4600). Thus, we tested the functionality on a commit which had flaky test.
##### Flaky Test Commit
```
commit a2192158e3fbb94b2d972ff3e1693fffa65e50be       
Author: keewis <keewis@users.noreply.github.com>
Date:   Fri Nov 20 22:04:20 2020 +0100
```

##### To Run
```
python polluterMinimiser.py -if C:/Users/Yash/Desktop/Courses/CS527/Project/randomOrderForkTestENV/reposToTestPlugin/xarray/xarray/flaky_test.json -of C:/Users/Yash/Desktop/Courses/CS527/Project/randomOrderForkTestENV/reposToTestPlugin/xarray/xarray/polluter_minimised_file.json -tp C:/Users/Yash/Desktop/Courses/CS527/Project/randomOrderForkTestENV/reposToTestPlugin/xarray/
```

##### Input
The input file was created by running pytest-random-order by using the seed: *731984*

##### Output
The output *polluterminimisedfile.json* looks like this which identifies the correct polluter and has also been fixed in our [Pull Request](https://github.com/pydata/xarray/pull/4600):
```
{
  "xarray/tests/test_plot.py::TestImshow::test_origin_overrides_xyincrease": {
    "software_defect": false,
    "polluter": [
      "xarray/tests/test_plot.py::TestAxesKwargs::test_xscale_kwarg"
    ]
  },
  "xarray/tests/test_plot.py::TestContourf::test_colorbar_default_label": {
    "sofware_defect": false,
    "polluter": [
      "xarray/tests/test_plot.py::TestAxesKwargs::test_xscale_kwarg"
    ]
  },
  "list_of_tests_ran": [
    ......<list of tests>........
  ],
  "random_order_seed": "731984",
  "random_order_bucket": "module",
  "flaky_test_finder": 2
}
```

### findCleaner
This file helps in finding cleaners

#### How to Run
```
python findCleaner.py -if <input_file> -of <output_file> -tp <tests_path>
```

#### Available Flags
```
'-if', '--input_file', 'This specifies the input filename whic has been generated from polluterMinimiser.'
'-of', '--output_file', 'This specifies the output filename.'
'-tp', '--tests_path', 'This is the directory path for tests to be ran. It is relative to where the script is being run from. If this flag is not on the the tests will be looked in the current directory'
```

#### Test Run On Dummy Example

##### Run
```
python findCleaner.py -if polluter_minimised_file.json -of cleaner_file.json
```

##### Input
Input is the output from polluter_minimiser

##### Output
The output *cleaner_file.json* looks like this which identifies the correct cleaner:
```
{
  "dummyPytestFile.py::test_example_3": {
    "flaky_failed_order": [
      "dummyPytestFile.py::test_example_4",
      "dummyPytestFile.py::test_example_2",
      "dummyPytestFile.py::test_example_1",
      "dummyPytestFile.py::test_example_3"
    ],
    "sofware_defect": false,
    "polluter": [
      "dummyPytestFile.py::test_example_1"
    ],
    "cleaner": "dummyPytestFile.py::test_example_4"
  },
  "list_of_tests_ran": [
    "dummyPytestFile.py::test_example_2",
    "dummyPytestFile.py::test_example_1",
    "dummyPytestFile.py::test_example_3",
    "dummyPytestFile.py::test_example_4"
  ],
  "random_order_seed": "309034",
  "random_order_bucket": "module",
  "flaky_test_finder": 2
}
```
