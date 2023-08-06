"""
User interface for module currency

When run as a script, this module prompts the user for two currencies and amount.
It prints out the result of converting the first currency to the second.

Author: Monika Racia
Date:   October 28, 2022
"""
import currency


dst_input = input("3-letter code for original currency: ")
src_input = input("3-letter code for the new currency: ")
amt_input = float(input("Amount of the original currency: "))
result = currency.exchange(dst_input, src_input, amt_input)
result2 = round(result, 3)

print("You can exchange " + str(amt_input) + " " + str(dst_input) + " for " + str(result2) + " " + str(src_input) + ".")


