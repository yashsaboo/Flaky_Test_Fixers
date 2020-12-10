import pytest
import random

def test_example_1():
  with open("dummyFileForFlakyTest.txt", "w") as outputFile:
    outputFile.write("100")
  assert True
def test_example_2():
  assert True
def test_example_3():
  with open("dummyFileForFlakyTest.txt", "r") as inputFile:
    val = inputFile.read().splitlines()
  with open("dummyFileForFlakyTest.txt", "w") as outputFile:
    outputFile.write("0") 
  assert val[0] == "0"