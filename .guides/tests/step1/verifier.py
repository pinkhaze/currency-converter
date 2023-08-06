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


def import_module(name,step=0):
    """
    Returns a reference to the module.
    
    Returns an error message if it fails.
    
    Parameter name: The module name
    Precondition: name is a string
    """
    try:
        import types
        refs = os.path.splitext(name)[0]
        environment = Environment(refs,WORKSPACE)
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


# Localized error codes
DOCSTRING_MISSING   = 1
DOCSTRING_UNCLOSED  = 2
DOCSTRING_NOT_FIRST = 3

def get_docstring(text,first=True):
    """
    Returns the docstring as a list of lines
    
    This function returns an error code if there is no initial docstring.
    
    Parameter text: The text to search for a docstring.
    Precondition: text is a string
    
    Parameter text: Whether to require the docstring to be first.
    Precondition: text is a string
    """
    lines = text.split('\n')
    lines = list(map(lambda x: x.strip(),lines))
    
    start = -1
    for pos in range(len(lines)):
        if len(lines[pos]) >= 3 and lines[pos][:3] in ['"""',"'''"]:
            start = pos
            break
    
    if start == -1:
        return DOCSTRING_MISSING
    
    end = -1
    for pos in range(start+1,len(lines)):
        if lines[pos][-3:] == lines[start][:3]:
            end = pos
            break
    
    if end == -1:
        return DOCSTRING_UNCLOSED
    
    if first:
        for pos in range(start):
            if len(lines[pos]) > 0:
                return DOCSTRING_NOT_FIRST
    
    # One last trim
    if len(lines[start]) > 3:
        lines[start] = lines[start][3:]
    else:
        start += 1
    if len(lines[end]) > 3:
        lines[end] = lines[end][:-3]
    else:
        end -= 1
    
    for x in range(start,end+1):
        lines[x] = lines[x].rstrip()
    return lines[start:end+1]


# Localized error codes
NAME_MISSING     = 1
NAME_INCOMPLETE  = 2

def check_name(text):
    """
    Returns TEST_SUCCESS if the name is correct, and error code otherwise
    
    Parameter text: The docstring text as a list.
    Precondition: text is a list of strings
    """
    if not text[-2].lower().startswith('author:'):
        return NAME_MISSING
    if not text[-2][7:].strip():
        return NAME_INCOMPLETE
    if 'your name here' in text[-2][7:].lower():
        return NAME_INCOMPLETE
    return TEST_SUCCESS


# Localized error codes
DATE_MISSING     = 1
DATE_INCOMPLETE  = 2

def check_date(text):
    """
    Returns TEST_SUCCESS if the date is correct, and error code otherwise
    
    Parameter text: The docstring text as a list.
    Precondition: text is a list of strings
    """
    if not text[-1].lower().startswith('date:'):
        return DATE_MISSING
    
    date = text[-1][5:].strip()
    try:
        import dateutil.parser as util
        temp = util.parse(date)
        return TEST_SUCCESS
    except:
        return DATE_INCOMPLETE


# Localized error codes
KEY_MISSING   = 1
KEY_MULTIPLE  = 2

def check_key(passkey):
    """
    Returns TEST_SUCCESS if the passkey is correct, and error code otherwise
    
    This function also returns the name of the person registered with the key.
    
    Parameter text: The docstring text as a list.
    Precondition: text is a list of strings
    """
    url  = 'https://ecpyfac.ecornell.com/python/currency/lookup/'+passkey
    text = introcs.urlread(url)
    data = json.loads(text)
    if not data['valid']:
        return (KEY_MISSING,"API key %s is not valid." % repr(passkey))
    
    name = data['last']+', '+data['first']
    if len(data['err']) > 0:
        return (KEY_MULTIPLE,'WARNING: API key %s is linked to multiple accounts.\nAccount %s is selected.' % (repr(passkey),repr(name)))
    return (TEST_SUCCESS,"API key %s is registered to %s." % (repr(passkey),name))


