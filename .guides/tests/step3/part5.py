#!/usr/local/bin/python3
"""
Assess part 5, before moving on to the next step.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step5(files,func):
    """
    Checks that the function and test cases are all correct
    
    Parameter files: The files to check
    Precondition: files is a list of strings
    
    Parameter func: The function to check
    Precondition: funcs is a strings, and a name of a function in file
    """
    result = verifier.grade_func_stub(files[0],func,0)
    if not result[0]:
        result = verifier.grade_test_cases(files[1],func,0)
    if not result[0]:
        result = verifier.grade_func_body(files[0],func,0)
    if not result[0]:
        result = verifier.grade_asserts(files[0],func,0)
    if not result[0]:
        print("The tests and implementation for %s look correct." % repr(func))
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step5(['currency.py','tests.py'],'first_inside_quotes'))