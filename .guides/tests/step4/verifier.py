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
def the_first(s):
    """Helper function"""
    pos1 = s.find('"')
    pos2 = s.find('"',pos1+1)
    return s[pos1+1:pos2]


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
    
    def reset(self):
        self._tests   = {}
        self._asserts = {}
    
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
    
    def get_src1(self,s):
        """
        Incorrect version for first pass
        """
        if not 'get_src' in self._tests:
            self._tests['get_src'] = []
        self._tests['get_src'].append(s)
        return None
    
    def get_src2(self,s):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'get_src' in self._tests:
            self._tests['get_src'] = []
        self._tests['get_src'].append(s)
        return self.get_src3(s)
    
    def get_src3(self,s):
        """
        Correct version, no logging
        """
        return the_first(s[s.find('"src"')+5:])
    
    def get_dst1(self,s):
        """
        Incorrect version for first pass
        """
        if not 'get_dst' in self._tests:
            self._tests['get_dst'] = []
        self._tests['get_dst'].append(s)
        return None
    
    def get_dst2(self,s):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'get_dst' in self._tests:
            self._tests['get_dst'] = []
        self._tests['get_dst'].append(s)
        return self.get_dst3(s)
    
    def get_dst3(self,s):
        """
        Correct version, no logging
        """
        return the_first(s[s.find('"dst"')+5:])
    
    def has_error1(self,s):
        """
        Incorrect version for first pass
        """
        if not 'has_error' in self._tests:
            self._tests['has_error'] = []
        self._tests['has_error'].append(s)
        return 2
    
    def has_error2(self,s):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'has_error' in self._tests:
            self._tests['has_error'] = []
        self._tests['has_error'].append(s)
        return self.has_error3(s)
    
    def has_error3(self,s):
        """
        Correct version, no logging
        """
        return len(the_first(s[s.find('"error"')+7:])) > 0


# Docstrings
DOCSTRING = {
            'get_src':
                ['Returns the src value in the response to a currency query.',
                 ('Given a JSON string provided by the web service, this function returns the string '+
                  'inside string quotes (") immediately following the substring \'"src"\'. For example, '+
                  'if the json is '+
                  '\'{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}\' '+
                  'then this function returns \'2 United States Dollars\' (not \'"2 United States Dollars"\'). '+ 
                  'On the other hand if the json is '+
                  '\'{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}\' '+
                  'then this function returns the empty string. '+
                  'The web server does NOT specify the number of spaces after the colons. The JSON '+
                  '\'{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}\' '+
                  'is also valid (in addition to the examples above).'),
                 ('Parameter json: a json string to parse '+
                  'Precondition: json a string provided by the web service (ONLY enforce the type)')],
            'get_dst':
                ['Returns the dst value in the response to a currency query.',
                 ('Given a JSON string provided by the web service, this function returns the string '+
                  'inside string quotes (") immediately following the substring \'"dst"\'. For example, '+
                  'if the json is '+
                  '\'{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}\' '+
                  'then this function returns \'1.772814 Euros\' (not \'"1.772814 Euros"\'). On the other '+
                  'hand if the json is '+
                  '\'{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}\' '+
                  'then this function returns the empty string. '+
                  'The web server does NOT specify the number of spaces after the colons. The JSON '+
                  '\'{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}\' '+
                  'is also valid (in addition to the examples above).'),
                 ('Parameter json: a json string to parse '+
                  'Precondition: json a string provided by the web service (ONLY enforce the type)')],
            'has_error':
                ['Returns True if the response to a currency query encountered an error.',
                 ('Given a JSON string provided by the web service, this function returns True if the '+
                  'query failed and there is an error message. For example, if the json is '+
                  '\'{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}\' '+
                  'then this function returns True (It does NOT return the error message '+
                  "'Source currency code is invalid'). On the other hand if the json is "+
                  '\'{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}\' '+
                  'then this function returns False. '+
                  'The web server does NOT specify the number of spaces after the colons. The JSON '+
                  '\'{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}\' '+
                  'is also valid (in addition to the examples above).'),
                 ('Parameter json: a json string to parse '+
                  'Precondition: json a string provided by the web service (ONLY enforce the type)')]
            }

