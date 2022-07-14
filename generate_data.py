import pandas as pd
import numpy as np
from functools import partial
import datetime
from faker import Faker
import configparser
import logging
from faker.providers import BaseProvider

def child_table_generate(numIDs, numIndx):
    fake = Faker()
    id_col = []
    index_col = []
    id_number = 1
    while(id_number != numIDs+1): # while loop goes up to the number of id's in the parent table
        duplicates = fake.random_int(1, numIndx) # random number of rows is generated
        for _ in range(duplicates):
            id_col.append(id_number)
        id_number += 1
    index_col.append(1)
    counter = 1
    for i in range(1, len(id_col)): 
        if id_col[i-1] != id_col[i]: # checks if the previous element is the same as the last and start the counter again or adds to it
            index_col.append(1)
            counter = 1
        else:
            counter += 1
            index_col.append(counter)
    return id_col, index_col, len(id_col)

def consec_dates(datesArr, startDate): # adds 1 to the date 
    return datesArr[-1] + datetime.timedelta(days=1) if len(datesArr) != 0 else startDate
    
def consec_datetimes(startDate, rows):
    fake = Faker()
    temp_time = []
    unix_start_time = datetime.datetime.timestamp(startDate) #convert it to unix timestamp to generate random times
    temp_time.append(datetime.datetime.fromtimestamp(unix_start_time))
    next_day = unix_start_time # generate random datetimes using unix time stamp since it is an integer and faster than using datetime library
    for _ in range(rows):
        next_day += 60*60*24
        next_day += fake.random_int(1, 86399) #this is how many seconds are in a day so it can generate between midnight and next midnight
        temp_time.append(datetime.datetime.fromtimestamp(next_day))
    return temp_time

# create a class whose parent class is the BaseProvider for faker, basically creating own providers
class DataTypeProvider(BaseProvider):
    
    def create_col_using_data(self, data, rows):
        fake = Faker()

        random_col_data = [] # temporary list that will be returned
        for _ in range(rows): # generate however many rows are necessary
            random_col_data.append(fake.random_element(data)) # randomly choosing from given data

        return random_col_data
    
    def create_col_using_faker(self, dataType, rows, startDate=None, endDate=None, min=None, max=None, contentCell=None, uniqueCell='no'):
        
        fake = Faker()
        temp_data = []

        # Dictionary that holds possible inputs from the user and makes them unique depending on if the user wants unique values
        # partial function is used so that when I call the function in the for loop below it will automatically send the argument
        switcher = {
            "int": partial(fake.unique.random_int, min, max) if uniqueCell=="yes" else partial(fake.random_int, min, max),
            "uuid": fake.unique.uuid4 if uniqueCell=="yes" else fake.uuid4,
            "date": partial(fake.unique.date_between, startDate, endDate) if uniqueCell=="yes" 
                    else partial(consec_dates, temp_data, startDate) if uniqueCell=="consecutive" 
                    else partial(fake.date_between, startDate, endDate),
            "timestamp": partial(fake.unique.date_time_between, startDate, endDate) if uniqueCell=="yes" 
                    else partial(fake.date_time_between, startDate, endDate),
            "name": fake.first_name,
            "bool": fake.pybool
        }
        
        #Create fake data using faker 
        
        typeNeeded = switcher.get(dataType, switcher.get(contentCell)) # get the value and if its a string get the value from the content array
        for _ in range(rows): 
            if callable(typeNeeded): # check if the value in the dictionary is callable and then call the function
                temp_data.append(typeNeeded())
        return temp_data


def fake_data(dataType, rows, startDate=None, endDate=None, min=None, max=None, contentCell=None, uniqueCell='no'):
    fake = Faker()
    fake.add_provider(DataTypeProvider)# add the newly created provider so Faker knows what it is
    return fake.create_col_using_faker(dataType, rows, startDate, endDate, min, max, contentCell, uniqueCell) # run the function that was created to generate values 

# this is a function that generates data based off a csv file that has premade columns 
def fake_data_uploaded(data, rows):
    fake = Faker()
    fake.add_provider(DataTypeProvider) # add the newly created provider so Faker knows what it is
    return fake.create_col_using_data(data, rows) # run the function that was created to generate values 


startDate = datetime.datetime(1970,1,1) # intitalizing the start and end dates
endDate = datetime.datetime.now()