pass
#mark -
#mark Subgraders
def grade_docstring(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the docstring.
    
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
    code = read_file(file)
    if code is None:
        outp.write('Could not find the file %s.\n' % repr(file))
        return (FAIL_NO_FILE, 0)
    
    score = 1
    docs = get_docstring(code)
    if type(docs) == int:
        if docs == DOCSTRING_MISSING:
            outp.write('There is no docstring in %s.\n' % repr(file))
            return (FAIL_BAD_STYLE,0)
        if docs == DOCSTRING_UNCLOSED:
            outp.write('The docstring is not properly closed.\n')
            return (FAIL_CRASHES,0.1)
        if docs == DOCSTRING_NOT_FIRST:
            outp.write('The docstring is not the first non-blank line.\n')
            score -= 0.3
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    docs = get_docstring(code,False)
    
    if file in DOCSTRING:
        if not docs[0].strip().startswith(DOCSTRING[file][0]):
            outp.write('The docstring for %s does not start with %s.\n' % (repr(file),repr(DOCSTRING[file])))
            score -= 0.3
            if not step:
                return (FAIL_BAD_STYLE,max(0,score))
        if docs[1].strip() != '':
            outp.write('The second line of the docstring for %s is not blank.\n' % repr(file))
            score -= 0.1
            if not step:
                return (FAIL_BAD_STYLE,max(0,score))
        elif docs[-3].strip() != '':
            outp.write('The third-to-last line of the docstring for %s is not blank.\n' % repr(file))
            score -= 0.1
            if not step:
                return (FAIL_BAD_STYLE,max(0,score))
        else:
            descrip = (' '.join(docs[2:-3])).strip()
            correct = DOCSTRING[file][1]
            if correct != descrip:
                outp.write('The descriptive paragraph in the docstring for %s does not match the one provided:\n' % repr(file))
                outp.write('Found  %s\n' %repr(descrip))
                outp.write('Wanted %s\n' %repr(correct))
                score -= 0.3
                if not step:
                    return (FAIL_BAD_STYLE,max(0,score))
    
    test = check_name(docs)
    if test:
        if test == NAME_MISSING:
            outp.write("The second-to-last line of the docstring for %s does not start with 'Author:'\n" % repr(file))
            score -= 0.3
        if test == NAME_INCOMPLETE:
            outp.write("There is no name after 'Author:' in the docstring for %s\n" % repr(file))
            score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    test = check_date(docs)
    if test:
        if test == DATE_MISSING:
            outp.write("The last line of the docstring for %s does not start with 'Date:'\n" % repr(file))
            score -= 0.2
        if test == DATE_INCOMPLETE:
            outp.write("The date after 'Date:' is invalid in the docstring for %s\n" % repr(file))
            score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_mod_structure(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the file structure for the function module
    
    The step parameter is the phase in the grading pass.  Step 0 does not allow anything
    other than a docstring or import statements.  Step 1 looks for these, but will allow
    other structures. Steps 0-1 will stop at the first error found.  Step 2 is the grading 
    pass and will continue through and try to find all errors.

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
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES, 0)
    elif type(code) != ast.Module:
        outp.write('File %s appears to be corrupted.' % repr(file))
        return (FAIL_CRASHES, 0)
    
    # Crawl to make sure nothing is bad out of body
    body = code.body
    importeds = []
    foundkey = False
    foundfun = False
    for pos in range(len(body)):
        if type(body[pos]) == ast.FunctionDef:
            if not step:
                outp.write('File %s should not contain any function definitions at this step.\n' % repr(file))
                return (FAIL_INCORRECT, max(0,score))
            elif not body[pos].name in FUNCTIONS:
                outp.write('The function %s is not part of this assignment.\n' % repr(body[pos].name))
                score -= 0.1
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            else:
                foundfun = True
        elif foundfun:
            outp.write('Unexpected Python command after function definitions at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            outp.write('Function definitions should be last.\n')
            score -= 0.1
            if step < 2:
                return (FAIL_BAD_STYLE, max(0,score))
        elif type(body[pos]) == ast.Import:
            if len(body[pos].names) != 1 or body[pos].names[0].asname:
                outp.write('Nontraditional import at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.1
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            elif file in IMPORTMOD and not body[pos].names[0].name in IMPORTMOD[file]:
                outp.write('File %s should not import module %s.\n' % (repr(file),repr(body[pos].names[0].name)))
                score -= 0.1
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            else:
                importeds.append(body[pos].names[0].name)
        elif type(body[pos]) == ast.ImportFrom:
            outp.write('Nontraditional import at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if step < 2:
                return (FAIL_BAD_STYLE, max(0,score))
        elif type(body[pos]) == ast.Expr:
            if type(body[pos].value) == ast.Str and pos != 0:
                outp.write('Extraneous docstring at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.05
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            elif type(body[pos].value) != ast.Str:
                outp.write('Extraneous expression at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.05
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
        elif type(body[pos]) == ast.Assign:
            if body[pos].targets[0].id != 'APIKEY':
                outp.write("Unrecognized global variable %s in file %s.\n" % (repr(body[pos].targets[0].id),repr(file)))
                score -= 0.05
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            elif type(body[pos].value) != ast.Str:
                value = body[pos].value
                item = text[value.lineno-1]
                item = item[value.col_offset:]
                outp.write("The API Key %s is not a string.\n" % item)
            else:
                err,msg = check_key(body[pos].value.s)
                outp.write(msg+'\n')
                if err == KEY_MISSING:
                    return (FAIL_INCORRECT, 0)
                else:
                    foundkey = True
        else:
            outp.write('Unexpected Python command outside of function definition at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    if file in IMPORTMOD:
        for mod in IMPORTMOD[file]:
            if mod not in importeds:
                outp.write('File %s does not import module %s.\n' % (repr(file),repr(mod)))
                score -= 0.1
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
    
    if not foundkey:
        outp.write('File %s does not assign the API Key.\n' % (repr(file)))
        score -= 0.3
        if step < 2:
            return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_app_structure(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the existence of a valid API key.
    
    The step parameter is the phase in the grading pass.  Step 0 does not allow anything
    other than a docstring or import statements.  Step 1 looks for these, but will allow
    other structures. Steps 0-1 will stop at the first error found.  Step 2 is the grading 
    pass and will continue through and try to find all errors.
    
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
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES, 0)
    elif type(code) != ast.Module:
        outp.write('File %s appears to be corrupted.' % repr(file))
        return (FAIL_CRASHES, 0)
    
    # Crawl to make sure nothing is bad out of body
    body = code.body
    importeds = []
    for pos in range(len(body)):
        if type(body[pos]) == ast.FunctionDef and body[pos].name != 'main':
            outp.write("File %s should not contain any function definitions other than 'main' (found %s).\n" % (repr(file),repr(body[pos].name)))
            score -= 0.1
            if step < 2:
                return (FAIL_BAD_STYLE, max(0,score))
        elif type(body[pos]) == ast.Import:
            if len(body[pos].names) != 1 or body[pos].names[0].asname:
                outp.write('Nontraditional import at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.1
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            elif file in IMPORTMOD and not body[pos].names[0].name in IMPORTMOD[file]:
                outp.write('File %s should not import module %s.\n' % (repr(file),repr(body[pos].names[0].name)))
                score -= 0.1
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            else:
                importeds.append(body[pos].names[0].name)
        elif type(body[pos]) == ast.ImportFrom:
            outp.write('Nontraditional import at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if step < 2:
                return (FAIL_BAD_STYLE, max(0,score))
        elif type(body[pos]) == ast.Expr:
            if type(body[pos].value) == ast.Str and pos != 0:
                outp.write('Extraneous docstring at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.05
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            elif type(body[pos].value) == ast.Str:
                pass
            elif not step:
                outp.write("File %s should not contain command other than 'import' at this step.\n" % repr(file))
                return (FAIL_INCORRECT, max(0,score))
            elif type(body[pos].value) != ast.Call:
                outp.write('Extraneous expression at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.05
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
        elif type(body[pos]) == ast.Assign:
            pass
        elif not step:
            outp.write('Unexpected Python command at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    if file in IMPORTMOD:
        for mod in IMPORTMOD[file]:
            if mod not in importeds:
                outp.write('File %s does not import module %s.\n' % (repr(file),repr(mod)))
                score -= 0.1
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_test_structure(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test script structure
    
    The step parameter is the phase in the grading pass.  Step 0 does not allow anything
    other than a docstring or import statements.  Step 1 looks for these, but will allow
    other structures. Steps 0-1 will stop at the first error found.  Step 2 is the grading 
    pass and will continue through and try to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES, 0)
    elif type(code) != ast.Module:
        outp.write('File %s appears to be corrupted.' % repr(file))
        return (FAIL_CRASHES, 0)
    
    # Crawl to make sure nothing is bad out of body
    body = code.body
    functions = ['print']
    importeds = []
    TESTPROCS = list(map(lambda x : 'test_'+x, FUNCTIONS))
    for pos in range(len(body)):
        if type(body[pos]) == ast.FunctionDef:
            if not step:
                outp.write('File %s should not contain any test procedures at this step.\n' % repr(file))
                return (FAIL_INCORRECT, max(0,score))
            elif not body[pos].name in TESTPROCS:
                outp.write('The function %s is not part of this assignment.\n' % repr(body[pos].name))
                score -= 0.1
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            else:
                functions.append(body[pos].name)
        elif type(body[pos]) == ast.Import:
            pass
            if len(body[pos].names) != 1 or body[pos].names[0].asname:
                outp.write('Nontraditional import at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.1
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
            else:
                importeds.append(body[pos].names[0].name)
        elif type(body[pos]) == ast.ImportFrom:
            outp.write('Nontraditional import at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if step < 2:
                return (FAIL_BAD_STYLE, max(0,score))
        elif type(body[pos]) == ast.Assign:
            outp.write('Unexpected assignment outside of outside of test procedure at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
        elif type(body[pos]) == ast.Expr:
            if type(body[pos].value) == ast.Str and pos != 0:
                outp.write('Extraneous docstring at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.05
                if step < 2:
                    return (FAIL_BAD_STYLE, max(0,score))
        else:
            outp.write('Unexpected Python command outside of test procedure at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    # Find position of first function def
    start = 0
    while start < len(body) and type(body[start]) != ast.FunctionDef:
        start += 1
    
    if start >= len(body) and step:
        outp.write('File %s has no procedure definitions.' % repr(file))
        return (FAIL_INCORRECT, 0)
    
    # Find the position of the first out of body
    end = start
    while end < len(body) and type(body[end]) == ast.FunctionDef:
        end += 1
    
    if end == len(body) and len(functions[1:]) > 0:
        outp.write('The following test procedures have not been called: '+', '.join(map(repr,functions[1:]))+'.\n')
        score -= 0.35*len(functions[1:])
        if step < 2:
            return (FAIL_INCORRECT, max(0,score))
        
        if step:
            missing = []
            for item in TESTPROCS:
                if not item in functions:
                    missing.append(item)
            if missing != []:
                outp.write('The following test procedures have not been defined: '+', '.join(map(repr,missing))+'.\n')
                score -= 0.35*len(missing)
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))

    else:
        called = []
        while end < len(body):
            if type(body[end]) != ast.Expr or type(body[end].value) != ast.Call:
                outp.write('Unexpected Python command outside of test procedure at line %d:\n' % body[end].lineno)
                outp.write(text[body[end].lineno-1]+'\n')
                outp.write(' '*body[end].col_offset+'^\n')
                score -= 0.1
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            elif not body[end].value.func.id in functions:
                print(body[end].value.func.id)
                print(functions)
                outp.write('Unexpected function call outside of test procedure at line %d:\n' % body[end].lineno)
                outp.write(text[body[end].lineno-1]+'\n')
                outp.write(' '*body[end].col_offset+'^\n')
                score -= 0.1
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            elif body[end].value.func.id == 'print' and end < len(body)-1:
                outp.write('Unexpected print statement at line %d:\n' % body[end].lineno)
                outp.write("The print 'Module funcs is working correctly' must come last in %s.\n" % repr(file))
                outp.write(text[body[end].lineno-1]+'\n')
                outp.write(' '*body[end].col_offset+'^\n')
                score -= 0.1
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            elif body[end].value.func.id != 'print':
                called.append(body[end].value.func.id)
            end += 1
        
        if len(called) != len(functions[1:]):
            missing = []
            for item in functions[1:]:
                if not item in called:
                    missing.append(item)
            if missing != []:
                outp.write('The following test procedures have not been called: '+', '.join(map(repr,missing))+'.\n')
                score -= 0.35*len(missing)
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
        
        if step:
            missing = []
            for item in TESTPROCS:
                if not item in functions:
                    missing.append(item)
            if missing != []:
                outp.write('The following test procedures have not been defined: '+', '.join(map(repr,missing))+'.\n')
                score -= 0.35*len(missing)
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            

    
    if type(body[-1]) != ast.Expr or type(body[-1].value) != ast.Call:
        outp.write('File %s does not end with a print statement.\n' % repr(file))
        score -= 0.2
        if step < 2:
            return (FAIL_INCORRECT, max(0,score))
    elif type(body[-1].value.func) != ast.Name or body[-1].value.func.id != 'print':
        outp.write('File %s does not end with a print statement.\n' % repr(file))
        score -= 0.2
        if step < 2:
            return (FAIL_INCORRECT, max(0,score))
    else:
        bad = False
        correct = 'All tests completed successfully'
        if len(body[-1].value.args) != 1 or type(body[-1].value.args[0]) != ast.Str:
            bad = True
        elif not body[-1].value.args[0].s.startswith(correct):
            bad = True
        if bad:
            outp.write('The final print statement does not show %s.\n' % repr(correct))
            score -= 0.15
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    # Check imports
    if file in IMPORTMOD:
        for mod in IMPORTMOD[file]:
            if mod not in importeds:
                outp.write('File %s does not import module %s.\n' % (repr(file),repr(mod)))
                score -= 0.1
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_proc_headers(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test procedure headers
    
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
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES, 0)
    elif type(code) != ast.Module:
        outp.write('File %s appears to be corrupted.' % repr(file))
        return (FAIL_CRASHES, 0)
    
    body = code.body
    functions = []
    want = 0
    for pos in range(len(body)):
        if type(body[pos]) == ast.FunctionDef:
            ident = body[pos].name
            functions.append(ident)
            have = len(body[pos].args.args)
            if have != want:
                outp.write("Test procedure %s has %d parameter%s (expected %d).\n" % (repr(ident),have,'' if have == 1 else 's', want))
                score -= 0.2
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            
            count = 0
            value = None
            for next in range(len(body[pos].body)):
                item = body[pos].body[next]
                if (type(item) == ast.Expr and type(item.value) == ast.Call and 
                    type(item.value.func) == ast.Name and item.value.func.id == 'print'):
                    count += 1
                    if len(item.value.args) == 1 and type(item.value.args[0]) == ast.Str:
                        value = item.value.args[0].s
                elif type(item) == ast.Expr and type(item.value) == ast.Str:
                    if next != 0:
                        outp.write('Extraneous docstring for function %s at line %d:\n' % (repr(ident), body[pos].lineno))
                        outp.write(text[item.lineno-1]+'\n')
                        outp.write(' '*item.col_offset+'^\n')
                        score -= 0.05
                        if not step:
                            return (FAIL_BAD_STYLE, max(0,score))
                    else:
                        correct = 'Test procedure for '+ident[5:]
                        actual = item.value.s.strip()
                        if not actual.startswith(correct):
                            outp.write("Test procedure %s does not have the correct docstring.\n" % repr(ident))
                            outp.write("Wanted: %s\n" % repr(correct))
                            score -= 0.2
                            if step < 2:
                                return (FAIL_INCORRECT, max(0,score))
            
            goal = 'Testing '+ident[5:]
            if count == 0:
                outp.write("Test procedure %s does not have a print statement.\n" % repr(ident))
                score -= 0.2
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            elif count > 1:
                outp.write("Test procedure %s has more than one print statement.\n" % repr(ident))
                score -= 0.2
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            elif value is None or not value.startswith(goal):
                outp.write("Test procedure %s does not print %s.\n" % (repr(ident),repr(goal)))
                score -= 0.2
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_style(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the file style
    
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
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES, 0)
    elif type(code) != ast.Module:
        outp.write('File %s appears to be corrupted.' % repr(file))
        return (FAIL_CRASHES, 0)
    
    if '\t' in text:
        outp.write('The file %s contains tabs (instead of spaces).\n' % repr(file))
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    # Check functions and indentation
    badlines = False
    for pos in range(len(code.body)):
        item = code.body[pos]
        next = None if pos >= len(code.body)-1 else code.body[pos+1]
        if type(item) == ast.FunctionDef:
            head1 = item.lineno-1
            head2 = next.lineno-1 if next else len(text)
            head2 = head2
            last = head2-1
            while text[last].strip() == '' or text[last].strip()[0] == '#' :
                last -= 1
            
            source = text[head1:last+1]
            diff = 0
            for pos in range(last+1,head2):
                if text[pos].strip() == '':
                    diff += 1
            
            if diff != 2 and next:
                outp.write('There %s %d blank line%s after the body of %s [wanted 2].\n'
                            % ('is' if diff == 1 else 'are',diff,'' if diff == 1 else 's',repr(item.name)))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            
            if not source:
                outp.write('The definition for %s appears to be empty.\n',repr(item.name))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            
            # Enough to check indentation from the first (non-header) line
            begin = 1
            while begin < len(source) and not source[begin]:
                begin += 1
            
            if begin == len(source):
                outp.write('The definition for %s appears to be empty.\n',repr(item.name))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            
            run = 0
            while run < len(source[begin]) and source[begin][run] == ' ':
                run += 1
            
            if run != 4:
                outp.write('Function %s is indented with %d spaces [wanted 4].\n' % (repr(item.name),run))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            
            if run != 4:
                outp.write('Function %s is indented with %d spaces [wanted 4].\n' % (repr(item.name),run))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            
            # Check line length in functions
            HARDCAP = 90
            for line in item.body:
                if type(line) != ast.Expr or type(line.value) != ast.Str:
                    pos = line.lineno-1
                    if len(text[pos]) >= HARDCAP:
                        outp.write('Line %d in file %s is %d characters long.\n' % (line.lineno,repr(file),len(text[pos])))
                        badlines = True
                        score -= 0.05
                        if not step:
                            return (FAIL_INCORRECT, max(0,score))
    
    if badlines:
        outp.write('Break up all lines in file %s more than 89 characters long.\n' %  repr(file))

    return (TEST_SUCCESS, max(0,score))

pass
#mark -
#mark Graders
def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    file = 'currency.py'
    msg = "File %s comments" % repr(file)
    outp.write(msg+'\n')
    outp.write(('='*len(msg))+'\n')    
    status, p1a = grade_docstring(file,1,outp)
    if not status:
        status, p1b = grade_mod_structure(file,2,outp)
    else:
        p1b = 0
    p1 = 0.4*p1a+0.6*p1b
    if p1 == 1:
        outp.write('The module %s is structured properly.\n\n' % repr(file))
    else:
        outp.write('\n')
    
    if not status:
        file = 'exchangeit.py'
        msg = "File %s comments" % repr(file)
        outp.write(msg+'\n')
        outp.write(('='*len(msg))+'\n')    
        status, p2a = grade_docstring(file,1,outp)
        if not status:
            status, p2b = grade_app_structure(file,2,outp)
        else:
            p2b = 0
        p2 = 0.4*p2a+0.6*p2b
        if p2 == 1:
            outp.write('The script %s is structured properly.\n\n' % repr(file))
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    if not status:
        file = 'testcurrency.py'
        msg = "File %s comments" % repr(file)
        outp.write(msg+'\n')
        outp.write(('='*len(msg))+'\n')
        status, p3a = grade_docstring(file,1,outp)
        if not status:
            status, p3b = grade_test_structure(file,2,outp)
        else:
            p3b = 0
        if not status:
            status, p3c = grade_proc_headers(file,1,outp)
        else:
            p3c = 0
        p3 = 0.2*p3a+0.4*p3b+0.4*p3c
        if p3 == 1:
            outp.write('The script %s is structured properly.\n\n' % repr(file))
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    if not status:
        msg = "Style comments"
        outp.write(msg+'\n')
        outp.write(('='*len(msg))+'\n')
        file = 'testcurrency.py'
        status, p4a = grade_style(file,1,outp)
        if not status:
            file = 'currency.py'
            status, p4b = grade_style(file,1,outp)
        else:
            p4b = 0
        if not status:
            file = 'exchangeit.py'
            status, p4c = grade_style(file,1,outp)
        else:
            p4c = 0
        p4 = 0.5*p4a+0.4*p4b+0.1*p4c
        if p4 == 1:
            outp.write('The coding style looks correct.\n\n')
        else:
            outp.write('\n')
    else:
        p4 = 0
        
    total = round(0.3*p1+0.3*p2+0.2*p4+0.2*p4,3)
    return total


if __name__ == '__main__':
    print(grade())