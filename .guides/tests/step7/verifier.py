"""
The verification functions for Course 3 scripts

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import os, os.path, sys
import importlib, importlib.util
import traceback
import inspect
import introcs
import builtins
import json
import ast
from modlib import Environment

# For support
import introcs

#mark Constants

# The status codes
TEST_SUCCESS      = 0
FAIL_NO_FILE      = 1
FAIL_BAD_STYLE    = 2
FAIL_CRASHES      = 4
FAIL_INCORRECT    = 5


WORKSPACE = [os.path.expanduser('~'),'workspace']
#WORKSPACE = ['..']


# Docstrings
DOCSTRING = {'currency.py': ['Module for currency exchange',
                             'This module provides several string parsing functions to implement a simple currency exchange routine using an online currency service. The primary function in this module is exchange().'],
             'exchangeit.py': ['User interface for module currency',
                        'When run as a script, this module prompts the user for two currencies and amount. It prints out the result of converting the first currency to the second.'],
             'testcurrency.py': ['Unit tests for module currency',
                          'When run as a script, this module invokes several procedures that test the various functions in the module currency.']}

# Allowable modules
IMPORTMOD = {'currency.py' : ['introcs'], 'exchangeit.py' : ['currency'], 'testcurrency.py' : ['introcs','currency']}

# Expected functions
FUNCTIONS = ['after_space','before_space','first_inside_quotes','get_src','get_dst','has_error','service_response','iscurrency','exchange']


#mark -
#mark Helpers
def read_file(name):
    """
    Returns the contents of the file or None if missing.
    
    Parameter name: The file name
    Precondition: name is a string
    """
    path = os.path.join(*WORKSPACE,name)
    try:
        with open(path) as file:
            result = file.read()
        return result
    except:
        return None


def parse_file(name):
    """
    Returns an AST of the file, or a error message if it cannot be parsed.
    
    Parameter name: The file name
    Precondition: name is a string
    """
    import ast
    path = os.path.join(*WORKSPACE,name)
    try:
        with open(path) as file:
            result = ast.parse(file.read())
        return result
    except Exception as e:
        msg = traceback.format_exc(0)
        msg = msg.replace('<unknown>',name)
        return msg


def import_script(name,*inputs):
    """
    Returns a reference to the script.
    
    Returns an error message if it fails.
    
    Parameter name: The module name
    Precondition: name is a string
    """
    try:
        import types
        refs = os.path.splitext(name)[0]
        environment = Environment(refs,WORKSPACE,*inputs)
        if not environment.execute():
            return '\n'.join(environment.printed)+'\n'
        return environment
    except Exception as e:
        msg = traceback.format_exc(0)
        pos2 = msg.find('^')
        pos1 = msg.rfind(')',0,pos2)
        if 'SyntaxError: unexpected EOF' in msg or 'IndentationError' in msg:
            msg = 'Remember to include and indent the docstring properly.\n'+msg
        elif pos1 != -1 and pos2 != -1 and not msg[pos1+1:pos2].strip():
            msg = 'Remember to end the header with a colon.\n'+msg
        else:
            msg = ("File %s has a major syntax error.\n" % repr(name))+msg
        return msg


pass
#mark -
#mark Subgraders
def grade_application(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the currency application.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    tests = [('JPY','EUR','3.5'),('BDT','NPR','-4.5')]
    for plan in tests:
        apps =  import_script(file,*plan)
        if type(apps) == str:
            outp.write(apps)
            return (FAIL_CRASHES,0)
        if not hasattr(apps.module,'currency'):
            outp.write("File %s does not import 'currency' as instructed.\n" % repr(file))
            return (FAIL_INCORRECT,0)
        if not hasattr(apps.module.currency,'exchange'):
            outp.write("The module 'currency' does not implement the function 'exchange'.\n")
            return (FAIL_INCORRECT,0)
    
        if len(apps.inputed) == 0:
            outp.write("The app does not ask for any user input.\n")
            return (FAIL_INCORRECT,0)

        correct = '3-letter code for original currency: '
        if not apps.inputed[0].startswith(correct[:-1]):
            outp.write("The prompt for the first currency code is incorrect.\n")
            outp.write('Found  %s\n' % repr(apps.inputed[0]))
            outp.write('Wanted %s\n' % repr(correct))
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        elif not apps.inputed[0].startswith(correct):
            outp.write("The prompt for the first currency code does not end with a space.\n")
            score -= 0.05
            if not step:
                return (FAIL_INCORRECT,max(0,score))

        correct = '3-letter code for the new currency: '
        if  len(apps.inputed) < 2:
            outp.write("The app does not ask for a second currency.\n")
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        elif not apps.inputed[1].startswith(correct[:-1]):
            outp.write("The prompt for the second currency code is incorrect.\n")
            outp.write('Found  %s\n' % repr(apps.inputed[0]))
            outp.write('Wanted %s\n' % repr(correct))
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        elif not apps.inputed[1].startswith(correct):
            outp.write("The prompt for the second currency code does not end with a space.\n")
            score -= 0.05
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
        correct = 'Amount of the original currency: '
        if  len(apps.inputed) < 3:
            outp.write("The app does not ask for an amount.\n")
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        elif not apps.inputed[2].startswith(correct[:-1]):
            outp.write("The prompt for the currency amount is incorrect.\n")
            outp.write('Found  %s\n' % repr(apps.inputed[0]))
            outp.write('Wanted %s\n' % repr(correct))
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        elif not apps.inputed[2].startswith(correct):
            outp.write("The prompt for the currency amount does not end with a space.\n")
            score -= 0.05
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
        if len(apps.inputed) > 3:
            outp.write("The app asks for too much user input.\n")
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
        if len(apps.printed) == 0:
            outp.write("The app does not print the result.\n")
            score -= 0.4
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        else:
            try:
                line  = apps.printed[0].strip()
                value = apps.module.currency.exchange(plan[0],plan[1],float(plan[2]))
                prefix = 'You can exchange %s %s for ' % (plan[2],plan[0])
                suffix = plan[1]+'.'
                if not line.startswith(prefix):
                    outp.write("The print statement does not start with the correct prefix.\n")
                    outp.write('Found  %s\n' % repr(line[:len(prefix)]))
                    outp.write('Wanted %s\n' % repr(prefix))
                    score -= 0.2
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if not line.endswith(suffix):
                    outp.write("The print statement does not end with the correct suffix (including the period).\n")
                    outp.write('Found  %s\n' % repr(line[-len(suffix):x]))
                    outp.write('Wanted %s\n' % repr(suffix))
                    score -= 0.1
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                extract = line[:line.rfind(' ')]
                extract = extract[extract.rfind(' '):]
                try:
                    shown = repr(float(extract))
                    wants = repr(round(value,3))
                    if shown == wants:
                        pass
                    elif shown == repr(value):
                        outp.write("The print statement does not correctly round the final amount [wanted %s, found %s].\n" % (wants,shown))
                        score -= 0.1
                        if not step:
                            return (FAIL_INCORRECT,max(0,score))
                    else:
                        outp.write("The print statement does not show the correct final amount [wanted %s, found %s].\n" % (wants,shown))
                        score -= 0.1
                        if not step:
                            return (FAIL_INCORRECT,max(0,score))
                except:
                    outp.write("The print statement does not put the final amount in the right place.\n")
                    score -= 0.2
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
            except:
                outp.write('The function call exchange%s crashed.\n' % repr(plan))
                score -= 0.3
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            
            if len(apps.printed) > 1:
                outp.write("The app prints too many lines.\n")
                score -= 0.05
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


pass
#mark -
#mark Graders
def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    file = 'exchangeit.py'
    msg = "Application comments"
    outp.write(msg+'\n')
    outp.write(('='*len(msg))+'\n')    
    status, p = grade_application(file,1,outp)
    if p == 1:
        outp.write('The script %s is working correctly.\n\n' % repr(file))
    else:
        outp.write('\n')
    
    return round(p,3)


if __name__ == '__main__':
    print(grade())