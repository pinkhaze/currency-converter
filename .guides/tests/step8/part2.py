#!/usr/local/bin/python3
"""
Assess before final submission.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier1
import verifier2
import verifier3
import verifier4
import verifier5
import verifier6
import verifier7
import sys


def check_funcs(file,*funcs):
    """
    Checks that the functions are all correct
    
    Parameter file: The file to check
    Precondition: file is a string
    
    Parameter funcs: The functions to check
    Precondition: funcs is a list of string verifier pairs
    """
    result = verifier1.grade_docstring(file,0)
    if not result[0]:
        result = verifier1.grade_mod_structure(file,1)
    if not result[0]:
        result = verifier1.grade_style(file,0)
    for pair in funcs:
        if not result[0]:
            result = pair[1].grade_func_stub(file,pair[0],0)
        if not result[0]:
            result = pair[1].grade_func_body(file,pair[0],0)
    if not result[0]:
        print("The file %s looks correct." % repr(file))
    return result[0]


def check_tests(file,*funcs):
    """
    Checks that the test cases are all correct
    
    Parameter file: The file to check
    Precondition: file is a string
    
    Parameter funcs: The functions to check
    Precondition: funcs is a list of string verifier pairs
    """
    result = verifier1.grade_docstring(file,0)
    if not result[0]:
        result = verifier1.grade_test_structure(file,1)
    if not result[0]:
        result = verifier1.grade_proc_headers(file,0)
    if not result[0]:
        result = verifier1.grade_style(file,0)
    for pair in funcs:
        if not result[0]:
            result = pair[1].grade_test_cases(file,pair[0],0)
    if not result[0]:
        print("The file %s looks correct." % repr(file))
    return result[0]


def check_script(file):
    """
    Checks that the application is all correct
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier1.grade_docstring(file,0)
    if not result[0]:
        result = verifier1.grade_app_structure(file,1)
    if not result[0]:
        result = verifier1.grade_style(file,0)
    if not result[0]:
        result = verifier7.grade_application(file,0)
    if not result[0]:
        print("The script %s looks correct." % repr(file))
    return result[0]


def check_all(*files):
    """
    Checks that the files all correct
    
    Parameter files: The file to check
    Precondition: file is a list of strings: module, test, then app
    """
    funcs = [('before_space',verifier2),('after_space',verifier2),
             ('first_inside_quotes',verifier3),
             ('get_src',verifier4),('get_dst',verifier4),('has_error',verifier4),
             ('service_response',verifier5),
             ('exchange',verifier6),('exchange',verifier6)]
    result = check_tests(files[0],*funcs)
    if not result:
        result = check_funcs(files[1],*funcs)
    if not result:
        result = check_script(files[2])
    return result


if __name__ == '__main__':
    sys.exit(check_all('testcurrency.py','currency.py','exchangeit.py'))
