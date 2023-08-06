#!/usr/local/bin/python3
"""
Assess part 3, test cases for before_space

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step3(file,func):
    """
    Checks that the test case for the given function are correct
    
    Parameter file: The file to check
    Precondition: file is a string
    
    Parameter func: The function to checl
    Precondition: func is a string, a name of a function in file
    """
    result = verifier.grade_test_cases(file,func,0)
    if not result[0]:
        print("The test cases for %s look correct." % repr(func))
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step3('testcurrency.py','before_space'))
