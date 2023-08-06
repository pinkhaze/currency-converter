#!/usr/local/bin/python3
"""
Assess part 4, the assert statements

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step4(file,*funcs):
    """
    Checks that the function asserts in file are correct.
    
    Parameter file: The file to check
    Precondition: file is a string
    
    Parameter funcs: The function stubs to check
    Precondition: funcs a list of strings, each a name of a function in file
    """
    result = [0,0]
    for item in funcs:
        if not result[0]:
            result = verifier.grade_asserts(file,item,0)
    if not result[0]:
        thefunc = ', '.join(list(map(repr,funcs)))
        print("The asserts for %s look correct." % thefunc)
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step4('currency.py','first_inside_quotes'))