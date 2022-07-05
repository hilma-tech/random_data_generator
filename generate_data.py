import csv
import os
import pandas as pd
from pathlib import Path
from functools import partial
import datetime
from faker import Faker
import configparser
from faker.providers import BaseProvider

# WHAT IS LEFT
'''
DUPLICATES: allow users to choose to create duplicates
CHOOSE WHICH ROWS TO DUPLICATE AND WHICH TO DO RANDOM THINGS
maybe when they upload a file they can choose which columns are random from faker or random from col?
'''
#send row before it is added to the list of lists list.insert(spot, element)

class DataTypeProvider(BaseProvider):
    

    def create_col_using_data(self, data, rows):
        fake = Faker()
        # with open('fake_data_export.csv', "w", newline='') as csvFile: # create a new file (or overwrite) to write data to
        #     writer = csv.writer(csvFile)
        #     writer.writerow(data.columns.values) # write the column names from the user provided csv file
        # all_random_col_data = [] # list of lists of randomly generated data 
        random_col_data = [] # temporary list that will be appened to above list

        #for col_name in data.columns: # loop through all cols in file
        # if numDups != 0:
        #     rand_num = fake.pyint(1, numDups)
        for _ in range(rows): # generate however many rows are necessary
            # random_data = fake.random_element(data) # need to dupe only cols not rows too
                #if numDups == 0:
                    # random_col_data.append(random_data)
                # else:
                #     for _ in range(rand_num):
            random_col_data.append(fake.random_element(data)) # randomly choosing from given data
        # all_random_col_data.append(random_col_data) # add to list of lists
        # random_col_data = [] # reset temp array
        #all_data = list(zip(*all_random_col_data)) # zip the data so each tuple is one row in the csv file
        #print(all_data)
        #writer.writerows(all_data) # write the list of tuples to the csv file
        return random_col_data
    
    def create_col_using_faker(self, dataType, rows, startDate=None, endDate=None, min=None, max=None, content=None):
        
        fake = Faker()

        switcher = {
            "int": partial(fake.random_int, min, max),
            "uuid": fake.uuid4,
            "date between": partial(fake.date_between, startDate, endDate), #date_between
            "timestamp": partial(fake.date_time_between, startDate, endDate),
            "first name": fake.first_name, #first_name
        }
        # need to generate ints, uuid, things related to dates, name
        #Create fake data using faker 
        temp_data = []
        # for col in columnType:
        typeNeeded = switcher.get(dataType, switcher.get(content))
        # if(dataType.lower() == "id"):
        #     temp_data = running_id(rows)
        # else:
        for _ in range(rows): 
            if callable(typeNeeded):
                temp_data.append(typeNeeded())

        return temp_data
    


    
def fake_data(dataType, rows, startDate=None, endDate=None, min=None, max=None, content=None):
    fake = Faker()
    fake.add_provider(DataTypeProvider)
    return fake.create_col_using_faker(dataType, rows, startDate, endDate, min, max, content)
    # df = pd.DataFrame(list()) # Create a new csv file that will contain the randomly generated data 
    # df.to_csv("fake_data_export.csv")
    # fake = Faker()
    # switcher = {
    #     "int": partial(fake.random_int, min, max),
    #     "uuid": fake.uuid4,
    #     "date between": partial(fake.date_between, startDate, endDate), #date_between
    #     "timestamp": partial(fake.date_time_between, startDate, endDate),
    #     "first name": fake.first_name, #first_name
    #     #"id": running_id
    # }
    # # need to generate ints, uuid, things related to dates, name
    # #Create fake data using faker 
    # data_to_be_exported = []
    # temp_data = []
    # # for col in columnType:
    # typeNeeded = switcher.get(dataType)
    # # if(dataType.lower() == "id"):
    # #     temp_data = running_id(rows)
    # # else:
    # for _ in range(rows): 
    #     if callable(typeNeeded):
    #         temp_data.append(typeNeeded())

    # return temp_data
    # data_to_be_exported.append(temp_data)
    # all_data = list(zip(*data_to_be_exported))
    # df = pd.DataFrame(all_data)
    # filepath = Path(r'c:\Users\pc\Downloads\fake_data_export.csv')
    # df.to_csv("fake_data_export.csv", index=False, header=header)

# this is a function that generates data based off a csv file that has premade columns 
def fake_data_uploaded(data, rows):
    fake = Faker()
    fake.add_provider(DataTypeProvider) # add the newly created provider so Faker knows what it is
    return fake.create_col_using_data(data, rows) # run the function that was created to generate values 



