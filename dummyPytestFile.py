import pytest
import random

# def test_example_1():
#   assert random.choice([True, True])
# def test_example_2():
#   assert random.choice([False, False])
# def test_example_3():
#   assert random.choice([True, False])
def test_example_4():
  with open("dummyFileForFlakyTest.txt", "w") as outputFile:
    outputFile.write("100")
  assert True
def test_example_5():
  assert True
def test_example_6():
  with open("dummyFileForFlakyTest.txt", "r") as inputFile:
    val = inputFile.read().splitlines()
  with open("dummyFileForFlakyTest.txt", "w") as outputFile:
    outputFile.write("0") 
  assert val[0] == "0"