# Expected functions
FUNCTIONS = ['get_src','get_dst','has_error']


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
                func.get_src = testplan.get_src2
                func.get_dst = testplan.get_dst2
                func.has_error = testplan.has_error2
            elif step < 2:
                func.get_src = testplan.get_src1
                func.get_dst = testplan.get_dst1
                func.has_error = testplan.has_error1
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
def decode_json(value):
    """
    Returns: decoded JSON string
    
    If the JSON is not valid, this function returns None
    
    Parameter value: A JSON string
    """
    import json
    try:
        decode = json.loads(value)
        if len(decode) !=4:
            return None
        if type(decode['src']) != str:
            return None
        if type(decode['dst']) != str:
            return None
        if type(decode['error']) != str:
            return None
        if type(decode['success']) != bool:
            return None
        if decode['src'] != '' and decode['dst'] == '':
            return None 
        if decode['src'] == '' and decode['dst'] != '':
            return None 
        if decode['src'] == '' and decode['error'] == '':
            return None 
        if decode['src'] != '' and decode['error'] != '':
            return None 
        return decode
    except:
        return None


def encode_get_src(input):
    """
    Returns: the hash encoding for input to get_src
    
    Parameter input: The input to get_src
    """
    if type(input) != str:
        return -1
    elif decode_json(input) is None:
        return -1
    
    tail = input[input.find('"src":')+6:]
    item = the_first(tail)
    if tail[0] == ' ':
        return 3 if item == '' else 4
    else:
        return 1 if item == '' else 2


def encode_get_dst(input):
    """
    Returns: the hash encoding for input to get_dst
    
    Parameter input: The input to get_dst
    """
    if type(input) != str:
        return -1
    elif decode_json(input) is None:
        return -1
    
    tail = input[input.find('"dst":')+6:]
    item = the_first(tail)
    if tail[0] == ' ':
        return 3 if item == '' else 4
    else:
        return 1 if item == '' else 2


def encode_has_error(input):
    """
    Returns: the hash encoding for input to has_error
    
    Parameter input: The input to has_error
    """
    if type(input) != str:
        return -1
    elif decode_json(input) is None:
        return -1
    
    tail = input[input.find('"error":')+8:]
    item = the_first(tail)
    if tail[0] == ' ':
        return 3 if item == '' else 4
    else:
        return 1 if item == '' else 2


# The explanatory reasons for the tests
GET_SRC = [
    'a test with an empty value for "src" and no spaces after the colon',
    'a test with a nonempty value for "src" and no spaces after the colon',
    'a test with an empty value for "src" and spaces after the colon',
    'a test with a nonempty value for "src" and spaces after the colon'
]

GET_DST = [
    'a test with an empty value for "dst" and no spaces after the colon',
    'a test with a nonempty value for "dst" and no spaces after the colon',
    'a test with an empty value for "dst" and spaces after the colon',
    'a test with a nonempty value for "dst" and spaces after the colon'
]

HAS_ERROR = [
    'a test with no error message and no spaces after the colon for "error" or "success"',
    'a test with an error message and no spaces after the colon for "error" or "success"',
    'a test with no error message and spaces after the colon for "error" or "success"',
    'a test with an error message and spaces after the colon for "error" or "success"'
]



pass
#mark -
#mark Subgraders
def grade_func_stub(file,func,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the function stub for the given function.
    
    This function is only good for get_src, get_dst, has_error.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter func: The function being tested (not the test procedure)
    Precondition: func one of 'get_src', 'get_dst', 'has_error'
    
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
    want = 1
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
            descrip = (' '.join(filter(lambda x : x != '', map(lambda x : x.strip(), spec[2:-2])))).strip()
            correct = DOCSTRING[func][1]
            if correct != descrip:
                outp.write('The descriptive paragraph in the specification for %s does not match the one provided:\n' % repr(func))
                outp.write('Found  %s\n' %repr(descrip))
                outp.write('Wanted %s\n' %repr(correct))
                score -= 0.2
                if not step:
                    return (FAIL_BAD_STYLE,max(0,score))
        
        if spec[-3].strip() != '':
            outp.write('The specification of %s does not have a blank line before the parameter.\n' % repr(func))
            score -= 0.2
            if not step:
                return (FAIL_BAD_STYLE,max(0,score))
        else:
            descrip = (' '.join(filter(lambda x : x != '',map(lambda x: x.strip(), spec[-2:])))).strip()
            correct = DOCSTRING[func][2]
            if correct != descrip:
                outp.write('The parameter description for %s does not match the one provided:\n' % repr(func))
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

    if not check_args(body,'json'):
        outp.write('The parameters for %s do not match the specification.\n' % repr(func))
        score -= 1.0
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))



