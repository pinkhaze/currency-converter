#!/usr/local/bin/python3
"""
Assess part 8, before moving on to the next step.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step8(files,funcs):
    """
    Checks that the functions and test cases are all correct
    
    Parameter files: The files to check
    Precondition: files is a list of strings
    
    Parameter funcs: The function to check
    Precondition: funcs a list of strings, each a name of a function in file
    """
    result = [0,0]
    for item in funcs:
        if not result[0]:
            result = verifier.grade_func_stub(files[0],item,0)
        if not result[0]:
            result = verifier.grade_test_cases(files[1],item,0)
        if not result[0]:
            result = verifier.grade_func_body(files[0],item,0)
        if not result[0]:
            result = verifier.grade_asserts(files[0],item,0)
    if not result[0]:
        thefunc = ', '.join(list(map(repr,funcs)))
        print("The tests and implementations for %s look correct." % thefunc)
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step8(['currency.py','testcurrency.py'],['iscurrency','exchange']))