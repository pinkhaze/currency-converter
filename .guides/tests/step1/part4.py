#!/usr/local/bin/python3
"""
Assess part 4, stubbing the test procedures

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step2(file):
    """
    Checks that the script docstring and import is correct.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_test_structure(file,1)
    if not result[0]:
        result = verifier.grade_proc_headers(file,0)
    if not result[0]:
        print("The test procedure stubs in %s look correct." % repr(file))
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step2('testcurrency.py'))


