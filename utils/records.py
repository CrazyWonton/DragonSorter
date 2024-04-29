#records.py

import sys
import csv
import readline
import glob

csv_file = None

# Allow user to set csv file name and location
def set_csv_file():
  # Allow user to specify the name and location of the CSV file they want to create
    global csv_file
    # Prompt user to enter name and location of CSV file to create, then provide autocompletion
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(' \t\n')
    readline.set_completer(lambda input, state: [i for i in glob.glob(input + '*')][state]) 
    csv_file = input("Enter name and location of CSV file to create: ")
    print("CSV file set to: " + csv_file)
    # create csv file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'price'])
        file.close()
    print("CSV file created successfully!")


# Test set_csv_file
def test_set_csv_file():
    set_csv_file()

# Add card entry (name,price) to csv file
def add_card_entry(name, price):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, price])
        file.close()


# Test add_card_entry
def test_add_card_entry():
    add_card_entry("Kamahl Pit Fighter", "1.00")

#test_set_csv_file()
#test_add_card_entry()
