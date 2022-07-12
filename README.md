# Random Data Generator

Create a csv file in the format:

table | column | date_type | unique | content 
----- | ------ | --------- | ------ | ------- 
*table name* | *column name* | *int, string, timestamp or input* | *running, yes, no* | *range, name, list, uuid, timestamp, date*
*table name* | *column name* | *int, string, timestamp or input* | *running, yes, no* | *range, name, list, uuid, timestamp, date*

Make as many columns as you need and write as many tables as you need

Once the csv is created put the exact file location into the config file and then run the program and check the working directory for the newly created csv file which is called {table name}.csv

Link to make own csv file
https://docs.google.com/spreadsheets/d/1qrj5qgR5Nt9fVzN4rNuI6r_-CUFUxOiYcbjLMKsKC5Y/edit?usp=sharing

Once csv file is made download it as a csv file and put the path to the file in the config file and run the program
Check the working directory once the program runs to see the files

Errors may include: range of dates chosen is to small to be consecutive for given amount of rows
If unique is chosen and there are not enough unique values that can be generated in the row count
Data was not put in properly
