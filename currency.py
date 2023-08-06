"""
Module for currency exchange

This module provides several string parsing functions to implement a simple
currency exchange routine using an online currency service. The primary function
in this module is exchange().

Author: Monika Racia
Date:   October 28, 2022
"""
import introcs

APIKEY = "skUUt7kY3w7AKWopByMWR8QS10r2ZlsUT3xSVvPtipAe"

def before_space(s):
    """
    Returns the substring of s up to, but not including, the first space.

    Example: before_space('Hello World') returns 'Hello'
    
    Parameter s: the string to slice
    Precondition: s is a string with at least one space in it
    """

    #Enforce the preconditions
    assert type(s) == str, "Precondition violation"
    assert introcs.count_str(s, " ") >= 1, "Precondition violation"

    pos = introcs.find_str(s, " ")
    #print(pos)
    result = s[:pos]
    #print(result)
    return result
    

def after_space(s):
    """
    Returns the substring of s after the first space
    
    Example: after_space('Hello World') returns 'World'
    
    Parameter s: the string to slice
    Precondition: s is a string with at least one space in it
    """

    assert type(s) == str, "Precondition violation"
    assert introcs.count_str(s, " ") >= 1, "Precondition violation"

    pos = introcs.find_str(s, " ")
    result = s[pos + 1:]
    #print(result)
    return result


def first_inside_quotes(s):
    """
    Returns the first substring of s between two (double) quote characters
    
    Note that the double quotes must be part of the string.  So "Hello World" is a 
    precondition violation, since there are no double quotes inside the string.
    
    Example: first_inside_quotes('A "B C" D') returns 'B C'
    Example: first_inside_quotes('A "B C" D "E F" G') returns 'B C', because it only 
    picks the first such substring.
    
    Parameter s: a string to search
    Precondition: s is a string with at least two (double) quote characters inside
    """

    assert type(s) == str, "Precondition violation"
    assert introcs.count_str(s, "\"") >= 2, "Precondition violation"

    first_parens = introcs.find_str(s, "\"")
    #print(first_parens)
    n = s[first_parens+1:]
    #print(n)
    second_parens = introcs.find_str(n, "\"")
    #print(second_parens)
    result = n[:second_parens]
    return result


def get_src(json):
    """
    Returns the src value in the response to a currency query.
    
    Given a JSON string provided by the web service, this function returns the string
    inside string quotes (") immediately following the substring '"src"'. For example,
    if the json is
    
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'
    
    then this function returns '2 United States Dollars' (not '"2 United States Dollars"'). 
    On the other hand if the json is 
    
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'
    
    then this function returns the empty string.
    
    The web server does NOT specify the number of spaces after the colons. The JSON
    
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
    
    is also valid (in addition to the examples above).
    
    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
    """

    assert type(json) == str, "Precondition violation"

    src = introcs.find_str(json, "\"src\"")
    #print(src)
    n = json[src+5:]
    #print(n)
    result = first_inside_quotes(n)
    #print(result)
    return result


def get_dst(json):
    """
    Returns the dst value in the response to a currency query.
    
    Given a JSON string provided by the web service, this function returns the string
    inside string quotes (") immediately following the substring '"dst"'. For example,
    if the json is
    
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'
    then this function returns '1.772814 Euros' (not '"1.772814 Euros"'). On the other
    hand if the json is 
    
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'
    
    then this function returns the empty string.
    
    The web server does NOT specify the number of spaces after the colons. The JSON
    
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
    
    is also valid (in addition to the examples above).
    
    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
    """

    assert type(json) == str, "Precondition violation"

    dst = introcs.find_str(json, "\"dst\"")
    #print(dst)
    n = json[dst+5:]
    #print(n)
    result = first_inside_quotes(n)
    #print(result)
    return result


def has_error(json):
    """
    Returns True if the response to a currency query encountered an error.
    
    Given a JSON string provided by the web service, this function returns True if the
    query failed and there is an error message. For example, if the json is
    
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'
        
    then this function returns True (It does NOT return the error message 
    'Source currency code is invalid'). On the other hand if the json is 
    
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'
    
    then this function returns False.
    
    The web server does NOT specify the number of spaces after the colons. The JSON
    
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
        
    is also valid (in addition to the examples above).
    
    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
    """

    assert type(json) == str, "Precondition violation"

    error = introcs.find_str(json, "\"error\"")
    #print(error)
    n = json[error+7:]
    result = first_inside_quotes(n)
    #print(result)
    return result != ""


def service_response(src, dst, amt):
    """
    Returns a JSON string that is a response to a currency query.
    
    A currency query converts amt money in currency src to the currency dst. The response 
    should be a string of the form
    
        '{"success": true, "src": "<src-amount>", dst: "<dst-amount>", error: ""}'
        
    where the values src-amount and dst-amount contain the value and name for the src 
    and dst currencies, respectively. If the query is invalid, both src-amount and 
    dst-amount will be empty, and the error message will not be empty.
    
    There may or may not be spaces after the colon.  To test this function, you should
    chose specific examples from your web browser.
    
    Parameter src: the currency on hand
    Precondition src is a nonempty string with only letters
    
    Parameter dst: the currency to convert to
    Precondition dst is a nonempty string with only letters
    
    Parameter amt: amount of currency to convert
    Precondition amt is a float or int
    """

    assert type(src) == str, "Precondition violation"
    assert introcs.isalpha(src) == True, "Precondition violaton"

    assert type(dst) == str, "Precondition violation"
    assert introcs.isalpha(dst) == True, "Precondition violaton"

    assert type(amt) == float or type(amt) == int, "Precondition violation"

    query_string = "https://ecpyfac.ecornell.com/python/currency/fixed?src=" + (src) +\
    "&dst=" + (dst) + "&amt=" + str(amt) + "&key=" + APIKEY
    result = introcs.urlread(query_string)
    return result


def iscurrency(currency):
    """
    Returns True if currency is a valid (3 letter code for a) currency.
    
    It returns False otherwise.
    
    Parameter currency: the currency code to verify
    Precondition: currency is a nonempty string with only letters
    """

    assert introcs.isalpha(currency) == True, "Precondition violation"

    api_response = service_response(currency, "EUR", 2.0)
    error_check = has_error(api_response)
    return error_check != True


def exchange(src, dst, amt):
    """
    Returns the amount of currency received in the given exchange.
    
    In this exchange, the user is changing amt money in currency src to the currency 
    dst. The value returned represents the amount in currency currency_to.
    
    The value returned has type float.

    Parameter src: the currency on hand
    Precondition src is a string for a valid currency code
    
    Parameter dst: the currency to convert to
    Precondition dst is a string for a valid currency code
    
    Parameter amt: amount of currency to convert
    Precondition amt is a float or int
    """
    
    assert iscurrency(src) and iscurrency(dst) == True, "Precondition violation"
    assert introcs.isfloat(amt) or introcs.isint(amt) == True, "Precondition violation"
    api_response = service_response(src, dst, amt)
    dst_loc = get_dst(api_response)
    dst_value = introcs.index_str(dst_loc, " ")
    value_loc = dst_loc[:dst_value]
    return float(value_loc)