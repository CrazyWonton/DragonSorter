#sorter.py

import sys

min_price = 0.0

# Allow user to set min price threshold
def set_min_price_threshold():
    if len(sys.argv) > 1:
        min_price = float(sys.argv[1])
    else:
        print("Enter minimum price threshold: ")
        min_price = float(input())
    while min_price < 0.0:
        print("Min price must be greater than or equal to 0.0")
        min_price = float(input())

# Test set_min_price_threshold
def test_set_min_price_threshold():
    set_min_price_threshold()

# Determine if price is above min price threshold
def is_above_threshold(price):
    if price >= min_price:
        return True
    else:
        return False

# Test is_above_threshold
def test_is_above_threshold():
    # set global value of min_price to 3.7
    global min_price
    min_price = 3.7
    assert is_above_threshold(4.0) == True
    assert is_above_threshold(2.0) == False

#test_set_min_price_threshold()
#test_is_above_threshold()