def create_csv():
    
    for j in range(len(header)): # loop through all the tables that are supposed to be created

        file_data = []
        rows = 0
        df = pd.DataFrame(list()) # Create a new csv file that will contain the randomly generated data 
        df.to_csv(f"{table_name[j]}.csv") # write nothing to the csv file with the name of the table

        standardized = [ element.lower() for element in unique[j]] # lowercase all the elements just in case nothing extra

        # try catch depending on if there is an id counter or if the number of rows is random everytime 
        try:
            parent_id_loc = standardized.index('parent_id') # finds the index of the parent_id
            index_spot = standardized.index('index') # finds the index of the index
            # generates 2 columns based on the parameters provided in the start and end columns 
            id_col, index_col, rows = child_table_generate(int(starter[j][parent_id_loc]), int(end[j][index_spot]))
            file_data.append([i for i in range(1, rows+1)]) # creates the column of id's dependent on the length of the random column lengths
            file_data.append(id_col)
            file_data.append(index_col)
            rowStart = 3 # number that for loop starts at because this takes care of the first 3 rows 
        except:
            rows = int(end[j][0]) # gets the end number saying how many rows
            file_data.append([i for i in range(1, rows+1) ]) # creates a column based on how many rows user wants
            rowStart = 1 # this takes care of the first row so we skip it
        
        for i in range(rowStart,len(header[j])): # loop through each column and create the array that will have the random data

            # Call necessary methods to get desire output       
            if(columnDataType[j][i].lower() == 'int'): # this is a range 
                min = int(starter[j][i])
                max = int(end[j][i])
                file_data.append(fake_data(columnDataType[j][i], rows, min=min, max=max, uniqueCell=unique[j][i].lower()))

            elif(columnDataType[j][i].lower() == 'bool'):
                file_data.append(fake_data(columnDataType[j][i], rows))

            elif(columnDataType[j][i].lower() == 'input'): # this is related to the list provided by the user
                file_data.append(fake_data_uploaded(starter[j][i].split(','), rows))

            elif(columnDataType[j][i].lower() == 'string'): # strings are associated with different calls related to the content column
                file_data.append(fake_data(columnDataType[j][i], rows, contentCell=starter[j][i].lower(), uniqueCell=unique[j][i].lower()))

            elif(columnDataType[j][i].lower() == 'timestamp'): # separate dates and then call the method to generate the dates
                year, month, day = map(int, starter[j][i].split('/')) # split the data based on slashes in the date
                startDate = datetime.datetime(year, month, day)
                year, month, day = map(int, end[j][i].split('/'))
                endDate = datetime.datetime(year, month, day)
                if(unique[j][i].lower()=='consecutive'): 
                    if((endDate - startDate).days < rows): # if the number of days between the 2 dates is less than the number of rows quit
                        print("Number of days is less than desired amount of rows for consecutive dates!")
                        quit()
                    file_data.append(consec_datetimes(startDate, rows))
                else: file_data.append(fake_data(columnDataType[j][i], rows, startDate, endDate, uniqueCell=unique[j][i].lower()))

            elif(columnDataType[j][i].lower() == 'date'): #separate dates and then call the method to generate the dates
                year, month, day = map(int, starter[j][i].split('/'))
                startDate = datetime.datetime(year, month, day)
                year, month, day = map(int, end[j][i].split('/'))
                endDate = datetime.datetime(year, month, day)
                if(unique[j][i].lower()=='consecutive'): 
                    if((endDate - startDate).days < rows): 
                        print("Number of days is less than desired amount of rows for consecutive dates!")
                        quit()
                file_data.append(fake_data(columnDataType[j][i], rows, startDate, endDate, uniqueCell=unique[j][i].lower()))
            else:
                continue # other cases have already been taken care of in the try catch and do not need to be done in this for loop
        all_data = list(zip(*file_data)) #zips the whole file so that all the column arrays turn into rows
        df = pd.DataFrame(all_data) # inserts the zipped array into data frame
        df.to_csv(f"{table_name[j]}.csv", index=False, header=header[j], encoding='utf-8-sig') # writes whole file to csv
        print(f"Data generated! Check your working directory for the file {table_name[j]}.csv")

# global variables
header = [] # column names
columnDataType = [] 
unique = []
starter = []
end = []

def parse_data():
    global table_name, header, columnDataType, unique, starter, end, data
    config = configparser.ConfigParser()
    config.read('data_configurator.ini', encoding='utf-8-sig') # read the config file
    # take all the data from the csv file and put it into arrays to use later
    data = pd.read_csv(config['Input Table']['file'], encoding='utf-8-sig')
    table_name = np.array(data['table'].values)
    header = np.array(data['column'].values)
    columnDataType = np.array(data['data_type'].values)
    unique = np.array(data['unique'].values)
    starter = np.array(data['start'].values)
    end = np.array(data['end'].values)

    # finds where all the nans are in a file and provides it in a list format
    nans_in_file = np.where(pd.isna(table_name))[0].tolist()

    # use the nans_in_file to split the array and make a new list filled with lists of the split data
    table_name = np.split(table_name, nans_in_file)
    table_name = [table[1] for table in table_name]

    header = np.split(header, nans_in_file)
    header = [element.tolist() for element in header]

    columnDataType = np.split(columnDataType, nans_in_file)
    columnDataType = [element.tolist() for element in columnDataType]

    unique = np.split(unique, nans_in_file)
    unique = [element.tolist() for element in unique]

    starter = np.split(starter, nans_in_file)
    starter = [element.tolist() for element in starter]

    end = np.split(end, nans_in_file)
    end = [element.tolist() for element in end]

    #get rid of the nans in the first spot of each element except the first one
    for i in range(1,len(header)):
        header[i] = header[i][1:]
        columnDataType[i] = columnDataType[i][1:]
        unique[i] = unique[i][1:]
        starter[i] = starter[i][1:]
        end[i] = end[i][1:]


def main():
    print("The program will take a couple seconds to generate the data please wait")
    #try:
    parse_data()
    create_csv()
    # except Exception as Argument:
    #     print("An error has occured, please check the working directing for the error file to see what the error was")
    #     f = open("error_file.txt", "w")
    #     f.write(str(Argument))
    #     f.close()

    

if __name__ == "__main__":
    main()