startDate = datetime.datetime(1970,1,1)
endDate = datetime.datetime.now()

def create_csv():
    
    df = pd.DataFrame(list()) # Create a new csv file that will contain the randomly generated data 
    df.to_csv(f"{table_name}.csv")

    file_data = []

    standardized = [ element.replace(' ', '') for element in content ]
    
    for i in range(len(header)):

        if(unique[i].lower() == 'running'):
            min, rows = map(int, standardized[i].split("-"))
            file_data.append([i for i in range(1, rows+1) ])
            
        elif(columnDataType[i].lower() == 'int'):
            min, max = map(int, standardized[i].split("-"))
            file_data.append(fake_data(columnDataType[i], rows, min=min, max=max))

        elif(columnDataType[i].lower() == 'input'):
            file_data.append(fake_data_uploaded(standardized[i].split(','), rows))

        elif(columnDataType[i].lower() == 'string'):
            file_data.append(fake_data(columnDataType[i], rows, content=content[i]) )

        elif(columnDataType[i].lower() == 'timestamp'):
            start, end = standardized[i].split('-')
            year, month, day = map(int, start.split('/'))
            startDate = datetime.datetime(year, month, day)
            year, month, day = map(int, end.split('/'))
            endDate = datetime.datetime(year, month, day)
            file_data.append(fake_data(columnDataType[i], rows, startDate, endDate))
        
        
        

    all_data = list(zip(*file_data))
    df = pd.DataFrame(all_data)
    df.to_csv(f"{table_name}.csv", index=False, header=header)
   

        
header = [] # column names
columnDataType = [] 
unique = []
content = []

def parse_data():
    global table_name, header, columnDataType, unique, content
    config = configparser.ConfigParser()
    config.read('data_configurator.ini')
    data = pd.read_csv(config['Input Table']['file'])
    table_name = data['table'].values[0]
    header = data['column'].values
    columnDataType = data['data_type'].values
    unique = data['unique'].values
    content = data['content/range'].values
    
def main():
    parse_data()
    create_csv()

    # user_input = input("Upload data or enter column and type? (upload or manual) ")
    # numRows = int(input("How many rows would you like generated? "))
    # dupsAns = ""
    # dups = False
    # numDups = 0
    # if user_input == "manual":
    #     while True: # Get user input until user quits
    #         column_name = input("Enter column name or quit: ")
    #         if column_name == "quit":
    #             break
    #         # if dupsAns.lower() == "yes": 
    #         #     dups = True
    #         #     dupeCol.append(1)
    #         #     numDups = int(input("What is the maximum duplicates that can appear in a column?"))
    #         # else:
    #         #     dupeCol.append(0)
    #         header.append(column_name)
    #         column_type = input("Enter type (int, uuid, date between, date time, first name, running id): ")
    #         startDate = datetime.datetime(1970,1,1)
    #         endDate = datetime.datetime.now()
    #         min = 0
    #         max = 9999
    #         if(column_type.lower() == "date between" or column_type.lower() == "date time between"):
    #             date = input("Start date (YYYY-MM-DD): ")
    #             year, month, day = map(int, date.split('-'))
    #             startDate = datetime.datetime(year, month, day)
    #             date = input("End date (YYYY-MM-DD): ")
    #             year, month, day = map(int, date.split('-'))
    #             endDate = datetime.datetime(year, month, day)
    #         elif (column_type.lower() == "int"):
    #             range = input("Input a range between 0 and 9999 (i.e 2-2000): ")
    #             min, max = map(int, range.split("-"))

    #         dups = bool(input("Would you like duplicates? "))
    #         columnType.append(column_type)
    #     fake_data(numRows, startDate, endDate, min, max)
    #     #print(columns)
    # else:
    #     # if dupsAns.lower() == "yes": 
    #     #     dups = True
    #     #     dupeCol.append(1)
    #     #     numDups = int(input("What is the maximum duplicates that can appear in a column? "))
    #     # else:
    #     #     dupeCol.append(0)
    #     csvFile = input("Input file name and location: ")
    #     data = pd.read_csv(csvFile) # Use pandas library to read the csv file as input 
    #     for col in data.columns:
    #         fakeOrRealData.append(input(f"Should the data for {col.upper()} be fake or should the data be randomized from column data? (fake or random): "))

    #     #print(data.head())
    #     fake_data_uploaded(data, numRows, numDups)


    
    print(f"Data generated! Check your working directory for the file {table_name}!")

if __name__ == "__main__":
    main()