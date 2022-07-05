import pandas as pd
from functools import partial
import datetime
from faker import Faker
import configparser
from faker.providers import BaseProvider

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

        # Dictionary that holds possible inputs from the user and makes them unique depending on if the user wants unique values
        switcher = {
            "int": partial(fake.unique.random_int, min, max) if uniqueCell=="yes" else partial(fake.random_int, min, max),
            "uuid": fake.unique.uuid4 if uniqueCell=="yes" else fake.uuid4,
            "date between": partial(fake.unique.date_between, startDate, endDate) if uniqueCell=="yes" else partial(fake.date_between, startDate, endDate), #date_between
            "timestamp": partial(fake.unique.date_time_between, startDate, endDate) if uniqueCell=="yes" else partial(fake.date_time_between, startDate, endDate),
            "name": fake.first_name, #first_name
        }
        
        #Create fake data using faker 
        temp_data = []
        typeNeeded = switcher.get(dataType, switcher.get(contentCell)) # get the value and if its a string get the value from the content array
        for _ in range(rows): 
            if callable(typeNeeded): # check if the value in the dictionary is callable and then call the fucntion
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
    
    df = pd.DataFrame(list()) # Create a new csv file that will contain the randomly generated data 
    df.to_csv(f"{table_name}.csv")

    file_data = []

    standardized = [ element.replace(' ', '') for element in content ] #standardize the cells to make sure nothing extra
    
    for i in range(len(header)):

        #Call necessary methods to get desire output
        if(unique[i].lower() == 'running'): # this is generally an id listing how many rows there are
            min, rows = map(int, standardized[i].split("-"))
            file_data.append([i for i in range(1, rows+1) ])
            
        elif(columnDataType[i].lower() == 'int'): # this is a range 
            min, max = map(int, standardized[i].split("-"))
            file_data.append(fake_data(columnDataType[i], rows, min=min, max=max))

        elif(columnDataType[i].lower() == 'input'): # this is related to the list provided by the user
            file_data.append(fake_data_uploaded(standardized[i].split(','), rows))

        elif(columnDataType[i].lower() == 'string'): # strings are associated with different calls related to the content column
            file_data.append(fake_data(columnDataType[i], rows, contentCell=content[i]) )

        elif(columnDataType[i].lower() == 'timestamp'): #separate dates and then call the method to generate the dates
            start, end = standardized[i].split('-')
            year, month, day = map(int, start.split('/'))
            startDate = datetime.datetime(year, month, day)
            year, month, day = map(int, end.split('/'))
            endDate = datetime.datetime(year, month, day)
            file_data.append(fake_data(columnDataType[i], rows, startDate, endDate))

    all_data = list(zip(*file_data)) #zips the whole file so that all the column arrays turn into rows
    df = pd.DataFrame(all_data) # inserts the zipped array into data frame
    df.to_csv(f"{table_name}.csv", index=False, header=header) # writes whole file to csv


# global variables
header = [] # column names
columnDataType = [] 
unique = []
content = []

def parse_data():
    global table_name, header, columnDataType, unique, content
    config = configparser.ConfigParser()
    config.read('data_configurator.ini') # read the config file
    # take all the data from the csv file and put it into arrays to use later
    data = pd.read_csv(config['Input Table']['file'])
    table_name = data['table'].values[0]
    header = data['column'].values
    columnDataType = data['data_type'].values
    unique = data['unique'].values
    content = data['content/range'].values
    
def main():
    parse_data()
    create_csv()
    print(f"Data generated! Check your working directory for the file {table_name}.csv!")


if __name__ == "__main__":
    main()