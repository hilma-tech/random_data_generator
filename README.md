# Random Data Generator

PROGRAM RUNS ONCE THE EXE IS CLICKED DO NOT CLOSE THE CMD WINDOW

Open the "dist" file and run the application OR make the python environment and run the python program with the config file

Create a csv file in the format:

table | column | date_type | unique | start | end 
----- | ------ | --------- | ------ | ----- | --- 
*table name* | *column name* | *int, string, timestamp, input, bool, date* | *running, yes, no, consecutive, parent_id,index* | *name, list, uuid, start date, start range* | *end date, end range* |
*table name* | *column name* | *int, string, timestamp, input, bool, date* | *running, yes, no, consecutive, parent_id,index* | *name, list, uuid, start date, start range* | *end date, end range* |

**Some notes on usage**
1. When making parent_id and index columns make sure they are next to eachother since they will be generated as the second and third row
2. When making a running id make sure to use a range i.e 1 - 10 (example in the sheets provided)
3. When making multiple tables in the csv file make a space between tables (example in the sheets provided)

Make as many columns as you need and write as many tables as you need

Once the csv is created put the exact file location into the config file and then run the program and check the working directory for the newly created csv file which is called {table name}.csv

**Make a copy of the Google Sheet**
[Link](shorturl.at/jlqWX) to make own csv file 

Once csv file is made download it as a csv file and put the path to the file in the config file and run the program
Check the working directory once the program runs to see the files

**Errors may include**: 
1. Range of dates chosen is to small to be consecutive for given amount of rows
2. If unique is chosen and there are not enough unique values that can be generated in the row count
3. Data was not put in properly

