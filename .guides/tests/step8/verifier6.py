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
from modlib import Environment, Fragment, load_from_path

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


#mark -
#mark Test Capture
class TestPlan(object):

    @property
    def tested(self):
        """
        The captured print statements of this environment.

        Each call to `print` is a separate entry to this list.  Special
        endlines (or files) are ignored.

        **Invariant**: Value is a list of strings.
        """
        return self._tests

    @property
    def asserted(self):
        """
        The captured input statements of this environment.

        Each call to `input` adds a new element to the list.  Only the
        prompts are added to this list, not the user response (which
        are specified in the initializer).

        **Invariant**: Value is a list of strings or None.
        """
        return self._asserts
    
    def __init__(self,env):
        self._environment = env
        self._tests   = {}
        self._asserts = {}
        self._key = ''
    
    def reset(self):
        self._tests   = {}
        self._asserts = {}
    
    def setKey(self,key):
        self._key = key
    
    def assert_equals(self,expected,received,message=None):
        """
        Wrapper for introcs.assert_equals
        """
        if not 'assert_equals' in self._asserts:
            self._asserts['assert_equals'] = []
        self._asserts['assert_equals'].append((expected,received))
    
    def assert_not_equals(self,expected,received,message=None):
        """
        Wrapper for introcs.assert_not_equals
        """
        if not 'assert_not_equals' in self._asserts:
            self._asserts['assert_not_equals'] = []
        self._asserts['assert_not_equals'].append((expected,received))
    
    def assert_true(self,received,message=None):
        """
        Wrapper for introcs.assert_true.
        
        Allow it to be interchanged with assert_equals.
        """
        if not 'assert_equals' in self._asserts:
            self._asserts['assert_equals'] = []
        self._asserts['assert_equals'].append((True,received))
    
    def assert_false(self,received,message=None):
        """
        Wrapper for introcs.assert_false
        
        Allow it to be interchanged with assert_equals.
        """
        if not 'assert_equals' in self._asserts:
            self._asserts['assert_equals'] = []
        self._asserts['assert_equals'].append((False,received))
    
    def assert_floats_equal(self,expected, received,message=None):
        """
        Wrapper for introcs.assert_floats_equal
        """
        if not 'assert_floats_equal' in self._asserts:
            self._asserts['assert_floats_equal'] = []
        self._asserts['assert_floats_equal'].append((expected,received))
    
    def assert_floats_not_equal(self,expected, received,message=None):
        """
        Wrapper for introcs.assert_floats_not_equal
        """
        if not 'assert_floats_not_equal' in self._asserts:
            self._asserts['assert_floats_not_equal'] = []
        self._asserts['assert_floats_not_equal'].append((expected,received))
    
    def iscurrency1(self,code):
        """
        Incorrect version for first pass
        """
        if not 'iscurrency' in self._tests:
            self._tests['iscurrency'] = []
        self._tests['iscurrency'].append((code,))
        return 2
    
    def iscurrency2(self,code):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'iscurrency' in self._tests:
            self._tests['iscurrency'] = []
        self._tests['iscurrency'].append((code,))
        return self.iscurrency3(code)
    
    def iscurrency3(self,code):
        """
        Correct version, no logging
        """
        return checkit(code,self._key)
    
    def exchange1(self,src,dst,amt):
        """
        Incorrect version for first pass
        """
        if not 'exchange' in self._tests:
            self._tests['exchange'] = []
        self._tests['exchange'].append((src,dst,amt))
        return self.exchange3(src,dst,amt)+2
        return None
    
    def exchange2(self,src,dst,amt):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'exchange' in self._tests:
            self._tests['exchange'] = []
        self._tests['exchange'].append((src,dst,amt))
        return self.exchange3(src,dst,amt)
    
    def exchange3(self,src,dst,amt):
        """
        Correct version, no logging
        """
        import json
        parse = 'https://ecpyfac.ecornell.com/python/currency/fixed?'
        parse += 'src='+src+'&dst='+dst+'&amt='+str(amt)
        parse += '&key='+self._key
        result = introcs.urlread(parse)
        string = json.loads(result)['dst']
        value = string[:string.find(' ')]
        return float(value)


