import csv
import os
import pandas as pd
import random
from pathlib import Path
from faker import Faker
from faker.providers import BaseProvider, DynamicProvider

# WHAT IS LEFT
'''
DUPLICATES: allow users to choose to create duplicates
'''

def fake_data(rows):
    df = pd.DataFrame(list()) # Create a new csv file that will contain the randomly generated data 
    df.to_csv("fake_data_export.csv")
    fake = Faker()
    switcher = {
        "int": fake.random_int,
        "uuid": fake.uuid4,
        "date between": fake.date_between, #date_between
        "date time": fake.date_time,
        "first name": fake.first_name #first_name
    }
    # need to generate ints, uuid, things related to dates, name
    #Create fake data using faker 
    data_to_be_exported = []
    temp_data = []
    for col in columnType:
        typeNeeded = switcher.get(col)
        for _ in range(rows): 
            if callable(typeNeeded):
                temp_data.append(typeNeeded())
        data_to_be_exported.append(temp_data)
    all_data = list(zip(*data_to_be_exported))
    df = pd.DataFrame(all_data)
    filepath = Path(r'c:\Users\pc\Downloads\fake_data_export.csv')
    df.to_csv(filepath, index=False, header=header)    
# this is a function that generates data based off a csv file that has premade columns 
def fake_data_uploaded(data, rows):
    fake = Faker()

    class DataTypeProvider(BaseProvider):

        def create_csv(self):
            with open(os.path.join(r'c:\Users\pc\Downloads','fake_data_export.csv'), "w", newline='') as csvFile: # create a new file (or overwrite) to write data to
                writer = csv.writer(csvFile)
                writer.writerow(data.columns.values) # write the column names from the user provided csv file
                all_random_col_data = [] # list of lists of randomly generated data 
                random_col_data = [] # temporary list that will be appened to above list

                for col_name in data.columns: # loop through all cols in file
                        for _ in range(rows): # generate however many rows are necessary
                                random_col_data.append(fake.random_element(data[col_name].values)) # randomly choosing from given data
                        all_random_col_data.append(random_col_data) # add to list of lists
                        random_col_data = [] # reset temp array
                all_data = list(zip(*all_random_col_data)) # zip the data so each tuple is one row in the csv file
                #print(all_data)
                writer.writerows(all_data) # write the list of tuples to the csv file

    fake.add_provider(DataTypeProvider) # add the newly created provider so Faker knows what it is
    fake.create_csv() # run the function that was created to generate values 


header = [] # column names
columnType = [] 
def main():
    user_input = input("Upload data or enter column and type? (upload or manual) ")
    numRows = int(input("How many rows would you like generated? "))
    if user_input == "manual":
        while True: # Get user input until user quits
            column_name = input("Enter column name or quit: ")
            if column_name == "quit":
                break
            header.append(column_name)
            column_type = input("Enter type (int, uuid, between 2 dates, date time, first name): ")
            columnType.append(column_type)
        fake_data(numRows)
        #print(columns)
    else:
        csvFile = input("Input file name and location: ")
        data = pd.read_csv(csvFile) # Use pandas library to read the csv file as input 
        #print(data.head())
        fake_data_uploaded(data, numRows)

if __name__ == "__main__":
    main()