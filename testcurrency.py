"""
Unit tests for module currency

When run as a script, this module invokes several procedures that test
the various functions in the module currency.

Author: Monika Racia
Date:   October 28, 2022
"""
import introcs
import currency

# Script code
def test_before_space():
    """
    Test procedure for before_space.
    """
    
    print("Testing before_space.")

    result = currency.before_space("2.30 Euros")
    introcs.assert_equals("2.30", result)

    result = currency.before_space(" 23.2")
    introcs.assert_equals("", result)

    result = currency.before_space("5.54 United States Dollars")
    introcs.assert_equals("5.54", result)

    result = currency.before_space("2.35  Turkish Lira")
    introcs.assert_equals("2.35", result)


def test_after_space():
    """
    Test procedure for after_space.
    """

    print("Testing after_space.")

    result = currency.after_space("2.30 Euros")
    introcs.assert_equals("Euros", result)

    result = currency.after_space("Euros ")
    introcs.assert_equals("", result)

    result = currency.after_space("5.54 United States Dollars")
    introcs.assert_equals("United States Dollars", result)

    result = currency.after_space("2.35  Turkish Lira")
    introcs.assert_equals(" Turkish Lira", result)


def test_first_inside_quotes():
    """
    Test procedure for first_inside_quotes.
    """

    result = currency.first_inside_quotes("true, \"src\": 2")
    introcs.assert_equals("src", result)

    result = currency.first_inside_quotes("\"success\": true, \"src\":")
    introcs.assert_equals("success", result)

    result = currency.first_inside_quotes("\"dst\"")
    introcs.assert_equals("dst", result)

    result = currency.first_inside_quotes("\"\"")
    introcs.assert_equals("", result)

    print("Testing first_inside_quotes.")


def test_get_src():
    """
    Test procedure for get_src.
    """

    result = currency.get_src("{\"success\": true, \"src\": \"2 United States "+\
    "Dollars\", \"dst\": \"1.772814 Euros\", \"error\": \"\"}")
    introcs.assert_equals("2 United States Dollars", result)

    result = currency.get_src("{\"success\": true, \"src\":\"2 United States "+\
    "Dollars\", \"dst\": \"1.772814 Euros\", \"error\": \"\"}")
    introcs.assert_equals("2 United States Dollars", result)

    result = currency.get_src("{\"success\":false,\"src\":\"\",\"dst\":\"\","+\
    "\"error\": \"Source currency code is invalid.\"}")
    introcs.assert_equals("", result)

    result = currency.get_src("{\"success\":false,\"src\": \"\",\"dst\":\"\","+\
    "\"error\": \"Source currency code is invalid.\"}")
    introcs.assert_equals("", result)

    print("Testing get_src.")


def test_get_dst():
    """
    Test procedure for get_dst.
    """

    result = currency.get_dst("{\"success\": true, \"src\": \"2 United States "+\
    "Dollars\", \"dst\": ""\"1.772814 Euros\", \"error\": \"\"}")
    introcs.assert_equals("1.772814 Euros", result)

    result = currency.get_dst("{\"success\": true, \"src\":\"2 United States "+\
    "Dollars\", \"dst\":\"1.772814 Euros\", \"error\": \"\"}")
    introcs.assert_equals("1.772814 Euros", result)

    result = currency.get_dst("{\"success\":false,\"src\":\"\",\"dst\":"+\
    "\"\",\"error\":\"Source currency code is invalid.\"}")
    introcs.assert_equals("", result)

    result = currency.get_dst("{\"success\":false,\"src\": \"\",\"dst\": "+\
    "\"\",\"error\":\"Source currency code is invalid.\"}")
    introcs.assert_equals("", result)

    print("Testing get_dst.")


def test_has_error():
    """
    Test procedure for has_error.
    """

    result = currency.has_error("{\"success\":false,\"src\":\"\",\"dst\":\"\",\"error"+\
    "\": \"Source currency code is invalid.\"}")
    introcs.assert_true(result)

    result = currency.has_error("{\"success\":false,\"src\":\"\",\"dst\":\"\","+\
    "\"error\":\"Source currency code is invalid.\"}")
    introcs.assert_true(result)

    result = currency.has_error("{\"success\": true, \"src\": \"2 United States "+\
    "Dollars\", \"dst\": \"1.772814 Euros\", \"error\": \"\"}")
    introcs.assert_false(result)

    result = currency.has_error("{\"success\": true, \"src\": \"2 United States "+\
    "Dollars\", \"dst\": \"1.772814 Euros\", \"error\":\"\"}")
    introcs.assert_false(result)

    print("Testing has_error.")


def test_service_response():
    """
    Test procedure for service_response.
    """

    result = currency.service_response("USD", "EUR", 2.5)
    introcs.assert_equals("{\"success\": true, \"src\": \"2.5 United States "+\
    "Dollars\", \"dst\": \"2.2160175 Euros\", \"error\": \"\"}", result)
    
    result = currency.service_response("USD", "EUR", -2.5)
    introcs.assert_equals("{\"success\": true, \"src\": \"-2.5 United States "+\
    "Dollars\", \"dst\": \"-2.2160175 Euros\", \"error\": \"\"}", result)

    result = currency.service_response("PZN", "EUR", -2.5)
    introcs.assert_equals("{\"success\": false, \"src\": \"\", \"dst\": \"\", "+\
    "\"error\": \"The rate for currency PZN is not present.\"}", result)

    result = currency.service_response("PLN", "ERU", -2.5)
    introcs.assert_equals("{\"success\": false, \"src\": \"\", \"dst\": \"\", "+\
    "\"error\": \"The rate for currency ERU is not present.\"}", result)

    print("Testing service_response.")


def test_iscurrency():
    """
    Test procedure for iscurrency.
    """

    result = currency.iscurrency("USD")
    introcs.assert_true(result)

    result = currency.iscurrency("ERU")
    introcs.assert_false(result)

    print("Testing iscurrency.")


def test_exchange():
    """
    Test procedure for exchange.
    """

    result = currency.exchange("PLN", "EUR", -3.5)
    introcs.assert_floats_equal(-0.8189057674541375, result)

    result = currency.exchange("PLN", "EUR", 3.5)
    introcs.assert_floats_equal(0.8189057674541375, result)

    print("Testing exchange.")


test_before_space()
test_after_space()
test_first_inside_quotes()
test_get_src()
test_get_dst()
test_has_error()
test_service_response()
test_iscurrency()
test_exchange()
print("All tests completed successfully.")