# Docstrings
DOCSTRING = {
            'iscurrency': 
                ['Returns True if currency is a valid (3 letter code for a) currency.',
                 'It returns False otherwise.',
                 ('Parameter currency: the currency code to verify '+
                  'Precondition: currency is a nonempty string with only letters')],
             'exchange': 
                ['Returns the amount of currency received in the given exchange.',
                 ('In this exchange, the user is changing amt money in currency src to the currency '+
                  'dst. The value returned represents the amount in currency currency_to. '+
                  'The value returned has type float.'),
                 ('Parameter src: the currency on hand '+
                  'Precondition src is a string for a valid currency code'),
                 ('Parameter dst: the currency to convert to '+
                  'Precondition dst is a string for a valid currency code'),
                 ('Parameter amt: amount of currency to convert '+
                  'Precondition amt is a float or int')]
            }



# Expected functions
FUNCTIONS = ['iscurrency','exchange']


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


def import_module(name):
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


def import_script(name,step=0):
    """
    Returns a reference to the script.
    
    Returns an error message if it fails.
    
    Parameter name: The script name
    Precondition: name is a string
    """
    try:
        import types
        
        # Strip out procedure calls for efficiency
        refs = os.path.splitext(name)[0]
        file = open(os.path.join(*WORKSPACE,refs+'.py'))
        text = file.read().split('\n')
        file.close()
        for pos in range(len(text)):
            if text[pos].startswith('test_'):
                text[pos] = ''
        text = '\n'.join(text)
        
        environment = Fragment(refs,text)
        testplan = TestPlan(environment)
        
        intro = types.ModuleType('introcs')
        for func in dir(introcs):
            if func[0] != '_':
                if 'assert' in func and hasattr(testplan,func):
                    setattr(intro,func,getattr(testplan,func))
                else:
                    setattr(intro,func,getattr(introcs,func))
        environment.capture('introcs',intro)
        
        try:
            func = load_from_path('currency',WORKSPACE)
            func.print = environment.print
            func.input = environment.input
            if step:
                func.iscurrency = testplan.iscurrency2
                func.exchange = testplan.exchange2
            elif step < 2:
                func.iscurrency = testplan.iscurrency1
                func.exchange = testplan.exchange1
            environment.capture('currency',func)
        except:
            pass
        
        if not environment.execute():
            return ('\n'.join(environment.printed)+'\n',None)
        return (environment, testplan)
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
        return (msg,None)

    
def check_args(func,*args):
    """
    Returns True if the given function has the specified positional arguments.
    
    This function returns False if there are any arguments other than positional ones.
    The names to the positional arguments must match.
    
    Parameter func: The function ast to check.
    Precondition: func is an instance of ast.FunctionDef
    
    Parameter args: The argument list
    Precondition: args is a list of strings
    """
    others = not func.args.vararg is None
    others = others or not func.args.kwarg is None
    others = others or func.args.kwonlyargs != []
    others = others or func.args.kw_defaults != []
    others = others or func.args.defaults != []
    if others:
        return False
    
    actual = tuple(map(lambda x : x.arg, func.args.args))
    return actual == args


pass
#mark -
#mark Test Case Checking
def checkit(code,key):
    """
    Currency checking
    """
    parse = 'https://ecpyfac.ecornell.com/python/currency/fixed?'
    parse += 'src='+code+'&dst='+code+'&amt=1'
    parse += '&key='+key
    result = introcs.urlread(parse)
    return ' true' in result


def pullit(*input):
    """
    Currency checking
    """
    parse = 'https://ecpyfac.ecornell.com/python/currency/fixed?'
    parse += 'src='+input[0]+'&dst='+input[1]+'&amt='+str(input[2])
    parse += '&key='+input[3]
    result = introcs.urlread(parse)


def encode_iscurrency(*input):
    """
    Returns: the hash encoding for input to iscurrency
    
    Parameter input: The input to iscurrency
    """
    if len(input) != 2:
        return -1
    elif type(input[0]) != str or type(input[1]) != str:
        return -1
    elif not input[0].isalpha():
        return -1
    if checkit(*input):
        return 1
    else:
        return 2


def encode_exchange(*input):
    """
    Returns: the hash encoding for input to exchange
    
    Parameter input: The input to exchange
    """
    if len(input) != 4:
        return -1
    if type(input[0]) != str or type(input[1]) != str or type(input[3]) != str:
        return -1
    elif not input[0].isalpha() or not input[1].isalpha():
        return -1
    elif not checkit(input[0],input[3]) or not checkit(input[1],input[3]):
        return -1
    elif not type(input[2]) in [int,float]:
        return -1
    
    return 1 if input[2] >= 0 else 2


