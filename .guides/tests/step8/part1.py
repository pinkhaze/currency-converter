#!/usr/local/bin/python3
"""
Assess the sytle before final submission.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier1
import sys


def check_style(*files):
    """
    Checks that the file style is correct
    
    Parameter file: The file to check
    Precondition: file is a string
    
    Parameter funcs: The functions to check
    Precondition: funcs is a list of string verifier pairs
    """
    result = [0,0]
    for item in files:
        if not result[0]:
            result = verifier1.grade_style(item,0)
    if not result[0]:
        thefiles = ', '.join(list(map(repr,files)))
        print("The coding style for the files %s looks correct." % thefiles)
    return result[0]

if __name__ == '__main__':
    sys.exit(check_style('testcurrency.py','currency.py','exchangeit.py'))
