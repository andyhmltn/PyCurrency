from PyCurrency import *

# Instantiate the class
convert = PyCurrency()

# How much USD is 10 GBP? Don't round it, please!
print convert.convert(10, 'GBP', 'USD')

# How much USD do I need for 20 EUR? Oh, and round it :)
print convert.amountTo(20, 'USD', 'EUR', True)