def grade_test_cases(file,func,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test case for the given function.
    
    This function is only good for get_src, get_dst, has_error.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter func: The function being tested (not the test procedure)
    Precondition: func one of 'get_src', 'get_dst', 'has_error'
    
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
    
    env.reset()
    tests.reset()
    proc = getattr(env.module,'test_'+func)
    proc()
    
    if not func in tests.tested:
        outp.write("You have not called the function %s properly in the test cases.\n" % repr(func))
        return (FAIL_INCORRECT,0)
    
    if not 'assert_equals' in tests.asserted or len(tests.asserted['assert_equals']) != len(tests.tested[func]):
        outp.write("You were supposed to call 'assert_equals' for each test case.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    encoder = globals()['encode_'+func]
    correct = getattr(tests,func+'3')
    badin = None
    for pos in range(len(tests.asserted['assert_equals'])):
        if  pos < len(tests.tested[func]):
            pair  = tests.asserted['assert_equals'][pos]
            input = tests.tested[func][pos]
            if pair[0] != correct(input) and encoder(input) >= 0 and correct(input) == pair[1]:
                badin = input
    
    if badin:
        outp.write("In 'assert_equals', the expected value goes first [see %s(%s)].\n" % (func,repr(badin)))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,0)
    
    env, tests = import_script(file,1)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    env.reset()
    tests.reset()
    proc = getattr(env.module,'test_'+func)
    proc()
    
    badin = None
    for pos in range(len(tests.asserted['assert_equals'])):
        pair = tests.asserted['assert_equals'][pos]
        input = tests.tested[func][pos]
        if pair[0] != pair[1] and encoder(input) >= 0:
            badin = tests.tested[func][pos]
        if not badin is None:
            outp.write("The test %s(%s) has incorrect output.\n" % (func,repr(badin)))
            score -= 0.3
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    # Look for proper coverage
    THECASES = globals()[func.upper()]
    results = [0]*len(THECASES)
    for input in tests.tested[func]:
        code = encoder(input)
        if code == -1:
            outp.write("The test %s(%s) violates the precondition.\n" % (func,repr(input)))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        results[code-1] += 1
    
    ntests = len(list(filter(lambda x : x > 0, results)))
    wtests = 4
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
    
    This function is only good for get_src, get_dst, has_error.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter func: The function being tested (not the test procedure)
    Precondition: func one of 'get_src', 'get_dst', 'has_error'
    
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
    
    tests = TestPlan(None)
    submit  = getattr(env.module,func)
    correct = getattr(tests,func+'3')
    inputs = ['{"success": true, "src": "2.5 United States Dollars", "dst": "2.28242 Euros", "error": ""}',
              '{"success": false, "src": "", "dst": "", "error": "The rate for currency EUF is not present."}',
              '{"success":true, "src":"2.5 United States Dollars", "dst":"2.28242 Euros", "error":""}',
              '{"success":false, "src":"", "dst":"", "error":"The rate for currency EUF is not present."}']
    for item in inputs:
        try:
            want = correct(item)
            have = submit(item)
            if want != have:
                outp.write('Call %s(%s) returned %s, not the expected %s.\n' % (func,repr(item),repr(have),repr(want)))
                score -= 1.0/len(inputs)
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
        except:
            outp.write('Call %s(%s) crashed.\n' % (func,repr(item)))
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
            elif type(frag) in [ast.If, ast.For, ast.While, ast.Try]:
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
    
    This function is only good for get_src, get_dst, has_error.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter func: The function being tested (not the test procedure)
    Precondition: func one of 'get_src', 'get_dst', 'has_error'
    
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
    tests  = ['{"success": true, "src": "2.5 United States Dollars", "dst": "2.28242 Euros", "error": ""}',
              '{"success": false, "src": "", "dst": "", "error": "The rate for currency EUF is not present."}',
              '{"success":true, "src":"2.5 United States Dollars", "dst":"2.28242 Euros", "error":""}',
              '{"success":false, "src":"", "dst":"", "error":"The rate for currency EUF is not present."}']
    for item in tests:
        try:
            call(item)
        except:
            import traceback
            outp.write("The call %s(%s) no longer works properly.\n" % (func,repr(item)))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 1/len(tests)
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    tests = [1,True,3.5]
    for item in tests:
        try:
            call(item)
            outp.write("The call %s(%s) did not enforce the function precondition.\n" % (func,repr(item)))
            score -= 1/len(tests)
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        except AssertionError:
            pass
        except:
            outp.write("The call %s(%s) did not enforce the function precondition.\n" % (func,repr(item)))
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
    p1 = 0.3*grade_func('get_src',outp)
    p2 = 0.3*grade_func('get_dst',outp)
    p3 = 0.4*grade_func('has_error',outp)
    return round(p1+p2+p3,3)


if __name__ == '__main__':
    print(grade())