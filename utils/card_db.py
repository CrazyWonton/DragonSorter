#card_db.py

import re
import urllib.request
import json
import urllib.parse

# Clean up text for db lookup
def clean_text(text):
    # trim leading and trailing whitesapce from text
    text = text.strip()  
    # remove trailing non-alphanumeric characters from text
    text = re.sub(r'[^a-zA-Z0-9]+$', '', text)
    # remove all non-alphanumeric characters from text
    text = re.sub(r'\W+', '_', text)
    return text

# Test clean_text
def test_clean_text():
    text = "Hello, World!"
    cleaned_text = clean_text(text)
    print(cleaned_text)
    assert cleaned_text == "Hello_World"

# Look up card name in db and get price
def lookup_average_price(name):
    url = "https://api.scryfall.com/cards/named?fuzzy=" + urllib.parse.quote(name)
    #try:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    prices = []
    return data["prices"]["usd"]
    
# Test lookup_average_price
def test_lookup_average_price():
    price = lookup_average_price("kamahl_pit_fighter")
    print(price)
    # cast price to float and make sure it is greater than 0
    price_1 = float(price)
    assert price_1 > 0

#test_clean_text()
#test_lookup_average_price()