# The explanatory reasons for the tests
ISCURRENCY = [
    "a test with a valid currency",
    "a test with an invalid currency"
]

EXCHANGE = [
    "a test with a non-negative amount",
    "a test with a negative amount"
]



pass
#mark -
#mark Subgraders
def grade_func_stub(file,func,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the function stub for the given function.
    
    This function is only good for service_response
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter func: The function being tested (not the test procedure)
    Precondition: func is 'service_response'
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    if not hasattr(env.module,'introcs'):
        outp.write("File %s does not import 'introcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,func):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(func)))
        return (FAIL_INCORRECT, 0)
    
    call = getattr(env.module,func)
    want = 3 if func == 'exchange' else 1
    have = call.__code__.co_argcount
    if want != have:
        outp.write("Function %s has %d parameter%s (expected %d).\n" % (repr(func),have,'' if have == 1 else 's', want))
        score -= 0.3
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if call.__doc__ is None:
        outp.write("Function %s has no docstring.\n" % (repr(func)))
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif func in DOCSTRING:
        spec = call.__doc__.split('\n')
        start = 0
        ends  = 0
        while spec[start].strip() == '':
            start += 1
        while spec[ends-1].strip() == '':
            ends -= 1
        spec = spec[start:len(spec)+ends]
        
        params = len(DOCSTRING[func]) - 2
        
        if not spec[0].strip().startswith(DOCSTRING[func][0]):
            outp.write('The specification for %s does not start with %s.\n' % (repr(func),repr(DOCSTRING[func][0])))
            score -= 0.3
            if not step:
                return (FAIL_BAD_STYLE,max(0,score))
        
        if spec[1].strip() != '':
            outp.write('The second line of the specification for %s is not blank.\n' % repr(func))
            score -= 0.2
            if not step:
                return (FAIL_BAD_STYLE,max(0,score))
        else:
            descrip = (' '.join(filter(lambda x : x != '', map(lambda x : x.strip(), spec[2:-3*params+1])))).strip()
            correct = DOCSTRING[func][1]
            if correct != descrip:
                outp.write('The descriptive paragraph in the specification for %s does not match the one provided:\n' % repr(func))
                outp.write('Found  %s\n' %repr(descrip))
                outp.write('Wanted %s\n' %repr(correct))
                score -= 0.2
                if not step:
                    return (FAIL_BAD_STYLE,max(0,score))
        
        for index in range(params):
            if spec[-3*(params-index)].strip() != '':
                outp.write('The specification of %s does not have a blank line before parameter %d.\n' % (repr(func),index))
                score -= 0.2
                if not step:
                    return (FAIL_BAD_STYLE,max(0,score))
            else:
                descrip = (' '.join(filter(lambda x : x != '',map(lambda x: x.strip(), spec[-3*(params-index)+1:len(spec)-3*(params-index-1)])))).strip()
                correct = DOCSTRING[func][index+2]
                if correct != descrip:
                    outp.write('The description for parameter %d in %s does not match the one provided:\n' % (index, repr(func)))
                    outp.write('Found  %s\n' %repr(descrip))
                    outp.write('Wanted %s\n' %repr(correct))
                    score -= 0.2
                    if not step:
                        return (FAIL_BAD_STYLE,max(0,score))
    
    # Check the args
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES, 0)
    elif type(code) != ast.Module:
        outp.write('File %s appears to be corrupted.\n' % repr(file))
        return (FAIL_CRASHES, 0)
    
    body = None
    for item in code.body:
        if type(item) == ast.FunctionDef and item.name == func:
            body = item
    if body is None:
        outp.write('File %s appears to be corrupted.\n' % repr(file))
        return (FAIL_CRASHES, 0)

    params = ('currency',) if func == 'iscurrency' else ('src','dst','amt')
    if not check_args(body,*params):
        outp.write('The parameters for %s do not match the specification.\n' % repr(func))
        score -= 1.0
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_test_cases(file,func,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test case for the given function.
    
    This function is only good for service_response
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter func: The function being tested (not the test procedure)
    Precondition: func is 'service_response'
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env, tests = import_script(file,0)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    # Step 1
    score = 1
    if not hasattr(env.module,'introcs'):
        outp.write("File %s does not import 'introcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'currency'):
        outp.write("File %s does not import 'currency' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'test_'+func):
        outp.write("File %s is missing the header for 'test_%s'.\n" % (repr(file),func))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module.currency,'APIKEY'):
        outp.write("Module 'currency' does not have a variable 'APIKEY'.\n")
        return (FAIL_INCORRECT,0)
    
    thekey = env.module.currency.APIKEY
    tests.setKey(thekey)
    env.reset()
    tests.reset()
    proc = getattr(env.module,'test_'+func)
    proc()
    asserter = 'assert_equals' if func == 'iscurrency' else 'assert_floats_equal'
    
    if not func in tests.tested:
        outp.write("You have not called the function %s properly in the test cases.\n" % repr(func))
        return (FAIL_INCORRECT,0)
    
    if not asserter in tests.asserted or len(tests.asserted[asserter]) != len(tests.tested[func]):
        if func == 'iscurrency' or not 'assert_equals' in tests.asserted:
            outp.write("You were supposed to call %s for each test case.\n" % repr(asserter))
        else:
            outp.write("You cannot use 'assert_equals' to test %s.\n" % repr(func))
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    encoder = globals()['encode_'+func]
    correct = getattr(tests,func+'3')
    badin = None
    for pos in range(len(tests.asserted[asserter])):
        if  pos < len(tests.tested[func]):
            pair  = tests.asserted[asserter][pos]
            input = tests.tested[func][pos]
            if pair[0] != correct(*input) and encoder(*(input+(thekey,))) >= 0 and correct(*input) == pair[1]:
                badin = input
    
    if badin:
        outp.write("In %s, the expected value goes first [see %s(%s)].\n" % (repr(asserter),func,repr(badin)))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,0)
    
    env, tests = import_script(file,1)
    tests.setKey(thekey)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    env.reset()
    tests.reset()
    proc = getattr(env.module,'test_'+func)
    proc()
    
    badin = None
    for pos in range(len(tests.asserted[asserter])):
        pair = tests.asserted[asserter][pos]
        input = tests.tested[func][pos]
        if pair[0] != pair[1] and encoder(*(input+(thekey,))) >= 0:
            badin = tests.tested[func][pos]
        if not badin is None:
            outp.write("The test %s%s has incorrect output.\n" % (func,repr(badin)))
            score -= 0.3
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    # Look for proper coverage
    THECASES = globals()[func.upper()]
    results = [0]*len(THECASES)
    for input in tests.tested[func]:
        code = encoder(*(input+(thekey,)))
        if code == -1:
            outp.write("The test %s%s violates the precondition.\n" % (func,repr(input)))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        results[code-1] += 1
    
    ntests = len(list(filter(lambda x : x > 0, results)))
    wtests = 2
    if  ntests < wtests:
        outp.write("There are only %d distinct test case%s for %s [wanted %d].\n" % (ntests,'' if ntests == 1 else 's', repr(func),wtests))
        if ntests > 0:
            outp.write('For comparison, you have the following tests:\n')
            for pos in range(len(results)):
                if results[pos] > 0:
                    outp.write('* '+THECASES[pos]+'\n')
            outp.write('Look at these and think about what you are missing.\n')
        else:
            outp.write('Read the specification of %s for a hint.\n' % repr(func) )
        score -= 0.1* (wtests-ntests)
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_func_body(file,func,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the function body for the given function.
    
    This function is only good for first_inside_quotes
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter func: The function being tested (not the test procedure)
    Precondition: func is 'first_inside_quotes'
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    if not hasattr(env.module,'introcs'):
        outp.write("File %s does not import 'introcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,func):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(func)))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'APIKEY'):
        outp.write("File %s does not have a variable 'APIKEY'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    tests = TestPlan(None)
    tests.setKey(env.module.APIKEY)
    submit  = getattr(env.module,func)
    correct = getattr(tests,func+'3')
    
    if func == 'iscurrency':
        inputs = [('JPY',),('AXA',)]
    else:
        inputs = [('JPY','CNY',2.5),('GBP','XAU',-3.5),('USD','USD',1.0)]
    for item in inputs:
        try:
            want = correct(*item)
            have = submit(*item)
            if want != have:
                outp.write('Call %s%s returned %s, not the expected %s.\n' % (func,repr(item),repr(have),repr(want)))
                score -= 1.0/len(inputs)
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
        except:
            import traceback
            traceback.print_exc()
            outp.write('Call %s%s crashed.\n' % (func,repr(item)))
            score -= 1.0/len(inputs)
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    if len(env.printed) > 0:
        outp.write("The function %s contains print statements.\n" % repr(func))
        score -= 0.05
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    # Make sure no illegal steps
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES, 0)
    elif type(code) != ast.Module:
        outp.write('File %s appears to be corrupted.\n' % repr(file))
        return (FAIL_CRASHES, 0)
    
    body = None
    for item in code.body:
        if type(item) == ast.FunctionDef and item.name == func:
            body = item.body
    if body is None:
        outp.write('File %s appears to be corrupted.\n' % repr(file))
        return (FAIL_CRASHES, 0)
    
    for item in body:
        for frag in ast.walk(item):
            # No method calls
            if type(frag) == ast.Call and type(frag.func) == ast.Attribute:
                name = frag.func.value
                if type(name) != ast.Name or name.id != 'introcs':
                    outp.write('Unpermitted call in %s at line %d:\n' % (repr(func),frag.lineno))
                    outp.write(text[frag.lineno-1]+'\n')
                    outp.write(' '*frag.col_offset+'^\n')
                    outp.write('Method calls are not permitted in this project.\n')
                    score -= 0.1
                    if not step:
                        return (FAIL_INCORRECT, max(0,score))
            elif type(frag) in [ast.If, ast.For, ast.While]:
                outp.write('Unpermitted control structure in %s at line %d:\n' % (repr(func),frag.lineno))
                outp.write(text[frag.lineno-1]+'\n')
                outp.write(' '*frag.col_offset+'^\n')
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_asserts(file,func,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the asserts for the given function.
    
    This function is only good for first_inside_quotes
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter func: The function being tested (not the test procedure)
    Precondition: func is 'first_inside_quotes'
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    if not hasattr(env.module,'introcs'):
        outp.write("File %s does not import 'introcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,func):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(func)))
        return (FAIL_INCORRECT, 0)
    
    call = getattr(env.module,func)
    if func == 'iscurrency':
        tests = [('JPY',),('AXA',)]
    else:
        tests = [('JPY','CNY',2.5),('GBP','XAU',-3.5),('USD','USD',1.0)]
    
    for item in tests:
        try:
            call(*item)
        except:
            import traceback
            outp.write("The call %s%s no longer works properly.\n" % (func,repr(item)))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 1/len(tests)
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    if func == 'iscurrency':
        tests = [('',),('1',),(1,),(2.5,),(True,)]
    else:
        amts = [2.5,'1',True]
        srcs = ['USD',2,3.5,True,'','AAA']
        dsts = ['EUR',2,3.5,True,'','AAA']
        tests = []
        for amt in amts:
            for src in srcs:
                for dst in dsts:
                    tests.append((src,dst,amt))
        tests = tests[1:]
    
    for item in tests:
        try:
            call(*item)
            outp.write("The call %s%s did not enforce the function precondition.\n" % (func,repr(item)))
            score -= 1/len(tests)
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        except AssertionError:
            pass
        except:
            outp.write("The call %s%s did not enforce the function precondition.\n" % (func,repr(item)))
            score -= 1/len(tests)
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


pass
#mark -
#mark Graders
def grade_func(func,outp=sys.stdout):
    """
    Grades the given function.
    
    Parameter func: The function name
    Precondition: func is a string and a name of a function in currency
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    msg = 'Comments for %s' % repr(func)
    outp.write(msg+'\n')
    outp.write(('='*len(msg))+'\n')
    file = 'testcurrency.py'
    status, p1 = grade_test_cases(file,func,1,outp)
    if p1 == 1:
        outp.write('The test cases look good.\n')
    else:
        outp.write('\n')
    
    file = 'currency.py'
    status, p2a = grade_func_stub(file,func,1,outp)
    if not status:
        status, p2b = grade_func_body(file,func,1,outp)
    else:
        p2b = 0
    if p2a == 1 and p2b == 1:
        outp.write('The implementation looks good.\n')
    else:
        outp.write('\n')
    p2 = 0.2*p2a+0.8*p2b
    
    if not status:
        status, p3 = grade_asserts(file,func,1,outp)
        if p3 == 1:
            outp.write('The assert statements look good.\n')
    else:
        p3 = 0
    
    outp.write('\n')
    total = round(0.5*p1+0.4*p2+0.1*p3,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return round(0.5*grade_func('iscurrency',outp)+
                 0.5*grade_func('exchange',outp),   3)


if __name__ == '__main__':
    print(grade())